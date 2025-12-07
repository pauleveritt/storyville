# Configuration file for the Sphinx documentation builder.

# -- Project information
project = "Storyville"
copyright = "2025, Paul Everitt"
author = "Paul Everitt"
release = "0.1.0"

# -- General configuration
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output
html_theme = "furo"
# html_static_path = ['_static']

# -- MyST configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
]

# -- Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pytest": ("https://docs.pytest.org/en/stable/", None),
}

# -- Autodoc configuration
autodoc_typehints = "description"
autodoc_member_order = "bysource"
