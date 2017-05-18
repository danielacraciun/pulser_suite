"""
This file contains running and processing of SA Heart Disease data set
"""
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

from model_processor import Processor
from utils import timing


class SaProcessor(Processor):
    def __init__(self, size, url=None):
        super(SaProcessor, self).__init__(size=size)
        self.data = super(SaProcessor, self).get_data(url, sep= ",", header=0)
        if not url:
            self.url = self.dp.process_sa()[0]
            self.data = self.get_data(self.url)

    @timing
    def run(self, model=XGBClassifier(), verbose=False):
        X_train, X_test, y_train, y_test = self.split_data(data=self.process_data())
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        predictions = [round(value) for value in y_pred]
        accuracy = accuracy_score(y_test, predictions)
        return accuracy * 100.0

    def process_data(self):
        mapping = {'Present': 1, 'Absent': 2}
        dataframe = self.data.applymap(lambda s: mapping.get(s) if s in mapping else s)
        return dataframe