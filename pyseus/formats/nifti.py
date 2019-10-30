import nibabel
import numpy
import os

from .base import BaseFormat, LoadError


class NIfTI():
    """Defines the basic functionality for file / data formats."""

    def __init__(self, app):
        BaseFormat.__init__(self)
        self.app = app

    EXTENSIONS = (".nii")

    @classmethod
    def check_file(cls, path):
        """See if the format can handle the file at `path`."""
        _, ext = os.path.splitext(path)
        return ext in cls.EXTENSIONS

    def load_file(self, path):
        """Attempt to load the file at `path`."""
        self.file = nibabel.load(path)
        shape = self.file.header.get_data_shape()
        scan_count = 0 if len(shape) <= 3 else shape[3]
        scans = list(range(0, scan_count))
        current_scan = 0

        return path, scans, current_scan
    
    def load_scan(self, scan):
        """Attempt to load the scan `scan`."""
        data = self.file.get_fdata()
        scan_data = numpy.swapaxes(data[:,:,:,scan], 0, 2)
        return numpy.asarray(scan_data)
    
    def load_scan_thumb(self, scan):
        """Attempt to load the thumbnail for scan `scan`."""
        scan_data = self.load_scan(scan)
        return scan_data[ len(scan_data) // 2 ]
    
    def load_metadata(self, scan, keys=None):
        """..."""
        meta = []
        header = self.file.header.items()
        for key, value in header:
            meta.append((key, value))
        return meta
