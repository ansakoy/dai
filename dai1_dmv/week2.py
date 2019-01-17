'''
Some code to test the course material
'''

import pandas
# import numpy
import time

# from origins_ref import ORIGINS

CODE = 'code'
MEANING = 'meaning'
VALUES = 'values'

DATA_SOURCE = r"C:\Users\USER\Documents\Courses\Coursera\Data Analysis\nesarc\nesarc_pds.csv"
ANIMALS_MAP = {
    CODE:'S8Q1A1',
    MEANING: 'EVER HAD FEAR/AVOIDANCE OF INSECTS, SNAKES, BIRDS, OTHER ANIMALS',
    VALUES: '1 - Yes, 2 - No, 9 - Unknown'
}
AGE_MAP = {
    CODE: 'AGE',
    MEANING: 'AGE',
    VALUES: 'Age in years'
}
ORIGIN_MAP = {
    CODE: 'S1Q1E',
    MEANING: 'ORIGIN OR DESCENT',
    VALUES: 'Origin descriptions'
}
PERCEIVED_HEALTH = {
    CODE: 'S1Q16',
    MEANING: 'SELF-PERCEIVED CURRENT HEALTH',
    VALUES: '1. Excellent, 2. Very good, 3. Good, 4. Fair, 5. Poor, 9. Unknown'
}


def load_data(source):
    data = pandas.read_csv(source, low_memory=False)
    return data


def get_data_measures(source):
    data = load_data(source)
    num_rows = len(data)
    num_cols = len(data.columns)
    print('Num rows: {}\nNum cols: {}\n'.format(num_rows, num_cols))


def get_stats_via_value_counts(data, var_map):
    # data[var_map[CODE]] = data[var_map[CODE]].infer_objects()  # Convert values to numeric
    animals_vals = data[var_map[CODE]].value_counts(sort=False)
    animals_percent = data[var_map[CODE]].value_counts(sort=False, normalize=True)
    print('Counts for {} - {}, {}\n'.format(var_map[CODE], var_map[MEANING], var_map[VALUES]))
    print(animals_vals)
    print('Percentages for {} - {}, {}\n'.format(var_map[CODE], var_map[MEANING], var_map[VALUES]))
    print(animals_percent)


def get_stats_via_groupby(data, var_map):
    num_rows = len(data)
    # data[var_map[CODE]] = data[var_map[CODE]].infer_objects()  # Convert values to numeric
    print('[GROUPBY] Counts for {} - {}, {}'.format(var_map[CODE], var_map[MEANING], var_map[VALUES]))
    var_vals_group = data.groupby(var_map[CODE]).size()
    print(var_vals_group)
    print('[GROUPBY] Percentages for {} - {}, {}'.format(var_map[CODE], var_map[MEANING], var_map[VALUES]))
    var_percent_group = data.groupby(var_map[CODE]).size() * 100 / num_rows
    print(var_percent_group)


def get_subset_by_age(data):
    condition1 = data[AGE_MAP[CODE]] >= 60
    condition2 = data[AGE_MAP[CODE]] < 80
    condition3 = data[ANIMALS_MAP[CODE]] == 1
    subset = data[(condition1 & condition2 & condition3)]
    # Make a copy of subset:
    subset2 = subset.copy()
    # get_stats_via_value_counts(subset2, AGE_MAP[CODE])
    # get_stats_via_value_counts(subset2, ANIMALS_MAP[CODE])
    by_age = subset2[AGE_MAP[CODE]].value_counts(sort=False)
    by_age_percent = subset2[AGE_MAP[CODE]].value_counts(sort=False, normalize=True)
    print(by_age)
    print(by_age_percent)


def main():
    data = load_data(DATA_SOURCE)
    # get_stats_via_groupby(data, AGE_MAP)
    # get_subset_by_age(data)
    get_stats_via_groupby(data, ORIGIN_MAP)


if __name__ == '__main__':
    start = time.time()
    main()
    stop = time.time()
    print('Running time: {}'.format(stop - start))