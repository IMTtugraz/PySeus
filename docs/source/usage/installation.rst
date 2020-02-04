Installation
============

You can download the latest version from 
`GitHub <https://github.com/calmer/PySEUS>`_.

From the downloaded directory, run ``python setup.py install`` to install 
PySeus. Running ``pip uninstall pyseus`` will remove all installed files.

Requirements
------------

PySeus requires `Python 3 <https://www.python.org/download/releases/3.0/>`_ 
and works on Windows, Linux and MacOS.

The following **dependencies** will be installed with PySeus:

- PySide2
- numpy
- opencv-python
- h5py
- pydicom
- nibabel
- natsort

Optional Dependencies
---------------------

**GDCM** (`Grass Roots DICOM <https://sourceforge.net/projects/gdcm>`_) is 
required for DICOM files using certain encodings.

If *conda* is available on your system, you can simply run 
``conda install -c conda-forge -y gdcm``. On Ubuntu/Debian you can run 
``sudo apt install python3-gdcm`` or `build GDCM 
from source <http://gdcm.sourceforge.net/wiki/index.php/Compilation>`_. 
For Windows systems, you can get the latest installer from their 
`GitHub Mirror <https://github.com/malaterre/GDCM/releases/>`_.
