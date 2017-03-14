from __future__ import division
import numpy as np
from sklearn.tree import DecisionTreeRegressor


class Performance:
    def __init__(self, train_independent, train_dependent, test_independent, test_dependent):
        self.train_independent = train_independent
        self.train_dependent = train_dependent
        self.test_independent = test_independent.values.tolist()
        self.test_dependent = [l[-1] for l in test_dependent.values.tolist()]

    def find_min_rank(self,model=DecisionTreeRegressor(), bracket=10):
        # Sorting the test data Test data
        sorted_index = [i[0] for i in sorted(enumerate(self.test_dependent), key=lambda x:x[1])]
        assert(len(sorted_index) == len(self.test_dependent)), "Somethign is wrong"

        sorted_testing_independent = [self.test_independent[i] for i in sorted_index]
        sorted_testing_dependent = [self.test_dependent[i] for i in sorted_index]
        assert(sorted_testing_dependent[0] < sorted_testing_dependent[-1]), "Something is wrong"

        model.fit(self.train_independent, self.train_dependent)
        predicted = model.predict(sorted_testing_independent)

        # Adding actual ranks. This is because the testing data has been sorted based on the dependent values
        actual_ranks = [[i, p] for i, p in enumerate(predicted)]
        # Sorting based on predicted values
        predicted_sorted = sorted(actual_ranks, key=lambda x: x[-1])
        # assigning predicted ranks
        predicted_rank_sorted = [[p[0], p[-1], i] for i,p in enumerate(predicted_sorted)]
        select_few = predicted_rank_sorted[:bracket]
        return min([sf[0] for sf in select_few]), len(self.train_dependent)

    def find_mmre(self, model=DecisionTreeRegressor()):

        model.fit(self.train_independent, self.train_dependent)
        predicted = model.predict(self.test_independent)

        mre = []
        for org, pred in zip(self.test_dependent, predicted):
            if org == 0: continue
            mre.append(abs(org - pred)/ abs(org))
        return round(np.mean(mre), 5) * 100, len(self.train_dependent)

    def find_abs_diff(self, model=DecisionTreeRegressor):
        model.fit(self.train_independent, self.train_dependent)
        predicted = model.predict(self.test_independent)

        abs_diff = []
        for org, pred in zip(self.test_dependent, predicted):
            abs_diff.append(abs(org - pred))
        return sum(abs_diff), len(self.train_dependent)


    def get_precitions(self, model=DecisionTreeRegressor()):
        model.fit(self.train_independent, self.train_dependent)
        predicted = model.predict(self.test_independent)
        return predicted
