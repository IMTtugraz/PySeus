"""

Starting file for pyseus

"""

from pyseus import load
from pyseus.settings import DataType


load('./tests/samples/sample.h5', DataType.IMAGE)

