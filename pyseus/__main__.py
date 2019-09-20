from sys import argv
import numpy

from pyseus.core import PySeus


def load(arg=None):
    """Start Pyseus and load `arg`. `arg` can be a path or data array."""
    app = PySeus()

    if len(argv) > 1 and arg is None:
        arg = argv[1]

    if isinstance(arg, str):  # and path.isfile(arg):
        app.load_file(arg)

    else:
        app.load_data(arg)

    return app.exec_()

if __name__ == "__main__":
    load()
