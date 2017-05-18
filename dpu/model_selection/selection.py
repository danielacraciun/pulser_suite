import matplotlib.pyplot as plt
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from processors.pamap_processor import PamapProcessor

test_url = '../ds/pamap2/Optional/subject106.dat'

# prepare models
models = []
# todo: bagged vs boosted algorithm comparison
models.append(('CART', DecisionTreeClassifier()))
models.append(('RFC',  RandomForestClassifier()))
models.append(('AdaBoost',  AdaBoostClassifier()))
models.append(('NaiveB',  GaussianNB()))
models.append(('XGB', XGBClassifier()))
# todo: check why svc takes too long
# svc takes abnormally long, excluded
# models.append(('SVM', SVC()))

results, names = [], []
pp = PamapProcessor(url=test_url, impute=True, size=53)
for name, model in models:
    res = pp.run(model)
    results.append(res)
    names.append(name)
    print(name, res)

# boxplot algorithm comparison
# todo check why only first model is plotted
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()
