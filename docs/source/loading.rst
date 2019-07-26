Loading Data
============

After installing, PySeus can be invoced in a number of ways:

**Standalone:** You can always start the PySeus GUI by running pyseus.pyw.

**Console:** You can start the Pyseus from the command line via ``pyseus [file]``.

If a single file contains more than one frame, you can specify a single frame to load by appending ``:[frame]`` to the file path.

If no file is provided, PySeus will attempt to interpret any data it recieves through stdin.

**Python:** You can call PySeus directly from any python script.

.. code-block:: python

   import pyseus

   pyseus.load() # starts the PySeus GUI
   pyseus.load(data) # starts the GUI and loads [data]
   pyseus.load(path) # starts the GUI and loads [path]

Frame Selection (Coming soon)
-----------------------------

If a file or data set contains more than one frame, the frame selection dialog will appear.


