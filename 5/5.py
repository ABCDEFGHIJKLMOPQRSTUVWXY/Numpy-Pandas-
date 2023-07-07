import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# STEP1:泰坦尼克号生存数据特征处理

# 1. 合并训练集与测试集
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
df = pd.concat([train, test], axis=0)     # 建议使用concat，append将在未来版本被移除
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 100)

# 2. 缺失值处理
# 2.1 对Embarked直接用众数填充
df.fillna(value={'Embarked': df['Embarked'].mode()[0]}, inplace=True)
# print(df[df['Embarked'].isnull()])

# 2.2 填充船票Fare字段
df.fillna(value={'Fare': df['Fare'].mean()}, inplace=True)
# print(df[df['Fare'].isnull()])

# 2.3 填充年龄Age字段
# 为尽可能用多的特征去预测Age的值，先对Cabin、Embarked、Name、Sex、Ticket、Pclass等特征进行处理，模型预测见后

# 3. 不同特征字段的数据处理
# 3.1 先对Embarked、Sex以及Pclass等用dummy处理
df = pd.get_dummies(df, columns=['Embarked', 'Sex', 'Pclass'])

# 3.2 票价分级处理
df['qcut_fare'], bins = pd.qcut(df['Fare'], 5, retbins=True)
df['qcut_fare_2fact'] = pd.factorize(df['qcut_fare'])[0]
tmp_fare_lv = pd.get_dummies(df['qcut_fare_2fact']).rename(columns=lambda x: 'Fare_lv_' + str(x))
df = pd.concat([df, tmp_fare_lv], axis=1)
df.drop(['qcut_fare', 'qcut_fare_2fact'], axis=1, inplace=True)

# 3.3 名字处理
df['Title'] = df['Name'].apply(lambda x: x.split(',')[1].split('.')[0].strip())

# 3.3.1 对头衔进行oner-hot编码
# tmp_title_lv = pd.crosstab(df.Title, df.Sex)    # 查看头衔人群稀有度
# print(tmp_title_lv.T)
# 提取称呼
df['Title'] = df['Name'].apply(lambda x : x.split(',')[1].split('.')[0].strip())
titleDict = {
    "Capt": "Officer",
    "Col": "Officer",
    "Major": "Officer",
    "Jonkheer": "Royalty",
    "Don": "Royalty",
    "Sir": "Royalty",
    "Dr": "Officer",
    "Rev":  "Officer",
    "the Countess": "Royalty",
    "Dona": "Royalty",
    "Mme": "Mrs",
    "Mlle": "Miss",
    "Ms": "Mrs",
    "Mr": "Mr",
    "Mrs": "Mrs",
    "Miss": "Miss",
    "Master": "Master",
    "Lady": "Royalty"
}
df['Title'] = df['Title'].map(titleDict)
# one_hot编码
df['Title'] = pd.factorize(df['Title'])[0]
title_dummies_df = pd.get_dummies(df['Title'], prefix=df[['Title']].columns[0])
df = pd.concat([df, title_dummies_df], axis=1)

# 3.3.2 添加一列：提取名字长度
df['len_name'] = df['Name'].apply(len)

# 3.4 Cabin处理 　Cabin缺失值过多，将其分为有无两类，进行编码，如果缺失，即为0，否则为1
df.loc[df.Cabin.isnull(), 'Cabin'] = 'nan'
df['Cabin'] = df.Cabin.apply(lambda x: 0 if x == 'nan' else 1)
# print(df['Cabin'].value_counts())

# 3.5 Ticket处理
df['Ticket_latter'] = df['Ticket'].apply(lambda x: x.split(' ')[0].strip())
df['Ticket_latter'] = df['Ticket_latter'].apply(lambda x: 'Latter' if x.isnumeric() == False else x)
df['Ticket_latter'] = pd.factorize(df['Ticket_latter'])[0]


# 4. 利用随机森林预测Age缺失值

missing_age = df.drop(['PassengerId', 'Survived', 'Name', 'Ticket'], axis=1)  # 去除字符串类型的字段
missing_age_train = missing_age[missing_age['Age'].notnull()]
missing_age_test = missing_age[missing_age['Age'].isnull()]

X_train = missing_age_train.iloc[:, 1:]
y_train = missing_age_train.iloc[:, 0]
X_test = missing_age_test.iloc[:, 1:]

rfr = RandomForestRegressor(n_estimators=1000, n_jobs=-1)
rfr.fit(X_train, y_train)
y_predict = rfr.predict(X_test)
df.loc[df['Age'].isnull(), 'Age'] = y_predict

# 5. 各特征与Survived的相关系数排序
df.corr()['Survived'].abs().sort_values(ascending=False)

del df['Age']
df = df.round(0)

df2 = df[['Title']]
df2.columns = ['answer']
df2.dropna(axis=0, how='any', inplace=True)
df2['id'] = range(len(df2))
df2 = df2[['id', 'answer']]

df2.to_csv('answer_5.csv', index=False, encoding='utf-8-sig')