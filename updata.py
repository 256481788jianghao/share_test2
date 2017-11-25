import tushare as ts
import pandas as pd
import os

cons = ts.get_apis()

#df = ts.bar('300024',conn=cons)

#all_base_info = ts.get_stock_basics()

#codes = all_base_info.index
codes = ['300024','000002','601878']

codes_len = len(codes)

data_list = []
index = 0

for code in codes:
    try:
        d = ts.bar(code,conn=cons,freq='D',adj='qfq',start_date='2000-1-1')
        if type(d) != pd.DataFrame:
            print(code+" get failed!")
        else:
            index = index + 1
            print(code+" finish="+str(index)+'/'+str(codes_len))
            d['code'] = code
            data_list.append(d)
    except:
        print(code+" error")

data = pd.concat(data_list)

if os.path.exists('./database.csv'):
    os.remove('./database.csv')

data.to_csv('./database.csv')




