import pandas as pd 
import numpy as np

df = pd.read_excel('pandas120.xlsx')
print(df.head())


#将salary列数据转换为最大值与最小值的平均值
# apply + 自定义函数

#将salary列数据转换为最大值与最小值的平均值
# 提取'salary'列中样例为'25k-30k'的数据
df1 = df

df1['salary_range'] = df1['salary'].str.extract(r'(\d+k-\d+k)')

# 拆分'salary_range'列为'25k'和'30k'两列数据
df1[['min_salary', 'max_salary']] = df1['salary_range'].str.split('-', expand=True)

# 将字符串转换为数值类型
df1['min_salary'] = df1['min_salary'].str.extract(r'(\d+)').astype(int)
df1['max_salary'] = df1['max_salary'].str.extract(r'(\d+)').astype(int)

# 计算每一行的平均值保存在'avr'列中
df1['salary'] = ((df1['min_salary'] + df1['max_salary']) / 2) * 1000

columns_to_drop = ['salary_range', 'min_salary', 'max_salary']  # 请将'column1'、'column2'、'column3'替换为你要删除的列名
df1 = df1.drop(columns=columns_to_drop)

df1['salary'] = df1['salary']

df1.head()

# 方法一：max()，min()
# 方法二：apply + lambda
# 方法三：numpy.ptp()函数

# 计算'salary'列的最大值和最小值之差
df1['ptp'] = df1['salary'].str.extract(r'(\d+)').astype(int).ptp()