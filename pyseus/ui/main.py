import sys
import webbrowser

from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QAction, \
    QLabel, QScrollArea, QFileDialog


class MainWindow(QMainWindow):
    """The main window for PySeus."""

    def __init__(self, app):
        QMainWindow.__init__(self)
        self.setWindowTitle("PySEUS")
        self.app = app

        # Menu Bar
        self.menu = self.menuBar()
        self.setup_menu()

        # Status Bar
        self.status = self.statusBar()
        # Image View & Scroll Area
        self.view = QLabel()
        self.view.setScaledContents(True)
        self.zoom_factor = 1
        self.mouse_action = 0

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.view)
        # Reset Scroll event Handler
        self.scroll_area.wheelEvent = lambda e: False

        self.setCentralWidget(self.scroll_area)

        # Window dimensions
        geometry = app.desktop().availableGeometry(self)
        self.resize(geometry.width() * 0.5, geometry.height() * 0.6)

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

        # File Menu
        self.file_menu = self.menu.addMenu("File")

        ami(self.file_menu, "Load", self._action_open, "Ctrl+O")
        ami(self.file_menu, "Exit", self._action_exit, "Ctrl+Q")
        # View Menu
        self.view_menu = self.menu.addMenu("View")

        ami(self.view_menu, "Zoom in", self._action_zoom_in, "+")
        ami(self.view_menu, "Zoom out", self._action_zoom_out, "-")
        ami(self.view_menu, "Fit", self._action_zoom_fit, "#")
        ami(self.view_menu, "Reset", self._action_zoom_reset, "0")

        # Mode Menu
        self.mode_menu = self.menu.addMenu("Mode")

        ami(self.mode_menu, "Amplitude", self._action_mode_ampl, "1")
        ami(self.mode_menu, "Phase", self._action_mode_phase, "2")
        # Window Menu
        self.window_menu = self.menu.addMenu("Window")

        ami(self.window_menu, "Lower", self._action_win_lower, "q")
        ami(self.window_menu, "Raise", self._action_win_raise, "w")
        ami(self.window_menu, "Shrink", self._action_win_shrink, "a")
        ami(self.window_menu, "Enlarge", self._action_win_enlarge, "s")
        ami(self.window_menu, "Reset", self._action_win_reset, "d")

        # Functions Menu
        self.functions_menu = self.menu.addMenu("Functions")
        from ..core import PySeus
        for f in PySeus.functions:
            ami(self.functions_menu, f, self._action_set_fct)

        # About Menu
        ami(self.menu, "About", self._action_about)

    def _action_exit(self):
        sys.exit()

    def _action_open(self):
        path, filter = QFileDialog.getOpenFileName(None, "Open file",
                                                   ".", "*.h5")
        self.app.load_file(path)

    def zoom(self, factor, relative=True):
        if relative and not (0.1 <= self.zoom_factor * factor <= 10):
            return

        self.zoom_factor = self.zoom_factor * factor if relative else factor
        self.view.resize(self.zoom_factor * self.view.pixmap().size())

        # @TODO Refactor into View Widgete (!!!)
        v_scroll = int(factor * self.scroll_area.verticalScrollBar().value() +
            ((factor - 1) * self.scroll_area.verticalScrollBar().pageStep()/2))
        self.scroll_area.verticalScrollBar().setValue(v_scroll)
        
        # @TODO Refactor into View Widgete (!!!)
        h_scroll = int(factor * self.scroll_area.horizontalScrollBar().value() +
            ((factor - 1) * self.scroll_area.horizontalScrollBar().pageStep()/2))
        self.scroll_area.horizontalScrollBar().setValue(h_scroll)

    def _action_zoom_in(self):
        self.zoom(1.25)

    def _action_zoom_out(self):
        self.zoom(0.8)

    def _action_zoom_fit(self):
        image = self.view.pixmap().size()
        viewport = self.scroll_area.size()
        v_zoom = viewport.height() / image.height()
        h_zoom = viewport.width() / image.width()
        self.zoom(min(v_zoom, h_zoom)*0.99, False)

    def _action_zoom_reset(self):
        self.zoom(1, False)

    def _action_about(self):
        webbrowser.open("https://github.com/calmer/PySEUS", new=0,
                        autoraise=True)

    def mousePressEvent(self, event):
        """Handle pan, window and RoI functionality on mouse button down."""
        self.last_position = event.pos()
        if(event.buttons() == QtCore.Qt.RightButton):
            self.mouse_action = "PAN"
        elif(event.buttons() == QtCore.Qt.MiddleButton):
            self.mouse_action = "WINDOW"
        elif(event.buttons() == QtCore.Qt.LeftButton):
            self.mouse_action = "ROI"
            scroll_x = int(self.scroll_area.horizontalScrollBar().value()
                           / self.zoom_factor)
            scroll_y = int(self.scroll_area.verticalScrollBar().value()
                           / self.zoom_factor)
            self.app.roi[0] = int((event.pos().x()) / self.zoom_factor) \
                + scroll_x
            self.app.roi[1] = int((event.pos().y() - 26) / self.zoom_factor) \
                + scroll_y
        else:
            self.mouse_action = ""  # nothing

    def mouseReleaseEvent(self, event):
        """Handle pan, window and RoI functionality on mouse button up."""
        if(self.mouse_action == "ROI"):
            scroll_x = int(self.scroll_area.horizontalScrollBar().value()
                           / self.zoom_factor)
            scroll_y = int(self.scroll_area.verticalScrollBar().value()
                           / self.zoom_factor)
            roi_end_x = int((event.pos().x()) / self.zoom_factor) + scroll_x
            roi_end_y = int((event.pos().y() - 26) / self.zoom_factor) \
                + scroll_y
            if(self.app.roi[0] == roi_end_x and self.app.roi[1] == roi_end_y):
                self.app.roi = [0, 0, 0, 0]
                self.app.refresh()
            self.app.recalculate()

        self.last_position = None
        self.mouse_action = 0

    def mouseMoveEvent(self, event):
        """Handle pan, window and RoI functionality on mouse move."""
        if(self.mouse_action == "PAN"):
            vertical = self.scroll_area.verticalScrollBar().value() \
                + self.last_position.y() - event.pos().y()
            horizontal = self.scroll_area.horizontalScrollBar().value() \
                + self.last_position.x() - event.pos().x()

            self.scroll_area.verticalScrollBar().setValue(vertical)
            self.scroll_area.horizontalScrollBar().setValue(horizontal)
            self.last_position = event.pos()

        elif(self.mouse_action == "WINDOW"):
            move = self.last_position.x() - event.pos().x()
            scale = self.last_position.y() - event.pos().y()
            self.last_position = event.pos()
            self.app.mode.adjust(move, scale)
            self.app.refresh()
        elif(self.mouse_action == "ROI"):
            scroll_x = int(self.scroll_area.horizontalScrollBar().value()
                           / self.zoom_factor)
            scroll_y = int(self.scroll_area.verticalScrollBar().value()
                           / self.zoom_factor)
            self.app.roi[2] = int((event.pos().x()) / self.zoom_factor) \
                + scroll_x
            self.app.roi[3] = int((event.pos().y() - 26) / self.zoom_factor) \
                + scroll_y
            self.app.refresh()

    def wheelEvent(self, event):
        self.zoom(0.8 if event.delta() < 0 else 1.25)

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
