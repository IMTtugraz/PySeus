from .core import PySeus
from .ui import MainWindow

def show(arg):
    app = PySeus()
    app.window = MainWindow(app)
    app.window.show()

    # if arg is numpy.array:
    #     PySeus.load_npa(arg)
    #     PySeus.show()
    # else:
    #     pass

    return app.exec_()
