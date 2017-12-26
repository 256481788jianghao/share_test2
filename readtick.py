import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt

baseDir = "./database"
"""
datetime  price  vol
type 0-B 1-S 2-start
"""

def readTick(code,date):
    return pd.read_csv(baseDir+'/tick_'+code+'_'+date+'.csv')

def compute_price(code,date,hold=30*10000):
    data = readTick(code,date)
    data['amount'] = data.price*data.vol*100
    data_b = data[data.type == 0]
    data_s = data[data.type == 1]
    data_b_big = data_b[data_b.amount >= hold]
    data_s_big = data_s[data_s.amount >= hold]
    data_b_small = data_b[data_b.amount < hold]
    data_s_small = data_s[data_s.amount < hold]
    v = data.vol.sum()
    v_b_big = data_b_big.vol.sum()
    v_b_small = data_b_small.vol.sum()
    v_s_big = data_s_big.vol.sum()
    v_s_small = data_s_small.vol.sum()
    p_b_big = data_b_big.amount.sum()/v_b_big/100
    p_b_small = data_b_small.amount.sum()/v_b_small/100
    p_s_big = data_s_big.amount.sum()/v_s_big/100
    p_s_small = data_s_small.amount.sum()/v_s_small/100
    return p_b_big,p_b_small,v_b_big/v_b_small,p_s_big,p_s_small,v_s_big/v_s_small

dates = ['2017-12-08','2017-12-11','2017-12-12','2017-12-13']
ans_list = []
for d in dates:
    ans_list.append(compute_price('300024',d)[0])
plt.plot(dates,ans_list)
plt.show()
