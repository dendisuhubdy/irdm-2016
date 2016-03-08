import requests
import numpy as np
from PIL import Image
from io import BytesIO

__author__ = 'Helias'


class Painting:

    def __init__(self, id_number, year, author, url, school, feature_vector):
        self.__id = id_number
        self.__year = int(year)
        self.__author = author
        self.__url = url
        self.__school = school
        self.__features = feature_vector
        self.__similarities = dict()
        self.__innovation = np.nan

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

    def set_innovation(self, innovation):
        self.__innovation = innovation

    def get_innovation(self):
        return self.__innovation

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

    def __str__(self):
        return 'id: '+str(self.__id)+' year: '+str(int(self.__year))
