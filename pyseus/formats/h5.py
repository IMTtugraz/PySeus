import h5py
import numpy
from functools import partial
import os

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QLayout, \
        QVBoxLayout, QDialogButtonBox, QTreeWidget, QTreeWidgetItem

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
            if len(f.keys()) > 1:
                dialog = H5Explorer(f)
                choice = dialog.exec()
                if choice == QDialog.Accepted:
                    self.ds_path = dialog.result()
                else:
                    self.ds_path = None
            else:
                self.ds_path = list(f.keys())[0]
            
            dimensions = len(f[self.ds_path].dims)
            if 2 <= dimensions <= 3:  # single or multiple slices
                return path, [0], 0
            elif dimensions == 4:  # multiple scans
                return path, range(0, len(f[self.ds_path].dims[3])-1), 0
                pass
            else:
                raise LoadError("Invalid dataset '{}' in '{}': Wrong dimensions.".format(self.ds_path, path))
    
    def load_scan(self, scan):
        with h5py.File(self.path, "r") as f:
            dimensions = len(f[self.ds_path].dims)
            if 2 <= dimensions <= 3:  # single or multiple slices
                return numpy.asarray(f[self.ds_path])
            elif dimensions == 4:  # multiple scans
                return numpy.asarray(f[self.ds_path][scan])

    def load_scan_thumb(self, scan):
        with h5py.File(self.path, "r") as f:
            scan = f[self.ds_path][scan]
            return numpy.asarray(scan[len(scan) // 2])


class H5Explorer(QDialog):

    def __init__(self, file):
        QDialog.__init__(self)
        self.setWindowTitle("Test")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowModality(Qt.ApplicationModal)  

        self.label = QLabel("Choose the dataset to load:")
        self.view = QTreeWidget()
        self.view.setHeaderHidden(True)
        self.view.setColumnCount(1)

        node = QTreeWidgetItem()
        file.visititems(partial(self._walk, node))
        for n in node.takeChildren():
            self.view.addTopLevelItem(n)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel);
        self.buttons.accepted.connect(self._button_ok)
        self.buttons.rejected.connect(self._button_cancel)

        layout = QVBoxLayout()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        layout.addWidget(self.label)
        layout.addWidget(self.view)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def _walk(self, tree_node, name, node):
        tree_node.addChild(QTreeWidgetItem([name]))
    
    def _button_ok(self):
        self.accept()
    
    def _button_cancel(self):
        self.reject()
    
    def result(self):
        return self.view.currentItem().text(0)
