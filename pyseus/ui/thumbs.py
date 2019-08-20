from PySide2.QtCore import QSize
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QLabel, QScrollArea, QSizePolicy, \
    QVBoxLayout, QFrame, QSpacerItem

from pyseus.settings import settings


class ThumbsWidget(QScrollArea):
    """The widget for thumb thumbnail display."""

    def __init__(self, app):
        QScrollArea.__init__(self)
        self.app = app

        self.wrapper = QFrame()
        self.wrapper.setLayout(QVBoxLayout())
        self.wrapper.layout().addStretch()
        self.setProperty("debug", "green")
        self.wrapper.setProperty("debug", "red")

        self.thumbs = []

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.MinimumExpanding)

        # Hide horizontal scollbar
        self.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0 }")

        self.setWidgetResizable(True)
        self.setWidget(self.wrapper)

    def add_thumbs(self):
        image = QImage("test2.jpg")
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaledToWidth(int(settings["ui"]["thumb_size"]))

        self.thumbs.append(QLabel())
        self.thumbs[-1].setScaledContents(True)
        self.thumbs[-1].setProperty("debug", "blue")
        self.thumbs[-1].setScaledContents(True)
        self.thumbs[-1].setPixmap(pixmap)

        layout = self.wrapper.layout()
        layout.insertWidget(layout.count() - 1, self.thumbs[-1])
        self.wrapper.updateGeometry()

        # image = QImage(data.data, data.shape[1],
                    #    data.shape[0], data.strides[0],
                    #    QImage.Format_Grayscale8)
        # pixmap = QPixmap.fromImage(image)

        # thumb = QLabel()
        # thumb.setScaledContents(True)
        # thumb.setPixmap(pixmap)

        # self.thumbs.append(thumb)
        # self.wrapper.layout().addWidget(thumb)

    def clear(self):
        for t in self.thumbs:
            t.deleteLater()
        self.thumbs = []

    def minimumSizeHint(self):
        return QSize(int(settings["ui"]["thumb_size"])+24, 0)
