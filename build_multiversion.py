# -*- coding: utf-8 -*-
# Copyright (C) 2026 Open Robotics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import sys
import textwrap
import yaml

import build_utils

build_utils.register_yaml_include(Path(__file__).parent)
from build_utils import flatten_navigation


def _build_sphinx(src_dir, output_dir, variables, extra_args, strict_mode=True):
    """Build arguments for running sphinx-build

    Args:
        src_dir (str): Source directory
        output_dir (str): Output directory
        variables (dict): Dictionary of variables passed with `-D`
        extra_args (list): Extra arguments forwarded to sphinx
    """
    sphinx_args = [
        "sphinx-build",
        "--nitpick",
        "-b",
        "dirhtml"]
    if strict_mode:
        sphinx_args.append("--fail-on-warning")

    sphinx_args.extend([str(src_dir), str(output_dir)])

    for key, val in variables.items():
        sphinx_args.extend(["-D", f"{key}={val}"])

    sphinx_args.extend(extra_args)

    build_utils_src = Path(src_dir)
    env = dict(os.environ)
    existing_pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        existing_pp + os.pathsep + str(build_utils_src)
        if existing_pp else str(build_utils_src)
    )
    subprocess.run(sphinx_args, check=True, env=env)


def generate_sources(nav_yaml, root_src_dir, tmp_dir, ngp_release):

    if not ngp_release:
        raise RuntimeError("ngp_release not provided")

    base = nav_yaml["base"]

    matching_release = [
        release for release in nav_yaml["releases"] if release["name"] == ngp_release
    ]
    if not matching_release:
        raise RuntimeError(
            f"Provided ngp_release '{ngp_release}' not registered in `index.yaml`"
        )
    elif len(matching_release) > 1:
        raise RuntimeError(f"More than one releases named '{ngp_release}' found.")

    release_info = matching_release[0]

    tmp_dir.mkdir(exist_ok=True)
    version_tmp_dir = tmp_dir / ngp_release

    # Start with a clean slate
    if version_tmp_dir.exists():
        shutil.rmtree(version_tmp_dir)

    if ngp_release == base:
        # Build the base release directly from the base content.
        shutil.copytree(root_src_dir / base, version_tmp_dir, dirs_exist_ok=True)
    else:
        # 1. Start from the base (formerly "common") content
        shutil.copytree(root_src_dir / base, version_tmp_dir, dirs_exist_ok=True)

        # 2. Overlay release-specific files on top
        release_src_dir = root_src_dir / ngp_release
        shutil.copytree(release_src_dir, version_tmp_dir, dirs_exist_ok=True)

    # 3. Copy sphinx infrastructure files
    for dir in ["_static", "_templates"]:
        shutil.copytree(root_src_dir / dir, version_tmp_dir / dir, dirs_exist_ok=True)
    shutil.copy2(root_src_dir / "base_conf.py", version_tmp_dir)
    shutil.copy2(root_src_dir / "conf.py", version_tmp_dir)
    shutil.copy2(root_src_dir / "build_utils.py", version_tmp_dir)

    # 4. Generate the source manifest for "Edit on GitHub" links
    manifest = {}
    base_dir = root_src_dir / base
    for path in base_dir.glob('**/*'):
        if path.is_file():
            rel_path = path.relative_to(base_dir)
            manifest[str(rel_path)] = f"{base}/{rel_path}"

    if ngp_release != base:
        release_dir = root_src_dir / ngp_release
        for path in release_dir.glob('**/*'):
            if path.is_file():
                rel_path = path.relative_to(release_dir)
                manifest[str(rel_path)] = f"{ngp_release}/{rel_path}"

    manifest_path = version_tmp_dir / 'source_manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    deploy_url = os.environ.get("NGP_DEPLOY_URL", "http://localhost:8000")
    # Path sub-directory where this release tree is published. Defaults to ""
    # (web root, matching the local `python3 -m http.server .build/docs` server).
    # Set to "/docs" (etc.) when serving under a sub-directory.
    docs_path = os.environ.get("NGP_DOCS_PATH", "")
    is_hex = lambda s: all(c in "0123456789abcdef" for c in s.lower())
    switcher = []
    for release in nav_yaml["releases"]:
        name = release["name"]
        if not is_hex(name):
            name = name.capitalize()
        if release["eol"]:
            name += " (EOL)"
        elif release["lts"]:
            name += " (LTS)"
        elif release.get("dev", False):
            name += " (dev)"

        switcher.append(
            {
                "name": name,
                "version": release["name"],
                "url": f"{deploy_url}{docs_path}/{release['name']}/",
                "preferred": release.get("preferred", False)
            }
        )

    static_dir = version_tmp_dir / "_static"
    static_dir.mkdir(exist_ok=True)
    json.dump(switcher, open(static_dir / "switcher.json", "w"))

    # 5. Load navigation
    with open(version_tmp_dir / "index.yaml") as f:
        version_nav_yaml = yaml.safe_load(f)
        if not version_nav_yaml or not version_nav_yaml.get("pages"):
            raise RuntimeError(
                f"{ngp_release}/index.yaml is missing a non-empty `pages:` list."
            )
        version_nav_yaml['pages'] = flatten_navigation(version_nav_yaml['pages'])

    def handle_file_url_rename(file_path, file_url):
        computed_url, ext = os.path.splitext(file_path)
        if file_url != computed_url:
            new_path = file_url + ext
            shutil.move(version_tmp_dir / file_path, version_tmp_dir / new_path)
            return new_path
        return file_path


    def create_toctrees(pages):
        nav_md = []
        for page in pages:
            maybe_hidden = ":hidden:"
            file_url = page["name"]

            # If the page references an existing file, resolve its path
            # (stripping the base-commit prefix, e.g. "251cfbf:") and rename
            # the source file in the temporary directory if its custom URL
            # path name differs from the underlying filename.
            if "file" in page:
                file_path = page["file"].removeprefix(f"{base}:")
                new_file_path = handle_file_url_rename(file_path, file_url)
            else:
                new_file_path = f"{file_url}.md"
                maybe_hidden = ""
                with open(version_tmp_dir / new_file_path, "w") as ind_f:
                    ind_f.write(textwrap.dedent(f"""\
                        ---
                        html_theme.sidebar_secondary.remove: true
                        ---

                        # {page['title']}
                        """))

            nav_md.append(f"{page['title']} <{file_url}>")
            children = page.get("children")
            if children:
                child_md = create_toctrees(children)
                with open(version_tmp_dir / new_file_path, "a") as ind_f:
                    ind_f.write(textwrap.dedent(f"""
                        ```{{toctree}}
                        :maxdepth: 1
                        :titlesonly:
                        {maybe_hidden}
                        """))
                    ind_f.write("\n".join(child_md))
                    ind_f.write("\n```\n")
        return nav_md

    # Respect a hand-authored index.md: if the base or release source dir
    # shipped its own index.md, the copy above already placed it in the
    # version dir — use it and skip auto-generation. Otherwise fall back to
    # generating a toctree page from index.yaml.
    if (version_tmp_dir / "index.md").exists():
        return

    index_toc = "# Index\n\n"
    for page in version_nav_yaml["pages"]:
        if "section" not in page:
            print(
                "The top level item in the pages entry of index.yaml should be a 'section'.\n"
                f"Found {page}"
            )
            sys.exit(1)
        index_toc += textwrap.dedent(f"""\
        ```{{toctree}}
        :hidden:
        :maxdepth: 1
        :titlesonly:
        :caption: {page["section"]}
        """)

        nav_md = create_toctrees(page["children"])
        index_toc += "\n".join(nav_md) + "\n"
        index_toc += "```\n\n"

    with open(version_tmp_dir / "index.md", "w") as ind_f:
        ind_f.write(index_toc)


def get_preferred_release(releases: dict):
    preferred = [rel for rel in releases if rel.get("preferred", False)]
    assert len(preferred) == 1
    return preferred[0]


def main(argv=None):
    src_dir = Path(__file__).parent

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--releases",
        metavar="NGP_RELEASES",
        nargs="*",
        help="Names of releases to build. Builds all known releases if empty.",
    )
    parser.add_argument(
        "--output_dir", default=src_dir / ".build", help="Path to output directory"
    )
    parser.add_argument(
        "--pointers",
        action="store_true",
        default=False,
        help="Build 'latest' and 'all'",
    )

    args, unknown_args = parser.parse_known_args(argv)

    index_yaml = src_dir / "index.yaml"
    assert index_yaml.exists()

    with open(index_yaml) as top_index_file:
        nav_yaml = yaml.safe_load(top_index_file)

    if not args.releases:
        args.releases = [release["name"] for release in nav_yaml["releases"]]

    preferred_release = get_preferred_release(nav_yaml["releases"])
    tmp_dir = src_dir / ".tmp"
    tmp_dir.mkdir(exist_ok=True)
    build_dir = Path(args.output_dir)
    build_dir.mkdir(exist_ok=True)

    build_docs_dir = build_dir / "docs"
    for release in args.releases:
        generate_sources(nav_yaml, src_dir, tmp_dir, release)
        release_build_dir = build_docs_dir / release
        _build_sphinx(
            tmp_dir / release,
            release_build_dir,
            {"ngp_release": release, "ngp_root_index_file": index_yaml},
            unknown_args,
        )

    # Handle "latest" and "all"
    release = preferred_release["name"]
    if args.pointers and (release in args.releases):
        for pointer in ["latest", "all"]:
            release_build_dir = build_docs_dir / pointer
            pointer_tmp_dir = tmp_dir / pointer
            try:
                pointer_tmp_dir.symlink_to(tmp_dir / release)
            except FileExistsError:
                # It's okay for it to exist, but make sure it's a symlink
                if not pointer_tmp_dir.is_symlink:
                    raise RuntimeError(
                        f"{pointer_tmp_dir} already exists and is not a symlink"
                    )

            _build_sphinx(
                pointer_tmp_dir,
                release_build_dir,
                {"ngp_release": release, "ngp_root_index_file": index_yaml},
                unknown_args,
            )

        # Create a redirect to "/latest"
        redirect_page = build_docs_dir / "index.html"
        redirect_page.write_text("""\
<!DOCTYPE html>
<html>
  <head>
    <meta content="0; url=latest" http-equiv="refresh" />
  </head>
</html>
""")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
