import pandas as pd
import numpy as np

__author__ = 'helias'


def loadDataset(path, starting_year=0, ordered=True):
    data = pd.read_excel(path)
    data = data[data.FORM == 'painting']
    data = data[['AUTHOR', 'DATE', 'URL', 'SCHOOL']]
    data.reset_index(drop=True, inplace=True)

    data['YEAR'] = data.DATE.apply(getYear)
    data.dropna(subset=['YEAR'], inplace=True)
    data.reset_index(drop=True, inplace=True)

    data = data[data.YEAR >= starting_year]
    data.reset_index(drop=True, inplace=True)

    # TODO if not ordered shuffle the dataset
    if ordered:
        data.sort_values(by=['YEAR'], inplace=True)
        data.reset_index(drop=True, inplace=True)
    else:
        data = data.reindex(np.random.permutation(data.index))
        data.reset_index(drop=True, inplace=True)

    data = data[['AUTHOR', 'YEAR', 'URL', 'SCHOOL']]

    return data


def getYear(x):
    if type(x) is unicode:
        x = x.encode('utf-8', 'ignore')
        # x = x.encode('ascii', 'ignore')
    x = str(x)
    if len(x) < 4:
        return np.nan
    else:
        result =''
        for i in range(0, len(x)-3):
            sub_string = x[i:i+4]
            if allNumbers(sub_string):
                result = sub_string
                break
        if len(result) == 4:
            return int(result)
        else:
            return np.nan


def allNumbers(x):
    flag = True
    for letter in x:
        if letter not in '0123456789':
            flag = False
    return flag