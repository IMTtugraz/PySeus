import os
import sys
import webbrowser

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, \
    QLabel, QScrollArea, QFileDialog
from PySide2.QtGui import QImage, QPixmap

class MainWindow(QMainWindow):
    MA_PAN    = 3
    MA_WINDOW = 2
    MA_ROI    = 1

    def __init__(self, app):
        QMainWindow.__init__(self)
        self.setWindowTitle("PySEUS")
        self.app = app

        # Menu Bar
        self.menu = self.menuBar()
        self.setup_menu()

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Ready")
        
        # Image View & Scroll Area
        self.view = QLabel()
        self.view.setScaledContents(True)
        self.zoom_factor = 1
        self.mouse_action = 0

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.view)
        # Reset Scroll event Handler
        self.scrollArea.wheelEvent = lambda e: False

        self.setCentralWidget(self.scrollArea)

        # Window dimensions
        geometry = app.desktop().availableGeometry(self)
        self.resize(geometry.width() * 0.5, geometry.height() * 0.6)

    def add_menu_item(self, menu, title, callback, shortcut = ""):
        action = QAction(title, self)
        if(shortcut != ""):
            action.setShortcut(shortcut)
        action.triggered.connect(callback)
        menu.addAction(action)
        return action

    def setup_menu(self):
        # File Menu
        self.file_menu = self.menu.addMenu("File")

        self.add_menu_item(self.file_menu, "Load", self._action_open, "Ctrl+O")
        self.add_menu_item(self.file_menu, "Exit", self._action_exit, "Ctrl+Q")
        
        # View Menu
        self.view_menu = self.menu.addMenu("View")

        self.add_menu_item(self.view_menu, "Zoom in", self._action_zoom_in, "+")
        self.add_menu_item(self.view_menu, "Zoom out", self._action_zoom_out, "-")
        self.add_menu_item(self.view_menu, "Fit", self._action_zoom_fit, "#")
        self.add_menu_item(self.view_menu, "Reset", self._action_zoom_reset, "0")

        # Window Menu
        self.window_menu = self.menu.addMenu("Window")

        self.add_menu_item(self.window_menu, "Lower", self._action_win_lower, "q")
        self.add_menu_item(self.window_menu, "Raise", self._action_win_raise, "w")
        self.add_menu_item(self.window_menu, "Shrink", self._action_win_shrink, "a")
        self.add_menu_item(self.window_menu, "Enlarge", self._action_win_enlarge, "s")
        self.add_menu_item(self.window_menu, "Reset", self._action_win_reset, "d")

        # About Menu
        self.add_menu_item(self.menu, "About", self._action_about)

    def _action_exit(self):
        sys.exit()
    
    def _action_open(self):
        path, filter = QFileDialog.getOpenFileName(None, "Open file", ".", "*.h5")
        self.app.load_file(path)
    
    def zoom(self, factor, relative = True):
        if relative and not (0.1 <= self.zoom_factor * factor <= 10):
            return

        self.zoom_factor = self.zoom_factor * factor if relative else factor
        self.view.resize(self.zoom_factor * self.view.pixmap().size())

        self.scrollArea.verticalScrollBar().setValue(int(factor * \
            self.scrollArea.verticalScrollBar().value() + \
            ((factor - 1) * self.scrollArea.verticalScrollBar().pageStep()/2)))
        self.scrollArea.horizontalScrollBar().setValue(int(factor * \
            self.scrollArea.horizontalScrollBar().value() + \
            ((factor - 1) * self.scrollArea.horizontalScrollBar().pageStep()/2)))

    def _action_zoom_in(self):
        self.zoom(1.25)
        
    def _action_zoom_out(self):
        self.zoom(0.8)
        
    def _action_zoom_fit(self):
        image = self.view.pixmap().size()
        viewport = self.scrollArea.size()
        v_zoom = viewport.height() / image.height()
        h_zoom = viewport.width() / image.width()
        self.zoom(min(v_zoom, h_zoom)*0.99, False)
    
    def _action_zoom_reset(self):
        self.zoom(1, False)
    
    def _action_about(self):
        webbrowser.open("https://github.com/calmer/PySEUS", new=0, 
            autoraise=True)

    def mousePressEvent(self, event):
        self.last_position = event.pos()
        if(event.buttons() == QtCore.Qt.RightButton):
            self.mouse_action = self.MA_PAN
        elif(event.buttons() == QtCore.Qt.MiddleButton):
            self.mouse_action = self.MA_WINDOW
        elif(event.buttons() == QtCore.Qt.LeftButton):
            self.mouse_action = self.MA_ROI
            print("roi")
        else:
            self.mouse_action = 0 # nothing

    def mouseReleaseEvent(self, event):
        self.last_position = None
        self.mouse_action = 0

    def mouseMoveEvent(self, event):
        if(self.mouse_action == self.MA_PAN):
            vertical = self.scrollArea.verticalScrollBar().value() \
                + self.last_position.y() - event.pos().y()
            horizontal = self.scrollArea.horizontalScrollBar().value() \
                + self.last_position.x() - event.pos().x()

            self.scrollArea.verticalScrollBar().setValue(vertical)
            self.scrollArea.horizontalScrollBar().setValue(horizontal)
            self.last_position = event.pos()

        elif(self.mouse_action == self.MA_WINDOW):
            move = self.last_position.x() - event.pos().x()
            scale = self.last_position.y() - event.pos().y()
            self.last_position = event.pos()
            self.app.mode.adjust(move, scale)
            self.app.refresh()
        
        elif(self.mouse_action == self.MA_ROI):
            pass
    
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

    def wheelEvent(self, event):
        self.zoom(0.8 if event.delta() < 0 else 1.25)
