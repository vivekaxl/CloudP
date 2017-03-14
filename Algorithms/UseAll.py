from __future__ import division
from BoilerPlate import BoilerPlate


class UseAll(BoilerPlate):
    def __init__(self, filename, training_percentage=0.4):
        super(UseAll, self).__init__(filename, training_percentage)
        self.model_independent, self.model_dependent = self.get_model_data()

    def get_model_data(self):
        model_independent = self.training_independent.values.tolist()
        model_dependent = [l[-1] for l in self.training_dependent.values.tolist()]

        return model_independent, model_dependent

    def get_training_data(self):
        return self.model_independent, self.model_dependent
