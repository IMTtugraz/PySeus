"""Contains the main GUI elements for PySeus.

Format specific GUI elements are defined in format modules.

Classes
-------

**MainWindow**
**MetaWindow** - Window for displaying metadata.
**ViewWidget** - Widget handling image display.
**InfoWidget** - Sidebar widget for basic file information.
**MetaWidget** - Sidebar widget for basic metadata.
**ConsoleWidget** - Sidebar widget for basic text output.
**ThumbsWidget** - Widget displaying scan thumbnails in a column.
"""

from .main import MainWindow
from .view import ViewWidget
from .sidebar import InfoWidget, ConsoleWidget, MetaWidget
from .thumbs import ThumbsWidget
from .meta import MetaWindow
