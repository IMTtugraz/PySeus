import pydicom
import numpy
import os
from natsort import natsorted

from .base import BaseFormat, LoadError

from profilehooks import profile

class DICOM(BaseFormat):
    """Support for DICOM files (Coming soon)."""

    def __init__(self):
        BaseFormat.__init__(self)

    EXTENSIONS = (".dcm", ".DCM")

    @classmethod
    def check_file(cls, path):
        _, ext = os.path.splitext(path)
        return ext in cls.EXTENSIONS

    def load_file(self, path):
        slice_level = os.path.abspath(os.path.dirname(path))
        self.scan_level = os.path.abspath(os.path.join(slice_level, os.pardir))

        scans = []
        scan_dirs = next(os.walk(self.scan_level))[1]
        # @see https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
        for d in natsorted(scan_dirs):
            if d != "localizer":
                scans.append(d)
        
        current_scan = scans.index(os.path.basename(slice_level))
        return self.scan_level, scans, current_scan

    def load_scan(self, key):
        slices = []
        scan_dir = os.path.join(self.scan_level, key)
        for f in os.listdir(scan_dir):
            if f.endswith(DICOM.EXTENSIONS): 
                slice = pydicom.read_file(os.path.join(scan_dir,f), defer_size=0)
                slices.append(slice)

        slices = [s for s in slices if hasattr(s, "SliceLocation")]
        slices = sorted(slices, key=lambda s: s.SliceLocation)

        slice_data = []
        for s in slices:
            if "PixelData" in s:
                slice_data.append(numpy.asarray(s.pixel_array))
        
        return slice_data

    def load_scan_thumb(self, key):
        slices = []
        scan_dir = os.path.join(self.scan_level, key)
        for f in os.listdir(scan_dir):
            if f.endswith(DICOM.EXTENSIONS): 
                slice = (f, pydicom.filereader.read_file(
                    os.path.join(scan_dir,f), specific_tags=["SliceLocation"]))
                slices.append(slice)
        
        slices = [s for s in slices if hasattr(s[1], "SliceLocation")]
        slices = sorted(slices, key=lambda s: s[1].SliceLocation)

        thumb_slice = pydicom.read_file(os.path.join(scan_dir,
                                        slices[len(slices) // 2][0]))

        return numpy.asarray(thumb_slice.pixel_array)
