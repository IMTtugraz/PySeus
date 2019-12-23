"""Support for DICOM files.

Classes
-------

**H5** - Class modeling HDF5 datasets.
**H5Explorer** - Dialog for selecting a dataset in an H5 file.
"""

import os
import numpy

import h5py

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QLabel, QLayout, QVBoxLayout, \
                              QDialogButtonBox, QMessageBox, \
                              QListWidget, QListWidgetItem

from .base import BaseFormat, LoadError


class H5(BaseFormat):
    """Class modeling DICOM datasets.

    Supports *.h5*-files in HDF5 format.
    Supports metadata, pixelspacing, scale, units and orientation
    using attributes and DICOM-standard keywords."""

    EXTENSIONS = (".h5", ".hdf5")

    @classmethod
    def can_handle(cls, path):
        _, ext = os.path.splitext(path)
        return ext.lower() in H5.EXTENSIONS

    def __init__(self):
        BaseFormat.__init__(self)

        self.meta_keymap = {
            "pys:patient": ["PatientName"],
            "pys:series": ["SeriesDescription"],
            "pys:sequence": ["SequenceName"],
            "pys:matrix": ["AcquisitionMatrix"],
            "pys:tr": ["RepetitionTime"],
            "pys:te": ["EchoTime"],
            "pys:alpha": ["FlipAngle"]
        }

        self.subpath = ""
        """Internal path to the current dataset in the H5 file."""

        self.dims = 0
        """Number of dimensions of the current dataset in the H5 file."""

    def load(self, path):
        if not os.path.isfile(path):
            raise LoadError("File not found.")

        with h5py.File(path, "r") as file_:

            nodes = []

            def _walk(name, item):
                if isinstance(item, h5py.Dataset):
                    nodes.append(name)

            file_.visititems(_walk)

            if len(nodes) == 1:
                self.subpath = nodes[0]

            else:
                dialog = H5Explorer(nodes)
                choice = dialog.exec()
                if choice == QDialog.Accepted:
                    self.subpath = dialog.result()
                else:
                    return False

            self.path = path
            self.dims = len(file_[self.subpath].dims)

            if 2 <= self.dims <= 3:  # single or multiple slices
                self.scans = [0]

            elif self.dims == 4:  # multiple scans
                self.scans = list(range(0, len(file_[self.subpath])-1))

            elif self.dims == 5:
                message = ("The selected dataset is 5-dimensional."
                           "The first two dimensions will be concatenated.")
                QMessageBox.warning(None, "Pyseus", message)
                scan_count = (file_[self.subpath].shape[0]
                              * file_[self.subpath].shape[1])
                self.scans = list(range(0, scan_count-1))

            else:
                message = "Invalid dataset '{}' in '{}': Wrong dimensions." \
                          .format(self.subpath, path)
                raise LoadError(message)

            self.scan = 0
            return True

    def get_scan_pixeldata(self, scan):
        with h5py.File(self.path, "r") as file_:
            if self.dims == 2:  # single slice
                return numpy.asarray([file_[self.subpath]])

            if self.dims == 3:  # multiple slices
                return numpy.asarray(file_[self.subpath])

            if self.dims == 4:  # multiple scans
                return numpy.asarray(file_[self.subpath][scan])

            if self.dims == 5:
                dim_4, dim_5 = divmod(scan, file_[self.subpath].shape[1])
                return numpy.asarray(file_[self.subpath][dim_4][dim_5])

            return []  # can´t interpret data with dimensions <= 1 or > 5

    def get_scan_metadata(self, scan):
        metadata = {}

        with h5py.File(self.path, "r") as file_:
            for attribute in file_[self.subpath].attrs:
                metadata[attribute[0]] = attribute[1]

        return metadata

    def get_spacing(self, axis=None):
        pixel_spacing = [1, 1, 1]
        if "PixelSpacing" in self.metadata.keys():
            pixel_spacing = list(self.metadata["PixelSpacing"])
        elif "pixdim" in self.metadata.keys():
            pixel_spacing = list(self.metadata["pixdim"])

        if axis is None:
            return pixel_spacing[0:2]

        return pixel_spacing[axis]

    def get_scale(self):
        return 0.0

    def get_units(self):
        return ""

    def get_orientation(self):
        return []


class H5Explorer(QDialog):
    """Dialog for selecting a dataset in an H5 file."""

    def __init__(self, items):
        QDialog.__init__(self)
        self.setWindowTitle("Select Dataset")
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.label = QLabel("Choose the dataset to load:")
        self.label.setStyleSheet("color: #000")
        self.view = QListWidget()

        for i in items:
            self.view.addItem(QListWidgetItem(i))

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok
                                        | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self._button_ok)
        self.buttons.rejected.connect(self._button_cancel)

        layout = QVBoxLayout()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        layout.addWidget(self.label)
        layout.addWidget(self.view)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def _button_ok(self):
        self.accept()

    def _button_cancel(self):
        self.reject()

    def result(self):
        """Returns the selected element."""
        return self.view.currentItem().text()
