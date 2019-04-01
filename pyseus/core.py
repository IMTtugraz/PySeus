from PySide2.QtWidgets import QApplication

from .ui import MainWindow

class PySeus(QApplication):

    def __init__(self):
        QApplication.__init__(self)

    @staticmethod
    def show():
        app = PySeus()
        app.window = MainWindow(app)
        app.window.show()
        return app.exec_()
