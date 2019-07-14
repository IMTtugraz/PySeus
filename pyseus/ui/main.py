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
        self.view.setScaledContents(True)

        image = QImage("./tests/test.jpg")
        self.view.setPixmap(QPixmap.fromImage(image))
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.view)

        self.setCentralWidget(self.scrollArea)

        # Window dimensions
        geometry = app.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.5, geometry.height() * 0.6)

    def setup_menu(self):
        # File Menu
        self.file_menu = self.menu.addMenu("File")

        # Load Action
        load_action = QAction("Load", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self._action_load)

        # Exit Action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self._action_exit)

        self.file_menu.addAction(load_action)
        # self.file_menu.addSeparator()
        self.file_menu.addAction(exit_action)

        # End File Menu
        
        # View Menu
        self.view_menu = self.menu.addMenu("View")

        # Zoom In Action
        zoom_in_action = QAction("Zoom in", self)
        zoom_in_action.setShortcut("+")
        zoom_in_action.triggered.connect(self._action_zoom_in)
        
        # Zoom Out Action
        zoom_out_action = QAction("Zoom out", self)
        zoom_out_action.setShortcut("-")
        zoom_out_action.triggered.connect(self._action_zoom_out)
        
        # Fit Action
        zoom_fit_action = QAction("Fit", self)
        zoom_fit_action.setShortcut("#")
        zoom_fit_action.triggered.connect(self._action_zoom_fit)
        
        # Reset Action
        reset_action = QAction("Reset", self)
        reset_action.setShortcut("0")
        reset_action.triggered.connect(self._action_zoom_reset)

        self.view_menu.addAction(zoom_in_action)
        self.view_menu.addAction(zoom_out_action)
        self.view_menu.addAction(zoom_fit_action)
        self.view_menu.addAction(reset_action)

        # End View Menu

        # About Action
        about_action = QAction("About", self)
        about_action.triggered.connect(self._action_about)

        self.menu.addAction(about_action)

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
QScrollBar:horizontal {
  background: transparent;
  height: 8px;
  margin: 2px 10px 2px 10px;
}
QScrollBar::handle:horizontal {
  background-color: #bbb;
  min-width: 12px;
  border-radius: 2px;
}
QScrollBar::handle:horizontal:hover {
  background-color: #eee;
}

QScrollBar:vertical {
  background: transparent;
  width: 8px;
  margin: 10px 2px 10px 2px;
}
QScrollBar::handle:vertical {
  background-color: #bbb;
  min-height: 12px;
  border-radius: 2px;
}
QScrollBar::handle:vertical:hover {
  background-color: #eee;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
  width: 0px;
}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical {
  height: 0px;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
  background: none;
}

QLabel { background: #111; }

QStatusBar { background: #111; color: #eee; }
"""
        )

    def _action_exit(self):
        sys.exit()
    
    def _action_load(self):
        print("load")
    
    def _action_zoom_in(self):
        print("+")
        
    def _action_zoom_out(self):
        print("-")
        
    def _action_zoom_fit(self):
        print("#")
    
    def _action_zoom_reset(self):
        print("0")
    
    def _action_about(self):
        webbrowser.open("https://github.com/calmer/PySEUS", new=0, 
            autoraise=True)

    def view(img):
        self.view.setPixmap(QPixmap.fromImage(image))
