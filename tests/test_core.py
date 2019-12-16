"""...
"""

import numpy
import pytest

from context import pyseus
from pyseus import PySeus, DisplayHelper
from pyseus.settings import settings


def test_core():
    # @TODO testing for Qt applications
    pass

def test_settigns():
    assert isinstance(settings["ui"]["style"], str)
    with pytest.raises(Exception) as error:
        settings["does_not_exist"]
        assert error.type == KeyError

def test_display():
    # @TODO testing for Qt applications
    pass
