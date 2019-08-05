import h5py

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QApplication, QMainWindow, QScrollArea, QFrame, QLabel, QHBoxLayout, QSizePolicy
from PySide2.QtGui import QImage, QPixmap

from context import pyseus
from pyseus.ui import ViewWidget

image = QImage("test2.jpg")

class Widget2(ViewWidget):
    def __init__(self, app):
        ViewWidget.__init__(self, app)
        self.size = 200
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding)
        # self.updateGeometry()
    
    def mousePressEvent(self, event):
        self.size +=100
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding)
        self.updateGeometry()

    def sizeHint(self):
        return QSize(self.size, 0)
    
    def minimumSizeHint(self):
        return QSize(self.size, 0)


class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self)

        v1 = ViewWidget(app)
        v1.view.setPixmap(QPixmap.fromImage(image))

        v2 = Widget2(app)
        v2.view.setPixmap(QPixmap.fromImage(image))

        wrapper = QFrame(self)
        wrapper.setLayout(QHBoxLayout())
        
        wrapper.layout().addWidget(v1)
        wrapper.layout().addWidget(v2)

        self.setCentralWidget(wrapper)

app = QApplication()
app.win = MainWindow(app)
app.win.show()
app.exec_()
