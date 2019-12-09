from functools import partial

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QLabel, QScrollArea, QSizePolicy, \
                              QVBoxLayout, QFrame

from pyseus.settings import settings


class ThumbsWidget(QScrollArea):
    """The widget for scan thumbnail display."""

    def __init__(self, app):
        QScrollArea.__init__(self)
        self.app = app

        self.wrapper = QFrame()
        self.wrapper.setLayout(QVBoxLayout())
        self.wrapper.layout().setContentsMargins(5, 0, 0, 5)
        self.wrapper.layout().addStretch()

        self.thumbs = []

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.MinimumExpanding)

        # Hide horizontal scollbar
        self.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0 }")

        self.setWidgetResizable(True)
        self.setWidget(self.wrapper)

    def add_thumb(self, pixmap):
        """Add the thumbnail in `pixmap` to the widget."""
        pixmap = pixmap.scaledToWidth(int(settings["ui"]["thumb_size"]))

        thumb = QLabel()
        # thumb.setProperty("role", "current_scan")
        thumb.setPixmap(pixmap)
        thumb.mousePressEvent = partial(self._thumb_clicked,
                                        len(self.thumbs))
        thumb.setProperty("role", "scan_thumb")
        thumb.setMaximumWidth(int(settings["ui"]["thumb_size"])+2)

        self.thumbs.append(thumb)
        self.wrapper.layout().insertWidget(self.wrapper.layout().count()-1,
                                           thumb)

        self.updateGeometry()

    def clear(self):
        """Remove all thumbnails."""
        for t in self.thumbs:
            t.deleteLater()
        self.thumbs = []

    def _thumb_clicked(self, thumb, event):
        """Trigger `app.select_scan` when a thumbnail is clicked."""
        self.app.select_scan(thumb)

    def minimumSizeHint(self):
        """Return widget size; width should be `thumb_size + scrollbar_width` or 0 if there are no thumbnails."""
        if self.thumbs:
            return QSize(int(settings["ui"]["thumb_size"])+25, 0)
        else:
            return QSize(0, 0)
