class BaseFormat():
    """Defines the basic functionality for file / data formats."""

    def __init__(self):
        pass

    @classmethod
    def check_file(cls, path):
        """See if the format can handle the file at `path`."""
        pass

    def load_file(self, path):
        """Attempt to load the file at `path`."""
        pass
