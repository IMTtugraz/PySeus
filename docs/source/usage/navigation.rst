Navigation
##########

Depending on whether you are viewing 2D, 3D or higher dimensional data, 
different options to navigate that data are available.

Exploring a Dataset
===================

If the current dataset has more than 3 dimensions, the first dimension(s) will 
be interpreted as a list of 3D scans. These will be displayed in the thumb bar 
on the left and clicking a thumbnail will load the corresponding scan.

+-------------------------+--------------+----------------------+
| **Menu**                | **Keyboard** | **Mouse**            |
+-------------------------+--------------+----------------------+
| Explore / Next Scan     | Alt + PgUp   | Alt + Wheel Down     |
+-------------------------+--------------+----------------------+
| Explore / Previous Scan | Alt + PgDown | Alt + Wheel Up       |
+-------------------------+--------------+----------------------+

For 3D data, the first dimension will be interpreted as a list of slices.

+--------------------------+--------------+----------------------+
| **Menu**                 | **Keyboard** | **Mouse**            |
+--------------------------+--------------+----------------------+
| Explore / Next Slice     | PgUp         | Wheel Down           |
+--------------------------+--------------+----------------------+
| Explore / Previous Slice | PgDown       | Wheel Up             |
+--------------------------+--------------+----------------------+

Rotate & Flip
-------------

The current scan can be rotated around the three principal axes. The axes are 
always relative to the viewport and rotation will be done in pi/2 increments 
counter clockwise.

+--------------------------+--------------+----------------------+
| **Menu**                 | **Keyboard** | **Mouse**            |
+--------------------------+--------------+----------------------+
| Explore / Rotate z       | Strg + E     |                      |
+--------------------------+--------------+----------------------+
| Explore / Rotate x       | Strg + R     |                      |
+--------------------------+--------------+----------------------+
| Explore / Rotate y       | Strg + T     |                      |
+--------------------------+--------------+----------------------+
| Explore / Reset Scan     | Strg + Z     |                      |
+--------------------------+--------------+----------------------+

Additionally, the current scan can be flipped in the three principal axes. Again, axes 
are relative to the viewport.

+--------------------------+--------------+----------------------+
| **Menu**                 | **Keyboard** | **Mouse**            |
+--------------------------+--------------+----------------------+
| Explore / Flip x (L-R)   | Strg + D     |                      |
+--------------------------+--------------+----------------------+
| Explore / Flip y (U-D)   | Strg + F     |                      |
+--------------------------+--------------+----------------------+
| Explore / Flip z (F-B)   | Strg + G     |                      |
+--------------------------+--------------+----------------------+
| Explore / Reset Scan     | Strg + Z     |                      |
+--------------------------+--------------+----------------------+

Viewing a Slice
===============

PySeus can visualize either the amplitude or phase part of data.

+---------------------+--------------+----------------------+
| **Menu**            | **Keyboard** | **Mouse**            |
+---------------------+--------------+----------------------+
| View / Amplitude    | F1           |                      |
+---------------------+--------------+----------------------+
| View / Phase        | F2           |                      |
+---------------------+--------------+----------------------+

Zoom & Pan
----------

By default, the entire image will be visible in the viewport.
The image can be zoomed in several ways, and panned by holding *RMB* while 
moving the mouse.

+---------------------+--------------+----------------------+
| **Menu**            | **Keyboard** | **Mouse**            |
+---------------------+--------------+----------------------+
| View / Zoom in      | \+           | Strg + Wheel up      |
+---------------------+--------------+----------------------+
| View / Zoom out     | \-           | Strg + Wheel down    |
+---------------------+--------------+----------------------+
| View / Fit          | #            |                      |
+---------------------+--------------+----------------------+
| View / Reset        | 0            |                      |
+---------------------+--------------+----------------------+

Windowing
---------

Windowing controls the translation of values to color. The following example 
are based on the default translation to grayscale:

- *Lowering* or *raising* the window results in a darker or lighter image 
  respectively.
- *Shrinking* or *widening* the window results in higher or lower contrast 
  respectively.
- *Reseting* the window will use the default options of covering all values 
  present in the data.

+----------------------+--------------+--------------------+
| **Menu**             | **Keyboard** | **Mouse**          |
+----------------------+--------------+--------------------+
| View / Lower Window  | Q            | MMB + Right        |
+----------------------+--------------+--------------------+
| View / Raise Window  | W            | MMB + Left         |
+----------------------+--------------+--------------------+
| View / Shrink Window | A            | MMB + Down         |
+----------------------+--------------+--------------------+
| View / Widen Window  | S            | MMB + Up           |
+----------------------+--------------+--------------------+
| View / Reset Window  | D            |                    |
+----------------------+--------------+--------------------+
