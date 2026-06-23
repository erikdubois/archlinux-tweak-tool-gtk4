#!/usr/bin/env python3
"""Generate the Surfn icon-theme table and folder thumbnails for the Icons page.

Run automatically by up.sh. Surfn ships as ~50 standalone colour-variant packages
(sources in ~/EDU/surfn*, build recipes in ~/KIRO-PKG-BUILD-ICONS); the Surfn tab
must stay in sync without hand-editing icons.py for every new variant.

For each variant this records:

  * token   — the source/repo directory name (e.g. surfn-mint-y-blue), the unique key
  * package — pkgname from the build recipe's PKGBUILD (fallback: <token>-icons-git)
  * family  — display group / filter button (Mint-X, Mint-Y, Plasma, …)

and renders a small folder preview for the page by loading the theme's canonical
folder icon (folder.png or folder.svg, following index.theme `Inherits=` for sparse
overlays) and scaling it to a PNG thumbnail via GdkPixbuf.

Outputs:
  * usr/share/archlinux-tweak-tool/data/surfn_families.json
  * usr/share/archlinux-tweak-tool/images/surfn/<token>.png
"""

import json
import os
import re
import sys
from os import path

import gi

gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf  # noqa: E402

SCRIPT_DIR = path.dirname(path.realpath(__file__))
APP_DIR = path.join(SCRIPT_DIR, "usr/share/archlinux-tweak-tool")
DATA_OUT = path.join(APP_DIR, "data", "surfn_families.json")
THUMB_DIR = path.join(APP_DIR, "images", "surfn")
THUMB_SIZE = 28

HOME = path.expanduser("~")
SRC_ROOT = os.environ.get("SURFN_SRC_ROOT", path.join(HOME, "EDU"))
PKG_ROOT = os.environ.get("SURFN_PKG_ROOT", path.join(HOME, "KIRO-PKG-BUILD-ICONS"))

# Display order of the families; tokens within a family are sorted alphabetically.
FAMILY_ORDER = ["Mint-X", "Mint-Y", "Plasma", "Numix", "Papirus", "Arc / Breeze", "Other"]
ARC_BREEZE = {"arc-breeze", "breeze-arc", "breeze-dark"}


def _classify(token):
    rest = token[len("surfn-"):] if token.startswith("surfn-") else token
    if rest.startswith("mint-x"):
        return "Mint-X"
    if rest.startswith("mint-y"):
        return "Mint-Y"
    if rest.startswith("plasma"):
        return "Plasma"
    if rest.startswith("numix"):
        return "Numix"
    if rest.startswith("papirus"):
        return "Papirus"
    if rest in ARC_BREEZE:
        return "Arc / Breeze"
    return "Other"


def _theme_dir(token):
    icons_root = path.join(SRC_ROOT, token, "usr/share/icons")
    if not path.isdir(icons_root):
        return None
    for name in sorted(os.listdir(icons_root)):
        if path.isdir(path.join(icons_root, name)):
            return name
    return None


def _package_name(token):
    pkgbuild = path.join(PKG_ROOT, token, "PKGBUILD")
    try:
        with open(pkgbuild, "r", encoding="utf-8") as f:
            for line in f:
                m = re.match(r"\s*pkgname=\(?\s*['\"]?([^'\"()\s]+)", line)
                if m:
                    return m.group(1)
    except OSError:
        pass
    return token + "-icons-git"


def _size_of(p):
    m = re.search(r"(\d+)", p)
    return int(m.group(1)) if m else 0


def _canonical_folder(token, theme_dir, _seen=None):
    """Return the path to the theme's main folder icon, following Inherits when absent."""
    if _seen is None:
        _seen = set()
    if theme_dir in _seen:
        return None
    _seen.add(theme_dir)

    theme_root = path.join(SRC_ROOT, token, "usr/share/icons", theme_dir)
    hits = []
    for dirpath, _dirnames, filenames in os.walk(theme_root):
        for fname in filenames:
            if fname in ("folder.png", "folder.svg"):
                hits.append(path.join(dirpath, fname))
    if hits:
        # Prefer PNG, then the largest size dir for a crisp thumbnail.
        hits.sort(key=lambda p: (p.endswith(".png"), _size_of(p)), reverse=True)
        return hits[0]

    # Sparse overlay (e.g. plasma-flow): follow index.theme Inherits to a parent surfn theme.
    index = path.join(theme_root, "index.theme")
    try:
        with open(index, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("Inherits="):
                    for parent in line.split("=", 1)[1].split(","):
                        parent = parent.strip()
                        parent_token = _token_for_theme_dir(parent)
                        if parent_token:
                            found = _canonical_folder(parent_token, parent, _seen)
                            if found:
                                return found
    except OSError:
        pass
    return None


_THEME_DIR_INDEX = {}


def _token_for_theme_dir(theme_dir):
    return _THEME_DIR_INDEX.get(theme_dir)


def _discover_tokens():
    tokens = []
    for name in sorted(os.listdir(SRC_ROOT)):
        if name != "surfn" and not name.startswith("surfn-"):
            continue
        if not path.isdir(path.join(SRC_ROOT, name, "usr/share/icons")):
            continue
        tokens.append(name)
    return tokens


def _write_thumbnail(folder_path, token):
    out = path.join(THUMB_DIR, token + ".png")
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(folder_path, THUMB_SIZE, THUMB_SIZE)
    pixbuf.savev(out, "png", [], [])
    return out


def main():
    if not path.isdir(SRC_ROOT):
        print(f"[surfn] source root not found: {SRC_ROOT} — skipping", file=sys.stderr)
        return 0

    os.makedirs(THUMB_DIR, exist_ok=True)
    os.makedirs(path.dirname(DATA_OUT), exist_ok=True)

    tokens = _discover_tokens()
    for token in tokens:
        td = _theme_dir(token)
        if td:
            _THEME_DIR_INDEX[td] = token

    families = {fam: [] for fam in FAMILY_ORDER}
    no_thumb = []
    for token in tokens:
        theme_dir = _theme_dir(token)
        package = _package_name(token)
        families[_classify(token)].append({"token": token, "package": package})

        folder = _canonical_folder(token, theme_dir) if theme_dir else None
        if not folder:
            # Last resort (e.g. an overlay inheriting only system Breeze): use the base Surfn folder.
            base_dir = _theme_dir("surfn")
            if base_dir:
                folder = _canonical_folder("surfn", base_dir)
        if folder:
            try:
                _write_thumbnail(folder, token)
            except Exception as error:  # noqa: BLE001 - bad SVG/PNG must not abort the run
                no_thumb.append(f"{token} ({error})")
        else:
            no_thumb.append(token)

    ordered = {fam: sorted(items, key=lambda e: e["token"]) for fam, items in families.items() if families[fam]}
    with open(DATA_OUT, "w", encoding="utf-8") as f:
        json.dump(ordered, f, indent=2)
        f.write("\n")

    total = sum(len(v) for v in ordered.values())
    print(f"[surfn] {total} variants across {len(ordered)} families -> {path.relpath(DATA_OUT, SCRIPT_DIR)}")
    print(f"[surfn] thumbnails -> {path.relpath(THUMB_DIR, SCRIPT_DIR)}/<token>.png")
    if no_thumb:
        print(f"[surfn] no folder preview for: {', '.join(no_thumb)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
