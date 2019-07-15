from math import floor
import keyboard
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



        self.menu = self.menuBar()
        
        out_action = QAction("-", self)
        out_action.setShortcut("-")
        out_action.triggered.connect(self._action_out)
        self.menu.addAction(out_action)
        
        reset_action = QAction("0", self)
        reset_action.setShortcut("0")
        reset_action.triggered.connect(self._action_reset)
        self.menu.addAction(reset_action)

        fit_action = QAction("#", self)
        fit_action.setShortcut("#")
        fit_action.triggered.connect(self._action_fit)
        self.menu.addAction(fit_action)

        in_action = QAction("+", self)
        in_action.setShortcut("+")
        in_action.triggered.connect(self._action_in)
        self.menu.addAction(in_action)



        self.imageLabel = QLabel()
        self.imageLabel.setScaledContents(True)

        image = QImage("test.jpg")
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.zoom_factor = 1



        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.imageLabel)

        self.setCentralWidget(self.scrollArea)

        # Window dimensions
        geometry = app.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.4, geometry.height() * 0.4)

    # Test Actions
    def _action_in(self):
        self.zoom_factor = self.zoom_factor * 1.25
        self.imageLabel.resize(self.zoom_factor * self.imageLabel.pixmap().size())
    
    def _action_out(self):
        self.zoom_factor = self.zoom_factor * 0.8
        self.imageLabel.resize(self.zoom_factor * self.imageLabel.pixmap().size())
    
    def _action_reset(self):
        self.zoom_factor = 1
        self.imageLabel.resize(self.imageLabel.pixmap().size())
    
    def _action_fit(self):
        image = self.imageLabel.pixmap().size()
        viewport = self.scrollArea.size()
        v_zoom = viewport.height() / image.height()
        h_zoom = viewport.width() / image.width()
        self.zoom_factor = min(v_zoom, h_zoom)*0.99
        self.imageLabel.resize(self.zoom_factor * self.imageLabel.pixmap().size())

if __name__ == "__main__":
    app = QApplication()
    app.window = MainWindow(app)
    app.window.show()
    sys.exit(app.exec_())
