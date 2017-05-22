import numpy as np
import pandas
from matplotlib import pyplot as plt
from sklearn import model_selection
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, BaggingClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, KFold
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

test_url = '../ds/full_pamap3.csv'

# prepare models
models = []
# different bagging methods
models.append(('NaiveB', GaussianNB()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('RFC', RandomForestClassifier()))
models.append(('GBC', GradientBoostingClassifier()))
models.append(('Bagging KNN', BaggingClassifier(KNeighborsClassifier(), max_samples=0.5, max_features=0.5)))
models.append(('Ada', AdaBoostClassifier()))

def get_data(url, sep=","):
    return pandas.read_csv(url, sep=sep)


def split_data(test_size=0.33):
    data = get_data(url=test_url)

    array = data.values
    bad_indices = np.where(np.isnan(array))
    array[bad_indices] = 0

    X = array[:, 1:15]
    y = np.ravel(array[:, 0:1])
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    return X, y


results, names = [], []
X, Y = split_data()

# evaluate each model in turn
seed = 7
scoring = 'accuracy'
for name, model in models:
    print("starting {}".format(name))
    kfold = KFold(n_splits=2, random_state=seed)
    cv_results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

# boxplot algorithm comparison
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
fig.savefig("fig1.png")
