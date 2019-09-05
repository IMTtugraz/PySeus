import os

from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtGui import QImage, QPixmap, QPainter, QColor, QPen

from pyseus import settings
from pyseus import DisplayHelper
from pyseus.ui import MainWindow
from pyseus.formats import Raw, H5, DICOM, LoadError
from pyseus.functions import RoIFct, StatsFct

class PySeus(QApplication):
    """The main application class acts as controller."""

    def __init__(self):
        """Setup the GUI and default values."""

        QApplication.__init__(self)

        self.formats = [H5, DICOM, Raw]
        """Holds all avaiable data formats."""

        self.functions = [RoIFct, StatsFct]
        """Holds all avaiable RoI evaluation functions."""

        self.dataset = None
        """dataset"""

        self.function = self.functions[0]()
        """Function"""

        # @ TODO roi util functions (reset, set, get --> property ?!?)
        self.roi = [0, 0, 0, 0]
        """Region of Interest"""

        self.window = MainWindow(self)
        """Window"""

        self.display = DisplayHelper()
        """DisplayHelper"""

        self.path = ""
        """Path"""

        self.scans = []
        """Scans"""

        self.current_scan = -1
        """Current Scan"""

        self.slices = []
        """Slices"""

        self.current_slice = -1
        """Current Slice"""

        # Stylesheet
        style_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "./ui/" + settings["app"]["style"] + ".qss"))
        with open(style_path, "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

        self.setup_functions_menu()
        self.window.thumbs.thumb_clicked = self._load_scan

        self.window.show()

    def setup_functions_menu(self):
        """Add functions to main windows `Evals` menu."""
        for key, function in enumerate(self.functions):
            self.window.add_function_to_menu(key, function)

    def load_file(self, path):
        """Try to load file at `path`."""
        self.deload()

        dataset = None
        for f in self.formats:
            if f.check_file(path):
                dataset = f()
                break
        
        if not dataset is None:
            try:
                self.path, self.scans, self.current_scan = dataset.load_file(path)

                if len(self.scans) > 1:
                    for s in self.scans:
                        thumb = self._generate_thumb(
                            dataset.load_scan_thumb(s))
                        self.window.thumbs.add_thumb(thumb)

                self._load_scan(self.current_scan,  dataset)

            except OSError as e:
                QMessageBox.warning(self.window, "Pyseus", 
                    str(e))
            except LoadError as e:
                QMessageBox.warning(self.window, "Pyseus", 
                    e)

            self.dataset = dataset

        else:
            QMessageBox.warning(self.window, "Pyseus", 
                "Unknown file format.")

    def _generate_thumb(self, data):
        thumb_size = int(settings["ui"]["thumb_size"])
        x_factor = data.shape[0] // thumb_size
        y_factor = data.shape[1] // thumb_size
        factor = max(x_factor, y_factor)
        thumb_data = data[::factor, ::factor]

        self.display.setup_window(thumb_data)
        return self.display.prepare(thumb_data)

    def load_data(self, data):
        """Try to load `data`."""
        # @TODO
        pass

    def deload(self):
        self.dataset = None
        self.scans = []
        self.current_scan = -1
        self.slices = []
        self.current_slice = -1
        self.window.view.set(None)
        self.window.thumbs.clear()

    def refresh(self):
        """Refresh the displayed image."""
        if self.current_slice == -1: return

        tmp = self.display.prepare(self.slices[self.current_slice].copy())

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

        self.window.view.set(pixmap)

    def set_mode(self, mode):
        """Set the mode with the slug `mode` as current."""
        self.display.mode = mode
        self.display.reset_window()
        self.refresh()

    def show_status(self, message):
        """Display `message` in status bar."""
        self.window.statusBar().showMessage(message)

    def recalculate(self):
        """Recalculate the current RoI-function."""
        if self.roi != [0, 0, 0, 0]:
            result = self.function.recalculate(self.slices[self.current_slice],
                                               self.roi)
            self.window.console.print(result)

    def set_function(self, key):
        """Set the RoI-function with the slug `key` as current."""
        self.function = self.functions[key]()
        self.recalculate()

    def _load_scan(self, key, dataset=None):
        dataset = self.dataset if dataset is None else dataset

        self.slices = dataset.load_scan(self.scans[key])
        self.current_slice = len(self.slices) // 2

        self.display.setup_window(self.slices[self.current_slice])
        self.refresh()
        self.window.view.zoom_fit()

    def select_slice(self, sid, relative=False):
        if self.path == "": return

        new_slice = self.current_slice + sid if relative == True else sid
        if 0 <= new_slice < len(self.slices):
            self.current_slice = new_slice
        self.refresh()

    def select_scan(self, sid, relative=False):
        if self.path == "": return

        new_scan = self.current_scan + sid if relative == True else sid
        if 0 <= new_scan < len(self.scans):
            self._load_scan(self.scans[new_scan])
            self.current_scan = new_scan
