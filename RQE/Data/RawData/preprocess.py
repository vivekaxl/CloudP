from __future__ import division
import pandas as pd
import numpy as np


def get_series_ids(x):
    """Function returns a pandas series consisting of ids,
       corresponding to objects in models pandas series x
       Example:
       get_series_ids(pd.Series(['a','a','b','b','c']))
       returns Series([0,0,1,1,2], dtype=int)"""

    values = np.unique(x)
    values2nums = dict(zip(values,range(len(values))))
    return x.replace(values2nums)


def process_data(data_file):
    df = pd.read_csv(data_file, header=False)
    fields = df.columns
    for field in fields:
        if df[field].dtypes != np.float64 and df[field].dtypes != np.int64:
            df[field] = get_series_ids(df[field])

    independent_fields = [f for f in df.columns if "$<" not in f]
    # dependent_fields = [f for f in df.columns if "$<" in f]

    # All together
    df.to_csv('p_' + data_file, index=False)

    # Diving the objectives into seperate datasets
    df[independent_fields + ['$<1']].to_csv(data_file + '_o1', index=False)
    df[independent_fields + ['$<2']].to_csv(data_file + '_o2', index=False)
    df[independent_fields + ['$<3']].to_csv(data_file + '_o3', index=False)


if __name__ == "__main__":
    data_files = ["collector.csv"]
    for data_file in data_files:
        process_data(data_file)