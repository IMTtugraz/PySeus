"""Formats model different data sources.

All formats extend the *BaseFormat* class, guaranteeing basic
functionality of checking files and data, loading files and data and
extracting frames and metadata.
"""

from .base import BaseFormat, LoadError  # noqa: F401
from .h5 import H5  # noqa: F401
from .raw import Raw  # noqa: F401
from .dicom import DICOM  # noqa: F401
from .nifti import NIfTI  # noqa: F401