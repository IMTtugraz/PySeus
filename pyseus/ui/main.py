import sys
import webbrowser

from PySide2.QtWidgets import QMainWindow, QAction, \
    QLabel, QFileDialog, QFrame, QVBoxLayout, QHBoxLayout

from .view import ViewWidget
from .console import ConsoleWidget
from .info import InfoWidget
from .thumbs import ThumbsWidget


class MainWindow(QMainWindow):
    """The main window for PySeus."""

    def __init__(self, app):
        QMainWindow.__init__(self)
        self.setWindowTitle("PySEUS")
        self.app = app

        self.menu = self.menuBar()
        self.setup_menu()

        self.status = self.statusBar()

        self.thumbs = ThumbsWidget(app)

        self.view = ViewWidget(app)

        self.info = InfoWidget(app)
        self.console = ConsoleWidget(app)

        # Layout
        self.wrapper = QFrame(self)
        self.wrapper.setLayout(QHBoxLayout())
        self.wrapper.layout().setContentsMargins(0, 0, 0, 0)

        self.wrapper.layout().addWidget(self.thumbs)

        self.wrapper.layout().addWidget(self.view)

        self.sidebar = QFrame(self)
        self.sidebar.setLayout(QVBoxLayout())
        self.sidebar.layout().setContentsMargins(0, 0, 5, 5)

        info_heading = QLabel()
        info_heading.setText("FILE INFO")
        info_heading.setProperty("role", "widget_heading__first")
        info_heading.setMinimumHeight(24)
        info_heading.setMaximumHeight(24)
        self.sidebar.layout().addWidget(info_heading)
        self.sidebar.layout().addWidget(self.info)

        console_heading = QLabel()
        console_heading.setText("CONSOLE")
        console_heading.setProperty("role", "widget_heading")
        console_heading.setMinimumHeight(24)
        console_heading.setMaximumHeight(24)
        self.sidebar.layout().addWidget(console_heading)
        self.sidebar.layout().addWidget(self.console)

        self.wrapper.layout().addWidget(self.sidebar)

        self.setCentralWidget(self.wrapper)

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

        self.file_menu = self.menu.addMenu("&File")
        ami(self.file_menu, "&Load", self._action_open, "Ctrl+O")
        ami(self.file_menu, "&Exit", self._action_exit, "Ctrl+Q")

        self.view_menu = self.menu.addMenu("&View")
        ami(self.view_menu, "Zoom &in", self._action_zoom_in, "+")
        ami(self.view_menu, "Zoom &out", self._action_zoom_out, "-")
        ami(self.view_menu, "&Fit", self._action_zoom_fit, "#")
        ami(self.view_menu, "&Reset", self._action_zoom_reset, "0")

        self.mode_menu = self.menu.addMenu("&Mode")
        ami(self.mode_menu, "&Amplitude", self._action_mode_ampl, "1")
        ami(self.mode_menu, "&Phase", self._action_mode_phase, "2")

        self.window_menu = self.menu.addMenu("&Window")
        ami(self.window_menu, "&Lower", self._action_win_lower, "q")
        ami(self.window_menu, "&Raise", self._action_win_raise, "w")
        ami(self.window_menu, "&Shrink", self._action_win_shrink, "a")
        ami(self.window_menu, "&Enlarge", self._action_win_enlarge, "s")
        ami(self.window_menu, "Rese&t", self._action_win_reset, "d")

        # @TODO remove import; maybe call "add function to menu" from app ?!?
        # self.functions_menu = self.menu.addMenu("&Evals")
        # from ..core import PySeus
        # for f in PySeus.functions:
        #     ami(self.functions_menu, f, self._action_set_fct)

        # About action is its own top level menu
        ami(self.menu, "&About", self._action_about)

    def _action_exit(self):
        sys.exit()

    def _action_open(self):
        path, filter = QFileDialog.getOpenFileName(None, "Open file",
                                                   ".", "*.h5")
        self.app.load_file(path)

    def _action_zoom_in(self):
        self.view.zoom(1.25)

    def _action_zoom_out(self):
        self.view.zoom(0.8)

    def _action_zoom_fit(self):
        image = self.view.view.pixmap().size()
        viewport = self.view.size()
        v_zoom = viewport.height() / image.height()
        h_zoom = viewport.width() / image.width()
        self.view.zoom(min(v_zoom, h_zoom)*0.99, False)

    def _action_zoom_reset(self):
        self.view.zoom(1, False)

    def _action_about(self):
        webbrowser.open("https://github.com/calmer/PySEUS", new=0,
                        autoraise=True)

    def _action_win_lower(self):
        self.app.mode.move(-20)
        self.app.refresh()

    def _action_win_raise(self):
        self.app.mode.move(20)
        self.app.refresh()

    def _action_win_shrink(self):
        self.app.mode.scale(-25)
        self.app.refresh()

    def _action_win_enlarge(self):
        self.app.mode.scale(25)
        self.app.refresh()

    def _action_win_reset(self):
        self.app.mode.reset()
        self.app.refresh()

    def _action_mode_ampl(self):
        self.app.set_mode("Amplitude")

    def _action_mode_phase(self):
        self.app.set_mode("Phase")

    def _action_set_fct(self):
        from ..core import PySeus
        fct = self.sender().text()
        self.app.set_function(PySeus.functions[fct])
