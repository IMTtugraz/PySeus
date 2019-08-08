from PySide2.QtCore import QSize
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QLabel, QScrollArea, QSizePolicy, \
    QVBoxLayout, QFrame

from pyseus.settings import settings


class ThumbsWidget(QScrollArea):
    """The widget for thumb thumbnail display."""

    def __init__(self, app):
        QScrollArea.__init__(self)
        self.app = app

        self.wrapper = QFrame()
        self.wrapper.setLayout(QVBoxLayout())

        self.thumbs = []
        image = QImage("test2.jpg")
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaledToWidth(int(settings["ui"]["thumb_size"]))
        for i in range(5):
            self.thumbs.append(QLabel())
            self.thumbs[i].setScaledContents(True)
            self.thumbs[i].setPixmap(pixmap)
            self.wrapper.layout().addWidget(self.thumbs[i])

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.MinimumExpanding)

        # Hide horizontal scollbar
        self.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0 }")

        self.setWidget(self.wrapper)

    def minimumSizeHint(self):
        return QSize(int(settings["ui"]["thumb_size"])+20, 300)
