class BaseFormat():
    """Defines the basic functionality for file / data formats."""

    def __init__(self):
        self.path = ""
        """..."""

        self.scans = []
        """..."""

        self.scan = None
        """..."""

        self.metadata = {}
        """..."""

        self.pixeldata = None
        """..."""

    @classmethod
    def can_handle(cls, path):
        """Determines if the format class can handle the file at `path`."""
        pass

    def load_file(self, path):
        """Attempt to load the file at `path`."""
        pass
    
    def load_scan(self, scan):
        """..."""
        self.pixeldata = self._get_pixeldata(scan)
        self.metadata = self._get_metadata(scan)
        self.scan = scan

    def rotate(self, axis):
        if axis == -1:  # reset
            self.load_scan(self.scan)

        else:
            if axis == 0 and len(self.pixeldata) > 2:  # x-axis
                self.pixeldata = numpy.asarray(numpy.swapaxes(self.pixeldata, 0, 2))
                self._set_current_slice(len(self.pixeldata) // 2)
                
            elif axis == 1 and len(self.pixeldata) > 2:  # y-axis
                self.pixeldata = numpy.asarray(numpy.rot90(self.pixeldata))
                self._set_current_slice(len(self.pixeldata) // 2)

            elif axis == 2:  # z-axis
                self.pixeldata = numpy.asarray([numpy.rot90(slice) for slice in self.pixeldata])

    def metadata(self, keys=None):
        """Returns specific metadata items; returns standard list of most important metadata"""
        pass

    def pixeldata(self, slice=-1):
        """Returns pixeldata of current scan; should always be used if data is to be processed further"""

# @TODO redo interface here



class LoadError(Exception):
    """Raised when an error is encountered loading a file or scan."""
    pass
