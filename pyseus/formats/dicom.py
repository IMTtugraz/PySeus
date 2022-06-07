"""Support for DICOM files.

Classes
-------

**DICOM** - Class modeling DICOM datasets.
"""

import os
import numpy

import pydicom
from natsort import natsorted

from .base import BaseFormat, LoadError


class DICOM(BaseFormat):
    """Class modeling DICOM datasets.

    Supports multiple *.dcm*-files in standard directory structure; DICOMDIR
    files are not supported.
    Supports metadata, pixelspacing, scale, units and orientation.
    """

    EXTENSIONS = (".dcm", ".dicom")

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

        self.scan_level = ""
        """Relative path to the current scan from *self.path* ."""

    @classmethod
    def can_handle(cls, path):
        _, ext = os.path.splitext(path)
        return ext.lower() in cls.EXTENSIONS

    def load(self, path, data_type):
        if not os.path.isfile(path):
            raise LoadError("File not found.")

        self.path = os.path.abspath(path)

        slice_level = os.path.abspath(os.path.dirname(path))
        self.scan_level = os.path.abspath(os.path.join(slice_level, os.pardir))

        scan_dirs = next(os.walk(self.scan_level))[1]
        for dir_ in natsorted(scan_dirs):
            has_dcm = False
            for file_ in os.listdir(os.path.abspath(
                                os.path.join(self.scan_level, dir_))):
                _, ext = os.path.splitext(file_)
                if ext.lower() in DICOM.EXTENSIONS:
                    has_dcm = True
                    break

            if has_dcm and dir_ != "localizer":
                self.scans.append(dir_)

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
        first_slice = True
        scan_dir = os.path.join(self.scan_level, self.scans[scan])
        for file_ in os.listdir(scan_dir):
            _, ext = os.path.splitext(file_)
            if ext.lower() in DICOM.EXTENSIONS:
                slice_ = pydicom.read_file(os.path.join(scan_dir, file_))

                if first_slice:  # get metadata

                    metadata = {}
                    meta_ignore = ["", "PixelData"]
                    for element in slice_:
                        if element.keyword not in meta_ignore:
                            metadata[element.keyword] = element.value

                slices.append(slice_)

        file_count = len(slices)
        slices = [s for s in slices if hasattr(s, "SliceLocation")]

        if file_count > 0 and not slices:
            raise LoadError("DICOM files are missing SliceLocation data.")

        slices = sorted(slices, key=lambda s: s.SliceLocation)

        pixeldata = []
        for slice_ in slices:
            if "PixelData" in slice_:
                pixeldata.append(slice_.pixel_array)

        self.pixeldata = numpy.asarray(pixeldata)
        self.metadata = metadata
        self.scan = scan

        return True

    def get_scan_thumbnail(self, scan):
        # "Correct" implementation; current version guesses middle slice
        # based on file names for performance reasons.
        #
        # slices = []
        # scan_dir = os.path.join(self.scan_level, self.scans[scan])
        # for file_ in os.listdir(scan_dir):
        #     _, ext = os.path.splitext(file_)
        #     if ext.lower() in DICOM.EXTENSIONS:
        #         slice_ = (f, pydicom.filereader.read_file(
        #             os.path.join(scan_dir, file_),
        #             specific_tags=["SliceLocation"]))
        #         slices.append(slice_)
        #
        # slices = [s for s in slices if hasattr(s[1], "SliceLocation")]
        # slices = sorted(slices, key=lambda s: s[1].SliceLocation)
        #
        # thumb_slice = pydicom.read_file(
        #         os.path.join(scan_dir, slices[len(slices) // 2][0]))

        slices = []
        scan_dir = os.path.join(self.scan_level, self.scans[scan])
        for file_ in os.listdir(scan_dir):
            _, ext = os.path.splitext(file_)
            if ext.lower() in DICOM.EXTENSIONS:
                slices.append(file_)

        slices = natsorted(slices)
        thumb_slice = pydicom.read_file(
            os.path.join(scan_dir, slices[len(slices) // 2]))

        return numpy.asarray(thumb_slice.pixel_array)

    def get_scan_metadata(self, scan):
        metadata = {}
        slice_ = None

        scan_dir = os.path.join(self.scan_level, self.scans[scan])
        for file_ in os.listdir(scan_dir):
            _, ext = os.path.splitext(file_)
            if ext.lower() in DICOM.EXTENSIONS:
                slice_ = pydicom.read_file(os.path.join(scan_dir, file_))

                ignore = ["", "PixelData"]
                for element in slice_:
                    if element.keyword not in ignore:
                        metadata[element.keyword] = element.value

        return metadata

    def get_spacing(self, reset=False):
        if not self.pixel_spacing or reset:
            if "PixelSpacing" in self.metadata.keys():
                self.pixel_spacing = list(self.metadata["PixelSpacing"])
            else:
                self.pixel_spacing = [1, 1]

            if "SliceThickness" in self.metadata.keys():
                self.pixel_spacing.append(self.metadata["SliceThickness"])
            else:
                self.pixel_spacing.append(1)

        return self.pixel_spacing

    def get_scale(self):
        if "PixelSpacing" in self.metadata.keys():
            pixel_spacing = list(self.metadata["PixelSpacing"])
            return float(min(pixel_spacing))

        return 0.0

    def get_units(self):
        if "Units" in self.metadata.keys():
            return "{}".format(self.metadata["Units"])
            # not accounting for Rescale Intercept, Rescale Slope

        return "1"

    def get_orientation(self):
        return []
