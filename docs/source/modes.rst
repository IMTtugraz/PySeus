Modes
=====

.. automodule:: pyseus.modes

.. autoclass:: pyseus.modes.BaseMode
   :members:
   :undoc-members:

Built-in Modes
--------------

.. autoclass:: pyseus.modes.Amplitude

.. autoclass:: pyseus.modes.Phase

Custom Modes
------------

Just extend the *BaseMode* Class and register the new mode with 
``app().register_mode()`` (coming soon).
