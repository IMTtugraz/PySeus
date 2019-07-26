import h5py

from context import pyseus

file = h5py.File("test.h5", "r")

pyseus.load(file['images'][0])
