from .base import BaseFct


class TestFct(BaseFct):
    """Displays the coordinates of the current RoI."""

    def __init__(self):
        BaseFct.__init__(self)

    def recalculate(self, data, roi):
        return "RoI: {}x{} - {}x{}".format(roi[0], roi[1], roi[2], roi[3])
