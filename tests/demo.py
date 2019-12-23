"""Various demos for PySeus using sample data."""

# flake8: noqa
# pylint: skip-file

from context import pyseus


def demo():
    pyseus.load()

def demo_numpy():
    pyseus.load("./samples/sample.npy")

def demo_data():
    import numpy
    data = numpy.load("./samples/sample.npy")
    pyseus.load(data)

def demo_h5():
    pyseus.load("./samples/sample.h5")

def demo_h5_2():
    pyseus.load("C:/temp/sample_huge.h5")

def demo_dicom():
    pyseus.load("./samples/sample.dcm/0000.dcm")

def demo_dicom_2():
    pyseus.load("C:/temp/sample_huge.dcm/RAVE_longRF_1deg/"
                "VFA_Prob010201030001000100010001.DCM")

def demo_nifti():
    pyseus.load("./samples/sample.nii")

def demo_nifti_2():
    pyseus.load("C:/temp/sample_huge.nii")


if __name__ == "__main__":
    demo_dicom_2()
