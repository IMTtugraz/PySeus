from .base import BaseFct


class RoIFct(BaseFct):
    """Displays the coordinates of the current RoI."""

    def __init__(self):
        BaseFct.__init__(self)

    def recalculate(self, data, roi):
        result = "X: {}-{} | Y: {}-{} | Area: {}".format(
            roi[0], roi[2], roi[1], roi[3],
            abs((roi[0]-roi[2])*(roi[3]-roi[1])))

        return "RoI: " + result
