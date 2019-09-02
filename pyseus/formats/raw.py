from .base import BaseFormat


class Raw(BaseFormat):
    """Support for NumPy array data and files."""

    def __init__(self):
        BaseFormat.__init__(self)

    @classmethod
    def check_file(cls, path):
        # Check file if no extension present !!!
        return False

    def load_file(self, file):
        # @TODO load a npa file (pickle)
        pass

    def load_data(self, data):
        # @TODO check for different data types
        # only accepts data from h5 for now
        self.data = data
