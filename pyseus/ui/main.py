import sys
import webbrowser

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QAction

class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self)
        self.setWindowTitle("PySEUS")

        self.setup_menu()

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Ready")

        # Window dimensions
        geometry = app.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

    def setup_menu(self):
        self.menu = self.menuBar()

        # File Menu
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        load_action = QAction("Load", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self._action_load)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self._action_exit)

        self.file_menu.addAction(load_action)
        self.file_menu.addAction(exit_action)

        # End File Menu
        
        # View Menu
        self.view_menu = self.menu.addMenu("View")

        # Reset QAction
        reset_action = QAction("Reset", self)
        reset_action.setShortcut("0")
        reset_action.triggered.connect(self._action_reset)

        self.view_menu.addAction(reset_action)

        # End View Menu

        # About Menu
        self.about_menu = self.menu.addMenu("About")

        # About QAction
        about_action = QAction("About", self)
        about_action.triggered.connect(self._action_about)

        self.about_menu.addAction(about_action)

        # End View Menu

    def _action_exit(self):
        sys.exit()
    
    def _action_load(self):
        pass
    
    def _action_reset(self):
        pass
    
    def _action_about(self):
        webbrowser.open("https://github.com/calmer/PySEUS", new=0, 
            autoraise=True)
