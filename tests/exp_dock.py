from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtWidgets import QMainWindow, QDockWidget, QPushButton, QFrame, QLabel
from PySide2.QtCore import Qt


class DockTest(QDockWidget):
    def __init__(self):
        QDockWidget.__init__(self)
        button = QPushButton("Test")
        self.setWidget(button)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        label = QLabel("Test")
        self.setTitleBarWidget(label)
    
    def mouseMoveEvent(self, event):
        event.ignore()
    
    def mousePressEvent(self, event):
        event.ignore()
    
    def mouseReleaseEvent(self, event):
        event.ignore()

class WindowTest(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        test = DockTest()
        self.addDockWidget(Qt.LeftDockWidgetArea, test)
        test.setFloating(True);
        test.setWindowOpacity(0.8)
        self.setCentralWidget(QFrame())


app = QApplication()
app.setStyleSheet("""
QPushButton { margin: 20px; }
QDockWidget, QDockWidget::title {
    background: red;
}
""")
win = WindowTest()
win.show()
app.exec_()
