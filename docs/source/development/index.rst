Development
===========

PySeus was envisioned as a basis for more advanced tools to be developed on 
top of it. This section of the documentation is aimed at providing a 
starting point for future developers.

Virtual Environment
-------------------

It is recommended that you use a virtual Python environment (like the 
`venv module <https://docs.python.org/3/library/venv.html>`_ to isolate 
PySeus from other Python projects.

Testing
-------

For unit testing, `PyTest <https://pypi.org/project/pytest/>`_ is used. 
Testcases are defined under *tests/*. To run all testcases, run ``pytest``
from the root directory.

When changes are pushed to github, all testcases are run on
`Travis CI <https://travis-ci.org/calmer/PySEUS>`_.


Coding style
------------

The coding style follows `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_
specifications, except where close coupling with PySide2 makes this impossible
or where it would result in code that is harder to read or understand. For 
example, when a member function overrides the function of a Qt parent
class, the PySide coding style is used.

Compliance with the coding style can be checked with
`flake8 <https://pypi.org/project/flake8/>`_ by running ``flake8`` from the 
root directory. The *flake8.log* file in the root directory contains a list of 
current problems with the coding style. To update it, run 
``flake8 > flake8.log``.

When changes are pushed to github, compliance with the coding style is also
checked on `Travis CI <https://travis-ci.org/calmer/PySEUS>`_, but problems 
with the coding style do not lead to a failed build.


Code Quality
------------

The ensure code quiality, `Pylint <https://www.pylint.org/>`_ is used by
running ``pylint pyseus`` or ``python -m pylint pyseus`` 
from the root directory. The *pylint.log* file in the root directory contains 
a list of current code quality problems. To update it, run 
``pylint pyseus > pylint.log`` or ``python -m pylint pyseus > pylint.log``.

When changes are pushed to github, code quality is also checked on 
`Travis CI <https://travis-ci.org/calmer/PySEUS>`_, but problems do not lead 
to a failed build.


Documentation
-------------

The documentation for PySeus is created with
`Sphinx <http://www.sphinx-doc.org>`_ using the `Read-the-Docs Theme 
<https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html>`_. The 
documentation files are stored under *docs/*. After making changes, run
``./make.bat html`` (Windows) or ``make html`` from the *docs/* directory;
the new files are placed under *docs/build/html*.

When changes are pushed to github, the documentation is built automatically
and published to `Read-the-Docs <https://pyseus.readthedocs.io/en/latest/>`_;
you can check whether a built was successful `here 
<https://readthedocs.org/projects/pyseus/builds/>`_.
