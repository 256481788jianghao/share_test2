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

class NetWorkDNN:
    def __init__(self,sizes):
        self,sizes = sizes
        self.layerNum = len(sizes)
        self.Ws = []
        self.Bs = []
        if self.layerNum < 3:
            print('DNN must have inputlayer hiddenlayer and outputlayer,but layerNum < 3')
        else:
            with tf.name_scope('input_layer'):
                self.Ws.append(tf.Varaible(tf.eyes(shape=[sizes[0],sizes[0]],name='input_w')))


StockData('4')
