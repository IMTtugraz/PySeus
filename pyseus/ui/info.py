from PySide2.QtCore import QSize
from PySide2.QtWidgets import QSizePolicy, QFormLayout, QHBoxLayout, QFrame, QLabel, QSpinBox

from pyseus.settings import settings


class InfoWidget(QFrame):
    """The widget for file info and metadata."""

    def __init__(self, app):
        QFrame.__init__(self)
        self.app = app

        self.setLayout(QFormLayout())

        self.location = QLabel("Location")
        self.scan = QLabel("Scan")
        self.slice = QHBoxLayout()
        self.current_slice = QLabel("0 / 7")
        # self.current_slice = QSpinBox()
        # self.current_slice.setMaximumWidth(50)
        # self.max_slice = QLabel("/ 7")
        self.slice.addWidget(self.current_slice)
        # self.slice.addWidget(self.max_slice)

        self.layout().addRow("Location:", self.location)
        self.layout().addRow("Scan:", self.scan)
        self.layout().addRow("Slice:", self.slice)

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.MinimumExpanding)

        self.updateGeometry()

    def minimumSizeHint(self):
        return QSize(int(settings["ui"]["sidebar_size"]), 100)
