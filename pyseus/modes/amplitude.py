import numpy

from .base import BaseMode

class Amplitude(BaseMode):

    def __init__(self, data):
        self.data_min = numpy.amin(data)
        self.data_max = numpy.amax(data)
        self.reset()

    def prepare(self, data):
        data -= self.window_min # align window_min to 0
        data *= 255 / (self.window_max - self.window_min) # scale window_max to 255

        data = data.clip(0, 255)
        return data.astype(numpy.int8).copy()

    def move(self, steps):
        delta = self.data_max - self.data_min
        self.window_min += delta * 0.003 * steps
        self.window_max += delta * 0.003 * steps
    
    def scale(self, steps):
        delta = self.data_max - self.data_min
        new_min = self.window_min - delta * 0.003 * steps
        new_max = self.window_max + delta * 0.003 * steps
        if(new_max > new_min):
            self.window_min = new_min
            self.window_max = new_max

    def reset(self):
        self.window_min = self.data_min
        self.window_max = self.data_max