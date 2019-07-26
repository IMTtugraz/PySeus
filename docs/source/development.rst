Development
===========

asdf

Environment
-----------

0. If you don´t have the *virtualenv* package, get it with ``pip install virtualenv``.
1. Checkout the source code from `GitHub <>`.
2. In the source directory, run ``virtualenv pyseus`` to create a new virtual environment.
3. Active the virtual environment with ``pyseus\scripts\active``.
4. Run ``pip install -r requirements.txt`` to install all required packages.
5. After you are done, run ``deactivate`` to disable the virtual environment.

Documentation
-------------

The documentation for PySeus is created with `Sphinx <http://www.sphinx-doc.org>` using the `Read-the-Docs Theme <https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html>`.

You can setup these dependencies with ``cd docs`` and ``pip install requirements.txt``.
After making changes, run ``./make.bat html`` or ``make html`` and check the results under *docs/build/html*.
