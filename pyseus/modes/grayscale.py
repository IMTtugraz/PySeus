"""Display classes model the translation of values to color.

Classes
-------

**Grayscale** - Grayscale images with simple windowing.
"""

from functools import partial

import numpy

from ..settings import settings, DataType
from .base import BaseMode


# M: This class just adjusts the value border for graphical
# representation, no gui things themselves
class Grayscale(BaseMode):
    """Display class for grayscale images with simple windowing."""

    @classmethod
    def setup_menu(cls, app, menu, ami):
        ami(menu, "&Gray - Amplitude - Image",
            partial(cls.start, app, DataType.IMAGE))
        ami(menu, "&Gray - Phase", partial(cls.start, app, DataType.PHASE))
        ami(menu, "&Gray - Amplitude - Root(k-space)",
            partial(cls.start, app, DataType.KSPACE))

    @classmethod
    def start(cls, app, src):  # pylint: disable=W0221
        if not isinstance(app.mode, cls):
            app.mode = cls()
        app.mode.set_source(src)
        app.load_scan()

    def __init__(self):
        BaseMode.__init__(self)

        self.source = DataType.IMAGE
        """Determines wheter (IMAGE) amplitude or PHASE information from the
        data is used or the KSPACE FFT representation. Default is IMAGE amplitude."""

        # exponent for root amplitude representation of k-space
        self.exp_kspace = 0.3

    def prepare(self, data):
        data = self.prepare_raw(data)
        data = self.apply_window(data)
        return data

    def prepare_raw(self, data):
        if self.source == DataType.PHASE:
            data = numpy.angle(data).astype(float)
        elif self.source == DataType.IMAGE:
            data = numpy.absolute(data).astype(float)
        elif self.source == DataType.KSPACE:
            data = ((numpy.absolute(numpy.fft.fftshift(data)))
                    ** self.exp_kspace).astype(float)

        return data

    def apply_window(self, data):
        if self.source == DataType.PHASE:
            data += numpy.pi  # align -pi to 0
            data *= 255 / (2 * numpy.pi)  # scale pi to 255

        elif self.source == DataType.IMAGE or self.source == DataType.KSPACE:
            data -= self.black  # align black to 0
            data *= 255 / (self.white - self.black)  # scale white to 255

        data = data.clip(0, 255)
        return data.astype(numpy.uint8).copy()

    def setup_window(self, data):
        if self.source == DataType.IMAGE or self.source == DataType.PHASE:
            data = numpy.absolute(data)
            self.data_min = numpy.amin(data)
            self.data_max = numpy.amax(data)
        elif self.source == DataType.KSPACE:
            data = (numpy.absolute(data))**self.exp_kspace
            self.data_min = numpy.amin(data)
            self.data_max = numpy.amax(data)
        self.reset_window()

    def temporary_window(self, data):
        if self.source == DataType.IMAGE or self.source == DataType.PHASE:
            data = numpy.absolute(data)
            self.black = numpy.amin(data)
            self.white = numpy.amax(data)
        elif self.source == DataType.KSPACE:
            data = (numpy.absolute(data))**self.exp_kspace
            self.black = numpy.amin(data)
            self.white = numpy.amax(data)

    # reset Window just for current scan (3D) to original value
    def reset_window(self):
        self.black = self.data_min
        self.white = self.data_max

    def move_window(self, steps):
        delta = self.data_max - self.data_min
        step_size = float(settings["window"]["move_step"])
        self.black += delta * step_size * steps
        self.white += delta * step_size * steps

    def scale_window(self, steps):
        delta = self.data_max - self.data_min
        step_size = float(settings["window"]["scale_step"])
        new_black = self.black - delta * step_size * steps
        new_white = self.white + delta * step_size * steps
        if new_white > new_black:
            self.black = new_black
            self.white = new_white

    def adjust_window(self, move_steps, scale_steps):
        self.move_window(move_steps)
        self.scale_window(scale_steps)

    def set_source(self, src):
        """Represent amplitude (1) or phase (0) or FFT (2) (Root(data) and FFTShift) information in data."""

        self.source = src
        self.reset_window()
