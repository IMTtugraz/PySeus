.. _tools:

Tools
#####

.. automodule:: pyseus.tools

.. autoclass:: pyseus.tools.BaseTool
  :members:

Built-in Tools
==============

Area Tool
---------

.. autoclass:: pyseus.tools.AreaTool
  :members: roi

Line Tool
---------

.. autoclass:: pyseus.tools.LineTool
   :members: line

.. autoclass:: pyseus.tools.line.LineToolWindow
   :members: load_data

Custom Tools
============

Just extend the *BaseTool* class and add the class to the *PySeus.tools* list.
