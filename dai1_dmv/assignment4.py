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


def sort_health(row):
    '''
    Recoding values for perceived health
    :param row: row of a dataset
    :return: code value (int)
    '''
    good = [1, 2, 3, 4]
    if row[HEALTH_MAP[CODE]] in good:
        return 1
    else:
        return 0


def assign_region(row):
    '''
    Recoding values for origins to group them by region
    :param row: row of a dataset
    :return: value (region name, str)
    '''
    return REGIONS[row[ORIGIN_MAP[CODE]]]


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

    ### VISUALIZATIONS

    ## UNIVARIATE

    # Univariate 1: Plotting APPUREMIXED variable

    # Read APPUREMIXED data as categorical
    condition_ap = data[ANIMALS_MAP[CODE]] == 1
    subset_ap = data[condition_ap].copy()  # Make a subset of those with animal phobia
    subset_ap[APPUREMIXED] = subset_ap[APPUREMIXED].astype('category')
    subset_ap[APPUREMIXED] = subset_ap[APPUREMIXED].cat.rename_categories(['Mixed', 'Pure'])
    # seaborn.countplot(x=APPUREMIXED, data=subset_ap)
    # plt.xlabel('Types of Animal Phobia')
    # plt.title ('Distribution of Pure and Mixed Animal Phobia')
    # plt.show()

    # Univariate 1.1: Plotting original animal phobia variable

    # Read animal phobia data as categorical
    data[ANIMALS_MAP[CODE]] = data[ANIMALS_MAP[CODE]].replace(9, np.nan)
    data[ANIMALS_MAP[CODE]] = data[ANIMALS_MAP[CODE]].astype('category')
    data[ANIMALS_MAP[CODE]] = data[ANIMALS_MAP[CODE]].cat.rename_categories(ANIMALS_MAP[VALUES])
    # seaborn.countplot(x=ANIMALS_MAP[CODE], data=data)
    # plt.xlabel('Ever had fear/avoidance of insects, snakes, birds, other animals')
    # plt.title ('Distribution of Animal Phobia Cases')
    # plt.show()

    # Univariate 2: Plotting ORIGINS variable

    # Create subset for the 20 origins that have more than 400 occurrences (calculated in Assignment 3)
    condition_origin = data[ORIGIN_MAP[CODE]].isin(REGIONS)
    subset_origin = data[condition_origin].copy()

    # Add a new column with regions based on origin values

    # seaborn.countplot(subset_origin['REGION'])
    # plt.xlabel('Regions of Origin')
    # plt.xticks(rotation=20)
    # plt.title('Distribution by Regions of Origin')
    # plt.tight_layout()
    # plt.show()

    # Univariate 3: Plotting PERCEIVED HEALTH variable

    data[HEALTH_MAP[CODE]] = data[HEALTH_MAP[CODE]].astype('category')
    data[HEALTH_MAP[CODE]] = data[HEALTH_MAP[CODE]].cat.rename_categories(HEALTH_VALUES)
    # seaborn.countplot(data[HEALTH_MAP[CODE]])
    # plt.xlabel('Self-Preceived Current Health')
    # plt.title('Distribution by Health Perception')
    # plt.show()


    ## BIVARIATE

    # Bivariate 1 - Health
    # If a person with animal phobia perceives their health as good, is it reasonable to expect that their AP is pure?

    # group health categories into two
    subset_ap['HEALTHBINARY'] = subset_ap.apply(lambda row: sort_health(row), axis=1)
    # seaborn.catplot(x=APPUREMIXED, y='HEALTHBINARY', kind='bar', ci=None, data=subset_ap)
    # plt.xlabel('Type of Animal Phobia')
    # plt.ylabel('Proportion of Good Perceived Health')
    # plt.title('Perceived Health -> Type of AP')
    # plt.xticks(rotation=20)
    # plt.tight_layout()
    # plt.show()


    # Bivariate 2 - Region vs. Health Perception
    # Create a column with regions (as 'bins')
    # Is there any association between region and health perception? SPOILER: NO
    subset_origin['HEALTHBINARY'] = subset_ap.apply(lambda row: sort_health(row), axis=1)
    # seaborn.catplot(x='REGION', y='HEALTHBINARY', kind='bar', ci=None, data=subset_origin)
    # plt.xlabel('Region of Origin')
    # plt.ylabel('Proportion of Good Perceived Health')
    # plt.title('Region of Origin -> Perceived Health')
    # plt.xticks(rotation=20)
    # plt.tight_layout()
    # plt.show()


    # Bivariate 3: region -> AP (general)
    subset_origin[ANIMALS_MAP[CODE]] = subset_origin[ANIMALS_MAP[CODE]].replace(9, np.nan)
    subset_origin[ANIMALS_MAP[CODE]] = subset_origin[ANIMALS_MAP[CODE]].replace(2, 0)
    subset_origin[ANIMALS_MAP[CODE]] = subset_origin[ANIMALS_MAP[CODE]].astype('category')
    print(subset_origin[ANIMALS_MAP[CODE]].describe())
    subset_origin[ANIMALS_MAP[CODE]] = pd.to_numeric(subset_origin[ANIMALS_MAP[CODE]], errors='coerce')
    seaborn.catplot(x='REGION', y=ANIMALS_MAP[CODE], kind='bar', ci=None, data=subset_origin)
    plt.xlabel('Regions of Origin')
    plt.ylabel('Proportion of Animal Phobia')
    plt.title('Animal Phobia vs. Region of Origin')
    plt.xticks(rotation=20)
    plt.show()


    # Bivariate 4: region -> pure AP
    condition_ap_for_origin = subset_origin[ANIMALS_MAP[CODE]] == 1
    subset_origin_ap = subset_origin[condition_ap_for_origin].copy()
    subset_origin_ap[APPUREMIXED] = pd.to_numeric(subset_origin_ap[APPUREMIXED], errors='coerce')
    # seaborn.catplot(x='REGION', y=APPUREMIXED, kind='bar', ci=None, data=subset_origin_ap)
    # plt.xlabel('Regions of Origin')
    # plt.ylabel('Proportion of Pure Animal Phobia')
    # plt.title('Pure Animal Phobia vs. Region of Origin')
    # plt.xticks(rotation=20)
    # plt.show()


def distribute_origins_by_regions():
    '''
    Using a hand-made dictionary REGIONS_ORIGINS ({origin_name: region_name}), and ORIGINS_VALUES mapper,
    create a new dictionary {origin_category_code: region_name}
    '''
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