import pydicom
import numpy
import os
from natsort import natsorted
from PySide2.QtWidgets import QMessageBox

from .base import BaseFormat, LoadError

class DICOM(BaseFormat):
    """Support for DICOM files."""

    def __init__(self, app):
        BaseFormat.__init__(self)
        self.app = app

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

        if len(scans) > 1:
            load_all = QMessageBox.question(self.app.window, "Pyseus", 
                "{} scans detected. Do you want to load all scans?".format(len(scans)))
            
            if load_all is QMessageBox.StandardButton.No:
                scans = [scans[current_scan]]
                current_scan = 0        
        
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
                slice_data.append(s.pixel_array)
        
        return numpy.asarray(slice_data)

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

    def load_metadata(self, scan):
        slice = None
        scan_dir = os.path.join(self.scan_level, scan)
        for f in os.listdir(scan_dir):
            if f.endswith(DICOM.EXTENSIONS): 
                slice = pydicom.read_file(os.path.join(scan_dir,f), defer_size=0)
                break

        if slice == None:
            raise LoadError("Couldn´t load metadata.")

        metadata = {}

        ignore = ["PixelData"]
        for e in slice:
            if not e.keyword in ignore and not e.keyword == "":
                metadata[e.keyword] = e.value
        
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
