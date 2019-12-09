Interface
#########

.. automodule:: pyseus.ui

Styling can be controlled in the Qt stylesheet under `ui/style_dark.qss`.

Main Window
===========

.. autoclass:: pyseus.ui.MainWindow
  :members: add_menu_item, setup_menu, app, console, info, meta, thumbs,
    view, show_status, resizeEvent

.. fails when all members are to be documented (works, when class has no
  private members ???)

View Widget
===========

.. autoclass:: pyseus.ui.ViewWidget
  :members:

Thumbnails Widget
=================

.. autoclass:: pyseus.ui.ThumbsWidget
  :members:

Sidebar Widgets
===============

.. autoclass:: pyseus.ui.main.SidebarHeading

File Info Widget
----------------

.. autoclass:: pyseus.ui.InfoWidget
  :members:

Metadata Widget
---------------

.. autoclass:: pyseus.ui.MetaWidget
  :members:

.. autoclass:: pyseus.ui.meta.MetaWindow
  :members:

Console Widget
--------------

.. autoclass:: pyseus.ui.ConsoleWidget
  :members:
