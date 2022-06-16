"""Testcases for NumPy format class."""

import numpy
import pytest

from context import pyseus
from pyseus import formats


dataset = formats.NumPy()


def test_numpy_load():
    """Test loading of NumPy files."""

    assert dataset.load("./tests/samples/sample.npy") is True
    assert isinstance(dataset.path, str)
    assert isinstance(dataset.scans, list)
    assert isinstance(dataset.scan, int)

    assert dataset.load_scan(0) is True
    assert isinstance(dataset.pixeldata, numpy.ndarray)
    assert isinstance(dataset.metadata, dict)

    assert isinstance(dataset.get_scan_thumbnail(0), numpy.ndarray)


def test_numpy_data():
    """Test access to data in a NumPy dataset."""

    assert isinstance(dataset.get_pixeldata(), numpy.ndarray)
    assert isinstance(dataset.get_metadata(), dict)
    assert isinstance(dataset.get_spacing(), list)
    assert isinstance(dataset.get_scale(), float)
    assert isinstance(dataset.get_units(), str)
    assert isinstance(dataset.get_orientation(), list)


def test_numpy_errors():
    """Test how NumPy handles failure conditions."""

    with pytest.raises(formats.LoadError) as error:
        dataset.load("./this/does/not/exist")
    assert error.type == formats.LoadError
