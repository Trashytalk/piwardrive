"""Sphinx configuration for building the project documentation."""

import os
import sys

project = os.getenv("PW_DOC_PROJECT", "PiWardrive")
author = os.getenv("PW_DOC_AUTHOR", "TRASHYTALK")
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.graphviz",
    "sphinxcontrib.mermaid",
]
html_theme = os.getenv("PW_DOC_THEME", "alabaster")
html_title = project
sys.path.insert(0, os.path.abspath(".."))

__all__ = [
    "project",
    "author",
    "extensions",
    "html_theme",
    "html_title",
]
