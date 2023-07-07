import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# STEP1:泰坦尼克号生存数据特征处理

# 1. 合并训练集与测试集
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
train_and_test = pd.concat([train, test], axis=0)     # 建议使用concat，append将在未来版本被移除
PassengerId=test['PassengerId']
print(train_and_test.shape)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 100)

# 2. 缺失值处理
# 2.1 对Embarked直接用众数填充
train_and_test.fillna(value={'Embarked': train_and_test['Embarked'].mode()[0]}, inplace=True)
# print(train_and_test[train_and_test['Embarked'].isnull()])

# 2.2 填充船票Fare字段
train_and_test.fillna(value={'Fare': train_and_test['Fare'].mean()}, inplace=True)
# print(train_and_test[train_and_test['Fare'].isnull()])

# 2.3 填充年龄Age字段
# 为尽可能用多的特征去预测Age的值，先对Cabin、Embarked、Name、Sex、Ticket、Pclass等特征进行处理，模型预测见后

# 3. 不同特征字段的数据处理
# 3.1 先对Embarked、Sex以及Pclass等用dummy处理
train_and_test = pd.get_dummies(train_and_test, columns=['Embarked', 'Sex', 'Pclass'])

# 3.2 票价分级处理
train_and_test['qcut_fare'], bins = pd.qcut(train_and_test['Fare'], 5, retbins=True)
train_and_test['qcut_fare_2fact'] = pd.factorize(train_and_test['qcut_fare'])[0]
tmp_fare_lv = pd.get_dummies(train_and_test['qcut_fare_2fact']).rename(columns=lambda x: 'Fare_lv_' + str(x))
train_and_test = pd.concat([train_and_test, tmp_fare_lv], axis=1)
train_and_test.drop(['qcut_fare', 'qcut_fare_2fact'], axis=1, inplace=True)

# 3.3 名字处理
train_and_test['Title'] = train_and_test['Name'].apply(lambda x: x.split(',')[1].split('.')[0].strip())

# 3.3.1 对头衔进行oner-hot编码
# tmp_title_lv = pd.crosstab(train_and_test.Title, train_and_test.Sex)    # 查看头衔人群稀有度
# print(tmp_title_lv.T)
# 提取称呼
train_and_test['Title'] = train_and_test['Name'].apply(lambda x : x.split(',')[1].split('.')[0].strip())
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
train_and_test['Title'] = train_and_test['Title'].map(titleDict)
# one_hot编码
train_and_test['Title'] = pd.factorize(train_and_test['Title'])[0]
title_dummies_train_and_test = pd.get_dummies(train_and_test['Title'], prefix=train_and_test[['Title']].columns[0])
train_and_test = pd.concat([train_and_test, title_dummies_train_and_test], axis=1)

# 3.3.2 添加一列：提取名字长度
train_and_test['len_name'] = train_and_test['Name'].apply(len)

# 3.4 Cabin处理 　Cabin缺失值过多，将其分为有无两类，进行编码，如果缺失，即为0，否则为1
train_and_test.loc[train_and_test.Cabin.isnull(), 'Cabin'] = 'nan'
train_and_test['Cabin'] = train_and_test.Cabin.apply(lambda x: 0 if x == 'nan' else 1)
# print(train_and_test['Cabin'].value_counts())

# 3.5 Ticket处理
train_and_test['Ticket_latter'] = train_and_test['Ticket'].apply(lambda x: x.split(' ')[0].strip())
train_and_test['Ticket_latter'] = train_and_test['Ticket_latter'].apply(lambda x: 'Latter' if x.isnumeric() == False else x)
train_and_test['Ticket_latter'] = pd.factorize(train_and_test['Ticket_latter'])[0]

# 4. 利用随机森林预测Age缺失值
missing_age = train_and_test.drop(['PassengerId', 'Survived', 'Name', 'Ticket'], axis=1)  # 去除字符串类型的字段
missing_age_train = missing_age[missing_age['Age'].notnull()]
missing_age_test = missing_age[missing_age['Age'].isnull()]

X_train = missing_age_train.iloc[:, 1:]
y_train = missing_age_train.iloc[:, 0]
X_test = missing_age_test.iloc[:, 1:]

rfr = RandomForestRegressor(n_estimators=1000, n_jobs=-1)
rfr.fit(X_train, y_train)
y_predict = rfr.predict(X_test)
train_and_test.loc[train_and_test['Age'].isnull(), 'Age'] = y_predict

# 5. 各特征与Survived的相关系数排序
train_and_test.corr()['Survived'].abs().sort_values(ascending=False)

del train_and_test['Age']
train_and_test = train_and_test.round(0)

df2 = train_and_test[['Title']]
df2.columns = ['answer']
df2.dropna(axis=0, how='any', inplace=True)
df2['id'] = range(len(df2))
df2 = df2[['id', 'answer']]

df2.to_csv('answer_5.csv', index=False, encoding='utf-8-sig')