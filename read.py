import pandas as pd
import tushare as ts
import os
import matplotlib.pyplot as plt
import datetime

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

def readSomeData(codes,startDate=None,endDate=None):
    if len(codes) == 0:
        return pd.DataFrame()
    ans_list = []
    for code in codes:
        d = readData(code,startDate=startDate,endDate=endDate)
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

baseInfo = baseInfo[baseInfo.days > 10]
#======================================================================================================

def computeData(data):
    data_g = data.groupby('code')
    def selfCompute(item):
        ans_dict = {}
        ans_dict['p_change'] = (item.close.max()-item.close.mean())/item.close.mean()
        return pd.Series(ans_dict)
    return data_g.apply(selfCompute)

def compute_pc_mean(data):
    ret = 0
    if not data.empty:
        cx_data = readSomeData(data.codeStr,'2017-12-01','2017-12-22')
        if not cx_data.empty:
            ans = computeData(cx_data)
            ret = ans.p_change.mean()
    return ret
            
def returnAns(items):
    ans_dict = {}
    cx_frame = items[items.days <=365]
    fcx_frame = items[items.days > 365]
    ans_dict['cx_len'] = len(cx_frame)
    ans_dict['fcx_len'] = len(fcx_frame)
    ans_dict['cx_pc_mean'] = compute_pc_mean(cx_frame)
    ans_dict['fcx_pc_mean'] = compute_pc_mean(fcx_frame)
    
    
    return pd.Series(ans_dict)
'''
ans_frame = baseInfo.groupby('industry').apply(returnAns)
print(ans_frame[(ans_frame.cx_len > 0) & (ans_frame.cx_pc_mean < ans_frame.fcx_pc_mean)])
'''
#================================================================================================
def pe_mean(item):
    ans_dict = {}
    pe_zero = item[item.pe <= 0.0]
    pe_h = item[item.pe > 0]
    pb_zero = item[item.pb <= 0.0]
    pb_h = item[item.pb > 0]
    #ans_dict['pe_zero_len'] = len(pe_zero)
    #ans_dict['pb_zero_len'] = len(pb_zero)
    #ans_dict['pe_h_len'] = len(pe_h)
    #ans_dict['pb_h_len'] = len(pb_h)
    ans_dict['pe_mean'] = pe_h.pe.mean()
    ans_dict['pb_mean'] = pb_h.pb.mean()
    return pd.Series(ans_dict)


ans_data = baseInfo.groupby('industry').apply(pe_mean)
print(ans_data.sort_values(by=['pb_mean']))

#==================================================================================
def my_test_1(item):
    ans_dict = {}
    data = readSomeData(item.codeStr,startDate='2017-12-01')
    if not data.empty:
        data_g = data.groupby('code')
        ans_dict['ch_max'] = data_g.apply(lambda x:x.close.std()/x.close.mean()).max()
        ans_dict['ch_min'] = data_g.apply(lambda x:x.close.std()/x.close.mean()).min()
        ans_dict['ch_mean'] = data_g.apply(lambda x:x.close.std()/x.close.mean()).mean()
    return pd.Series(ans_dict)
'''
ans_data = baseInfo.groupby('industry').apply(my_test_1)
print(ans_data.sort_values('ch_max'))
'''
#===================================================================================
def getB(code):
    data = readSomeData([code],startDate='2017-01-01')
    ans_dict = {}
    ans_dict['codeStr'] = code
    if not data.empty:
        data_s1 = data.shift(1)
        diff = (data_s1.high - data.open)/data.open
        diff_s = (data_s1.low - data.open)/data.open
        ans_dict['change_b'] = len(diff[diff > 5/1000.0])/len(diff)
        ans_dict['change_s_min'] = diff_s.min()
        ans_dict['change_s_mean'] = diff_s.mean()
        return pd.Series(ans_dict)
'''
ans = baseInfo.codeStr.apply(getB)
ans = ans.set_index(keys='codeStr')
baseInfo = baseInfo.set_index('codeStr')
baseInfo = pd.concat([baseInfo,ans],axis = 1)
print(baseInfo[baseInfo.change_b > 0.6])
'''

#==================================================================================
def my_test_2(data):
    ans_dict = {}
    my_acount_n = 0
    my_acount_price = 0
    data_len = len(data)
    for index in range(data_len):
        item = data.iloc[-index]
        if my_acount_n == 0:
            my_acount_price = item.open
            my_acount_n = 1000
        else:
            pass
    return pd.Series(ans_dict)
'''
print(my_test_2(readSomeData(['000002'],startDate='2017-01-01')))
'''
#===================================================================================

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





