import pandas as pd
import numpy as np
import matplotlib

data=pd.read_excel('./600000.SH.xls')
data.shift(-5)


# data.rolling(window = 1, min_periods = 1)["开盘价(元)"].agg(np.mean)

data_expanding = data.expanding(min_periods = 1)["开盘价(元)"].mean()



#方法一：分开绘制曲线
import pandas as pd
import matplotlib.pyplot as plt
font = {"family":"MicroSoft YaHei", "weight":"bold", "size":12 }
matplotlib.rc("font", **font)

plt.rc("figure", figsize = (16,6), dpi = 150)#设置图的大小
plt.plot(data["开盘价(元)"], label = "原始数据")
plt.plot(data_expanding, label = "累积数据")
plt.legend(loc = "upper right")
#plt.show()
#方法二：新增一列，一起生成曲线（可以自动生成图例）
# data = pd.merge(data,data_expanding, on ="日期" )
# data["开盘价(元)_x"].plot()
# data["开盘价(元)_y"].plot()



N = 20 #布林线指标的参数最好设为20
#第一步：计算MA
MA = data["收盘价(元)"]
#第二步：计算标准差MD
MD = data["收盘价(元)"].rolling(N, min_periods = 1).std(ddof=1)
#第三步：计算MB、UP、DN线
MB = data["收盘价(元)"].rolling(N, min_periods = 1).mean()
UP = MB + 2 * MD
DN = MB - 2 * MD

import matplotlib.pyplot as plt

font = {"family":"MicroSoft YaHei", "weight":"bold", "size":12 }
matplotlib.rc("font", **font)
plt.rc("figure", figsize = (16,6), dpi = 150)#设置图的大小
#绘制网格
plt.grid()
#设置x,y轴标签
plt.xlabel("时间")
plt.ylabel("收盘价(元)")
#绘制布林线(中轨线、上轨线、下轨线)
plt.plot(MA, label = "MA")
plt.plot(MB, label = "MB")
plt.plot(UP, label = "UP")
plt.plot(DN, label = "DN")

plt.legend(loc = "upper right")
#plt.show()

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