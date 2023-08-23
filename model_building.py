

import matplotlib as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

df=pd.read_csv('data_eda.csv')

#choose relevant columns

df.columns
df_model=df[['seniority', 'Job Description length','salary_avg',"Rating","Size", 'Type of ownership', 'state', 'same_state',
 'Industry', 'Sector', 'Revenue','salary per hour', 'employer provided salary','python', 'aws', 'excel'            
 ]]

#get dummy data 

df_dum =pd.get_dummies(df_model)
#split train test data 


X=df_dum.drop("salary_avg",axis=1)
y=df_dum.salary_avg.values

X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.22, random_state=42)
   


#linear regression

import statsmodels.api as sm

x_sm =X=sm.add_constant(X)
model = sm.OLS(y,x_sm)
model.fit().summary()


#linear regression with sklearn
from sklearn.linear_model import LinearRegression,Lasso
from sklearn.model_selection import cross_val_score
import matplotlib as plt

reg = LinearRegression()
reg.fit(X_train, y_train)
np.mean(cross_val_score(reg,X_train,y_train,scoring="neg_mean_absolute_error",cv=3))

#lasso model
lm_m=Lasso()

lm_m.fit(X_train, y_train)
np.mean(cross_val_score(lm_m,X_train,y_train,scoring="neg_mean_absolute_error",cv=3))


alpha=[]
error=[]
for i in range(1,100):
    alpha.append(i)
    lm_m=Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lm_m,X_train,y_train,scoring="neg_mean_absolute_error",cv=3)))


plt.pyplot.plot(alpha, error)

lm_m=Lasso(alpha=0.12)
lm_m.fit(X_train, y_train)
df_error=pd.DataFrame(tuple(zip(alpha,error)),columns=['alpha','error'])
print(df_error[df_error.error==max(df_error.error)])

lm_m=Lasso(alpha=0.12)
np.mean(cross_val_score(lm_m,X_train,y_train,scoring="neg_mean_absolute_error",cv=3))
lm_m=Lasso(alpha=0.12)
lm_m.fit(X_test,y_train)

#Random forest regressor 
from sklearn.ensemble import RandomForestRegressor
regr= RandomForestRegressor()
regr.fit(X_train,y_train)
np.mean(cross_val_score(regr,X_train,y_train,scoring="neg_mean_absolute_error",cv=3))

#hyperparameter tuning 
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10),'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}

#gs = GridSearchCV(regr,parameters,scoring='neg_mean_absolute_error',cv=3)
#gs.fit(X_train,y_train)

#gs.best_score_
#gs.best_estimator_

#test
 
reg_pred=reg.predict(X_test)
lm_m_pred=lm_m.predict(X_test)
regr_pred=regr.predict(X_test)

from sklearn.metrics import mean_absolute_error
error_lr=mean_absolute_error(reg_pred, y_test)
error_lassr=mean_absolute_error(lm_m_pred, y_test)
error_rf=mean_absolute_error(regr_pred, y_test)
print(error_lr,error_lassr,error_rf)





