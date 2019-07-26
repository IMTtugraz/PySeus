Formats
=======

.. automodule:: pyseus.formats

.. autoclass:: pyseus.formats.BaseFormat
   :members:
   :undoc-members:

Built-in Formats
----------------

Built-in formats follow the same structure as ``BaseFormat``.
Due to differences in the formats, they rely on further helper functions.

.. autoclass:: pyseus.formats.Raw

.. autoclass:: pyseus.formats.H5

.. autoclass:: pyseus.formats.DICOM

Custom Formats
--------------

Just extend the *BaseFormat* Class and register the new format with 
``app().register_format()`` (coming soon).
