import pandas as pd

df4 = pd.DataFrame({'B': ['B2', 'B3', 'B6', 'B7'],
                   'D': ['D2', 'D3', 'D6', 'D7'],
                    'F': ['F2', 'F3', 'F6', 'F7']},
                   index=[2, 3, 6, 7])

df1 = pd.DataFrame({'A': ['B1', 'B3', 'B6', 'B7'],
                   'B': ['D1', 'D3', 'D6', 'D7'],
                    'F': ['F1', 'F2', 'F6', 'F7']},
                   index=[0, 1, 6, 8])

print(pd.concat([df1,df4],axis=0,join='inner'))
