import requests
from bs4 import BeautifulSoup
from steem import Steem

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

if __name__ == "__main__":
    links = get_created_link('eos')
    for link in links:
        steemit_id, permlink = get_post_from_link(link)
        s = Steem()
        post_dic = s.get_content(steemit_id, permlink) 
        print(steemit_id, permlink)
        print(post_dic)
