import pydicom
import numpy
import os
from natsort import natsorted
from PySide2.QtWidgets import QMessageBox

from .base import BaseFormat, LoadError

class DICOM(BaseFormat):
    """Support for DICOM files."""

    def __init__(self):
        BaseFormat.__init__(self)

    @classmethod
    def can_handle(cls, path):
        _, ext = os.path.splitext(path)
        return ext.lower() in (".dcm")

    def load(self, path):
        self.path = os.path.abspath(path)

        slice_level = os.path.abspath(os.path.dirname(path))
        self.scan_level = os.path.abspath(os.path.join(slice_level, os.pardir))

        scan_dirs = next(os.walk(self.scan_level))[1]
        # @see https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
        for d in natsorted(scan_dirs):
            has_dcm = False
            for f in os.listdir(os.path.abspath(os.path.join(self.scan_level, d))):
                _, ext = os.path.splitext(f)
                if ext.lower() in (".dcm"):
                    has_dcm = True
                    break

            if has_dcm and d != "localizer":
                self.scans.append(d)

        self.scan = self.scans.index(os.path.basename(slice_level))

        if len(self.scans) > 1:
            load_all = QMessageBox.question(None, "Pyseus", 
                "{} scans detected. Do you want to load all scans?".format(len(self.scans)))

            if load_all is QMessageBox.StandardButton.No:
                self.scans = [self.scans[current_scan]]
                self.scan = 0        

        return True

    def load_scan(self, key=None):
        if key == None: key = self.scan
        else: self.scan = key

        slices = []
        scan_dir = os.path.join(self.scan_level, self.scans[key])
        for f in os.listdir(scan_dir):
            _, ext = os.path.splitext(f)
            if ext.lower() in (".dcm"):
                slice = pydicom.read_file(os.path.join(scan_dir,f), defer_size=0)
                slices.append(slice)

        slice_count = len(slices)
        slices = [s for s in slices if hasattr(s, "SliceLocation")]

        self._load_file_metadata(slices[0])
        
        if slice_count > 0 and len(slices) == 0:
            raise LoadError("DICOM files are missing SliceLocation data.")

        slices = sorted(slices, key=lambda s: s.SliceLocation)

        slice_data = []
        for s in slices:
            if "PixelData" in s:
                slice_data.append(s.pixel_array)
        
        self.pixeldata = numpy.asarray(slice_data)

    def get_thumbnail(self, key):
        slices = []
        scan_dir = os.path.join(self.scan_level, key)
        for f in os.listdir(scan_dir):
            _, ext = os.path.splitext(f)
            if ext.lower() in (".dcm"):
                slice = (f, pydicom.filereader.read_file(
                    os.path.join(scan_dir,f), specific_tags=["SliceLocation"]))
                slices.append(slice)
        
        slices = [s for s in slices if hasattr(s[1], "SliceLocation")]
        slices = sorted(slices, key=lambda s: s[1].SliceLocation)

        thumb_slice = pydicom.read_file(os.path.join(scan_dir,
                                        slices[len(slices) // 2][0]))

        return numpy.asarray(thumb_slice.pixel_array)

    def load_metadata(self, scan):
        slice = None
        scan_dir = os.path.join(self.scan_level, scan)
        for f in os.listdir(scan_dir):
            _, ext = os.path.splitext(f)
            if ext.lower() in (".dcm"):
                slice = pydicom.read_file(os.path.join(scan_dir,f), defer_size=0)
                self._load_file_metadata(slice)
    
    def _load_file_metadata(self, slice):
        metadata = {}

        ignore = ["PixelData"]
        for e in slice:
            if not e.keyword in ignore and not e.keyword == "":
                metadata[e.keyword] = e.value
        
        self.metadata = metadata

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
    
    def get_spacing(self, axis=None):
        if self.app.metadata is None:
            self.app.metadata = self.load_metadata()
        meta = self.app.metadata

        pixel_spacing = [1,1,1]
        if "PixelSpacing" in meta.keys():
            pixel_spacing = meta["PixelSpacing"]
        
        return pixel_spacing
    
    def get_scale(self):
        pass

    def get_orientation(self):
        pass
