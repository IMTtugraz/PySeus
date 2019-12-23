"""PySeus is a simple viewer for MRI imaging data.

Version: 1.0
License: MIT License


Methods
-------

**load([arg])** - Start PySeus; see __main__.py for details.

Classes
-------

**PySeus** - Main application class; see core.py for details.

Subpackages
-----------

**UI** - Contains user interface components.
**Formats** - Contains classes modeling different data sources.
**Tools** - Contains classes for evaluating datasets.
"""

from .settings import settings
from .display import DisplayHelper
from .core import PySeus
from .__main__ import load
