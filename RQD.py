from __future__ import division
from Algorithms.FactorialDesign import FactorialDesign
from Algorithms.UseAll import UseAll
from Algorithms.RankProgressive import RankProgressive
from Algorithms.MMREProgressive import MMREProgressive
from Performance.Performance import Performance
from sklearn.tree import DecisionTreeRegressor
from Algorithms.utility import find_non_dominated_solutions, find_igd
import sys
import os

# Can Throughput be predicted based on the configuration and workload information
repeats = 20
data_dir = "./Data/Provider/"
filenames = [data_dir + file for file in os.listdir(data_dir)]
methods = [FactorialDesign, UseAll, RankProgressive, MMREProgressive]
results = {}
for filename in filenames:
    results[filename] = {}
    for method in methods:
        print method.__name__,
        results[filename][method.__name__] = {}
        results[filename][method.__name__]['min_rank'] = []
        results[filename][method.__name__]['training_size'] = []
        results[filename][method.__name__]['mmre'] = []
        for _ in xrange(repeats):
            print "# ",
            sys.stdout.flush()
            method_obj = method(filename)
            training_independent, training_dependent = method_obj.get_training_data()
            testing_independent, testing_dependent = method_obj.get_testing_data()
            performance_obj = Performance(training_independent, training_dependent,
                                          testing_independent, testing_dependent)
            min_rank, training_size = performance_obj.find_min_rank(DecisionTreeRegressor())
            mmre, _ = performance_obj.find_mmre(DecisionTreeRegressor())
            results[filename][method.__name__]['min_rank'].append(min_rank)
            results[filename][method.__name__]['training_size'].append(training_size)
            results[filename][method.__name__]['mmre'].append(mmre)
        print

import pickle
pickle.dump(results, open('./PickleLocker/RQD.p', 'w'))