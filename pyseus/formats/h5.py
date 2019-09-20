import h5py
import numpy
from functools import partial
import os

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QLayout, \
        QVBoxLayout, QDialogButtonBox, QListWidget, QListWidgetItem

from .base import BaseFormat, LoadError


class H5(BaseFormat):
    """Support for HDF5 files."""

    def __init__(self):
        BaseFormat.__init__(self)

    EXTENSIONS = (".h5", ".hdf5")

    @classmethod
    def check_file(cls, path):
        _, ext = os.path.splitext(path)
        return ext in cls.EXTENSIONS

    def load_file(self, path):
        self.path = path

        with h5py.File(path, "r") as f:

            nodes = []
            def _walk(name, item):
                if isinstance(item, h5py.Dataset):
                    nodes.append(name)
            
            f.visititems(_walk)

            if len(nodes) == 1:
                self.ds_path = nodes[0]
            
            else:
                dialog = H5Explorer(nodes)
                choice = dialog.exec()
                if choice == QDialog.Accepted:
                    self.ds_path = dialog.result()
                else:
                    return "", [], -1
            
            self.dimensions = len(f[self.ds_path].dims)
            if 2 <= self.dimensions <= 3:  # single or multiple slices
                return path, [0], 0
            elif self.dimensions == 4:  # multiple scans
                return path, list(range(0, len(f[self.ds_path])-1)), 0
            elif self.dimensions == 5:
                QMessageBox.warning(self.window, "Pyseus", 
                    "The selected dataset ist 5-dimensional. The first two dimensions will be concatenated.")
                scan_count = f[self.ds_path].shape[0]*f[self.ds_path].shape[1]
                return path, list(range(0, scan_count-1)), 0
            else:
                raise LoadError("Invalid dataset '{}' in '{}': Wrong dimensions.".format(self.ds_path, path))
    
    def load_scan(self, scan):
        with h5py.File(self.path, "r") as f:
            if self.dimensions == 2:  # single slice
                return numpy.asarray([f[self.ds_path]])
            if self.dimensions == 3:  # multiple slices
                return numpy.asarray(f[self.ds_path])
            elif self.dimensions == 4:  # multiple scans
                return numpy.asarray(f[self.ds_path][scan])
            elif self.dimensions == 5:
                q, r = divmod(scan, f[self.ds_path].shape[1])
                return numpy.asarray(f[self.ds_path][q][r])


    def load_scan_thumb(self, scan):
        with h5py.File(self.path, "r") as f:
            scan = f[self.ds_path][scan]
            return numpy.asarray(scan[len(scan) // 2])


class H5Explorer(QDialog):
    """H5Explorer"""

    def __init__(self, items):
        QDialog.__init__(self)
        self.setWindowTitle("Select Dataset")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowModality(Qt.ApplicationModal)  

        self.label = QLabel("Choose the dataset to load:")
        self.label.setStyleSheet("color: #000")
        self.view = QListWidget()

        for i in items:
            self.view.addItem(QListWidgetItem(i))

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel);
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
