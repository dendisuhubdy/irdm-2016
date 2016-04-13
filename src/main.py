import time
import gc

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pandas.tools.plotting import autocorrelation_plot

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

# HISTOGRAM
# plot_histogram(similarities)


# MOST AND LEAST SIMILAR PAINTINGS

# find most and least similar pairs of paintings
# max_pair = Painting.get_max()
# min_pair = Painting.get_min()
# max_sim = paintings.get(max_pair[0]).get_similarity(max_pair[1])
# min_sim = paintings.get(min_pair[0]).get_similarity(min_pair[1])
#
# print str(max_sim)+' '+paintings.get(max_pair[0]).get_url()+' '+paintings.get(max_pair[1]).get_url()
# min_0 = paintings.get(max_pair[0]).get_min_similarity()
# min_1 = paintings.get(max_pair[1]).get_min_similarity()
# print str(paintings.get(max_pair[0]).get_similarity(min_0))+' ' +\
#       paintings.get(max_pair[0]).get_url()+' ' + paintings.get(min_0).get_url()
# print str(paintings.get(max_pair[1]).get_similarity(min_1))+' ' +\
#       paintings.get(max_pair[1]).get_url()+' ' + paintings.get(min_1).get_url()
# print ''
#
# print str(min_sim)+' '+paintings.get(min_pair[0]).get_url()+' '+paintings.get(min_pair[1]).get_url()
# max_0 = paintings.get(min_pair[0]).get_max_similarity()
# max_1 = paintings.get(min_pair[1]).get_max_similarity()
# print str(paintings.get(min_pair[0]).get_similarity(max_0))+' ' +\
#       paintings.get(min_pair[0]).get_url()+' ' + paintings.get(max_0).get_url()
# print str(paintings.get(min_pair[1]).get_similarity(max_1))+' ' +\
#       paintings.get(min_pair[1]).get_url()+' ' + paintings.get(max_1).get_url()

years_back = 10

mask = np.zeros(Painting.similarities_matrix.shape, dtype=np.int8)

for painting in paintings.values():
    year = painting.get_year()
    p_id = painting.get_id()
    ids = []
    for year_past in range(year-years_back, year):
        ids.extend([p.get_id() for p in years.get(year_past, list())])
    for past_id in ids:
        mask[past_id, p_id] = 1

similarities = np.multiply(mask, Painting.similarities_matrix)
del mask
similarities = keep_col_k(similarities, 27)
gc.collect()

# INNOVATIONS
# Calculate innovations
print 'Calculating creativities...'
start = time.time()

set_innovations(paintings, years, similarities, alpha=0.7)

end = time.time()
print 'Creativities calculated: '+str(end-start)+'secs'


mask = np.zeros(Painting.similarities_matrix.shape, dtype=np.int8)

for painting in paintings.values():
    year = painting.get_year()
    p_id = painting.get_id()
    ids = []
    for year_past in range(min(years.keys()), year-years_back):
        ids.extend([p.get_id() for p in years.get(year_past, list())])
    for past_id in ids:
        mask[past_id, p_id] = 1

similarities = np.multiply(mask, Painting.similarities_matrix)
del mask
similarities = keep_col_k(similarities, 27)
gc.collect()

# RETRO
# Calculate retro scores
print 'Calculating retro scores...'
start = time.time()

set_retro(paintings, years, similarities, alpha=0.7)

end = time.time()
print 'Retro Scores calculated: '+str(end-start)+'secs'

max_year = max(years.keys()) - years_back

plot_points_timeline(paintings, min(years.keys()), max_year, ['RETRO'])

_ = plot_timeline(years, min(years.keys()), max_year, ['INNOVATION'])

innos = []
for p in paintings.values():
    innos.append(p.get_innovation())

my_bins = np.linspace(.0, max(innos), 100)
plt.hist(innos, bins=my_bins)
plt.show()

# Print most creative and most retro work!
max_cr_id = None
max_cr_val = 0.

max_re_id = None
max_re_val = 0.

sum_creat = 0.
sum_retro = 0.
for p in paintings.values():
    sum_creat += p.get_innovation()
    sum_retro += p.get_retro()
    if p.get_innovation() > max_cr_val: max_cr_id, max_cr_val = p.get_id(), p.get_innovation()
    if p.get_retro() > max_re_val: max_re_id, max_re_val = p.get_id(), p.get_retro()

print 'Sum of innovations: '+str(sum_creat)
print 'Sum of retro scores: '+str(sum_retro)

print 'Most innovative painting:'
print paintings.get(max_cr_id).get_url(), paintings.get(max_cr_id)

print 'Most retro painting:'
print paintings.get(max_re_id).get_url(), paintings.get(max_re_id)

print ''
print 'Most innovative painting per century'
for i in range(16, 19):
    year_beg = i*100
    year_end = year_beg + 100
    max_id = None
    max_val = 0.
    for year in range(year_beg, year_end):
        p_in_year = years.get(year, list())
        for p in p_in_year:
            if p.get_innovation() > max_val: max_val, max_id = p.get_innovation(), p.get_id()

    print paintings.get(max_id).get_url(), paintings.get(max_id)

# year_dict: keep paintings that have creativity more than the year's average
ps = []
year_dict = defaultdict(list)
for year in range(min(years.keys()), max(years.keys())+1):
    ps = years.get(year, list())

    # list of all innovations in this year
    innos = [p.get_innovation() for p in ps]
    if not innos:
        mean = 1.
    else:
        mean = np.mean(innos)

    # pings: list of paintings in year with innovation more than mean
    pings = [p for p in ps if p.get_innovation() >= mean]
    year_dict[year] = pings

frame = plot_timeline(year_dict, 1600, 1900)
frame['IN_RE'] = frame.INNOVATION*frame.RETRO
frame = frame[['IN_RE']]
frame.plot()
plt.show()
autocorrelation_plot(frame.IN_RE)
plt.show()
