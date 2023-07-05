import pandas as pd 
import numpy as np

df = pd.read_excel('/home/mw/input/pandas1206855/pandas120.xlsx')
df.head()


#
salary_25k_35k_df = df[df['salary'] == '25k-30k']
edu_df = salary_25k_35k_df[salary_25k_35k_df['education'] == '本科']
df1 = edu_df



end_40k_df = df[df['salary']].str.match('*40k')
df2 = end_40k_df



# 提取'salary'列中样例为'25k-30k'的数据
df['salary_range'] = df['salary'].str.extract(r'(\d+k-\d+k)')

# 拆分'salary_range'列为'25k'和'30k'两列数据
df[['min_salary', 'max_salary']] = df['salary_range'].str.split('-', expand=True)

# 将字符串转换为数值类型
df['min_salary'] = df['min_salary'].str.extract(r'(\d+)').astype(int)
df['max_salary'] = df['max_salary'].str.extract(r'(\d+)').astype(int)

# 计算每一行的平均值保存在'avr'列中
df['avr'] = (df['min_salary'] + df['max_salary']) / 2