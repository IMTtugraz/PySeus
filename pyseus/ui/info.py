from PySide2.QtCore import QSize
from PySide2.QtWidgets import QSizePolicy, QFormLayout, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QSpinBox, QLineEdit, QPushButton

from pyseus.settings import settings


class InfoWidget(QFrame):
    """The widget for file info."""

    def __init__(self, app):
        QFrame.__init__(self)
        self.app = app

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.path = QLineEdit("")
        self.scan = QLineEdit("")
        self.slice = QHBoxLayout()
        self.current_slice = QLabel("")
        # self.current_slice = QSpinBox()
        # self.current_slice.setMaximumWidth(50)
        # self.max_slice = QLabel("/ 7")
        self.slice.addWidget(self.current_slice)
        # self.slice.addWidget(self.max_slice)

        info = QFrame()
        info.setLayout(QFormLayout())
        # info.layout().setContentsMargins(0, 0, 0, 0)
        info.layout().addRow("Path:", self.path)
        info.layout().addRow("Scan:", self.scan)
        info.layout().addRow("Slice:", self.slice)
        self.layout().addWidget(info)

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.MinimumExpanding)

        self.updateGeometry()

    def minimumSizeHint(self):
        return QSize(int(settings["ui"]["sidebar_size"]), 100)

    def update_slice(self, current, max):
        self.current_slice.setText("{} / {}".format(current+1, max))

    def update_scan(self, scan):
        self.scan.setText("{}".format(scan))
    
    def update_path(self, path):
        self.path.setText(path)
