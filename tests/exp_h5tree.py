import h5py
from functools import partial

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QLayout, \
        QVBoxLayout, QDialogButtonBox, QTreeWidget, QTreeWidgetItem


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
        f = h5py.File(file, "r")
        f.visititems(partial(self._walk, node))
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

app = QApplication()
win = H5Explorer("test.h5")
res = win.exec()
if res == QDialog.Accepted:
    print(win.result())
else:
    print("Cancled")
