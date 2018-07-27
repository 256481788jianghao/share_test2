from readbaseInfo import *
import pandas as pd
import tushare as ts
import os
import matplotlib.pyplot as plt
import datetime
import math
import tensorflow as tf
import numpy as np

#用于存储单个股票数据的变量，防止重复读取
one_stack_data = {'code':-1,'data':None}

def SetOneData(codestr):
    one_stack_data['code'] = codestr
    one_stack_data['data'] = readData(codestr).loc[:,['open','close','high','low','vol','amount','tor']]

#得到以当前日期前N天基准，前before个交易日和后after个交易日的数据
def GetStockData(codestr,N,before = 5,after = 5):
    if one_stack_data['code'] != codestr:
        SetOneData(codestr)
    if N -1 < after:
        print('error:GetData N-1 < after');
        return None
    tmpData = one_stack_data['data']
    #归一化
    nclose = tmpData.iloc[N].close
    nvol = tmpData.iloc[N].vol
    namount = tmpData.iloc[N].amount
    ntor = tmpData.iloc[N].tor
    
    tmpData.loc[:,'open']  = tmpData.open/nclose
    tmpData.loc[:,'close'] = tmpData.close/nclose
    tmpData.loc[:,'high']  = tmpData.high/nclose
    tmpData.loc[:,'low']   = tmpData.low/nclose
    tmpData.loc[:,'vol']   = tmpData.vol/nvol
    tmpData.loc[:,'amount']   = tmpData.amount/namount
    tmpData.loc[:,'tor']   = tmpData.tor/ntor

    afterData = tmpData.iloc[N - after:N]
    beforeData = tmpData.iloc[N:N+before]
    return beforeData,afterData,nclose

#将pandas数据转换为训练数据,X为beforeData，Y如下定义：
# afterData中的high 比 nclose 高 p% 输出 [1,0,0]
# afterData中的low  比 nclose 低 p% 输出 [0,0,1]
# 其他输出 [0,1,0]
def GetNetWorkData(codestr,N,before = 5,after = 5,p=5):
    beforeData,afterData,nclose = GetStockData(codestr,N,before,after)
    
    x = np.reshape(beforeData.values,before*7)
    
    ph = afterData.high.max() - 1
    pl = afterData.low.min() - 1

    y = np.array([0,1,0])
    if ph*100 >= p :
        y = np.array([1,0,0])
    if pl*100 <= -p:
        y = np.array([0,0,1])
    return x,y
    


x,y = GetNetWorkData('300024',15)

print(y)
'''
code,代码
name,名称
industry,所属行业
area,地区
pe,市盈率
outstanding,流通股本(亿)
totals,总股本(亿)
totalAssets,总资产(万)
liquidAssets,流动资产
fixedAssets,固定资产
reserved,公积金
reservedPerShare,每股公积金
esp,每股收益
bvps,每股净资
pb,市净率
timeToMarket,上市日期
undp,未分利润
perundp, 每股未分配
rev,收入同比(%)
profit,利润同比(%)
gpr,毛利率(%)
npr,净利润率(%)
holders,股东人数
'''
'''
code,代码
        name,名称
        eps,每股收益
        eps_yoy,每股收益同比(%)
        bvps,每股净资产
        roe,净资产收益率(%)
        epcf,每股现金流量(元)
        net_profits,净利润(万元)
        profits_yoy,净利润同比(%)
        distrib,分配方案
        report_date,发布日期
'''
'''
code,代码
        name,名称
        roe,净资产收益率(%)
        net_profit_ratio,净利率(%)
        gross_profit_rate,毛利率(%)
        net_profits,净利润(万元)
        eps,每股收益
        business_income,营业收入(百万元)
        bips,每股主营业务收入(元)
'''
