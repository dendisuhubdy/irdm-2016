import requests
import numpy as np
import leargist
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

        # write image path to listimages.txt file
        if file is not None:
            file.write(path[3:]+name+'.png\n')

    def load_features(self, feats=['GIST', 'picodes2048', 'classemes'], features_path='../features/', images_path='../images/'):
        """
        load_features takes as input the list of desired features and computes the unary feature vector
        :param feats: the features we want to take into account
        :param features_path: the path to the picodes and classemes features
        :param images_path: the path to the downloaded images -- In case images are not downloaded None.
        if images_path == None get image through url. Used for GIST features
        :return: It saves result in self.__features as a unary np.array
        """

        features = []
        if 'GIST' in feats:
            if images_path is None:
                image_url = self.__url.replace('/html', '/detail')
                image_url = image_url.replace('.html', '.jpg')

                # get image through url
                response = requests.get(image_url)
                painting_file = BytesIO(response.content)
                img = Image.open(painting_file)
            else:
                # load image from disc
                img = Image.open(images_path+self.__name+'.png')

            # compute GIST features and append to features
            features.extend(leargist.color_gist(img).tolist())

        for feat in feats:
            file_name = features_path+self.__name+'_'+feat+'.dat'

        features = np.array(features)
        norm = np.linalg.norm(features)
        self.__features = features/norm


    def __str__(self):
        return 'id: '+str(self.__id)+' year: '+str(self.__year)+' inno: '+str(self.__innovation)
