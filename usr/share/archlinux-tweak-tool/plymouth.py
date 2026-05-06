import os
import subprocess


def list_themes():
    themes_dir = "/usr/share/plymouth/themes"
    try:
        return sorted(
            d for d in os.listdir(themes_dir)
            if os.path.isdir(os.path.join(themes_dir, d))
        )
    except OSError:
        return []


def get_current_theme():
    try:
        result = subprocess.run(
            ["plymouth-set-default-theme"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def list_available_packages():
    try:
        all_pkgs = set(subprocess.run(
            ["pacman", "-Ssq", "^plymouth-theme"],
            capture_output=True, text=True
        ).stdout.strip().splitlines())
        installed = set(subprocess.run(
            ["pacman", "-Qq"],
            capture_output=True, text=True
        ).stdout.strip().splitlines())
        return sorted(all_pkgs - installed)
    except Exception:
        return []
