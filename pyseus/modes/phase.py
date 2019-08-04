import numpy

from .base import BaseMode


class Phase(BaseMode):
    """Visualizes the phase of a complex dataset. Uses standard
    windowing behavior.
    """

    def __init__(self):
        BaseMode.__init__(self)

    def prepare(self, data):
        data = numpy.angle(data)
        # align -pi to 0
        data += numpy.pi
        # scale pi to 255
        data *= 255 / (2*numpy.pi)

        data = data.clip(0, 255)
        return data.astype(numpy.int8).copy()

    def move(self, steps):
        pass

    def scale(self, steps):
        pass

    def reset(self):
        pass

    def setup(self, data):
        pass
