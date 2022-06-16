Startup
=======

After installing, PySeus can be invoced in the command line via 
``pyseus [file]``. Alternatively, you can call PySeus directly from any 
python script:

.. code-block:: python

   import pyseus
   from pyseus.settings import DataType


   pyseus.load()  # starts the PySeus GUI in image mode
   pyseus.load(data)  # starts the GUI and loads [data] in image mode (standard)
   pyseus.load(path)  # starts the GUI and loads [path] in image mode (standard)
   pyseus.load(data, data_type=DataType.IMAGE)  # starts the GUI and loads [data] in image mode
   pyseus.load(data, data_type=DataType.KSPACE)  # starts the GUI and loads [data] in kspace mode
   pyseus.load(path, data_type=DataType.KSPACE)  # starts the GUI and loads [path] in kspace mode

Supported formats
-----------------

PySeus supports the following data formats:

**Python lists / arrays**: PySeus will accept any 2 to 5 dimensional data.

**Numpy nd-arrays**: PySeus will accept nd-arrays and *.npy* files. *.npz* files 
are currently *not* supported.

**HDF5 files**: PySeus will accept HDF5 files; if multiple datasets are 
present within a file, a selection dialog is displayed. Additionally to image data
HDF5 also accepts kspace data with three datasets. These three datasets are the real and the imaginary
part of the kspace and the corresponding coil sensitivities. 

**DICOM files**: PySeus will accept *.DCM* files and attempt to load slices 
and scans form the base and parent directories. *DICOMDIR* files are currently 
*not* supported.

**NIfTI files**: Pyseus will accept NIfTI-1 and NIfTI-2 *.nii* files.

If you need to extend PySeus to use other file formats, see 
`Development / Formats <../development/formats.html>`_.

Data conventions
----------------

Some formats, like NumPy and HDF5 allow for a lot of freedom in how the data 
is structured; in these cases, PySeus interprets data like this:

**Image data:**

*Two dimensional data* is interpreted as a single slice, the first dimension 
being the y-axis.

*Three dimensional data* is interpreted as a set of slices, where the first 
dimension is the slice index.

*Four dimensional data* is interpreted as a set of scans, where the first 
dimension is the scan index.

*Five dimensional data* is interpreted as a set of scans, where the first 
two dimensions are merged for the scan index.

**Kspace data:**

*Three dimensional data* is interpreted as a single slice for every coil, the first 
dimension being the coil index and the second being the y-axis.

*Four dimensional data* is interpreted as a set of slices for every coil, where the first 
dimension is the coil index and the second the slice index.

*Five dimensional data* is interpreted as a set of scans for every coil, where the first 
dimension is the coil index and the second is the scan index.
