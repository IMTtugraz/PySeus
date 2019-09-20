import h5py
import numpy

from context import pyseus

# file = h5py.File("test.h5", "r")
# pyseus.load(file['images'])

# file = h5py.File("test.h5", "r")
# array = numpy.asarray(file['images'])
# numpy.save("test", array)

pyseus.load("test.npy")
