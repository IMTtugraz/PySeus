from sys import argv
import numpy

from pyseus.core import PySeus


def load(arg=None):
    """Start Pyseus and load `arg`. `arg` can be a path or data array."""
    app = PySeus()

    if len(argv) > 1 and arg is None:
        arg = argv[1]

    if isinstance(arg, str):
        app.load_file(arg)

    elif isinstance(arg, numpy.ndarray):
        app.load_data(arg)

    return app.exec_()

if __name__ == "__main__":
    load()
