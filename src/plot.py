import numpy as np
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


def plot_points_timeline(paintings, min_year, max_year):
    year = []
    inno = []
    for p in paintings.values():
        if p.get_year() in range(min_year, max_year):
            year.append(p.get_year())
            inno.append(p.get_innovation())

    plt.plot(year, inno, 'o')
    plt.show()

    return True
