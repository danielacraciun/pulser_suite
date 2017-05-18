"""
subject108 was chosen as sample because the actions cover
 the most activities (check details/PerformedActivitySummary.pdf)
 also reduces the row attributes to out discoverable ones and added relevant
"""
import matplotlib.pyplot as plt
import pandas
from numpy import ravel
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer
from sklearn.tree import DecisionTreeClassifier
from xgboost import plot_importance, XGBClassifier

from constants import PAMAP_HEADERS, pamap_details
from pamap_processor import PamapProcessor

test_url = '../ds/pamap2/Protocol/subject106.dat'
details = pamap_details[106]
pp = PamapProcessor(url=test_url, impute=True, size=53)
data = pp.get_data(test_url)

# Get the activity id for prediction
activities = pandas.DataFrame(columns=['activity'])
activities['activity'] = data[1]

# Remove unused columns:
# 0 - timestamp
# 1 - activity id, this is to predict
# 3 - body temperature, no way to fetch this
# 8-10 - inaccurate accel measurements, using the 16g ones

data.drop(data.columns[[0, 1, 3, 7, 8, 9]], axis=1, inplace=True)

# insert other details
for k, v in  zip(["sex", "age", "height", "weight"], details):
    data.insert(0, k, [v] * data.shape[0])
data.insert(0, "activity", activities['activity'])
print(data.iloc[:,range(15)])

# # data shape: hr 3*accel(16g) 3*gyro 3*magnetometer
# X = data.values[:, 0:14]
# y = ravel(activities.values)

# imputer = Imputer()
# X = imputer.fit_transform(X)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
# model = XGBClassifier()
# model.fit(X_train, y_train)
# y_pred = model.predict(X_test)
# predictions = [round(value) for value in y_pred]
# accuracy = accuracy_score(y_test, predictions)
# print(accuracy * 100)
#
# plot_importance(model)
# plt.show()
