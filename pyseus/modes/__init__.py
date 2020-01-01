"""Modes model different ways of visualization.

All modes extend the *BaseMode* class, guaranteeing basic functionality
of preparing data, converting data to pixmaps and handling viewport events.
"""

from .base import BaseMode
from .grayscale import Grayscale
