import nibabel
import numpy
import os

from .base import BaseFormat, LoadError


class NIfTI():
    """Defines the basic functionality for file / data formats."""

    def __init__(self):
        pass

    @classmethod
    def check_file(cls, path):
        """See if the format can handle the file at `path`."""
        pass

    def load_file(self, path):
        """Attempt to load the file at `path`."""
        pass
    
    def load_scan(self, scan):
        """Attempt to load the scan `scan`."""
        pass
    
    def load_scan_thumb(self, scan):
        """Attempt to load the thumbnail for scan `scan`."""
        pass
    
    def load_metadata(self, scan, keys=None):
        """..."""
        pass