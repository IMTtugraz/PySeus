import h5py
import numpy

from .base import Format

class H5(Format):

    def __init__(self):
        Format.__init__(self)
        self.type = "H5"

    def load_file(self, file):
        # @TODO check file access
        self.path = file
        self.file = h5py.File(file, "r")
    
    def load_frame(self, frame):
        data = numpy.asarray(self.file['images'][0])
        return data
