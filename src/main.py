import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from collections import defaultdict
from Util import loadDataset
from paintings_dictionary_functions import set_innovations
from classes.Painting import Painting

# load dataset as a dataFrame
# columns: AUTHOR YEAR URL SCHOOL
data = loadDataset('../data/catalog.xls', starting_year=1600, ordered=False)

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
    painting.load_features(feats=['GIST', 'picodes2048', 'classemes'])

    # append feature vector to features_list
    features_list.append(painting.get_features().tolist())

    # append painting to the dictionaries
    paintings[index] = painting
    years[int(row.YEAR)].append(painting)

    print(str(index+1)+'th image processed...')

    if index + 1 == 5000:
        break

matrix = np.matrix(features_list)
matrix_t = matrix.transpose()

end = time.time()
print 'Time to load images: '+str(end - start)

# Calculate similarities between feature vectors
start = time.time()

# Usage of cosine similarity
# TODO try different similarity metrics
# similarities matrix -- efficient way to calculate using matrix form because vectors are unary
print 'Calculating similarities matrix'
similarities = matrix * matrix_t
del matrix, matrix_t
print 'Similarities matrix calculated. Size: '+str(similarities.shape)

end = time.time()
print 'Time to calculate similarities: '+str(end - start)

# similarities to np.array instead of np.matrix
similarities = np.asarray(similarities)

# similarities_matrix is shared by all Painting objects
Painting.similarities_matrix = similarities

# Build histogram of similarities
# keep only distinct similarities in order to build the histogram
triangle = np.triu_indices(len(similarities), 1)
distinct_similarities = np.squeeze(similarities[triangle])

my_bins = np.linspace(.0, 1.0, 100)
plt.hist(distinct_similarities, bins=my_bins)
plt.show()

# least similar paintings another way
# diagonal elements of similarities are equal to 1.0
# TODO set diagonal elements of similarities equal to nan and use different way to compare - see np.nanmin
# i_min, j_min = np.unravel_index(similarities.argmin(), similarities.shape)
# print(paintings.get(i_min).get_similarity(j_min))

# find most and least similar pairs of paintings
max_pair = Painting.get_max(0.000001)
min_pair = Painting.get_min()
max_sim = paintings.get(max_pair[0]).get_similarity(max_pair[1])
min_sim = paintings.get(min_pair[0]).get_similarity(min_pair[1])

print str(max_sim)+' '+paintings.get(max_pair[0]).get_url()+' '+paintings.get(max_pair[1]).get_url()
min_0 = paintings.get(max_pair[0]).get_min_similarity()
min_1 = paintings.get(max_pair[1]).get_min_similarity()
print str(paintings.get(max_pair[0]).get_similarity(min_0))+' ' +\
      paintings.get(max_pair[0]).get_url()+' ' + paintings.get(min_0).get_url()
print str(paintings.get(max_pair[1]).get_similarity(min_1))+' ' +\
      paintings.get(max_pair[1]).get_url()+' ' + paintings.get(min_1).get_url()
print ''

print str(min_sim)+' '+paintings.get(min_pair[0]).get_url()+' '+paintings.get(min_pair[1]).get_url()
max_0 = paintings.get(min_pair[0]).get_max_similarity()
max_1 = paintings.get(min_pair[1]).get_max_similarity()
print str(paintings.get(min_pair[0]).get_similarity(max_0))+' ' +\
      paintings.get(min_pair[0]).get_url()+' ' + paintings.get(max_0).get_url()
print str(paintings.get(min_pair[1]).get_similarity(max_1))+' ' +\
      paintings.get(min_pair[1]).get_url()+' ' + paintings.get(max_1).get_url()


# Calculate innovations
set_innovations(paintings, years, 5, 10)

# Create a frame with two columns
# YEAR, INNOVATION: average innovation per year
inv_frame = pd.DataFrame(columns=['YEAR', 'INNOVATION'])
for year in years.keys():
    paintings_in_year = years.get(year, list())
    innovation_list = []
    for painting in paintings_in_year:
        innovation_list.append(painting.get_innovation())
    if innovation_list:
        inv_frame = inv_frame.append({'YEAR': year, 'INNOVATION': np.mean(innovation_list)},
                                     ignore_index=True)

inv_frame.set_index('YEAR', inplace=True)
inv_frame.sort_index(inplace=True)
inv_frame.plot()
plt.show()