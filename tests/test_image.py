import numpy

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, \
    QLabel, QScrollArea
from PySide2.QtGui import QImage, QPixmap, QPalette

import context
from context import pyseus

image = QImage("test.jpg")

pyseus.load_image(image)
