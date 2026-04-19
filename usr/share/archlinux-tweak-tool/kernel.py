# ============================================================
# Authors: Erik Dubois
# ============================================================

import functions as fn
import subprocess


KERNELS = [
    {
        "pkg": "linux",
        "headers": "linux-headers",
        "label": "Linux",
        "description": "Vanilla Arch kernel",
        "group": "Standard Arch",
        "url": "https://github.com/archlinux/linux",
    },
    {
        "pkg": "linux-lts",
        "headers": "linux-lts-headers",
        "label": "Linux LTS",
        "description": "Long-term support kernel",
        "group": "Standard Arch",
        "url": "https://www.kernel.org/",
    },
    {
        "pkg": "linux-zen",
        "headers": "linux-zen-headers",
        "label": "Linux Zen",
        "description": "Tuned for desktop responsiveness",
        "group": "Standard Arch",
        "url": "https://github.com/zen-kernel/zen-kernel",
    },
    {
        "pkg": "linux-hardened",
        "headers": "linux-hardened-headers",
        "label": "Linux Hardened",
        "description": "Security-focused kernel",
        "group": "Standard Arch",
        "url": "https://github.com/anthraxx/linux-hardened",
    },
    {
        "pkg": "linux-rt",
        "headers": "linux-rt-headers",
        "label": "Linux RT",
        "description": "Real-time kernel",
        "group": "Standard Arch",
        "url": "https://wiki.linuxfoundation.org/realtime/start",
    },
    {
        "pkg": "linux-cachyos",
        "headers": "linux-cachyos-headers",
        "label": "Linux CachyOS",
        "description": "CachyOS default kernel",
        "requires_chaotic": True,
        "group": "CachyOS",
        "url": "https://github.com/CachyOS/linux-cachyos",
    },
    {
        "pkg": "linux-cachyos-bore",
        "headers": "linux-cachyos-bore-headers",
        "label": "Linux CachyOS BORE",
        "description": "CachyOS with BORE scheduler",
        "requires_chaotic": True,
        "group": "CachyOS",
        "url": "https://github.com/CachyOS/linux-cachyos",
    },
    {
        "pkg": "linux-cachyos-lts",
        "headers": "linux-cachyos-lts-headers",
        "label": "Linux CachyOS LTS",
        "description": "CachyOS long-term support kernel",
        "requires_chaotic": True,
        "group": "CachyOS",
        "url": "https://github.com/CachyOS/linux-cachyos",
    },
    {
        "pkg": "linux-cachyos-rc",
        "headers": "linux-cachyos-rc-headers",
        "label": "Linux CachyOS RC",
        "description": "CachyOS release candidate kernel",
        "requires_chaotic": True,
        "group": "CachyOS",
        "url": "https://github.com/CachyOS/linux-cachyos",
    },
    {
        "pkg": "linux-cjktty",
        "headers": "linux-cjktty-headers",
        "label": "Linux CJKTTY",
        "description": "CachyOS kernel with CJK TTY font support",
        "requires_chaotic": True,
        "group": "CachyOS",
        "url": "https://github.com/CachyOS/linux-cachyos",
    },
    {
        "pkg": "linux-xanmod-lts",
        "headers": "linux-xanmod-lts-headers",
        "label": "Linux Xanmod LTS",
        "description": "Xanmod long-term support kernel",
        "requires_chaotic": True,
        "group": "Xanmod",
        "url": "https://xanmod.org/",
    },
    {
        "pkg": "linux-xanmod-rt",
        "headers": "linux-xanmod-rt-headers",
        "label": "Linux Xanmod RT",
        "description": "Xanmod real-time kernel",
        "requires_chaotic": True,
        "group": "Xanmod",
        "url": "https://xanmod.org/",
    },
    {
        "pkg": "linux-xanmod-x64v2",
        "headers": "linux-xanmod-x64v2-headers",
        "label": "Linux Xanmod x64v2",
        "description": "Xanmod optimized for x86-64-v2 (post-2009 CPUs)",
        "requires_chaotic": True,
        "group": "Xanmod",
        "url": "https://xanmod.org/",
    },
    {
        "pkg": "linux-xanmod-x64v3",
        "headers": "linux-xanmod-x64v3-headers",
        "label": "Linux Xanmod x64v3",
        "description": "Xanmod optimized for x86-64-v3 (Haswell+)",
        "requires_chaotic": True,
        "group": "Xanmod",
        "url": "https://xanmod.org/",
    },
    {
        "pkg": "linux-xanmod-edge-x64v3",
        "headers": "linux-xanmod-edge-x64v3-headers",
        "label": "Linux Xanmod Edge x64v3",
        "description": "Xanmod bleeding-edge, x86-64-v3",
        "requires_chaotic": True,
        "group": "Xanmod",
        "url": "https://xanmod.org/",
    },
    {
        "pkg": "linux-lqx",
        "headers": "linux-lqx-headers",
        "label": "Linux Liquorix",
        "description": "Desktop/multimedia optimized kernel",
        "requires_chaotic": True,
        "group": "Liquorix",
        "url": "https://liquorix.net/",
    },
    {
        "pkg": "linux-mainline",
        "headers": "linux-mainline-headers",
        "label": "Linux Mainline",
        "description": "Latest upstream mainline kernel",
        "requires_chaotic": True,
        "group": "Mainline",
        "url": "https://www.kernel.org/",
    },
    {
        "pkg": "linux-mainline-x64v3",
        "headers": "linux-mainline-x64v3-headers",
        "label": "Linux Mainline x64v3",
        "description": "Mainline optimized for x86-64-v3",
        "requires_chaotic": True,
        "group": "Mainline",
        "url": "https://www.kernel.org/",
    },
    {
        "pkg": "linux-lts515",
        "headers": "linux-lts515-headers",
        "label": "Linux LTS 5.15",
        "description": "Long-term support kernel 5.15",
        "requires_chaotic": True,
        "group": "Specific LTS versions",
        "url": "https://www.kernel.org/",
    },
    {
        "pkg": "linux-lts61",
        "headers": "linux-lts61-headers",
        "label": "Linux LTS 6.1",
        "description": "Long-term support kernel 6.1",
        "requires_chaotic": True,
        "group": "Specific LTS versions",
        "url": "https://www.kernel.org/",
    },
    {
        "pkg": "linux-lts612",
        "headers": "linux-lts612-headers",
        "label": "Linux LTS 6.12",
        "description": "Long-term support kernel 6.12",
        "requires_chaotic": True,
        "group": "Specific LTS versions",
        "url": "https://www.kernel.org/",
    },
    {
        "pkg": "linux-lts66",
        "headers": "linux-lts66-headers",
        "label": "Linux LTS 6.6",
        "description": "Long-term support kernel 6.6",
        "requires_chaotic": True,
        "group": "Specific LTS versions",
        "url": "https://www.kernel.org/",
    },
    # ── x86-64 microarch level builds ────────────────────────────
    {
        "pkg": "linux-x64v2",
        "headers": "linux-x64v2-headers",
        "label": "Linux x64v2",
        "description": "Arch kernel optimized for x86-64-v2",
        "requires_chaotic": True,
        "group": "x86-64 microarch level builds",
        "url": "https://github.com/archlinux/linux",
    },
    {
        "pkg": "linux-x64v3",
        "headers": "linux-x64v3-headers",
        "label": "Linux x64v3",
        "description": "Arch kernel optimized for x86-64-v3 (Haswell+)",
        "requires_chaotic": True,
        "group": "x86-64 microarch level builds",
        "url": "https://github.com/archlinux/linux",
    },
    {
        "pkg": "linux-x64v4",
        "headers": "linux-x64v4-headers",
        "label": "Linux x64v4",
        "description": "Arch kernel optimized for x86-64-v4 (AVX-512)",
        "requires_chaotic": True,
        "group": "x86-64 microarch level builds",
        "url": "https://github.com/archlinux/linux",
    },
    # ── AMD Zen builds ───────────────────────────────────────────
    {
        "pkg": "linux-znver2",
        "headers": "linux-znver2-headers",
        "label": "Linux Znver2",
        "description": "Optimized for AMD Zen 2 CPUs",
        "requires_chaotic": True,
        "group": "AMD Zen builds",
        "url": "https://github.com/archlinux/linux",
    },
    {
        "pkg": "linux-znver3",
        "headers": "linux-znver3-headers",
        "label": "Linux Znver3",
        "description": "Optimized for AMD Zen 3 CPUs",
        "requires_chaotic": True,
        "group": "AMD Zen builds",
        "url": "https://github.com/archlinux/linux",
    },
    {
        "pkg": "linux-znver4",
        "headers": "linux-znver4-headers",
        "label": "Linux Znver4",
        "description": "Optimized for AMD Zen 4 CPUs",
        "requires_chaotic": True,
        "group": "AMD Zen builds",
        "url": "https://github.com/archlinux/linux",
    },
    {
        "pkg": "linux-znver5",
        "headers": "linux-znver5-headers",
        "label": "Linux Znver5",
        "description": "Optimized for AMD Zen 5 CPUs",
        "requires_chaotic": True,
        "group": "AMD Zen builds",
        "url": "https://github.com/archlinux/linux",
    },
    # ── Specialty ────────────────────────────────────────────────
    {
        "pkg": "linux-nitrous",
        "headers": "linux-nitrous-headers",
        "label": "Linux Nitrous",
        "description": "Performance-tuned kernel",
        "requires_chaotic": True,
        "group": "Specialty",
        "url": "https://github.com/archlinux/linux",
    },
    {
        "pkg": "linux-tachyon",
        "headers": "linux-tachyon-headers",
        "label": "Linux Tachyon",
        "description": "High-performance kernel",
        "requires_chaotic": True,
        "group": "Specialty",
        "url": "https://github.com/archlinux/linux",
    },
    {
        "pkg": "linux-vfio",
        "headers": "linux-vfio-headers",
        "label": "Linux VFIO",
        "description": "Kernel with VFIO/GPU passthrough patches",
        "requires_chaotic": True,
        "group": "Specialty",
        "url": "https://github.com/archlinux/linux",
    },
    {
        "pkg": "linux-vfio-lts",
        "headers": "linux-vfio-lts-headers",
        "label": "Linux VFIO LTS",
        "description": "LTS kernel with VFIO/GPU passthrough patches",
        "requires_chaotic": True,
        "group": "Specialty",
        "url": "https://github.com/archlinux/linux",
    },
    {
        "pkg": "linux-vfio-x64v3",
        "headers": "linux-vfio-x64v3-headers",
        "label": "Linux VFIO x64v3",
        "description": "VFIO kernel optimized for x86-64-v3",
        "requires_chaotic": True,
        "group": "Specialty",
        "url": "https://github.com/archlinux/linux",
    },
]


def get_running_kernel():
    """Return the running kernel package name, e.g. 'linux' or 'linux-lts'."""
    try:
        uname = subprocess.check_output(["uname", "-r"], text=True).strip()
        result = subprocess.check_output(
            ["pacman", "-Qo", f"/usr/lib/modules/{uname}/pkgbase"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        # Output format: "/path/to/file is owned by package-name version"
        # Extract package name (second to last element)
        parts = result.split()
        if len(parts) >= 2:
            return parts[-2]
        return None
    except Exception:
        return None


def get_installed_kernels():
    """Return dict of {pkg_name: version} for all installed packages (one pacman call)."""
    try:
        output = subprocess.check_output(["pacman", "-Q"], text=True, stderr=subprocess.DEVNULL)
        result = {}
        for line in output.splitlines():
            parts = line.split()
            if len(parts) == 2:
                result[parts[0]] = parts[1]
        return result
    except Exception:
        return {}


def is_chaotic_aur_enabled():
    try:
        with open("/etc/pacman.conf", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() == "[chaotic-aur]":
                    return True
    except Exception:
        pass
    return False


def get_boot_entries():
    """Return list of (id, title) tuples from bootctl list."""
    try:
        output = subprocess.check_output(
            ["bootctl", "list", "--no-pager"],
            text=True, stderr=subprocess.DEVNULL
        )
        entries = []
        current_id = None
        current_title = None
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("id:"):
                current_id = line.split(":", 1)[1].strip()
            elif line.startswith("title:") and current_id:
                current_title = line.split(":", 1)[1].strip()
                entries.append((current_id, current_title))
                current_id = None
                current_title = None
        return entries
    except Exception:
        return []


def get_default_boot_entry():
    """Return the current default boot entry ID."""
    try:
        output = subprocess.check_output(
            ["bootctl", "status", "--no-pager"],
            text=True, stderr=subprocess.DEVNULL
        )
        for line in output.splitlines():
            if "Default Entry:" in line or "default entry:" in line.lower():
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return None


def set_default_boot_entry(entry_id):
    """Set the default boot entry using bootctl set-default."""
    return subprocess.Popen(
        ["bootctl", "set-default", entry_id],
        shell=False
    )


INSTALL_SCRIPT = "/usr/share/archlinux-tweak-tool/data/any/install-kernel"
REMOVE_SCRIPT = "/usr/share/archlinux-tweak-tool/data/any/remove-kernel"


def install_kernel(self, pkg, headers):
    fn.install_package(self, "alacritty")
    return subprocess.Popen(
        ["alacritty", "--hold", "-e", INSTALL_SCRIPT, pkg, headers],
        shell=False,
    )


def remove_kernel(self, pkg, headers):
    fn.install_package(self, "alacritty")
    return subprocess.Popen(
        ["alacritty", "--hold", "-e", REMOVE_SCRIPT, pkg, headers],
        shell=False,
    )
