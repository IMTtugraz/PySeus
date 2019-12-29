"""Support for NIfTI files.

Classes
-------

**NIfTI** - Class modeling NIfTI datasets.
"""

import os

import nibabel
import numpy

from .base import BaseFormat, LoadError


class NIfTI(BaseFormat):
    """Class modeling NIfTI datasets.

    Supports single file *.nii*-files according to the NIfTI-2 standard.
    Supports metadata, pixelspacing, scale, units and orientation.
    """

    EXTENSIONS = (".nii")

    def __init__(self):
        BaseFormat.__init__(self)

        self.meta_keymap = {
            "pys:descr": "descrip"
        }

        self.file = None
        """Instance of the NIfTI file handler."""

    @classmethod
    def can_handle(cls, path):
        _, ext = os.path.splitext(path)
        return ext.lower() in NIfTI.EXTENSIONS

    def load(self, path):
        if not os.path.isfile(path):
            raise LoadError("File not found.")

        self.path = path
        self.file = nibabel.load(path)

        shape = self.file.header.get_data_shape()
        scan_count = 0 if len(shape) <= 3 else shape[3]
        self.scans = list(range(0, scan_count))

        self.scan = 0
        return True

    def get_scan_pixeldata(self, scan):
        canonical = nibabel.as_closest_canonical(self.file)
        data = canonical.get_fdata()
        scan_data = numpy.swapaxes(data[:, :, :, scan], 0, 2)
        return numpy.asarray(scan_data)

    def get_scan_metadata(self, scan):
        metadata = {}
        header = self.file.header.items()
        for key, value in header:
            metadata[key] = value
        return metadata

    def get_spacing(self, reset=False):
        if not self.pixel_spacing or reset:
            if "pixdim" in self.metadata.keys():
                self.pixel_spacing = list(self.metadata["pixdim"])[1:4]
            else:
                self.pixel_spacing = [1, 1, 1]

        return self.pixel_spacing

    def get_scale(self):
        if "xyzt_units" in self.metadata.keys():
            pixdim = min(self.get_spacing())  # units per pixel
            if self.metadata["xyzt_units"] & 1:
                return 1000.0 * pixdim
            if self.metadata["xyzt_units"] & 2:
                return 1.0 * pixdim
            if self.metadata["xyzt_units"] & 3:
                return 0.001 * pixdim

        return 0.0

    def get_units(self):
        return "1"

    def get_orientation(self):
        # uses only sform (affine transform) but ignores qform
        if "sform_code" in self.metadata.keys() \
                and self.metadata["sform_code"] > 0:
            orientation = list(nibabel.aff2axcodes(self.file.affine))
            # @TODO convert to internal form
            return orientation

        return []
