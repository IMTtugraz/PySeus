import pydicom
import numpy
import os
from natsort import natsorted

from .base import BaseFormat, LoadError

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
            has_dcm = False
            for f in os.listdir(os.path.abspath(os.path.join(self.scan_level, d))):
                if f.endswith(DICOM.EXTENSIONS):
                    has_dcm = True
                    break

            if has_dcm and d != "localizer":
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

        slice_count = len(slices)
        slices = [s for s in slices if hasattr(s, "SliceLocation")]
        
        if slice_count > 0 and len(slices) == 0:
            raise LoadError("DICOM files are missing SliceLocation data.")

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

    def load_metadata(self, scan, keys=None):
        slices = []
        slice = None
        scan_dir = os.path.join(self.scan_level, scan)
        for f in os.listdir(scan_dir):
            if f.endswith(DICOM.EXTENSIONS): 
                slice = pydicom.read_file(os.path.join(scan_dir,f), defer_size=0)
                break

        if slice == None:
            raise LoadError("Couldn´t load metadata.")

        metadata = []
        # for k in keys:
        #     if hasattr(slice, k):
        #         metadata.append (k, slice.data_element(k).value)

        for e in slice:
            metadata.append((e.description(), e.value))
        
        return metadata
