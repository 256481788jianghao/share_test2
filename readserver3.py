import sqlite3
import tushare as ts
import pandas as pd
import os
import datetime

baseDir = './database2'

sql_conn = sqlite3.connect('database3.db')

for dateStr in ['20180904']:
    table_name = 'stock_'+dateStr
    table_adjust_name = 'stock_adjust_'+dateStr
    stockdata_filename = baseDir+'/stock_'+dateStr+'.csv'
    stockdata_adjust_filename = baseDir+'/stock_adjust_'+dateStr+'.csv'
    if os.path.exists(stockdata_filename):
        data = pd.read_csv(stockdata_filename,encoding='utf-8',index_col=0)
        print(data)
        data.to_sql(table_name,sql_conn)

input()
sql_conn.close()
