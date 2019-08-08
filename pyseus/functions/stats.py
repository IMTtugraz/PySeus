import numpy

from .base import BaseFct


class StatsFct(BaseFct):
    """Displays basic statistics (min, max, avg) for the RoI."""

    MENU_NAME = "Statistics"

    def __init__(self):
        BaseFct.__init__(self)

    def recalculate(self, data, roi):
        roi = data[roi[0]:roi[2], roi[1]:roi[3]]
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

        return "Stats: " + result
