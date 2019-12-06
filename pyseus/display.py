import numpy

from PySide2.QtGui import QImage, QPixmap

from pyseus import settings


class DisplayHelper():
    """A collection of display helper functions."""

    def __init__(self, app):
        self.app = app
        
        self.mode = 0
        """Determines wheter amplitude (0) or phase (1) from the data is used.
        Default ist amplitude (0)."""


    def prepare(self, data):
        """Prepare data for display or analysis (see `prepare_without_window`)
        and apply windowing settings."""

        data = self.prepare_without_window(data)
        data = self.apply_window(data)
        return data


    def prepare_without_window(self, data):
        """Prepare data for display or analysis.
        Use amplitude or phase data occording to the current display mode
        and apply pixel scaling."""

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
        return data.astype(numpy.int8).copy()


    def setup_window(self, data):
        """Analyze data and set window boundary conditions (min, max)."""

        data = numpy.absolute(data)
        self.data_min = numpy.amin(data)
        self.data_max = numpy.amax(data)
        self.reset_window()

   
    def reset_window(self):
        """Reset the window to cover the entire range of values in the data."""

        self.black = self.data_min
        self.white = self.data_max


    def move_window(self, steps):
        """Move the window up / down; results in a darker / lighter image.
        Step size is controlled in settings.ini."""

        delta = self.data_max - self.data_min
        step_size = float(settings["window"]["move_step"])
        self.black += delta * step_size * steps
        self.white += delta * step_size * steps


    def scale_window(self, steps):
        """Shrink / widen the window; results in higher / lower contrast.
        Step size is controlled in settings.ini."""

        delta = self.data_max - self.data_min
        step_size = float(settings["window"]["scale_step"])
        new_black = self.black - delta * step_size * steps
        new_white = self.white + delta * step_size * steps
        if(new_white > new_black):
            self.black = new_black
            self.white = new_white


    def adjust_window(self, move_steps, scale_steps):
        """Move and scale the window simultaneously."""

        self.move_window(move_steps)
        self.scale_window(scale_steps)


    def set_mode(self, mode):
        """Set the display mode to Amplitude (1) or phase (0)."""

        self.mode = mode
        self.app.refresh()


    def generate_thumb(self, data):
        """Resize data for use as a thumbnail.
        Thumbnail size is controlled in settings.ini."""

        thumb_size = int(settings["ui"]["thumb_size"])
        thumb_data = cv2.resize(data, (thumb_size, thumb_size))

        self.setup_window(thumb_data)
        return self.prepare(thumb_data)


    def get_pixmap(self, data):
        """Convert `data` into a QPixmap object."""

        tmp = self.prepare(data)
        image = QImage(tmp.data, tmp.shape[1], tmp.shape[0], tmp.data.strides[0],
                       QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image)

        return pixmap
