# Docs Template

A starting point for Sphinx-based documentation: pydata-sphinx-theme + MyST
Markdown + custom CSS, derived from the Gazebo Sim docs.

:::{toctree}
:maxdepth: 1
:caption: Get started
getting_started
tutorials
api
:::

:::{grid} 1 1 2 3
:::{grid-row}
:::{grid-item}
:::{grid-item-card} Get started
:link: getting_started.html

Prerequisites, installation and a quick tour of the toolchain.
:::
:::
:::{grid-item}
:::{grid-item-card} Tutorials
:link: tutorials.html

Hands-on examples with callouts and task lists.
:::
:::
:::{grid-item}
:::{grid-item-card} API
:link: api.html

Placeholder for generated or hand-written API reference.
:::
:::
:::
:::

:::{note}
To rebrand, edit `conf.py` (project name, logo paths, github_user/repo),
`_templates/navbar-nav.html` (navbar links), and `css/gazebo.css` (colours).
:::
