from PySide2.QtWidgets import QApplication, QMainWindow, QScrollArea, QLabel
from PySide2.QtGui import QImage, QPixmap

class ViewWidget(QScrollArea):
    def __init__(self):
        QScrollArea.__init__(self)

        imageLabel = QLabel()
        image = QImage("test.jpg")
        imageLabel.setPixmap(QPixmap.fromImage(image))

        self.setWidget(imageLabel)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        viewport = ViewWidget()

        self.setCentralWidget(viewport)

app = QApplication()
app.win = MainWindow()
app.win.show()
app.exec_()
