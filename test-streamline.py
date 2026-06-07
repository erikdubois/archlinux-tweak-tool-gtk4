#!/usr/bin/env python3
"""Verification for streamline.py logic — DEV TOOL, not packaged.

Stubs the `functions` module so the logic is testable without GTK or root.
Covers: removed_packages (full list - installed), selected_packages (left
column), selected_reinstall (right column), and read_profile_file skipping the
'#' header. Run: python3 test-streamline.py  (exits non-zero on any failure).
"""

import os.path
import sys
import tempfile
import types

REPO_ROOT = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.join(REPO_ROOT, "usr/share/archlinux-tweak-tool")


class FakeCheck:
    def __init__(self, active):
        self._active = active

    def get_active(self):
        return self._active


def _make_fn(categories, installed_set):
    fn = types.ModuleType("functions")
    fn.load_streamline_categories = lambda: categories
    fn.check_packages_installed = lambda pkgs: {p: (p in installed_set) for p in pkgs}
    fn.path = os.path
    return fn


def main():
    sys.path.insert(0, APP_DIR)
    categories = {"BROWSERS": ["firefox", "brave-bin"], "ARCHIVE": ["p7zip", "unzip"]}
    installed = {"firefox", "unzip"}
    sys.modules["functions"] = _make_fn(categories, installed)
    import streamline

    # removed_packages = full list (in order) minus what's installed
    removed = streamline.removed_packages(object())
    assert removed == ["brave-bin", "p7zip"], removed

    # selected_packages reads the left/installed column checks
    obj = types.SimpleNamespace()
    obj.streamline_checks = [("firefox", FakeCheck(True)), ("unzip", FakeCheck(False))]
    assert streamline.selected_packages(obj) == ["firefox"]

    # selected_reinstall reads the right/already-removed column checks
    obj.streamline_reinstall_checks = [("brave-bin", FakeCheck(True)), ("p7zip", FakeCheck(False))]
    assert streamline.selected_reinstall(obj) == ["brave-bin"]

    # read_profile_file skips the '#' header and blank lines
    profile_path = os.path.join(tempfile.gettempdir(), "streamline-test-profile.txt")
    with open(profile_path, "w", encoding="utf-8") as f:
        f.write("# header line\n# another\n\nfirefox\nbrave-bin\n")
    assert streamline.read_profile_file(profile_path) == ["firefox", "brave-bin"]
    os.remove(profile_path)

    print("All streamline logic tests passed.")


if __name__ == "__main__":
    main()
