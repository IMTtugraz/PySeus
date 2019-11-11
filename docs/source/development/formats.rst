Formats
=======

.. automodule:: pyseus.formats

.. autoclass:: pyseus.formats.BaseFormat
   :members:
   :undoc-members:
   :private-members:
   :special-members:

Built-in Formats
----------------

Built-in formats follow the same structure as ``BaseFormat``.

.. autoclass:: pyseus.formats.Raw

.. autoclass:: pyseus.formats.H5

.. autoclass:: pyseus.formats.DICOM

Custom Formats
--------------

Just extend the *BaseFormat* Class and add the format class to the `pyseus.formats` list.
