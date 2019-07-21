import h5py
import numpy

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, \
    QLabel, QScrollArea
from PySide2.QtGui import QImage, QPixmap, QPalette

from context import pyseus

pyseus.load_file("test.h5")
