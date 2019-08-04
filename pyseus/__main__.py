from os import path
from sys import stdin, argv

from PySide2.QtGui import QImage

from .core import PySeus


def load(arg=None):
    """Start Pyseus and load `arg`.
    `arg` can be a file path or data array."""
    app = PySeus()

    if isinstance(arg, str):  # and path.isfile(arg):
        app.load_file(arg)

    # @TODO remove after testing
    elif isinstance(arg, QImage):
        app.load_image(arg)

    elif arg is not None:
        app.load_data(arg)

    return app.exec_()

if __name__ == "__main__":
    load()
