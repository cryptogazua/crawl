import requests
from bs4 import BeautifulSoup
from steem import Steem
import time
import json

# 새글 q 검색어로 링크만 가져오기
def get_created_link(q):
    link_list = []
    r = requests.get("https://steemit.com/created/%s" % q)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.findAll('h2', {'class':'articles__h2 entry-title'})
    for link in links:
        a = link.find_all("a")
        link_list.append(a[0]['href'])
    return link_list

def get_post_from_link(link):
    link_split = link.split('/')
    steemit_id = link_split[2].replace('@','')
    permlink = link_split[3]
    return steemit_id, permlink

import findspark
findspark.init()

import pyspark
from pyspark.sql.session import SparkSession
sc = pyspark.SparkContext()
spark = SparkSession(sc)

from pyspark.sql import *
from pyspark.sql.functions import *

KEYWORDS = ('btc', 'etc', 'xrp', 'bch', 'eos')
NEEDED = ('author','permlink','last_update','id','category','title','body','created','net_votes')
def pub_steemit():
    links_list = []
    try:
        links_list = [(k, get_created_link(k)) for k in KEYWORDS]
    except Exception as e:
        print("links_list => " + e)

    for k, links in links_list:
        for link in links:
            steemit_id, permlink = get_post_from_link(link)
            try:
                s = Steem()
            except Exception as e:
                print("Steem() => " + e)
                continue
            post_dic = s.get_content(steemit_id, permlink)
            #print(steemit_id, permlink)
            #print(post_dic)
            dic = {}
            dic['keyword'] = k
            for field in NEEDED:
                if field in post_dic:
                    dic[field] = post_dic[field]
                    #dic[field] = post_dic[field].encode('utf-8') if type(post_dic[field]) is str else post_dic[field]
            d=[{'key':steemit_id, 'value':str(dic)}]
            df = spark.createDataFrame(d)
            df.write \
                .format("kafka") \
                .option("kafka.bootstrap.servers", "localhost:9092") \
                .option("topic", "steemit") \
                .save()

# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python
if __name__ == "__main__":
    start = time.time()
    while True:
        pub_steemit()
        #time.sleep(60.0 - ((time.time() - start) % 60.0) )
        time.sleep(1.0 - ((time.time() - start) % 1.0) )
