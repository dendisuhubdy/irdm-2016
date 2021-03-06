import time

from Util import loadDataset
from classes.Painting import Painting

__author__ = 'helias'


# load dataset as a dataFrame
# columns: AUTHOR YEAR URL SCHOOL
data = loadDataset('../data/catalog.xls', starting_year=1600, ordered=False)

# begin timer in order to see how long it takes to save images
start = time.time()

list_file = open('../listimages.txt', 'w')

# Process all images -- Create Image objects and add to the dictionary
for index, row in data.iterrows():

    painting = Painting(index, int(row.YEAR), row.AUTHOR, row.URL, row.SCHOOL)
    painting.save_painting(file=list_file)

    print(str(index+1)+'th image saved...')

list_file.close()

end = time.time()
print 'Time to save images: '+str(end - start)