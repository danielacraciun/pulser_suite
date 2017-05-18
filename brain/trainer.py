import os
import pandas
import pickle
import numpy as np

from datetime import datetime
from sklearn.ensemble import RandomForestClassifier

# Fetching latest generated file, ensuring completeness
train = os.path.join(os.path.dirname(__file__), 'datasets/full_pamap.csv')
test = os.path.join(os.path.dirname(__file__), 'datasets/spare_test.csv')
# latest_file = max(dir, key=os.path.getctime)

# Reading latest dataset contents into variables
data = pandas.read_csv(train, sep=',')
array = data.values
X = array[:, 1:15]
y = np.ravel(array[:, 0:1])

# Fit the model on fetched data
model = RandomForestClassifier()
model.fit(X, y)

data = pandas.read_csv(test, sep=',')
array = data.values
X = array[:, 1:15]
y = np.ravel(array[:, 0:1])

# Save the model to disk
today = datetime.now()
filename = 'model_{}{}{}{}.sav'.format(today.hour, today.minute, today.day, today.month)
pickle.dump(model, open(filename, 'wb'))