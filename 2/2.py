import pandas as pd 

df = pd.read_excel('pandas120.xlsx')
print(df.head())

#提取学历为本科，工资在25k-35k的数据
salary_25k_35k_df = df[df['salary'] == '25k-35k']
edu_df = salary_25k_35k_df[salary_25k_35k_df['education'] == '本科']
df1 = edu_df

#提取salary列中以'40k'结尾的数据
end_40k_df = df[df['salary'].str.endswith('40k')]
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

df3 = df[df['avr'] > 30]

answer_2 = pd.concat([df1, df2, df3], axis=0)

data = pd.concat([answer_2.iloc[:,0],answer_2.iloc[:,1],answer_2.iloc[:,2]])
df = pd.DataFrame(data, columns=['answer'])
df['id'] = range(len(df))
df = df[['id', 'answer']]

df.to_csv('answer_2.csv', index=False, encoding='utf-8-sig')