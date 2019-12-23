import numpy


class BaseFormat():
    """Defines the basic functionality for file / data formats."""

    def __init__(self):
        self.path = ""
        """The path to the currently loaded."""

        self.scans = []
        """List of loaded scan IDs."""

        self.scan = None
        """The ID of the currently loaded scan."""

        self.metadata = {}
        """Dictionary list of the metadata of the current scan."""

        self.pixeldata = []
        """3D array of the pixeldata of the current scan."""

        self.meta_keymap = {}
        """Maps common metadata keys to format specific keys.
        ```
        "meta1": "format_specific_meta1",
        "meta2": ["format_specific_meta2a", "format_specific_meta2b"]
        ```"""

    @classmethod
    def can_handle(cls, path):
        """Check if the format class can handle the file at `path`."""
        pass

    def load(self, path):
        """Attempt to load the file at `path`.
        Return True on success or throw an exception."""
        pass

    def load_scan(self, scan):
        """Load the scan with the ID `scan`, and set self.scan to the scan ID
        on success or throw an exception.
        By default, uses *get_scan_pixeldata* and *get_scan_metadata*."""
        try:
            self.metadata = self.get_scan_metadata(scan)
            self.pixeldata = self.get_scan_pixeldata(scan)
            self.scan = scan
        except LoadError:
            return False
        else:
            return True

    def get_scan_pixeldata(self, scan):
        pass

    def get_scan_metadata(self, scan):
        pass

    def get_scan_thumbnail(self, scan):
        """Return the pixeldata to use for a scan thumbnail."""
        scan_data = self.get_scan_pixeldata(scan)
        return scan_data[len(scan_data) // 2]

    def get_metadata(self, keys=None):
        """Return metadata items specified in `keys`.
        If `keys` is empty, returns standard metadata items."""

        if self.meta_keymap is None:
            return {}  # format does not support metadata
        if keys is None:
            return self.metadata  # return all metadata
        if keys == "DEFAULT":
            keys = self.meta_keymap.keys()  # return standard meta set
        if isinstance(keys, str):
            keys = [keys]

        meta_set = {}
        for key in keys:
            if key in self.meta_keymap:
                if isinstance(self.meta_keymap[key], str):
                    key_list = [self.meta_keymap[key]]
                elif isinstance(self.meta_keymap[key], list):
                    key_list = self.meta_keymap[key]

                for k in key_list:
                    if k in self.metadata.keys():
                        meta_set[k] = self.metadata[k]

            elif key in self.metadata.keys():
                meta_set[key] = self.metadata[key]

        return meta_set

    def get_pixeldata(self, slice=-1):
        """Return pixeldata of current scan. By default, the entire 3D
        pixeldata is returned. If `slice` is set, a 2D array of
        `pixeldata[slice]` is returned."""

        if slice == -1:
            return self.pixeldata.copy()
        else:
            return self.pixeldata[slice].copy()

    def get_spacing(self, axis=None):
        """Return the pixel aspect ratio, if available.
        Otherweise, return 1:1:1."""
        return [1, 1, 1]

    def get_scale(self):
        """Return the actual size of a pixel, if available.
        Otherwise, return 0."""
        return 0.0

    def get_units(self):
        return ""

    def get_orientation(self):
        """Return the default image orientation, if available."""
        return []

    def rotate(self, axis):
        """Rotate the currently loaded pixeldata in 3D."""
        if axis == -1:  # reset
            self.load_scan(self.scan)

        else:
            if axis == 0 and len(self.pixeldata) > 2:  # x-axis
                self.pixeldata = numpy.asarray(numpy.swapaxes(self.pixeldata,
                                                              0, 2))

            elif axis == 1 and len(self.pixeldata) > 2:  # y-axis
                self.pixeldata = numpy.asarray(numpy.rot90(self.pixeldata))

            elif axis == 2:  # z-axis
                self.pixeldata = numpy.asarray([numpy.rot90(slice)
                                               for slice in self.pixeldata])

    def flip(self, direction):
        """Flip the currently loaded pixeldata."""
        if direction == -1:  # reset
            self.load_scan(self.scan)

        else:
            if direction == 0:  # horizontal
                self.pixeldata = numpy.asarray([numpy.flipud(slice)
                                               for slice in self.pixeldata])

            elif direction == 1:  # vertical
                self.pixeldata = numpy.asarray([numpy.fliplr(slice)
                                               for slice in self.pixeldata])

            elif direction == 2:  # back-front
                self.pixeldata = numpy.asarray(numpy.flipud(self.pixeldata))

    def scan_count(self):
        return len(self.scans)

    def slice_count(self, scan=None):
        if scan is None:
            return len(self.pixeldata)
        else:
            pass
            # @TODO determine slice count for arbitrary scans


class LoadError(Exception):
    """Raised when an error is encountered loading a file or scan."""
    pass
