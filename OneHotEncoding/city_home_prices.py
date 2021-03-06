###
import numpy as np
import pandas as pd

df = pd.read_csv('homeprices_OHE.csv')
df.head(2)

dummies = pd.get_dummies(df.town)
dummies


merged = pd.concat([df, dummies], axis='columns')
merged

final = merged.drop(['town', 'west windsor'], axis='columns')

final

from sklearn.linear_model import LinearRegression
model = LinearRegression()


X = final.drop(['price'], axis='columns')
y = final['price']


model.fit(X,y)

model.predict([[2800,0,1]])

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

dfle = df
dfle.town = le.fit_transform(dfle.town)

X = dfle[['town', 'area']].values
X

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
ct = ColumnTransformer([('town', OneHotEncoder(), [0])], remainder = 'passthrough')


X = ct.fit_transform(X)
X


X = X[:,1:]
X

y = dfle.price.values
y

model.fit(X,y)

model.predict([[0,1,3400]]) # 3400 sqr ft home in west windsor
#array([681241.6684584])

model.predict([[1,0,2800]]) # 2800 sqr ft home in robbinsville
#array([590775.63964739])


