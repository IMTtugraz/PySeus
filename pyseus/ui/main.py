import os
import sys
import webbrowser

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, \
    QLabel, QScrollArea
from PySide2.QtGui import QImage, QPixmap, QPalette

class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self)
        self.setWindowTitle("PySEUS")
        self.app = app

        # Stylesheet
        qss = os.path.join(os.path.dirname(__file__), "style.qss")
        with open(qss,"r") as f:
            app.setStyleSheet(f.read())

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
        self.mouse_move_mode = 0

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

        self.add_menu_item(self.file_menu, "Load", self._action_load, "Ctrl+O")
        self.add_menu_item(self.file_menu, "Exit", self._action_exit, "Ctrl+Q")
        
        # View Menu
        self.view_menu = self.menu.addMenu("View")

        self.add_menu_item(self.view_menu, "Zoom in", self._action_zoom_in, "+")
        self.add_menu_item(self.view_menu, "Zoom out", self._action_zoom_out, "-")
        self.add_menu_item(self.view_menu, "Fit", self._action_zoom_fit, "#")
        self.add_menu_item(self.view_menu, "Reset", self._action_zoom_reset, "0")

        # About Menu
        self.add_menu_item(self.menu, "About", self._action_about)

    def _action_exit(self):
        sys.exit()
    
    def _action_load(self):
        print("load")
    
    def zoom(self, factor, relative = True):
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
            self.mouse_move_mode = 3 # pan
        elif(event.buttons() == QtCore.Qt.MiddleButton):
            self.mouse_move_mode = 2 # window
            print("window")
        elif(event.buttons() == QtCore.Qt.LeftButton):
            self.mouse_move_mode = 1 # mark roi
            print("mark roi")
        else:
            self.mouse_move_mode = 0 # nothing

    def mouseReleaseEvent(self, event):
        self.last_position = None
        self.mouse_move_mode = 0

    def mouseMoveEvent(self, event):
        if(self.mouse_move_mode == 3): # pan
            vertical = self.scrollArea.verticalScrollBar().value() \
                + self.last_position.y() - event.pos().y()
            horizontal = self.scrollArea.horizontalScrollBar().value() \
                + self.last_position.x() - event.pos().x()

            self.scrollArea.verticalScrollBar().setValue(vertical)
            self.scrollArea.horizontalScrollBar().setValue(horizontal)
            self.last_position = event.pos()
    
    def wheelEvent(self, event):
        self.zoom(0.8 if event.delta() < 0 else 1.25)
