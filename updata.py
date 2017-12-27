import tushare as ts
import pandas as pd
import os
import datetime

cons = ts.get_apis()
baseDir = './database'

if not os.path.exists(baseDir):
    os.mkdir(baseDir)

#df = ts.bar('300024',conn=cons)

#all_base_info = ts.get_stock_basics()
#all_base_info.to_csv(baseDir+"/"+"baseInfo.csv",encoding='utf-8');

#codes = all_base_info.index
codes = ['300024','000002','601878']

codes_len = len(codes)

data_list = []
index = 0

todaytime = datetime.datetime.now()

for code in codes:
    try:
        if os.path.exists(baseDir+"/"+code+".csv"):
            index = index+1
            print(baseDir+"/"+code+".csv exists")
            dold = pd.read_csv(baseDir+"/"+code+".csv");
            oldtime = datetime.datetime.strptime(dold.datetime.iloc[0],'%Y-%m-%d')
            delta = todaytime - oldtime

            if delta.days > 0:
                startTime = oldtime+datetime.timedelta(days=1)
                s = startTime.strftime('%Y-%m-%d')
                ditems = ts.bar(code,conn=cons,freq='D',adj='qfq',start_date=s,factors=['tor'])
                dold.set_index('datetime')
                dnew = pd.merge(ditems,dold)
                print(dnew)
                break            
        else:
            d = ts.bar(code,conn=cons,freq='D',adj='qfq',start_date='2014-1-1',factors=['tor'])
            if type(d) != pd.DataFrame:
                print(code+" get failed!")
            else:
                index = index + 1
                print(code+" finish="+str(index)+'/'+str(codes_len))
                d['code'] = code
                d.to_csv(baseDir+"/"+code+".csv",encoding='utf-8')
            #data_list.append(d)
    except:
        print(code+" error")


"""
def getTickData(code,dates):
    index = 0
    datalen = len(dates)
    for d in dates:
        try:
            index = index+1
            #df = ts.get_tick_data(code,date=d,pause = 0.1)
            df = ts.tick(code,conn=cons,date=d)
            df.to_csv(baseDir+"/tick_"+code+"_"+d+".csv",encoding='utf-8')
            print(code+" "+d+"_"+str(index)+"/"+str(datalen))
        except:
            print(code+" "+d+" error")
        
for code in codes:
    try:
        d_ra = pd.date_range('2017-11-25',periods=5)
        print(d_ra)
        getTickData(code,d_ra)
    except:
        print(code+" error");

"""

