"""Configuration file for the Sphinx documentation builder."""
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
from datetime import date

# -- Path Setup --------------------------------------------------------------
from os.path import abspath, dirname
from pathlib import Path

from aind_data_schema import __version__ as package_version

INSTITUTE_NAME = "Allen Institute for Neural Dynamics"

current_year = date.today().year

this_file_path = abspath(__file__)
project = Path(dirname(dirname(dirname(this_file_path)))).name
project_copyright = f"{current_year}, {INSTITUTE_NAME}"
author = INSTITUTE_NAME
release = package_version
diagrams_path = Path(dirname(this_file_path)) / "_static" / "diagrams"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_jinja",
]
templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_title = "aind-data-schema"
html_favicon = "_static/favicon.ico"
html_theme_options = {
    "light_logo": "light-logo.svg",
    "dark_logo": "dark-logo.svg",
}

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

jinja_contexts = {
    "first_ctx": {
        "diagrams": dict(
            [(str(f).replace(".png", ""), f"_static/diagrams/{str(f)}") for f in os.listdir(diagrams_path)]
        )
    }
}
