Startup
=======

After installing, PySeus can be invoced in the **command line** via ``pyseus [file]``.

Alternatively, you can call PySeus directly from any python script:

.. code-block:: python

   import pyseus

   pyseus.load() # starts the PySeus GUI
   pyseus.load(data) # starts the GUI and loads [data]
   pyseus.load(path) # starts the GUI and loads [path]

User Interface
--------------

Image: Thumbanail bar, Viewport, Sidebar (File Info, Metadata, Console)


Supported formats
-----------------

PySeus support the following data formats:

**Python lists**: PySeus will accept any 2 or 3 dimensional python list.

**Numpy ndArrays**: PySeus will accept ndArrays and `.npy` files. `.npz` files are currently *not* supported.

**HDF5 files**: PySeus will accept HDF5 files; if multiple datasets are present within a file, a selection dialog is displayed.

**DICOM files**: PySeus will accept `.DCM` files and attempt to load slices and scans form the base and parent directories. DICOM directory files are currently *not* supported.

If you need to extend PySeus with custom formats, see :ref:`formats`.

Data conventions
----------------

Two dimensional data is interpreted as a single slice.

Three dimensional data is interpreted as a set of slices, where the first dimension is the slice location.

Four dimensional data ist interpreted as a set of scans, where the first dimension is the scan index.

Fife dimensional data is interpreted as a set of scans, where the first two dimensions are merged for the scan index.

