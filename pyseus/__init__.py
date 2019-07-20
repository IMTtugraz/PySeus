from sys import stdin, argv

from .core import PySeus
from .ui import MainWindow


def load_image(data):
    app = PySeus()
    app.view_data(data)
    return app.exec_()

def show():
    app = PySeus()
    return app.exec_()
