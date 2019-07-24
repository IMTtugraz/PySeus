class BaseMode():
    def prepare(self, data):
        pass
    
    def move(self, steps):
        pass

    def scale(self, steps):
        pass

    def adjust(self, move, scale):
        self.move(move)
        self.scale(scale)

    def reset(self):
        pass

    def setup(self, data):
        pass
