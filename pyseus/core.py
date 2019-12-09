import os

from PySide2.QtWidgets import QApplication, QMessageBox

from pyseus import settings
from pyseus import DisplayHelper
from pyseus.ui import MainWindow
from pyseus.formats import Raw, NumPy, H5, DICOM, NIfTI, LoadError
from pyseus.tools import AreaTool, LineTool
from pyseus.ui.meta import MetaWindow


class PySeus(QApplication):
    """The main application class acts as front controller."""

    def __init__(self):
        """Setup the application and default values."""

        QApplication.__init__(self)

        self.dataset = None
        """The current dataset object. See `Formats <development/formats>`_."""

        self.formats = [H5, DICOM, NIfTI, NumPy, Raw]
        """List of all avaiable data formats."""

        self.tools = [AreaTool, LineTool]
        """List of all avaiable evaluation tools."""

        self.tool = None
        """The current tool object. See `Tools <development/tools>`_."""

        self.window = MainWindow(self)
        """The main window object. See `Interface <development/interface>`_."""

        self.display = DisplayHelper()
        """The display helper object. See `Display <development/display>`_."""

        self.slice = -1
        """Index of the current slice."""

        # Stylesheet
        style_path = "./ui/" + settings["ui"]["style"] + ".qss"
        style_path = os.path.join(os.path.dirname(__file__), style_path)
        with open(style_path, "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

        self.font().setPixelSize(int(settings["ui"]["font_size"]))

        self.window.show()

    def load_file(self, path):
        """Try to load the file at `path`. See also `setup_dataset`."""

        self.new_dataset = None
        for f in self.formats:
            if f.can_handle(path):
                self.new_dataset = f()
                break

        if self.new_dataset is not None:
            self.setup_dataset(path)

        else:
            QMessageBox.warning(self.window, "Pyseus", "Unknown file format.")

    def load_data(self, data):
        """Try to load `data`. See also `setup_dataset`."""

        self.new_dataset = Raw()
        self.setup_dataset(data)

    def setup_dataset(self, arg):
        """Setup a new dataset: Load scan list, generate thumbnails and load default scan."""
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
                        self.dataset.get_scan_thumbnail(s))
                    pixmap = self.display.get_pixmap(thumb)
                    self.window.thumbs.add_thumb(pixmap)

            self.load_scan()

        except OSError as e:
            QMessageBox.warning(self.window, "Pyseus", str(e))

        except LoadError as e:
            QMessageBox.warning(self.window, "Pyseus", str(e))

        self.window.info.update_path(self.dataset.path)

    def set_mode(self, mode):
        """Set display mode to amplitude (0) or phase (1)."""
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
        """Refresh the active evaluation tool."""
        if self.tool is not None:
            self.tool.recalculate(
                self.display.prepare_without_window(self.slices[self.slice]))

    def select_scan(self, sid, relative=False):
        """Select and load a scan from the current dataset. See also `load_scan`."""
        if self.dataset is None:
            return

        new_scan = self.dataset.scan + sid if relative is True else sid
        if 0 <= new_scan < len(self.dataset.scans):
            self.clear_tool()
            self.load_scan(new_scan)

    def load_scan(self, sid=None):
        """Load a scan from the current dataset."""
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

        self.window.meta.update_meta(self.dataset.get_metadata("DEFAULT"),
                                     len(self.dataset.metadata) > 0)
        self.window.info.update_scan(self.dataset.scans[sid])

        self.display.setup_window(pixeldata[self.slice])
        self.refresh()
        self.window.view.zoom_fit()

    def select_slice(self, sid, relative=False):
        """Select and display a slice from the current scan."""
        if self.dataset is None:
            return

        new_slice = self.slice + sid if relative is True else sid
        if 0 <= new_slice < len(self.dataset.pixeldata):
            self._set_slice(new_slice)
            self.refresh()
            self.recalculate()

    def _set_slice(self, sid):
        """Set the current slice index."""
        self.window.info.update_slice(sid, len(self.dataset.pixeldata))
        self.slice = sid

    def show_metadata_window(self):
        """Show the metadata window (pyseus.ui.meta.MetaWindow)."""
        self.meta_window = MetaWindow(self, self.dataset.metadata)
        self.meta_window.show()

    def clear(self):
        """Reset the application."""
        self.dataset = None
        self.slice = -1
        self.window.view.set(None)
        self.window.thumbs.clear()
        self.clear_tool()

    def clear_tool(self):
        """Reset the active evaluation tool."""
        if self.tool is not None:
            self.tool.clear()

    def rotate(self, axis):
        """Rotate the pixeldata of the current scan in 3D."""
        self.dataset.rotate(axis)
        if not axis == 2:
            self._set_slice(len(self.dataset.pixeldata) // 2)

        self.refresh()
        self.window.view.zoom_fit()
        self.clear_tool()
