import numpy

from .base import BaseFormat


class Raw(BaseFormat):
    """Support for NumPy array data and files."""

    def __init__(self):
        BaseFormat.__init__(self)

    @classmethod
    def check_file(cls, path):
        try:
            numpy.load(path, None, False)
            return True
        
        except:        
            return False

    def load_file(self, file):
        data = numpy.load(file, None, False)
        return self.load_data(data)

    def load_data(self, data):
        try:
            self.data = numpy.asarray(data)
        except e:
            raise LoadError("Invalid data.")

        path = "<data>"

        if 2 <= self.data.ndim <= 3:
            return path, [0], 0
        elif self.data.ndim == 4:
            return path, list(range(0, len(f[self.ds_path])-1)), 0
        elif self.data.ndim == 5:
            QMessageBox.warning(self.window, "Pyseus", 
                "The selected dataset ist 5-dimensional. The first two dimensions will be concatenated.")
            scan_count = f[self.ds_path].shape[0]*f[self.ds_path].shape[1]
            return path, list(range(0, scan_count-1)), 0

    def load_scan(self, scan):
        if self.data.ndim == 2:  # single slice
            return numpy.asarray([self.data])
        if self.data.ndim == 3:  # multiple slices
            return numpy.asarray(self.data)
        elif self.data.ndim == 4:  # multiple scans
            return numpy.asarray(self.data[scan])
        elif self.data.ndim == 5:
            q, r = divmod(scan, self.data.shape[1])
            return numpy.asarray(self.data[q][r])
