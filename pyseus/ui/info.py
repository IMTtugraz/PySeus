from PySide2.QtCore import QSize
from PySide2.QtWidgets import QSizePolicy, QFormLayout, QFrame

from pyseus.settings import settings


class InfoWidget(QFrame):
    """The widget for file info and metadata."""

    def __init__(self, app):
        QFrame.__init__(self)
        self.app = app

        self.setLayout(QFormLayout())

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.MinimumExpanding)

        self.updateGeometry()

    def minimumSizeHint(self):
        return QSize(int(settings["ui"]["sidebar_size"]), 100)
