from __future__ import division
from BoilerPlate import BoilerPlate
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor


class MMREProgressive(BoilerPlate):
    def __init__(self, filename, training_percentage=0.4):
        super(MMREProgressive, self).__init__(filename, training_percentage)
        self.model_independent, self.model_dependent = self.get_model_data()


    @staticmethod
    def mmre_progressive(train_independent, train_dependent, validation_independent, validation_dependent):
        model = DecisionTreeRegressor()
        model.fit(train_independent, train_dependent)
        predicted = model.predict(validation_independent)
        mre = []
        for org, pred in zip(validation_dependent, predicted):
            if org == 0: continue
            mre.append(abs(org - pred)/ abs(org))
        return np.mean(mre) * 100

    def get_model_data(self, validation_percentage=0.1, threshold=10):
        # Merging the training_independent and training_dependent
        merged_training = pd.concat([self.training_independent, self.training_dependent], axis=1)
        assert(len(merged_training.index) == len(self.training_dependent.index)), "Something is wrong"

        test = merged_training.sample(frac=validation_percentage, random_state=200)
        test = test.sort_values(self.dependent_columns)
        train = merged_training.drop(test.index)

        assert(len(train.index) + len(test.index) == len(merged_training.index)), "Something is wrong"

        training_independent = train[self.independent_columns].reset_index(drop=True).values.tolist()
        training_dependent = train[self.dependent_columns].reset_index(drop=True).values.tolist()

        validation_independent = test[self.independent_columns].reset_index(drop=True).values.tolist()
        validation_dependent = test[self.dependent_columns].reset_index(drop=True).values.tolist()
        validation_dependent = [v[-1] for v in validation_dependent]
        assert(validation_dependent[0] < validation_dependent[-1]), "Something is wrong"

        # Setting up for rank progressive
        initial_size = 10
        sub_train_indep = [training_indep for training_indep in training_independent[:initial_size]]
        sub_train_dep = [training_dep for training_dep in training_dependent[:initial_size]]

        steps = 0
        while (initial_size+steps) < len(training_independent) - 1:
            returned_mmre = self.mmre_progressive(sub_train_indep, sub_train_dep, validation_independent, validation_dependent)
            if returned_mmre < threshold: break
            steps += 1
            sub_train_indep.append(training_independent[initial_size+steps])
            sub_train_dep.append(training_dependent[initial_size+steps])
            assert(len(sub_train_indep) == len(sub_train_dep)), "Something is wrong"

        return sub_train_indep, sub_train_dep

    def get_training_data(self):
        return self.model_independent, self.model_dependent

if __name__ == "__main__":
    rank_design = MMREProgressive("/Users/viveknair/GIT/CloudP/Data/Client/collector.csv_EnergyConsumption")
    print rank_design.model_dependent
