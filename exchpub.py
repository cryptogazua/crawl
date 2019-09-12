# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import json
from copy import deepcopy

URL_TEMPL = "https://api.bithumb.com/public/ticker/%s"
URL_ALL = "https://api.bithumb.com/public/ticker/ALL"

class Bithumb:
    def __init__(self, currency=""):
        self.url = URL_TEMPL % currency
        self.quote = {} 

    def set_currency(self, currency):
        self.url = URL_TEMPL % currency

    def get_ohlcs(self, data):
        quote = {}
        try:
            quote['open'] = float(data['opening_price'])
            quote['high'] = float(data['max_price'])
            quote['low'] = float(data['min_price'])
            quote['close'] = float(data['closing_price'])
            quote['change'] = quote['close'] - quote['open']
            if not quote['open']:
                # print("open=0.0", str(quote))
                quote['rate'] = 0.0
            else:
                quote['rate'] = quote['change'] / quote['open'] * 100.0
        except Exception as e:
            print("get_ohlcs error", str(e))
            quote = {}
        return quote

    def get_quote(self):
        quote = {}
        res = requests.get(self.url)
        quote_json = json.loads(res.text)
        if 'status' in quote_json and quote_json['status'] == '0000':
            quote = self.get_ohlcs(quote_json['data'])
        return quote

    def get_all_quote(self):
        quote = {}
        # https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url
        try:
            res = requests.get(URL_ALL)
            quote_json = json.loads(res.text)
        except Exception as e:
            print("get_all_quote error", str(e))
            return quote
        if 'status' in quote_json and quote_json['status'] == '0000':
            for currency in quote_json['data']:
                if currency == 'date':
                    continue
                quote[currency] = self.get_ohlcs(quote_json['data'][currency])
        return quote

    def get_all_updates(self):
        quote = self.get_all_quote()
        up_quote = {}
        # print("1 - len(self.quote) = %d" % len(self.quote))
        if len(self.quote) > 0:
            for currency in quote:
                if currency in self.quote:
                    lqc = self.quote[currency]
                    cqc = quote[currency]
                    if lqc['close'] != cqc['close']:
                        up_quote[currency] = cqc
        else:
            # print("up_quote")
            up_quote = quote
        self.quote = deepcopy(quote)
        # print("2 - len(self.quote) = %d" % len(self.quote))
        return up_quote

import findspark
findspark.init()

import pyspark
from pyspark.sql.session import SparkSession
sc = pyspark.SparkContext()
spark = SparkSession(sc)

from pyspark.sql import *
from pyspark.sql.functions import *


# KEYWORDS = ('btc', 'etc', 'xrp', 'bch', 'eos')
def pub_steemit(exch):
    quotes = exch.get_all_quote() # 모든 시세 처리
    #quotes = exch.get_all_updates() # 현재가가 갱신되는 시세만 처리

    quote_list = []
    for c in quotes:
        # https://stackoverflow.com/questions/13890935/does-pythons-time-time-return-the-local-or-utc-timestamp
        quotes[c]['eventTime'] = int(time.time())
        quote_dic = {'key':c, 'value':str(quotes[c])}
        quote_list.append(quote_dic)

    if len(quote_list) == 0:
        return

    df = spark.createDataFrame(quote_list)
    df.write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "bithumb") \
        .save()


# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python
if __name__ == "__main__":
    start = time.time()
    exch = Bithumb()
    while True:
        pub_steemit(exch)
        time.sleep(1.0 - ((time.time() - start) % 1.0) )
