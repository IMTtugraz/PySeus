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

from os import path
from sys import stdin, argv

import numpy as np
from PySide2.QtGui import QImage

from .core import PySeus
from .ui import MainWindow

def load(arg = None):
    """Start Pyseus and load `arg`.
    `arg` can be a file path or data array."""
    app = PySeus()
    
    if isinstance(arg, str) and path.isfile(arg):
        app.load_file(arg)
    
    # @TODO remove after testing
    elif isinstance(arg, QImage):
        app.load_image(arg)

    elif arg is not None:
        app.load_data(arg)

    return app.exec_()

def _console_entry():
    """Start Pyseus from Console.
    Loads path from arguments or data from stdin, if available.
    """

    if len(argv) > 1:
        load(argv[1])

    elif not stdin.isatty():
        # @TODO try loading data from stdin
        # data = stdin.read()
        # load(np.loadtxt(data))
        pass

    else:
        load()
