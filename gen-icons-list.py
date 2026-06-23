#!/usr/bin/env python3
"""Generate the Surfn + Neo Candy icon-theme tables and folder thumbnails for the Icons page.

Run automatically by up.sh. Both families show a small folder preview (the theme's real
folder icon) beside each checkbox, so they stay in sync without hand-editing icons.py.

Surfn ships as ~50 standalone colour-variant packages (sources in ~/EDU/surfn*, recipes in
~/KIRO-PKG-BUILD-ICONS); each records token / package / family. Neo Candy is a fixed set of 9
packages whose sources are not all available as repos, so its folder icons are read from the
installed theme dirs in /usr/share/icons (fallback to ~/EDU sources).

Folder previews are rendered by loading the theme's canonical folder icon (folder.png or
folder.svg — PNG, then scalable, then largest numbered size, since small numbered folders are
often the `currentColor` symbolic outline) and scaling it to a PNG thumbnail via GdkPixbuf.

Outputs:
  * usr/share/archlinux-tweak-tool/data/surfn_families.json   + images/surfn/<token>.png
  * usr/share/archlinux-tweak-tool/data/neocandy_list.json    + images/neocandy/<token>.png
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
DATA_DIR = path.join(APP_DIR, "data")
IMAGES_DIR = path.join(APP_DIR, "images")
THUMB_SIZE = 28

HOME = path.expanduser("~")
SRC_ROOT = os.environ.get("SURFN_SRC_ROOT", path.join(HOME, "EDU"))
PKG_ROOT = os.environ.get("SURFN_PKG_ROOT", path.join(HOME, "KIRO-PKG-BUILD-ICONS"))
SYS_ICONS = "/usr/share/icons"

# ── Surfn ────────────────────────────────────────────────────────────────────
# Display order of the families; tokens within a family are sorted alphabetically.
FAMILY_ORDER = ["Mint-X", "Mint-Y", "Tela", "Plasma", "Numix", "Papirus", "Arc / Breeze", "Other"]
ARC_BREEZE = {"arc-breeze", "breeze-arc", "breeze-dark"}

# ── Neo Candy ────────────────────────────────────────────────────────────────
# Fixed set: (token, package, label, [theme-dir candidates]). Sources aren't all in ~/EDU,
# so folder icons are taken from the installed theme dir (first candidate that has a folder).
NEOCANDY = [
    ("neo-candy", "neo-candy-icons-git", "Neo Candy Icons", ["neo-candy-icons", "al-candy-icons", "candy-icons"]),
    ("neo-candy-arc", "kiro-neo-candy-arc", "Neo Candy Arc", ["edu-neo-candy-arc"]),
    ("neo-candy-arc-mint-grey", "kiro-neo-candy-arc-mint-grey", "Neo Candy Arc Mint Grey", ["edu-neo-candy-arc-mint-grey"]),
    ("neo-candy-arc-mint-red", "kiro-neo-candy-arc-mint-red", "Neo Candy Arc Mint Red", ["edu-neo-candy-arc-mint-red"]),
    ("neo-candy-tela", "kiro-neo-candy-tela", "Neo Candy Tela", ["edu-neo-candy-tela"]),
    ("papirus-dark-tela", "kiro-papirus-dark-tela", "Papirus Dark Tela", ["edu-papirus-dark-tela"]),
    ("papirus-dark-tela-grey", "kiro-papirus-dark-tela-grey", "Papirus Dark Tela Grey", ["edu-papirus-dark-tela-grey"]),
    ("vimix-dark-tela", "kiro-vimix-dark-tela", "Vimix Dark Tela", ["edu-vimix-dark-tela"]),
    ("neo-candy-qogir", "kiro-neo-candy-qogir", "Neo Candy Qogir", ["edu-neo-candy-qogir"]),
]

_THEME_DIR_INDEX = {}


def _classify(token):
    rest = token[len("surfn-"):] if token.startswith("surfn-") else token
    if rest.startswith("mint-x"):
        return "Mint-X"
    if rest.startswith("mint-y"):
        return "Mint-Y"
    if rest.startswith("tela"):
        return "Tela"
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


def _icon_size(p):
    """Sort weight for a folder icon path: scalable (full-colour vector) beats numbered sizes."""
    if "scalable" in p.lower():
        return 10000
    m = re.search(r"/(\d+)(?:@\d+x)?/", p)
    return int(m.group(1)) if m else 0


def _folder_in_root(theme_root):
    """Return the best folder.png/folder.svg under an absolute theme root, or None."""
    if not path.isdir(theme_root):
        return None
    hits = []
    for dirpath, _dirnames, filenames in os.walk(theme_root):
        for fname in filenames:
            if fname in ("folder.png", "folder.svg"):
                hits.append(path.join(dirpath, fname))
    if not hits:
        return None
    # Prefer PNG, then the largest/scalable size for a crisp, full-colour thumbnail.
    hits.sort(key=lambda p: (p.endswith(".png"), _icon_size(p)), reverse=True)
    return hits[0]


def _canonical_folder(token, theme_dir, _seen=None):
    """Surfn folder icon, following index.theme Inherits to a parent surfn theme when absent."""
    if _seen is None:
        _seen = set()
    if theme_dir in _seen:
        return None
    _seen.add(theme_dir)

    theme_root = path.join(SRC_ROOT, token, "usr/share/icons", theme_dir)
    found = _folder_in_root(theme_root)
    if found:
        return found

    index = path.join(theme_root, "index.theme")
    try:
        with open(index, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("Inherits="):
                    for parent in line.split("=", 1)[1].split(","):
                        parent_token = _THEME_DIR_INDEX.get(parent.strip())
                        if parent_token:
                            found = _canonical_folder(parent_token, parent.strip(), _seen)
                            if found:
                                return found
    except OSError:
        pass
    return None


def _discover_surfn_tokens():
    tokens = []
    for name in sorted(os.listdir(SRC_ROOT)):
        if name != "surfn" and not name.startswith("surfn-"):
            continue
        if not path.isdir(path.join(SRC_ROOT, name, "usr/share/icons")):
            continue
        tokens.append(name)
    return tokens


def _write_thumbnail(folder_path, thumb_dir, token):
    out = path.join(thumb_dir, token + ".png")
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(folder_path, THUMB_SIZE, THUMB_SIZE)
    pixbuf.savev(out, "png", [], [])
    return out


def _generate_surfn():
    if not path.isdir(SRC_ROOT):
        print(f"[surfn] source root not found: {SRC_ROOT} — skipping", file=sys.stderr)
        return
    thumb_dir = path.join(IMAGES_DIR, "surfn")
    data_out = path.join(DATA_DIR, "surfn_families.json")
    os.makedirs(thumb_dir, exist_ok=True)

    tokens = _discover_surfn_tokens()
    for token in tokens:
        td = _theme_dir(token)
        if td:
            _THEME_DIR_INDEX[td] = token

    families = {fam: [] for fam in FAMILY_ORDER}
    no_thumb = []
    for token in tokens:
        theme_dir = _theme_dir(token)
        families[_classify(token)].append({"token": token, "package": _package_name(token)})

        folder = _canonical_folder(token, theme_dir) if theme_dir else None
        if not folder:
            base_dir = _theme_dir("surfn")
            if base_dir:
                folder = _canonical_folder("surfn", base_dir)
        if folder:
            try:
                _write_thumbnail(folder, thumb_dir, token)
            except Exception as error:  # noqa: BLE001 - bad SVG/PNG must not abort the run
                no_thumb.append(f"{token} ({error})")
        else:
            no_thumb.append(token)

    ordered = {fam: sorted(items, key=lambda e: e["token"]) for fam, items in families.items() if families[fam]}
    with open(data_out, "w", encoding="utf-8") as f:
        json.dump(ordered, f, indent=2)
        f.write("\n")

    total = sum(len(v) for v in ordered.values())
    print(f"[surfn] {total} variants across {len(ordered)} families -> {path.relpath(data_out, SCRIPT_DIR)}")
    if no_thumb:
        print(f"[surfn] no folder preview for: {', '.join(no_thumb)}", file=sys.stderr)


def _neocandy_folder(theme_dirs):
    for dir_name in theme_dirs:
        for root in (path.join(SYS_ICONS, dir_name), path.join(SRC_ROOT, dir_name, "usr/share/icons", dir_name)):
            found = _folder_in_root(root)
            if found:
                return found
    return None


def _generate_neocandy():
    thumb_dir = path.join(IMAGES_DIR, "neocandy")
    data_out = path.join(DATA_DIR, "neocandy_list.json")
    os.makedirs(thumb_dir, exist_ok=True)

    entries = []
    no_thumb = []
    for token, package, label, theme_dirs in NEOCANDY:
        entries.append({"token": token, "package": package, "label": label})
        folder = _neocandy_folder(theme_dirs)
        if folder:
            try:
                _write_thumbnail(folder, thumb_dir, token)
            except Exception as error:  # noqa: BLE001 - bad SVG/PNG must not abort the run
                no_thumb.append(f"{token} ({error})")
        else:
            no_thumb.append(token)

    with open(data_out, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
        f.write("\n")

    print(f"[neocandy] {len(entries)} themes -> {path.relpath(data_out, SCRIPT_DIR)}")
    if no_thumb:
        print(
            f"[neocandy] no folder preview for: {', '.join(no_thumb)} (install the theme, then rerun)",
            file=sys.stderr,
        )


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    _generate_surfn()
    _generate_neocandy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
