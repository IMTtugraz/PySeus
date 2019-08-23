"""PySeus is a minimal viewer for medical imaging data.

Version: 0.1 (Alpha)
License: GNU General Public License


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

from pyseus.settings import settings
from pyseus.display import DisplayHelper
from pyseus.core import PySeus
from pyseus.__main__ import load
