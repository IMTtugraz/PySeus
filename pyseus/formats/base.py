class BaseFormat():

    def __init__(self):
        self.type = ""
        self.path = ""
        self.file = None
    
    def load_file(self, file):
        pass
    
    def load_frame(self, frame):
        pass
    
    def prepare(self, data):
        pass
