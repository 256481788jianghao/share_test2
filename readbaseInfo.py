import pandas as pd
import tushare as ts
import os
import matplotlib.pyplot as plt
import datetime
import math

baseDir = './database'

def readBaseInfo():
    d = pd.read_csv(baseDir+"/baseInfo.csv",encoding='utf-8')
    return d[(d.holders > 0)]

def readData(codeStr,startDate=None,endDate=None,first=None):
    if not os.path.exists(baseDir+'/'+codeStr+'.csv'):
        print(baseDir+'/'+codeStr+'.csv not exists')
        return pd.DataFrame()
    
    d = pd.read_csv(baseDir+'/'+codeStr+'.csv',encoding='utf-8')
    if startDate != None:
        d = d[d.datetime >= startDate]
    if endDate != None:
        d = d[d.datetime <= endDate]
    if first != None:
        d = d.head(first)
    return d

def readSomeData(codes,startDate=None,endDate=None,first=None):
    if len(codes) == 0:
        return pd.DataFrame()
    ans_list = []
    for code in codes:
        d = readData(code,startDate=startDate,endDate=endDate,first=first)
        if not d.empty:
            ans_list.append(d)
    if len(ans_list) == 0:
        return pd.DataFrame()
    return pd.concat(ans_list)
    
def readAllData(startDate=None,endDate=None):
    return readSomeData(baseInfo.codeStr,startDate,endDate)
#====================================================================================================    
baseInfo = readBaseInfo()

def changeCodeToStr(code):
    codeStr = str(code)
    codeStr_len = len(codeStr)
    if codeStr_len < 6:
        sublen = 6-codeStr_len
        for i in range(sublen):
            codeStr = '0'+codeStr;
    return codeStr

baseInfo['codeStr'] = baseInfo.code.apply(changeCodeToStr)
baseInfo = baseInfo[baseInfo.timeToMarket != 0]

time_now = datetime.datetime.now()
def computeDays(date):
    t = datetime.datetime.strptime(str(date),'%Y%m%d')
    delta = time_now - t
    return delta.days

baseInfo['days'] = baseInfo.timeToMarket.apply(computeDays)

baseInfo = baseInfo[baseInfo.days >= 365*3]

#=====================================================================================================
report_year = 2017
report_data_list = []
report_data_list.append(pd.read_csv(baseDir+"/reportdata_"+str(report_year)+"_4.csv",encoding='utf-8'))
report_data_list.append(pd.read_csv(baseDir+"/reportdata_"+str(report_year - 1)+"_4.csv",encoding='utf-8'))
report_data_list.append(pd.read_csv(baseDir+"/reportdata_"+str(report_year - 2)+"_4.csv",encoding='utf-8'))
#=====================================================================================================
profit_year = 2017
profit_data_list = []
profit_data_list.append(pd.read_csv(baseDir+"/profitdata_"+str(profit_year)+"_4.csv",encoding='utf-8'))
profit_data_list.append(pd.read_csv(baseDir+"/profitdata_"+str(profit_year - 1)+"_4.csv",encoding='utf-8'))
profit_data_list.append(pd.read_csv(baseDir+"/profitdata_"+str(profit_year - 2)+"_4.csv",encoding='utf-8'))
#======================================================================================================
