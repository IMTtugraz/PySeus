"""GUI elements for displaying thumbnails.

Classes
-------

**ThumbsWidget** - Widget displaying scan thumbnails in a column.
"""

from functools import partial

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QLabel, QScrollArea, QSizePolicy, \
                              QVBoxLayout, QFrame

from pyseus.settings import settings


class ThumbsWidget(QScrollArea):
    """Widget displaying scan thumbnails in a column."""

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
        for thumb in self.thumbs:
            thumb.deleteLater()
        self.thumbs = []

    def _thumb_clicked(self, thumb, event):  # pylint: disable=W0613
        """Trigger `app.select_scan` when a thumbnail is clicked."""
        self.app.select_scan(thumb)

    def minimumSizeHint(self):  # pylint: disable=C0103
        """Return widget size; width should be `thumb_size + scrollbar_width`
        or 0 if there are no thumbnails."""
        if self.thumbs:
            return QSize(int(settings["ui"]["thumb_size"])+25, 0)

        return QSize(0, 0)
