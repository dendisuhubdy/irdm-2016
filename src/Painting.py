import requests
import numpy as np
from PIL import Image
from io import BytesIO

__author__ = 'Helias'


class Painting:

    def __init__(self, id_number, year, author, url, school, feature_vector):
        self.__id = id_number
        self.__year = year
        self.__author = author
        self.__url = url
        self.__school = school
        self.__features = feature_vector
        self.__similarities = dict()

    def get_id(self):
        return self.__id

    def get_year(self):
        return self.__year

    def get__author(self):
        return self.__author

    def get_url(self):
        return self.__url

    def get_features(self):
        return self.__features

    def set_similarity(self, image_id, score):
        self.__similarities[image_id] = score

    def get_similarity(self, image_id):
        return self.__similarities.get(image_id, 0.0)

    def get_max_similarity(self):
        return max(self.__similarities, key=self.__similarities.get)

    def get_min_similarity(self):
        return min(self.__similarities, key=self.__similarities.get)

    def save_painting(self, path='../images/'):
        name = self.__url
        name = name[25:]
        name = name[:-5]
        name = name.replace('/', '_')

        # download image
        response = requests.get(self.__url)
        painting_file = BytesIO(response.content)
        img = Image.open(painting_file)

        # save image
        img.save(path+name+'.png')


def get_distinct_similarities(paintings):
    """
    get_distinct_similarities: Given a collection of Painting objects (dictionary) returns the similarity
    between each pair excluding similarities between one painting with itself
    :param paintings: dictionary from any key (here an integer) to a Painting object
    :return: an numpy array of all similarities between each pair of paintings
    """
    distinct_similarities = []
    for key1 in paintings.keys():
        for key2 in paintings.keys():
            if key1 < key2:
                distinct_similarities.append(paintings.get(key1).get_similarity(key2))
    return np.array(distinct_similarities)


def get_max_min_pairs(paintings):
    """
    get_max_min_pair: finds the most similar and least similar of paintings over a collection of them
    :param paintings: dictionary from any key (here an integer) to a Painting object
    :return: max_similarity, pair of keys that correspond to most similar paintings (key1, key2),
    min_similarity, pair of keys that correspond to least similar paintings as tuple (key3, key4)
    """
    max_pair = (0, 0)
    min_pair = (0, 0)
    max_sim = 0.0
    min_sim = 1.0
    for key in paintings.keys():
        most_similar = paintings.get(key).get_max_similarity()
        least_similar = paintings.get(key).get_min_similarity()

        sim_most = paintings.get(key).get_similarity(most_similar)
        sim_least = paintings.get(key).get_similarity(least_similar)

        if sim_most > max_sim:
            max_sim, max_pair = sim_most, (key, most_similar)
        if sim_least < min_sim:
            min_sim, min_pair = sim_least, (key, least_similar)

    return max_sim, max_pair, min_sim, min_pair
