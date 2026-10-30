# -*- coding: utf-8 -*-
#
# Base / shared Sphinx configuration for the multi-release docs build.
# Imported (via `from base_conf import *`) by the per-release conf.py.
#
# This holds only theme / MyST / static-path settings that are identical
# across all releases. Per-release values (version/release, html_context,
# exclude_patterns, switcher) are set in conf.py at build time.

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))

# -- Project information -----------------------------------------------------

project = "NGP"
author = "Bey Hao Yun"
copyright = "2026, Bey Hao Yun"

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
]

templates_path = ["_templates"]

source_suffix = {
    ".md": "markdown",
}

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

myst_fence_as_directive = ["mermaid"]

# Be forgiving about unresolved references; tighten to True once links are clean.
nitpicky = False

# -- Options for HTML output -------------------------------------------------

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
    "navbar_end": ["version-switcher", "theme-switcher", "navbar-icon-links"],
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

html_sidebars = {"**": ["sidebar-nav"]}
html_sidebar = "sidebar-nav"

import os

html_context = {
    # Default to empty (origin-relative) so local servers on any host/port work.
    "deploy_url": os.environ.get("NGP_DEPLOY_URL", ""),
}
