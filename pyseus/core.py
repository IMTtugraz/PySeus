import os
import numpy
import cv2

from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtGui import QFont, QImage, QPixmap, QPainter, QColor, QPen

from pyseus import settings
from pyseus import DisplayHelper
from pyseus.ui import MainWindow
from pyseus.formats import Raw, H5, DICOM, NIfTI, LoadError
from pyseus.tools import AreaTool, LineTool
from pyseus.ui.meta import MetaWindow

class PySeus(QApplication):
    """The main application class acts as controller."""

    def __init__(self):
        """Setup the GUI and default values."""

        QApplication.__init__(self)

        self.formats = [H5, DICOM, NIfTI, Raw]
        """Holds all avaiable data formats."""

        self.tools = [AreaTool, LineTool]
        """Holds all avaiable evaluation tools."""

        self.dataset = None
        """dataset"""

        self.tool = None
        """Tool"""

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

        self.font().setPixelSize(12)

        self.window.show()

    def load_file(self, path):
        """Try to load file at `path`."""

        if not os.path.exists(path):
            QMessageBox.error(self.window, "Pyseus", 
                "Path not found.")

        dataset = None
        for f in self.formats:
            if f.check_file(path):
                dataset = f(self)
                break
        
        self.deload()

        if not dataset is None:
            try:
                self.path, self.scans, self.current_scan = dataset.load_file(path)
                if self.path == "": return

                if len(self.scans) > 1:
                    self.window.thumbs.clear()
                    for s in self.scans:
                        thumb = self._generate_thumb(
                            dataset.load_scan_thumb(s))
                        self.window.thumbs.add_thumb(thumb)

                self._load_scan(self.current_scan,  dataset)
                self._set_current_scan(self.current_scan)
        
                self.window.info.update_path(self.path)

                self.dataset = dataset

            except OSError as e:
                QMessageBox.warning(self.window, "Pyseus", 
                    str(e))
            except LoadError as e:
                QMessageBox.warning(self.window, "Pyseus", 
                    e)

        else:
            QMessageBox.warning(self.window, "Pyseus", 
                "Unknown file format.")

    def _generate_thumb(self, data):
        thumb_size = int(settings["ui"]["thumb_size"])
        thumb_data = cv2.resize(data, (thumb_size, thumb_size))

        self.display.setup_window(thumb_data)
        return self.display.prepare(thumb_data)

    def load_data(self, data):
        """Try to load `data`."""
        self.deload()

        dataset = Raw()
        
        try:
            self.path, self.scans, self.current_scan = dataset.load_data(data)
            if self.path == "": return

            if len(self.scans) > 1:
                self.window.thumbs.clear()
                for s in self.scans:
                    thumb = self._generate_thumb(
                        dataset.load_scan_thumb(s))
                    self.window.thumbs.add_thumb(thumb)

            self._load_scan(self.current_scan,  dataset)
            self._set_current_scan(self.current_scan)

            self.dataset = dataset
        
            self.window.info.update_path(self.path)

        except OSError as e:
            QMessageBox.warning(self.window, "Pyseus", 
                str(e))
        except LoadError as e:
            QMessageBox.warning(self.window, "Pyseus", 
                e)

    def deload(self):
        self.dataset = None
        self.scans = []
        self.current_scan = -1
        self.slices = []
        self.current_slice = -1
        self.window.view.set(None)
        self.window.thumbs.clear()
        self.clear_roi()

    def refresh(self):
        """Refresh the displayed image."""
        if self.current_slice == -1: return

        tmp = self.display.prepare(self.slices[self.current_slice].copy())

        image = QImage(tmp.data, tmp.shape[1],
                       tmp.shape[0], tmp.strides[0],
                       QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image)

        if not self.tool is None:
            pixmap = self.tool.draw_overlay(pixmap)

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
        """Recalculate the current function."""
        if not self.tool is None:
            self.tool.recalculate(self.slices[self.current_slice])

    def _load_scan(self, key, dataset=None):
        dataset = self.dataset if dataset is None else dataset
        
        try:
            self.slices = dataset.load_scan(self.scans[key])

            # make sure the new scan has enough slices
            if self.current_slice >= len(self.slices) or self.current_slice == -1:
                self._set_current_slice(len(self.slices) // 2)

            self.metadata = dataset.load_metadata(self.scans[key])
            key_meta = dataset.get_key_meta(None, self.metadata)
            self.window.meta.update_meta(key_meta, len(self.metadata) > 0)

            self.display.setup_window(self.slices[self.current_slice])
            self.refresh()
            self.window.view.zoom_fit()
        except LoadError as e:
            QMessageBox.warning(self.window, "Pyseus", 
                e)

    def select_slice(self, sid, relative=False):
        if self.path == "": return

        new_slice = self.current_slice + sid if relative == True else sid
        if 0 <= new_slice < len(self.slices):
            self._set_current_slice(new_slice)
            self.refresh()
            self.recalculate()
    
    def _set_current_slice(self, sid):
        self.window.info.update_slice(sid, len(self.slices))
        self.current_slice = sid

    def select_scan(self, sid, relative=False):
        if self.path == "": return

        new_scan = self.current_scan + sid if relative == True else sid
        if 0 <= new_scan < len(self.scans):
            self.clear_roi()
            self._set_current_scan(new_scan)
            self._load_scan(new_scan)
    
    def _set_current_scan(self, sid):
        if len(self.scans) > 1:
            self.window.thumbs.thumbs[self.current_scan].setStyleSheet("border: 1px solid transparent")
            self.window.thumbs.thumbs[sid].setStyleSheet("border: 1px solid #aaa")
        
        self.window.info.update_scan(self.scans[sid])
        self.current_scan = sid

    def rotate(self, axis, steps=1, refresh=True):
        if axis == -1:  # reset
            self._load_scan(self.current_scan)

        else:
            if axis == 0 and len(self.slices) > 2:  # x-axis
                self.slices = numpy.asarray(numpy.swapaxes(self.slices, 0, 2))
                self._set_current_slice(len(self.slices) // 2)
                
            elif axis == 1 and len(self.slices) > 2:  # y-axis
                self.slices = numpy.asarray(numpy.rot90(self.slices))
                self._set_current_slice(len(self.slices) // 2)

            elif axis == 2:  # z-axis
                self.slices = numpy.asarray([numpy.rot90(slice) for slice in self.slices])

        if steps > 1: self.rotate(axis, steps-1, refresh)

        if refresh:
            self.refresh()
            self.window.view.zoom_fit()
            self.tool.clear()
    
    def clear_roi(self):
        if not self.tool is None: self.tool.clear()

    def show_metadata_window(self):
        data = self.dataset.load_metadata(self.scans[self.current_scan])
        self.meta_window = MetaWindow(self, data)
        self.meta_window.show()
