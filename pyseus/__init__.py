from sys import stdin, argv

from .core import PySeus
from .ui import MainWindow


def load_image(data):
    app = PySeus()
    app.window = MainWindow(app)
    app.window.show()
    app.window.view_data(data)
    return app.exec_()

def show():
    app = PySeus()
    app.window = MainWindow(app)
    app.window.show()
    return app.exec_()
