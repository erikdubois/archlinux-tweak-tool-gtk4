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
