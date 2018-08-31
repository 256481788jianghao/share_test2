import redis
import tushare as ts
import pandas as pd
import os
import datetime

pool= redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)

r=redis.Redis(connection_pool=pool)

baseDir = './database2'

todaytime = datetime.datetime.now()
today_str = todaytime.strftime('%Y_%m_%d')
today_str2 = todaytime.strftime('%Y%m%d')

stock_trade_cal_filename = baseDir+"/"+"trade_cal_"+today_str+".csv"
stock_trade_cal_info = pd.read_csv(stock_trade_cal_filename,encoding='utf-8',index_col=0)


def get_stockdata_by_date(item):
    if item.is_open == 1:
        dateStr = str(item.cal_date)
        stockdata_filename = baseDir+'/stock_'+dateStr+'.csv'
        stockdata_adjust_filename = baseDir+'/stock_adjust_'+dateStr+'.csv'
        if os.path.exists(stockdata_filename):
            try:
                data = pd.read_csv(stockdata_filename,encoding='utf-8',index_col=0)
                #dataStr = data.to_json()
                #print(dataStr)
                key = 'stock_'+dateStr
                r.set(key,data)
                print(stockdata_filename+' finish')
            except Exception as e:
                print(e)
        if os.path.exists(stockdata_adjust_filename):
            try:
                data_adjust = pd.read_csv(stockdata_adjust_filename,encoding='utf-8',index_col=0)
                key = 'stock_adjust_'+dateStr
                r.set(key,data)
                print(stockdata_adjust_filename+' finish')
            except Exception as e:
                print(e)
            
stock_trade_cal_info.apply(get_stockdata_by_date,axis=1)
r.set('apple','a')
print(r.get('apple'))
