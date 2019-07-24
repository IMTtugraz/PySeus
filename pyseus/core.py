from os import path

import numpy

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QImage, QPixmap, QPainter, QColor, QPen

from .ui import MainWindow, get_stylesheet
from .formats import Raw, H5
from .modes import Amplitude, Phase
from .functions import TestFct

class PySeus(QApplication):

    # @TODO Allow registering modes dynamically
    modes = {
        "Amplitude": Amplitude,
        "Phase": Phase,
    }

    # @TODO Allow registering formats dynamically
    formats = {
        "Raw": Raw,
        "H5": H5,
        # "DICOM": DICOM,
    }

    # @TODO Allow registering functions dynamically
    functions = {
        "Test": TestFct
    }

    def __init__(self):
        QApplication.__init__(self)
        
        # Stylesheet
        self.setStyleSheet(get_stylesheet())

        self.file = Raw() # Remove, only set after "try_load"
        self.mode = PySeus.modes["Amplitude"]()

        self.window = MainWindow(self)
        self.window.show()

        self.roi = [0,0,0,0]
        self.function = TestFct()

    def load_image(self, image):
        # @TODO remove after testing
        self.window.view.setPixmap(QPixmap.fromImage(image))
        self.window._action_zoom_reset()

    def load_file(self, file):
        # @TODO check for Format
        self.file = H5()
        self.file.load_file(file)
        self.frame_data = self.file.load_frame(0)

        self.mode.setup(self.frame_data)
        self.refresh()
        self.window._action_zoom_reset()
    
    def load_data(self, data):
        # @TODO check for Format
        self.file.load_data(data)
        self.frame_data = self.file.load_frame(0)

        self.mode.setup(self.frame_data)
        self.refresh()
        self.window._action_zoom_reset()
        
    def refresh(self):
        tmp = self.mode.prepare(self.frame_data.copy())

        image = QImage(tmp.data, tmp.shape[1],
                       tmp.shape[0], tmp.strides[0],
                       QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image)
        if self.roi != [0,0,0,0]:
            painter = QPainter(pixmap)
            pen = QPen(QColor("red"))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawRect(self.roi[0], self.roi[1], 
                self.roi[2] - self.roi[0], self.roi[3] - self.roi[1])
            painter.end()

        self.window.view.setPixmap(pixmap)

    def set_mode(self, mode):
        self.mode = PySeus.modes[mode]()
        self.mode.setup(self.frame_data)
        self.refresh()

    def show_status(self, message):
        self.window.status.showMessage(message)

    def recalculate(self):
        result = ""
        if self.roi != [0,0,0,0]:
            result = self.function.recalculate(self.frame_data, self.roi)
        self.show_status(result)
