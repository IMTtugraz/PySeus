from functools import partial

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

        self.thumbs = []

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.MinimumExpanding)

        # Hide horizontal scollbar
        self.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0 }")

        self.setWidgetResizable(True)
        self.setWidget(self.wrapper)

    def add_thumb(self, data):
        data = self.app.display.prepare(data.copy())

        image = QImage(data.data, data.shape[1],
                       data.shape[0], data.strides[0],
                       QImage.Format_Grayscale8)

        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaledToWidth(int(settings["ui"]["thumb_size"]))

        thumb = QLabel()
        thumb.setPixmap(pixmap)
        thumb.mousePressEvent = partial(self._thumb_clicked, 
                                        self.wrapper.layout().count()-1)

        self.thumbs.append(thumb)
        self.wrapper.layout().insertWidget(self.wrapper.layout().count()-1, 
                                           thumb)

        self.updateGeometry()


    def clear(self):
        for t in self.thumbs:
            t.deleteLater()
        self.thumbs = []
    
    def _thumb_clicked(self, thumb, event):
        self.thumb_clicked(thumb)
    
    def thumb_clicked(self, thumb):
        pass

    def minimumSizeHint(self):
        if self.thumbs:
            return QSize(int(settings["ui"]["thumb_size"])+16, 0)
        else:
            return QSize(0,0)
