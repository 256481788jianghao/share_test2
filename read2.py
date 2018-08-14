from readbaseInfo import *
import pandas as pd
import tushare as ts
import os
import matplotlib.pyplot as plt
import datetime
import math
import tensorflow as tf
import numpy as np
import random

#用于存储单个股票数据的变量，防止重复读取
one_stack_data = {'code':-1,'data':None}

def SetOneData(codestr):
    one_stack_data['code'] = codestr
    one_stack_data['data'] = readData(codestr).loc[:,['open','close','high','low','vol','amount','tor']]

#得到以当前日期前N天基准，前before个交易日和后after个交易日的数据
def GetStockData(codestr,N,before = 5,after = 5):
    if one_stack_data['code'] != codestr:
        SetOneData(codestr)
    if N < after:
        print('error:GetStockData N < after');
        return None
    tmpData = one_stack_data['data'].copy()
    tmpDataLen = len(tmpData)
    if tmpDataLen < N+before:
        print('error:GetStockData tmpDataLen < N+before')
        return None
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
# afterData中的high 比 nclose 高 pp% and afterData中的low  比 nclose up -pn% 输出 [1,0,0,0]
# high up low down [0,1,0,0]; high down low up [0,0,1,0];high down low down [0,0,0,1]
def GetNetWorkData(codestr,N,before = 5,after = 5,pp=5,pn=5):
    beforeData,afterData,nclose = GetStockData(codestr,N,before,after)
    #print(beforeData)

    x = np.reshape(beforeData.values,before*7)
    #print(x)
    
    ph = afterData.high.max() - 1
    pl = afterData.low.min() - 1

    y = None
    hflag = ph*100 >= pp
    lflag = pl*100 >= -pn
    if hflag and lflag:
        y = np.array([1,0,0,0])
    elif hflag and not lflag:
        y = np.array([0,1,0,0])
    elif not hflag and lflag:
        y = np.array([0,0,1,0])
    else:
        y= np.array([0,0,0,1])
    return x,y
    
def GetNetWorkDataNum(codestr,Num=100,before = 5,after = 5,pp=5,pn=5):
    if one_stack_data['code'] != codestr:
        SetOneData(codestr)
    maxLen = len(one_stack_data['data'])
    if maxLen < before+after:
        print('GetNetWorkDataNum error maxLen < before+after')
        return None,None
    if Num > maxLen - before - after:
        Num = maxLen - before - after
    xList = []
    yList = []
    for i in range(0,Num):
        rIndex = random.randint(after+1,maxLen-before)
        x,y = GetNetWorkData(codestr,rIndex,before,after,pp,pn)
        xList.append(x)
        yList.append(y)
    return np.mat(xList),np.mat(yList)


class NetWork:
    def __init__(self,size):
        self.layerNum = len(size)
        self.size = size
        self.Ws = []
        self.Bs = []
        self.Zs = []
        self.As = []
        self._make_mid_layers()
        
    def _make_mid_layers(self):
        for i in range(self.layerNum-1):
            w = tf.Variable(tf.random_normal(shape=[self.size[i],self.size[i+1]]),name='W'+str(i+1)+str(i+2))
            b = tf.Variable(tf.random_normal(shape=[1,self.size[i+1]]),name='B'+str(i+2))
            self.Ws.append(w)
            self.Bs.append(b)
            
    def _mid_fun(self,in_data):
        return in_data

    def _out_fun(self,in_data):
        return in_data

    def forward(self,x):
        self.Zs.append(tf.matmul(x,self.Ws[0])+self.Bs[0])
        self.As.append(self._mid_fun(self.Zs[0]))
        for i in range(self.layerNum-2):
            self.Zs.append(tf.matmul(self.As[i],self.Ws[i+1])+self.Bs[i+1])
            if i == self.layerNum - 3:
                self.As.append(self._out_fun(self.Zs[-1]))
            else:
                self.As.append(self._mid_fun(self.Zs[-1]))
        return self.As[-1]


network = NetWork([35,15,4])
            
x,y = GetNetWorkDataNum('300024',Num=5)

input_data = tf.placeholder(dtype='float',shape=[None,5*7],name='input_data')
out_data = tf.placeholder(dtype='float',shape=[None,5*7],name='out_data')

init_variable = tf.global_variables_initializer()
forward_out = network.forward(input_data)

with tf.Session() as sess:
    sess.run(init_variable)
    sess.run(forward_out,feed_dict={input_data:x})
    writer = tf.summary.FileWriter('D:/TensorBoard/test',sess.graph)
    writer.close()

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
