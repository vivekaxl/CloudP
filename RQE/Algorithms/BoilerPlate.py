from __future__ import division
import pandas as pd


class BoilerPlate(object):
    def __init__(self, filename, training_percent=0.4):
        self.data_filename = filename
        self.training_percentage = training_percent
        self.independent_columns = None
        self.dependent_columns = None
        self.training_independent = None
        self.training_dependent = None
        self.testing_independent = None
        self.testing_dependent = None
        self.get_data()

    def get_data(self, base=30):
        data = pd.read_csv(self.data_filename)
        columns = data.columns
        self.independent_columns = [c for c in columns if "$<" not in c]
        self.dependent_columns = [c for c in columns if "$<" in c]
        assert(len(self.independent_columns) + len(self.dependent_columns) == len(columns)), "Something is wrong"

        # Divide Training and Testing such that all the data from cluster >= 30 and above is in testing dataset

        train = data[data['$2 '] < base]
        test = data[data['$2 '] >= base]

        assert(len(train.index) + len(test.index) == len(data.index)), "Something is wrong"

        self.training_independent = train[self.independent_columns].reset_index(drop=True)
        self.training_dependent = train[self.dependent_columns].reset_index(drop=True)

        self.testing_independent = test[self.independent_columns].reset_index(drop=True)
        self.testing_dependent = test[self.dependent_columns].reset_index(drop=True)

        assert(len(self.training_independent.index) + len(self.testing_independent.index) == len(data.index))\
            , "Something is wrong"

    def get_testing_data(self):
        return self.testing_independent, self.testing_dependent
