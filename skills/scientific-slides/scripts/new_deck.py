#!/usr/bin/env python3
"""Copy the bundled, offline layout gallery into a new project directory."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


OMIT = {".preview", "_cache", "__pycache__", ".venv", "node_modules", "dist"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dest", type=Path, help="new directory; must not already exist")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / "assets" / "template"
    destination = args.dest.expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        parser.error(f"destination already exists: {destination}")
    if not (source / "index.html").is_file():
        parser.error(f"template not found beside this skill: {source}")
    if source == destination.resolve() or source in destination.resolve().parents:
        parser.error("destination must be outside the template directory")
    for path in source.rglob("*"):
        if path.is_symlink():
            parser.error(f"template contains a symlink; use ordinary local files: {path}")
    try:
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns(*OMIT, "*.pyc", "*.pyo", ".DS_Store"),
        )
    except OSError as exc:
        # Leave a partial copy available for inspection; never remove caller paths.
        print(f"Could not finish copying: {exc}", file=sys.stderr)
        return 1
    print(f"Created {destination}")
    print(f"Open {destination / 'index.html'} in a browser.")
    print("Edit presentation.md, then ask your agent to translate the agreed draft into HTML.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
