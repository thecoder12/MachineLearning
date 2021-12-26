import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
import numpy as np


df = pd.read_csv('car data.csv') # read the dataset

def get_current_year():
    import datetime
    now = datetime.datetime.now()  # 2015 5 6 8 53 40 -> now.year, now.month, now.day, now.hour, now.minute, now.second
    return(now.year)
    
# print(df.head(5)) # check the data sample by head

# print(df.shape) #row=301, cols=9

# print(df['Seller_Type'].unique())  #['Dealer' 'Individual']
# print(df['Fuel_Type'].unique())   #['Petrol' 'Diesel' 'CNG']
# print(df['Transmission'].unique())   #['Manual' 'Automatic']
# print(df['Owner'].unique())   # [0 1 3]


#check missing & null values.
# print(df.isnull().sum()) # there is no null value or missing value the dataset is clean and good to use.

# dataset stats
# print(df.describe())

# get all the column names
# print(df.columns)

final_dataset = df[['Year','Selling_Price','Present_Price','Kms_Driven','Fuel_Type', 'Seller_Type', 'Transmission','Owner']]
#normalize the columns and data.

year = get_current_year()
final_dataset['no_year'] = year - final_dataset['Year']

#drop the columns
final_dataset.drop(['Year'], axis=1, inplace=True)


## convert vaules to 1-hot-encoding
final_dataset = pd.get_dummies(final_dataset, drop_first=True)


# find correlation
# final_dataset = final_dataset.corr()
# print(final_dataset.tail())

# print(sns.pairplot(final_dataset))
# plt.show()

corrmat = final_dataset.corr()
top_corr_features = corrmat.index
# plt.figure(figsize=(20,20))

#plot heat map
# g = sns.heatmap(final_dataset[top_corr_features].corr(), annot=True, cmap="RdYlGn")

# independant and dependant features
X = final_dataset.iloc[:,1:] # independant features
y = final_dataset.iloc[:,0]  # dependant features

print(X.head())
print(y.head(5))


## Feature Importance
from sklearn.ensemble import ExtraTreesRegressor
model = ExtraTreesRegressor()
print(model.fit(X,y))
# print(ExtraTreesRegressor())
print(model.feature_importances_)


#plot graph of feature importances for better visualization
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(5).plot(kind='barh')
# feat_importances.plot()
# plt.show()


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

print(X_train)

rf_random = RandomForestRegressor()

#hyper parameters
n_estimators = [int(x) for x in np.linspace(start=100, stop=1200, num=12)]
print(n_estimators)

#Randomized Search CV

# No of features to consider at every split
max_features = ['auto', 'sqrt']

# Max no of levels in tree
max_depth = [int(x) for x in np.linspace(5, 30, num=6)]

# Min no of samples reqd to split the node
min_samples_split = [2,5,10,15,100]

# min no of samples reqd at each leaf node
min_samples_leaf = [1,2,5,10]


# create the random grid
random_grid = {
    'n_estimators': n_estimators, 'max_features': max_features, 'max_depth': max_depth, 
    'min_samples_split': min_samples_split, 'min_samples_leaf':min_samples_leaf
    }
print(random_grid)


# use the random grid to search for best hyper-parameters
# first create the base model to tune

rf = RandomForestRegressor()
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid,scoring='neg_mean_squared_error', n_iter = 10, cv = 5, verbose=2, random_state=42, n_jobs = 1)

rf_random.fit(X_train,y_train)

predictions=rf_random.predict(X_test)
sns.distplot(y_test-predictions)
plt.scatter(y_test,predictions)

from sklearn import metrics

print('MAE:', metrics.mean_absolute_error(y_test, predictions))
print('MSE:', metrics.mean_squared_error(y_test, predictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

import pickle
# open a file, where you ant to store the data
file = open('random_forest_regression_model.pkl', 'wb')

# dump information to that file
pickle.dump(rf_random, file)




