# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools
import privacy


def init_privacy_lazy_load(self):
    """Refresh label and button states when page becomes visible."""
    try:
        privacy._refresh_ublock_label(self)
        privacy._refresh_hblock_label(self)
    except Exception:
        pass


def gui(self, Gtk, vboxstack3, fn):
    """create a gui"""
    # Title
    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_title = Gtk.Label(xalign=0)
    lbl_title.set_text("Privacy/Security")
    lbl_title.set_name("title")
    lbl_title.set_margin_start(10)
    hbox_title.append(lbl_title)

    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hbox_sep.append(hseparator)

    # ========== SECTION 1: CONTENT BLOCKING ==========

    hbox_section1_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_section1 = Gtk.Label(xalign=0)
    lbl_section1.set_markup("<b>Content Blocking</b>")
    lbl_section1.set_margin_start(10)
    hbox_section1_title.append(lbl_section1)

    # uBlock Origin — install / remove
    hbox_ublock = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_ublock.set_margin_start(10)
    hbox_ublock.set_margin_end(10)

    self.lbl_ublock = Gtk.Label(xalign=0)
    self.lbl_ublock.set_hexpand(True)
    installed_ublock = fn.check_package_installed("firefox-ublock-origin")
    self.lbl_ublock.set_markup(
        "uBlock Origin for Firefox" + (" <b>installed</b>" if installed_ublock else "")
    )

    btn_install_ublock = Gtk.Button(label="Install uBlock")
    btn_install_ublock.set_size_request(160, -1)
    btn_install_ublock.connect("clicked", functools.partial(privacy.on_click_install_ublock, self))

    btn_remove_ublock = Gtk.Button(label="Remove uBlock")
    btn_remove_ublock.set_size_request(160, -1)
    btn_remove_ublock.connect("clicked", functools.partial(privacy.on_click_remove_ublock, self))

    hbox_ublock.append(self.lbl_ublock)
    hbox_ublock.append(btn_install_ublock)
    hbox_ublock.append(btn_remove_ublock)

    # ========== SECTION 2: NETWORK & TRACKING PROTECTION ==========

    hbox_sep2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator2.set_hexpand(True)
    hbox_sep2.append(hseparator2)

    hbox_section2_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_section2 = Gtk.Label(xalign=0)
    lbl_section2.set_markup("<b>Network &amp; Tracking Protection</b>")
    lbl_section2.set_margin_start(10)
    hbox_section2_title.append(lbl_section2)

    # hblock — install / remove
    hbox_hblock_pkg = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_hblock_pkg.set_margin_start(10)
    hbox_hblock_pkg.set_margin_end(10)

    self.lbl_hblock = Gtk.Label(xalign=0)
    self.lbl_hblock.set_hexpand(True)
    installed_hblock = fn.check_package_installed("edu-hblock-git")
    self.lbl_hblock.set_markup(
        "hblock — ad/tracker blocking via /etc/hosts" + (" <b>installed</b>" if installed_hblock else "")
    )

    btn_install_hblock = Gtk.Button(label="Install hblock")
    btn_install_hblock.set_size_request(160, -1)
    btn_install_hblock.connect("clicked", functools.partial(privacy.on_click_install_hblock, self))

    btn_remove_hblock = Gtk.Button(label="Remove hblock")
    btn_remove_hblock.set_size_request(160, -1)
    btn_remove_hblock.connect("clicked", functools.partial(privacy.on_click_remove_hblock, self))

    hbox_hblock_pkg.append(self.lbl_hblock)
    hbox_hblock_pkg.append(btn_install_hblock)
    hbox_hblock_pkg.append(btn_remove_hblock)

    # hblock — enable / disable
    hbox_hblock_toggle = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_hblock_toggle.set_margin_start(10)
    hbox_hblock_toggle.set_margin_end(10)

    self.lbl_hblock_status = Gtk.Label(xalign=0)
    self.lbl_hblock_status.set_hexpand(True)
    hblock_active = fn.hblock_get_state(self) if installed_hblock else False
    status_str = " <b>enabled</b>" if hblock_active else " disabled"
    self.lbl_hblock_status.set_markup("Enable or disable hblock — check /etc/hosts" + status_str)

    self.btn_enable_hblock = Gtk.Button(label="Enable hblock")
    self.btn_enable_hblock.set_size_request(160, -1)
    self.btn_enable_hblock.set_sensitive(installed_hblock)
    self.btn_enable_hblock.connect("clicked", functools.partial(privacy.on_click_enable_hblock, self))

    self.btn_disable_hblock = Gtk.Button(label="Disable hblock")
    self.btn_disable_hblock.set_size_request(160, -1)
    self.btn_disable_hblock.set_sensitive(installed_hblock)
    self.btn_disable_hblock.connect("clicked", functools.partial(privacy.on_click_disable_hblock, self))

    hbox_hblock_toggle.append(self.lbl_hblock_status)
    hbox_hblock_toggle.append(self.btn_enable_hblock)
    hbox_hblock_toggle.append(self.btn_disable_hblock)

    # Status feedback (shown during enable/disable)
    self.label7 = Gtk.Label(xalign=0)
    self.label7.set_margin_start(10)
    self.label7.set_visible(False)

    self.progress = Gtk.ProgressBar()
    self.progress.set_pulse_step(0.2)
    self.progress.set_margin_start(10)
    self.progress.set_margin_end(10)
    self.progress.set_visible(False)

    # ========== APPEND TO VBOX ==========

    vboxstack3.append(hbox_title)
    vboxstack3.append(hbox_sep)

    vboxstack3.append(hbox_section1_title)
    vboxstack3.append(hbox_ublock)

    vboxstack3.append(hbox_sep2)
    vboxstack3.append(hbox_section2_title)
    vboxstack3.append(hbox_hblock_pkg)
    vboxstack3.append(hbox_hblock_toggle)

    vboxstack3.append(self.label7)
    vboxstack3.append(self.progress)

    fn.GLib.idle_add(init_privacy_lazy_load, self, priority=fn.GLib.PRIORITY_LOW)
