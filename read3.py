import pandas as pd
import tushare as ts
import os
import matplotlib.pyplot as plt
import datetime
import math
import tensorflow as tf
import numpy as np
import random
import sqlite3

sql_conn = sqlite3.connect('database3.db')
def getOneStock(codeStr,dateStr):
    return 'select * from stock_'+dateStr+' where ts_code like "'+codeStr+'%"'

def getOneStockAdjust(codeStr,dateStr):
    return 'select * from stock_adjust_'+dateStr+' where ts_code like "'+codeStr+'%"'

def getOneStockBasic(codeStr,dateStr):
    return 'select * from stock_basic_'+dateStr+' where ts_code like "'+codeStr+'%"'


def getTradeDate(start_date,end_date):
    return pd.read_sql('select * from trade_cal where is_open = 1 and cal_date >='+start_date+' and cal_date <= '+end_date,sql_conn)

def getStock(codeStr,start_date,end_date):
    trade_cal_data = getTradeDate(start_date,end_date)
    trade_cal_data_len = len(trade_cal_data)
    orders = ''
    for i in range(trade_cal_data_len):
        if i == trade_cal_data_len - 1:
            orders = orders+getOneStock(codeStr,trade_cal_data.cal_date.iloc[i])
        else:
            orders = orders+getOneStock(codeStr,trade_cal_data.cal_date.iloc[i])+' union all '
    return orders

def getStockAdjust(codeStr,start_date,end_date):
    trade_cal_data = getTradeDate(start_date,end_date)
    trade_cal_data_len = len(trade_cal_data)
    orders = ''
    for i in range(trade_cal_data_len):
        if i == trade_cal_data_len - 1:
            orders = orders+getOneStockAdjust(codeStr,trade_cal_data.cal_date.iloc[i])
        else:
            orders = orders+getOneStockAdjust(codeStr,trade_cal_data.cal_date.iloc[i])+' union all '
    return orders

def getStockBasic(codeStr,start_date,end_date):
    trade_cal_data = getTradeDate(start_date,end_date)
    trade_cal_data_len = len(trade_cal_data)
    orders = ''
    for i in range(trade_cal_data_len):
        if i == trade_cal_data_len - 1:
            orders = orders+getOneStockBasic(codeStr,trade_cal_data.cal_date.iloc[i])
        else:
            orders = orders+getOneStockBasic(codeStr,trade_cal_data.cal_date.iloc[i])+' union all '
    return orders

pd.set_option('max_columns', 100)
 
orders = getStockAdjust('601878','20170101','20181019')
data_adj = pd.read_sql(orders,sql_conn)
orders = getStock('601878','20170101','20181019')
data = pd.read_sql(orders,sql_conn)
orders = getStockBasic('601878','20170101','20181019')
databasic = pd.read_sql(orders,sql_conn)
#print(databasic.turnover_rate*databasic.free_share)
#print(data)

big_trade = pd.DataFrame();
big_trade['date'] = ['20180112','20180515','20180627','20180703','20180706','20180712','20180717','20180807','20180809','20180926','20181015']
big_trade['price'] = [14.68,11.92,7.61,7.11,6.99,6.68,6.87,6.18,6.26,6.6,5.48]
big_trade['vol'] = [18.40,18.40,200,200,200,200,200,3662.67,1422.44,300,200]
print(big_trade)

p0 = data.pre_close.iloc[0]
p_mean = []
data_len = len(data)
for i in range(data_len):
    brate = 0
    bprice = 0
    date = data.trade_date[i]
    print(date)
    big_item = big_trade[big_trade.date == date]
    #print(big_item)
    if len(big_item) > 0:
        v = big_item.vol.iloc[0]
        #print(v)
        brate = (v / databasic.float_share.iloc[i])
        bprice = big_item.price.iloc[0]
        print(brate)
        print(bprice)
    rate = databasic.turnover_rate.iloc[i]/100
    p_mean.append(p0*(1-rate-brate)+data.low.iloc[i]*rate+bprice*brate)
    p0 = p_mean[-1]
data['p_mean'] = p_mean
#print(data)
data.loc[:,['close','p_mean']].plot()
plt.show()
sql_conn.close()
