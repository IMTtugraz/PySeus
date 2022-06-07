"""Support for raw data arrays.

Classes
-------

**Raw** - Class modeling raw data arrays as datasets.
"""

import numpy

from PySide2.QtWidgets import QMessageBox

from .base import BaseFormat, LoadError


class Raw(BaseFormat):
    """Class modeling raw data arrays as datasets.

    Supports python lists, tuples and numpy arrays.
    Metadata, pixelspacing, scale, units and orientation are *not* supported.
    """

    def __init__(self):
        BaseFormat.__init__(self)

        self.data = None
        """Current data array."""

    @classmethod
    def can_handle(cls, path):
        return False

    def load(self, data, data_type=None):
        self.data = numpy.asarray(data)
        valid = isinstance(self.data, numpy.ndarray) and \
            numpy.issubdtype(self.data.dtype, numpy.number)
        if not valid:
            raise LoadError("Invalid data.")

        self.path = "<data>"

        if 2 <= self.data.ndim <= 3:
            self.scans = [0]

        if self.data.ndim == 4:
            self.scans = list(range(0, len(self.data) - 1))

        if self.data.ndim == 5:
            message = ("The selected dataset ist 5-dimensional. "
                       "The first two dimensions will be concatenated.")
            QMessageBox.warning(None, "Pyseus", message)
            scan_count = self.data.shape[0] * self.data.shape[1]

            self.scans = list(range(0, scan_count - 1))

        self.scan = 0
        return True

    def get_scan_pixeldata(self, scan):
        if self.data.ndim == 2:  # single slice
            return numpy.asarray([self.data])

        if self.data.ndim == 3:  # multiple slices
            return numpy.asarray(self.data)

        if self.data.ndim == 4:  # multiple scans
            return numpy.asarray(self.data[scan])

        if self.data.ndim == 5:
            dim_4, dim_5 = divmod(scan, self.data.shape[1])
            return numpy.asarray(self.data[dim_4][dim_5])

        return []  # can´t interpret data with dimensions <= 1 or > 5

    def get_scan_metadata(self, scan):
        return {}  # metadata not supported

    def get_scan_thumbnail(self, scan):
        scan_data = self.get_scan_pixeldata(scan)
        return scan_data[len(scan_data) // 2]
