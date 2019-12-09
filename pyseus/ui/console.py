from PySide2.QtCore import QSize
from PySide2.QtWidgets import QTextEdit, QSizePolicy

from pyseus.settings import settings


class ConsoleWidget(QTextEdit):
    """The widget for generic text output."""

    def __init__(self, app):
        QTextEdit.__init__(self)
        self.app = app

        self.setReadOnly(True)

        self.setSizePolicy(QSizePolicy.Policy.Fixed,
                           QSizePolicy.Policy.MinimumExpanding)
        self.updateGeometry()

    def minimumSizeHint(self):
        """Return widget size to ensure unifrom sidebar width."""
        return QSize(int(settings["ui"]["sidebar_size"]), 100)

    def print(self, text):
        """Print a simple text message to the console."""
        self.append(text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
