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
'''
连续三年净利润率大于 yoy_up or roe
'''

'''
report_yoy_up = 100
report_data_list_p = []
report_data_list_p.append(report_data_list[0][report_data_list[0].profits_yoy > report_yoy_up])
report_data_list_p.append(report_data_list[1][report_data_list[1].profits_yoy > report_yoy_up])
report_data_list_p.append(report_data_list[2][report_data_list[2].profits_yoy > report_yoy_up])
report_data_p_code = set(report_data_list_p[0].code) & set(report_data_list_p[1].code) & set(report_data_list_p[2].code)
print(report_data_p_code)

report_roe_up = 20
report_data_list_p = []
report_data_list_p.append(report_data_list[0][report_data_list[0].roe > report_roe_up])
report_data_list_p.append(report_data_list[1][report_data_list[1].roe > report_roe_up])
report_data_list_p.append(report_data_list[2][report_data_list[2].roe > report_roe_up])
report_data_p_code = set(report_data_list_p[0].code) & set(report_data_list_p[1].code) & set(report_data_list_p[2].code)

baseInfo_p_up = baseInfo[[x in report_data_p_code for x in baseInfo.code]]
print(baseInfo_p_up)
'''
#======================================================================================================
'''
连续三年净利润率大于 
'''
'''
s_roe = 30
profit_data_list_p = []
profit_data_list_p.append(profit_data_list[0][profit_data_list[0].net_profit_ratio > s_roe])
profit_data_list_p.append(profit_data_list[1][profit_data_list[1].net_profit_ratio > s_roe])
profit_data_list_p.append(profit_data_list[2][profit_data_list[2].net_profit_ratio > s_roe])
profit_data_p_code = set(profit_data_list_p[0].code) & set(profit_data_list_p[1].code) & set(profit_data_list_p[2].code)
'''
s_roe = 15
profit_data_list_p = []
profit_data_list_p.append(profit_data_list[0][profit_data_list[0].roe > s_roe])
profit_data_list_p.append(profit_data_list[1][profit_data_list[1].roe > s_roe])
profit_data_list_p.append(profit_data_list[2][profit_data_list[2].roe > s_roe])
profit_data_p_code = set(profit_data_list_p[0].code) & set(profit_data_list_p[1].code) & set(profit_data_list_p[2].code)

baseInfo_p_up = baseInfo[[x in profit_data_p_code for x in baseInfo.code]]
baseInfo_last_year = pd.merge(baseInfo,profit_data_list[0],on='code')
#print(baseInfo_last_year)

def dealdata1(items):
    ans_dict = {}
    ans_dict['num'] = len(items)
    #ans_dict['mean_roe'] = items.roe.mean()
    return pd.Series(ans_dict)
#print(baseInfo_p_up.groupby('industry').apply(dealdata1))
#print(baseInfo_p_up[baseInfo_p_up.industry == '专用机械'])
#print(profit_data_list_p[2][profit_data_list_p[2].code == 300743])

def dealdata2(items):
    ans_dict = {}
    ans_dict['num'] = len(items)
    ans_dict['mean_roe'] = items.roe.mean()
    return pd.Series(ans_dict)
#print(baseInfo_last_year.groupby('industry').apply(dealdata2).sort_values(by='mean_roe'))
print(baseInfo_last_year[baseInfo_last_year.industry == '广告包装'])
#===============================================================================================
'''
计算压力线与抛售线
原理：交易必须有买卖双方，当某股以P价格成交B股时，卖出方相当于在P价格减轻W1*B了卖出压力
      而买入方，会在K1*P价格由于获利而抛出，形成W2*B抛压；而在K2*P的价格由于止损而抛出，也
      形成W3*B抛压。
算法：1.实践中考虑到前复权的问题，交易数量已换手率代替；
      2.为了便于横向比较，同一用当天价格对过去价格进行归一化,当天还手率对过去还手率进行归一化；
      3.由于无法得到每时每刻准确的数据，价格以收盘价估计
'''


#计算W，price_set为目标价，price_cur为当前价
'''
1.此函数还有待改进，比如，如果当前价位处于历史高位附近，则每上涨1元所带来的获利性抛压，显然比
其他价位要大
2.应该引进时间上的修正，越久远的数据，对现在影响应该越小，但似乎只对压力的增加有效，对释放压力无效
'''
def getW(price_set,price_cur,time_len):
    #由于price_set的精度是0.01，所以price_cur要进行精度的四舍五入
    price_cur_k = int(price_cur*100+0.5)*0.01
    #print(price_cur_k)
    diff = price_set - price_cur_k
    if diff > 0.0001:
        return diff*math.exp(-1*time_len)
    elif diff < -0.0001:
        return (-diff)*math.exp(-1*time_len)*1.01 #人类往往厌恶风险，所以止损性抛压要略加强，但幅度估计是否合理，待验证
    else:
        return -1

def getWFrame(price_cur,time_len):
    return pd.DataFrame({'W':[getW(x*0.01,price_cur,time_len) for x in range(0,200)]})

def readPriceData(code,start_date,end_date):
    data = readData(code,startDate=start_date,endDate=end_date)
    if data.empty:
        return pd.DataFrame()
    else:
        data['price_cur'] = data.close/data.close.iloc[0]
        data['tor_u'] = data.tor/data.tor.iloc[0]
        return data

def getPressFrame(code,start_date,end_date):
    ans = pd.DataFrame()
    data = readPriceData(code,start_date,end_date)
    if data.empty:
        return None,None,None
    else:
        length = len(data)
        for i in range(0,length):
            #计算增加的卖出压力
            if ans.empty:
                ans['press'] = getWFrame(data.price_cur.iloc[i],i).W*data.tor_u.iloc[i]
            else:
                ans['press'] = ans.press + getWFrame(data.price_cur.iloc[i],i).W*data.tor_u.iloc[i]
            #print(ans.iloc[0])
    ans['price'] = ans.index*0.01*data.close.iloc[0]
    #print(ans)
    minPress = ans.press.min()
    maxPress = ans.press.max()
    ans['press_u'] = (ans.press - minPress)/(maxPress - minPress)
    curPress_u = ans.press_u[100]
    minPress_u = ans.press_u.min()
    ans['minPress_u'] = minPress_u
    ans['curPress_u'] = curPress_u
    return ans,minPress_u,curPress_u
            
        
'''
testData,minPress,curPress = getPressFrame('601878','2017-09-01','2018-03-23')
testData.plot(y=['press_u'],x='price')
print(curPress)
print(minPress)
plt.show()
'''

#======================================================================================================
'''
对所有股票进行压力计算
'''

def getAllPress(start_date,end_date):
    def subFunc(item):
        ans_dict = {}
        pressFrame,minPress,curPress = getPressFrame(item,start_date,end_date)
        ans_dict['code'] = item
        ans_dict['minPress'] = minPress
        ans_dict['curPress'] = curPress
        print(item)
        return pd.Series(ans_dict)
    return baseInfo.codeStr.apply(subFunc)
        
        
    
#print(getAllPress('2017-09-01','2018-03-23'))
#==================================================================

'''
计算行业指数
算法：
1.行业内按流通股本分配权重
2.以虚拟本金100元，按权重买入个股
3.买入价为前一日开盘价格，卖出价为当日收盘价格
'''
com_date = '2018-03-07'    #必须补零

def apply_group_func(items):
    ans_dict = {}
    items['save'] = 1
    items['k'] = 0
    items['p1'] = 1
    items['p2'] = 1
    for code in items.codeStr:
        data = readData(code,endDate=com_date,first=2)
        if len(data) < 2:
            items.loc[items.codeStr == code,'save'] = 0
        else:
            items.loc[items.codeStr == code,'p1'] = data.iloc[1].open
            items.loc[items.codeStr == code,'p2'] = data.iloc[0].close
                
    items_save = items[items.save == 1]
    items_save.loc[:,'k'] = items_save.outstanding/items_save.outstanding.sum()
    #print(items_save)
    ans_dict['time'] = com_date
    ans_dict['a_in'] = (items_save.k/items_save.p1*(items_save.p2-items_save.p1)).sum()*100
    return pd.Series(ans_dict)
'''
ans_data = baseInfo.groupby('industry').apply(apply_group_func)
print(ans_data.sort_values(by='a_in',ascending=False))
'''
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

'''
ans_data = baseInfo.groupby('industry').apply(pe_mean)
print(ans_data.sort_values(by=['pb_mean']))
'''

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
