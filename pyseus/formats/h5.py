import h5py
import numpy

from .base import BaseFormat

class H5(BaseFormat):
    """Support for HDF5 files."""

    def __init__(self):
        BaseFormat.__init__(self)
        self.type = "H5"

    def load_file(self, file):
        # @TODO check file access
        self.path = file
        self.file = h5py.File(file, "r")
    
    def load_frame(self, frame):
        data = numpy.asarray(self.file['images'][frame])
        return data
