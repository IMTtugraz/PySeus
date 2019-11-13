"""...
"""

import numpy
import os

from context import pyseus


app = pyseus.PySeus(False)

def test_raw():
    format = pyseus.formats.Raw(app)

    path, scans, current = format.load_file("./samples/sample.npy")
    assert isinstance(path, str)  # path
    assert isinstance(scans, list)  # scan list
    assert isinstance(current, int)  # current scan

    scan_data = format.load_scan(scans[0])
    assert isinstance(scan_data, numpy.ndarray)

    metadata = format.load_metadata(scans[0])
    assert isinstance(metadata, dict)

def test_h5():
    format = pyseus.formats.H5(app)

    path, scans, current = format.load_file("./samples/sample.h5")
    assert isinstance(path, str)  # path
    assert isinstance(scans, list)  # scan list
    assert isinstance(current, int)  # current scan

    scan_data = format.load_scan(scans[0])
    assert isinstance(scan_data, numpy.ndarray)

    metadata = format.load_metadata(scans[0])
    assert isinstance(metadata, dict)

def test_dicom():
    format = pyseus.formats.DICOM(app)

    path, scans, current = format.load_file("./samples/sample.dcm/0000.DCM")
    assert isinstance(path, str)  # path
    assert isinstance(scans, list)  # scan list
    assert isinstance(current, int)  # current scan

    scan_data = format.load_scan(scans[0])
    assert isinstance(scan_data, numpy.ndarray)

    metadata = format.load_metadata(scans[0])
    assert isinstance(metadata, dict)

def test_nifti():
    format = pyseus.formats.NIfTI(app)

    path, scans, current = format.load_file("./samples/sample.nii")
    assert isinstance(path, str)  # path
    assert isinstance(scans, list)  # scan list
    assert isinstance(current, int)  # current scan

    scan_data = format.load_scan(scans[0])
    assert isinstance(scan_data, numpy.ndarray)

    metadata = format.load_metadata(scans[0])
    assert isinstance(metadata, dict)
