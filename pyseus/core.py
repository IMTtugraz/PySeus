from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QImage, QPixmap
import numpy

from .ui import MainWindow, get_stylesheet
from .formats import H5
from .modes import Amplitude

class PySeus(QApplication):

    def __init__(self):
        QApplication.__init__(self)
        
        # Stylesheet
        self.setStyleSheet(get_stylesheet())

        self.window = MainWindow(self)
        self.window.show()

    def view_data(self, image):
        self.window.view.setPixmap(QPixmap.fromImage(image))
        self.window._action_zoom_reset()

    def load_file(self, file):
        print("core.load_file")
        # @TODO check for Format
        self.file = H5()
        self.file.load_file(file)
        self.frame_data = self.file.load_frame(0)

        self.mode = Amplitude(self.frame_data)
        self.refresh()
        self.window._action_zoom_reset()
        

    def refresh(self):
        tmp = self.mode.prepare(self.frame_data.copy())

        image = QImage(tmp.data, tmp.shape[1],
                            tmp.shape[0], tmp.strides[0],
                            QImage.Format_Grayscale8)
        self.window.view.setPixmap(QPixmap.fromImage(image))
