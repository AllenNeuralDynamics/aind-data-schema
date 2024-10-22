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
from aind_data_schema.core import (  # A temporary workaround to fix NameError when building Sphinx
    acquisition,
    data_description,
    instrument,
    metadata,
    procedures,
    processing,
    rig,
    session,
    subject,
    quality_control
)

dummy_object = [
    acquisition,
    data_description,
    instrument,
    metadata,
    procedures,
    processing,
    rig,
    session,
    subject,
    quality_control
]  # A temporary workaround to bypass "Imported but unused" error

INSTITUTE_NAME = "Allen Institute for Neural Dynamics"

current_year = date.today().year

this_file_path = abspath(__file__)
project = Path(dirname(dirname(dirname(this_file_path)))).name
project_copyright = f"{current_year}, {INSTITUTE_NAME}"
author = INSTITUTE_NAME
release = package_version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx.ext.napoleon",
    "sphinx_jinja",
    "myst_parser",
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

DIAGRAM_URL = os.getenv("DIAGRAM_URL")
diagrams_list = [
    "acquisition",
    "data_description",
    "instrument",
    "metadata.nd",
    "procedures",
    "processing",
    "rig",
    "session",
    "subject",
    "quality_control",
]
rst_epilog = ""
for diagram in diagrams_list:
    rst_epilog = (
        rst_epilog
        + """
.. |{diagram}| image:: {url_base}/{diagram}.svg
""".format(
            diagram=diagram, url_base=DIAGRAM_URL
        )
    )
