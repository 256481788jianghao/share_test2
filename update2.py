import tushare as ts
import pandas as pd
import os
import datetime


baseDir = './database2'
if not os.path.exists(baseDir):
    os.mkdir(baseDir)


ts.set_token('edd599506620c2fa4466f6ff765ff458d3dd894b136356c68b8baa32')
ts_api = ts.pro_api()

todaytime = datetime.datetime.now()
today_str = todaytime.strftime('%Y_%m_%d')



#get all stock code list
stock_base_info_filename = baseDir+"/"+"baseInfo_"+today_str+".csv"
stock_base_info = None
if not os.path.exists(stock_base_info_filename):
    stock_base_info_tmp = ts_api.stock_basic(list_status='L')
    stock_base_info_tmp.to_csv(stock_base_info_filename,encoding='utf-8')

stock_base_info = pd.read_csv(stock_base_info_filename,encoding='utf-8',index_col=0)

stock_len = len(stock_base_info)
stock_update_index = 0
for code in stock_base_info.ts_code:
    stock_update_index = stock_update_index + 1
    data_filename = baseDir+'/'+code+'.csv'
    data_need_update = False
    if os.path.exists(data_filename):
        data_tmp = pd.read_csv(data_filename,encoding='utf-8',index_col=0)
        data_time = datetime.datetime.strptime(str(data_tmp.trade_date.iloc[0]), "%Y%m%d")
        delta = todaytime - data_time
        if todaytime.weekday() < 5 and delta.days == 1 and todaytime.hour >= 23:
            data_need_update = True
        elif todaytime.weekday() < 5 and delta.days > 1:
            data_need_update = True
        elif todaytime.weekday() == 5 and delta.days > 1:
            data_need_update = True
        elif todaytime.weekday() == 6 and delta.days > 2:
            data_need_update = True
    else:
        data_need_update = True
    if data_need_update:
        data = ts_api.daily(ts_code=code,start_date='2016-1-1')
        data.to_csv(data_filename,encoding='utf-8')
        
    print(code+" "+str(stock_update_index)+"/"+str(stock_len))


'''
ts_code	str	股票代码
trade_date	str	交易日期
open	float	开盘价
high	float	最高价
low	float	最低价
close	float	收盘价
pre_close	float	昨收价
change	float	涨跌额
pct_change	float	涨跌幅
vol	float	成交量 （手）
amount	float	成交额 （千元）
'''
