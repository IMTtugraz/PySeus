"""Collection of helper functions for displaying image data.

Classes
-------

**DisplayHelper** - Greyscale images with simple windowing.
"""

import numpy
import cv2

from PySide2.QtGui import QImage, QPixmap

from pyseus import settings


class DisplayHelper():
    """Display helper functions for greyscale images with simple windowing."""

    def __init__(self):
        self.mode = 0
        """Determines wheter amplitude (0) or phase (1) information from the
        data is used. Default ist amplitude (0)."""

        self.data_min = 0
        """Minimum value used for resetting the window."""

        self.data_max = 1
        """Maximum value used for resetting the window."""

        self.black = 0
        """Value translated to black (lower bound of window)."""

        self.white = 1
        """Value translated to white (upper bound of window)."""

    def prepare(self, data):
        """Prepare data for display or analysis (see `prepare_without_window`)
        and apply windowing settings."""

        data = self.prepare_without_window(data)
        data = self.apply_window(data)
        return data

    def prepare_without_window(self, data):
        """Prepare data for display or analysis.
        Use amplitude or phase data occording to the current display mode."""

        if self.mode == 1:
            data = numpy.angle(data).astype(float)
        elif self.mode == 0:
            data = numpy.absolute(data).astype(float)

        return data

    def apply_window(self, data):
        """Apply current window settings to `data`."""

        if self.mode == 1:
            data += numpy.pi  # align -pi to 0
            data *= 255 / (2*numpy.pi)  # scale pi to 255

        elif self.mode == 0:
            data -= self.black  # align black to 0
            data *= 255 / (self.white - self.black)  # scale white to 255

        data = data.clip(0, 255)
        return data.astype(numpy.uint8).copy()

    def setup_data(self, data):
        """Analyze data and set window and boundary conditions (min, max)."""

        data = numpy.absolute(data)
        self.data_min = numpy.amin(data)
        self.data_max = numpy.amax(data)
        self.reset_window()

    def setup_window(self, data):
        """Analyze data and set window (black, white). Used for temporary
        changes in window settings like thumbnail generation."""

        data = numpy.absolute(data)
        self.black = numpy.amin(data)
        self.white = numpy.amax(data)

    def reset_window(self):
        """Reset the window to cover the entire range of values in the data."""

        self.black = self.data_min
        self.white = self.data_max

    def move_window(self, steps):
        """Move the window up / down; results in a darker / lighter image.
        Step size is controlled in `settings.ini`."""

        delta = self.data_max - self.data_min
        step_size = float(settings["window"]["move_step"])
        self.black += delta * step_size * steps
        self.white += delta * step_size * steps

    def scale_window(self, steps):
        """Shrink / widen the window; results in higher / lower contrast.
        Step size is controlled in `settings.ini`."""

        delta = self.data_max - self.data_min
        step_size = float(settings["window"]["scale_step"])
        new_black = self.black - delta * step_size * steps
        new_white = self.white + delta * step_size * steps
        if new_white > new_black:
            self.black = new_black
            self.white = new_white

    def adjust_window(self, move_steps, scale_steps):
        """Move and scale the window simultaneously."""

        self.move_window(move_steps)
        self.scale_window(scale_steps)

    def set_mode(self, mode):
        """Set the display mode to amplitude (1) or phase (0)."""

        self.mode = mode
        self.reset_window()

    def generate_thumb(self, data):
        """Resize data for use as a thumbnail.
        Thumbnail size is controlled in `settings.ini`."""

        self.setup_window(data)

        thumb_size = int(settings["ui"]["thumb_size"])
        thumb = cv2.resize(data, (thumb_size, thumb_size))
        # @TODO preserve AR (calculate height, width separately)

        return thumb

    def get_pixmap(self, data):
        """Convert `data` into a QPixmap object."""

        data = self.prepare(data)
        image = QImage(data.data, data.shape[1], data.shape[0],
                       data.data.strides[0], QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image)

        return pixmap
