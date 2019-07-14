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
        self.setup_stylesheet(app)

        # Menu Bar
        self.menu = self.menuBar()
        self.setup_menu()

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Ready")
        
        # Image View & Scroll Area
        self.view = QLabel()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.view)

        self.setCentralWidget(self.scrollArea)

        # Window dimensions
        geometry = app.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.5, geometry.height() * 0.6)

    def setup_menu(self):
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

        # End About Menu

    def setup_stylesheet(self, app):
        app.setStyleSheet("""
QMenuBar { background: #111; color: #ddd; }
QMenuBar::item { padding: 5px 10px 5px 10px; }
QMenuBar::item:selected { background: #222; }
QMenu { background: #222; color: #eee; padding: 0px; }
QMenu::item { padding: 5px 10px 5px 10px; }
QMenu::item:selected { background: #333; }
QScrollArea { background: #111; border: none; }
QLabel { background: #111; }
QStatusBar { background: #222; color: #eee; }
"""
        )

    def _action_exit(self):
        sys.exit()
    
    def _action_load(self):
        pass
    
    def _action_reset(self):
        pass
    
    def _action_about(self):
        webbrowser.open("https://github.com/calmer/PySEUS", new=0, 
            autoraise=True)

    def view(img):
        self.view.setPixmap(QPixmap.fromImage(image))
