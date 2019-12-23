"""...
"""

import numpy
import pytest

from PySide2.QtGui import QPixmap

from context import pyseus 
from pyseus import PySeus, DisplayHelper
from pyseus.settings import settings


def test_core():
    # @TODO testing for Qt GUIs
    pass


def test_settigns():
    assert isinstance(settings["ui"]["style"], str)
    with pytest.raises(Exception) as error:
        settings["does_not_exist"]
        assert error.type == KeyError


def test_display():
    app = PySeus(False)  # noqa E841
    display = DisplayHelper()

    data = numpy.array([[1, 3, 0],
                        [0, 9, 0],
                        [0, 1, 0]])

    display.setup_data(data)
    assert display.white == 9
    assert display.black == 0

    prepared = display.prepare(data)
    assert numpy.amin(prepared) == 0
    assert numpy.amax(prepared) == 255

    thumbnail = display.generate_thumb(prepared)
    assert isinstance(thumbnail, numpy.ndarray)
    assert thumbnail.shape[0] <= int(settings["ui"]["thumb_size"])
    assert thumbnail.shape[1] <= int(settings["ui"]["thumb_size"])

    assert isinstance(display.get_pixmap(thumbnail), QPixmap)

    display.reset_window()
    assert display.white == 9
    assert display.black == 0

    display.move_window(2)
    assert display.white > 9
    assert display.black > 0
    display.move_window(-4)
    assert display.white < 9
    assert display.black < 0

    display.scale_window(2)
    assert display.white > 9
    assert display.black < 0
    display.scale_window(-4)
    assert display.white < 9
    assert display.black > 0
