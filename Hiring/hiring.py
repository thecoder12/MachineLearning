import pandas as pd
from word2number import w2n
import re
from sklearn import linear_model


df = pd.read_csv('hiring.csv')

df['experience'] = df['experience'].fillna(0)

def charCheck(ip):
    ip = str(ip)
    if ip.isalpha():
        return(True)
    elif ip.isdigit():
        return(False)
      
      
for count, exp in enumerate(df['experience']):
    if charCheck(exp):
        df['experience'][count] = w2n.word_to_num(exp)
df['test_score(out of 10)'] = df['test_score(out of 10)'].fillna(df['test_score(out of 10)'].median())

model = linear_model.LinearRegression()
model.fit(df[['experience','test_score(out of 10)','interview_score(out of 10)']], df['salary($)'])


model.predict([[0,9,9]]) # 0->exp, 9-> test_score, 9-> interview
# array([54195.77874818])
