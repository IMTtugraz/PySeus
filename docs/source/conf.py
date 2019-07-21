# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
print(__file__ + '../pyseus')
sys.path.insert(0, os.path.abspath('../../'))


# -- Project information -----------------------------------------------------

project = 'PySeus'
author = 'Christoph Almer'
copyright = '2019, Christoph Almer'
version = '0.1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'classic'
html_theme_options = {
    'rightsidebar': 'false',
    'stickysidebar': 'true',

    'footerbgcolor': '#eee',
    'footertextcolor': '#aaa',

    'sidebarbgcolor': '#ddd',
    'sidebartextcolor': '#333',
    'sidebarlinkcolor': '#e4154b',

    'relbarbgcolor': '#ccc',
    'relbartextcolor': '#333',
    'relbarlinkcolor': '#e4154b',

    'bgcolor': '#fff',
    'textcolor': '#111',
    'linkcolor': '#e4154b',
    'visitedlinkcolor': '#e4154b',

    'headbgcolor': '#eee',
    'headtextcolor': '#e4154b',
    'headlinkcolor': '#111',

    'codebgcolor': 'green',
    'codetextcolor': '#111',

    'bodyfont': 'Arial, sans-serif',
    'headfont': 'Arial, sans-serif',
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
