# ============================================================
# Authors: Erik Dubois
# ============================================================
# Distro-specific requirements for the kernel manager tab.
# Add a new entry here when a distro needs packages that are
# not available in standard Arch repos.
# ============================================================

import subprocess
import functions as fn


# Each distro maps to a list of required packages.
# Missing packages trigger a console warning + in-app notice + install dialog.
DISTRO_REQUIREMENTS = {
    "arch": [
        {
            "pkg": "pacman-hook-kernel-install",
            "reason": "provides /usr/lib/modules/*/pkgbase — needed for running kernel detection",
            "repo": "nemesis-repo",
        }
    ],
    # Other distros added here as needed.
    # "manjaro": [...],
    # "artix": [...],
}


def get_missing_requirements():
    """Return list of missing required packages for the current distro."""
    requirements = DISTRO_REQUIREMENTS.get(fn.distr, [])
    missing = []
    for req in requirements:
        try:
            result = subprocess.run(["pacman", "-Q", req["pkg"]], capture_output=True)
            if result.returncode != 0:
                missing.append(req)
        except Exception:
            pass
    return missing
