"""...
"""

import numpy

from context import pyseus


# No data
# pyseus.load()

# Numpy (pickel file)
# pyseus.load("./samples/sample.npy")

# Numpy (array)
# data = numpy.load("./samples/sample.npy")
# pyseus.load(data)

# HDF5
# pyseus.load("./samples/sample.h5")

# DICOM
# pyseus.load("./samples/sample.dcm/0000.dcm")

# NIfTI
pyseus.load("./samples/sample.nii")
