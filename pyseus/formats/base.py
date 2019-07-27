class BaseFormat():
    """Defines the basic functionality for file / data formats."""

    def __init__(self):
        self.type = ""
        self.path = ""
        self.file = None

    def load_file(self, path):
        """Attempt to load the file at *path*."""
        pass

    def load_data(self, data):
        """Attempt to load *data*."""
        pass

    def load_frame(self, frame):
        """Extract the specified frame from the current file / dataset."""
        pass
