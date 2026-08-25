# ============================================================
# Author: Erik Dubois
# ============================================================
# Btrfs snapshot page — GUI.

import functools

import btrfs

_GREEN = "#4e9a06"
_ORANGE = "#FFA500"

# Short "what it's for" blurbs (4–5 words) shown beside each tool name.
_TOOL_BLURBS = {
    "snapper": "creates and manages snapshots",
    "snap-pac": "snapshots on every pacman action",
    "btrfs-assistant": "GUI to browse and restore",
    "btrfsmaintenance": "scheduled scrub, balance and trim",
}


def _state(ok, yes, no):
    color = _GREEN if ok else _ORANGE
    return f"<span foreground='{color}'>{yes if ok else no}</span>"


def _refresh_unavailable(self, fn):
    """Blank the live rows and disable every action when the root is not btrfs."""
    for pkg in btrfs.PACKAGES:
        self.btrfs_tool_labels[pkg].set_markup(f"<b>{pkg}</b> <small>— {_TOOL_BLURBS[pkg]}</small>")
        self.btrfs_tool_buttons[pkg].set_sensitive(False)

    fstype = fn.get_root_filesystem_type() or "unknown"
    self.btrfs_summary_label.set_markup(
        f"<span foreground='{_ORANGE}'>Not available — this system's root filesystem is "
        f"<b>{fstype}</b>, not btrfs</span>"
    )
    self.btrfs_config_label.set_markup(
        "<small>Btrfs snapshots need a btrfs root, and the filesystem is chosen when the system\n"
        "is installed — it cannot be switched afterwards. Pick btrfs in the installer to use this page.</small>"
    )
    self.btrfs_cleanup_label.set_text("")
    self.btrfs_maint_label.set_text("")
    self.btn_btrfs_enable.set_sensitive(False)
    self.btn_btrfs_disable.set_sensitive(False)


def refresh(self, fn):
    """Update every status row + tool button to reflect the live system state."""
    if not self.btrfs_available:
        _refresh_unavailable(self, fn)
        return

    any_installed = False
    for pkg in btrfs.PACKAGES:
        installed = fn.check_package_installed(pkg)
        any_installed = any_installed or installed
        self.btrfs_tool_labels[pkg].set_markup(
            f"<b>{pkg}</b> <small>— {_TOOL_BLURBS[pkg]}</small> — "
            + _state(installed, "installed", "not installed")
        )
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
    """Create the Btrfs snapshot page (always shown; inert unless the root is btrfs)."""
    fn.log_info("Building Btrfs page")

    # The page is always in the sidebar so the feature is discoverable and the tab
    # list matches across machines (docs and videos show what every user sees). On a
    # non-btrfs root everything is rendered but disabled, with Status explaining why.
    # --dev keeps the page fully live so it can be exercised off a btrfs box.
    self.btrfs_available = btrfs.is_btrfs_root() or fn.DEV

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
    if self.btrfs_available:
        intro_label.set_markup(
            "Your root filesystem is <b>btrfs</b>, so snapshots can be used on this system.\n"
            "These snapshot tools are <b>not on the ISO</b> — install them here, then enable snapshots.\n\n"
            "How it works: a snapshot pair is taken on every <b>pacman</b> action (via snap-pac);\n"
            "<b>no</b> hourly timeline snapshots. Cleanup prunes old pairs automatically."
        )
    else:
        intro_label.set_markup(
            "Btrfs snapshots let you roll the system back after an update breaks something.\n"
            "This page needs a <b>btrfs</b> root filesystem — see <b>Status</b> below.\n\n"
            "Where it is available: a snapshot pair is taken on every <b>pacman</b> action\n"
            "(via snap-pac); <b>no</b> hourly timeline snapshots, and cleanup prunes old pairs."
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
    btn_enable = Gtk.Button(label="Enable snapshots")
    btn_enable.set_tooltip_text("Install any missing tools and configure snapshots (config + timers + baseline)")
    btn_enable.connect("clicked", functools.partial(btrfs.on_click_enable_snapshots, self))
    btn_enable.set_margin_start(20)
    btn_enable.set_margin_end(10)
    self.btn_btrfs_enable = btn_enable
    self.btn_btrfs_disable = Gtk.Button(label="Disable snapshots")
    self.btn_btrfs_disable.set_tooltip_text("Remove the snapshot tools and config — snapshots already taken are kept")
    self.btn_btrfs_disable.connect("clicked", functools.partial(btrfs.on_click_disable_snapshots, self))
    self.btn_btrfs_disable.set_margin_end(10)
    hbox_actions.append(btn_enable)
    hbox_actions.append(self.btn_btrfs_disable)

    # ── Rollback caveat ──────────────────────────────────────────────
    hbox_caveat = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    caveat_label = Gtk.Label(xalign=0)
    caveat_label.set_markup(
        "<i>This setup does not add a boot-menu snapshot picker. Rollback is done from the\n"
        "running system or the live ISO with snapper — Btrfs Assistant makes this easy.\n"
        "If you installed with GRUB you can add a picker yourself with grub-btrfs;\n"
        "systemd-boot has no equivalent.</i>"
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
