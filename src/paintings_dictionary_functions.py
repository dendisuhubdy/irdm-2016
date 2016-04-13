import numpy as np
import pandas as pd

from classes.Painting import Painting

__author__ = 'helias'


# def get_max_min_pairs(paintings):
#     """
#     get_max_min_pair: finds the most similar and least similar of paintings over a collection of them
#     :param paintings: dictionary from any key (here an integer) to a Painting object
#     :return: max_similarity, pair of keys that correspond to most similar paintings (key1, key2),
#     min_similarity, pair of keys that correspond to least similar paintings as tuple (key3, key4)
#     """
#     max_pair = (0, 0)
#     min_pair = (0, 0)
#     max_sim = 0.0
#     min_sim = 1.0
#     for key in paintings.keys():
#         most_similar = paintings.get(key).get_max_similarity()
#         least_similar = paintings.get(key).get_min_similarity()
#
#         sim_most = paintings.get(key).get_similarity(most_similar)
#         sim_least = paintings.get(key).get_similarity(least_similar)
#
#         if sim_most > max_sim:
#             max_sim, max_pair = sim_most, (key, most_similar)
#         if sim_least < min_sim:
#             min_sim, min_pair = sim_least, (key, least_similar)
#
#     return max_sim, max_pair, min_sim, min_pair


def set_innovations(paintings, years, similarities, alpha=0.5):
    """
    A method that sets an innovation score for each painting, based on the similarities between paintings
    The creativity for the painting i is denoted as C(p_i). So based on "Quantifying Creativity in Art Networks":
    C(p_i) = (1-a)/N + a SUM_j (similarity_ij C(p_j)/ N(p_j)) where N(p_j) = SUM_k (similarity_kj)
    :param paintings: a dictionary from any key (here an int or painting id) to a Painting object
    :param years: a dictionary from any year to a list of Painting objects that exact year
    :param alpha: parameter 0.<=alpha<=1.
    :return: It updates the innovative field of all Painting objects
    """
    # estimates (1-a)/N
    n = len(paintings)
    creativity_const = (1. - alpha)/n

    min_year = min(years.keys())
    max_year = max(years.keys())

    # estimate creativities of paintings in year min_year
    for p in years.get(min_year, list()):
        p.set_innovation(creativity_const)

    # estimate creativities of paintings the years after
    for year in range(min_year+1, max_year+1):
        # list of paintings in this specific year
        paintings_in_year = years.get(year, list())

        # iterate through all paintings in this specific year
        for painting in paintings_in_year:
            # get painting id
            pid = painting.get_id()

            # get id of all paintings that influenced current painting
            # this will be the id of all non zero elements in pid column in similarities matrix
            column = similarities[:, pid]
            paintings_ids_influenced_current = np.nonzero(column)[0].tolist()
            # paintings_ids_influenced_current = np.argpartition(column, -4)[-4:]

            # estimate creativity of painting
            creativity_painting = 0.

            for past_id in paintings_ids_influenced_current:
                # get painting object with id past_id
                painting_influenced_current = paintings.get(past_id)

                # similarity between painting_influenced_current and painting
                similarity = similarities[past_id, pid]
                similarity = 1. - similarity

                # estimate parameter N(p_j) = SUM (similarity_kj)
                # all paintings that painting_influenced_current influenced
                past_row = similarities[past_id, :]
                past_row = past_row[past_row > 0.]
                n_p_j = np.sum(1. - past_row)
                del past_row

                creativity_painting += similarity*painting_influenced_current.get_innovation()/n_p_j

            creativity_painting *= alpha
            creativity_painting += creativity_const
            painting.set_innovation(creativity_painting)


def set_retro(paintings, years, similarities, alpha=0.5):
    """

    :param paintings:
    :param years:
    :param similarities:
    :param alpha:
    :return:
    """
    n = len(paintings)
    creativity_const = (1. - alpha)/n

    min_year = min(years.keys())
    max_year = max(years.keys())

    # estimate retro score of paintings
    for year in range(min_year, max_year+1):
        # list of paintings in this specific year
        paintings_in_year = years.get(year, list())

        # iterate through all paintings in this specific year
        for painting in paintings_in_year:
            # get painting id
            pid = painting.get_id()

            # get id of all paintings that influenced current painting
            # this will be the id of all non zero elements in pid column in similarities matrix
            column = similarities[:, pid]
            paintings_ids_influenced_current = np.nonzero(column)[0].tolist()
            # paintings_ids_influenced_current = np.argpartition(column, -4)[-4:]

            # estimate creativity of painting
            retro_painting = 0.

            for past_id in paintings_ids_influenced_current:
                # get painting object with id past_id
                painting_influenced_current = paintings.get(past_id)

                # similarity between painting_influenced_current and painting
                similarity = similarities[past_id, pid]

                # estimate parameter N(p_j) = SUM (similarity_kj)
                # all paintings that painting_influenced_current influenced
                past_row = similarities[past_id, :]
                past_row = past_row[past_row > 0.]
                n_p_j = np.sum(past_row)
                del past_row

                retro_painting += similarity*painting_influenced_current.get_innovation()/n_p_j

            retro_painting *= alpha
            retro_painting += creativity_const
            painting.set_retro(retro_painting)


def paintings_to_csv(paintings, path='../results/'):
    frame = pd.DataFrame(columns=['Year', 'Author', 'School', 'URL', 'Innovation', 'Retro'])
    for p in paintings.values():
        frame = frame.append({'Year': p.get_year(), 'Author': p.get_author(),
                              'School': p.get_school(), 'URL': p.get_url(),
                              'Innovation': p.get_innovation(), 'Retro': p.get_retro()},
                             ignore_index=True)
    frame.to_csv(path+'data_with_innovations.csv', encoding='utf8', index=False)
    # writer = pd.ExcelWriter(path+'data.xlsx')
    # frame.to_excel(writer, encoding='utf8', index=False)
    # writer.save()


def keep_col_k(matr, k):
    mask = np.zeros(matr.shape, dtype=np.int8)
    rows, columns = matr.shape
    for col in range(0, columns):
        column = matr[:, col]
        indices = np.argpartition(column, -k)[-k:].tolist()
        for ind in indices: mask[ind, col] = 1
    matr = np.multiply(mask, matr)
    del mask
    return matr

