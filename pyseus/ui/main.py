"""Main window for PySeus.

Classes
-------

**MainWindow** - Class representing the main window for PySeus.
"""

import sys
import webbrowser
from functools import partial
import os
import numpy

from PySide2 import QtWidgets
from PySide2.QtCore import QLine
from PySide2.QtWidgets import QButtonGroup, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QMainWindow, QAction, QLabel, QFileDialog, \
    QFrame, QPushButton, QRadioButton, QVBoxLayout, QHBoxLayout, QWidget
from PySide2.QtGui import QIcon

from .view import ViewWidget
from .sidebar import ConsoleWidget, InfoWidget, MetaWidget
from .thumbs import ThumbsWidget
from ..settings import DataType, ProcessType

import scipy.io
import matplotlib.pyplot as plt


class MainWindow(QMainWindow):  # pylint: disable=R0902
    """Class representing the main window for PySeus."""

    def __init__(self, app):
        QMainWindow.__init__(self)
        self.setWindowTitle("PySEUS")

        self.app = app
        """Reference to the main application object."""

        self.thumbs = ThumbsWidget(app)
        """Reference to the thumbs widget."""

        self.view = ViewWidget(app)
        """Reference to the view widget."""

        self.info = InfoWidget(app)
        """Reference to the info sidebar widget."""

        self.meta = MetaWidget(app)
        """Reference to the meta sidebar widget."""

        self.console = ConsoleWidget(app)
        """Reference to the console sidebar widget."""

        # Default path for file open dialoge
        self._open_path = ""

        # Horizontal layout (thumbs, view, sidebar)
        wrapper = QFrame(self)
        wrapper.setLayout(QHBoxLayout())
        wrapper.layout().setContentsMargins(0, 0, 0, 0)
        wrapper.layout().addWidget(self.thumbs)
        wrapper.layout().addWidget(self.view)

        # Sidebar / Vertical layout (info, meta, console)
        sidebar = QFrame(self)
        sidebar.setLayout(QVBoxLayout())
        sidebar.layout().setContentsMargins(0, 0, 5, 0)

        sidebar.layout().addWidget(SidebarHeading("File Info", True))
        sidebar.layout().addWidget(self.info)

        sidebar.layout().addWidget(SidebarHeading("Metadata"))
        sidebar.layout().addWidget(self.meta)

        sidebar.layout().addWidget(SidebarHeading("Console"))
        sidebar.layout().addWidget(self.console)

        wrapper.layout().addWidget(sidebar)

        self.setup_menu()

        self.statusBar().setSizeGripEnabled(False)

        self.setCentralWidget(wrapper)

        icon = QIcon(os.path.abspath(os.path.join(
            os.path.dirname(__file__), "./icon.png")))
        self.setWindowIcon(icon)

        # Window dimensions
        geometry = self.app.qt_app.desktop().availableGeometry(self)
        self.resize(geometry.width() * 0.6, geometry.height() * 0.6)

    def add_menu_item(self, menu, title, callback, shortcut=""):
        """Create a menu item."""
        action = QAction(title, self)
        if shortcut != "":
            action.setShortcut(shortcut)
        action.triggered.connect(callback)
        menu.addAction(action)
        return action

    def setup_menu(self):
        """Setup the menu bar. Items in the *Evaluate* menu are created
        in the *setup_menu* function of tool classes."""
        ami = self.add_menu_item
        menu_bar = self.menuBar()

        # partial fixes a given number of arguments to a function and generates a new function without
        # calling it
        self.file_menu = menu_bar.addMenu("&File")
        ami(self.file_menu, "&Load image", partial(
            self._action_open, DataType.IMAGE), "Ctrl+O")
        ami(self.file_menu, "&Load k-space",
            partial(self._action_open, DataType.KSPACE), "Ctrl+K")
        ami(self.file_menu, "&Save dataset",
            partial(self._action_save), "Ctrl+S")
        ami(self.file_menu, "&Reload", self._action_reload, "Ctrl+L")
        self.file_menu.addSeparator()
        ami(self.file_menu, "&Quit", self._action_quit, "Ctrl+Q")

        self.view_menu = menu_bar.addMenu("&View")
        for mode in self.app.modes:
            mode.setup_menu(self.app, self.view_menu, self.add_menu_item)
        self.view_menu.addSeparator()

        ami(self.view_menu, "Zoom &in", self._action_zoom_in, "+")
        ami(self.view_menu, "Zoom &out", self._action_zoom_out, "-")
        ami(self.view_menu, "Zoom to &fit", self._action_zoom_fit, "#")
        ami(self.view_menu, "Reset &Zoom", self._action_zoom_reset, "0")
        self.view_menu.addSeparator()

        ami(self.view_menu, "&Lower Window", self._action_win_lower, "q")
        ami(self.view_menu, "&Raise Window", self._action_win_raise, "w")
        ami(self.view_menu, "&Shrink Window", self._action_win_shrink, "a")
        ami(self.view_menu, "&Enlarge Window", self._action_win_enlarge, "s")
        ami(self.view_menu, "Reset &Window", self._action_win_reset, "d")

        self.explore_menu = menu_bar.addMenu("E&xplore")
        ami(self.explore_menu, "Nex&t Slice",
            partial(self._action_slice, 1), "PgUp")
        ami(self.explore_menu, "P&revious Slice",
            partial(self._action_slice, -1), "PgDown")
        self.explore_menu.addSeparator()

        ami(self.explore_menu, "Rotate z",
            partial(self._action_rotate, 2), "Ctrl+E")
        ami(self.explore_menu, "Rotate x",
            partial(self._action_rotate, 1), "Ctrl+R")
        ami(self.explore_menu, "Rotate y",
            partial(self._action_rotate, 0), "Ctrl+T")
        self.explore_menu.addSeparator()
        ami(self.explore_menu, "Flip x (L-R)",
            partial(self._action_flip, 1), "Ctrl+D")
        ami(self.explore_menu, "Flip y (U-D)",
            partial(self._action_flip, 0), "Ctrl+F")
        ami(self.explore_menu, "Flip z (F-B)",
            partial(self._action_flip, 2), "Ctrl+G")
        self.explore_menu.addSeparator()
        ami(self.explore_menu, "Reset Scan",
            partial(self._action_rotate, -1), "Ctrl+Z")
        self.explore_menu.addSeparator()

        ami(self.explore_menu, "Next &Scan",
            partial(self._action_scan, 1), "Alt+PgUp")
        ami(self.explore_menu, "Previous Sc&an",
            partial(self._action_scan, -1), "Alt+PgDown")
        self.explore_menu.addSeparator()
        ami(self.explore_menu, "Cine Play", self._action_cine, "Ctrl+#")

        self.tools_menu = menu_bar.addMenu("&Evaluate")
        for tool in self.app.tools:
            tool.setup_menu(self.app, self.tools_menu, self.add_menu_item)
        self.tools_menu.addSeparator()
        ami(self.tools_menu, "&Clear RoI", self._action_tool_clear, "Esc")

        self.process_menu = menu_bar.addMenu("&Process")
        ami(self.process_menu, "Denoising",
            partial(self._open_process_dialog, ProcessType.DENOISING), "---")
        ami(self.process_menu, "Reconstruction", partial(
            self._open_process_dialog, ProcessType.RECONSTRUCTION), "---")

        # About action is its own top level menu
        ami(menu_bar, "&About", self._action_about)

    def show_status(self, message):
        """Display *message* in the status bar."""
        self.statusBar().showMessage(message)

    def resizeEvent(self, event):  # pylint: disable=C0103
        """Keep the viewport centered and adjust zoom on window resize."""
        x_factor = event.size().width() / event.oldSize().width()
        # y_factor = event.size().height() / event.oldSize().height()
        # @TODO x_factor if xf < yf or xf * width * zoom_factor < viewport_x
        self.view.zoom(x_factor, True)

    def _action_quit(self):
        self.app.qt_app.quit()
        sys.exit(0)

    # without event it would work that all windows close
    def closeEvent(self, event):
        self._action_quit()

    def _action_open(self, data_type=DataType.IMAGE):
        path, _ = QFileDialog.getOpenFileName(None, "Open file",
                                              self._open_path, "*.*")

        if not path == "":
            self._open_path = os.path.dirname(path)
            self.app.load_file(path, data_type)

    def _action_save(self):

        path, _ = QFileDialog.getSaveFileName(None, "Save dataset",
                                              self._open_path, "*.npy")

        with open(path, 'wb') as file:
            numpy.save(file, self.app.dataset.get_pixeldata())

    def _action_reload(self):
        if self.app.dataset is not None:
            data_type = self.app.dataset.get_data_type()
            self.app.load_file(self.app.dataset.path, data_type)

    def _action_zoom_in(self):
        self.view.zoom(1.25)

    def _action_zoom_out(self):
        self.view.zoom(0.8)

    def _action_zoom_fit(self):
        self.view.zoom_fit()

    def _action_zoom_reset(self):
        self.view.zoom(1, False)

    def _action_about(self):  # pylint: disable=R0201
        webbrowser.open_new("https://github.com/IMTtugraz/PySeus")

    def _action_win_lower(self):
        self.app.mode.move_window(-20)
        self.app.refresh()

    def _action_win_raise(self):
        self.app.mode.move_window(20)
        self.app.refresh()

    def _action_win_shrink(self):
        self.app.mode.scale_window(-25)
        self.app.refresh()

    def _action_win_enlarge(self):
        self.app.mode.scale_window(25)
        self.app.refresh()

    def _action_win_reset(self):
        self.app.mode.reset_window()
        self.app.refresh()

    def _action_slice(self, step):
        self.app.select_slice(step, True)

    def _action_scan(self, step):
        self.app.select_scan(step, True)

    def _action_tool_clear(self):
        self.app.clear_tool()

    def _action_rotate(self, axis):
        self.app.rotate(axis)

    def _action_flip(self, direction):
        self.app.flip(direction)

    def _action_cine(self):
        self.app.toggle_cine()

    def _open_process_dialog(self, proc_type):
        self.app.show_process_window(proc_type)


class SidebarHeading(QLabel):  # pylint: disable=R0903
    """Widget for sidebar separators and headings."""

    def __init__(self, text="", first=False):
        QLabel.__init__(self)
        self.setText(text)
        role = "widget_heading__first" if first else "widget_heading"
        self.setProperty("role", role)
        self.setMinimumHeight(24)
        self.setMaximumHeight(24)
