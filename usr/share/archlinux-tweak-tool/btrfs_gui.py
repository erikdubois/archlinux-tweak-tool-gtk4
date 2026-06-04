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
    return f"<span foreground='{color}'>{yes if ok else no}</span>"


def refresh(self, fn):
    """Update every status row + tool button to reflect the live system state."""
    any_installed = False
    for pkg in btrfs.PACKAGES:
        installed = fn.check_package_installed(pkg)
        any_installed = any_installed or installed
        self.btrfs_tool_labels[pkg].set_markup(f"<b>{pkg}</b> — " + _state(installed, "installed", "not installed"))
        self.btrfs_tool_buttons[pkg].set_sensitive(not installed)

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

    active = btrfs.all_packages_installed() and config_ok and cleanup_ok
    self.btrfs_summary_label.set_markup(_state(active, "Snapshots are active", "Snapshots are not set up yet"))
    self.btn_btrfs_assistant.set_sensitive(fn.check_package_installed("btrfs-assistant"))
    self.btn_btrfs_disable.set_sensitive(any_installed or config_ok)


def _build_tool_row(self, Gtk, btrfs, fn, package):
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label = Gtk.Label(xalign=0)
    label.set_margin_start(20)
    label.set_margin_end(10)
    label.set_hexpand(True)
    button = Gtk.Button(label=f"Install {package}")
    button.connect("clicked", functools.partial(btrfs.on_click_install_tool, self, package))
    button.set_margin_end(10)
    hbox.append(label)
    hbox.append(button)
    self.btrfs_tool_labels[package] = label
    self.btrfs_tool_buttons[package] = button
    return hbox


def gui(self, Gtk, vboxstack_btrfs, btrfs, fn):
    """Create the Btrfs snapshot page (shown on a btrfs root, or with --dev)."""
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
        "These snapshot tools are <b>not on the ISO</b> — install them here, then enable snapshots.\n\n"
        "Kiro policy: a snapshot pair is taken on every <b>pacman</b> action (via snap-pac);\n"
        "<b>no</b> hourly timeline snapshots. Cleanup prunes old pairs automatically."
    )
    intro_label.set_margin_start(20)
    intro_label.set_margin_end(10)
    hbox_intro.append(intro_label)

    # ── Snapshot tools (not on the ISO) ──────────────────────────────
    hbox_tools_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    tools_header_label = Gtk.Label(xalign=0)
    tools_header_label.set_markup("<b>Snapshot tools (not on the ISO)</b>")
    tools_header_label.set_margin_start(10)
    hbox_tools_header.append(tools_header_label)

    self.btrfs_tool_labels = {}
    self.btrfs_tool_buttons = {}
    tool_rows = [_build_tool_row(self, Gtk, btrfs, fn, pkg) for pkg in btrfs.PACKAGES]

    # ── Status panel ─────────────────────────────────────────────────
    hbox_status_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    status_header_label = Gtk.Label(xalign=0)
    status_header_label.set_markup("<b>Status</b>")
    status_header_label.set_margin_start(10)
    hbox_status_header.append(status_header_label)

    self.btrfs_summary_label = Gtk.Label(xalign=0)
    self.btrfs_summary_label.set_margin_start(20)
    self.btrfs_config_label = Gtk.Label(xalign=0)
    self.btrfs_config_label.set_margin_start(20)
    self.btrfs_cleanup_label = Gtk.Label(xalign=0)
    self.btrfs_cleanup_label.set_margin_start(20)
    self.btrfs_maint_label = Gtk.Label(xalign=0)
    self.btrfs_maint_label.set_margin_start(20)

    # ── Setup actions ────────────────────────────────────────────────
    hbox_setup_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    setup_header_label = Gtk.Label(xalign=0)
    setup_header_label.set_markup("<b>Setup</b>")
    setup_header_label.set_margin_start(10)
    hbox_setup_header.append(setup_header_label)

    hbox_actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    btn_enable = Gtk.Button(label="Enable Kiro snapshots")
    btn_enable.set_tooltip_text("Install any missing tools and configure snapshots (config + timers + baseline)")
    btn_enable.connect("clicked", functools.partial(btrfs.on_click_enable_snapshots, self))
    btn_enable.set_margin_start(20)
    btn_enable.set_margin_end(10)
    self.btn_btrfs_disable = Gtk.Button(label="Disable Kiro snapshots")
    self.btn_btrfs_disable.set_tooltip_text("Remove the snapshot tools and config — snapshots already taken are kept")
    self.btn_btrfs_disable.connect("clicked", functools.partial(btrfs.on_click_disable_snapshots, self))
    self.btn_btrfs_disable.set_margin_end(10)
    self.btn_btrfs_assistant = Gtk.Button(label="Launch Btrfs Assistant")
    self.btn_btrfs_assistant.connect("clicked", functools.partial(btrfs.on_click_launch_assistant, self))
    self.btn_btrfs_assistant.set_margin_end(10)
    hbox_actions.append(btn_enable)
    hbox_actions.append(self.btn_btrfs_disable)
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
    vboxstack_btrfs.append(hbox_tools_header)
    for row in tool_rows:
        vboxstack_btrfs.append(row)
    vboxstack_btrfs.append(hbox_status_header)
    vboxstack_btrfs.append(self.btrfs_summary_label)
    vboxstack_btrfs.append(self.btrfs_config_label)
    vboxstack_btrfs.append(self.btrfs_cleanup_label)
    vboxstack_btrfs.append(self.btrfs_maint_label)
    vboxstack_btrfs.append(hbox_setup_header)
    vboxstack_btrfs.append(hbox_actions)
    vboxstack_btrfs.append(hbox_caveat)

    refresh(self, fn)
