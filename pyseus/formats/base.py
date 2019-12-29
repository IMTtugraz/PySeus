"""Basics for format classes.

Classes
-------

**BaseFormat** - Defines interface for formats classes.
**LoadError** - Exception for various errors during loading.
"""

import numpy


class BaseFormat():
    """Defines the interface for format classes."""

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
        """Maps common metadata keys to format specific keys."""

        self.pixel_spacing = []
        """The pixel spacing metadata adjusted for rotation."""

    @classmethod
    def can_handle(cls, path):
        """Return True if the format class can handle the file at `path`,
        otherwise return False.

        Custom formats have to override this function."""

    def load(self, path):
        """Attempt to load the file at `path`. Return True on success or
        throw an exception."""

    def load_scan(self, scan):
        """Load pixeldata and metadata from the scan with the ID `scan`.
        Set self.scan to the scan ID on success or throw an exception.
        Uses *get_scan_pixeldata* and *get_scan_metadata*.

        Custom formats have to override either this function or
        *get_scan_pixeldata* and *get_scan_metadata*.
        """

        try:
            self.metadata = self.get_scan_metadata(scan)
            self.pixeldata = self.get_scan_pixeldata(scan)
            self.scan = scan
        except LoadError:
            return False
        else:
            return True

    def get_scan_pixeldata(self, scan):  # pylint: disable=R0201,W0613
        """Collect and return the pixeldata from the scan *scan*.

        Custom formats have to override either this function and
        *get_scan_metadata* or reimplement *load_scan*.
        """

        return []

    def get_scan_metadata(self, scan):  # pylint: disable=R0201,W0613
        """Collect and return the metadata from the scan *scan*.

        Custom formats have to override either this function and
        *get_scan_pixeldata* or reimplement *load_scan*.
        """

        return {}

    def get_scan_thumbnail(self, scan):
        """Return the pixeldata to use for a scan thumbnail."""
        scan_data = self.get_scan_pixeldata(scan)
        return scan_data[len(scan_data) // 2]

    def get_metadata(self, keys=None):
        """Return metadata items specified in `keys`.

        If `keys` is empty, returns standard metadata items.
        """

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

    def get_pixeldata(self, slice_=-1):
        """Return pixeldata of current scan. By default, the entire 3D
        pixeldata is returned. If `slice_` is set, a 2D array of
        `pixeldata[slice_]` is returned."""

        if slice_ == -1:
            return self.pixeldata.copy()

        return self.pixeldata[slice_].copy()

    def get_spacing(self, reset=False):  # pylint: disable=R0201
        """Return the pixel spacing, if available.

        This is used for calculation of the pixel aspect ratio; the value
        has to be stored in *self.pixel_spacing* to be adjusted on rotation."""
        if not self.pixel_spacing or reset:
            self.pixel_spacing = [1, 1, 1]

        return self.pixel_spacing

    def get_scale(self):  # pylint: disable=R0201
        """Return the actual size of a pixel in mm, if available."""
        return 0.0

    def get_units(self):  # pylint: disable=R0201
        """Return units associated with the loaded values, if available."""
        return "1"

    def get_orientation(self):  # pylint: disable=R0201
        """Return the default image orientation, if available."""
        return []

    def rotate(self, axis):
        """Rotate the currently loaded pixeldata in 3D."""
        if axis == -1:  # reset
            self.get_spacing(reset=True)
            self.load_scan(self.scan)

        else:
            if not self.pixel_spacing:
                self.get_spacing()

            if axis == 0 and len(self.pixeldata) > 2:  # x-axis
                self.pixeldata = numpy.asarray(numpy.swapaxes(self.pixeldata,
                                                              0, 2))
                self.pixel_spacing[0], self.pixel_spacing[1] = \
                    self.pixel_spacing[2], self.pixel_spacing[1]

            elif axis == 1 and len(self.pixeldata) > 2:  # y-axis
                self.pixeldata = numpy.asarray(numpy.rot90(self.pixeldata))
                self.pixel_spacing[0], self.pixel_spacing[1] = \
                    self.pixel_spacing[0], self.pixel_spacing[2]

            elif axis == 2:  # z-axis
                self.pixeldata = numpy.asarray([numpy.rot90(slice)
                                                for slice in self.pixeldata])
                self.pixel_spacing[0], self.pixel_spacing[1] = \
                    self.pixel_spacing[1], self.pixel_spacing[0]

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
        """Return the number of scans in the current dataset."""
        return len(self.scans)

    def slice_count(self):
        """Return the number of slices in the current scan."""
        return len(self.pixeldata)
        # @TODO determine slice count for arbitrary scans


class LoadError(Exception):
    """Raised when an error is encountered loading a file or scan."""
