"""...
"""

import numpy
import pytest

from context import pyseus
from pyseus import formats


dataset = formats.NIfTI()

def test_load():
    assert dataset.load("./samples/sample.nii") == True
    assert isinstance(dataset.path, str)
    assert isinstance(dataset.scans, list)
    assert isinstance(dataset.scan, int)

    assert dataset.load_scan(0) == True
    # uses get_scan_pixeldata and get_scan_metadata
    assert isinstance(dataset.pixeldata, numpy.ndarray)
    assert isinstance(dataset.metadata, dict)

    assert isinstance(dataset.get_scan_thumbnail(0), numpy.ndarray)

def test_data():
    assert isinstance(dataset.get_pixeldata(), numpy.ndarray)
    assert isinstance(dataset.get_metadata(), dict)
    assert isinstance(dataset.get_spacing(), list)
    assert isinstance(dataset.get_scale(), float)
    assert isinstance(dataset.get_units(), str)
    assert isinstance(dataset.get_orientation(), int)

# def test_errors():
#     with pytest.raises(formats.LoadError) as error:
#        dataset.load("./this/does/not/exist")
#     assert error.type == formats.LoadError
