from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QImage, QPixmap

from .ui import MainWindow

class PySeus(QApplication):

    def __init__(self):
        QApplication.__init__(self)
        self.window = MainWindow(self)
        self.window.show()

    def view_data(self, image):
        self.window.view.setPixmap(QPixmap.fromImage(image))
        self.window._action_zoom_reset()