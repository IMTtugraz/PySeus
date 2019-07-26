class BaseMode():
    """Defines the basic functionality for visualization modes."""

    def __init__(self):
        pass

    def setup(self, data):
        """Adjust mode configuration (eg. window) on loading new frame."""
        pass

    def prepare(self, data):
        """Prepare frame data for display."""
        pass
    
    def move(self, steps):
        """Move the window up / down; results in a darker / lighter image."""
        pass

    def scale(self, steps):
        """Shrink / widen the window; results in higher / lower contrast."""
        pass

    def adjust(self, move, scale):
        """Move the window up / down and shrink / widen simultaneously."""
        self.move(move)
        self.scale(scale)

    def reset(self):
        """Reset the window configuration to the initial values."""
        pass
