import leargist
import scipy.spatial.distance as dis
import time
import requests
from src.Util import loadDataset
from PIL import Image
from io import BytesIO


data = loadDataset('../data/catalog.xls', starting_year=1600, ordered=False)

im = Image.open('../images/index.jpeg')
descriptors = leargist.color_gist(im)
im1 = Image.open('../images/gate7.jpeg')
descr1 = leargist.color_gist(im1)
im2 = Image.open('../images/vg.jpg')
descr2 = leargist.color_gist(im2)
# print 1.0 - dis.cosine(descriptors, descr1)
# print 1.0 - dis.cosine(descriptors, descr2)


start = time.time()
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

end = time.time()
print end - start