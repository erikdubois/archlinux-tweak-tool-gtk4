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
        "cpu_compat": {"flags": ["sse4_2", "popcnt", "ssse3"]},
    },
    {
        "pkg": "linux-xanmod-x64v3",
        "headers": "linux-xanmod-x64v3-headers",
        "label": "Linux Xanmod x64v3",
        "description": "Xanmod optimized for x86-64-v3 (Haswell+)",
        "requires_chaotic": True,
        "group": "Xanmod",
        "url": "https://xanmod.org/",
        "cpu_compat": {"flags": ["avx", "avx2", "bmi1", "bmi2"]},
    },
    {
        "pkg": "linux-xanmod-edge-x64v3",
        "headers": "linux-xanmod-edge-x64v3-headers",
        "label": "Linux Xanmod Edge x64v3",
        "description": "Xanmod bleeding-edge, x86-64-v3",
        "requires_chaotic": True,
        "group": "Xanmod",
        "url": "https://xanmod.org/",
        "cpu_compat": {"flags": ["avx", "avx2", "bmi1", "bmi2"]},
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
        "cpu_compat": {"flags": ["avx", "avx2", "bmi1", "bmi2"]},
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
        "cpu_compat": {"flags": ["sse4_2", "popcnt", "ssse3"]},
    },
    {
        "pkg": "linux-x64v3",
        "headers": "linux-x64v3-headers",
        "label": "Linux x64v3",
        "description": "Arch kernel optimized for x86-64-v3 (Haswell+)",
        "requires_chaotic": True,
        "group": "x86-64 microarch level builds",
        "url": "https://github.com/archlinux/linux",
        "cpu_compat": {"flags": ["avx", "avx2", "bmi1", "bmi2"]},
    },
    {
        "pkg": "linux-x64v4",
        "headers": "linux-x64v4-headers",
        "label": "Linux x64v4",
        "description": "Arch kernel optimized for x86-64-v4 (AVX-512)",
        "requires_chaotic": True,
        "group": "x86-64 microarch level builds",
        "url": "https://github.com/archlinux/linux",
        "cpu_compat": {"flags": ["avx512f", "avx512bw", "avx512cd", "avx512dq", "avx512vl"]},
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
        "cpu_compat": {"vendor": "AMD", "min_zen": 2},
    },
    {
        "pkg": "linux-znver3",
        "headers": "linux-znver3-headers",
        "label": "Linux Znver3",
        "description": "Optimized for AMD Zen 3 CPUs",
        "requires_chaotic": True,
        "group": "AMD Zen builds",
        "url": "https://github.com/archlinux/linux",
        "cpu_compat": {"vendor": "AMD", "min_zen": 3},
    },
    {
        "pkg": "linux-znver4",
        "headers": "linux-znver4-headers",
        "label": "Linux Znver4",
        "description": "Optimized for AMD Zen 4 CPUs",
        "requires_chaotic": True,
        "group": "AMD Zen builds",
        "url": "https://github.com/archlinux/linux",
        "cpu_compat": {"vendor": "AMD", "min_zen": 4},
    },
    {
        "pkg": "linux-znver5",
        "headers": "linux-znver5-headers",
        "label": "Linux Znver5",
        "description": "Optimized for AMD Zen 5 CPUs",
        "requires_chaotic": True,
        "group": "AMD Zen builds",
        "url": "https://github.com/archlinux/linux",
        "cpu_compat": {"vendor": "AMD", "min_zen": 5},
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
        "cpu_compat": {"flags": ["avx", "avx2", "bmi1", "bmi2"]},
    },
]


def get_cpu_info():
    """Return dict with vendor, flags (set), family, model from /proc/cpuinfo."""
    info = {"vendor": "", "flags": set(), "family": 0, "model": 0}
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("vendor_id"):
                    info["vendor"] = line.split(":")[1].strip()
                elif line.startswith("cpu family"):
                    info["family"] = int(line.split(":")[1].strip())
                elif line.startswith("model\t"):
                    info["model"] = int(line.split(":")[1].strip())
                elif line.startswith("flags"):
                    info["flags"] = set(line.split(":")[1].strip().split())
                if info["vendor"] and info["flags"] and info["family"] and info["model"]:
                    break
    except Exception:
        pass
    return info


def _amd_zen_generation(family, model):
    """Return AMD Zen generation number (1-5) or 0 if not Zen."""
    if family == 23:   # 0x17 — Zen / Zen+ / Zen 2
        return 2 if model >= 0x31 else 1
    if family == 24:   # 0x18 — some Zen 2 mobile
        return 2
    if family == 25:   # 0x19 — Zen 3 / Zen 4
        return 4 if model >= 0x60 else 3
    if family >= 26:   # 0x1A — Zen 5+
        return 5
    return 0


def is_kernel_compatible(k, cpu_info):
    """Return True if the kernel can run on the given CPU."""
    compat = k.get("cpu_compat")
    if not compat:
        return True

    # Flag check (x86-64 microarch levels)
    required_flags = compat.get("flags", [])
    if required_flags and not set(required_flags).issubset(cpu_info["flags"]):
        return False

    # Vendor check
    vendor = compat.get("vendor", "")
    if vendor and vendor not in cpu_info["vendor"]:
        return False

    # AMD Zen generation check
    min_zen = compat.get("min_zen", 0)
    if min_zen:
        gen = _amd_zen_generation(cpu_info["family"], cpu_info["model"])
        if gen < min_zen:
            return False

    return True


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


def is_systemd_boot():
    """Return True if systemd-boot is the active bootloader."""
    try:
        result = subprocess.run(
            ["bootctl", "is-installed"],
            capture_output=True,
        )
        return result.returncode == 0
    except Exception:
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
            elif line.startswith("title:"):
                current_title = line.split(":", 1)[1].strip().replace(" (default)", "")
            if current_id and current_title:
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
    """Set the default boot entry using bootctl set-default. Returns True on success."""
    try:
        result = subprocess.run(
            ["bootctl", "set-default", entry_id],
            shell=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            fn.log_error(f"bootctl set-default failed: {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        fn.log_error(f"set_default_boot_entry error: {e}")
        return False


def install_kernel(self, pkg, headers):
    """Install kernel and headers with detailed logging."""
    fn.log_subsection(f"Installing kernel: {pkg}")
    fn.debug_print(f"Headers: {headers}")
    script = f"""#!/bin/bash
tput setaf 6
echo "================================================================"
echo "  Installing kernel: {pkg}"
echo "  Headers: {headers}"
echo "================================================================"
tput sgr0

pacman -S "{pkg}" "{headers}" --noconfirm --needed
RESULT=$?

echo
if [ $RESULT -eq 0 ]; then
    tput setaf 2
    echo "================================================================"
    echo "  ✓ Successfully installed {pkg}"
    echo "================================================================"
    tput sgr0
else
    tput setaf 1
    echo "================================================================"
    echo "  ✗ Failed to install {pkg}"
    echo "================================================================"
    tput sgr0
fi

echo
echo "###############################################################################"
echo "###                DONE - YOU CAN CLOSE THIS WINDOW                        ####"
echo "###############################################################################"
read -p 'Press Enter to close...'
"""
    process = subprocess.Popen(["alacritty", "-e", "bash", "-c", script])
    fn.show_in_app_notification(self, f"Installing {pkg}...")
    return process


def remove_kernel(self, pkg, headers):
    """Remove kernel and headers with detailed logging."""
    fn.log_subsection(f"Removing kernel: {pkg}")
    fn.debug_print(f"Headers: {headers}")
    script = f"""#!/bin/bash
tput setaf 6
echo "================================================================"
echo "  Removing kernel: {pkg}"
echo "  Headers: {headers}"
echo "================================================================"
tput sgr0

pacman -R "{headers}" "{pkg}" --noconfirm 2>/dev/null || pacman -R "{pkg}" --noconfirm
RESULT=$?

echo
if [ $RESULT -eq 0 ]; then
    tput setaf 2
    echo "================================================================"
    echo "  ✓ Successfully removed {pkg}"
    echo "================================================================"
    tput sgr0
else
    tput setaf 1
    echo "================================================================"
    echo "  ✗ Failed to remove {pkg}"
    echo "================================================================"
    tput sgr0
fi

echo
echo "###############################################################################"
echo "###                DONE - YOU CAN CLOSE THIS WINDOW                        ####"
echo "###############################################################################"
read -p 'Press Enter to close...'
"""
    process = subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    fn.show_in_app_notification(self, f"Removing {pkg}...")
    return process
