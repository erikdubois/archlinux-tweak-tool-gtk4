# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import datetime
import tempfile
from gi.repository import GLib  # noqa
import functions as fn
import desktopr

# Wayland window managers offered on the dedicated "Wayland" page.
#
# Only Hyprland is curated: installing it pulls the kiro-hyprland meta (config +
# full dependency stack) and seeds its config from /etc/skel. The others install
# the bare upstream package with no Kiro config yet (ready=False). dwl has no repo
# package — it stays a disabled "coming soon" row until packaged.
#
# Status detection is free: desktopr.check_desktop() scans /usr/share/wayland-sessions,
# so each entry's "key" matches the session .desktop name (hyprland → hyprland.desktop).
WAYLAND_WMS = [
    {
        "key": "hyprland",
        "label": "Hyprland",
        "backend": "aquamarine",
        "packages": ["kiro-hyprland"],
        "repo": "nemesis_repo",
        "skel": ["/etc/skel/.config/hypr", "/etc/skel/.config/waybar", "/etc/skel/.config/mako"],
        "ready": True,
        # Removal targets only Hyprland-SPECIFIC packages. Shared tools the install
        # pulled (waybar, mako, swaybg, rofi, grim, slurp, wl-clipboard, polkit-gnome,
        # network-manager-applet, pavucontrol, playerctl, wireplumber, brightnessctl)
        # are kept — XFCE/chadwm and other WMs rely on them. hyprland-tweak-tool is a
        # standalone app and is also left in place.
        "remove": ["kiro-hyprland", "hyprland", "hyprlock", "hypridle", "hyprpicker", "xdg-desktop-portal-hyprland"],
        "proc": "Hyprland",
    },
    {"key": "niri", "label": "niri", "backend": "smithay", "packages": ["niri"], "repo": "extra", "skel": [], "ready": False},
    {"key": "sway", "label": "sway", "backend": "wlroots 0.20", "packages": ["sway"], "repo": "extra", "skel": [], "ready": False},
    {"key": "river", "label": "river", "backend": "wlroots 0.20", "packages": ["river"], "repo": "extra", "skel": [], "ready": False},
    {"key": "wayfire", "label": "wayfire", "backend": "wlroots 0.19", "packages": ["wayfire"], "repo": "extra", "skel": [], "ready": False},
    {"key": "labwc", "label": "labwc", "backend": "wlroots 0.20", "packages": ["labwc"], "repo": "extra", "skel": [], "ready": False},
    {
        "key": "dwl",
        "label": "dwl",
        "backend": "wlroots (AUR)",
        "packages": [],
        "repo": "aur",
        "skel": [],
        "ready": False,
        "disabled": True,
    },
]


def get_wm(key):
    """Return the WAYLAND_WMS entry for a key, or None."""
    return next((wm for wm in WAYLAND_WMS if wm["key"] == key), None)


def selection_needs_nemesis(keys):
    """True if any selected WM ships from nemesis_repo (currently only Hyprland)."""
    return any((wm := get_wm(k)) and wm["repo"] == "nemesis_repo" for k in keys)


def installed_wayland_sessions():
    """Return sorted names of installed /usr/share/wayland-sessions entries (sans .desktop)."""
    wayland_dir = "/usr/share/wayland-sessions"
    if not fn.path.exists(wayland_dir):
        return []
    return sorted(f[:-8] for f in fn.listdir(wayland_dir) if f.endswith(".desktop"))


def _backup_overwritten_configs(skel_dirs):
    to_backup = [fn.path.basename(p) for p in skel_dirs if fn.path.exists(fn.home + "/.config/" + fn.path.basename(p))]
    if not to_backup:
        fn.log_info("Selection overwrites no existing configs — nothing to back up")
        return
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    backup_dir = fn.home + "/.config-att/config-att-" + timestamp
    fn.log_info(f"Backing up {len(to_backup)} config(s) the install will overwrite to {backup_dir}")
    fn.makedirs(backup_dir)
    for name in to_backup:
        fn.log_info(f"Backing up ~/.config/{name}")
        fn.copy_func(fn.home + "/.config/" + name, backup_dir + "/" + name, isdir=True)
    fn.permissions(fn.home + "/.config-att")


def install_wayland_selection(self, keys):
    """Install the selected Wayland WMs in one terminal, then seed configs for curated ones.

    Runs as a daemon-thread target. Mirrors desktopr.install_desktop for a set of WMs:
    union the packages, scoped-backup the configs about to be overwritten, run one
    pkexec pacman install, then copy /etc/skel configs home for the curated (ready) WMs.
    """
    selected = [wm for k in keys if (wm := get_wm(k)) and not wm.get("disabled")]
    if not selected:
        fn.log_warn("install_wayland_selection called with no installable WMs")
        return

    names = ", ".join(wm["label"] for wm in selected)
    fn.log_section(f"Installing Wayland WM(s): {names}")
    fn.show_in_app_notification(self, f"Opening terminal for: {names}")

    packages = [pkg for wm in selected for pkg in wm["packages"]]
    skel_dirs = [d for wm in selected if wm["ready"] for d in wm["skel"]]

    _backup_overwritten_configs(skel_dirs)

    fn.log_subsection(f"Installing {len(packages)} packages")
    fn.debug_print("Packages to install: " + str(packages))

    log_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".log", delete=False)
    log_path = log_file.name
    log_file.close()

    package_list = "\n".join([f"  • {pkg}" for pkg in packages])
    install_cmd = (
        f"( "
        f"RED=$(tput setaf 1); RESET=$(tput sgr0); "
        f"echo 'Installing Wayland window manager(s): {names}' && "
        f"echo '' && "
        f"echo 'The following packages will be installed:' && "
        f"echo '{package_list}' && "
        f"echo '' && "
        f"read -p 'Press Enter to begin installation... ' && "
        f"echo '' && "
        f"pkexec pacman -S {' '.join(packages)} --needed --noconfirm --ask=4 "
        f"&& echo '' && echo '=== Installation Complete ===' "
        f"|| ( echo '' && echo '=== Installation failed — see errors above ===' && echo '' && "
        f'echo "${{RED}}  [EE]  Package(s) not found in enabled repos.${{RESET}}" && '
        f'echo "${{RED}}  [EE]  Hyprland needs nemesis_repo — enable it in ATT > Pacman tab.${{RESET}}" ); '
        f"read -p 'Press Enter to close...' "
        f") 2>&1 | tee {log_path}"
    )

    fn.log_info("Starting package installation...")
    fn.debug_print(f"Terminal cmd: {install_cmd}")
    process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", install_cmd])
    process.wait()
    fn.invalidate_pkg_cache()
    GLib.idle_add(_seed_and_refresh, self, selected)


def remove_wayland_selection(self, keys):
    """Remove the Hyprland-specific packages for the selected WMs, keeping shared tools.

    Runs as a daemon-thread target. Uses plain `pacman -R` (no -s) on an explicit,
    WM-specific package list so shared utilities and orphaned libs are never cascaded
    out. Refuses to remove a WM whose compositor is the current running session.
    """
    selected = [wm for k in keys if (wm := get_wm(k)) and wm.get("remove")]
    if not selected:
        fn.log_warn("remove_wayland_selection called with nothing removable")
        return

    for wm in selected:
        proc = wm.get("proc")
        if proc and fn.subprocess.run(["pgrep", "-x", proc], capture_output=True).returncode == 0:
            fn.log_warn(f"Refusing to remove {wm['label']} — it is the current running session")
            fn.show_in_app_notification(self, f"Cannot remove {wm['label']} — log out of it first")
            return

    names = ", ".join(wm["label"] for wm in selected)
    packages = [pkg for wm in selected for pkg in wm["remove"]]
    fn.log_section(f"Removing Wayland WM(s): {names}")
    fn.show_in_app_notification(self, f"Opening terminal to remove: {names}")

    log_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".log", delete=False)
    log_path = log_file.name
    log_file.close()

    package_list = "\n".join([f"  • {pkg}" for pkg in packages])
    remove_cmd = (
        f"( "
        f"echo 'Removing Wayland window manager(s): {names}' && "
        f"echo '' && "
        f"echo 'The following packages will be removed:' && "
        f"echo '{package_list}' && "
        f"echo '' && "
        f"echo 'Shared tools (waybar, rofi, polkit, pavucontrol, …) are kept.' && "
        f"echo 'Your ~/.config is left untouched.' && "
        f"echo '' && "
        f"read -p 'Press Enter to remove... ' && "
        f"echo '' && "
        f"pkexec pacman -R {' '.join(packages)} --noconfirm "
        f"|| {{ echo ''; echo 'ERROR: removal failed — a package may still be in use (see above)'; echo ''; }} ; "
        f"echo '=== Done ===' ; "
        f"read -p 'Press Enter to close...' "
        f") 2>&1 | tee {log_path}"
    )

    fn.debug_print(f"Remove command: {remove_cmd}")
    process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", remove_cmd])
    process.wait()
    fn.invalidate_pkg_cache()
    GLib.idle_add(_reset_caches_and_refresh, self, names)


def _reset_caches_and_refresh(self, names):
    desktopr._xsession_files = None
    desktopr._wayland_files = None
    fn.log_success(f"Wayland removal finished: {names}")
    if hasattr(self, "wayland_refresh"):
        self.wayland_refresh()
    return False


def _seed_and_refresh(self, selected):
    # Reset desktopr's session-file caches so check_desktop re-scans and sees the
    # newly installed wayland-session files (mirrors desktopr._after_install).
    desktopr._xsession_files = None
    desktopr._wayland_files = None
    for wm in selected:
        if not (wm["ready"] and desktopr.check_desktop(wm["key"])):
            continue
        fn.log_info(f"Seeding {wm['label']} config from /etc/skel")
        for src in wm["skel"]:
            if not (fn.path.isdir(src) or fn.path.isfile(src)):
                continue
            dest = src.replace("/etc/skel", fn.home)
            if fn.path.isdir(src):
                dest = fn.path.split(dest)[0]
            fn.log_info(f"Copying skel: {src}  →  {dest}")
            with fn.subprocess.Popen(desktopr.copy + [src, dest], bufsize=1, stdout=fn.subprocess.PIPE, universal_newlines=True) as p:
                for line in p.stdout:
                    fn.debug_print(line.strip())
            fn.permissions(dest)
    fn.log_success(f"Wayland install finished: {', '.join(wm['label'] for wm in selected)}")
    if hasattr(self, "wayland_refresh"):
        self.wayland_refresh()
    return False
