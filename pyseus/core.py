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

        self.dataset = None
        """Dataset"""

        self.formats = [H5, DICOM, NIfTI, Raw]
        """Holds all avaiable data formats."""

        self.tools = [AreaTool, LineTool]
        """Holds all avaiable evaluation tools."""

        self.tool = None
        """Tool"""

        self.window = MainWindow(self)
        """Window"""

        self.display = DisplayHelper(self)
        """DisplayHelper"""

        self.slice = -1
        """Current Slice"""

        # Stylesheet
        style_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
            "./ui/" + settings["ui"]["style"] + ".qss"))
        with open(style_path, "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

        self.font().setPixelSize(12)

        self.window.show()

    def load_file(self, path):
        """Try to load file at `path`."""

        dataset = None
        for f in self.formats:
            if f.can_handle(path):
                dataset = f()
                break

        if not dataset is None:
            try:
                if not dataset.load_file(path):  # canceled by user
                    return

                # @TODO refactor ?!? --> DRY with load_data
                if len(dataset.scans) > 1:
                    self.window.thumbs.clear()
                    for s in dataset.scans:
                        thumb = self.display.generate_thumb(
                            dataset.get_thumbnail(s))
                        self.window.thumbs.add_thumb(thumb)

                self.clear()
                self.dataset = dataset

                self._load_scan(self.current_scan, dataset)
                self._set_current_scan(self.current_scan)
        
                self.window.info.update_path(self.path)

            except OSError as e:
                QMessageBox.warning(self.window, "Pyseus", str(e))

            except LoadError as e:
                QMessageBox.warning(self.window, "Pyseus", str(e))

        else:
            QMessageBox.warning(self.window, "Pyseus", "Unknown file format.")


    def load_data(self, data):
        """Try to load `data`."""

        dataset = Raw(self)
        
        try:
            if not dataset.load_data(data):  # canceled by user
                return

            # @TODO refactor ?!?
            if len(self.scans) > 1:
                self.window.thumbs.clear()
                for s in self.scans:
                    thumb = self.display.generate_thumb(
                        dataset.get_thumbnail(s))
                    self.window.thumbs.add_thumb(thumb)
            
            self.clear()
            self.dataset = dataset

            self._load_scan(self.current_scan, dataset)
            self._set_current_scan(self.current_scan)
        
            self.window.info.update_path(self.path)

        except OSError as e:
            QMessageBox.warning(self.window, "Pyseus", 
                str(e))
        except LoadError as e:
            QMessageBox.warning(self.window, "Pyseus", 
                e)

    def clear(self):
        self.dataset = None
        self.slice = -1
        self.window.view.set(None)
        self.window.thumbs.clear()
        self.clear_tool()

    def refresh(self):
        """Refresh the displayed image."""
        if self.slice == -1: return

        pixmap = self.display.get_pixmap(dataset.pixeldata(self.slice))

        if not self.tool is None:
            pixmap = self.tool.draw_overlay(pixmap)

        self.window.view.set(pixmap) # @TODO Refactor ?!?

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
            self.tool.recalculate(self.slices[self.slice])

    def _load_scan(self, key):
        pixeldata = self.dataset.pixeldata
        # make sure the new scan has enough slices
        if self.slice >= len(pixeldata) or self.slice == -1:
            self._set_current_slice(len(pixeldata) // 2)

        self.window.meta.update_meta(dataset.metadata(), 
            len(self.dataset.metadata) > 0)

        self.display.setup_window(pixeldata[self.slice])
        self.refresh()
        self.window.view.zoom_fit()

    def select_slice(self, sid, relative=False):
        if self.dataset is None: return

        new_slice = self.slice + sid if relative == True else sid
        if 0 <= new_slice < len(self.slices):
            self._set_current_slice(new_slice)
            self.refresh()
            self.recalculate()
    
    def _set_current_slice(self, sid):
        self.window.info.update_slice(sid, len(self.slices))
        self.slice = sid

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

    def rotate(self, axis):
        self.dataset.rotate(axis)
        self.refresh()
        self.window.view.zoom_fit()
        self.tool.clear()

    def show_metadata_window(self):
        self.meta_window = MetaWindow(self, self.dataset.metadata)
        self.meta_window.show()

    def clear_tool(self):
        if not self.tool is None:
            self.too.clear()
