import pydicom
import numpy
import os
from natsort import natsorted

from .base import BaseFormat, LoadError


class DICOM(BaseFormat):
    """Support for DICOM files.

    Currently, only .dcm files are supported.
    Metadata, pixelspacing, scale and orientation are all supported."""

    def __init__(self):
        BaseFormat.__init__(self)

        self.meta_keymap = {
            "pys:patient": "PatientName",
            "pys:series": "SeriesDescription",
            "pys:sequence": "SequenceName",
            "pys:matrix": "AcquisitionMatrix",
            "pys:tr": "RepetitionTime",
            "pys:te": "EchoTime",
            "pys:alpha": "FlipAngle"
        }

    @classmethod
    def can_handle(cls, path):
        _, ext = os.path.splitext(path)
        return ext.lower() in (".dcm")

    def load(self, path):
        if not os.path.isfile(path):
            raise LoadError("File not found.")

        self.path = os.path.abspath(path)

        slice_level = os.path.abspath(os.path.dirname(path))
        self.scan_level = os.path.abspath(os.path.join(slice_level, os.pardir))

        scan_dirs = next(os.walk(self.scan_level))[1]
        for d in natsorted(scan_dirs):
            has_dcm = False
            for f in os.listdir(os.path.abspath(
                                os.path.join(self.scan_level, d))):
                _, ext = os.path.splitext(f)
                if ext.lower() in (".dcm"):
                    has_dcm = True
                    break

            if has_dcm and d != "localizer":
                self.scans.append(d)

        self.scan = self.scans.index(os.path.basename(slice_level))

        # Currently handled in core
        #
        # if len(self.scans) > 1:
        #     message = "{} scans detected. Do you want to load all scans?" \
        #               .format(len(self.scans))
        #     load_all = QMessageBox.question(None, "Pyseus", message)

        #    if load_all is QMessageBox.StandardButton.No:
        #        self.scans = [self.scans[self.scan]]
        #        self.scan = 0

        return True

    def load_scan(self, scan):
        slices = []
        scan_dir = os.path.join(self.scan_level, self.scans[scan])
        for f in os.listdir(scan_dir):
            _, ext = os.path.splitext(f)
            if ext.lower() in (".dcm"):
                slice = pydicom.read_file(os.path.join(scan_dir, f),
                                          defer_size=0)
                slices.append(slice)

        slice_count = len(slices)
        slices = [s for s in slices if hasattr(s, "SliceLocation")]

        if slice_count > 0 and len(slices) == 0:
            raise LoadError("DICOM files are missing SliceLocation data.")

        slices = sorted(slices, key=lambda s: s.SliceLocation)

        pixeldata = []
        for s in slices:
            if "PixelData" in s:
                pixeldata.append(s.pixel_array)

        self.pixeldata = numpy.asarray(pixeldata)
        self.metadata = self.get_scan_metadata(scan)
        self.scan = scan

        return True

    def get_scan_thumbnail(self, scan):
        slices = []
        scan_dir = os.path.join(self.scan_level, self.scans[scan])
        for f in os.listdir(scan_dir):
            _, ext = os.path.splitext(f)
            if ext.lower() in (".dcm"):
                slice = (f, pydicom.filereader.read_file(
                                os.path.join(scan_dir, f),
                                specific_tags=["SliceLocation"]))
                slices.append(slice)

        slices = [s for s in slices if hasattr(s[1], "SliceLocation")]
        slices = sorted(slices, key=lambda s: s[1].SliceLocation)

        thumb_slice = pydicom.read_file(os.path.join(scan_dir,
                                        slices[len(slices) // 2][0]))

        return numpy.asarray(thumb_slice.pixel_array)

    def get_scan_metadata(self, scan):
        metadata = {}
        slice = None

        scan_dir = os.path.join(self.scan_level, self.scans[scan])
        for f in os.listdir(scan_dir):
            _, ext = os.path.splitext(f)
            if ext.lower() in (".dcm"):
                slice = pydicom.read_file(os.path.join(scan_dir, f),
                                          defer_size=0)

                ignore = ["PixelData"]
                for e in slice:
                    if e.keyword not in ignore and not e.keyword == "":
                        metadata[e.keyword] = e.value

        return metadata

    def get_spacing(self, axis=None):
        pixel_spacing = [1, 1, 1]
        if "PixelSpacing" in self.metadata.keys():
            pixel_spacing = list(self.metadata["PixelSpacing"])

        if axis is None:
            return pixel_spacing[0:2]
        else:
            return pixel_spacing[axis]

    def get_scale(self):
        return 0.001  # DICOM always uses mm here

    def get_units(self):
        if "Units" in self.metadata.keys():
            return "{}*".format(self.metadata["Units"])
            # not accounting for Rescale Intercept, Rescale Slope
        else:
            return "1"

    def get_orientation(self):
        if "DisplaySetPatientOrientation" in self.metadata.keys():
            (right, bottom) = self.metadata["DisplaySetPatientOrientation"]

        return []
