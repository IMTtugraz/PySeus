import h5py
import numpy

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, \
    QLabel, QScrollArea
from PySide2.QtGui import QImage, QPixmap, QPalette

from context import pyseus

file = h5py.File("test.h5", "r")
tmp = numpy.asarray(file['images'][0])
a = numpy.amax(tmp)
b = numpy.amin(tmp)
tmp = tmp * (255 / a)
npa = tmp.astype(numpy.int8).copy()

image = QImage(npa.data, npa.shape[1], npa.shape[0], npa.strides[0], QImage.Format_Grayscale8)

pyseus.load_image(image)
