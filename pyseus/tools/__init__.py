"""Tools provide different ways to evaluate data.

All tools extend the *BaseTool* class, guaranteeing basic functionality
of marking regions of interest, and displaying results.
"""

from .base import BaseTool
from .area import AreaTool
from .line import LineTool
