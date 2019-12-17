import h5py
import numpy
import os

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QLabel, QLayout, QVBoxLayout, \
                              QDialogButtonBox, QMessageBox, \
                              QListWidget, QListWidgetItem

from .base import BaseFormat, LoadError


class H5(BaseFormat):
    """Support for HDF5 files.

    Metadata, pixelspacing, scale and orientation are all supported."""

    @classmethod
    def can_handle(cls, path):
        _, ext = os.path.splitext(path)
        return ext.lower() in (".h5", ".hdf5")

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

    def load(self, path):
        with h5py.File(path, "r") as f:

            nodes = []

            def _walk(name, item):
                if isinstance(item, h5py.Dataset):
                    nodes.append(name)

            f.visititems(_walk)

            if len(nodes) == 1:
                self._subpath = nodes[0]

            else:
                dialog = H5Explorer(nodes)
                choice = dialog.exec()
                if choice == QDialog.Accepted:
                    self._subpath = dialog.result()
                else:
                    return False

            self.path = path
            self.dims = len(f[self._subpath].dims)

            if 2 <= self.dims <= 3:  # single or multiple slices
                self.scans = [0]

            elif self.dims == 4:  # multiple scans
                self.scans = list(range(0, len(f[self._subpath])-1))

            elif self.dims == 5:
                message = ("The selected dataset is 5-dimensional."
                           "The first two dimensions will be concatenated.")
                QMessageBox.warning(self.app.window, "Pyseus", message)
                scan_count = f[self._subpath].shape[0]*f[self._subpath].shape[1]
                self.scans = list(range(0, scan_count-1))

            else:
                message = "Invalid dataset '{}' in '{}': Wrong dimensions." \
                          .format(self._subpath, path)
                raise LoadError(message)

            self.scan = 0
            return True

    def get_scan_pixeldata(self, scan):
        with h5py.File(self.path, "r") as f:
            if self.dims == 2:  # single slice
                return numpy.asarray([f[self._subpath]])

            if self.dims == 3:  # multiple slices
                return numpy.asarray(f[self._subpath])

            elif self.dims == 4:  # multiple scans
                return numpy.asarray(f[self._subpath][scan])

            elif self.dims == 5:
                q, r = divmod(scan, f[self._subpath].shape[1])
                return numpy.asarray(f[self._subpath][q][r])

    def get_scan_metadata(self, scan):
        metadata = {}

        with h5py.File(self.path, "r") as f:
            for a in f[self._subpath].attrs:
                metadata[a[0]] = a[1]

        return metadata

    def get_spacing(self, axis=None):
        pixel_spacing = [1, 1, 1]
        if "PixelSpacing" in self.metadata.keys():
            pixel_spacing = list(self.metadata["PixelSpacing"])
        elif "pixdim" in self.metadata.keys():
            pixel_spacing = list(self.metadata["pixdim"])

        if axis is None:
            return pixel_spacing[0:2]
        else:
            return pixel_spacing[axis]

    def get_scale(self):
        return 0.0

    def get_units(self):
        pass

    def get_orientation(self):
        return 0


class H5Explorer(QDialog):
    """H5Explorer"""

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
        """Handles button click on OK"""
        self.accept()

    def _button_cancel(self):
        """Handles button click on Cancel"""
        self.reject()

    def result(self):
        """Returns the selected element"""
        return self.view.currentItem().text()
