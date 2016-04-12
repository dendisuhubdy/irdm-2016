import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

__author__ = 'helias'


def plot_histogram(similarities_matrix):
    """
    given a squared similarities matrix (symmetric) it plots the histogram of the upper triangle
    :param similarities_matrix: squared symmetric matrix
    :return: True
    """
    # keep only distinct similarities in order to build the histogram
    triangle = np.triu_indices(len(similarities_matrix), 1)
    distinct_similarities = np.squeeze(similarities_matrix[triangle])

    my_bins = np.linspace(.0, 1.0, 100)
    plt.hist(distinct_similarities, bins=my_bins)
    plt.show()

    return True


def plot_points_timeline(paintings, min_year, max_year, plot_type=['INNOVATION', 'RETRO']):
    year = []
    inno = []
    retro = []
    for p in paintings.values():
        if p.get_year() in range(min_year, max_year):
            year.append(p.get_year())
            inno.append(p.get_innovation())
            retro.append(p.get_retro())

    if 'INNOVATION' in plot_type: plt.plot(year, inno, 'o')
    if 'RETRO' in plot_type: plt.plot(year, retro, 'ro')
    plt.show()

    return True


def plot_timeline(years, min_year, max_year, plot_type=['INNOVATION', 'RETRO']):
    frame = pd.DataFrame(columns=['YEAR', 'INNOVATION', 'RETRO'])
    for year in years.keys():
        if year in range(min_year, max_year):
            innos = []
            retros = []
            for painting in years.get(year, list()):
                innos.append(painting.get_innovation())
                retros.append(painting.get_retro())
            if innos:
                frame = frame.append({'YEAR': year, 'INNOVATION': np.mean(innos),
                                      'RETRO': np.mean(retros)}, ignore_index=True)

    frame.set_index('YEAR', inplace=True)
    frame.sort_index(inplace=True)
    frame = frame[plot_type]
    frame.plot()
    plt.show()

    return True
