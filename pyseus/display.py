import numpy

from pyseus import settings


class DisplayHelper():
    """A collection of display helper functions."""

    def __init__(self, app):
        self.app = app
        
        self.mode = 0
        """Amplitude or Phase"""
    
    def prepare(self, data):
        if self.mode == 1:
            data = numpy.angle(data).astype(float)
            data += numpy.pi  # align -pi to 0
            data *= 255 / (2*numpy.pi)  # scale pi to 255

        elif self.mode == 0:
            data = numpy.absolute(data).astype(float)
            data -= self.black  # align black to 0
            data *= 255 / (self.white - self.black)  # scale white to 255
        
        data = data.clip(0, 255)
        return data.astype(numpy.int8).copy()

    def setup_window(self, data):
        data = numpy.absolute(data)
        self.data_min = numpy.amin(data)
        self.data_max = numpy.amax(data)
        self.reset_window()
    
    def reset_window(self):
        self.black = self.data_min
        self.white = self.data_max

    def move_window(self, steps):
        """Move the window up / down; results in a darker / lighter image."""
        delta = self.data_max - self.data_min
        step_size = float(settings["window"]["move_step"])
        self.black += delta * step_size * steps
        self.white += delta * step_size * steps

    def scale_window(self, steps):
        """Shrink / widen the window; results in higher / lower contrast."""
        delta = self.data_max - self.data_min
        step_size = float(settings["window"]["scale_step"])
        new_black = self.black - delta * step_size * steps
        new_white = self.white + delta * step_size * steps
        if(new_white > new_black):
            self.black = new_black
            self.white = new_white

    def adjust_window(self, move, scale):
        """Move the window up / down and shrink / widen simultaneously."""
        self.move_window(move)
        self.scale_window(scale)

    def set_mode(self, mode):
        self.mode = mode
        self.app.refresh()

    def generate_thumb(self, data):
        thumb_size = int(settings["ui"]["thumb_size"])
        thumb_data = cv2.resize(data, (thumb_size, thumb_size))

        self.setup_window(thumb_data)
        return self.prepare(thumb_data)

    def get_pixmap(self, data):
        tmp = self.prepare(data)

        image = QImage(tmp.data, tmp.shape[1], tmp.shape[0], tmp.strides[0],
                       QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image)
