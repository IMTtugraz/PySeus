"""Testcases for Raw format class."""

import numpy
import pytest

from context import pyseus
from pyseus import formats


dataset = formats.Raw()


def test_raw_load():
    """Test loading of Raw data."""

    data = numpy.load("./tests/samples/sample.npy")
    assert dataset.load(data) is True
    assert isinstance(dataset.path, str)
    assert isinstance(dataset.scans, list)
    assert isinstance(dataset.scan, int)

    assert dataset.load_scan(0) is True
    assert isinstance(dataset.pixeldata, numpy.ndarray)
    assert isinstance(dataset.metadata, dict)

    assert isinstance(dataset.get_scan_thumbnail(0), numpy.ndarray)


def test_raw_data():
    """Test access to data in a Raw dataset."""

    assert isinstance(dataset.get_pixeldata(), numpy.ndarray)
    assert isinstance(dataset.get_metadata(), dict)
    assert isinstance(dataset.get_spacing(), list)
    assert isinstance(dataset.get_scale(), float)
    assert isinstance(dataset.get_units(), str)
    assert isinstance(dataset.get_orientation(), list)


def test_raw_errors():
    """Test how Raw handles failure conditions."""

    with pytest.raises(formats.LoadError) as error:
        data = ["invalid", "data"]
        dataset.load(data)
    assert error.type == formats.LoadError
