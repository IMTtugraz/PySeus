import h5py
import numpy

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, \
    QLabel, QScrollArea
from PySide2.QtGui import QImage, QPixmap, QPalette

from context import pyseus

file = h5py.File("test.h5", "r")

pyseus.load(file['images'][0])
