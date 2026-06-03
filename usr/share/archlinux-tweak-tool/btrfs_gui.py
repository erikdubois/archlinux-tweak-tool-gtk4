# ============================================================
# Author: Erik Dubois
# ============================================================
# Btrfs snapshot page — GUI.

import functools

import btrfs

_GREEN = "#4e9a06"
_ORANGE = "#FFA500"


def _state(ok, yes, no):
    color = _GREEN if ok else _ORANGE
    text = yes if ok else no
    return f"<span foreground='{color}'>{text}</span>"


def refresh(self, fn):
    """Update every status row to reflect the live system state."""
    pkgs_ok = btrfs.all_packages_installed()
    missing = [p for p in btrfs.PACKAGES if not fn.check_package_installed(p)]
    self.btrfs_pkgs_label.set_markup(
        "Snapshot tools (snapper · snap-pac · btrfs-assistant · btrfsmaintenance): "
        + _state(pkgs_ok, "installed", "missing: " + ", ".join(missing) if missing else "missing")
    )

    config_ok = btrfs.snapper_root_configured()
    self.btrfs_config_label.set_markup(
        "Snapper root config (/etc/snapper/configs/root): " + _state(config_ok, "configured", "not configured")
    )

    cleanup_ok = fn.check_service_enabled("snapper-cleanup.timer")
    self.btrfs_cleanup_label.set_markup(
        "Cleanup timer (prunes snap-pac pairs): " + _state(cleanup_ok, "enabled", "disabled")
    )

    maint_ok = fn.check_service_enabled("btrfsmaintenance-refresh.path")
    self.btrfs_maint_label.set_markup(
        "btrfsmaintenance (scrub · balance · trim): " + _state(maint_ok, "enabled", "not enabled")
    )

    active = pkgs_ok and config_ok and cleanup_ok
    self.btrfs_summary_label.set_markup(
        _state(active, "Snapshots are active", "Snapshots are not set up yet")
    )
    self.btn_btrfs_assistant.set_sensitive(fn.check_package_installed("btrfs-assistant"))


def gui(self, Gtk, vboxstack_btrfs, btrfs, fn):
    """Create the Btrfs snapshot page (shown only on a btrfs root)."""
    fn.log_info("Building Btrfs page")

    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_title_label = Gtk.Label(xalign=0)
    hbox_title_label.set_text("Btrfs")
    hbox_title_label.set_name("title")
    hbox_title_label.set_margin_start(10)
    hbox_title_label.set_margin_end(10)
    hbox_title.append(hbox_title_label)

    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hbox_sep.append(hseparator)

    # ── Intro ────────────────────────────────────────────────────────
    hbox_intro = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    intro_label = Gtk.Label(xalign=0)
    intro_label.set_markup(
        "Your root filesystem is <b>btrfs</b> with the Kiro subvolume layout already in place.\n"
        "Enable snapshots to install and configure the snapshot stack in one step — you will see\n"
        "every command run in a terminal window.\n\n"
        "Kiro policy: a snapshot pair is taken on every <b>pacman</b> action (via snap-pac);\n"
        "<b>no</b> hourly timeline snapshots. Cleanup prunes old pairs automatically."
    )
    intro_label.set_margin_start(20)
    intro_label.set_margin_end(10)
    hbox_intro.append(intro_label)

    # ── Status panel ─────────────────────────────────────────────────
    hbox_status_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    status_header_label = Gtk.Label(xalign=0)
    status_header_label.set_markup("<b>Status</b>")
    status_header_label.set_margin_start(10)
    hbox_status_header.append(status_header_label)

    self.btrfs_summary_label = Gtk.Label(xalign=0)
    self.btrfs_summary_label.set_margin_start(20)
    self.btrfs_pkgs_label = Gtk.Label(xalign=0)
    self.btrfs_pkgs_label.set_margin_start(20)
    self.btrfs_config_label = Gtk.Label(xalign=0)
    self.btrfs_config_label.set_margin_start(20)
    self.btrfs_cleanup_label = Gtk.Label(xalign=0)
    self.btrfs_cleanup_label.set_margin_start(20)
    self.btrfs_maint_label = Gtk.Label(xalign=0)
    self.btrfs_maint_label.set_margin_start(20)

    # ── Actions ──────────────────────────────────────────────────────
    hbox_actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    btn_enable = Gtk.Button(label="Enable Kiro snapshots")
    btn_enable.connect("clicked", functools.partial(btrfs.on_click_enable_snapshots, self))
    btn_enable.set_margin_start(20)
    btn_enable.set_margin_end(10)
    self.btn_btrfs_assistant = Gtk.Button(label="Launch Btrfs Assistant")
    self.btn_btrfs_assistant.connect("clicked", functools.partial(btrfs.on_click_launch_assistant, self))
    self.btn_btrfs_assistant.set_margin_end(10)
    hbox_actions.append(btn_enable)
    hbox_actions.append(self.btn_btrfs_assistant)

    # ── Rollback caveat ──────────────────────────────────────────────
    hbox_caveat = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    caveat_label = Gtk.Label(xalign=0)
    caveat_label.set_markup(
        "<i>Kiro uses systemd-boot, so there is no boot-menu snapshot picker. Rollback is done\n"
        "from the running system or the live ISO with snapper — Btrfs Assistant makes this easy.</i>"
    )
    caveat_label.set_margin_start(20)
    caveat_label.set_margin_end(10)
    hbox_caveat.append(caveat_label)

    vboxstack_btrfs.append(hbox_title)
    vboxstack_btrfs.append(hbox_sep)
    vboxstack_btrfs.append(hbox_intro)
    vboxstack_btrfs.append(hbox_status_header)
    vboxstack_btrfs.append(self.btrfs_summary_label)
    vboxstack_btrfs.append(self.btrfs_pkgs_label)
    vboxstack_btrfs.append(self.btrfs_config_label)
    vboxstack_btrfs.append(self.btrfs_cleanup_label)
    vboxstack_btrfs.append(self.btrfs_maint_label)
    vboxstack_btrfs.append(hbox_actions)
    vboxstack_btrfs.append(hbox_caveat)

    refresh(self, fn)
