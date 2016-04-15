irdm-2016
===================


This is the group project for **Information Retrieval and Data Mining** module.
Group Project Option 8 - *Mining fine-art paintings for creativity understanding*

----------


Data
-------------

All the data files are downloaded from http://www.wga.hu/index1.html

Team - Members
--------------
Name    | email
-------- | ---
Ilias Antoniou | ilias.antoniou.15@ucl.ac.uk
James Hale    | james.hale.15@ucl.ac.uk
Cyrus Parlin     | cyrus.parlin.15@ucl.ac.uk


Code
--------

We used **python 2.7**

Need to install the following modules:
```
leargist
PIL
```
Instructions for installing leargist can be found here: https://pypi.python.org/pypi/pyleargist

Procedure
---------------------
We will briefly describe the procedure needed to be followed in order to run the code.
>**Procedure**

> - We run `save_images.py` script in order to save images on disc. This is needed in order to extract *classemes* and *picodes* features later.
> - Default setting is to save images under */images* directory. A listimages.txt file is generated as well.
> -  We need to download **vlg extractor** from [vlg](http://vlg.cs.dartmouth.edu/projects/vlg_extractor/vlg_extractor/Home.html/). We need to download parameters as well (5GB)
> - For *linux* OS we need `opencv2.3.0`. This release is quite old so we need to download it from [opencv2.3](https://github.com/Itseez/opencv/releases/tag/2.3.0). After downloading it we need to compile it. Build FFMPEG option gives an error so we remove it as we do not need video analysis. We follow similar procedure as described [here](http://indranilsinharoy.com/2012/11/01/installing-opencv-on-linux/).
> - build configuration: `cmake -D CMAKE_BUILD_TYPE=RELEASE -D WITH_FFMPEG=OFF -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_ZLIB=ON -D BUILD_PYTHON_SUPPORT=ON ~/opencv/opencv-2.3.0`
> - Now we are ready to extract *classemes* and *picodes* using **vlg**. We run the following command: `./vlg_extractor --extract_classemes=FLOAT --extract_picodes2048=FLOAT --parameters-dir=parameters/parameters_1.1 ~/PycharmProjects/irdm-2016/listimages.txt ~/PycharmProjects/irdm-2016 ~/PycharmProjects/irdm-2016/features`. It saves features under `/features/images` directory if we stick with default configuration.
> - We run `main.py` script for analysis.

Literature Review
--------------------

> **Notes:**

> - *PylearGist*:  https://pypi.python.org/pypi/pyleargist
> - *PylearGist an example*:  http://people.csail.mit.edu/torralba/code/spatialenvelope/
> - *Picodes*:  http://vlg.cs.dartmouth.edu/projects/vlg_extractor/vlg_extractor/Home.html
> - *Large-scale Classification of Fine-Art Paintings: Learning The Right Metric on The Right Feature* : http://arxiv.org/pdf/1505.00855v1.pdf
> - *Quantifying Creativity in Art Networks*: http://arxiv.org/pdf/1506.00711v1.pdf
>

Results
-------
Most similar paintings:
![Regatta at Sainte-Adresse](http://www.wga.hu/detail/m/monet/01/early16.jpg "Regatta at Sainte-Adressequot;") ![enter image description here](http://www.wga.hu/detail/m/monet/01/early18.jpg "The Regatta at Sainte-Adresse2")
It seems like the same painting with slightly different colours appear twice in the dataset. Score: **0.8866**

Most different paintings:
![The Drunken Silenus](http://www.wga.hu/detail/r/rubens/22mythol/27mythol.jpg "The Drunken Silenus")
![The Grosse Gehege near Dresden](http://www.wga.hu/detail/f/friedric/4/410fried.jpg "The Grosse Gehege near Dresden")
The paintings are quite different with similarity score: **0.188156**
Interestingly enough the most similar painting to Ruben's *Silenus* is the *The Drunken Hercules* of the same artist. The similarities between the two paintings are obvious:
![The Drunken Hercules](http://www.wga.hu/detail/r/rubens/21mythol/09mythol.jpg "The Drunken Hercules")

**PageRank** analysis on the network:
After performing PageRank analysis on the network proposed by *Elgammal* and *Saleh* we end that the top-10 bost important (novel and influential) nodes of the network are the following:
http://www.wga.hu/html/l/lane/owlshead.html 0.000473825164847
http://www.wga.hu/html/b/beraud/selfport.html 0.00048041151832
http://www.wga.hu/html/k/kroyer/zbathing.html 0.000480969828368
http://www.wga.hu/html/f/friedric/3/307fried.html 0.000489828919249
http://www.wga.hu/html/c/courbet/4/courb400.html 0.000495143706113
http://www.wga.hu/html/f/friedric/1/107fried.html 0.00049721862977
http://www.wga.hu/html/f/friedric/3/306fried.html 0.000511199334791
http://www.wga.hu/html/b/beruete/manzana2.html 0.000520213748859
http://www.wga.hu/html/f/friedric/4/409fried.html 0.000660883742561
http://www.wga.hu/html/f/friedric/4/410fried.html 0.000748484616618


