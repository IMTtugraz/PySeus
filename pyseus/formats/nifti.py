import nibabel
import numpy
import os

from .base import BaseFormat


class NIfTI(BaseFormat):
    """Support for NIfTI files.
    
    Currently, only NIFTI-2 single files are supported.
    Metadata, pixelspacing, scale and orientation are all supported."""

    def __init__(self):
        BaseFormat.__init__(self)

        self.meta_keymap = {
            "pys:descr": "descrip"
        }

    @classmethod
    def can_handle(cls, path):
        _, ext = os.path.splitext(path)
        return ext.lower() in (".nii")

    def load(self, path):
        self.path = path
        self.file = nibabel.load(path)

        shape = self.file.header.get_data_shape()
        scan_count = 0 if len(shape) <= 3 else shape[3]
        self.scans = list(range(0, scan_count))

        self.scan = 0
        return True

    def get_scan_pixeldata(self, scan):
        data = self.file.get_fdata()
        scan_data = numpy.swapaxes(data[:, :, :, scan], 0, 2)
        return numpy.asarray(scan_data)

    def get_scan_metadata(self, scan):
        metadata = {}
        header = self.file.header.items()
        for key, value in header:
            metadata[key] = value
        return metadata

    def get_pixelspacing(self, axis=None):
        if "pixdim" in self.metadata.keys():
            pixdim = self.metadata["pixdim"]
            if "xyzt_units" in self.metadata.keys():
                # @TODO convert units
                pass
        else:
            pixdim = [1, 1, 1]

        if axis is None:
            return pixdim[0:2]
        else:
            return pixdim[axis]

    def get_scale(self):
        pass

    def get_orientation(self):
        pass
