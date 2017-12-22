deep-pink
=========

Deep Pink is a chess AI that learns to play chess using deep learning. [Here](http://erikbern.com/2014/11/29/deep-learning-for-chess/) is a  blog post providing some details about how it works.

Our goal for this project is to parallelize this AI for optimal run-time and better reliability.

Dependencies
============

* [Theano](https://github.com/Theano/Theano): `git clone https://github.com/Theano/Theano; cd Theano; python setup.py install`
* [Sunfish](https://github.com/thomasahle/sunfish): `git clone https://github.com/thomasahle/sunfish`. You need to add it to PYTHONPATH to be able to play
* [python-chess](https://pypi.python.org/pypi/python-chess) `pip install python-chess`
* [scikit-learn](http://scikit-learn.org/stable/install.html) (only needed for training)
* [h5py](http://www.h5py.org/): can be installed using `apt-get install python-hdf5` or `pip install hdf5` (only needed for training)
