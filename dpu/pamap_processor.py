"""
This file contains running and processing of PAMAP2 activity set from UCI repository
"""
import pandas
from numpy import ravel

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer
from xgboost import XGBClassifier

from constants import PAMAP_HEADERS
from model_processor import Processor
from utils import timing
import logging

# todo: scale down the feature set by clearly measuring feature importance and availability
class PamapProcessor(Processor):
    def __init__(self, url=None, size=0, nan_replacement=0, impute=False, predict_dataset=None):
        super(PamapProcessor, self).__init__(url=url, size=size, cols=PAMAP_HEADERS)
        self.rn = nan_replacement
        self.impute = impute
        if not url:
            urls = self.dp.process_pamap()
            self.url = self.dp.join_pamap(urls)
            self.data = self.get_data(self.url, cols=PAMAP_HEADERS)
        if predict_dataset:
            dataframe = self.get_data(predict_dataset)
            ds = self.split_data(with_training=False)
            self.predict_ds = ds[0], ds[1]

    @timing
    def run(self, model=XGBClassifier(), verbose=False):
        """
        This method fits the data set on a model
        :return: accuracy percentage 
        """
        X_train, X_test, y_train, y_test = self.split_data()
        print("fitting data")
        model.fit(X_train, y_train, verbose=verbose)
        print("done fitting")
        self.model = model
        y_pred = model.predict(X_test)
        self.last_prediction = y_pred
        predictions = [round(value) for value in y_pred]
        accuracy = accuracy_score(y_test, predictions)
        return accuracy * 100.0

    def split_data(self, test_size=0.2, data=pandas.DataFrame(), with_training=True):
        """
        Here the data is split into test and training
        :return: (X, x, Y, y) tuple where X, Y is training set and x, y is validation set
        """
        # todo: data processing, remove redundant and unattainable values - shorten the dataset
        # todo: extend data with pdf table info - sex, age ???
        print("splitting data")
        activities = pandas.DataFrame(columns=['activity'])
        activities['activity'] = self.data['activity']

        dataframe = self.data.drop(self.data.columns[1], axis=1)
        if not self.impute:
            dataframe = dataframe.fillna(self.rn)
        X = dataframe.values
        y = ravel(activities.values) if with_training else activities.values
        if with_training:
            if self.impute:
                imputer = Imputer()
                X = imputer.fit_transform(X)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
            print("done splitting data")
            return X_train, X_test, y_train, y_test
        return X, y, None, None

