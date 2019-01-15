'''
Counting rows in datasets
'''


import csv

NAME = 'name'
LOCATION = 'location'



ADDHEALTH = {LOCATION: r"C:\Users\USER\Documents\Courses\Coursera\dai\datasets\addhealth\addhealth_pds.csv",
             NAME: 'ADDHEALTH'}
OOL = {LOCATION: r"C:\Users\USER\Documents\Courses\Coursera\dai\datasets\ool\ool_pds.csv",
             NAME: 'OOL'}

GAPMINDER = {LOCATION: r"C:\Users\USER\Documents\Courses\Coursera\dai\datasets\gapminder\gapminder.csv",
             NAME: 'GAPMINDER'}

MARS = {LOCATION: r"C:\Users\USER\Documents\Courses\Coursera\dai\datasets\marscraters\marscrater_pds.csv",
             NAME: 'MARS'}

NESARC = {LOCATION: r"C:\Users\USER\Documents\Courses\Coursera\dai\datasets\nesarc\nesarc_pds.csv",
             NAME: 'NESARC'}


def count_lines(name, source):
    num_lines = 0
    with open(source, 'r', encoding='utf-8') as handler:
        reader = csv.reader(handler)
        for dummy in reader:
            num_lines += 1
    print('{}: {} lines'.format(name, num_lines - 1))


if __name__ == '__main__':

    count_lines(ADDHEALTH[NAME], ADDHEALTH[LOCATION])
    count_lines(MARS[NAME], MARS[LOCATION])
    count_lines(OOL[NAME], OOL[LOCATION])
    count_lines(NESARC[NAME], NESARC[LOCATION])
    count_lines(GAPMINDER[NAME], GAPMINDER[LOCATION])


# OUTPUT:

# ADDHEALTH: 6504 lines
# MARS: 384343 lines
# OOL: 2294 lines
# NESARC: 43093 lines
# GAPMINDER: 213 lines