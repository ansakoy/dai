'''
This is Assignment 3 for the course Data Management and Visualization, which is the first
part of Data Analysis and Interpretation Specialization series by Wesleyan University.
'''

import pandas as pd
import numpy as np
import time


from global_vars import *


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
        return
    if ind_sort:
        # Sort numeric labels for the output
        print(pd.concat(dict(Frequencies=series_freq.sort_index(),
                        Percentages=series_percent.sort_index()), axis=1))
        return
    print(pd.concat(dict(Frequencies=series_freq,
                             Percentages=series_percent), axis=1))



def main():
    '''
    This function contains the main flow of the process of operating the data
    :return:
    '''
    # Load data
    data = pd.read_csv(DATA_SOURCE, low_memory=False)

    # Convert necessary values to numbers
    data[ANIMALS_MAP[CODE]] = pd.to_numeric(data[ANIMALS_MAP[CODE]], errors='coerce')
    data[ORIGIN_MAP[CODE]] = pd.to_numeric(data[ORIGIN_MAP[CODE]], errors='coerce')
    data[HEALTH_MAP[CODE]] = pd.to_numeric(data[HEALTH_MAP[CODE]], errors='coerce')

    # Convert Unknown and Other to NaN
    # data[ANIMALS_MAP[CODE]] = data[ANIMALS_MAP[CODE]].replace(9, np.nan)
    # data[ORIGIN_MAP[CODE]] = data[ORIGIN_MAP[CODE]].replace([98, 99], np.nan)
    # data[HEALTH_MAP[CODE]] = data[HEALTH_MAP[CODE]].replace(9, np.nan)

    # Get frequencies and percentages for animals phobia
    animals_freq = data[ANIMALS_MAP[CODE]].value_counts(sort=False, dropna=False)
    animals_percent = data[ANIMALS_MAP[CODE]].value_counts(sort=False, dropna=False, normalize=True)
    label_print(animals_freq, animals_percent, ANIMALS_MAP)

    # Get frequencies and percentages for origins distribution
    origins_freq = data[ORIGIN_MAP[CODE]].value_counts(dropna=False).head(10)
    origins_percent = data[ORIGIN_MAP[CODE]].value_counts(dropna=False, normalize=True).head(10)
    label_print(origins_freq, origins_percent, ORIGIN_MAP)

    # Get frequencies and percentages for perceived health distribution
    health_freq = data[HEALTH_MAP[CODE]].value_counts(sort=True, dropna=False)
    health_percent = data[HEALTH_MAP[CODE]].value_counts(sort=True, dropna=False, normalize=True)
    label_print(health_freq, health_percent, HEALTH_MAP)

    # Making a subset for only those with animal phobia
    raw_subset = data[(data[ANIMALS_MAP[CODE]] == 1)]

    subset = raw_subset.copy()

    # Distinguish pure and mixed AP cases

    # Replacing 'NO/Unknown' with zero in all specific phobias to count only YES responses
    for phobia in SPECIFIC_PHOBIAS:
        subset[phobia[CODE]] = subset[phobia[CODE]].replace([2, 9], 0)

    # Create a new variable that sums up values across all specific phobias if AP == 1. Suggestion:
    # Those > 1 are mixed
    subset[APPUREMIXED] = subset[ANIMALS_MAP[CODE]] + subset[HEIGHTS_MAP[CODE]] + subset[THUNDER_MAP[CODE]]\
                          + subset[WATER_MAP[CODE]] + subset[FLYING_MAP[CODE]] + subset[CROWD_MAP[CODE]]\
                          + subset[CLOSED_MAP[CODE]] + subset[BLOOD_MAP[CODE]] + subset[TRAVELING_MAP[CODE]]\
                          + subset[DENTIST_MAP[CODE]] + subset[HOSPITAL_MAP[CODE]] + subset[OUTSIDE_MAP[CODE]]
    print('\nValues distribution for new APPUREMIXED variable')
    print(pd.concat(dict(Frequencies=subset[APPUREMIXED].value_counts(sort=True, dropna=False),
                         Percentages=subset[APPUREMIXED].value_counts(sort=True, dropna=False, normalize=True)), axis=1))

    # Replacing all values >1 with zero
    print('\nValues distribution for modified APPUREMIXED (1 - Pure, 0 - Not Pure, i.e. mixed)')
    condition_for_replace = subset[APPUREMIXED] > 1
    subset.loc[condition_for_replace, APPUREMIXED] = 0
    print('\nValues distribution for new APPUREMIXED variable')
    print(pd.concat(dict(Frequencies=subset[APPUREMIXED].value_counts(sort=True, dropna=False),
                         Percentages=subset[APPUREMIXED].value_counts(sort=True, dropna=False, normalize=True)), axis=1))


if __name__ == '__main__':
    start = time.time()
    main()
    stop = time.time()
    print('Running time: {}'.format(stop - start))