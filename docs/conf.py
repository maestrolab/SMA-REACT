# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os 
import sys
sys.path.insert(0,os.path.abspath(".."))


project = 'SMA-REACT'
copyright = '2024, Patrick Walgren and Jacob Mingear'
author = 'Patrick Walgren and Jacob Mingear'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    'sphinxcontrib.bibtex',
    "sphinx.ext.autosectionlabel",
    ]

# Make sure the target is unique for the labels
autosectionlabel_prefix_document = True

bibtex_bibfiles = ['SMA-REACT.bib']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
