Startup
=======

After installing, PySeus can be invoced in the **command line** via 
``pyseus [file]``. Alternatively, you can call PySeus directly from any 
python script:

.. code-block:: python

   import pyseus

   pyseus.load() # starts the PySeus GUI
   pyseus.load(data) # starts the GUI and loads [data]
   pyseus.load(path) # starts the GUI and loads [path]

Supported formats
-----------------

PySeus supports the following data formats:

**Python lists / arrays**: PySeus will accept any 2 or 3 dimensional data.

**Numpy ndArrays**: PySeus will accept ndArrays and `.npy` files. `.npz` files 
are currently *not* supported.

**HDF5 files**: PySeus will accept HDF5 files; if multiple datasets are 
present within a file, a selection dialog is displayed.

**DICOM files**: PySeus will accept `.DCM` files and attempt to load slices 
and scans form the base and parent directories. `DICOMDIR` files are currently 
*not* supported.

**NIfTI files**: Pyseus will accept NIFTI-2 `.nii` files; NIFTI-1 files and 
split files are currently *not* supported.

If you need to extend PySeus to use other file formats, see 
:ref:`Development / Formats<formats>`.

Data conventions
----------------

**Two dimensional data** is interpreted as a single slice.

**Three dimensional data** is interpreted as a set of slices, where the first 
dimension is the slice location.

**Four dimensional data** is interpreted as a set of scans, where the first 
dimension is the scan index.

**Five dimensional data** is interpreted as a set of scans, where the first 
two dimensions are merged for the scan index.
