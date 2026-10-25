# Getting started

This page demonstrates the building blocks the template ships with:
prose, code blocks with copy buttons, and callout boxes.

## Prerequisites

- Python 3.10+
- `make` (optional, we build directly with `sphinx-build` here)

## Install

:::{code-block} bash
:caption: Install the build dependencies
:emphasize-lines: 1

python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
:::

:::{tip}
The copy button on the right-hand side of every code block comes from
`myst_parser` + `sphinx_copybutton` — no extra work is needed to wire it up.
:::

## Build and preview

:::{code-block} bash
:caption: Build the site

sphinx-build -b html . _build/html
python -m http.server -d _build/html
:::

Then open <http://localhost:8000> in a browser.

## What's in the repo

- `conf.py` — single, self-contained Sphinx configuration.
- `_templates/` — custom navbar, sidebar and footer overrides.
- `_static/css/gazebo.css` — the theme's CSS overrides.
- Sample pages: `index.md`, `getting_started.md`, `tutorials.md`, `api.md`.
