import nibabel
import numpy
import os

from .base import BaseFormat, LoadError


class NIfTI():
    """Support for NIfTI files."""

    def __init__(self, app):
        BaseFormat.__init__(self)
        self.app = app

    EXTENSIONS = (".nii")

    @classmethod
    def can_handle(cls, path):
        _, ext = os.path.splitext(path)
        return ext in cls.EXTENSIONS

    def load(self, path):
        self.file = nibabel.load(path)
        shape = self.file.header.get_data_shape()
        scan_count = 0 if len(shape) <= 3 else shape[3]
        scans = list(range(0, scan_count))
        current_scan = 0

        return path, scans, current_scan
    
    def load_scan(self, scan):
        data = self.file.get_fdata()
        scan_data = numpy.swapaxes(data[:,:,:,scan], 0, 2)
        return numpy.asarray(scan_data)
    
    def load_scan_thumb(self, scan):
        scan_data = self.load_scan(scan)
        return scan_data[ len(scan_data) // 2 ]
    
    def load_metadata(self, scan):
        metadata = {}
        header = self.file.header.items()
        for key, value in header:
            metadata[key] = value
        return metadata

    def get_metadata(self, keys=None):
        if self.app.metadata is None:
            self.app.metadata = self.load_metadata()
        meta = self.app.metadata

        key_map = {
            "pys:patient": "PatientName",
            "pys:series": "SeriesDescription",
            "pys:sequence": "SequenceName",
            "pys:matrix": "AcquisitionMatrix",
            "pys:tr": "RepetitionTime",
            "pys:te": "EchoTime",
            "pys:alpha": "FlipAngle"
        }

        # keys starting with "_" are ignored unless specificially requested
        if keys is None: keys = [k for k in key_map.keys() if k[0] != "_"]

        if isinstance(keys, str): keys = [keys]

        meta_set = {}
        for key in keys:
            if key in key_map:
                real_key = key_map[key]
                if real_key in meta.keys():
                    meta_set[real_key] = meta[real_key]
            else:
                if key in meta.keys():
                    meta_set[key] = meta[key]

        return meta_set
    
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
