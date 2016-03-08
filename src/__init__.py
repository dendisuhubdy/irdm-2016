import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial.distance as dis
import leargist
import time
import requests
from PIL import Image
from io import BytesIO
from collections import defaultdict
from src.Util import loadDataset
from src.Painting import Painting


data = loadDataset('../data/catalog.xls', starting_year=1600, ordered=False)
print data.head

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
    years[row.YEAR].append(painting)

    print(str(i)+'th image processed...')

    if i == 100:
        break

i = 0
descriptors = []
for url in data.URL.values:
    image_url = url.replace('/html', '/detail')
    image_url = image_url.replace('.html', '.jpg')
    response = requests.get(image_url)
    painting_file = BytesIO(response.content)
    img = Image.open(painting_file)
    desc = leargist.color_gist(img)
    descriptors.append(desc)

    # process name for saving image
    # url = url[23:]
    # url = url[:-5]
    # url = url.replace('/', '_')
    # img.save('../images/'+url+'.png')

    i += 1
    print(str(i)+'th image processed...')
    if i == 100:
        break

end = time.time()
print 'Time to load images: '+str(end - start)

similarities = []
for desc1 in descriptors:
    for desc2 in descriptors:
        similarity = 1.0 - dis.cosine(desc1, desc2)
        similarities.append(similarity)

print min(similarities)
sim_array = np.array(similarities).reshape(len(descriptors), len(descriptors))
i_min, j_min = np.unravel_index(sim_array.argmin(), sim_array.shape)

row = sim_array.copy()[i_min,:]
j_max = row.argmax()
row[j_max] = 0.0
j_max = row.argmax()

print data.URL.values[i_min], data.URL.values[j_min], sim_array[i_min, j_min]
print data.URL.values[i_min], data.URL.values[j_max], sim_array[i_min, j_max]

triangle = np.triu_indices(len(sim_array), 1)
distinct_similarities = sim_array[triangle]
print triangle
print distinct_similarities
print sim_array
print len(distinct_similarities)

my_bins = np.linspace(.0, 1.0, 100)
plt.hist(distinct_similarities, bins=my_bins)
plt.show()