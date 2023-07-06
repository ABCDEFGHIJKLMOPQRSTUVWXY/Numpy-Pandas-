import pandas as pd 
import numpy as np

df = pd.read_excel('pandas120.xlsx')

#将salary列数据转换为最大值与最小值的平均值
def fun(x):
    list1 = x.split("k-")
    a = float(list1[0])
    b = float(list1[1].strip("k"))
    res = (b + a)*0.5*1000
    return int(res)
df["salary"] = df["salary"].map(fun)

ptp = pd.DataFrame({"ptp":[np.ptp(df["salary"]) for i in range(len(df))] } )
df = pd.concat((df,ptp), axis = 1)

df['category'] = pd.cut(df["salary"], bins = [0, 5000, 20000, 50000], labels = ["低", "中", "高"])

arr1 = []
arr2 = []
for i in range(len(df)):
    df2 = df.iloc[i][0].to_pydatetime()
    arr1.append(df2.strftime("%Y-%m-%d"))
    arr2.append(int(df2.strftime("%H")))
date_hour = pd.DataFrame({"date":arr1,"hour":arr2})
df = pd.concat((df,date_hour), axis = 1)

# 筛选出2020-03-16这一天的数据,并且命名为temp
temp = df[df["date"].isin(["2020-03-16"])]

# #按照date和hour分组统计
example = temp[["date","hour"]].drop_duplicates(["date","hour"]).sort_values("hour",ascending = True)
example.index = [0,1,2]
print(example)

#对temp的education和category进行dummy单片化
print(pd.get_dummies(temp['education'],temp['category']))


'''
# df4
df4 = temp.sort_values("hour",ascending = True)

mean_salary = df4.groupby(["date","hour"])["salary"].mean().round(2)# mean_salary
mean_ptp = df4.groupby(["date","hour"])["ptp"].mean().round(2)# mean_ptp
count_college = pd.DataFrame(df4.loc[df4.education=="本科"].groupby(["date","hour","education"]).education.count())# count_college
count_master = pd.DataFrame(df4.loc[df4.education=="硕士"].groupby(["date","hour","education"]).education.count())# count_master
count_low = pd.DataFrame(df4.loc[df4.category=="低"].groupby(["date","hour","category"]).category.count())
count_meddle = pd.DataFrame(df4.loc[df4.category=="中"].groupby(["date","hour","category"]).category.count())
count_high = pd.DataFrame(df4.loc[df4.category=="高"].groupby(["date","hour","category"]).category.count())# count_high

#数据框拼接
x = pd.merge(example, mean_salary, on = ["date","hour"])
x = pd.merge(x, mean_ptp,  on = ["date","hour"])
x = pd.merge(x, count_college, how='left', on = ["date","hour"])
x = pd.merge(x, count_master, how='left', on = ["date","hour"])

y = pd.merge(count_low, count_meddle, how='right', on = ["date","hour"])
y = pd.merge(y, count_high, how='right', on = ["date","hour"])

res = pd.merge(x, y, how='left', on = ["date","hour"])
df2 = res
'''

# 将df2的列名修改成题目要求的列名
df2.columns = ['date', 'hour', 'mean_salary', 'mean_ptp', 'count_college', 'count_master', 'count_low', 'count_meddle', 'count_high']

# 将含有nan的列数据类型转为int
df2["count_master"] = df2["count_master"].fillna(0)
df2["count_master"] = df2["count_master"].astype("int")
df2["count_master"] = df2["count_master"].astype("str")
df2["count_low"] = df2["count_low"].fillna(0)
df2["count_low"] = df2["count_low"].astype("int")
df2["count_low"] = df2["count_low"].astype("str")

df2.head()

data = pd.concat([df2.iloc[:,0],df2.iloc[:,1],df2.iloc[:,2],df2.iloc[:,3],df2.iloc[:,4],df2.iloc[:,5],df2.iloc[:,6],df2.iloc[:,7],df2.iloc[:,8]])
df3 = pd.DataFrame(data, columns=['answer'])
df3['id'] = range(len(df3))
df3 = df3[['id', 'answer']]

df3.to_csv('answer_3.csv', index=False, encoding='utf-8-sig')