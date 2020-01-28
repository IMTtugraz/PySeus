"""Testcases for main components of PySeus."""

import numpy
import pytest

from PySide2.QtGui import QPixmap

from context import pyseus # noqa F401  # pylint: disable=W0611
from pyseus import PySeus
from pyseus.modes import Grayscale
from pyseus.settings import settings


def test_core():
    """Test basic functionality of PySeus class."""

    # @TODO testing for Qt GUIs


def test_settigns():
    """Test basic functionality of settings implementation."""

    assert isinstance(settings["ui"]["style"], str)
    with pytest.raises(Exception) as error:
        settings["does_not_exist"] = "irrelevant"
        assert error.type == KeyError


def test_grayscale():
    """Test basic functionality of Grayscale class.

    Tests cover initializing window settings, preparing data, generating
    thumbnails, generating Pixmap objects (for display with ViewWidget) and
    manipulating window settings.
    """

    app = PySeus(False)  # noqa E841  # pylint: disable=W0612
    display = Grayscale()

    data = numpy.array([[1, 3, 0],
                        [0, 9, 0],
                        [0, 1, 0]])

    display.setup_data(data)
    assert display.white == 9
    assert display.black == 0

    prepared = display.prepare(data)
    assert numpy.amin(prepared) == 0
    assert numpy.amax(prepared) == 255

    thumbnail = display.generate_thumb(prepared, 
                                       int(settings["ui"]["thumb_size"]))
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
