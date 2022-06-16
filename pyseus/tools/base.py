"""Basics for tool classes.

Classes
-------

**BaseTool** - Defines interface for tool classes.
"""


class BaseTool():
    """Defines the basic functionality for RoI evaluation functions."""

    def __init__(self, app):
        self.app = app

    @classmethod
    def setup_menu(cls, app, menu, ami):
        """Add the mode to the menu bar in the main window."""

    @classmethod
    def start(cls, app):
        """Set the respective mode as active."""
        app.tool = cls(app)

    def start_roi(self, x, y):
        """Start marking a region of interest (on mouse button down)."""

    def end_roi(self, x, y):
        """End marking a region of interest (on mouse button up)."""

    def draw_overlay(self, pixmap):
        """Draws the tool specific overlay on the displayed image."""

    def clear(self):
        """Resets region of interest, image overlays and result display."""

    def recalculate(self, data):
        """Evaluates the data in the set region of interest."""
