'''
Some code to test the course material
NB: The course provides downloadable Python scripts with example code from lectures.
These scripts are sometimes considerably different from the scripts shown in the videos.
So both sources may be instructive in terms of familiarizing with pandas and numpy
'''

import pandas as pd
import numpy as np
import time

import reference  # Here are references for values for each variable that requires labelling

# Source file name
DATA_SOURCE = "nesarc_pds.csv"
ADDHEALTH_SOURCE = r'C:\Users\USER\Documents\Courses\Coursera\dai\datasets\addhealth\addhealth_pds.csv'

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
    health_freq = data[HEALTH_MAP[CODE]].value_counts(sort=True, dropna=False)
    health_percent = data[HEALTH_MAP[CODE]].value_counts(sort=True, dropna=False, normalize=True)
    label_print(health_freq, health_percent, HEALTH_MAP)

    # Get frequencies and percentages for age distribution
    # data[AGE_MAP[CODE]] = pd.to_numeric(data[AGE_MAP[CODE]])  # Convert index to numbers
    # age_freq = data[AGE_MAP[CODE]].value_counts(sort=False, dropna=False)
    # age_percent = data[AGE_MAP[CODE]].value_counts(sort=False, dropna=False, normalize=True)
    # label_print(age_freq, age_percent, HEALTH_MAP, rename=False, ind_sort=True)

    # Making a subset by animal phobia and health perception
    condition_ap = data[ANIMALS_MAP[CODE]] == 1
    raw_subset = data[(condition_ap)]
    subset_health_ap = raw_subset.copy()

    # Change indices
    print('\nUsing map to rename indices')  # Throws error when remapping None
    subset_health_ap['NEW_COLUMN_FOR_HEALTH'] = subset_health_ap[HEALTH_MAP[CODE]].map(HEALTH_MAP[VALUES])
    print(subset_health_ap['NEW_COLUMN_FOR_HEALTH'].value_counts(sort=True, dropna=False))


    subset_health_ap[HEALTH_MAP[CODE]] = subset_health_ap[HEALTH_MAP[CODE]].replace(9, np.nan)
    print('\nSubset: perceived health + have AP')
    health_ap_freq = subset_health_ap[HEALTH_MAP[CODE]].value_counts(sort=True, dropna=False)
    health_ap_percent = subset_health_ap[HEALTH_MAP[CODE]].value_counts(sort=True, dropna=False, normalize=True)
    label_print(health_ap_freq, health_ap_percent, HEALTH_MAP)

    # Replace NaN with dummy code where necessary
    # data.loc[(data['S2AQ3'] != 9) & (data['S2AQ8A'].isnull()), 'S2AQ8A'] = 11
    # OR: sub2['S2AQ8A'].fillna(11, inplace=True)

    # Creating secondary variables


def examples_on_other_vars_nesarc():
    # code mostly from the course source
    data = pd.read_csv(DATA_SOURCE, low_memory=False)

    # bug fix for display formats to avoid run time errors
    # pd.set_option('display.float_format', lambda x: '%f' % x)

    # setting variables you will be working with to numeric
    data['TAB12MDX'] = pd.to_numeric(data['TAB12MDX'], errors='coerce')  # Set values to NaN if conversion is impossible
    data['CHECK321'] = pd.to_numeric(data['CHECK321'], errors='coerce')
    data['S3AQ3B1'] = pd.to_numeric(data['S3AQ3B1'], errors='coerce')
    data['S3AQ3C1'] = pd.to_numeric(data['S3AQ3C1'], errors='coerce')
    data['S2AQ8A'] = pd.to_numeric(data['S2AQ8A'], errors='coerce')
    data['AGE'] = pd.to_numeric(data['AGE'], errors='coerce')

    # subset data to young adults age 18 to 25 who have smoked in the past 12 months
    sub1 = data[(data['AGE'] >= 18) & (data['AGE'] <= 25) & (data['CHECK321'] == 1)]

    # make a copy of new subsetted data
    sub2 = sub1.copy()

    print('counts for original S3AQ3B1')
    S3AQ3B1_freq = sub2['S3AQ3B1'].value_counts(sort=False, dropna=False)
    print(S3AQ3B1_freq)

    # recode missing values to python missing (NaN)
    sub2['S3AQ3B1'] = sub2['S3AQ3B1'].replace(9, np.nan)
    sub2['S3AQ3C1'] = sub2['S3AQ3C1'].replace(99, np.nan)

    # if you want to include a count of missing add, dropna=False
    print('counts for S3AQ3B1 with 9 set to NAN and number of missing requested')

    S3AQ3B1_freq_with_nan = sub2['S3AQ3B1'].value_counts(sort=False, dropna=False)
    print(S3AQ3B1_freq_with_nan)

    # coding in valid data
    # recode missing values to numeric value, in this example replace NaN with 11
    sub2['S2AQ8A'].fillna(11, inplace=True)
    # OR: data.loc[(data['S2AQ3'] != 9) & (data['S2AQ8A'].isnull()), 'S2AQ8A'] = 11

    # recode 99 values as missing
    sub2['S2AQ8A'] = sub2['S2AQ8A'].replace(99, np.nan)

    print('S2AQ8A with Blanks recoded as 11 and 99 set to NAN')
    # check coding
    check_coding = sub2['S2AQ8A'].value_counts(sort=False, dropna=False)
    print(check_coding)
    sub2_described = sub2["S2AQ8A"].describe()  # Provides stats summary, so only applicable to numeric variables
    print(sub2_described)

    # recoding values for S3AQ3B1 into a new variable, USFREQ
    # recode_map1 = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}
    recode_map1 = {key: sorted(list(range(1, 7)), reverse=True)[key - 1] for key in range(1, 7)}
    print(recode_map1)
    sub2['USFREQ'] = sub2['S3AQ3B1'].map(recode_map1)
    print('Counts for USFREQ')
    print(sub2['USFREQ'].value_counts(sort=False, dropna=False))

    # recoding values for S3AQ3B1 into a new variable, USFREQMO, showing smoking day rate per month
    recode_map2 = {1: 30, 2: 22, 3: 14, 4: 5, 5: 2.5, 6: 1}
    sub2['USFREQMO'] = sub2['S3AQ3B1'].map(recode_map2)
    print('Counts for USFREQMO')
    print(sub2['USFREQMO'].value_counts(sort=False, dropna=False))

    # secondary variable multiplying the number of days smoked/month and the approx number of cig smoked/day
    sub2['NUMCIGMO_EST'] = sub2['USFREQMO'] * sub2['S3AQ3C1']
    print('Counts for NUMCIGMO_EST')
    print(sub2['NUMCIGMO_EST'].value_counts(sort=False, dropna=False))

    # Create a new subset based on the old one (include only necessary columns)
    sub3 = sub2[['IDNUM', 'S3AQ3C1', 'USFREQMO', 'NUMCIGMO_EST']]
    print('\nPrinting out sub3.head(25)')
    print(sub3.head(25))  # Print out only first 25 lines

    # examining frequency distributions for age
    print('\ncounts for AGE')
    age_freq = sub2['AGE'].value_counts(sort=False)
    print(age_freq)

    print('percentages for AGE')
    age_percent = sub2['AGE'].value_counts(sort=False, normalize=True)
    print(age_percent)

    # quartile split (use qcut function & ask for 4 groups - gives you quartile split)
    print('AGE - 4 categories - quartiles')
    sub2['AGEGROUP4'] = pd.qcut(sub2.AGE, 4, labels=["1=0%tile", "2=25%tile", "3=50%tile", "4=75%tile"])
    age_group_freq = sub2['AGEGROUP4'].value_counts(sort=False, dropna=True)
    print(age_group_freq)

    # categorize quantitative variable based on customized splits using cut function
    # splits into 3 groups (18-20, 21-22, 23-25) - remember that Python starts counting from 0, not 1
    sub2['AGEGROUP3'] = pd.cut(sub2.AGE, [17, 20, 22, 25])
    age_group_cut_freq = sub2['AGEGROUP3'].value_counts(sort=False, dropna=True)
    print(age_group_cut_freq)

    # crosstabs evaluating which ages were put into which AGEGROUP3
    print(pd.crosstab(sub2['AGEGROUP3'], sub2['AGE']))

    # frequency distribution for AGEGROUP3
    print('counts for AGEGROUP3')
    c10 = sub2['AGEGROUP3'].value_counts(sort=False)
    print(c10)

    print('percentages for AGEGROUP3')
    p10 = sub2['AGEGROUP3'].value_counts(sort=False, normalize=True)
    print(p10)


#ADDHEALTH EXAMPLE

def examples_addhealth():

    # load data
    data = pd.read_csv(ADDHEALTH_SOURCE, low_memory=False)

    # making individual ethnicity variables numeric
    data['H1GI4'] = pd.to_numeric(data['H1GI4'], errors='coerce')
    data['H1GI6A'] = pd.to_numeric(data['H1GI6A'], errors='coerce')
    data['H1GI6B'] = pd.to_numeric(data['H1GI6B'], errors='coerce')
    data['H1GI6C'] = pd.to_numeric(data['H1GI6C'], errors='coerce')
    data['H1GI6D'] = pd.to_numeric(data['H1GI6D'], errors='coerce')

    # Set missing data to NAN
    # data['H1GI4'] = data['H1GI4'].replace(6, np.nan)
    # data['H1GI4'] = data['H1GI4'].replace(8, np.nan)
    # data['H1GI6A'] = data['H1GI6A'].replace(6, np.nan)
    # data['H1GI6A'] = data['H1GI6A'].replace(8, np.nan)
    # data['H1GI6B'] = data['H1GI6B'].replace(6, np.nan)
    # data['H1GI6B'] = data['H1GI6B'].replace(8, np.nan)
    # data['H1GI6C'] = data['H1GI6C'].replace(6, np.nan)
    # data['H1GI6C'] = data['H1GI6C'].replace(8, np.nan)
    # data['H1GI6D'] = data['H1GI6D'].replace(6, np.nan)
    # data['H1GI6D'] = data['H1GI6D'].replace(8, np.nan)

    # A better way to do the same
    data['H1GI4'] = data['H1GI4'].replace([6, 8], np.nan)
    data['H1GI6A'] = data['H1GI6A'].replace([6, 8], np.nan)
    data['H1GI6B'] = data['H1GI6B'].replace([6, 8], np.nan)
    data['H1GI6C'] = data['H1GI6C'].replace([6, 8], np.nan)
    data['H1GI6D'] = data['H1GI6D'].replace([6, 8], np.nan)

    # Create new var with the count of number of ethnicity categories endorsed
    data['NUMETHNIC'] = data['H1GI4'] + data['H1GI6A'] + data['H1GI6B'] + data['H1GI6C'] + data['H1GI6D']

    print('\nCounts for NUMETHNIC value')
    numethnic_freq = data['NUMETHNIC'].value_counts(sort=False, dropna=False)
    print(numethnic_freq)

    # subset variables in new data frame, sub1
    sub1 = data[['AID', 'H1GI4', 'H1GI6A', 'H1GI6B', 'H1GI6C', 'H1GI6D', 'NUMETHNIC']]

    # new ETHNICITY variable, categorical 1 through 6
    def get_ethnicity(row):
        if row['NUMETHNIC'] > 1:
            return 1
        if row['H1GI4'] == 1:
            return 2
        if row['H1GI6A'] == 1:
            return 3
        if row['H1GI6B'] == 1:
            return 4
        if row['H1GI6C'] == 1:
            return 5
        if row['H1GI6D'] == 1:
            return 6

    sub1['ETHNICITY'] = sub1.apply(lambda row: get_ethnicity(row), axis=1)

    print('\nPrinting out the head of the new dataframe')
    print(sub1.head(25))

    # frequency distributions for primary and secondary ethinciity variables
    print('counts for Hispanic/Latino')
    c10 = sub1['H1GI4'].value_counts(sort=False)
    print(c10)

    print('percentages for Hispanic/Latino')
    p10 = sub1['H1GI4'].value_counts(sort=False, normalize=True)
    print(p10)

    print('counts for Black/African American')
    c11 = sub1['H1GI6A'].value_counts(sort=False)
    print(c11)

    print('percentages for Black/African American')
    p11 = sub1['H1GI6A'].value_counts(sort=False, normalize=True)
    print(p11)

    print('counts for American Indian/Native American')
    c12 = sub1['H1GI6B'].value_counts(sort=False)
    print(c12)

    print('percentages for American Indian/Native American')
    p12 = sub1['H1GI6B'].value_counts(sort=False, normalize=True)
    print(p12)

    print('counts for Asian/Pacific Islander')
    c13 = sub1['H1GI6C'].value_counts(sort=False)
    print(c13)

    print('percentages for Asian/Pacific Islander')
    p13 = sub1['H1GI6C'].value_counts(sort=False, normalize=True)
    print(p13)

    print('counts for White')
    c14 = sub1['H1GI6D'].value_counts(sort=False)
    print(c14)

    print('percentages for White')
    p14 = sub1['H1GI6D'].value_counts(sort=False, normalize=True)
    print(p14)

    print('counts for number of races/ethnicities endorsed')
    c15 = sub1['NUMETHNIC'].value_counts(sort=False)
    print(c15)

    print('counts for each Ethnic group')
    c16 = sub1['ETHNICITY'].value_counts(sort=False)
    print(c16)

    print('percentages for each Ethnic Group')
    p16 = sub1['ETHNICITY'].value_counts(sort=False, normalize=True)
    print(p16)





if __name__ == '__main__':
    start = time.time()
    # main()
    examples_on_other_vars_nesarc()
    # examples_addhealth()
    stop = time.time()
    print('Running time: {}'.format(stop - start))