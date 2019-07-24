import numpy

from .base import BaseFct

class StatsFct(BaseFct):

    def __init__(self):
        BaseFct.__init__(self)

    def recalculate(self, data, roi):
        roi = data[roi[0]:roi[2], roi[1]:roi[3]]
        min = numpy.amin(roi)
        max = numpy.amax(roi)
        avg = numpy.average(roi)
        return "Min: {} | Max: {} | Avg: {}".format(min, max, avg)
