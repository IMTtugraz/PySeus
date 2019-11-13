"""...
"""

import numpy
import os

from context import pyseus, app


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
