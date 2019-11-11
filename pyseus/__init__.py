"""PySeus is a simple viewer for MRI imaging data.

Version: 1.0
License: MIT License


Methods
-------

**load([arg])** - Start PySeus and try to load `arg`.

Classes
-------

**PySeus** - The main application class.

Subpackages
-----------

**UI** - Contains user interface components.

**Formats** - Contains classes modeling different data sources.

**Modes** - Contains classes modeling different ways to display data.

**Functions** - Contains classes for evaluating datasets.

"""

from pyseus.settings import settings  # noqa: F401
from pyseus.display import DisplayHelper  # noqa: F401
from pyseus.core import PySeus  # noqa: F401
from pyseus.__main__ import load  # noqa: F401
