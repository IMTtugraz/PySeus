"""Settings container for PySeus. Uses *settings.ini*."""

import os
from configparser import ConfigParser

settings = ConfigParser()  # pylint: disable=C0103
settings.read(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "./settings.ini")))
