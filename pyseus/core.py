import os

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QImage, QPixmap, QPainter, QColor, QPen

from pyseus.settings import settings
from pyseus.ui import MainWindow
from pyseus.formats import Raw, H5, DICOM
from pyseus.modes import Amplitude, Phase
from pyseus.functions import RoIFct, StatsFct


class PySeus(QApplication):
    """The main application class acts as controller."""

    def __init__(self):
        """Setup the GUI and default values."""

        QApplication.__init__(self)

        self.modes = [Amplitude, Phase]
        """Holds all avaiable display modes."""

        self.formats = [Raw, H5, DICOM]
        """Holds all avaiable data formats."""

        self.functions = [RoIFct, StatsFct]
        """Holds all avaiable RoI evaluation functions."""

        self.format = None
        """Format"""

        self.mode = self.modes[0]()
        """Mode"""

        self.function = self.functions[0]()
        """Function"""

        # @ TODO roi util functions (reset, set, get --> property ?!?)
        self.roi = [0, 0, 0, 0]
        """Region of Interest"""

        self.window = MainWindow(self)
        """Window"""

        self.path = ""
        """Path"""

        self.scans = []
        """Scans"""

        self.slices = []
        """Slices"""

        self.current_slice = []
        """Current Slice"""

        # Stylesheet
        style_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "./ui/" + settings["app"]["style"] + ".qss"))
        with open(style_path, "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

        self.setup_functions_menu()
        self.window.show()

    def setup_functions_menu(self):
        """Add functions to main windows `Evals` menu."""
        for key, function in enumerate(self.functions):
            self.window.add_function_to_menu(key, function)

    # @TODO remove after testing // dont change at all !!!
    def load_image(self, image):
        """Display image (only for testing purposes)."""
        self.window.view.view.setPixmap(QPixmap.fromImage(image))
        self.window._action_zoom_fit()

    def load_file(self, path):
        """Try to load file at `path`."""
        # @TODO check for Format
        self.format = H5()
        self.format.load_file(path)
        # @TODO implement frame selection
        self.current_slice = self.format.load_frame(0)

        self.mode.setup(self.current_slice)
        self.refresh()
        self.window._action_zoom_fit()
        self.path = path

    def load_data(self, data):
        """Try to load the frame contained in `data`."""
        # @TODO check for Format
        self.format.load_data(data)
        self.current_slice = self.format.load_frame(0)

        self.mode.setup(self.current_slice)
        self.refresh()
        self.window._action_zoom_fit()

    def refresh(self):
        """Refresh the displayed image."""
        tmp = self.mode.prepare(self.current_slice.copy())

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
        self.mode = self.modes[mode]()
        self.mode.setup(self.current_slice)
        self.refresh()

    def show_status(self, message):
        """Display `message` in status bar."""
        self.window.statusBar().showMessage(message)

    def recalculate(self):
        """Recalculate the current RoI-function."""
        if self.roi != [0, 0, 0, 0]:
            result = self.function.recalculate(self.current_slice, self.roi)
            self.window.console.print(result)

    def set_function(self, key):
        """Set the RoI-function with the slug `key` as current."""
        self.function = self.functions[key]()
        self.recalculate()
