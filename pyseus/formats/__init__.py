"""Formats model different data sources.

All formats extend the *BaseFormat* class, guaranteeing basic
functionality of checking files and data, loading files and data and
extracting frames and metadata.
"""

from .base import BaseFormat, LoadError
from .h5 import H5
from .raw import Raw
from .dicom import DICOM