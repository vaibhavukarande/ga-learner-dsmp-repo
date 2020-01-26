# --------------
# import the libraries
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Code starts here
df=pd.read_csv(path)
print(df.head())
X=df.drop('insuranceclaim',axis=1)
y=df['insuranceclaim']
#Split the dataframe 
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size = 0.2,random_state = 6 )
# Code ends here


# --------------
import matplotlib.pyplot as plt


# Code starts here
#plt.boxplot(X_train['bmi'],inplace=True)
sns.boxplot(x=X_train['bmi'],y='insuranceclaim',data=df)

q_value=X_train['bmi'].quantile(0.95)
print(q_value)

print(y_train.value_counts(normalize=True))
# Code ends here


# --------------
# Code starts here


relation=X_train.corr()
print(relation)
g=sns.pairplot(X_train)
# Code ends here


# --------------
import seaborn as sns
import matplotlib.pyplot as plt

# Code starts here
cols=['children','sex','region','smoker']
fig,axes=plt.subplots(nrows=2,ncols = 2)

for i in range(0,2):
    for j in range(0,2):
        col=cols[ i * 2 + j]
sns.countplot(x=X_train[col], hue=y_train, ax=axes[i,j])



# Code ends here


# --------------
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error


# parameters for grid search
parameters = {'C':[0.1,0.5,1,5]}

# Code starts here
lr=LogisticRegression(random_state=9)
grid=GridSearchCV(estimator=LogisticRegression(),param_grid=parameters)
grid.fit(X_train,y_train)
y_pred=grid.predict(X_test)
accuracy=accuracy_score(y_test,y_pred)
print(accuracy)


# Code ends here


# --------------
from sklearn.metrics import roc_auc_score
from sklearn import metrics

# Code starts here
score=roc_auc_score(y_test,y_pred)

y_pred_proba = grid.predict_proba(X_test)[:,1]

fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred_proba)

roc_auc=roc_auc_score(y_test,y_pred_proba)

plt.plot(fpr,tpr,label="Logistic model, auc="+str(roc_auc))
# Code ends here


