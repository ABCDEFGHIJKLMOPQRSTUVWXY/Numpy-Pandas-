import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

data = pd.read_excel('/home/mw/input/pandas1206855/600000.SH.xls')

# 删除空值
data.dropna(axis=0, how='any', inplace=True)

# 删除非数值行
tmp = []
for i in range(len(data)):
    if type(data.loc[i, '换手率(%)']) != float:
        tmp.append(i)
data.drop(labels=tmp, inplace=True)

# 重置索引，并设置新index
data = data.reset_index()
data = data.set_index('日期')

# STEP1: 按照以下要求计算结果
# 1. 将数据往前移动5天 ！注意此处！第25步往后移动5天！

# data = data.shift(-5)   # 第25步操作
# data = data.shift(-5)   # 第一题操作

# 2. 使用expanding函数计算开盘价的移动窗口均值

meta_mean_sta = data['开盘价(元)']
exp_mean_sta = data['开盘价(元)'].expanding(min_periods=1, center=False, axis=0).mean()
plot_df1_mean = pd.concat([meta_mean_sta, exp_mean_sta], axis=1, ignore_index=True)
plot_df1_mean = plot_df1_mean.rename(columns={0: '原始数据',
                                              1: '移动窗口均值'})

# 3. 绘制上一题的移动均值与原始数据折线图

# plt.rc('figure', figsize=(16, 6), dpi=150)
# plt.plot(plot_df1_mean['原始数据'])
# plt.plot(plot_df1_mean['移动窗口均值'])
# plt.show()

# 4. 计算布林指标

N = 20  # 布林线指标的参数最好设为20

# 第一步：计算MA 移动平均线

ma = data['收盘价(元)'].rolling(N).mean()

# 第二步：计算标准差MD

md = data['收盘价(元)'].rolling(N).std()

# 第三步：计算MB、UP、DN线 分别对应 中轨线 上轨线 下轨线

mb = ma
up = mb + (md * 2)
dn = mb - (md * 2)

# 5. 计算布林线并绘制

plt.rc('figure', figsize=(16, 6), dpi=150)
plt.plot(ma, color='blue')
plt.plot(up, color='red')
plt.plot(dn, color='g')
#plt.show()

# STEP2: 为了简化最终提交的行数，所以这里只需要保留上轨线UP这一字段即可，并保存为 csv 文件

dic = {'上轨线': up}
df = pd.DataFrame(dic).reset_index(drop=True)
df = df.round(2)
df.columns = ['answer']
df.dropna(axis=0, how='any', inplace=True)
df['id'] = range(len(df))
df = df[['id', 'answer']]

df.to_csv('answer_4.csv', index=False, encoding='utf-8-sig')