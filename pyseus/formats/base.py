import numpy

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

    def load(self, path):
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
                
            elif axis == 1 and len(self.pixeldata) > 2:  # y-axis
                self.pixeldata = numpy.asarray(numpy.rot90(self.pixeldata))

            elif axis == 2:  # z-axis
                self.pixeldata = numpy.asarray([numpy.rot90(slice) for slice in self.pixeldata])

    def get_metadata(self, keys=None, key_map=None):
        """Returns specific metadata items; returns standard list of most important metadata."""
        if self.metadata is None:
            self.load_metadata()

        if key_map == None: return {}  # format does not support metadata
        if keys is None: keys = key_map.keys()  # return standard meta set
        if isinstance(keys, str): keys = [keys]

        meta_set = {}
        for key in keys:
            if key in key_map:
                if isinstance(key_map[key], str):
                    key_list = [key_map[key]]
                elif isinstance(key_map[key], list):
                    key_list = key_map[key]

                for k in key_list:
                    if k in self.metadata.keys():
                        meta_set[k] = self.metadata[k]

            elif key in self.metadata.keys():
                meta_set[key] = self.metadata[key]

        return meta_set

    def get_pixeldata(self, slice=-1):
        """Returns pixeldata of current scan; should always be used if data is to be processed further."""
        if slice == -1:
            return self.pixeldata
        else:
            return self.pixeldata[slice]



class LoadError(Exception):
    """Raised when an error is encountered loading a file or scan."""
    pass
