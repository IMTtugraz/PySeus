import numpy

from PySide2.QtWidgets import QMessageBox

from .base import BaseFormat, LoadError


class Raw(BaseFormat):
    """Support for (NumPy) array data.
    
    Metadata, pixelspacing, scale and orientation are NOT supported."""

    def __init__(self):
        BaseFormat.__init__(self)

    @classmethod
    def can_handle(cls, path):
        return False

    def load(self, data):
        self.data = numpy.asarray(data)
        if not isinstance(self.data, numpy.ndarray):
            raise LoadError("Invalid data.")

        self.path = "<data>"

        if 2 <= self.data.ndim <= 3:
            self.scans = [0]

        elif self.data.ndim == 4:
            self.scans = list(range(0, len(self.data)-1))

        elif self.data.ndim == 5:
            message = ("The selected dataset ist 5-dimensional. "
                       "The first two dimensions will be concatenated.")
            QMessageBox.warning(self.window, "Pyseus", message)
            scan_count = self.data.shape[0]*self.data.shape[1]

            self.scans = list(range(0, scan_count-1))

        self.scan = 0
        return True

    def get_scan_pixeldata(self, scan):
        if self.data.ndim == 2:  # single slice
            return numpy.asarray([self.data])

        elif self.data.ndim == 3:  # multiple slices
            return numpy.asarray(self.data)

        elif self.data.ndim == 4:  # multiple scans
            return numpy.asarray(self.data[scan])

        elif self.data.ndim == 5:
            q, r = divmod(scan, self.data.shape[1])
            return numpy.asarray(self.data[q][r])

    def get_scan_metadata(self, scan):
        return {}  # metadata not supported

    def get_scan_thumbnail(self, scan):
        if self.data.ndim == 2:  # single slice
            return numpy.asarray(self.data)

        elif self.data.ndim == 3:  # multiple slices
            return numpy.asarray(self.data[len(self.data) // 2])

        elif self.data.ndim == 4:  # multiple scans
            return numpy.asarray(self.data[scan][len(self.data) // 2])

        elif self.data.ndim == 5:
            q, r = divmod(scan, self.data.shape[1])
            return numpy.asarray(self.data[q][r][len(self.data) // 2])
