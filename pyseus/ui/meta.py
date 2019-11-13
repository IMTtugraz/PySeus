from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QDialog, QSizePolicy, QFormLayout, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QSpinBox, QScrollArea, QLineEdit, QPushButton

from pyseus.settings import settings


class MetaWidget(QScrollArea):
    """The widget for metadata."""

    def __init__(self, app):
        QScrollArea.__init__(self)
        self.app = app
        self._reset_ui()

    def _reset_ui(self):
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

    def update_meta(self, data, more=True):
        self._reset_ui()
        
        if not data is None and len(data) > 0:
            for k in sorted(data.keys()):
                value = QLineEdit(str(data[k]))
                self.table.addRow(k, value)

        if more:
            moreLabel = QLabel("more ...")
            moreLabel.mouseReleaseEvent = self._show_more
            self.table.addRow(moreLabel, None)
        elif data is None or len(data) == 0:
            self.table.addRow("No metadata available", None)

    def _show_more(self, event):
        self.app.show_metadata_window()


class MetaWindow(QDialog):
    """..."""

    def __init__(self, app, data):
        QDialog.__init__(self)
        self.setWindowTitle("Metadata")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.setLayout(QVBoxLayout())
        widget = MetaWidget(app)
        widget.update_meta(data, False)
        widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,
                             QSizePolicy.Policy.MinimumExpanding)
        self.layout().addWidget(widget)

        # Window dimensions
        geometry = app.desktop().availableGeometry(self)
        self.resize(geometry.width() * 0.3, geometry.height() * 0.8)
