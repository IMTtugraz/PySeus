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

        imageLabel = QLabel()
        image = QImage("test.jpg")
        imageLabel.setPixmap(QPixmap.fromImage(image))

        scrollArea = QScrollArea()
        scrollArea.setWidget(imageLabel)

        self.setCentralWidget(scrollArea)

        # Window dimensions
        geometry = app.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.4, geometry.height() * 0.4)

if __name__ == "__main__":
    app = QApplication()
    app.window = MainWindow(app)
    app.window.show()
    sys.exit(app.exec_())
