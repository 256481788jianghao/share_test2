import redis
import tushare as ts
import pandas as pd
import os
import datetime
from io import StringIO

pool= redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)

r=redis.Redis(connection_pool=pool)

baseDir = './database2'

todaytime = datetime.datetime.now()
today_str = todaytime.strftime('%Y_%m_%d')
today_str2 = todaytime.strftime('%Y%m%d')

stock_trade_cal_filename = baseDir+"/"+"trade_cal_"+today_str+".csv"
stock_trade_cal_info = pd.read_csv(stock_trade_cal_filename,encoding='utf-8',index_col=0)

def getData(key):
    dataStr = pd.read_msgpack(r.get(key),encoding='utf-8')
    return dataStr
    
print(getData('stock_20180904'))
