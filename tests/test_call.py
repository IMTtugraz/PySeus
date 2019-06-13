import numpy

import context
from context import pyseus

if __name__ == "__main__":
    npa = numpy.loadtxt("npa.txt", numpy.uint8)
    pyseus.show(npa.data)
