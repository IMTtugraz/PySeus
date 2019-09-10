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
        # self.statusBar().addPermanentWidget(self.slice)
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
        menu_bar = self.menuBar()

        self.file_menu = menu_bar.addMenu("&File")
        ami(self.file_menu, "&Load", self._action_open, "Ctrl+O")
        ami(self.file_menu, "&Quit", self._action_quit, "Ctrl+Q")

        self.view_menu = menu_bar.addMenu("&View")
        ami(self.view_menu, "&Amplitude", partial(self._action_mode, 0), "")
        ami(self.view_menu, "&Phase", partial(self._action_mode, 1), "")
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
        ami(self.explore_menu, "Nex&t Slice", partial(self._action_slice, 1), "PgUp")
        ami(self.explore_menu, "P&revious Slice", partial(self._action_slice, -1), "PgDown")
        self.explore_menu.addSeparator()
        ami(self.explore_menu, "Next &Scan", partial(self._action_scan, 1), "Alt+PgUp")
        ami(self.explore_menu, "Previous Sc&an", partial(self._action_scan, -1), "Alt+PgDown")

        self.functions_menu = menu_bar.addMenu("&Evaluate")
        ami(self.functions_menu, "&Rectangular RoI", partial(self._action_mark_roi, 0), "1")
        # ami(self.functions_menu, "&Circular RoI", partial(self._action_mark_roi, 1), "2")
        # ami(self.functions_menu, "&Line RoI", partial(self._action_mark_roi, 2), "3")
        self.functions_menu.addSeparator()

        # Functions menu is built in app.setup_functions_menu
        # by calling add_function_to_menu

        # About action is its own top level menu
        ami(menu_bar, "&About", self._action_about)

    def add_function_to_menu(self, key, function):
        "Add a entry in `Evals` menu for `function`."
        self.add_menu_item(self.functions_menu, function.MENU_NAME,
                           partial(self._action_set_function, key))

    def _action_quit(self):
        sys.exit()

    def _action_open(self):
        path, filter = QFileDialog.getOpenFileName(None, "Open file",
                           self._open_path, "*.*")

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

    def _action_slice(self, step):
        self.app.select_slice(step, True)
    
    def _action_scan(self, step):
        self.app.select_scan(step, True)

    def resizeEvent(self, event):
        x_factor = event.size().width() / event.oldSize().width()
        y_factor = event.size().height() / event.oldSize().height()
        self.view.zoom(x_factor, True)
        # @TODO x_factor if xf < yf or xf * width * zoom_factor < viewport_x

    def _action_mark_roi(self, type):
        self.roi_mode = 0
