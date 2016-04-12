import requests
import numpy as np
import leargist
from PIL import Image
from io import BytesIO

__author__ = 'helias'


class Painting:
    similarities_matrix = None  #numpy matrix of similarities

    @classmethod
    def get_max(cls):
        """
        This is a class method, meaning that it belongs to class and not to particular instances.
        It returns the pair of the most similar paintings if similarities_matrix is populated, -1,-1 else
        Similarities of 1. are not considered
        :return: Integer, Integer
        """
        if Painting.similarities_matrix is None: i, j = -1, -1
        else:
            similarities = Painting.similarities_matrix
            similarities[similarities == 1.] = -1.
            # np.fill_diagonal(similarities, -1.0)
            i, j = np.unravel_index(similarities.argmax(), similarities.shape)
            similarities[similarities == -1.] = 1.
        return i, j

    @classmethod
    def get_min(cls):
        """
        This is a class method, meaning that it belongs to class and not to particular instances.
        It returns the pair of the least similar paintings if similarities_matrix is populated, -1,-1 else
        :return: Integer, Integer
        """
        if Painting.similarities_matrix is None: i, j = -1, -1
        else:
            similarities = Painting.similarities_matrix
            similarities[similarities == 0.] = 2.
            i, j = np.unravel_index(similarities.argmin(), similarities.shape)
            similarities[similarities == 2.] = 0.
        return i, j

    def __init__(self, id_number, year, author, url, school):
        self.__id = id_number
        self.__year = year
        self.__author = author
        self.__url = url
        self.__school = school
        self.__features = None
        self.__innovation = np.nan
        self.__retro = np.nan
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

    def get_school(self):
        return self.__school

    def set_features(self, features):
        self.__features = features

    def get_features(self):
        return self.__features

    def set_innovation(self, innovation):
        self.__innovation = innovation

    def get_innovation(self):
        return self.__innovation

    def set_retro(self, retro):
        self.__retro = retro

    def get_retro(self):
        return self.__retro

    def get_similarity(self, image_id):
        if Painting.similarities_matrix is None: return -1.0
        else: return Painting.similarities_matrix[self.__id, image_id]

    def get_max_similarity(self, tolerance=0.0):
        """
        returns the index of the most similar painting if similarities are already calculated, -1.0 else
        :param tolerance: Some paintings appear twice because they belong to two different artists.
        So they have similarity 1.0. This parameter should be close to zero (e.g. e^-8 in order to reject
        values close to 1.0 by more than tolerance
        :return: Integer
        """
        if Painting.similarities_matrix is None: return -1.0
        else:
            row = Painting.similarities_matrix[self.__id, :].copy()
            row[self.__id] = -1.0
            if tolerance > 0.0: row[row > 1.0-tolerance] = -1.0
            res = row.argmax()
            del row
            return res

    def get_min_similarity(self):
        """
        returns the index of the least similar painting if similarities are already calculated, -1.0 else
        :return: Integer
        """
        if Painting.similarities_matrix is None: return -1.0
        else:
            row = Painting.similarities_matrix[self.__id].copy()
            row[row == 0.] = 2.
            res = row.argmin()
            del row
            return res

    def save_painting(self, file_name=None):
        """
        save_painting loads the painting given the url and saves it to disc under /images/ directory
        :param file_name: if it is None it just saves the image to disc.
        If there is a file name it saves the path to the image to that file.
        This file is used later to generate classemes and picodes features
        :return:
        """
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
        if file_name is not None:
            file_name.write(path[3:]+name+'.png\n')

    def load_features(self, feats=['GIST', 'picodes2048', 'classemes'], features_path='../features/images/', images_path='../images/'):
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
            feats.remove('GIST')
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

        for feat_name in feats:
            file_name = features_path+self.__name+'_'+feat_name+'.dat'
            feat = np.fromfile(file_name, dtype='float32')
            feat = feat[2:]
            features.extend(feat.tolist())

        features = np.array(features)
        norm = np.linalg.norm(features)
        self.__features = features/norm

    def __str__(self):
        return 'id: '+str(self.__id)+' year: '+str(self.__year)+' inno: '+str(self.__innovation)
