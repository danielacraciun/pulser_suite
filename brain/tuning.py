import os
import numpy as np
import pandas
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

from constant import train_ds, test_ds

train = os.path.join(os.path.dirname(__file__), train_ds)
test = os.path.join(os.path.dirname(__file__), test_ds)

print("Reading training set")
data1 = pandas.read_csv(train, sep=',')
print("Reading test set")
data2 = pandas.read_csv(test, sep=',')

print("Splitting sets")
array1, array2 = data1.values, data2.values
X = array1[:, 1:15]
y = np.ravel(array1[:, 0:1])
Xt = array2[:, 1:15]
yt = np.ravel(array2[:, 0:1])

model = RandomForestClassifier()
param_grid = {
    'n_estimators': [16, ],
    'max_features': [1, 'sqrt', 10],
    'criterion': ['gini', 'entropy'],
    "bootstrap": [True, False],
    "max_depth": [None, 1, 5, 10],
    "min_samples_split": [3, 4, 5],
    "min_samples_leaf": [2, 3],
}

CV_rfc = GridSearchCV(estimator=model, param_grid=param_grid, cv=5)
CV_rfc.fit(X, y)
print(CV_rfc.best_params_)
print(CV_rfc.best_score_)