import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi

NESARC = r"C:\Users\USER\Documents\Courses\Coursera\dai\datasets\nesarc\nesarc_pds.csv"

# Loading data
data = pd.read_csv(NESARC, low_memory=False)


# FIELDS
# FIELDS
CANNABIS_USE_12M = 'S3BD5Q2C'  # 'HOW OFTEN USED CANNABIS IN THE LAST 12 MONTHS'
HEALTH_PERCEPTION = 'S1Q16'  # 'SELF-PERCEIVED CURRENT HEALTH'


# Convert values to numeric
data[CANNABIS_USE_12M] = pd.to_numeric(data[CANNABIS_USE_12M], errors='coerce')
data[HEALTH_PERCEPTION] = pd.to_numeric(data[HEALTH_PERCEPTION], errors='coerce')


CANNABIS_USE_CAT_MAP = {
    1: "Every day",
    2: "Nearly every day",
    3: "3 to 4 times a week",
    4: "1 to 2 times a week",
    5: "2 to 3 times a month",
    6: "Once a month",
    7: "7 to 11 times a year",
    8: "3 to 6 times a year",
    9: "2 times a year",
    10: "Once a year",
    99: "Unknown",
    "BL": "NA, did not use cannabis in the last 12 months"
}

# Recoding values so that they reflect approximately number of times per last year

CANNABIS_USE_TIMES_MAP = {
    1: 365,
    2: 330,
    3: 182,
    4: 104,
    5: 75,
    6: 12,
    7: 9,
    8: 4.5,
    9: 2,
    10: 1,
    11: 0
}

# Get counts for CANNABIS_USE_12M
cannabis_count = data[CANNABIS_USE_12M].value_counts(sort=False, dropna=False)
print(cannabis_count)

# Recode meaningful NaN (to 11, N/A) and 'Unknowns' (99 to NaN)
data[CANNABIS_USE_12M] = data[CANNABIS_USE_12M].replace(np.NaN, 11).replace(99, np.NaN)
print(data[CANNABIS_USE_12M].value_counts(sort=False, dropna=False))


def recode_values(row):
    return CANNABIS_USE_TIMES_MAP[row[CANNABIS_USE_12M]]


CANNABIS_USE_QUANT = 'CANNABIS_USE_QUANT'

data[CANNABIS_USE_QUANT] = data.apply(lambda row: recode_values(row), axis=1)

data[CANNABIS_USE_QUANT] = pd.to_numeric(data[CANNABIS_USE_QUANT], errors='coerce')

