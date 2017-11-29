#
#
# titanic.py
#
# Eli Cohen
# CS 35 - CS for Insight
# Assignment 4
# 26 Sunday, 2017
#
#

import numpy as np
from sklearn import datasets
from sklearn import cross_validation
import pandas as pd

# Turn csv in pandas dataframe
df = pd.read_csv('titanic.csv', header=0)

# Drop unimportant columns
df = df.drop('body', axis=1)
df = df.drop('ticket', axis=1)
df = df.drop('fare', axis=1)
df = df.drop('cabin', axis=1)
df = df.drop('embarked', axis=1)
df = df.drop('boat', axis=1)
df = df.drop('home.dest', axis=1)
df = df.drop('name', axis=1)

# Drop missing data
df = df.dropna()

# Converting sex into numeric data
def tr_mf(s):
	""" from string to number
	"""
	d = { 'male':0, 'female':1 }
	return d[s]

# apply the function to the column
df['sex'] = df['sex'].map(tr_mf)

# Print the dataframe
df.head()
df.info()

print("+++ end of pandas +++\n")
print("+++ start of numpy/scikit-learn +++")

# extract the underlying data with the values attribute:
X_data = df.drop('survived', axis=1).values     # everything except the 'survival' column
y_data = df[ 'survived' ].values      			# also addressable by column name(s)

# Give young age a high score
for num in X_data[:,2]:
	num = 80 - num

# Feature Engineering!
X_data[:,0] *= 10
X_data[:,1] *= 12
X_data[:,2] *= 4
X_data[:,3] *= 1
X_data[:,4] *= 1

# Unknown data
X_unknown = X_data[0:42,:]
X_test_and_train = X_data[42:,:]
y_test_and_train = y_data[42:]

# Testing and training data
X_test = X_test_and_train[0:200,0:6]              # the final testing data
X_train = X_test_and_train[200:,0:6]              # the training data

y_test = y_test_and_train[0:200]                  # the final testing outputs/labels (unknown)
y_train = y_test_and_train[200:]                  # the training outputs/labels (known)


from sklearn.neighbors import KNeighborsClassifier

def cross_validate():
	""" This function tries all values of k between 1 and 101 ten times, 
		takes the average, and then reports the best value of k
	"""

	train_lst = []
	test_lst = []

	# Find best value of k between 1 and 21, odd only
	for k in range(1,101,2):

		knn = KNeighborsClassifier(n_neighbors=k+1)

		train_sum = 0
		test_sum = 0

		# run cross-validation
		for i in range(10):

			cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
			cross_validation.train_test_split(X_train, y_train, test_size=0.1)

			knn.fit(cv_data_train, cv_target_train)

			train_score = knn.score(cv_data_train,cv_target_train)
			train_sum += train_score

			test_score = knn.score(cv_data_test,cv_target_test)
			test_sum += test_score

		train_avg = (train_sum / 10)
		train_lst.append([train_avg,k])
		
		test_avg = (test_sum / 10)
		test_lst.append([test_avg,k])

	print("MAX: ", max(test_lst))
	return max(test_lst)

# Predict unkonwn passenger fates
best_k = cross_validate()
knn = KNeighborsClassifier(n_neighbors=best_k[1])
knn.fit(X_train,y_train)
predictions = knn.predict(X_unknown)
print('\n+++ UNKOWN PASSENGER FATES +++')

for i in range(len(predictions)):
	print(predictions[i])

"""
Comments and Results!

Once I had worked through syntatical problems of sci-kit learn in digits,
I thought this problem was actually easier. Sometimes I still just feel
like I am doing a prescribed program, however, and don't understand the 
full nuance of machine learning.

Best Cross Validation Score: 0.81604938271604932
K Value that Produced Score: 5
Prediction Results:
0
0
0
0
0
1
0
1
1
1
1
1
0
1
0
0
0
0
0
0
1
1
0
1
1
1
0
0
0
0
0
0
1
1
0
0
0
1
0
1
0
1
"""