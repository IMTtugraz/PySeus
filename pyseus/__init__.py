"""PySeus is a minimal viewer for medical imaging data


"""

from sys import stdin, argv

from .core import PySeus
from .ui import MainWindow

def load_image(data):
    """View QImage for testing purposes"""
    app = PySeus()
    app.view_data(data)
    return app.exec_()

def load_file(file):
    """Load File for testing purposes"""
    app = PySeus()
    app.load_file(file)
    return app.exec_()

def show():
    """Start Pyseus without data"""
    app = PySeus()
    return app.exec_()

def _console_entry():
    """Start Pyseus from Console

    Loads path from arguments or data from stdin, if available.
    """
    # @TODO check argv
    # @TODO check stdin
    show()
