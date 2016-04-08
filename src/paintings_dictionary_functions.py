import numpy as np
import pandas as pd

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


def set_innovations(paintings, years, years_back=5, top_paintings=5):
    """
    set_innovations: for each Painting object in the paintings dictionary it sets an innovation metric.
    That is how innovative is this painting based on the similarity with paintings the previous years
    Formula: 1.0 - (1/n) * /sum_1^n d_i
    :param paintings: dictionary from any key (here an integer or painting id) to a Painting object
    :param years: dictionary from any year to a list of Painting objects created that exact year
    :param years_back: how many years of not similar paintings make a painting considered as innovative
    :param top_paintings: most similar paintings over the years_back period
    :return: It just updates the innovative field of all Paintings objects
    """
    for key in paintings:
        # for each painting
        painting = paintings.get(key)
        similarity_list = []

        # for the last years_back years find the top_paintings more similar paintings
        for year in range(painting.get_year()-years_back, painting.get_year()):

            # get a list of all paintings during 'year' year
            paintings_in_year = years.get(year, list())
            for painting_year in paintings_in_year:
                # for each painting during year calculate similarity
                similarity_list.append(painting.get_similarity(painting_year.get_id()))

        # if list is empty meaning no painting during the past year_back years is found
        if not similarity_list:
            innovation = 0.0
        else:
            # sort and take the average of top_paintings most similar paintings
            similarity_list.sort(reverse=True)
            similarity_list = similarity_list[:top_paintings]
            innovation = np.mean(similarity_list)

        # set innovation of the painting
        painting.set_innovation(1.0 - innovation)


# TODO have not checked that it works
def paintings_to_csv(paintings, innovations=True, path='../results/'):
    if innovations:
        frame = pd.DataFrame(columns=['Year', 'Author', 'School', 'URL', 'Innovation'])
        for key in paintings.keys:
            p = paintings.get(key)
            frame = frame.append({'Year': p.get_year(), 'Author': p.get_author(),
                                  'School': p.get_school(), 'URL': p.get_author,
                                  'Innovation': p.get_innovation()})
    frame.to_csv(path+'data_with_innovations.csv', ignore_index=True)
