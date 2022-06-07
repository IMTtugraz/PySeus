"""Testcases for NIfTI format class."""

import numpy
import pytest

from pyseus import formats


dataset = formats.NIfTI()  # pylint: disable=C0103


def test_nifti_load():
    """Test loading of NIfTI files."""

    assert dataset.load("./tests/samples/sample.nii") is True
    assert isinstance(dataset.path, str)
    assert isinstance(dataset.scans, list)
    assert isinstance(dataset.scan, int)

    assert dataset.load_scan(0) is True
    # uses get_scan_pixeldata and get_scan_metadata
    assert isinstance(dataset.pixeldata, numpy.ndarray)
    assert isinstance(dataset.metadata, dict)

    assert isinstance(dataset.get_scan_thumbnail(0), numpy.ndarray)


def test_nifti_data():
    """Test access to data in a NIfTI dataset."""

    assert isinstance(dataset.get_pixeldata(), numpy.ndarray)
    assert isinstance(dataset.get_metadata(), dict)
    assert isinstance(dataset.get_spacing(), list)
    assert isinstance(dataset.get_scale(), float)
    assert isinstance(dataset.get_units(), str)
    assert isinstance(dataset.get_orientation(), list)


def test_nifti_errors():
    """Test how NIfTI handles failure conditions."""

    with pytest.raises(formats.LoadError) as error:
        dataset.load("./this/does/not/exist")
    assert error.type == formats.LoadError
