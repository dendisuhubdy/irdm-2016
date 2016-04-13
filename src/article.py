import time

import numpy as np

from sklearn.preprocessing import normalize
from numpy import linalg as la
from collections import defaultdict
from Util import loadDataset

from paintings_dictionary_functions import *
from plot import *
from classes.Painting import Painting

# load dataset as a dataFrame
# columns: AUTHOR YEAR URL SCHOOL
data = loadDataset('../data/catalog.xls', starting_year=1600, ending_year=1920, ordered=False)

# years dictionary: for each year a list of all Paintings in that year
years = defaultdict(list)

# paintings dictionary: for each id the corresponding Painting
paintings = dict()

# list of all feature lists -- later will be converted into matrix
features_list = []

# begin timer in order to see how long it takes to process images
start = time.time()
# Process all images -- Create Image objects and add to the dictionary
for index, row in data.iterrows():

    # create a Painting object and add it to the paintings and years dictionaries
    painting = Painting(index, int(row.YEAR), row.AUTHOR, row.URL, row.SCHOOL)

    # load features
    painting.load_features(feats=['picodes2048', 'classemes'])

    # append feature vector to features_list
    features_list.append(painting.get_features().tolist())

    # append painting to the dictionaries
    paintings[index] = painting
    years[int(row.YEAR)].append(painting)

    print(str(index+1)+'th image processed...')

    if index + 1 == 2000:
        break

matrix = np.matrix(features_list)
matrix_t = matrix.transpose()

end = time.time()
print 'Time to load images: '+str(end - start)


# SIMILARITIES
# Calculate similarities between feature vectors
start = time.time()

# Usage of cosine similarity
# similarities matrix -- efficient way to calculate using matrix form because vectors are unary
print 'Calculating similarities matrix...'
similarities = matrix * matrix_t
del matrix, matrix_t
print 'Similarities matrix calculated. Size: '+str(similarities.shape)

end = time.time()
print 'Time to calculate similarities: '+str(end - start)

# similarities to np.array instead of np.matrix
similarities = np.asarray(similarities)

# make values close to 1.0 equal to 1.0
epsilon = 0.00001
similarities[abs(similarities-1.) < epsilon] = 1.

# similarities_matrix is shared by all Painting objects
Painting.similarities_matrix = similarities

mask = np.zeros(Painting.similarities_matrix.shape, dtype=np.int8)

for painting in paintings.values():
    year = painting.get_year()
    p_id = painting.get_id()
    ids = []
    for year_past in range(min(years.keys()), year):
        ids.extend([p.get_id() for p in years.get(year_past, list())])
    for past_id in ids:
        mask[past_id, p_id] = 1

# use mask to put zero similarities from future to past paintings
Painting.similarities_matrix = np.multiply(mask, Painting.similarities_matrix)

# find mean similarity
mean = 1. * np.sum(Painting.similarities_matrix)/np.sum(mask)

# substract mean from similarity! this will introduce negative similarities
Painting.similarities_matrix = Painting.similarities_matrix - mean

# use mask again to put zero similarities from future to past paintings
Painting.similarities_matrix = np.multiply(mask, Painting.similarities_matrix)
del mask

# change direction of negative similarities
sim1 = np.clip(Painting.similarities_matrix, 0, 1)
sim2 = np.clip(Painting.similarities_matrix, -1, 0)
sim2 *= -1
sim2 = sim2.transpose()
sim = sim1 + sim2

# we want important nodes to have incoming edges and not outcoming
sim = sim.transpose()
sim = normalize(sim, norm='l1', axis=1)
sim = np.asmatrix(sim)

# vector with equal initial probability to each node in the network
init_vec = np.ones(sim.shape[0])/sim.shape[0]
init_vec = np.asmatrix(init_vec)

# print sim.shape
# print np.sum(sim, axis=1)

# PAGE RANK
mat = la.matrix_power(sim, 200)
significance = init_vec*mat

significance = np.asarray(significance)
significance = significance[0, :]
print 'Sum of Page Rank results! It should be one: '+str(np.sum(significance))

indices = significance.argsort()[-10:][::1].tolist()
# indices = np.argpartition(significance, -10)[-10:].tolist()

for i in indices:
    print paintings.get(i).get_url(), significance[i]
