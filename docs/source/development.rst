Development
===========

...


Environment
-----------

0. If you don´t have the *virtualenv* package, get it with ``pip install virtualenv``.
1. Checkout the source code from `GitHub <>`.
2. In the source directory, run ``virtualenv pyseus`` to create a new virtual environment.
3. Active the virtual environment with ``pyseus\scripts\active``.
4. Run ``pip install -r requirements.txt`` to install all required packages.
5. After you are done, run ``deactivate`` to disable the virtual environment.


Testing
-------

For unit and integration testing, `PyTest <https://pypi.org/project/pytest/>` and `Mock <https://pypi.org/project/mock/>` are used. Both dependencies are setup when you run ``pip install requirements.txt`` from the root directory.

All testcases are defined under *tests/*. To run all testcases, run ``pytest`` from the *tests/* directory.

When changes are pushed to github, all testcases are run by `Travis CI <https://travis-ci.org/>`; you can check whether a built was successful on https://travis-ci.org/calmer/PySEUS.


Coding style
------------

The coding style follows PEP8 specifications, except where close coupling with PySide 2 would lead to code that is harder to understand.
For example, when extending a QtWidget, the coding style from PySide is used.

The coding style can be checked with `flake8 <https://pypi.org/project/flake8/>`, which is setup when you run ``pip install requirements.txt`` from the root directory.
Just run ``flake8`` from the root directory.

Coding style is also checked with `Travis CI <https://travis-ci.org/>`, but problems with the coding style do not lead to a failed build.


Documentation
-------------

The documentation for PySeus is created with `Sphinx <http://www.sphinx-doc.org>` using the `Read-the-Docs Theme <https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html>`.
Both dependencies are setup when you run ``pip install requirements.txt`` from the root directory.

All documentation files are stored under *docs/*. After making changes, run ``./make.bat html`` (Windows) or ``make html`` from the *docs/* directory; the new files are placed under *docs/build/html*.

When changes are pushed to github, the documentation is built automatically and published under https://pyseus.readthedocs.io/en/latest/; you can check whether a built was successful on https://readthedocs.org/projects/pyseus/builds/.


Overview
--------

Class Overview
Control flow for loading
