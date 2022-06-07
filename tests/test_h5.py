"""Testcases for H5 format class."""

import numpy
import pytest

from context import pyseus
from pyseus import formats
from pyseus.settings import DataType


dataset = formats.H5()


def test_h5_load():
    """Test loading of H5 files."""

    assert dataset.load("./tests/samples/sample.h5", data_type=DataType.IMAGE) is True
    assert isinstance(dataset.path, str)
    assert isinstance(dataset.scans, list)
    assert isinstance(dataset.scan, int)

    assert dataset.load_scan(0) is True
    # uses get_scan_pixeldata and get_scan_metadata
    assert isinstance(dataset.pixeldata, numpy.ndarray)
    assert isinstance(dataset.metadata, dict)

    assert isinstance(dataset.get_scan_thumbnail(0), numpy.ndarray)


def test_h5_data():
    """Test access to data in a H5 dataset."""

    assert isinstance(dataset.get_pixeldata(), numpy.ndarray)
    assert isinstance(dataset.get_metadata(), dict)
    assert isinstance(dataset.get_spacing(), list)
    assert isinstance(dataset.get_scale(), float)
    assert isinstance(dataset.get_units(), str)
    assert isinstance(dataset.get_orientation(), list)


def test_h5_errors():
    """Test how H5 handles failure conditions."""

    with pytest.raises(formats.LoadError) as error:
        dataset.load("./this/does/not/exist", data_type=DataType.IMAGE)
    assert error.type == formats.LoadError
