"""GUI elements for use in the sidebar of the main window.

Classes
-------

**InfoWidget** - Sidebar widget for basic file information.
**MetaWidget** - Sidebar widget for basic metadata.
**ConsoleWidget** - Sidebar widget for basic text output.
"""

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QFormLayout, QFrame, QLabel, QLineEdit, \
    QScrollArea, QSizePolicy, QTextEdit, QVBoxLayout

from pyseus.settings import settings


class InfoWidget(QFrame):
    """The widget for file info. Displays path, scan ID and slice index."""

    def __init__(self, app):
        QFrame.__init__(self)
        self.app = app

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.path = QLineEdit("")
        self.scan = QLabel("")
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

    def minimumSizeHint(self):  # pylint: disable=C0103,R0201
        """Return widget size to ensure unifrom sidebar width."""
        return QSize(int(settings["ui"]["sidebar_size"]), 80)

    def update_slice(self, current, slices):
        """Update the displayed slice index."""
        self.slice.setText("{} / {}".format(current+1, slices))

    def update_scan(self, scan):
        """Update the displayed scan ID."""
        self.scan.setText("{}".format(scan))

    def update_path(self, path):
        """Update the displayed path."""
        self.path.setText(path)


class MetaWidget(QScrollArea):
    """The widget for metadata display."""

    def __init__(self, app):
        QScrollArea.__init__(self)
        self.app = app
        self._reset_ui()

    def _reset_ui(self):
        """Remove all metadata rows and reset the layout."""
        table = QFrame()
        table.setLayout(QFormLayout())
        self.table = table.layout()

        self.setWidgetResizable(True)
        self.setWidget(table)

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.MinimumExpanding)

        self.updateGeometry()

    def minimumSizeHint(self):  # pylint: disable=C0103,R0201
        """Return widget size to ensure unifrom sidebar width."""
        return QSize(int(settings["ui"]["sidebar_size"]), 100)

    def update_meta(self, data, more=True):
        """Set the displayed metadata; if *more* is True, display a button to
        show all metadata."""

        self._reset_ui()

        if data is not None and data:
            for key in sorted(data.keys()):
                value = QLabel(str(data[key]))
                self.table.addRow(key, value)

        if more:
            more_label = QLabel("more ...")
            more_label.setStyleSheet(" text-decoration: underline")
            more_label.mouseReleaseEvent = self._show_more
            self.table.addRow(more_label, None)
        elif data is None or not data:
            self.table.addRow("No metadata available", None)

    def _show_more(self, event):  # pylint: disable=W0613
        """Display a window showing all available metadata."""
        self.app.show_metadata_window()


class ConsoleWidget(QTextEdit):
    """The widget for generic text output."""

    def __init__(self, app):
        QTextEdit.__init__(self)
        self.app = app

        self.setReadOnly(True)

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.MinimumExpanding)
        self.updateGeometry()

    def minimumSizeHint(self):  # pylint: disable=C0103,R0201
        """Return widget size to ensure unifrom sidebar width."""
        return QSize(int(settings["ui"]["sidebar_size"]), 100)

    def print(self, text):
        """Print a simple text message to the console."""
        self.append(text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
