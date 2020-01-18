"""GUI elements for displaying metadata.

Classes
-------

**Meta** - Window for displaying metadata.
"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QSizePolicy, QVBoxLayout
from PySide2.QtGui import QIcon

from .sidebar import MetaWidget


class MetaWindow(QDialog):  # pylint: disable=R0903
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

        icon = QIcon(os.path.abspath(os.path.join(
            os.path.dirname(__file__), "./icon.png")))
        self.setWindowIcon(icon)

        # Window dimensions
        geometry = app.qt_app.desktop().availableGeometry(self)
        self.resize(geometry.width() * 0.3, geometry.height() * 0.8)
