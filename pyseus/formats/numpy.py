"""Support for NumPy files.

Classes
-------

**NumPy** - Class modeling NumPy datasets.
"""

import os
import numpy

from PySide2.QtWidgets import QMessageBox

from .base import BaseFormat, LoadError


class NumPy(BaseFormat):
    """Class modeling NumPy datasets.

    Supports arrays or pickeled objects in *.npy*-files.
    Metadata, pixelspacing, scale, units and orientation are *not* supported.
    """

    EXTENSIONS = (".npy")

    def __init__(self):
        BaseFormat.__init__(self)

    @classmethod
    def can_handle(cls, path):
        _, ext = os.path.splitext(path)
        return ext.lower() in NumPy.EXTENSIONS

    def load(self, path, data_type=None):
        try:
            data = numpy.load(path, None, False)
        except Exception:
            raise LoadError("Couldn´t load file.")

        data = numpy.asarray(data)
        if not isinstance(data, numpy.ndarray):
            raise LoadError("Invalid data.")

        self.path = os.path.abspath(path)

        if 2 <= data.ndim <= 3:
            self.scans = [0]

        elif data.ndim == 4:
            self.scans = list(range(0, len(data) - 1))

        elif data.ndim == 5:
            message = ("The selected dataset ist 5-dimensional. "
                       "The first two dimensions will be concatenated.")
            QMessageBox.warning(None, "Pyseus", message)
            scan_count = data.shape[0] * data.shape[1]

            self.scans = list(range(0, scan_count - 1))

        self.scan = 0
        return True

    def get_scan_pixeldata(self, scan):
        try:
            data = numpy.load(self.path, None, False)
        except Exception:
            raise LoadError("Couldn´t load file.")

        data = numpy.asarray(data)
        if not isinstance(data, numpy.ndarray):
            raise LoadError("Invalid data.")

        if data.ndim == 2:  # single slice
            return numpy.asarray([data])

        if data.ndim == 3:  # multiple slices
            return numpy.asarray(data)

        if data.ndim == 4:  # multiple scans
            return numpy.asarray(data[scan])

        if data.ndim == 5:
            dim_4, dim_5 = divmod(scan, data.shape[1])
            return numpy.asarray(data[dim_4][dim_5])

        return []  # can´t interpret data with dimensions <= 1 or > 5

    def get_scan_metadata(self, scan):
        return {}  # metadata not supported

    def get_scan_thumbnail(self, scan):
        scan_data = self.get_scan_pixeldata(scan)
        return scan_data[len(scan_data) // 2]
