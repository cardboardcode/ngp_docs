# -*- coding: utf-8 -*-
#
# Sphinx configuration for the generic documentation template.
#
# Derived from gazebosim/docs (https://github.com/gazebosim/docs): it keeps the
# visual look (pydata-sphinx-theme + custom CSS + custom navbar/sidebar/footer
# templates) but strips all the Gazebo-specific and multi-release build
# machinery, leaving a single, self-contained config.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Docs Template"
author = "Your Org"
copyright = "2026, Your Org"

version = "0.1"   # The short X.Y version, e.g. "1.0"
release = "0.1"   # The full version, e.g. "1.0.3"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    # "sphinxcontrib.mermaid",  # optional: re-enable + uncomment myst_fence_as_directive below
]

templates_path = ["_templates"]

source_suffix = {
    ".md": "markdown",
}

# Don't ingest package READMEs / dist-info files that live under a local venv
# as "documents" — they would each emit a "not in any toctree" warning.
exclude_patterns = [
    "_build", "Thumbs.db", ".DS_Store", ".venv", ".tmp", ".build",
    "README.md", ".codespell",
]

myst_heading_anchors = 4

myst_enable_extensions = [
    "attrs_inline",
    "attrs_block",
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# myst_fence_as_directive = ["mermaid"]  # enable together with sphinxcontrib.mermaid

# Be forgiving about unresolved references; tighten to True once links are clean.
nitpicky = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["css/gazebo.css"]
html_favicon = "_static/icon/favicon.ico"

html_theme_options = {
    "header_links_before_dropdown": 4,
    "use_edit_page_button": True,
    "show_toc_level": 1,
    "navigation_with_keys": False,
    "show_prev_next": False,
    "footer_center": ["footer"],
    "secondary_sidebar_items": ["page-toc"],
    "navbar_align": "left",
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    "pygments_light_style": "tango",
    "pygments_dark_style": "monokai",
    # TODO: replace with your project logo (SVGs live in _static/images/logos/)
    "logo": {
        "image_light": "_static/images/logos/logo_light.svg",
        "image_dark": "_static/images/logos/logo_dark.svg",
    },
    "check_switcher": False,
    "show_version_warning_banner": False,
}

# The sidebar is driven by _templates/sidebar-nav.html, which renders a
# toctree explicitly named "sidebar" (see index.md).
html_sidebars = {"**": ["sidebar-nav"]}
html_sidebar = "sidebar-nav"

# "Edit this page" button: point these at your own repo (or set
# "use_edit_page_button": False to hide the button entirely).
html_context = {
    "github_user": "your-org",            # TODO: your GitHub org/user
    "github_repo": "your-docs",           # TODO: your documentation repo name
    "github_version": "main",             # TODO: the branch holding the docs
    "edit_page_url_template": "{{ github_url }}/{{ github_user }}/{{ github_repo }}/edit/{{ github_version }}/{{ doc_path }}",
    "edit_page_provider_name": "GitHub",
}
