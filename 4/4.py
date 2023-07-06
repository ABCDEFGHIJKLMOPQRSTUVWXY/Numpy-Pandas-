import pandas as pd
import numpy as np
import matplotlib

data=pd.read_excel('./600000.SH.xls')
data.shift(-5)

#data.rolling(window = 1, min_periods = 1)["开盘价(元)"].agg(np.mean)
data_expanding = data.expanding(min_periods = 1)["开盘价(元)"].mean()

N = 20 #布林线指标的参数最好设为20
#第一步：计算MA
MA = data["收盘价(元)"]
#第二步：计算标准差MD
MD = data["收盘价(元)"].rolling(N, min_periods = 1).std(ddof=1)
#第三步：计算MB、UP、DN线
MB = data["收盘价(元)"].rolling(N, min_periods = 1).mean()
UP = MB + 2 * MD
DN = MB - 2 * MD

dic = {'上轨线':UP}
df = pd.DataFrame(dic).reset_index(drop=True)
df = df.round(2)
print(df)

df.columns = ['answer']
df.dropna(axis=0, how='any', inplace=True)
df['id'] = range(len(df))
df = df[['id', 'answer']]


list=[]
for i in range(1,19):
    list.append(i)
#df=df.drop(list)

print(df)
df.to_csv('answer_4.csv', index=False, encoding='utf-8-sig')