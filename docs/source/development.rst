Development
===========

...

Setting up the environment
--------------------------

0. If you don´t have the *virtualenv* package, get it with ``pip install virtualenv``.
1. Checkout the source code from `GitHub <>`.
2. In the source directory, run ``virtualenv pyseus`` to create a new virtual environment.
3. Active the virtual environment with ``pyseus\scripts\active``.
4. Run ``pip install -r requirements.txt`` to install all required packages.
5. After you are done, run ``deactivate`` to disable the virtual environment.


Overview
--------

Class Overview
Control flow for loading


Updating the documentation
--------------------------

The documentation for PySeus is created with `Sphinx <http://www.sphinx-doc.org>` using the `Read-the-Docs Theme <https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html>`.

These dependencies are setup if you run ``pip install requirements.txt`` from the root directory.
After making changes, run ``./make.bat html`` or ``make html``; the new files are under *docs/build/html*.
