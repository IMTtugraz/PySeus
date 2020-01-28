Display Modes
=============

Display modes are responsible for the translation of values to color, provide 
functions like windowing and implement helper functions for displaying the 
results.

.. autoclass:: pyseus.modes.BaseMode
   :members:

Built-in Display Modes
----------------------

.. autoclass:: pyseus.modes.Grayscale
   :members: source, set_source

Built-in Display Modes
----------------------

Just extend the *BaseMode* class and add the mode class to the
*PySeus.modes* list.
