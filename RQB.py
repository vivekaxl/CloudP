from __future__ import division
from Algorithms.FactorialDesign import FactorialDesign
from Algorithms.UseAll import UseAll
from Algorithms.RankProgressive import RankProgressive
from Algorithms.MMREProgressive import MMREProgressive
from Performance.Performance import Performance
from sklearn.tree import DecisionTreeRegressor
from Algorithms.utility import find_non_dominated_solutions, find_igd
import sys

repeats = 20
filenames = ["/Users/viveknair/GIT/CloudP/Data/Client/collector.csv_AverageSLA"]
methods = [UseAll, FactorialDesign, MMREProgressive, RankProgressive]
results = {}
for filename in filenames:
    results[filename] = {}
    for method in methods:
        results[method.__name__] = {}
        results[method.__name__]['predicted_PF'] = []
        results[method.__name__]['training_size'] = []
        results[method.__name__]['mmre'] = []
        results[method.__name__]['abs_diff'] = []
        results[method.__name__]['actual_PF'] = []
        results[method.__name__]['IGD'] = []

        print method,
        for _ in xrange(repeats):
            print "# ",
            sys.stdout.flush()
            method_obj = method(filename)
            training_independent, training_dependent = method_obj.get_training_data()
            testing_independent, testing_dependent = method_obj.get_testing_data()
            performance_obj = Performance(training_independent, training_dependent,
                                          testing_independent, testing_dependent)

            # converting to list of list
            testing_independent = testing_independent.values.tolist()
            testing_dependent = [l[-1] for l in testing_dependent.values.tolist()]

            predictions = performance_obj.get_precitions()
            # Add Cost
            two_objectives = []
            for prediction, indep in zip(predictions, testing_independent):
                # SLA, Cost
                two_objectives.append([prediction, indep[8] * 400 + indep[9] * 200 + indep[10] * 100 + indep[11] * 10])

            sorted_two = sorted(two_objectives, key=lambda x: x[0])
            # Find Pareto Front of predicted solution
            predicted_pareto_front_indexes = find_non_dominated_solutions(sorted_two)

            actual_pareto_front_independent = [testing_independent[i] for i in predicted_pareto_front_indexes]
            actual_pareto_front_dependent = [testing_dependent[i] for i in predicted_pareto_front_indexes]
            # Add Cost
            two_objectives = []
            for dep, indep in zip(actual_pareto_front_dependent, actual_pareto_front_independent):
                # SLA, Cost
                two_objectives.append([dep, indep[8] * 400 + indep[9] * 200 + indep[10] * 100 + indep[11] * 10])

            # remove duplicates
            test = {}
            for s in two_objectives:
                if s[0] in test.keys():
                    if s[1] == test[s[0]]: continue
                else:
                    test[s[0]] = s[1]

            two_objectives = []
            for key, value in test.iteritems() :
                two_objectives.append([key, value])

            mmre, training_size = performance_obj.find_mmre(DecisionTreeRegressor())
            abs_diff, _ = performance_obj.find_abs_diff(DecisionTreeRegressor())
            results[method.__name__]['training_size'].append(training_size)
            results[method.__name__]['mmre'].append(mmre)
            results[method.__name__]['abs_diff'].append(abs_diff)
            results[method.__name__]['predicted_PF'].append(two_objectives)

            print " || ",
            # Actual Pareto Front
            # Add Cost
            actual_two_objectives = []
            for dep, indep in zip(testing_dependent, testing_independent):
                actual_two_objectives.append([dep, indep[8] * 400 + indep[9] * 200 + indep[10] * 100 + indep[11] * 10])

            sorted_two = sorted(actual_two_objectives, key=lambda x: x[0])
            actual_pareto_front_index = find_non_dominated_solutions(sorted_two)
            actual_pareto_front_independent = [testing_independent[i] for i in actual_pareto_front_index]
            actual_pareto_front_dependent = [testing_dependent[i] for i in actual_pareto_front_index]
            # Add Cost
            actual_two_objectives = []
            for dep, indep in zip(actual_pareto_front_dependent, actual_pareto_front_independent):
                # SLA, Cost
                actual_two_objectives.append([dep, indep[8] * 400 + indep[9] * 200 + indep[10] * 100 + indep[11] * 10])

            # remove duplicates
            test = {}
            for s in actual_two_objectives:
                if s[0] in test.keys():
                    if s[1] == test[s[0]]: continue
                else:
                    test[s[0]] = s[1]

            actual_two_objectives = []
            for key, value in test.iteritems() :
                actual_two_objectives.append([key, value])

            results[method.__name__]['actual_PF'].append(actual_two_objectives)
            igd = find_igd(actual_two_objectives, two_objectives)
            results[method.__name__]['IGD'].append(igd)
            print
        print

import pickle
pickle.dump(results, open('./PickleLocker/RQB.p', 'w'))

