import numpy
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

        self.npa = numpy.loadtxt("npa.txt", numpy.uint8)

        h, w = self.npa.shape
        image = QImage(self.npa.data, w, h, w, \
            QImage.Format_Grayscale8)

        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

        self.setCentralWidget(self.imageLabel)

        # Window dimensions
        geometry = app.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.4, geometry.height() * 0.4)

    def wheelEvent(self, event):
        if(event.delta() > 0):
            h, w = self.npa.shape
            data = numpy.asarray(self.npa.data) * 1.2
            image = QImage(data, w, h, w, \
            QImage.Format_Grayscale8)
            self.imageLabel.setPixmap(QPixmap.fromImage(image))
        else:
            h, w = self.npa.shape
            data = numpy.asarray(self.npa.data) * 0.8
            image = QImage(data, w, h, w, \
            QImage.Format_Grayscale8)
            self.imageLabel.setPixmap(QPixmap.fromImage(image))

if __name__ == "__main__":
    app = QApplication()
    app.window = MainWindow(app)
    app.window.show()
    sys.exit(app.exec_())
