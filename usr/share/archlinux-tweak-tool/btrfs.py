# ============================================================
# Author: Erik Dubois
# ============================================================
# Btrfs snapshot page — logic.
#
# Kiro pre-stages the Garuda-style @-prefixed subvolume layout at install
# time (Calamares mount.conf), including @snapshots -> /.snapshots. The disk
# is snapshot-ready but inert: the snapshot stack is NOT on the ISO, and there
# is no snapper config. This page installs those tools (per-tool buttons, or
# one-click install + configure) visibly — no black boxes — with Kiro's policy
# of snap-pac + cleanup but NO hourly timeline.

import functions as fn

SNAPPER_CONFIG = "/etc/snapper/configs/root"
PACKAGES = ("snapper", "snap-pac", "btrfs-assistant", "btrfsmaintenance")


def is_btrfs_root():
    """Return True when the root filesystem is btrfs."""
    return fn.get_root_filesystem_type() == "btrfs"


def snapper_root_configured():
    """Return True when the snapper 'root' config already exists."""
    return fn.path.isfile(SNAPPER_CONFIG)


def all_packages_installed():
    """Return True when the whole snapshot stack is installed."""
    return all(fn.check_package_installed(pkg) for pkg in PACKAGES)


def _refresh_page(self):
    import btrfs_gui

    fn.invalidate_pkg_cache()
    btrfs_gui.refresh(self, fn)
    return False


def on_click_install_tool(self, package, _widget):
    """Install a single snapshot tool visibly, then refresh the page."""
    fn.log_subsection(f"Installing {package}")
    fn.show_in_app_notification(self, f"Opening terminal to install {package}...")
    process = fn.launch_pacman_install_in_terminal(package)

    def wait_and_refresh():
        if process is not None:
            process.wait()
        fn.log_success(f"{package} install finished")
        fn.GLib.idle_add(_refresh_page, self)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_click_enable_snapshots(self, _widget):
    """Install any missing tools and configure snapshots in a visible terminal."""
    fn.log_subsection("Enabling Kiro btrfs snapshots")
    fn.show_in_app_notification(self, "Opening terminal to install and configure snapshots...")
    process = fn.launch_btrfs_setup_in_terminal()

    def wait_and_refresh():
        if process is not None:
            process.wait()
        fn.log_success("Btrfs snapshot setup finished")
        fn.GLib.idle_add(_refresh_page, self)
        fn.GLib.idle_add(fn.show_in_app_notification, self, "Snapshot setup complete")

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_click_launch_assistant(self, _widget):
    """Launch Btrfs Assistant (the Garuda GUI front-end)."""
    if not fn.check_package_installed("btrfs-assistant"):
        fn.log_warn("btrfs-assistant is not installed yet")
        fn.show_in_app_notification(self, "Install btrfs-assistant first")
        return
    fn.log_subsection("Launching Btrfs Assistant")
    fn.subprocess.Popen(["btrfs-assistant"], stdout=fn.subprocess.PIPE, stderr=fn.subprocess.PIPE)
