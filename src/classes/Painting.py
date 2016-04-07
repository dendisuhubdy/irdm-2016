import requests
import numpy as np
from PIL import Image
from io import BytesIO

__author__ = 'helias'


class Painting:

    def __init__(self, id_number, year, author, url, school):
        self.__id = id_number
        self.__year = year
        self.__author = author
        self.__url = url
        self.__school = school
        self.__features = None
        self.__similarities = None
        self.__innovation = np.nan
        self.__set_name()

    def __set_name(self):
        name = self.__url
        name = name[23:]
        name = name[:-5]
        name = name.replace('/', '_')
        self.__name = name

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__id

    def get_year(self):
        return self.__year

    def get_author(self):
        return self.__author

    def get_url(self):
        return self.__url

    def set_features(self, features):
        self.__features = features

    def get_features(self):
        return self.__features

    def set_innovation(self, innovation):
        self.__innovation = innovation

    def get_innovation(self):
        return self.__innovation

    def set_similarities(self, similarities_list):
        similarities_list[self.__id] = np.nan
        self.__similarities = similarities_list

    def get_similarity(self, image_id):
        return self.__similarities[image_id]

    def get_max_similarity(self):
        return self.__similarities.index(np.nanmax(np.asarray(self.__similarities)))

    def get_min_similarity(self):
        return self.__similarities.index(np.nanmin(np.asarray(self.__similarities)))

    def save_painting(self, file=None):
        name = self.__name
        path = '../images/'

        image_url = self.__url.replace('/html', '/detail')
        image_url = image_url.replace('.html', '.jpg')

        # download image
        response = requests.get(image_url)
        painting_file = BytesIO(response.content)
        img = Image.open(painting_file)

        # save image
        img.save(path+name+'.png')

        if file is not None:
            file.write(path[3:]+name+'.png\n')

    def __str__(self):
        return 'id: '+str(self.__id)+' year: '+str(self.__year)+' inno: '+str(self.__innovation)
