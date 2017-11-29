#
#
# digits.py
#
# Eli Cohen
# CS 35 - CS for Insight
# Assignment 4
# 26 Sunday, 2017
#
#

import numpy as np
from sklearn import cross_validation
import pandas as pd

df = pd.read_csv('digits.csv', header=0)

def transform(s):
    """ from number to string
    """
    return 'digit ' + str(s)
    
df['label'] = df['64'].map(transform)

# Print the dataframe
df.head()
df.info()

print("+++ End of pandas +++\n")
print("+++ Start of numpy/scikit-learn +++")

# Convert to numpy array
X_data_full = df.iloc[:,0:64].values    # iloc == "integer locations" of rows/cols
y_data_full = df[ '64' ].values      # also addressable by column name(s)

# Unkown data
X_unknown = X_data_full[0:22,:]
y_unknown = y_data_full[0:22]

# Unknown and not erased data
X_unknown_not_erased = X_unknown[10:22,:]

# Unknown and half-erased data
X_unknown_erased = X_unknown[0:10,:]

# Set to print entire array
np.set_printoptions(threshold=np.nan)

# Drop the initial unknowns from testing data
X_data_full = X_data_full[22:,:]
y_data_full = y_data_full[22:]

# Scramble the entries each time
indices = np.random.permutation(len(X_data_full))
X_data_full = X_data_full[indices]
y_data_full = y_data_full[indices]

# The first 100 are out test set. The remaining 1700 our training set.
X_test = X_data_full[0:100,0:64]     # the final testing data
X_train = X_data_full[100:,0:64]     # the training data

y_test = y_data_full[0:100]          # the final testing outputs/labels (unknown)
y_train = y_data_full[100:]          # the training outputs/labels (known)

# Feature Engineering! (NOT YET USED)
for i in range (64):
    X_data_full[:,i] *= 1

from matplotlib import pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

def show_digit( Pixels ):
    """ input Pixels should be an np.array of 64 integers (from 0 to 15) 
        there's no return value, but this should show an image of that 
        digit in an 8x8 pixel square
    """
    # print(Pixels.shape)
    Patch = Pixels.reshape((8,8))
    plt.figure(1, figsize=(4,4))
    plt.imshow(Patch, cmap=plt.cm.gray_r, interpolation='nearest')  # cm.gray_r   # cm.hot
    plt.show()
    
def show_multiple_digits( start_row , end_row ):
    """ Implements the show pixel function for
        as many rows as specified
    """
    for i in range(start_row,end_row):
        print(i)
        row = i
        Pixels = X_data_full[row:row+1,:]
        show_digit(Pixels)
        print("That image has the label:", y_unknown[row])

def cross_validate():
    """ This function tries all values of k between 1 and 101 ten times, 
        takes the average, and then reports the best value of k
    """

    train_lst = []
    test_lst = []

    # Find best value of k between 1 and 21, odd only
    for k in range(1,21,2):

        knn = KNeighborsClassifier(n_neighbors=k+1)

        train_sum = 0
        test_sum = 0

        # run cross-validation
        for i in range(10):

            cv_data_train, cv_data_test, cv_target_train, cv_target_test = \
            cross_validation.train_test_split(X_train, y_train, test_size=0.1) # random_state=0 

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

# Predict unkonwn digits
best_k = cross_validate()
print(best_k[1])
knn = KNeighborsClassifier(n_neighbors=best_k[1])
knn.fit(X_train,y_train)

# Predict the 12 unknown (but full digits)
print('\n+++ UNKOWN RESULTS +++')
print(knn.predict(X_unknown_not_erased))

# Feature Engineering!
for i in range (39,64):

    # Ignore blank data (Note: Does not use floats)
    X_data_full[:,i] *= 0

# Predict the 10 unknown digits (half-erased)
print('\n+++ UNKOWN ERASED RESULTS +++')
print(knn.predict(X_unknown_erased))


"""
Comments and Results!

It was not too difficult to adapt the iris starter code. The most trouble I
had was with figuring out what errors were thrown by knn built in methods. The 
erased digits wasn't too hard. In fact, my predictions did not change whether 
I weighted the blank pixels or not.

Best Cross Validation Score: 0.98988095238095242
K Value that Produced Score: 3
Prediction Results: 

Not erased:
9
9
5
5
6
5
0
9
8
9
8
4

Partially erased:
0
0
0
1
7
7
7
4
0
9
"""