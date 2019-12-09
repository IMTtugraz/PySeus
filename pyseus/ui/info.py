from PySide2.QtCore import QSize
from PySide2.QtWidgets import QSizePolicy, QFormLayout, QHBoxLayout, \
                              QVBoxLayout, QFrame, QLabel, QLineEdit

from pyseus.settings import settings


class InfoWidget(QFrame):
    """The widget for file info. Displays path, scan ID and slice index."""

    def __init__(self, app):
        QFrame.__init__(self)
        self.app = app

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.path = QLineEdit("")
        self.scan = QLineEdit("")
        self.slice = QLabel("")

        info = QFrame()
        info.setLayout(QFormLayout())
        info.layout().addRow("Path:", self.path)
        info.layout().addRow("Scan:", self.scan)
        info.layout().addRow("Slice:", self.slice)
        self.layout().addWidget(info)

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.Fixed)

        self.updateGeometry()

    def minimumSizeHint(self):
        """Return widget size to ensure unifrom sidebar width."""
        return QSize(int(settings["ui"]["sidebar_size"]), 80)

    def update_slice(self, current, max):
        """Update the displayed slice index."""
        self.slice.setText("{} / {}".format(current+1, max))

    def update_scan(self, scan):
        """Update the displayed scan ID."""
        self.scan.setText("{}".format(scan))

    def update_path(self, path):
        """Update the displayed path."""
        self.path.setText(path)
