import numpy
import os

from PySide2.QtWidgets import QMessageBox

from .base import BaseFormat, LoadError


class NumPy(BaseFormat):
    """Support for NumPy files.
    
    Currently, only .npy files are supported.
    Metadata, pixelspacing, scale and orientation are NOT supported."""

    def __init__(self):
        BaseFormat.__init__(self)

    @classmethod
    def can_handle(cls, path):
        _, ext = os.path.splitext(path)
        return ext.lower() in (".npy")

    def load(self, path):
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
            self.scans = list(range(0, len(data)-1))

        elif data.ndim == 5:
            message = ("The selected dataset ist 5-dimensional. "
                       "The first two dimensions will be concatenated.")
            QMessageBox.warning(self.window, "Pyseus", message)
            scan_count = data.shape[0]*data.shape[1]

            self.scans = list(range(0, scan_count-1))

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

        elif data.ndim == 3:  # multiple slices
            return numpy.asarray(data)

        elif data.ndim == 4:  # multiple scans
            return numpy.asarray(data[scan])

        elif data.ndim == 5:
            q, r = divmod(scan, data.shape[1])
            return numpy.asarray(data[q][r])

    def get_scan_metadata(self, scan):
        return {}  # metadata not supported

    def get_scan_thumbnail(self, scan):
        scan_data = self.get_scan_pixeldata(scan)
        return scan_data[len(scan_data) // 2]