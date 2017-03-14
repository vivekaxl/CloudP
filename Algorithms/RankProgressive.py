from __future__ import division
from BoilerPlate import BoilerPlate
import pandas as pd
import numpy as np


class RankProgressive(BoilerPlate):
    def __init__(self, filename, training_percentage=0.4):
        super(RankProgressive, self).__init__(filename, training_percentage)
        self.model_independent, self.model_dependent = self.get_model_data()

    @staticmethod
    def policy1(scores, lives=4):
        """
        no improvement in last 4 runs
        """
        temp_lives = lives
        last = scores[0]
        for i,score in enumerate(scores):
            if i > 0:
                if temp_lives == 0:
                    return i
                elif score >= last:
                    temp_lives -= 1
                    last = score
                else:
                    temp_lives = lives
                    last = score
        return -1

    @staticmethod
    def rank_progressive(train_independent, train_dependent, validation_independent, validation_dependent):
        # Note that we do not use the validation dependent since the validation data is presorted
        from sklearn.tree import DecisionTreeRegressor
        model = DecisionTreeRegressor()
        model.fit(train_independent, train_dependent)
        predicted = model.predict(validation_independent)
        # assigning actual rank, since validation datasets are already sorted
        actual_validation_order = [[i,p] for i,p in enumerate(predicted)]
        predicted_sorted = sorted(actual_validation_order, key=lambda x: x[-1])
        # assigning predicted ranks
        predicted_rank_sorted = [[p[0], p[-1], i] for i,p in enumerate(predicted_sorted)]
        rank_diffs = [abs(p[0] - p[-1]) for p in predicted_rank_sorted]
        return np.mean(rank_diffs)

    def get_model_data(self, validation_percentage=0.1):
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
        rank_diffs = []
        while (initial_size+steps) < len(training_independent) - 1:
            rank_diffs.append(self.rank_progressive(sub_train_indep, sub_train_dep, validation_independent, validation_dependent))
            policy_result = self.policy1(rank_diffs)
            if policy_result != -1: break
            steps += 1
            sub_train_indep.append(training_independent[initial_size+steps])
            sub_train_dep.append(training_dependent[initial_size+steps])
            assert(len(sub_train_indep) == len(sub_train_dep)), "Something is wrong"

        return sub_train_indep, sub_train_dep

    def get_training_data(self):
        return self.model_independent, self.model_dependent

if __name__ == "__main__":
    rank_design = RankProgressive("/Users/viveknair/GIT/CloudP/Data/Client/collector.csv_EnergyConsumption")
    print rank_design.test_model_dt()
