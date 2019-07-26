from PySide2.QtGui import QImage

from context import pyseus

image = QImage("test.jpg")

pyseus.load(image)
