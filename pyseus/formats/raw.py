import numpy

from .base import BaseFormat


class Raw(BaseFormat):
    """Support for NumPy array data and files."""

    def __init__(self):
        BaseFormat.__init__(self)

    @classmethod
    def can_handle(cls, path):    
        return False

    def load(self, data):
        try:
            self.data = numpy.asarray(data)
        except e:
            raise LoadError("Invalid data.")

        self.path = "<data>"

        if 2 <= self.data.ndim <= 3:
            self.scans = [0]

        elif self.data.ndim == 4:
            self.scans = list(range(0, len(f[self.ds_path])-1))

        elif self.data.ndim == 5:
            QMessageBox.warning(self.window, "Pyseus", 
                "The selected dataset ist 5-dimensional. The first two dimensions will be concatenated.")
            scan_count = f[self.ds_path].shape[0]*f[self.ds_path].shape[1]
            
            self.scans = list(range(0, scan_count-1))
        
        self.scan = 0
        return True

    def load_scan(self, scan):
        if self.data.ndim == 2:  # single slice
            self.pixeldata = numpy.asarray([self.data])

        elif self.data.ndim == 3:  # multiple slices
            self.pixeldata = numpy.asarray(self.data)

        elif self.data.ndim == 4:  # multiple scans
            self.pixeldata = numpy.asarray(self.data[scan])

        elif self.data.ndim == 5:
            q, r = divmod(scan, self.data.shape[1])
            self.pixeldata = numpy.asarray(self.data[q][r])
