.. _formats:

Formats
=======

.. automodule:: pyseus.formats

.. autoclass:: pyseus.formats.BaseFormat
  :members:

Built-in Formats
----------------

Built-in formats follow the same structure as ``BaseFormat``.

.. autoclass:: pyseus.formats.Raw

.. autoclass:: pyseus.formats.NumPy

.. autoclass:: pyseus.formats.H5

.. autoclass:: pyseus.formats.DICOM

.. autoclass:: pyseus.formats.NIfTI

Custom Formats
--------------

Just extend the *BaseFormat* Class and add the format class to the
`pyseus.formats` list.
