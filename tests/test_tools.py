"""Testcases for PySeus tool classes."""

import numpy

from PySide2.QtGui import QPixmap

from context import pyseus
from pyseus import PySeus
from pyseus.modes import Grayscale
from pyseus.tools import AreaTool, LineTool


app = PySeus(False)  # pylint: disable=C0103
display = Grayscale()  # pylint: disable=C0103
data = numpy.array([[1, 3, 0],  # pylint: disable=C0103
                    [0, 9, 0],
                    [0, 1, 0]])


def test_area_tool():
    """Test basic functionality of the AreaTool class."""

    tool = AreaTool(app)

    display.setup_window(data)
    pixmap = display.get_pixmap(data)
    assert isinstance(tool.draw_overlay(pixmap), QPixmap)

    tool.start_roi(1, 2)
    tool.end_roi(3, 4)
    assert tool.roi == [1, 2, 3, 4]


def test_line_tool():
    """Test basic functionality of the LineTool class."""

    tool = LineTool(app)

    display.setup_window(data)
    pixmap = display.get_pixmap(data)
    assert isinstance(tool.draw_overlay(pixmap), QPixmap)

    tool.start_roi(1, 2)
    tool.end_roi(3, 4)
    assert tool.line == [1, 2, 3, 4]

    # @TODO testing for Qt GUI (chart window)
