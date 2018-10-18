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
 
orders = getStockAdjust('601878','20160901','20180907')
data_adj = pd.read_sql(orders,sql_conn)
orders = getStock('601878','20160901','20180907')
data = pd.read_sql(orders,sql_conn)
orders = getStockBasic('601878','20160901','20180907')
databasic = pd.read_sql(orders,sql_conn)
print(databasic.turnover_rate*databasic.free_share)
print(data.vol)

sql_conn.close()
