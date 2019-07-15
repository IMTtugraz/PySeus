from math import floor
import keyboard
import sys
import webbrowser

from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, \
    QLabel, QScrollArea
from PySide2.QtGui import QImage, QPixmap, QPalette

class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self)
        self.setWindowTitle("PySEUS")

        self.imageLabel = QLabel()
        self.imageLabel.setScaledContents(True)

        image = QImage("test.jpg")
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.zoom_factor = 1
        self.imageLabel.setAlignment(Qt.AlignHCenter & Qt.AlignHCenter)



        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.imageLabel)

        # Reset Scroll event Handler
        self.scrollArea.wheelEvent = lambda e: False




        self.setCentralWidget(self.scrollArea)

        # Window dimensions
        geometry = app.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.4, geometry.height() * 0.4)

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
        change = 0.8 if event.delta() < 0 else 1.25
        if(self.zoom_factor * change > 5 or self.zoom_factor * change < 0.1): return
            
        self.zoom_factor = self.zoom_factor * change
        self.imageLabel.resize(self.zoom_factor * self.imageLabel.pixmap().size())

        self.scrollArea.verticalScrollBar().setValue(int(change * \
            self.scrollArea.verticalScrollBar().value() + \
            ((change - 1) * self.scrollArea.verticalScrollBar().pageStep()/2)))
        self.scrollArea.horizontalScrollBar().setValue(int(change * \
            self.scrollArea.horizontalScrollBar().value() + \
            ((change - 1) * self.scrollArea.horizontalScrollBar().pageStep()/2)))

if __name__ == "__main__":
    app = QApplication()
    app.window = MainWindow(app)
    app.window.show()
    sys.exit(app.exec_())
