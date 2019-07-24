from os import path

import numpy

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QImage, QPixmap

from .ui import MainWindow, get_stylesheet
from .formats import Raw, H5
from .modes import Amplitude, Phase

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

    def __init__(self):
        QApplication.__init__(self)
        
        # Stylesheet
        self.setStyleSheet(get_stylesheet())

        self.file = Raw() # Remove, only set after "try_load"
        self.mode = PySeus.modes["Amplitude"]()

        self.window = MainWindow(self)
        self.window.show()

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
        self.window.view.setPixmap(QPixmap.fromImage(image))

    def set_mode(self, mode):
        self.mode = PySeus.modes[mode]()
        self.mode.setup(self.frame_data)
        self.refresh()
