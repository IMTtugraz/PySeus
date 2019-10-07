from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QDialog, QSizePolicy, QFormLayout, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QSpinBox, QScrollArea, QLineEdit, QPushButton

from pyseus.settings import settings


class MetaWidget(QScrollArea):
    """The widget for metadata."""

    def __init__(self, app):
        QScrollArea.__init__(self)
        self.app = app

        table = QFrame()
        table.setLayout(QFormLayout())
        self.table = table.layout()

        self.setWidgetResizable(True)
        self.setWidget(table)

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.MinimumExpanding)

        self.updateGeometry()

    def minimumSizeHint(self):
        return QSize(int(settings["ui"]["sidebar_size"]), 100)

    def update_meta(self, data):
        for d in data:
            value = QLineEdit(str(d[1]))
            self.table.addRow(d[0], value)

class MetaWindow(QDialog):
    """..."""

    def __init__(self, data):
        QDialog.__init__(self)
        self.setWindowTitle("Metadata")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowModality(Qt.ApplicationModal) 

        self.setLayout(QFormLayout())
        self.table = self.layout()

        for d in data:
            value = QLineEdit(str(d[1]))
            self.table.addRow(d[0], value)
