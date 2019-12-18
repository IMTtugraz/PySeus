import numpy
from functools import partial

from PySide2.QtGui import QPainter, QColor, QPen

from .base import BaseTool


class AreaTool(BaseTool):
    """Evaluates data in a simple RoI."""

    def __init__(self, app):
        BaseTool.__init__(self, app)

        self.roi = [0, 0, 0, 0]
        """Coordinates of the current region of interest."""

    @classmethod
    def setup_menu(cls, app, menu, ami):
        ami(menu, "&Area Eval", partial(cls.start, app))

    def start_roi(self, x, y):
        self.roi[0] = x
        self.roi[1] = y

    def end_roi(self, x, y):
        self.roi[2] = x
        self.roi[3] = y

    def draw_overlay(self, pixmap):
        if self.roi == [0, 0, 0, 0]:
            return pixmap

        painter = QPainter(pixmap)
        pen = QPen(QColor("red"))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(self.roi[0], self.roi[1], self.roi[2]
                         - self.roi[0], self.roi[3] - self.roi[1])

        painter.end()
        return pixmap

    def clear(self):
        self.roi = [0, 0, 0, 0]

    def recalculate(self, data):
        xmin = numpy.minimum(self.roi[0], self.roi[2])
        xmax = numpy.maximum(self.roi[0], self.roi[2])
        ymin = numpy.minimum(self.roi[1], self.roi[3])
        ymax = numpy.maximum(self.roi[1], self.roi[3])

        roi = data[xmin:xmax, ymin:ymax]
        min = numpy.amin(roi)
        max = numpy.amax(roi)
        med = numpy.median(roi)
        avg = numpy.average(roi)

        if avg > med:
            result = ("Min: {:.4g}  |  Med: {:.4g}  |  Avg: {:.4g}  |  "
                      "Max: {:.4g}").format(min, med, avg, max)
        else:
            result = ("Min: {:.4g}  |  Avg: {:.4g}  |  Med: {:.4g}  |  "
                      "Max: {:.4g}").format(min, avg, med, max)

        self.app.window.console.print("Stats:   " + result)
