import h5py
import numpy
from functools import partial

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QLayout, \
        QVBoxLayout, QDialogButtonBox, QTreeWidget, QTreeWidgetItem

from .base import BaseFormat


class H5(BaseFormat):
    """Support for HDF5 files."""

    def __init__(self):
        BaseFormat.__init__(self)
        self.type = "H5"

    def load_file(self, path):
        # @TODO check file access
        self.file = h5py.File(path, "r")
        if len(self.file.keys()) > 1:
            dialog = H5Explorer(self.file)
            choice = dialog.exec()
            if choice == QDialog.Accepted:
                self.dataset = dialog.result()
            else:
                self.dataset = None
        else:
            self.dataset = list(self.file.keys())[0]

    def load_frame(self, frame):
        if not self.dataset == None:
            data = numpy.asarray(self.file[self.dataset][frame])
            return data


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
