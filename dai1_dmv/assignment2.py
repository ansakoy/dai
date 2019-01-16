'''
This is Assignment 2 for the course Data Management and Visualization, which is the first
part of Data Analysis and Interpretation Specialization series by Wesleyan University.
'''

import pandas as pd
import time

import reference  # Here are references for values for each variable that requires labelling

# Source file name
DATA_SOURCE = "nesarc_pds.csv"

# Globals (using them to avoid errors caused by typos)
CODE = 'code'
MEANING = 'meaning'
VALUES = 'values'
SINGLE_VAR_TITLE = '\nResults for {} - {}\n'

# Maps to keep variables and their descriptions in order
ANIMALS_MAP = {
    CODE:'S8Q1A1',
    MEANING: 'EVER HAD FEAR/AVOIDANCE OF INSECTS, SNAKES, BIRDS, OTHER ANIMALS',
    VALUES: reference.ANIMALS_VALUES
}
AGE_MAP = {
    CODE: 'AGE',
    MEANING: 'AGE',
    VALUES: 'Age in years'
}
ORIGIN_MAP = {
    CODE: 'S1Q1E',
    MEANING: 'ORIGIN OR DESCENT',
    VALUES: reference.ORIGINS_VALUES
}
HEALTH_MAP = {
    CODE: 'S1Q16',
    MEANING: 'SELF-PERCEIVED CURRENT HEALTH',
    VALUES: reference.HEALTH_VALUES
}


def label_print(series_freq, series_percent, series_map, rename=True, ind_sort=False):
    '''
    Print the output of an operation with all captions and labels needed
    :param series_freq: which series frequency to print out
    :param series_percent: which series percentages to print out
    :param series_map: set the dictionary describing the series
    :param rename: True by default; if True, replaces index with the given labels
    :param ind_sort: False by default; if True, sort index values (good for sorting numeric index)
    :return: None
    '''
    print(SINGLE_VAR_TITLE.format(series_map[CODE], series_map[MEANING]))
    if rename:
        # Use labels for the output
        print(pd.concat(dict(Frequencies=series_freq.rename(series_map[VALUES]),
                             Percentages=series_percent.rename(series_map[VALUES])), axis=1))
    if ind_sort:
        # Sort numeric labels for the output
        print(pd.concat(dict(Frequencies=series_freq.sort_index(),
                        Percentages=series_percent.sort_index()), axis=1))
    elif not rename and not ind_sort:
        # print(series)
        print(pd.concat(dict(Frequencies=series_freq,
                             Percentages=series_percent), axis=1))


def main():
    '''
    This function contains the whole process of operating the data
    :return: None
    '''
    # Load data
    data = pd.read_csv(DATA_SOURCE, low_memory=False)

    # Get general measurements of the dataset
    num_rows = len(data)
    num_cols = len(data.columns)
    print('Num rows: {}\nNum cols: {}\n'.format(num_rows, num_cols))

    # Get frequencies and percentages for animals phobia
    animals_freq= data[ANIMALS_MAP[CODE]].value_counts(sort=False)
    animals_percent = data[ANIMALS_MAP[CODE]].value_counts(sort=False, normalize=True)
    label_print(animals_freq, animals_percent, ANIMALS_MAP)

    # Get frequencies and percentages for origins distribution

    # origins_freq = data[ORIGIN_MAP[CODE]].value_counts(sort=False, dropna=False)
    # origins_percent = data[ORIGIN_MAP[CODE]].value_counts(sort=False, dropna=False, normalize=True)
    origins_freq = data[ORIGIN_MAP[CODE]].value_counts(dropna=False)
    origins_percent = data[ORIGIN_MAP[CODE]].value_counts(dropna=False, normalize=True)
    label_print(origins_freq, origins_percent, ORIGIN_MAP)

    # Get the number of distinct categories in origin
    unique_origins = data[ORIGIN_MAP[CODE]].unique()
    print('num distinct origins:', len(unique_origins))

    # Get frequencies and percentages for perceived health distribution
    health_freq = data[HEALTH_MAP[CODE]].value_counts(sort=False, dropna=False)
    health_percent = data[HEALTH_MAP[CODE]].value_counts(sort=False, dropna=False, normalize=True)
    label_print(health_freq, health_percent, HEALTH_MAP)

    # Get frequencies and percentages for age distribution
    # data[AGE_MAP[CODE]] = pd.to_numeric(data[AGE_MAP[CODE]])  # Convert index to numbers
    # age_freq = data[AGE_MAP[CODE]].value_counts(sort=False, dropna=False)
    # age_percent = data[AGE_MAP[CODE]].value_counts(sort=False, dropna=False, normalize=True)
    # label_print(age_freq, age_percent, HEALTH_MAP, rename=False, ind_sort=True)

    # Making a subset of origins by animal phobia and health perception
    condition_ap = data[ANIMALS_MAP[CODE]] == 1
    condition_health = data[HEALTH_MAP[CODE]] == 5
    condition_origin = data[ORIGIN_MAP[CODE]].isin([1, 19, 15, 18, 27, 29, 36, 35, 39, 3])
    raw_subset = data[(condition_ap & condition_health & condition_origin)]
    subset = raw_subset.copy()
    print('\nSubset: top origins + poor perceived health + have AP')
    origins_ap_freq = subset[ORIGIN_MAP[CODE]].value_counts(sort=False)
    origins_ap_percent = subset[ORIGIN_MAP[CODE]].value_counts(sort=False, normalize=True)
    label_print(origins_ap_freq, origins_ap_percent, ORIGIN_MAP)


    # Making a subset of perceiced health by animal phobia and health perception
    raw_subset = data[(condition_ap)]
    subset_health_ap = raw_subset.copy()
    print('\nSubset: perceived health + have AP')
    health_ap_freq = subset_health_ap[HEALTH_MAP[CODE]].value_counts(sort=True, dropna=False)
    health_ap_percent = subset_health_ap[HEALTH_MAP[CODE]].value_counts(sort=True, dropna=False, normalize=True)
    label_print(health_ap_freq, health_ap_percent, HEALTH_MAP)


if __name__ == '__main__':
    start = time.time()
    main()
    stop = time.time()
    print('Running time: {}'.format(stop - start))