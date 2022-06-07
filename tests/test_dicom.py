"""Testcases for DICOM format class."""

import numpy
import pytest

from pyseus import formats


dataset = formats.DICOM()  # pylint: disable=C0103


def test_dicom_load():
    """Test loading of DICOM files."""

    assert dataset.load("./tests/samples/sample.dcm/0000.DCM") is True
    assert isinstance(dataset.path, str)
    assert isinstance(dataset.scans, list)
    assert isinstance(dataset.scan, int)

    assert dataset.load_scan(0) is True
    assert isinstance(dataset.pixeldata, numpy.ndarray)
    assert isinstance(dataset.metadata, dict)

    assert isinstance(dataset.get_scan_thumbnail(0), numpy.ndarray)


def test_dicom_data():
    """Test access to data in a DICOM dataset."""

    assert isinstance(dataset.get_pixeldata(), numpy.ndarray)
    assert isinstance(dataset.get_metadata(), dict)
    assert isinstance(dataset.get_spacing(), list)
    assert isinstance(dataset.get_scale(), float)
    assert isinstance(dataset.get_units(), str)
    assert isinstance(dataset.get_orientation(), list)


def test_dicom_errors():
    """Test how DICOM handles failure conditions."""

    with pytest.raises(formats.LoadError) as error:
        dataset.load("./this/does/not/exist")
    assert error.type == formats.LoadError
