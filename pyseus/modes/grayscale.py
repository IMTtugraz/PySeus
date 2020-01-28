"""Display classes model the translation of values to color.

Classes
-------

**Grayscale** - Grayscale images with simple windowing.
"""

import numpy
import cv2
from functools import partial

from ..settings import settings
from .base import BaseMode


class Grayscale(BaseMode):
    """Display class for grayscale images with simple windowing."""

    @classmethod
    def setup_menu(cls, app, menu, ami):
        ami(menu, "&Gray - Amplitude", partial(cls.start, app, 0))
        ami(menu, "&Gray - Phase", partial(cls.start, app, 1))

    @classmethod
    def start(cls, app, src):
        if not isinstance(app.mode, cls):
            app.mode = cls()
        app.mode.set_source(src)
        app.refresh()

    def __init__(self):
        self.source = 0
        """Determines wheter amplitude (0) or phase (1) information from the
        data is used. Default ist amplitude (0)."""

    def prepare(self, data):
        data = self.prepare_raw(data)
        data = self.apply_window(data)
        return data

    def prepare_raw(self, data):
        if self.source == 1:
            data = numpy.angle(data).astype(float)
        elif self.source == 0:
            data = numpy.absolute(data).astype(float)

        return data

    def apply_window(self, data):
        if self.source == 1:
            data += numpy.pi  # align -pi to 0
            data *= 255 / (2*numpy.pi)  # scale pi to 255

        elif self.source == 0:
            data -= self.black  # align black to 0
            data *= 255 / (self.white - self.black)  # scale white to 255

        data = data.clip(0, 255)
        return data.astype(numpy.uint8).copy()

    def setup_data(self, data):
        data = numpy.absolute(data)
        self.data_min = numpy.amin(data)
        self.data_max = numpy.amax(data)
        self.reset_window()

    def temporary_window(self, data):
        data = numpy.absolute(data)
        self.black = numpy.amin(data)
        self.white = numpy.amax(data)

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
        """Use amplitude (1) or phase (0) infromation in data."""

        self.source = src
        self.reset_window()
