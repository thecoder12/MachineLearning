import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

d = pd.read_csv('canada_per_capita_income.csv')
d.head(3)

plt.scatter(d['year'], d['per capita income (US$)'], color='red', marker='+')

#model LR build
model = linear_model.LinearRegression()
model.fit(d[['year']], d['per capita income (US$)'])


model.predict([[2020]])
