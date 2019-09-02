import pydicom
import numpy
import os

from .base import BaseFormat


class DICOM(BaseFormat):
    """Support for DICOM files (Coming soon)."""

    def __init__(self):
        BaseFormat.__init__(self)

    @classmethod
    def check_file(cls, path):
        _, ext = os.path.splitext(path)
        return ext in [".dcm", ".DCM"]

    def load_file(self, path):
        path = os.path.dirname(path)

        slices = []

        for f in os.listdir(path):
            if f.endswith(".dcm") or f.endswith(".DCM"): 
                slice = pydicom.dcmread(os.path.join(path,f))
                slices.append(slice)
        
        slices = [s for s in slices if hasattr(s, "SliceLocation")]
        slices = sorted(slices, key=lambda s: s.SliceLocation)

        slice_data = []
        for s in slices:
            if "PixelData" in s:
                slice_data.append(numpy.asarray(s.pixel_array))
        
        return "", [], slice_data
