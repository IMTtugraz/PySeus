"""Basics for display mode classes.

Classes
-------

**BaseMode** - Defines the interface for display mode classes.
"""

import cv2

from PySide2.QtGui import QImage, QPixmap


class BaseMode():
    """Defines the interface for display mode classes."""

    @classmethod
    def setup_menu(cls, app, menu, ami):
        """Add the tool to the menu bar in the main window."""

    @classmethod
    def start(cls, app):
        """Set the respective tool as active."""
        app.mode = cls()

    def __init__(self):
        self.data_min = 0
        """Minimum value used for resetting the window."""

        self.data_max = 1
        """Maximum value used for resetting the window."""

        self.black = 0
        """Value translated to black (lower bound of window)."""

        self.white = 1
        """Value translated to white (upper bound of window)."""

    def prepare(self, data):  # pylint: disable=R0201
        """Prepare data for display (see *prepare_raw*)
        and apply windowing settings."""

        return data

    def prepare_raw(self, data):  # pylint: disable=R0201
        """Prepare data for analysis.
        Use amplitude or phase data occording to the current display mode."""

        return data

    def apply_window(self, data):
        """Apply current window settings to *data*."""

    def setup_window(self, data):
        """Analyze data and set window and boundary conditions (min, max)."""

    def temporary_window(self, data):
        """Analyze data and set window (black, white). Used for temporary
        changes in window settings like thumbnail generation."""

    def reset_window(self):
        """Reset the window to cover the entire range of values in the data."""

    def move_window(self, steps):
        """Move the window up / down; results in a darker / lighter image.
        Step size is controlled in *settings.ini*."""

    def scale_window(self, steps):
        """Shrink / widen the window; results in higher / lower contrast.
        Step size is controlled in *settings.ini*."""

    def adjust_window(self, move_steps, scale_steps):
        """Move and scale the window simultaneously."""

    def generate_thumb(self, data, size):
        """Resize data for use as a thumbnail.
        Thumbnail size is controlled in *settings.ini*."""

        self.temporary_window(data)

        # @TODO preserve AR (calculate height, width separately)
        thumb = cv2.resize(data, (size, size))

        return thumb

    def get_pixmap(self, data):
        """Convert *data* into a QPixmap object."""

        data = self.prepare(data)
        image = QImage(data.data, data.shape[1], data.shape[0],
                       data.data.strides[0], QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image)

        return pixmap
