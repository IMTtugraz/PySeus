.. _formats:

Formats
=======

.. automodule:: pyseus.formats

The BaseFormat Class
--------------------

.. autoclass:: pyseus.formats.BaseFormat
   :members:

Built-in Formats
----------------

.. autoclass:: pyseus.formats.Raw

.. autoclass:: pyseus.formats.NumPy

.. autoclass:: pyseus.formats.H5

.. autoclass:: pyseus.formats.DICOM

.. autoclass:: pyseus.formats.NIfTI

Custom Formats
--------------

Just extend the *BaseFormat* Class and add the format class to the
*PySeus.formats* list.
