import pandas

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from data_processor import DataProcessor
from utils import timing


class Processor(object):
    """
    Interface for concrete processors
    """
    # todo: infer size from data set shape
    def __init__(self, url=None, size=0, cols=None):
        if url:
            self.url = url
            print("Processing: " + url)
            self.data = self.get_data(url, cols=cols)
        else:
            url = "unset"
        self.size = size
        self.dp = DataProcessor()
        self.model = None
        self.last_prediction = None

    @property
    def get_url(self):
        return self.url

    @property
    def get_model(self):
        if not self.model:
            raise AttributeError("The model has not been trained yet!")
        return self.model

    @timing
    def run(self, model=XGBClassifier(), verbose=False):
        """
        This method fits the data set on a model
        :return: accuracy percentage 
        """
        X_train, X_test, y_train, y_test = self.split_data()
        model.fit(X_train, y_train, verbose=verbose)
        self.model = model
        y_pred = model.predict(X_test)
        predictions = [round(value) for value in y_pred]
        accuracy = accuracy_score(y_test, predictions)
        return accuracy * 100.0

    def process_data(self):
        """
        Here any processing and/or reshaping of the data set is done
        :return: hdd_processed data
        """
        #todo: some better processing here, remove uneeded
        #todo: variable for univariate plot and other *clustering*
        return self.data

    def split_data(self, test_size=0.33, data=pandas.DataFrame(), with_training=True):
        """
        Here the data is split into test and training
        :return: (X, x, Y, y) tuple where X, Y is training set and x, y is validation set
        """
        array = data.values if not data.empty else self.process_data().values
        X = array[:, 0:self.size]
        y = array[:, self.size]
        if with_training:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
            return X_train, X_test, y_train, y_test
        return X, y, None, None


    def get_data(self, url, sep=" ", cols=None, header=None):
        """
        Fetching of the data in a specific way for the data set 
        (may be reimplemented for special cases)
        :return: dataframe of the data set
        """
        csv =  pandas.read_csv(url, sep=sep, header=header)
        if cols:
            csv.columns = cols
        return csv