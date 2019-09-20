from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QSizePolicy, QDockWidget, QPushButton, QLabel

from pyseus.settings import settings


class OverlayWidget(QDockWidget):
    """@TODO"""

    def __init__(self, app):
        QDockWidget.__init__(self)
        self.app = app

        button = QPushButton("Test")
        self.setWidget(button)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        label = QLabel("Test")
        self.setTitleBarWidget(label)

    def minimumSizeHint(self):
        return QSize(int(settings["ui"]["sidebar_size"]), 100)

    def mouseMoveEvent(self, event):
        event.ignore()
    
    def mousePressEvent(self, event):
        event.ignore()
    
    def mouseReleaseEvent(self, event):
        event.ignore()
