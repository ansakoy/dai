'''
This is Assignment 4 for the course Data Management and Visualization, which is the first
part of Data Analysis and Interpretation Specialization series by Wesleyan University.
'''

import pandas as pd
import numpy as np
import seaborn
import matplotlib.pyplot as plt
import time
from pprint import pprint


from global_vars import *
from reference import *


def main():
    '''
    This function contains the main flow of the process of operating the data
    :return: None
    '''
    # Load data
    data = pd.read_csv(DATA_SOURCE, low_memory=False)

    # Convert necessary values to numbers
    data[ANIMALS_MAP[CODE]] = pd.to_numeric(data[ANIMALS_MAP[CODE]], errors='coerce')
    data[ORIGIN_MAP[CODE]] = pd.to_numeric(data[ORIGIN_MAP[CODE]], errors='coerce')
    data[HEALTH_MAP[CODE]] = pd.to_numeric(data[HEALTH_MAP[CODE]], errors='coerce')

    # Convert Unknown and Other to NaN
    data[ORIGIN_MAP[CODE]] = data[ORIGIN_MAP[CODE]].replace([98, 99], np.nan)
    data[HEALTH_MAP[CODE]] = data[HEALTH_MAP[CODE]].replace(9, np.nan)

    # Create mixed vs. pure variable

    # Create new columns to store recoded values for different kinds of specific phobias
    for phobia in ALL_SPECIFIC_PHOBIAS:
        data[phobia[CODE] + '_NEW'] = data[phobia[CODE]].replace([2, 9], 0)
    sp_new_list = [entry[CODE] + '_NEW' for entry in ALL_SPECIFIC_PHOBIAS]  # creating a list of names for the new columns

    # Sum up all values for phobias in new columns and store the result in a new column 'APPUREMIXED'
    data[APPUREMIXED] = data.loc[:, sp_new_list].sum(axis=1)
    condition_for_replace = data[APPUREMIXED] > 1
    data.loc[condition_for_replace, APPUREMIXED] = 0  # replace values > 1 with 0
    appuremixed_freq = data[data[ANIMALS_MAP[CODE]] == 1][APPUREMIXED].value_counts(sort=False, dropna=False)
    appuremixed_percent = data[data[ANIMALS_MAP[CODE]] == 1][APPUREMIXED].value_counts(sort=False, dropna=False, normalize=True)

    print('\nFrequencies, percentages for pure and mixed animal phobia')
    print(pd.concat(dict(Frequencies=appuremixed_freq.rename({1: 'Pure', 0: 'Mixed'}),
                         Percentages=appuremixed_percent.rename({1: 'Pure', 0: 'Mixed'})), axis=1))

    # Univariate 1: Plotting APPUREMIXED variable

    # Read APPUREMIXED data as categorical
    # data[APPUREMIXED] = data[APPUREMIXED].astype('category')
    # data[APPUREMIXED] = data[APPUREMIXED].cat.rename_categories(['Mixed', 'Pure'])
    # seaborn.countplot(x=APPUREMIXED, data=data)
    # plt.xlabel('Types of Animal Phobia')
    # plt.title ('Distribution of Pure and Mixed Animal Phobia')
    # plt.show()


    # Univariate 1: Plotting ORIGINS variable

    # origins = data[ORIGIN_MAP[CODE]].value_counts(sort=False, dropna=False)
    # print(origins.rename(ORIGIN_MAP[VALUES]))

    # Create subset for the 20 origins that have more than 400 occurrences (calculated in Assignment 3)
    condition_origin = data[ORIGIN_MAP[CODE]].isin(REGIONS)
    subset_origin = data[condition_origin].copy()

    # Create a column with regions (as 'bins')
    def assign_region(row):
        return REGIONS[row[ORIGIN_MAP[CODE]]]

    subset_origin['REGION'] = subset_origin.apply(lambda row: assign_region(row), axis=1)
    seaborn.countplot(subset_origin['REGION'])
    plt.xlabel('Regions of Origin')
    plt.xticks(rotation=20)
    plt.title('Distribution by Regions of Origin')
    plt.show()



    # has_ap = data[ANIMALS_MAP[CODE]] == 1
    # has_pure_ap = data[APPUREMIXED] == 1





def distribute_origins_by_regions():
    result = dict()
    for entry in REGIONS_ORIGINS:
        for code in ORIGINS_VALUES:
            if entry == ORIGINS_VALUES[code]:
                region = REGIONS_ORIGINS[entry]
                result[code] = region
    print(len(result))
    pprint(result)
    unique_regions = set(list(result.values()))
    print('Num unique regions: {}'.format(len(unique_regions)))
    for reg in unique_regions:
        print(reg)
    return result


if __name__ == '__main__':
    start = time.time()
    main()
    # distribute_origins_by_regions()
    stop = time.time()
    print('Running time: {}'.format(stop - start))