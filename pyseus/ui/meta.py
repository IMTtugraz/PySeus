"""GUI elements for displaying metadata.

Classes
-------

**Meta** - Window for displaying metadata.
"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QSizePolicy, QVBoxLayout

from .sidebar import MetaWidget


class MetaWindow(QDialog):
    """Window for displaying metadata."""

    def __init__(self, app, data):
        QDialog.__init__(self)
        self.setWindowTitle("Metadata")
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)

        self.setLayout(QVBoxLayout())
        widget = MetaWidget(app)
        widget.update_meta(data, False)
        widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,
                             QSizePolicy.Policy.MinimumExpanding)
        self.layout().addWidget(widget)

        # Window dimensions
        geometry = app.qt_app.desktop().availableGeometry(self)
        self.resize(geometry.width() * 0.3, geometry.height() * 0.8)
