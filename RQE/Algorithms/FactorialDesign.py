from __future__ import division
from BoilerPlate import BoilerPlate
from pyDOE import *
from utility import find_closest_point


class FactorialDesign(BoilerPlate):
    def __init__(self, filename, training_percentage=0.4):
        super(FactorialDesign, self).__init__(filename, training_percentage)
        self.model_independent, self.model_dependent = self.get_model_data()

    def get_model_data(self):
        # Find minimum values of all the columns
        min_values = self.training_independent.min().tolist()
        # Find maximum values of all the columns
        max_values = self.training_independent.max().tolist()

        # Dictionary to store the levels of dataset
        other_dict = {}
        converter_dict = {}

        # sorting list of strings based on values
        keys = sorted(self.training_independent.columns.tolist(), key=lambda x: float(''.join(x.split('$')[1:])))
        for i, key in enumerate(keys):
            # Ignore columns which has not variation
            if min_values[i] == max_values[i]:
                other_dict[key] = {0.0: min_values[i], 1.0: max_values[i]}
                continue
            converter_dict[key] = {0.0: min_values[i], 1.0: max_values[i]}

        # Columns to be considered
        columns = converter_dict.keys()
        designs = fullfact([2 for _ in xrange(len(columns))]).tolist()
        independent_columns = []
        for design in designs:
            row = []
            count = 0
            for key in keys:
                if key in converter_dict.keys():
                    row.append(converter_dict[key][design[count]])
                    count += 1
                else:
                    row.append(other_dict[key][0.0])
            assert(len(row) == len(keys)), "Something is wrong"
            independent_columns.append(row)
        assert(len(designs) == len(independent_columns)), "Somethign is wrong"

        return_training_independent = []
        return_training_dependent = []

        for row in independent_columns:
            data = self.training_independent
            # generating panda query to check where the independent rows generated exists in the data frame
            args = {}
            for i, key in enumerate(keys):
                args[key] = [row[i]]
            for key in keys:
                # print key, args[key],
                data = data[data[key].isin(args[key])]
                # print len(data)
            if len(data) == 0:
                # find the closed point
                # Optimization

                indep_value, dep_value = find_closest_point(row, self.training_independent, self.training_dependent)

            return_training_independent.append(indep_value)
            return_training_dependent.append(dep_value)
        print "finished fetching data", len(return_training_dependent)
        # assert(len(return_training_dependent) == len(independent_columns)), "Something is wrong"
        print "Length of data: ", len(return_training_dependent)
        return return_training_independent, return_training_dependent

    def get_training_data(self):
        return self.model_independent, self.model_dependent


if __name__ == "__main__":
    fact_design = FactorialDesign("/Users/viveknair/GIT/CloudP/Data/Client/collector.csv_EnergyConsumption")
    print fact_design.test_model_dt()