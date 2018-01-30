deep-pink
=========

Deep Pink is a chess AI that learns to play chess using deep learning. [Here](http://erikbern.com/2014/11/29/deep-learning-for-chess/) is a  blog post providing some details about how it works.

This project has been ported to CuPy to help alleviate CPU work and (possibly) accelerate its runtime and enhance capabilities.

Dependencies
============

* [Theano](https://github.com/Theano/Theano): `git clone https://github.com/Theano/Theano; cd Theano; python setup.py install`
* [Sunfish](https://github.com/thomasahle/sunfish): `git clone https://github.com/thomasahle/sunfish`. You need to add it to PYTHONPATH to be able to play
* [python-chess](https://pypi.python.org/pypi/python-chess/0.8.3) `pip install python-chess==0.8.3`(not tested)--The reason this version is needed is because newer versions of python-chess use a different method structure, which is incompatible with this project.
* [scikit-learn](http://scikit-learn.org/stable/install.html) (only needed for training)
* [cupy](https://github.com/cupy/cupy) `pip install cupy`. Needed to run the training module. CuDNN is highly recommended.
* [chainer](https://github.com/chainer/chainer) `pip install chainer` This is needed in order to translate cupy functions back to the CPU.
* [h5py](http://www.h5py.org/): can be installed using `apt-get install python-hdf5` or `pip install hdf5` (only needed for training)
