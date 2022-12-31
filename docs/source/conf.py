#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Configuration file for the Sphinx documentation builder."""

import os
import sys
from importlib import import_module

import sktime

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

ON_READTHEDOCS = os.environ.get("READTHEDOCS") == "True"
if not ON_READTHEDOCS:
    sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
project = "sktime"
copyright = "2019 - 2021 (BSD-3-Clause License)"
author = "sktime developers"

# The full version, including alpha/beta/rc tags
CURRENT_VERSION = f"v{sktime.__version__}"

# If on readthedocs, and we're building the latest version, update tag to generate
# correct links in notebooks
if ON_READTHEDOCS:
    READTHEDOCS_VERSION = os.environ.get("READTHEDOCS_VERSION")
    if READTHEDOCS_VERSION == "latest":
        CURRENT_VERSION = "main"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",  # link to GitHub source code via linkcode_resolve()
    "nbsphinx",  # integrates example notebooks
    "sphinx_gallery.load_style",
    "myst_parser",
    "sphinx_design",
    "sphinx_issues",
]

# Recommended by sphinx_design when using the MyST Parser
myst_enable_extensions = ["colon_fence"]

# Notebook thumbnails
nbsphinx_thumbnails = {
    "examples/02_classification": "examples/img/tsc.png",
}

# Use bootstrap CSS from theme.
panels_add_bootstrap_css = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# The main toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    ".ipynb_checkpoints",
    "Thumbs.db",
    ".DS_Store",
]

add_module_names = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# see http://stackoverflow.com/q/12206334/562769
numpydoc_show_class_members = True
# this is needed for some reason...
# see https://github.com/numpy/numpydoc/issues/69
numpydoc_class_members_toctree = False

numpydoc_validation_checks = {"all"}

# generate autosummary even if no references
autosummary_generate = True

# Members and inherited-members default to showing methods and attributes from a
# class or those inherited.
# Member-order orders the documentation in the order of how the members are defined in
# the source code.
autodoc_default_options = {
    "members": True,
    "inherited-members": True,
    "member-order": "bysource",
}

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# When building HTML using the sphinx.ext.mathjax (enabled by default),
# Myst-Parser injects the tex2jax_ignore (MathJax v2) and mathjax_ignore (MathJax v3)
# classes in to the top-level section of each MyST document, and adds some default
# configuration. This ensures that MathJax processes only math, identified by the
# dollarmath and amsmath extensions, or specified in math directives. We here silence
# the corresponding warning that this override happens.
suppress_warnings = ["myst.mathjax"]

# Link to GitHub repo for github_issues extension
issues_github_path = "sktime/sktime"


def linkcode_resolve(domain, info):
    """Return URL to source code corresponding.

    Parameters
    ----------
    domain : str
    info : dict

    Returns
    -------
    url : str
    """

    def find_source():
        # try to find the file and line number, based on code from numpy:
        # https://github.com/numpy/numpy/blob/main/doc/source/conf.py#L286
        obj = sys.modules[info["module"]]
        for part in info["fullname"].split("."):
            obj = getattr(obj, part)
        import inspect
        import os

        fn = inspect.getsourcefile(obj)
        fn = os.path.relpath(fn, start=os.path.dirname(sktime.__file__))
        source, lineno = inspect.getsourcelines(obj)
        return fn, lineno, lineno + len(source) - 1

    if domain != "py" or not info["module"]:
        return None
    try:
        filename = "sktime/%s#L%d-L%d" % find_source()
    except Exception:
        filename = info["module"].replace(".", "/") + ".py"
    return "https://github.com/sktime/sktime/blob/%s/%s" % (
        CURRENT_VERSION,
        filename,
    )


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "pydata_sphinx_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/sktime/sktime",
            "icon": "fab fa-github",
        },
        {
            "name": "Slack",
            "url": "https://join.slack.com/t/sktime-group/shared_invite/zt-1cghagwee-sqLJ~eHWGYgzWbqUX937ig",  # noqa: E501
            "icon": "fab fa-slack",
        },
        {
            "name": "Discord",
            "url": "https://discord.com/invite/gqSab2K",
            "icon": "fab fa-discord",
        },
        {
            "name": "LinkedIn",
            "url": "https://www.linkedin.com/company/sktime/",
            "icon": "fab fa-linkedin",
        },
        {
            "name": "Twitter",
            "url": "https://twitter.com/sktime_toolbox",
            "icon": "fab fa-twitter",
        },
    ],
    "favicons": [
        {
            "rel": "icon",
            "sizes": "16x16",
            "href": "images/sktime-favicon.ico",
        }
    ],
    "show_prev_next": False,
    "use_edit_page_button": False,
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links"],
}
html_logo = "images/sktime-logo-text-horizontal.png"
html_context = {
    "github_user": "sktime",
    "github_repo": "sktime",
    "github_version": "main",
    "doc_path": "docs/source/",
}
html_favicon = "images/sktime-favicon.ico"
html_sidebars = {
    "**": ["search-field.html", "sidebar-nav-bs.html", "sidebar-ethical-ads.html"]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_js_files = [
    "js/dynamic_table.js",
]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

html_show_sourcelink = False

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "sktimedoc"

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "sktime.tex", "sktime Documentation", "sktime developers", "manual"),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "sktime", "sktime Documentation", [author], 1)]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "sktime",
        "sktime Documentation",
        author,
        "sktime",
        "One line description of project.",
        "Miscellaneous",
    ),
]


def _make_estimator_overview(app):
    """Make estimator overview table."""
    import pandas as pd

    from sktime.registry import all_estimators

    def _process_author_info(author_info):
        """
        Process author information from source code files.

        Parameters
        ----------
        author_info : str
            Author information string from source code files.

        Returns
        -------
        author_info : str
            Preprocessed author information.

        Notes
        -----
        A list of author names is turned into a string.
        Multiple author names will be separated by a comma,
        with the final name always preceded by "&".
        """
        if isinstance(author_info, list):
            if len(author_info) > 1:
                return ", ".join(author_info[:-1]) + " & " + author_info[-1]
            else:
                return author_info[0]
        else:
            return author_info

    def _does_not_start_with_underscore(input_string):
        return not input_string.startswith("_")

    # creates dataframe as df
    COLNAMES = ["Class Name", "Estimator Type", "Authors"]

    df = pd.DataFrame([], columns=COLNAMES)

    for modname, modclass in all_estimators():
        algorithm_type = "::".join(str(modclass).split(".")[1:-2])
        try:
            author_info = _process_author_info(modclass.__author__)
        except AttributeError:
            try:
                author_info = _process_author_info(
                    import_module(modclass.__module__).__author__
                )
            except AttributeError:
                author_info = "no author info"

        # includes part of class string
        modpath = str(modclass)[8:-2]
        path_parts = modpath.split(".")
        # joins strings excluding starting with '_'
        clean_path = ".".join(list(filter(_does_not_start_with_underscore, path_parts)))
        # adds html link reference
        modname = str(
            '<a href="https://www.sktime.org/en/latest/api_reference'
            + "/auto_generated/"
            + clean_path
            + '.html">'
            + modname
            + "</a>"
        )

        record = pd.DataFrame([modname, algorithm_type, author_info], index=COLNAMES).T
        df = pd.concat([df, record], ignore_index=True)
    with open("estimator_overview_table.md", "w") as file:
        df.to_markdown(file, index=False)


def setup(app):
    """Set up sphinx builder.

    Parameters
    ----------
    app : Sphinx application object
    """

    def adds(pth):
        print("Adding stylesheet: %s" % pth)  # noqa: T201, T001
        app.add_css_file(pth)

    adds("fields.css")  # for parameters, etc.

    app.connect("builder-inited", _make_estimator_overview)


# -- Extension configuration -------------------------------------------------

# -- Options for nbsphinx extension ---------------------------------------
nbsphinx_execute = "never"  # always  # whether to run notebooks
nbsphinx_allow_errors = False  # False
nbsphinx_timeout = 600  # seconds, set to -1 to disable timeout

# add Binder launch buttom at the top
current_file = "{{ env.doc2path( env.docname, base=None) }}"

# make sure Binder points to latest stable release, not main
binder_url = f"https://mybinder.org/v2/gh/sktime/sktime/{CURRENT_VERSION}?filepath={current_file}"  # noqa
nbsphinx_prolog = f"""
.. |binder| image:: https://mybinder.org/badge_logo.svg
.. _Binder: {binder_url}

|Binder|_
"""

# add link to original notebook at the bottom
notebook_url = (
    f"https://github.com/sktime/sktime/tree/{CURRENT_VERSION}/{current_file}"  # noqa
)
nbsphinx_epilog = f"""
----

Generated using nbsphinx_. The Jupyter notebook can be found here_.

.. _here: {notebook_url}
.. _nbsphinx: https://nbsphinx.readthedocs.io/
"""

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/{.major}".format(sys.version_info), None),
    "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    "matplotlib": ("https://matplotlib.org/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "joblib": ("https://joblib.readthedocs.io/en/latest/", None),
    "scikit-learn": ("https://scikit-learn.org/stable/", None),
    "statsmodels": ("https://www.statsmodels.org/stable/", None),
}

# -- Options for _todo extension ----------------------------------------------
todo_include_todos = False
