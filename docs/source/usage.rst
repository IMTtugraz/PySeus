Usage
=====

Installation
------------

Startup
-------

After installing, pyseus can be invoced in a number of ways:

**Standalone:** You can always start the PySeus GUI by running pyseus.pyw.

**Console:** You can start the Pyseus from the command line via ``pyseus [file]``.

If a single file contains more than one frame, you can specify a single frame to load by appending ``:[frame]`` to the file path.

If no file is provided, PySeus will attempt to interpret any data it recieves through stdin (pipe).

**Python:** You can call PySeus directly from any python script.

.. code-block:: python

   import pyseus

   pyseus.show() # starts the PySeus GUI
   pyseus.load(data) # starts the GUI and loads [data]
   pyseus.load_file(path) # starts the GUI and loads [path]

User Interface
--------------

+---------------------+------------+--------------------+
| *Menu*              | *Keyboard* | *Mouse*            |
+---------------------+------------+--------------------+
| File / Open         | Strg+O     |                    |
+---------------------+------------+--------------------+
| File / Exit         | Strg+Q     |                    |
+---------------------+------------+--------------------+
| About               | ?          |                    |
+---------------------+------------+--------------------+

Navigation
----------

*Left Mouse Btn + Drag* pans the image.

+---------------------+------------+--------------------+
| *Menu*              | *Keyboard* | *Mouse*            |
+---------------------+------------+--------------------+
| View / Zoom in      | \+         | Scroll up          |
+---------------------+------------+--------------------+
| View / Zoom out     | \-         | Scroll down        |
+---------------------+------------+--------------------+
| View / Fit          | #          |                    |
+---------------------+------------+--------------------+
| View / Reset        | 0          |                    |
+---------------------+------------+--------------------+

Windowing
---------

+---------------------+------------+--------------------+
| *Menu*              | *Keyboard* | *Mouse*            |
+---------------------+------------+--------------------+
| Window / Move down  | a          | Middle Btn + Left  |
+---------------------+------------+--------------------+
| Window / Move up    | d          | Middle Btn + Right |
+---------------------+------------+--------------------+
| Window / Shrink     | s          | Middle Btn + Down  |
+---------------------+------------+--------------------+
| Window / Widen      | w          | Middle Btn + Up    |
+---------------------+------------+--------------------+
| Window / Reset      | r          |                    |
+---------------------+------------+--------------------+

Eval-Functions
--------------

*Right Mouse Btn + Drag* creates a region of interest in the image. This region is marked by an orange outline.
