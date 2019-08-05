from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QImage, QPixmap, QPainter, QColor, QPen

from .ui import MainWindow, get_stylesheet
from .formats import Raw, H5
from .modes import Amplitude, Phase
from .functions import RoIFct, StatsFct


class PySeus(QApplication):
    """The main application class acts as controller."""

    modes = {}
    """Holds all avaiable display modes."""

    formats = {}
    """Holds all avaiable data formats."""

    functions = {}
    """Holds all avaiable RoI evaluation functions."""

    def __init__(self):
        """Setup the GUI and default values."""
        QApplication.__init__(self)

        # Stylesheet
        self.setStyleSheet(get_stylesheet())

        PySeus.modes = {
            "Amplitude": Amplitude,
            "Phase": Phase,
        }

        PySeus.formats = {
            "Raw": Raw,
            "H5": H5,
            # "DICOM": DICOM,
        }

        PySeus.functions = {
            "Region of Interest": RoIFct,
            "Statistics": StatsFct
        }

        self.file = Raw()  # Remove, only set after "try_load"
        self.mode = PySeus.modes["Amplitude"]()

        self.window = MainWindow(self)
        self.window.show()

        self.roi = [0, 0, 0, 0]
        self.function = RoIFct()

    # @TODO remove after testing
    def load_image(self, image):
        """Display image (only for testing purposes)."""
        self.window.view.view.setPixmap(QPixmap.fromImage(image))
        self.window._action_zoom_reset()

    def load_file(self, path):
        """Try to load file at `path`."""
        # @TODO check for Format
        self.file = H5()
        self.file.load_file(path)
        # @TODO implement frame selection
        self.frame_data = self.file.load_frame(0)

        self.mode.setup(self.frame_data)
        self.refresh()
        self.window._action_zoom_reset()

    def load_data(self, data):
        """Try to load the frame contained in `data`."""
        # @TODO check for Format
        self.file.load_data(data)
        self.frame_data = self.file.load_frame(0)

        self.mode.setup(self.frame_data)
        self.refresh()
        self.window._action_zoom_reset()

    def refresh(self):
        """Refresh the displayed image."""
        tmp = self.mode.prepare(self.frame_data.copy())

        image = QImage(tmp.data, tmp.shape[1],
                       tmp.shape[0], tmp.strides[0],
                       QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image)
        if self.roi != [0, 0, 0, 0]:
            painter = QPainter(pixmap)
            pen = QPen(QColor("red"))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawRect(self.roi[0], self.roi[1], self.roi[2]
                             - self.roi[0], self.roi[3] - self.roi[1])
            painter.end()

        self.window.view.view.setPixmap(pixmap)

    def set_mode(self, mode):
        """Set the mode with the slug `mode` as current."""
        self.mode = PySeus.modes[mode]()
        self.mode.setup(self.frame_data)
        self.refresh()

    def show_status(self, message):
        """Display `message` in status bar."""
        self.window.status.showMessage(message)

    def recalculate(self):
        """Recalculate the current RoI-function."""
        result = ""
        if self.roi != [0, 0, 0, 0]:
            result = self.function.recalculate(self.frame_data, self.roi)
        self.show_status(result)

    def set_function(self, fct):
        """Set the RoI-function with the slug `fct` as current."""
        self.function = fct()
        self.recalculate()
