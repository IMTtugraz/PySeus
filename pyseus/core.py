"""Main components of PySeus.

Classes
-------

**PySeus** - The main application class.
"""

import os
import cv2

from PySide2.QtGui import qApp
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication, QMessageBox

from .modes import Grayscale
from .formats import Raw, NumPy, H5, DICOM, NIfTI, LoadError
from .settings import settings
from .tools import AreaTool, LineTool
from .ui import MainWindow
from .ui.meta import MetaWindow


class PySeus():  # pylint: disable=R0902
    """The main application class acts as front controller."""

    def __init__(self, gui=True):
        # set gui = false for testing

        self.qt_app = None
        """The QApplication instance for interaction with the Qt framework."""

        if isinstance(qApp, type(None)):
            self.qt_app = QApplication([])
        else:
            self.qt_app = qApp

        self.dataset = None
        """The current dataset object. See `Formats <development/formats>`_."""

        self.formats = [H5, DICOM, NIfTI, NumPy, Raw]
        """List of all avaiable data formats. See `Formats <development/formats>`_."""

        self.tools = [AreaTool, LineTool]
        """List of all avaiable evaluation tools. See `Tools <development/tools>`_."""

        self.tool = None
        """The current tool object. See `Tools <development/tools>`_."""

        self.window = MainWindow(self)
        """The main window object. See `Interface <development/interface>`_."""

        self.meta_window = None
        """Holds the meta window object."""

        self.display = Grayscale()
        """The display helper object. See `Display <development/display>`_."""

        self.slice = -1
        """Index of the current slice."""

        self.timer = QTimer()
        """Timer for timelapse view."""

        self.gui = gui
        """Flag wheter to use the GUI or not."""

        # Stylesheet
        style_path = "./ui/" + settings["ui"]["style"] + ".qss"
        style_path = os.path.join(os.path.dirname(__file__), style_path)
        with open(style_path, "r") as stylesheet:
            self.qt_app.setStyleSheet(stylesheet.read())

        self.qt_app.font().setPixelSize(int(settings["ui"]["font_size"]))

        if self.gui:
            self.window.show()

    def show(self):
        """Show the main window, even if initialized without the GUI."""
        if not self.gui:
            self.window.show()
            self.gui = True

        self.qt_app.exec_()

    def load_file(self, path):
        """Try to load the file at *path*. See also *setup_dataset*."""

        new_dataset = None
        for format_ in self.formats:
            if format_.can_handle(path):
                new_dataset = format_()
                break

        if new_dataset is not None:
            self.setup_dataset(path, new_dataset)

        else:
            QMessageBox.warning(self.window, "Pyseus", "Unknown file format.")

    def load_data(self, data):
        """Try to load *data*. See also *setup_dataset*."""

        new_dataset = Raw()
        self.setup_dataset(data, new_dataset)

    def setup_dataset(self, arg, dataset=None):
        """Setup a new dataset: Load scan list, generate thumbnails and load
        default scan."""
        if dataset is None:
            dataset = self.dataset

        try:
            if not dataset.load(arg):  # canceled by user
                return

            self.clear()
            self.dataset = dataset

            if self.dataset.scan_count() > 1:
                message = "{} scans detected. Do you want to load all?" \
                        .format(self.dataset.scan_count())
                # load_all = QMessageBox.question(None, "Pyseus", message)
                load_all = QMessageBox.StandardButton.Yes
                # @TODO reset after profiling

                self.window.thumbs.clear()
                if load_all is QMessageBox.StandardButton.Yes:
                    for scan_id in range(0, self.dataset.scan_count()):
                        thumb = self.display.generate_thumb(
                            self.dataset.get_scan_thumbnail(scan_id))
                        pixmap = self.display.get_pixmap(thumb)
                        self.window.thumbs.add_thumb(pixmap)
                else:
                    single_scan = self.dataset.scans[self.dataset.scan]
                    self.dataset.scans = [single_scan]
                    self.dataset.scan = 0

            self.load_scan()

        except LoadError as error:
            QMessageBox.warning(self.window, "Pyseus", str(error))

        except OSError as error:
            QMessageBox.warning(self.window, "Pyseus", str(error))

        else:
            self.window.info.update_path(self.dataset.path)

    def set_mode(self, mode):
        """Set display mode to amplitude (0) or phase (1)."""
        self.display.set_mode(mode)
        self.refresh()

    def refresh(self):
        """Refresh the displayed image."""
        if self.slice == -1:
            return

        data = self.dataset.get_pixeldata(self.slice)

        # @TODO move to FormatBase (get_pixeldata_adjusted)
        spacing = self.dataset.get_spacing()
        if spacing[0] != spacing[1]:
            if spacing[0] > spacing[1]:
                size = (int(data.shape[0]*spacing[0]/spacing[1]),
                        int(data.shape[1]))
            else:
                size = (int(data.shape[0]),
                        int(data.shape[1]*spacing[1]/spacing[0]))

            data = cv2.resize(data, size)

        pixmap = self.display.get_pixmap(data)

        if self.tool is not None:
            pixmap = self.tool.draw_overlay(pixmap)

        self.window.view.set(pixmap)  # @TODO Refactor ?!?

    def recalculate(self):
        """Refresh the active evaluation tool."""
        if self.tool is not None:
            slice_ = self.dataset.get_pixeldata(self.slice)
            self.tool.recalculate(
                self.display.prepare_without_window(slice_))

    def select_scan(self, sid, relative=False):
        """Select and load a scan from the current dataset.
        See also *load_scan*."""
        if self.dataset is None:
            return

        new_scan = self.dataset.scan + sid if relative is True else sid
        if 0 <= new_scan < self.dataset.scan_count():
            self.clear_tool()
            self.load_scan(new_scan)

    def load_scan(self, sid=None):
        """Load a scan from the current dataset."""
        old_sid = self.dataset.scan

        if sid is None:
            sid = self.dataset.scan
        self.dataset.load_scan(sid)

        if self.slice >= self.dataset.slice_count() or self.slice == -1:
            self._set_slice(self.dataset.slice_count() // 2)

        if self.dataset.scan_count() > 1:
            old_thumb = self.window.thumbs.thumbs[old_sid]
            new_thumb = self.window.thumbs.thumbs[sid]
            old_thumb.setStyleSheet("border: 1px solid transparent")
            new_thumb.setStyleSheet("border: 1px solid #aaa")

        default_metadata = self.dataset.get_metadata("DEFAULT")
        self.window.meta.update_meta(default_metadata,
                                     len(default_metadata) > 0)
        self.window.info.update_scan(self.dataset.scans[sid])

        self.display.setup_data(self.dataset.get_pixeldata())
        self.refresh()
        self.window.view.zoom_fit()

    def select_slice(self, sid, relative=False):
        """Select and display a slice from the current scan."""
        if self.dataset is None:
            return

        new_slice = self.slice + sid if relative is True else sid
        if 0 <= new_slice < self.dataset.slice_count():
            self._set_slice(new_slice)
            self.refresh()
            self.recalculate()

    def _set_slice(self, sid):
        """Set the current slice index."""
        self.window.info.update_slice(sid, self.dataset.slice_count())
        self.slice = sid

    def show_metadata_window(self):
        """Show the metadata window.
        See `Interface <development/interface>`_."""
        self.meta_window = MetaWindow(self, self.dataset.get_metadata())
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
            self._set_slice(self.dataset.slice_count() // 2)

        self.refresh()
        self.window.view.zoom_fit()
        self.clear_tool()

    def flip(self, direction):
        """Flip the pixeldata of the current scan."""
        self.dataset.flip(direction)

        self.refresh()
        self.clear_tool()

    def toggle_timelapse(self):
        """Toggle automatic loading of next scans."""
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.timeout.connect(self._timelapse_next)
            self.timer.start(int(settings["timelapse"]["interval"]))

    def _timelapse_next(self):
        self.select_scan(1, True)
