"""Defines ways to start PySeus.

Methods
-------

**load(arg)** - Startup function and console entry point.
"""

from sys import argv
import numpy
from .settings import DataType

from .core import PySeus


def load(arg=None, data_type=DataType.IMAGE):
    """Start Pyseus and load *arg* (can be a path or data array)."""

    app = PySeus()
    if len(argv) > 1 and arg is None:
        arg = argv[1]
    if len(argv) > 2:
        data_type = argv[2]
    if isinstance(arg, str):
        app.load_file(arg, data_type)
    elif isinstance(arg, (numpy.ndarray, list)):
        app.load_data(arg, data_type)

    return app.show()


if __name__ == "__main__":
    load()
