from .base import BaseFormat


class DICOM(BaseFormat):
    """Support for DICOM files (Coming soon)."""

    def __init__(self):
        BaseFormat.__init__(self)
        self.type = "DICOM"
