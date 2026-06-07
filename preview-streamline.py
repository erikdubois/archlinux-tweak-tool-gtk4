#!/usr/bin/env python3
"""Standalone visual preview of the Streamline page — DEV TOOL, not packaged.

Renders the real streamline_gui.gui() in its own GTK4 window so you can see the
layout without launching ATT, without --dev, and without root. It injects a
lightweight stand-in for the heavy `functions` module, so:

  * categories + packages come from the real data/streamline_packages.txt
  * the installed filter runs a real `pacman -Q` (shows YOUR installed apps)
  * "Remove selected" shows the real `pacman -Rns --print` cascade dialog,
    but performs NO actual removal (it just re-renders) — safe to click

Run it as your normal user from the repo root:

    python3 preview-streamline.py
"""

import datetime
import os.path
import subprocess
import sys
import threading
import types

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.join(REPO_ROOT, "usr/share/archlinux-tweak-tool")
DATA_FILE = os.path.join(APP_DIR, "data/streamline_packages.txt")


def _load_categories():
    categories = {}
    current = None
    with open(DATA_FILE, encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("###"):
                current = stripped.lstrip("#").strip()
                categories[current] = []
            elif stripped and not stripped.startswith("#") and current is not None:
                categories[current].append(stripped)
    return categories


def _check_packages_installed(packages):
    result = {p: False for p in packages}
    try:
        out = subprocess.check_output(["pacman", "-Q"], text=True, stderr=subprocess.DEVNULL)
        installed = {line.split()[0] for line in out.splitlines() if line.strip()}
        for pkg in result:
            result[pkg] = pkg in installed
    except Exception:
        pass
    return result


def _log(msg):
    print(f"[preview] {msg}")


def _make_fake_functions():
    """A stand-in `functions` module with just what streamline*.py touch."""
    fn = types.ModuleType("functions")
    fn.path = os.path
    fn.subprocess = subprocess
    fn.threading = threading
    fn.datetime = datetime
    fn.att_streamline_dir = os.path.expanduser("~/.config/archlinux-tweak-tool/streamline/")
    fn.load_streamline_categories = _load_categories
    fn.check_packages_installed = _check_packages_installed
    fn.show_in_app_notification = lambda _self, msg: _log(f"notify: {msg}")
    fn.invalidate_pkg_cache = lambda: None
    fn.makedirs = os.makedirs
    fn.permissions = lambda *_a: None
    for name in ("log_section", "log_subsection", "log_info", "log_success", "log_warn", "log_error", "debug_print"):
        setattr(fn, name, lambda msg, *_a, **_k: _log(msg))
    # Removal/install are stubbed — preview never actually changes the system.
    fn.launch_pacman_remove_in_terminal = lambda pkgs: _log(f"[stub] would run: pacman -R {pkgs}") or None
    fn.launch_pacman_remove_recursive_in_terminal = lambda pkgs: _log(f"[stub] would run: pacman -Rns {pkgs}") or None
    fn.get_aur_helper = lambda: "yay"
    fn.launch_aur_install_in_terminal = lambda helper, pkgs: _log(f"[stub] would run: {helper} -S {pkgs}") or None
    fn.launch_pacman_install_in_terminal = lambda pkgs: _log(f"[stub] would run: pacman -S {pkgs}") or None
    return fn


def on_activate(app):
    win = Gtk.ApplicationWindow(application=app, title="Streamline — preview (not shipped)")
    win.set_default_size(720, 820)
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    win.set_child(box)
    import streamline_gui

    streamline_gui.gui(win, Gtk, box, sys.modules["functions"])
    win.present()


def main():
    sys.path.insert(0, APP_DIR)
    sys.modules["functions"] = _make_fake_functions()
    app = Gtk.Application(application_id="be.kiroproject.att.streamline.preview")
    app.connect("activate", on_activate)
    app.run(None)


if __name__ == "__main__":
    main()
