"""Settings container for PySeus. Uses *settings.ini*."""

import os
from configparser import ConfigParser
from enum import IntEnum

settings = ConfigParser()  # pylint: disable=C0103
settings.read(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "./settings.ini")))

class DataType(IntEnum):
    """ Enumeration definition for data type of loaded file"""

    IMAGE = 0
    KSPACE = 1
    PHASE = 2

class ProcessType(IntEnum):
    """ Enumeration definition for processing type"""

    DENOISING = 0
    RECONSTRUCTION = 1

class ProcessSelDataType(IntEnum):
    """ Enumeration definition for the selection of the processed dataset"""

    SLICE_2D = 0
    WHOLE_SCAN_2D = 1
    WHOLE_SCAN_3D = 2


class ProcessRegType(IntEnum):
    """ Enumeration definition for regularisation type of processed dataset"""

    TV_L1 = 0 
    HUB_L2 = 1
    TV_L2 = 2
    TGV2_L2 = 3
