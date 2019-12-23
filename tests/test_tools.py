"""...
"""

import numpy

from PySide2.QtGui import QPixmap

from context import pyseus
from pyseus import PySeus, DisplayHelper
from pyseus.tools import AreaTool, LineTool


app = PySeus(False)
display = DisplayHelper()
data = numpy.array([[1, 3, 0],
                    [0, 9, 0],
                    [0, 1, 0]])


def test_area_tool():
    tool = AreaTool(app)

    display.setup_data(data)
    pixmap = display.get_pixmap(data)
    assert isinstance(tool.draw_overlay(pixmap), QPixmap)

    tool.start_roi(1, 2)
    tool.end_roi(3, 4)
    assert tool.roi == [1, 2, 3, 4]


def test_line_tool():
    tool = LineTool(app)

    display.setup_data(data)
    pixmap = display.get_pixmap(data)
    assert isinstance(tool.draw_overlay(pixmap), QPixmap)

    tool.start_roi(1, 2)
    tool.end_roi(3, 4)
    assert tool.line == [1, 2, 3, 4]

    # @TODO test Qt GUI (chart window)
