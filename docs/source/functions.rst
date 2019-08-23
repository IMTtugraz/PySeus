.. _functions:

Functions
=========

.. automodule:: pyseus.functions

.. autoclass:: pyseus.functions.BaseFct
   :members:
   :undoc-members:

Built-in Functions
------------------

.. autoclass:: pyseus.functions.RoIFct

.. autoclass:: pyseus.functions.StatsFct

Custom functions
----------------

Just extend the *BaseFct* Class and register the new function with 
``app().register_function()`` (coming soon).
