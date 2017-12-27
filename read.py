import pandas as pd
import tushare as ts
import os
import matplotlib.pyplot as plt

baseDir = './database'

def readBaseInfo():
    return pd.read_csv(baseDir+"/baseInfo.csv",encoding='utf-8')

def readData(codeStr,startDate=None,endDate=None):
    if not os.path.exists(baseDir+'/'+codeStr+'.csv'):
        print(baseDir+'/'+codeStr+'.csv not exists')
        return pd.DataFrame()
    
    d = pd.read_csv(baseDir+'/'+codeStr+'.csv',encoding='utf-8')
    if startDate != None:
        d = d[d.datetime >= startDate]
    if endDate != None:
        d = d[d.datetime <= endDate]
    return d

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

ans_list = []
for code in baseInfo.codeStr:
    d = readData(code,startDate='2017-12-21',endDate='2017-12-21')
    if not d.empty:
        ans_list.append(d)
data_all = pd.concat(ans_list)
data_all = data_all[(data_all.high-data_all.open)/data_all.open > 0.09]
print(pd.concat([baseInfo.set_index('code'),data_all.set_index('code')],axis=1,join='inner').timeToMarket)

    
'''
datetime
code
open
close
high
low
vol    成交量(手)
amount 成交额
ave    平均价


data = pd.read_csv('./database.csv')
data['ave'] = data['amount']/data['vol']/100
ans_data = data[data.code == 601878]
#ans_data = data[(data.code == 2)]
ans_data['vol_un'] = ans_data['vol']/ans_data['vol'].iloc[0]
ans_data['amount_un'] = ans_data['amount']/ans_data['amount'].iloc[0]
print(ans_data)
#plt.plot(ans_data.index,ans_data['close'],'r')
#plt.plot(ans_data.index,ans_data['ave'],'b')
plt.show()
'''
