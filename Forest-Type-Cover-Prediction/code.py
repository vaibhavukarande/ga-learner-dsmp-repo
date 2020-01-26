# --------------
import pandas as pd
from sklearn import preprocessing

#path : File path

# Code starts here



# read the dataset
dataset=pd.read_csv(path)

# look at the first five columns
print(dataset.head(5))

# Check if there's any column which is not useful and remove it like the column id
dataset.drop(['Id'],inplace=True,axis=1)
print(dataset.drop(dataset.ix[:,'Wilderness_Area2':'Soil_Type40'], axis = 1))

# check the statistical description
print(dataset.describe())


# --------------
# We will visualize all the attributes using Violin Plot - a combination of box and density plots
import seaborn as sns
from matplotlib import pyplot as plt

#names of all the attributes 
cols=list(dataset)
print(cols)

#number of attributes (exclude target)
size=dataset.drop('Cover_Type',axis=1)

print(len(size))

#x-axis has target attribute to distinguish between classes
x=dataset['Cover_Type']

#y-axis shows values of an attribute
y=dataset.drop('Cover_Type',inplace=True,axis=1)
print(y)
#Plot violin for all attributes
g=sns.violinplot(data=dataset,x=x,y=y)


# --------------
import numpy as np
upper_threshold = 0.5
lower_threshold = -0.5


# Code Starts Here
subset_train=dataset.iloc[:,:10]
#print(subset_train)

data_corr=subset_train.corr(method='pearson')
#print(data_corr)
#g=sns.heatmap(data_corr)

correlation=data_corr.unstack().sort_values(kind='quicksort')
#print(correlation.shape)
#print(correlation)
a=np.array(correlation.values)
#print(a)
#print(correlation.keys())
#print(correlation[:2])
corr_var_list=list()
for i in a:
    if((i!=1) & ((i>upper_threshold) | (i<lower_threshold))):
        corr_var_list.append(i)

print(corr_var_list)
#corr_var_list.append((correlation.values > upper_threshold) | (correlation.values < lower_threshold) & (correlation.values != 1 ))

#print(corr_var_list)
# Code ends here




# --------------
#Import libraries 
from sklearn import cross_validation
from sklearn.preprocessing import StandardScaler
import numpy
from sklearn.model_selection import train_test_split
# Identify the unnecessary columns and remove it 
dataset.drop(columns=['Soil_Type7', 'Soil_Type15'], inplace=True)

r,c = dataset.shape
X = dataset.iloc[:,:-1]
Y = dataset.iloc[:,-1]

# Scales are not the same for all variables. Hence, rescaling and standardization may be necessary for some algorithm to be applied on it.
X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y, test_size=0.2, random_state=0)



#Standardized

scaler = StandardScaler()

#Apply transform only for continuous data
X_train_temp = scaler.fit_transform(X_train.iloc[:,:10])
X_test_temp = scaler.transform(X_test.iloc[:,:10])

#Concatenate scaled continuous data and categorical
X_train1 = numpy.concatenate((X_train_temp,X_train.iloc[:,10:c-1]),axis=1)
X_test1 = numpy.concatenate((X_test_temp,X_test.iloc[:,10:c-1]),axis=1)

scaled_features_train_df = pd.DataFrame(X_train1, index=X_train.index, columns=X_train.columns)
scaled_features_test_df = pd.DataFrame(X_test1, index=X_test.index, columns=X_test.columns)


# --------------
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import f_classif


# Write your solution here:

# Code starts here
skb = SelectPercentile(score_func=f_classif,percentile=90)
predictors = skb.fit_transform(X_train1, Y_train)
scores = list(skb.scores_)

Features = scaled_features_train_df.columns

dataframe = pd.DataFrame({'Features':Features,'Scores':scores})

dataframe=dataframe.sort_values(by='Scores',ascending=False)

top_k_predictors = list(dataframe['Features'][:predictors.shape[1]])

print(top_k_predictors)

# Code Ends here


# --------------
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score

#define two variables as clf and clf1 intializing the one vs rest classifier with logistic regression 
clf = OneVsRestClassifier(LogisticRegression())
clf1 = OneVsRestClassifier(LogisticRegression())

#Create a variable model_fit_all_features which fits the classifier clf1 
model_fit_all_features=clf1.fit(X_train,Y_train)

#Predict the values with the above model fitted on X_test 
predictions_all_features=model_fit_all_features.predict(X_test)

#Get the accuracy score for the model 
score_all_features=accuracy_score(predictions_all_features,Y_test)

print(score_all_features)

#Create a variable model_fit_top_features 
model_fit_top_features=clf.fit(scaled_features_train_df[top_k_predictors], Y_train)

#Predict the values with the above model fitted on scaled_features_train_df 
predictions_top_features=model_fit_top_features.predict(scaled_features_test_df[top_k_predictors])

#Get the accuracy score for the model
score_top_features=accuracy_score(Y_test,predictions_top_features)

print(score_top_features)





