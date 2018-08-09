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
    if N -1 < after:
        print('error:GetStockData N-1 < after');
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
# afterData中的high 比 nclose 高 pp% and afterData中的low  比 nclose up -pn% 输出 [1,0,0,0]
# high up low down [0,1,0,0]; high down low up [0,0,1,0];high down low down [0,0,0,1]
def GetNetWorkData(codestr,N,before = 5,after = 5,pp=5,pn=5):
    beforeData,afterData,nclose = GetStockData(codestr,N,before,after)
    
    x = np.reshape(beforeData.values,before*7)
    
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
        self.level_num = len(size)
        self.size = size
        self.bais = [tf.Variable(tf.zeros([1,x])) for x in size]
        self.Ws = []
        self.Ws.append(tf.Variable(tf.zeros([size[0],size[0]])))
        self.Ws.extend([tf.Variable(tf.zeros([m,n]))  for m,n in zip(size[:-1],size[1:])])
        self.Zs = []
        self.As = []
        
    def sigmoid(self,z):
        return 1.0/(1.0+tf.exp(-z))

    def output_fun(self,z):
        return self.sigmoid(z)

    def forward(self,in_data):
        self.Zs.append(tf.matmul(in_data,self.Ws[0])+self.bais[0])
        self.As.append(self.output_fun(self.Zs[0]))
        for i in range(1,self.level_num):
            self.Zs.append(tf.matmul(self.As[i-1],self.Ws[i])+self.bais[i])
            self.As.append(self.output_fun(self.Zs[i]))
        return self.As[-1]

    def softmax(self,out_data):
        return tf.nn.softmax(logits=out_data)

    def cost_fun(self,y,out_data):
        return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=out_data,logits=y))

    def train_fun(self,dd,cost_):
        return tf.train.GradientDescentOptimizer(dd).minimize(cost_)

def accuracy(out_data,y):
    out_data_max = tf.argmax(out_data,axis=1)
    y_max = tf.argmax(y,axis=1)
    r_sum = tf.reduce_sum(tf.equal(out_data_max,y_max))


network = NetWork([35,7,4])

in_data = tf.placeholder('float')
out_data = tf.placeholder('float')

init = tf.global_variables_initializer()
y_tmp_ = network.forward(in_data)
y_ = network.Zs[-1]
#y_max_list = tf.argmax(y_,axis=1)
softmax_out = network.softmax(y_)
hcost_ = out_data*tf.log(softmax_out)
cost_ = network.cost_fun(y_,out_data)
train_ = network.train_fun(0.001,cost_)

with tf.Session() as sess:
    sess.run(init)
    for i in range(0,10):
        x,y = GetNetWorkDataNum('300024',Num=5)
        #print(y)
        sess.run(train_,feed_dict={in_data:x,out_data:y})
        #print(sess.run(hcost_,feed_dict={in_data:x,out_data:y}))
        print('cost=%f'%sess.run(cost_,feed_dict={in_data:x,out_data:y}))
        y_out = sess.run(y_,feed_dict={in_data:x})
        equal_list = np.argmax(y,axis=1).T == np.argmax(y_out,axis=1)
        #print(equal_list)
        print(np.sum(equal_list)/equal_list.shape[1])


    
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
