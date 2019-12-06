import nibabel
import numpy
import os

from .base import BaseFormat, LoadError


class NIfTI(BaseFormat):
    """Support for NIfTI files."""

    def __init__(self):
        BaseFormat.__init__(self)

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

    def _get_pixeldata(self, scan):
        data = self.file.get_fdata()
        scan_data = numpy.swapaxes(data[:,:,:,scan], 0, 2)
        return numpy.asarray(scan_data)
    
    def get_thumbnail(self, scan):
        scan_data = self._get_pixeldata(scan)
        return scan_data[ len(scan_data) // 2 ]
    
    def _get_metadata(self, scan):
        metadata = {}
        header = self.file.header.items()
        for key, value in header:
            metadata[key] = value
        return metadata

    def get_metadata(self, keys=None):
        key_map = {
            "pys:patient": "PatientName",
            "pys:series": "SeriesDescription",
            "pys:sequence": "SequenceName",
            "pys:matrix": "AcquisitionMatrix",
            "pys:tr": "RepetitionTime",
            "pys:te": "EchoTime",
            "pys:alpha": "FlipAngle"
        }

        return super().get_metadata(keys, key_map)
    
    def get_pixel_spacing(axis=None):
        meta = self.app.metadata
        
        if "pixdim" in meta.keys():
            pixdim = meta["pixdim"]
            if "xyzt_units" in meta.keys():
                # @TODO convert units
                pass
        else:
            pixdim = [1,1,1]

        if axis is None: return pixdim[0:2]
        else: return pixdim[axis]
