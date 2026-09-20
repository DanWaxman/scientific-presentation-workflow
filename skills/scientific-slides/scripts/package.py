#!/usr/bin/env python3
"""Stage a deck's publication files without deploying or copying authoring files."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import unquote, urlsplit


ROOT_FILES = ("index.html", "styles.css", "slides.js", "LICENSE", "THIRD_PARTY_NOTICES.md")
VENDOR_EXTENSIONS = {".js", ".mjs", ".css", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".svg"}
MEDIA_EXTENSIONS = {".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".mp4", ".webm", ".ogg", ".mp3", ".wav", ".pdf", ".vtt"}
OMIT = {".preview", "_cache", "__pycache__", ".venv", "node_modules", "dist", ".git"}
LICENSE_NAME = re.compile(r"^(?:licen[cs]e|copying|copyright|notice|ofl|third.party.notices)(?:[._-].*)?$", re.I)


class References(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[tuple[str, bool]] = []
        self.inline_css: list[str] = []
        self.in_style = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for key in ("src", "poster"):
            if values.get(key):
                self.references.append((values[key], True))
        if tag == "object" and values.get("data"):
            self.references.append((values["data"], True))
        for key in ("href", "xlink:href"):
            if values.get(key):
                self.references.append((values[key], tag in {"link", "image", "use"}))
        if values.get("style"):
            self.inline_css.append(values["style"])
        if values.get("srcset") and not values["srcset"].startswith("data:"):
            for candidate in values["srcset"].split(","):
                self.references.append((candidate.strip().split()[0], True))
        if tag == "style":
            self.in_style = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self.in_style = False

    def handle_data(self, data: str) -> None:
        if self.in_style:
            self.inline_css.append(data)


def css_references(css: str) -> list[str]:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    urls = re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", css, flags=re.I)
    urls.extend(re.findall(r"@import\s+['\"]([^'\"]+)['\"]", css, flags=re.I))
    return urls


def publishable_files(deck: Path) -> list[Path]:
    files = []
    for name in ROOT_FILES:
        path = deck / name
        if path.is_symlink():
            raise ValueError(f"refusing symlink: {path}")
        if not path.is_file():
            raise ValueError(f"required publication file is missing: {path}")
        files.append(path)
    for directory, extensions in (("vendor", VENDOR_EXTENSIONS), ("figs", MEDIA_EXTENSIONS)):
        root = deck / directory
        if root.is_symlink():
            raise ValueError(f"refusing symlink: {root}")
        if not root.is_dir():
            raise ValueError(f"required asset directory is missing: {root}")
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root)
            if any(part in OMIT or part.startswith(".") for part in relative.parts):
                continue
            if path.is_symlink():
                raise ValueError(f"refusing symlink: {path}")
            is_provenance = path == deck / "vendor" / "provenance.json"
            if path.is_file() and (path.suffix.lower() in extensions or LICENSE_NAME.fullmatch(path.name) or is_provenance):
                files.append(path)
    return files


def validate_references(deck: Path, files: list[Path]) -> list[str]:
    selected = {path.resolve() for path in files}
    problems = []
    for path in files:
        refs: list[tuple[str, bool]] = []
        if path.suffix in {".html", ".svg"}:
            parser = References()
            parser.feed(path.read_text(encoding="utf-8"))
            refs.extend(parser.references)
            for css in parser.inline_css:
                refs.extend((url, True) for url in css_references(css))
        elif path.suffix == ".css":
            refs.extend((url, True) for url in css_references(path.read_text(encoding="utf-8")))
        for reference, is_asset in refs:
            parsed = urlsplit(reference.strip())
            if parsed.scheme or parsed.netloc:
                if is_asset and parsed.scheme not in {"data", "blob"}:
                    problems.append(f"{path.relative_to(deck)}: external asset {reference}")
                continue
            if not parsed.path:
                continue
            local = unquote(parsed.path)
            if local.startswith("/"):
                problems.append(f"{path.relative_to(deck)}: root-relative path is not portable: {reference}")
                continue
            target = (path.parent / local).resolve()
            if target not in selected:
                problems.append(f"{path.relative_to(deck)}: reference is missing from publication files: {reference}")
    return sorted(set(problems))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path, help="deck directory")
    parser.add_argument("--out", required=True, type=Path, help="new staging directory; must not exist")
    args = parser.parse_args()
    deck = args.deck.expanduser().resolve()
    destination = args.out.expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        parser.error(f"destination already exists: {destination}")
    if deck == destination.resolve() or deck in destination.resolve().parents:
        parser.error("stage publication outside the source deck")
    try:
        files = publishable_files(deck)
        problems = validate_references(deck, files)
        if problems:
            raise ValueError("\n".join(problems))
        destination.mkdir(parents=True)
        for path in files:
            target = destination / path.relative_to(deck)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    except (OSError, ValueError) as exc:
        print(f"Publication staging failed: {exc}", file=sys.stderr)
        return 1
    print(f"Staged {len(files)} files in {destination}")
    print("Drafts, scientific source, caches, and previews were excluded. Nothing was deployed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
