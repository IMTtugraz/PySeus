Evaluating
==========

PySeus provides a simple way to evaluate image data via **tools**.

Area Tool
---------

To evaluate a region-of-interest in the current slice, select *Area Eval* from 
the *Evaluate* Menu.

Dragging while holding *Ctrl + LMB* will create a region-of-interest, marked 
by a red line, and print basic statistical information to the console.

Line Tool
---------

To evaluate the current dataset along a line in the current slice, select 
*Line Eval* from the *Evaluate* menu.

Dragging while holding *Ctrl + LMB* will create a line, marked in green and 
display the values along the line in a chart.

Custom Tools
------------

If you need to extend PySeus with custom tools, see 
`Development / Tools <../development/tools.html>`_.
