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
from paintings_dictionary_functions import get_distinct_similarities, get_max_min_pairs
from classes.Painting import Painting

# load dataset as a dataFrame
# columns: AUTHOR YEAR URL SCHOOL
data = loadDataset('../data/catalog.xls', starting_year=1600, ordered=False)

# years dictionary: for each year a list of all Paintings in that year
years = defaultdict(list)

# paintings dictionary: for each id the corresponding Painting
paintings = dict()

# begin timer in order to see how long it takes to process images
start = time.time()
for index, row in data.iterrows():
    i = index + 1   # begin counting from 1

    # get image and calculate GIST vector
    image_url = row.URL.replace('/html', '/detail')
    image_url = image_url.replace('.html', '.jpg')
    response = requests.get(image_url)
    painting_file = BytesIO(response.content)
    img = Image.open(painting_file)
    desc = leargist.color_gist(img)

    # create a Painting object and add it to the paintings and years dictionaries
    painting = Painting(i, row.YEAR, row.AUTHOR, image_url, row.SCHOOL, desc)
    paintings[i] = painting
    years[int(row.YEAR)].append(painting)

    print(str(i)+'th image processed...')

    if i == 10:
        break

end = time.time()
print 'Time to load images: '+str(end - start)

# Calculate similarities between feature vectors
# Usage of cosine similarity
# TODO try different similarity metrics
for key1 in paintings.keys():
    painting1 = paintings.get(key1)
    for key2 in paintings.keys():
        painting2 = paintings.get(key2)
        if painting1 is not painting2:
            # calculate similarity
            similarity = 1.0 - dis.cosine(painting1.get_features(), painting2.get_features())
            # set similarity for painting1
            painting1.set_similarity(key2, similarity)

# save an image in the default folder
# paintings.get(9).save_painting()

distinct_similarities = get_distinct_similarities(paintings)

# Plot histogram of distinct similarities
my_bins = np.linspace(.0, 1.0, 100)
plt.hist(distinct_similarities, bins=my_bins)
plt.show()

# find most and least similar pairs of paintings
max_sim, max_pair,  min_sim, min_pair = get_max_min_pairs(paintings)
print str(max_sim)+' '+paintings.get(max_pair[0]).get_url()+' '+paintings.get(max_pair[1]).get_url()
print str(min_sim)+' '+paintings.get(min_pair[0]).get_url()+' '+paintings.get(min_pair[1]).get_url()

# Calculate innovation
# Formula: 1.0 - (1/n) * /sum_1^n d_i
years_back = 5
top_paintings = 10
for key in paintings:
    # for each painting
    painting = paintings.get(key)
    similarity_list = []

    # for the last years_back years find the top_paintings more similar paintings
    for year in range(painting.get_year()-years_back, painting.get_year()):

        # get a list of all paintings during 'year' year
        paintings_in_year = years.get(year, list())
        for painting_year in paintings_in_year:
            # for each painting during year calculate similarity
            similarity_list.append(painting.get_similarity(painting_year.get_id()))

    # if list is empty meaning no painting during the past year_back years is found
    if not similarity_list:
        innovation = 0.0
    else:
        # sort and take the average of top_paintings most similar paintings
        similarity_list.sort(reverse=True)
        similarity_list = similarity_list[:top_paintings]
        innovation = np.mean(similarity_list)

    # set innovation of the painting
    painting.set_innovation(1.0 - innovation)

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
