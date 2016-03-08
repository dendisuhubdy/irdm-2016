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
