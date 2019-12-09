import os

from PySide2.QtWidgets import QApplication, QMessageBox

from pyseus import settings
from pyseus import DisplayHelper
from pyseus.ui import MainWindow
from pyseus.formats import Raw, NumPy, H5, DICOM, NIfTI, LoadError
from pyseus.tools import AreaTool, LineTool
from pyseus.ui.meta import MetaWindow


class PySeus(QApplication):
    """The main application class acts as controller."""

    def __init__(self):
        """Setup the GUI and default values."""

        QApplication.__init__(self)

        self.dataset = None
        """Dataset"""

        self.formats = [NumPy, H5, DICOM, NIfTI, Raw]
        """List of all avaiable data formats."""

        self.tools = [AreaTool, LineTool]
        """List of all avaiable evaluation tools."""

        self.tool = None
        """Tool"""

        self.window = MainWindow(self)
        """Window"""

        self.display = DisplayHelper()
        """DisplayHelper"""

        self.slice = -1
        """Current Slice"""

        # Stylesheet
        style_path = "./ui/" + settings["ui"]["style"] + ".qss"
        style_path = os.path.join(os.path.dirname(__file__), style_path)
        with open(style_path, "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

        self.font().setPixelSize(int(settings["ui"]["font_size"]))

        self.window.show()

    def load_file(self, path):
        """Try to load file at `path`."""

        self.new_dataset = None
        for f in self.formats:
            if f.can_handle(path):
                self.new_dataset = f()
                break

        if self.new_dataset is not None:
            self._setup_dataset(path)

        else:
            QMessageBox.warning(self.window, "Pyseus", "Unknown file format.")

    def load_data(self, data):
        """Try to load `data`."""

        self.new_dataset = Raw()
        self._setup_dataset(data)

    def _setup_dataset(self, arg):
        try:
            if not self.new_dataset.load(arg):  # canceled by user
                return

            self.clear()
            self.dataset = self.new_dataset
            del self.new_dataset

            if len(self.dataset.scans) > 1:
                self.window.thumbs.clear()
                for s in self.dataset.scans:
                    thumb = self.display.generate_thumb(
                        self.dataset.get_thumbnail(s))
                    pixmap = self.display.get_pixmap(thumb)
                    self.window.thumbs.add_thumb(pixmap)

            self._load_scan()

        except OSError as e:
            QMessageBox.warning(self.window, "Pyseus", str(e))

        except LoadError as e:
            QMessageBox.warning(self.window, "Pyseus", str(e))

        self.window.info.update_path(self.dataset.path)

    def set_mode(self, mode):
        """..."""
        self.display.mode = mode
        self.display.reset_window()
        self.refresh()

    def refresh(self):
        """Refresh the displayed image."""
        if self.slice == -1:
            return

        pixmap = self.display.get_pixmap(
                        self.dataset.get_pixeldata(self.slice))

        if self.tool is not None:
            pixmap = self.tool.draw_overlay(pixmap)

        self.window.view.set(pixmap)  # @TODO Refactor ?!?

    def recalculate(self):
        """Recalculate the current function."""
        if self.tool is not None:
            self.tool.recalculate(
                self.display.prepare_without_window(self.slices[self.slice]))

    def select_scan(self, sid, relative=False):
        if self.dataset is None:
            return

        new_scan = self.dataset.scan + sid if relative is True else sid
        if 0 <= new_scan < len(self.dataset.scans):
            self.clear_tool()
            self._load_scan(new_scan)

    def _load_scan(self, sid=None):
        old_sid = self.dataset.scan

        if sid is None:
            sid = self.dataset.scan
        self.dataset.load_scan(sid)

        pixeldata = self.dataset.pixeldata
        # make sure the new scan has enough slices
        if self.slice >= len(pixeldata) or self.slice == -1:
            self._set_slice(len(pixeldata) // 2)

        if len(self.dataset.scans) > 1:
            old_thumb = self.window.thumbs.thumbs[old_sid]
            new_thumb = self.window.thumbs.thumbs[sid]
            old_thumb.setStyleSheet("border: 1px solid transparent")
            new_thumb.setStyleSheet("border: 1px solid #aaa")

        self.window.meta.update_meta(self.dataset.get_metadata(),
                                     len(self.dataset.metadata) > 0)
        self.window.info.update_scan(self.dataset.scans[sid])

        self.display.setup_window(pixeldata[self.slice])
        self.refresh()
        self.window.view.zoom_fit()

    def select_slice(self, sid, relative=False):
        if self.dataset is None:
            return

        new_slice = self.slice + sid if relative is True else sid
        if 0 <= new_slice < len(self.dataset.pixeldata):
            self._set_slice(new_slice)
            self.refresh()
            self.recalculate()

    def _set_slice(self, sid):
        self.window.info.update_slice(sid, len(self.dataset.pixeldata))
        self.slice = sid

    def show_metadata_window(self):
        self.meta_window = MetaWindow(self, self.dataset.metadata)
        self.meta_window.show()

    def clear(self):
        self.dataset = None
        self.slice = -1
        self.window.view.set(None)
        self.window.thumbs.clear()
        self.clear_tool()

    def clear_tool(self):
        if self.tool is not None:
            self.tool.clear()

    def rotate(self, axis):
        self.dataset.rotate(axis)
        if not axis == 2:
            self._set_slice(len(self.dataset.pixeldata) // 2)

        self.refresh()
        self.window.view.zoom_fit()
        self.clear_tool()
