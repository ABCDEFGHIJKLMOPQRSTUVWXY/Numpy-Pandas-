import pandas as pd
import numpy as np
train = pd.read_csv('/home/mw/input/titanic/train.csv')
test = pd.read_csv('/home/mw/input/titanic/test.csv')
train_and_test = train.append(test, sort=False) # 合并训练集与测试集
PassengerId = test['PassengerId']
train_and_test.shape
train_and_test.head()



#查看缺失值情况
train_and_test.isnull().sum()
#众数填充Embarked字段
embarked_mode=train_and_test['Embarked'].mode()[0]
train_and_test['Embarked'].fillna(embarked_mode,inplace = True)
#船票均值填充NA值
fare_mean=round(train_and_test['Fare'].mean(),4)
train_and_test['Fare'].fillna(fare_mean,inplace = True)
## 对embarked,sex,pclass分类特征进行编码,embarked/sex文本型变量转换成数值型
train_and_test=pd.get_dummies(train_and_test,columns=['Embarked','Sex','Pclass'])
#票价处理，把票价分成5级
train_and_test['fare_category']=pd.cut(train_and_test['Fare'],5,labels=[1,2,3,4,5])
#提取title
import re
train_and_test['title']=train_and_test['Name'].apply(lambda x: re.search(r'[a-zA-Z]+\.',x).group(0).strip('.'))
train_and_test['title'].unique()
# one_hot编码,类似于get_dummies
#先把各称呼重新分类
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
train_and_test['title'] = train_and_test['title'].map(titleDict)
#分类完毕后进行转换成数值化特征，参考于帖子：[https://www.heywhale.com/home/competition/forum/628aeb26b29dff4411335e2c](http://)
train_and_test['title'] = pd.factorize(train_and_test['title'])[0]
title_dummies_df = pd.get_dummies(train_and_test['title'], prefix=train_and_test[['title']].columns[0])
train_and_test = pd.concat([train_and_test, title_dummies_df], axis=1)
train_and_test.head()
# 提取长度特征
train_and_test['length']=train_and_test['Name'].apply(len)
#Cabin缺失值过多，将其分为有无两类，进行编码，如果缺失，即为0，否则为1;
train_and_test.loc[train_and_test.Cabin.isnull(),'Cabin']='nan'
train_and_test['Cabin']= train_and_test['Cabin'].apply(lambda x: 0 if x=='nan' else 1)
#是把Ticket 分类，如果有字母的为一类，没有字母的为一类,有字母的为一类，没有字母的为0）
train_and_test['ticket_levl']=train_and_test['Ticket'].astype(str).apply(lambda x : len(re.search('([a-zA-Z]+)',x).group(0)) if re.search('([a-zA-Z]+)',x) else 0 )