import h5py
import numpy
from sys import stdout

file = h5py.File("test.h5", "r")

import ptvsd

# VSC remote debugging
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
ptvsd.wait_for_attach()
breakpoint()

stdout.write(numpy.array2string(file['images'][0]))
