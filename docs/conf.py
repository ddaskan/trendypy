# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import inspect
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../')
sys.path.append('../trendypy/')


# -- Project information -----------------------------------------------------

project = 'TrendyPy'
copyright = '2020, Dogan Askan'
author = 'Dogan Askan'

# The full version, including alpha/beta/rc tags
release = '0.2.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	'sphinx.ext.autodoc',
	'sphinxcontrib.napoleon',
	#'sphinx.ext.viewcode',
	'sphinx.ext.linkcode',
	'sphinx_copybutton',
	'recommonmark'
]

extensions += [#'matplotlib.sphinxext.only_directives',
              'matplotlib.sphinxext.plot_directive',
              'IPython.sphinxext.ipython_directive',
              'IPython.sphinxext.ipython_console_highlighting',
              'sphinx.ext.mathjax',
              'sphinx.ext.doctest',
              ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
html_theme = "pydata_sphinx_theme"
html_logo = "_static/trendypy.png"
html_favicon = "_static/favicon/favicon.ico"
html_theme_options = {
    "github_url": "https://github.com/ddaskan/trendypy/",
    "twitter_url": "https://twitter.com/_DoganAskan",
    "google_analytics_id": "UA-100432301-2",
    "navigation_with_keys": True,
    "use_edit_page_button": True,
    # "search_bar_position": "navbar",
}

html_context = {
    "github_user": "ddaskan",
    "github_repo": "trendypy",
    "github_version": "master",
    "doc_path": "docs",
    'page_source_suffix': '.rst',
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

autodoc_member_order = 'bysource'

# Napoleon settings
napoleon_google_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = None

copybutton_prompt_text = '>>> |\\\\.\\\\.\\\\. |\\\\$ |In \\\\[\\\\d*\\\\]: |\\\\s+\\.\\.\\.: '
copybutton_prompt_is_regexp = True

ipython_savefig_dir = ""

def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != "py":
        return None

    modname = info["module"]
    fullname = info["fullname"]

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except AttributeError:
            return None

    try:
        fn = inspect.getsourcefile(inspect.unwrap(obj))
    except TypeError:
        fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except OSError:
        lineno = None

    if lineno:
        linespec = f"#L{lineno}-L{lineno + len(source) - 1}"
    else:
        linespec = ""

    filename = info['module'].replace('.', '/')
    return "https://github.com/ddaskan/trendypy/blob/master/trendypy/%s.py" % filename+linespec
