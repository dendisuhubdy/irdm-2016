import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.spatial.distance as dis
import leargist
import time
import requests
from PIL import Image
from io import BytesIO
from collections import defaultdict
from src.Util import loadDataset
from paintings_dictionary_functions import get_max_min_pairs, set_innovations
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

    # get image and calculate GIST vector
    image_url = row.URL.replace('/html', '/detail')
    image_url = image_url.replace('.html', '.jpg')
    response = requests.get(image_url)
    painting_file = BytesIO(response.content)
    img = Image.open(painting_file)
    desc = leargist.color_gist(img)

    # unary feature vector - used later for cosine similarity in matrices form
    norm = np.linalg.norm(desc)
    unary_desc = desc/norm
    features_list.append(unary_desc.tolist())

    # create a Painting object and add it to the paintings and years dictionaries
    painting = Painting(index, int(row.YEAR), row.AUTHOR, row.URL, row.SCHOOL, desc)
    paintings[index] = painting
    years[int(row.YEAR)].append(painting)

    print(str(index+1)+'th image processed...')

    if index + 1 == 2000:
        break

matrix = np.matrix(features_list)
matrix_t = matrix.transpose()

end = time.time()
print 'Time to load images: '+str(end - start)

# Calculate similarities between feature vectors
# Usage of cosine similarity
# TODO try different similarity metrics
# similarities matrix -- efficient way to calculate using matrix form because vectors are unary
similarities = matrix * matrix_t
del matrix, matrix_t

# similarities to np.array instead of np.matrix
similarities = np.asarray(similarities)

# Populate Painting objects with similarities
for i in range(0, len(similarities)):
    sim_vector = similarities[i, :].tolist()
    paintings.get(i).set_similarities(sim_vector)

# save an image in the default folder
# paintings.get(9).save_painting()

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
max_sim, max_pair,  min_sim, min_pair = get_max_min_pairs(paintings)

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
