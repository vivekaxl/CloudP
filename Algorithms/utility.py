from __future__ import division
import sys
from collections import defaultdict
import time

def find_closest_point(search_point, indep_points, dep_points):
    """
    To find point in points which is closed to search_point
    :param search_point:  point to be searched for
    :param points: all the points in the training data (pandas data frame
    :return: point closed to search_point
    """
    import numpy as np
    from scipy.spatial import distance
    nodes = np.asarray(indep_points)
    index_no = distance.cdist([search_point], nodes).argmin()
    return_point = nodes[index_no].tolist()

    return return_point, dep_points.iloc[index_no].tolist()[-1]


def binary_domination(one, two):
    """
    Binary Domination: We are trying to minimize both SLA and cost
    :param one: First solution
    :param two: Second solution
    :return: True if one dominates two; False otherwise
    """
    not_equal = False
    for o, t in zip(one, two):
        if o < t:
            not_equal = True
        elif t < o:
            return False
    return not_equal


def _binary_domination():
    ones = [[1, 1], [2, 2], [3, 3]]
    twos = [[0, 0], [2, 0], [4, 4]]

    assert(binary_domination(ones[0], twos[0]) is False), "Failed"
    assert(binary_domination(ones[1], twos[1]) is False), "Failed"
    assert(binary_domination(ones[2], twos[2]) is True), "Failed"
    print "Finished"


def find_non_dominated_solutions(individuals):
    non_dominated_indexes = []
    dominating_fits = defaultdict(int)
    for first_count, f_individual in enumerate(individuals):
        for second_count, s_individual in enumerate(individuals):
            if first_count != second_count:
                if binary_domination(f_individual, s_individual) is True:
                    dominating_fits[second_count] += 1
                elif binary_domination(s_individual, f_individual) is True:
                    dominating_fits[first_count] += 1
                    break

        if dominating_fits[first_count] == 0:
            print ". ",
            sys.stdout.flush()
            non_dominated_indexes.append(first_count)

    return non_dominated_indexes


def _find_non_dominated_solution():
    filename = "/Users/viveknair/GIT/CloudP/Data/Client/collector.csv_AverageSLA"
    import pandas as pd
    data = pd.read_csv(filename)
    columns = data.columns
    independent_columns = [c for c in columns if "$<" not in c]
    dependent_columns = [c for c in columns if "$<" in c]
    independent = data[independent_columns].values.tolist()
    dependent = [d[-1] for d in data[dependent_columns].values.tolist()]
    two_objectives = []

    for indep,dep in zip(independent, dependent):
        cost = indep[8] * 400 + indep[9] * 200 + indep[10] * 100 + indep[11] * 10
        # Two dependent values are Energy Consumption and cost
        two_objectives.append([dep, cost])

    sorted_two = sorted(two_objectives, key=lambda x: x[0])

    non_dominated_indexes = find_non_dominated_solutions(sorted_two)

    import matplotlib.pyplot
    matplotlib.pyplot.scatter([s[0] for s in sorted_two],[s[1] for s in sorted_two])
    matplotlib.pyplot.show()

    test = {}
    for s in [sorted_two[i] for i in non_dominated_indexes]:
        if s[0] in test.keys():
            if s[1] == test[s[0]]: continue
        else:
            test[s[0]] = s[1]
    for key, value in test.iteritems() :
        print key, value
    matplotlib.pyplot.scatter([sorted_two[i][0] for i in non_dominated_indexes],[sorted_two[i][1] for i in non_dominated_indexes])
    matplotlib.pyplot.show()


def find_igd(original_points, approximation_points):
    def euclidean_distance(list1, list2):
        assert(len(list1) == len(list2)), "The points don't have the same dimension"
        distance = sum([(i - j) ** 2 for i, j in zip(list1, list2)])
        assert(distance >= 0), "Distance can't be less than 0"
        return distance

    # Normalize
    total = original_points + approximation_points
    assert(len(original_points) + len(approximation_points) == len(total)), "Something is wrong"

    for i in xrange(len(original_points[0])):
        column_extract = [t[i] for t in total]
        min_no = min(column_extract)
        max_no = max(column_extract)

        for t in total:
            t[i] = (t[i] - min_no)/(max_no - min_no)

    original_points = total[:len(original_points)]
    approximation_points = total[len(original_points):]
    assert(len(original_points) + len(approximation_points) == len(total)), "Something is wrong"

    summ = 0
    for o in original_points:
        min_distance = 1e32
        for a in approximation_points:
            min_distance = min(min_distance, euclidean_distance(o, a))
        summ += min_distance
    return summ/len(original_points)

if __name__ == "__main__":
    _find_non_dominated_solution()