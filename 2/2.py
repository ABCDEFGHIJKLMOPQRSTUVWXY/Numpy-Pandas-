import pandas as pd 
import numpy as np

df = pd.read_excel('/home/mw/input/pandas1206855/pandas120.xlsx')
df.head()

salary_25k_35k_df = df[df['salary'] == '25k-30k']
edu_df = salary_25k_35k_df[salary_25k_35k_df['education'] == '本科']
df1 = edu_df

end_40k_df = df[df['salary']].str.match('*40k')
df2 = end_40k_df


avr_30k_df = df[df['salary']]