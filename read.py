import pandas as pd
import tushare as ts
import os
import matplotlib.pyplot as plt

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
'''

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
