import numpy

from .base import BaseFct


class StatsFct(BaseFct):
    """Displays basic statistics (min, max, avg) for the RoI."""

    def __init__(self):
        BaseFct.__init__(self)

    def recalculate(self, data, roi):
        roi = data[roi[0]:roi[2], roi[1]:roi[3]]
        min = numpy.amin(roi)
        max = numpy.amax(roi)
        med = numpy.median(roi)
        avg = numpy.average(roi)
        
        if avg > med:
            return "Min: {g.4} | Med: {g.4} | Avg: {g.4} | Max: {g.4}".format(min, med, avg, max)
        else:
            return "Min: {g.4} | Avg: {g.4} | Med: {g.4} | Max: {g.4}".format(min, avg, med, max)
