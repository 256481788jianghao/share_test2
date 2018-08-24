import pandas as pd
import tushare as ts
import os
import matplotlib.pyplot as plt
import datetime
import math
import tensorflow as tf
import numpy as np
import random

baseDir = './database2'
todaytime = datetime.datetime.now()
today_str = todaytime.strftime('%Y_%m_%d')
stock_base_info_filename = baseDir+"/"+"baseInfo_"+today_str+".csv"
stock_base_info = pd.read_csv(stock_base_info_filename,encoding='utf-8',index_col=0)


class StockData:
    def __init__(self,codeStr):
        self.codeStr = codeStr
        self.data = None
        data_filename = baseDir+'/'+self._getCodeBySymbol(self.codeStr)+'.csv'
        if os.path.exists(data_filename):
            self.data = pd.read_csv(data_filename,encoding='utf-8',index_col=0)
        else:
            print(data_filename+' not exists')

    def _getCodeBySymbol(self,codeStr):
        code_int = int(codeStr)
        codeR = stock_base_info[stock_base_info.symbol == code_int].ts_code.iloc[0]
        return codeR

class NetWork:
    def __init__(self,sizes):
        self.writer = tf.summary.FileWriter('D:/TensorBoard/test')
        self.input_data = tf.placeholder(dtype='float',name='input_data')
        self.out_data = tf.placeholder(dtype='float',name='out_data')
        self.sizes = sizes
        self.layerNum = len(self.sizes)
        self.Ws = []
        self.Bs = []
        self.Zs = []
        self.As = []
        if self.layerNum < 3:
            print('DNN must have inputlayer hiddenlayer and outputlayer,but layerNum < 3')
                    

    def _input_layer_fun(self,in_data):
        return in_data
    
    def _hidden_layer_fun(self,in_data):
        return tf.sigmoid(in_data)

    def _output_layer_fun(self,in_data):
        return in_data

    def forward(self,input_data):
        for i in range(self.layerNum):
            if i == 0:
                with tf.name_scope('input_layer'):
                    self.Ws.append(tf.Variable(tf.eye(self.sizes[i]),name='input_w'))
                    self.Bs.append(tf.Variable(tf.zeros([1,self.sizes[i]]),name='input_b'))
                    mul_ans = tf.matmul(input_data,self.Ws[i],name='mul'+str(i))
                    add_ans = tf.add(mul_ans,self.Bs[i],name='add'+str(i))
                    self.Zs.append(add_ans)
                    self.As.append(self._input_layer_fun(add_ans))
            elif i > 0 and i < self.layerNum -1:
                with tf.name_scope('hidden_layer_'+str(i)):
                    self.Ws.append(tf.Variable(tf.random_normal([self.sizes[i-1],self.sizes[i]]),name='hidden_w'+str(i)+str(i+1)))
                    self.Bs.append(tf.Variable(tf.random_normal([1,self.sizes[i]]),name='hidden_b'+str(i)))
                    mul_ans = tf.matmul(self.As[i-1],self.Ws[i],name='mul'+str(i))
                    add_ans = tf.add(mul_ans,self.Bs[i],name='add'+str(i))
                    self.Zs.append(add_ans)
                    self.As.append(self._hidden_layer_fun(add_ans))
            else:
                with tf.name_scope('output_layer'):
                    self.Ws.append(tf.Variable(tf.random_normal([self.sizes[i-1],self.sizes[i]]),name='output_w'))
                    self.Bs.append(tf.Variable(tf.random_normal([1,self.sizes[i]]),name='output_b'))
                    mul_ans = tf.matmul(self.As[i-1],self.Ws[i],name='mul'+str(i))
                    add_ans = tf.add(mul_ans,self.Bs[i],name='add'+str(i))
                    self.Zs.append(add_ans)
                    self.As.append(self._output_layer_fun(add_ans))
                
    def run(self):
        forward_handle = self.forward(self.input_data)
        init_variable = tf.global_variables_initializer()
        with tf.Session() as sess:
            sess.run(init_variable)
            self.writer.add_graph(sess.graph)
            self.writer.close()


netWork = NetWork([15,100,55,4])
netWork.run()
