"""Sphinx configuration for PiWardrive documentation."""

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

project = 'PiWardrive'
author = 'PiWardrive contributors'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.graphviz',
    'sphinxcontrib.mermaid',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
