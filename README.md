# Docs Template

A reusable documentation starter built on **Sphinx** + **MyST Markdown** +
**pydata-sphinx-theme**, derived from the [Gazebo Sim docs](https://github.com/gazebosim/docs).
It keeps the full look (custom CSS, sidebar, navbar and footer templates)
while stripping all Gazebo-specific content and the multi-release build
machinery, replacing them with a handful of sample pages.

## What's inside

| Path | Purpose |
|------|---------|
| `conf.py` | Single, self-contained Sphinx configuration |
| `index.md` | Landing page, design grid, and the `main` + `sidebar` toctrees |
| `getting_started.md` | Code blocks with copy buttons, callouts |
| `tutorials.md` | Task lists (`- [ ]`) and admonitions (`{note}`, `{tip}`, `{danger}`) |
| `api.md` | API reference placeholder |
| `_templates/sidebar-nav.html` | Sidebar driven by a toctree named `sidebar` |
| `_templates/navbar-nav.html` | Placeholder top-nav links (edit me) |
| `_templates/footer.html` | Generic footer |
| `_static/css/gazebo.css` | CSS overrides — rebrand colours here |
| `_static/images/logos/` | Placeholder light/dark SVG logos |
| `requirements.txt` | Python build dependencies |

## Getting started

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

# build the site
sphinx-build -b html . _build/html

# preview
python -m http.server -d _build/html
# → http://localhost:8000
```

## Rebranding

1. **Project identity** — set `project`, `author` and `copyright` in `conf.py`.
2. **Logo** — drop your SVGs into `_static/images/logos/` and update the
   `logo` entry in `html_theme_options`.
3. **Colours** — edit `_static/css/gazebo.css` (root CSS custom properties
   drive the theme's accents).
4. **Navbar** — replace the placeholder links in `_templates/navbar-nav.html`.
5. **Footer** — adjust `_templates/footer.html`.
6. **"Edit this page"** — point `github_user` / `github_repo` / `github_version`
   in `conf.py` at your repo, or set `use_edit_page_button` to `False`.
7. **Content** — delete the sample `.md` files, add your own, and list them in
   **both** the visible toctree and the hidden `sidebar` toctree in
   `index.md`.

## Notes

- The sidebar navigation is driven by an explicitly named toctree
  (`toctrees = {"sidebar": ...}` in `conf.py` + matching hidden toctree in
  `index.md`) — there is no multi-version machinery.
- Optional extras commented out in `requirements.txt` / `conf.py`:
  `sphinxcontrib.mermaid`, `sphinxcontrib.googleanalytics`.
