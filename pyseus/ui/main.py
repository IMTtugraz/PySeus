import sys
import webbrowser
from functools import partial
import os

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QAction, \
    QLabel, QFileDialog, QFrame, QVBoxLayout, QHBoxLayout, QSpinBox

from .view import ViewWidget
from .console import ConsoleWidget
from .info import InfoWidget
from .thumbs import ThumbsWidget
from .overlay import OverlayWidget


class MainWindow(QMainWindow):
    """The main window for PySeus."""

    def __init__(self, app):
        QMainWindow.__init__(self)
        self.setWindowTitle("PySEUS")

        self.app = app
        """Holds reference to front controller."""

        self.thumbs = ThumbsWidget(app)
        """@TODO"""

        self.view = ViewWidget(app)
        """@TODO"""

        self.info = InfoWidget(app)
        """@TODO"""

        self.console = ConsoleWidget(app)
        """@TODO"""

        # Default path for file open dialoge
        self._open_path = ""

        # Horizontal layout (thumbs, view, sidebar)
        wrapper = QFrame(self)
        wrapper.setLayout(QHBoxLayout())
        wrapper.layout().setContentsMargins(0, 0, 0, 0)
        wrapper.layout().addWidget(self.thumbs)
        wrapper.layout().addWidget(self.view)

        # @TODO Remove overlay test
        # test = OverlayWidget(self.app)
        # self.addDockWidget(Qt.RightDockWidgetArea, test)
        # test.setFloating(True);
        # test.setWindowOpacity(0.8)

        # Sidebar / Vertical layout (info, meta, console)
        sidebar = QFrame(self)
        sidebar.setLayout(QVBoxLayout())
        sidebar.layout().setContentsMargins(0, 0, 5, 0)

        # @TODO refactor into sidebar widget (base class) or QDockWidget
        info_heading = QLabel()
        info_heading.setText("FILE INFO")
        info_heading.setProperty("role", "widget_heading__first")
        info_heading.setMinimumHeight(24)
        info_heading.setMaximumHeight(24)
        sidebar.layout().addWidget(info_heading)
        sidebar.layout().addWidget(self.info)

        console_heading = QLabel()
        console_heading.setText("CONSOLE")
        console_heading.setProperty("role", "widget_heading")
        console_heading.setMinimumHeight(24)
        console_heading.setMaximumHeight(24)
        sidebar.layout().addWidget(console_heading)
        sidebar.layout().addWidget(self.console)

        wrapper.layout().addWidget(sidebar)

        self.setup_menu()
        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().addPermanentWidget(self.slice)
        self.setCentralWidget(wrapper)

        # Window dimensions
        geometry = app.desktop().availableGeometry(self)
        self.resize(geometry.width() * 0.6, geometry.height() * 0.6)

    def add_menu_item(self, menu, title, callback, shortcut=""):
        """Create menu item (DRY wrapper function)."""
        action = QAction(title, self)
        if(shortcut != ""):
            action.setShortcut(shortcut)
        action.triggered.connect(callback)
        menu.addAction(action)
        return action

    def setup_menu(self):
        ami = self.add_menu_item

        self.file_menu = self.menuBar().addMenu("&File")
        ami(self.file_menu, "&Load", self._action_open, "Ctrl+O")
        ami(self.file_menu, "&Exit", self._action_exit, "Ctrl+Q")

        self.view_menu = self.menuBar().addMenu("&View")
        ami(self.view_menu, "Zoom &in", self._action_zoom_in, "+")
        ami(self.view_menu, "Zoom &out", self._action_zoom_out, "-")
        ami(self.view_menu, "&Fit", self._action_zoom_fit, "#")
        ami(self.view_menu, "&Reset", self._action_zoom_reset, "0")

        self.mode_menu = self.menuBar().addMenu("&Mode")
        ami(self.mode_menu, "&Amplitude", partial(self._action_mode, 0), "F1")
        ami(self.mode_menu, "&Phase", partial(self._action_mode, 1), "F2")

        self.window_menu = self.menuBar().addMenu("&Window")
        ami(self.window_menu, "&Lower", self._action_win_lower, "q")
        ami(self.window_menu, "&Raise", self._action_win_raise, "w")
        ami(self.window_menu, "&Shrink", self._action_win_shrink, "a")
        ami(self.window_menu, "&Enlarge", self._action_win_enlarge, "s")
        ami(self.window_menu, "Rese&t", self._action_win_reset, "d")

        # @TODO remove after thumb test
        ami(self.file_menu, "ThumbTest", self._thumb_test, "t")

        self.functions_menu = self.menuBar().addMenu("&Evals")
        # Functions menu is built in app.setup_functions_menu
        # by calling add_function_to_menu

        # About action is its own top level menu
        ami(self.menuBar(), "&About", self._action_about)

    def add_function_to_menu(self, key, function):
        "Add a entry in `Evals` menu for `function`."
        self.add_menu_item(self.functions_menu, function.MENU_NAME,
                           partial(self._action_set_function, key))

    def _action_exit(self):
        sys.exit()

    def _action_open(self):
        path, filter = QFileDialog.getOpenFileName(None, "Open file",
                           self._open_path, "*.h5")

        if path != "":
            self._open_path = os.path.dirname(path)
            self.app.load_file(path)

    def _action_zoom_in(self):
        self.view.zoom(1.25)

    def _action_zoom_out(self):
        self.view.zoom(0.8)

    def _action_zoom_fit(self):
        self.view.zoom_fit()

    def _action_zoom_reset(self):
        self.view.zoom(1, False)

    def _action_about(self):
        webbrowser.open_new("https://github.com/calmer/PySEUS")

    def _action_win_lower(self):
        self.app.display.move_window(-20)
        self.app.refresh()

    def _action_win_raise(self):
        self.app.display.move_window(20)
        self.app.refresh()

    def _action_win_shrink(self):
        self.app.display.scale_window(-25)
        self.app.refresh()

    def _action_win_enlarge(self):
        self.app.display.scale_window(25)
        self.app.refresh()

    def _action_win_reset(self):
        self.app.display.reset_window()
        self.app.refresh()

    def _action_mode(self, mode):
        self.app.set_mode(mode)

    def _action_set_function(self, key):
        self.app.set_function(key)

    def add_thumbs(self):
        self.thumbs = ThumbsWidget(app)

    def _thumb_test(self):
        self.thumbs.add_thumb(self.app.current_slice)
