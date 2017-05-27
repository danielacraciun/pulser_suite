import os
import pandas
import pickle
import numpy as np

from datetime import datetime
from sklearn.ensemble import RandomForestClassifier

# Fetching latest generated file, ensuring completeness
from constant import trained_models_folder, train_ds, test_ds

train = os.path.join(os.path.dirname(__file__), train_ds)
test = os.path.join(os.path.dirname(__file__), test_ds)
# latest_file = max(dir, key=os.path.getctime)

# Reading latest dataset contents into variables
data = pandas.read_csv(train, sep=',')
array = data.values
X = array[:, 1:15]
y = np.ravel(array[:, 0:1])

# Fit the model on fetched data
model = RandomForestClassifier()
model.fit(X, y)

# Save the model to disk
today = datetime.now()
filename = '{}/model_{}{}{}{}.sav'.format(trained_models_folder, today.hour, today.minute, today.day, today.month)
pickle.dump(model, open(filename, 'wb'))