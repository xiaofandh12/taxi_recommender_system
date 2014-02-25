networkx:
http://networkx.github.io/documentation/latest/install.html
1,Download the source (tar.gz or zip file) from https://pypi.python.org/pypi/networkx/ or get the latest development version from https://github.com/networkx/networkx/(download:networkx-1.8.1.tar.gz)
2,Unpack and change directory to the source directory (it should have the files README.txt and setup.py).(tar -xzvf networkx-1.8.1.tar.gz,cd networkx-1.8.1)
3,Run “python setup.py install” to build and install.
4,(optional) Run “python setup_egg.py nosetests” to execute the tests.（notice:4 is optional.if you use 3,there is no need to use 4)

rtree:
http://toblerity.org/rtree/install.html
1,download and install version 1.7.0 of the libspatialindex library from:http://libspatialindex.github.com.(download:spatialindex-src-1.7.0.tar.gz)
2,Unpack and change directory to the source directory.(tar -xzvf spatialindex-src-1.7.0.tar.gz,cd spatialindex-src-1.7.0)
3,./configure;make;make install
4,ldconfig
5,download Rtree(https://pypi.python.org/pypi/Rtree/:Rtree-0.7.0.tar.gz(md5))
6,unpack and change directory to the source directory.(tar -xzvf Rtree-0.7.0.tar.gz,cd Rtree-0.7.0)
7,python setup.py install

scipy:
http://www.scipy.org/install.html
sudo apt-get install python-scipy
