import numpy as np
import pandas
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

test_url = '../ds/pamap2/full_pamap.csv'

# prepare models
models = []
# different bagging methods
models.append(('RFC',  RandomForestClassifier()))
models.append(('GBC', AdaBoostClassifier()))

def get_data(url, sep=","):
    return pandas.read_csv(url, sep=sep)

def split_data(test_size=0.33):
    data = get_data(url=test_url)

    array = data.values
    # bad_indices = np.where(np.isnan(array))
    # array[bad_indices] = 0

    X = array[:, 1:15]
    y = np.ravel(array[:, 0:1])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    return X_train, X_test, y_train, y_test

results, names = [], []
X_train, X_test, y_train, y_test = split_data()

for name, model in models:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    predictions = [round(value) for value in y_pred]
    res = accuracy_score(y_test, predictions) * 100.0

    results.append(res)
    names.append(name)
    print(name, res)

# boxplot algorithm comparison
# todo check why only first model is plotted
# fig = plt.figure()
# fig.suptitle('Algorithm Comparison')
# ax = fig.add_subplot(111)
# plt.boxplot(results)
# ax.set_xticklabels(names)
# plt.show()
