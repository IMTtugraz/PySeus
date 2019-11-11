class BaseTool():
    """Defines the basic functionality for RoI evaluation functions."""

    def __init__(self):
        pass

    @classmethod
    def start(cls, app):
        app.tool = cls(app)

    def start_roi(self, x, y):
        pass
    
    def end_roi(self, x, y):
        pass

    def draw_overlay(self, pixmap):
        pass

    def clear(self):
        pass

    def recalculate(self, data, roi):
        """Evaluates the frame data in a given RoI and returns a result string."""
        pass
