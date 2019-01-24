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
    data[ORIGIN_MAP[CODE]] = data[ORIGIN_MAP[CODE]].replace([98, 99], np.nan)
    data[HEALTH_MAP[CODE]] = data[HEALTH_MAP[CODE]].replace(9, np.nan)

    # Get percentages / frequencies of AP by origin
    
    # Get frequencies by origin
    # origins = data[ORIGIN_MAP[CODE]].value_counts(sort=False, dropna=False)  # With NaN
    origins = data[ORIGIN_MAP[CODE]].value_counts(sort=False, dropna=True)  # Without NaN
    # print('\nOrigins frequencies')
    # print(origins.rename(ORIGIN_MAP[VALUES]))

    # print('\nOrigins with AP frequencies')
    # Get origin frequencies based on the condition that respondents have animal phobia
    condition = data[ANIMALS_MAP[CODE]] == 1
    # origins_with_ap = data[condition][ORIGIN_MAP[CODE]].value_counts(sort=False, dropna=False)  # With NaN
    origins_with_ap = data[condition][ORIGIN_MAP[CODE]].value_counts(sort=False, dropna=True)  # Without NaN
    # print(origins_with_ap.rename(ORIGIN_MAP[VALUES]))

    # Create a new dataframe out of these two frequency series
    origins_df = origins.rename(ORIGIN_MAP[VALUES]).to_frame(name='ORIGCOUNTS')
    origins_df['ORIGAPCOUNTS'] = origins_with_ap.rename(ORIGIN_MAP[VALUES])

    # Create a new column in this new df to store percentages
    origins_df['APPERCENT'] = origins_df['ORIGAPCOUNTS'] / origins_df['ORIGCOUNTS']
    # print('\nOrigins vs. AP dataframe')
    # print(origins_df.sort_values(by=['APPERCENT'], ascending=False))
    # print('\nPrint only percentages')
    # print(origins_df['APPERCENT'].sort_values(ascending=False))


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
    has_ap = data[ANIMALS_MAP[CODE]] == 1
    has_pure_ap = data[APPUREMIXED] == 1
    origins_pure_ap = data[(has_ap & has_pure_ap)][ORIGIN_MAP[CODE]].value_counts(sort=False, dropna=False)
    # print('\nFrequencies of pure animal phobia by origin')
    # print(origins_pure_ap.rename(ORIGIN_MAP[VALUES]))

    # Adding pure AP frequencies to my new dataframe
    origins_df['NUMWITHPUREAP'] = origins_pure_ap.rename(ORIGIN_MAP[VALUES])
    origins_df['PUREAPPERCENTALL'] = origins_df['NUMWITHPUREAP'] / origins_df['ORIGCOUNTS']
    origins_df['PUREAPPERCENTWITHIN'] = origins_df['NUMWITHPUREAP'] / origins_df['ORIGAPCOUNTS']
    # print('\nOrigins vs. AP dataframe - UPDATED')
    # print(origins_df.sort_values(by=['APPERCENT'], ascending=False))
    # print(origins_df.sort_values(by=['ORIGCOUNTS'], ascending=False))

    # Make a subset for origins with 400 or more respondents
    subset_orig_gte_400 = origins_df[origins_df['ORIGCOUNTS'] >= 400].copy()
    # print('Origins subset (gte 400 respondents)')
    # print(subset_orig_gte_400.sort_values(by=['APPERCENT'], ascending=False))
    #
    # print('\nOrigins subset (gte 400 respondents) - (colnum, rownum)')
    # print(subset_orig_gte_400.shape)
    print('\nAPPERCENT solo')
    print(subset_orig_gte_400['APPERCENT'].sort_values(ascending=False))


    # Processing health perception

    # Get percentages for perceived health distribution (for all)
    health_percent = data[HEALTH_MAP[CODE]].value_counts(sort=False, dropna=True, normalize=True)

    # health perception vs. animal phobia
    health_ap_percent = data[data[ANIMALS_MAP[CODE]] == 1][HEALTH_MAP[CODE]].value_counts(sort=False, dropna=True, normalize=True)

    # health perception vs. pure animal phobia
    health_pure_ap_percent = data[(has_ap & has_pure_ap)][HEALTH_MAP[CODE]].value_counts(sort=False, dropna=True,
                                                                                          normalize=True)

    print('\nCompared distribution percentages for Perceived Health')
    print(pd.concat(dict(Dataset=health_percent.rename(HEALTH_MAP[VALUES]),
                         AnimalPhobia=health_ap_percent.rename(HEALTH_MAP[VALUES]),
                         PureAnimalPhobia=health_pure_ap_percent.rename(HEALTH_MAP[VALUES])), axis=1))


if __name__ == '__main__':
    start = time.time()
    main()
    stop = time.time()
    print('Running time: {}'.format(stop - start))