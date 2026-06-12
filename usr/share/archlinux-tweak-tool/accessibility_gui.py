# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools

import accessibility

# Stack child-name of the Themer page (see gui.py add_titled calls).
_THEMER_PAGE = "stack11"


def _section_header(Gtk, text):
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label = Gtk.Label(xalign=0)
    label.set_markup(f"<b>{text}</b>")
    label.set_margin_start(10)
    label.set_margin_top(10)
    label.set_margin_end(10)
    hbox.append(label)
    return hbox


def _refresh(self, fn):
    """Sync every label and switch to the live system state (build-time + on map)."""
    for app in accessibility.ACCESSIBILITY_APPS:
        label = getattr(self, f"lbl_acc_{app['key']}", None)
        if label:
            installed = fn.check_package_installed(app["packages"].split()[0])
            label.set_markup(app["label"] + (" <b>installed</b>" if installed else ""))

    refresh_hc = getattr(self, "refresh_high_contrast_lbl", None)
    if refresh_hc:
        refresh_hc()

    state = accessibility.read_accessx_state()
    for feature in accessibility.ACCESSX:
        switch = getattr(self, f"accessx_switch_{feature['key']}", None)
        if switch:
            self.accessx_initializing = True
            switch.set_active(state.get(feature["key"], False))
            self.accessx_initializing = False


def _on_accessx_toggled(self, fn, feature, switch, _widget, _param):
    if getattr(self, "accessx_initializing", False):
        return
    enabled = switch.get_active()

    def worker():
        if enabled and not accessibility.ensure_xkbset(self):
            fn.GLib.idle_add(fn.show_in_app_notification, self, "xkbset is required — install an AUR helper first")
            fn.GLib.idle_add(_reset_switch, self, switch)
            return
        accessibility.apply_accessx(feature, enabled)
        where = "current session + saved for next login" if enabled else "current session"
        fn.GLib.idle_add(
            fn.show_in_app_notification,
            self,
            f"{feature['label']} {'enabled' if enabled else 'disabled'} ({where})",
        )

    fn.threading.Thread(target=worker, daemon=True).start()


def _reset_switch(self, switch):
    self.accessx_initializing = True
    switch.set_active(False)
    self.accessx_initializing = False


def gui(self, Gtk, vboxstack_accessibility, fn):
    """Create the Accessibility page: assistive tools, high contrast, X11 keyboard accessibility."""
    fn.log_info("Building Accessibility page")

    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_title_label = Gtk.Label(xalign=0)
    hbox_title_label.set_text("Accessibility")
    hbox_title_label.set_name("title")
    hbox_title_label.set_margin_start(10)
    hbox_title_label.set_margin_end(10)
    hbox_title.append(hbox_title_label)

    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox_sep.append(hseparator)

    vboxstack_accessibility.append(hbox_title)
    vboxstack_accessibility.append(hbox_sep)

    # ── Assistive tools ──────────────────────────────────────────────
    vboxstack_accessibility.append(_section_header(Gtk, "Assistive tools"))
    for app in accessibility.ACCESSIBILITY_APPS:
        hbox_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_row.set_margin_top(4)
        label = Gtk.Label(xalign=0)
        label.set_markup(app["label"])
        label.set_margin_start(20)
        label.set_margin_end(10)
        label.set_hexpand(True)
        setattr(self, f"lbl_acc_{app['key']}", label)

        btn_launch = Gtk.Button(label="Launch/Install")
        btn_launch.connect("clicked", functools.partial(accessibility.install_or_launch, self, app))
        btn_launch.set_margin_start(10)
        btn_launch.set_margin_end(5)

        btn_remove = Gtk.Button(label="Remove")
        btn_remove.connect("clicked", functools.partial(accessibility.remove, self, app))
        btn_remove.set_margin_start(5)
        btn_remove.set_margin_end(10)

        hbox_row.append(label)
        hbox_row.append(btn_launch)
        hbox_row.append(btn_remove)
        vboxstack_accessibility.append(hbox_row)

    # ── High contrast / large text ───────────────────────────────────
    vboxstack_accessibility.append(_section_header(Gtk, "High contrast &amp; large text"))
    hbox_hc = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_hc.set_margin_top(4)
    lbl_hc = Gtk.Label(xalign=0)
    lbl_hc.set_margin_start(20)
    lbl_hc.set_margin_end(10)
    lbl_hc.set_hexpand(True)

    def refresh_high_contrast_lbl():
        if accessibility.high_contrast_installed():
            lbl_hc.set_markup("High-contrast themes <b>installed</b> — apply them on the Themer page")
        else:
            lbl_hc.set_markup("Install high-contrast &amp; large-text GTK themes (gnome-themes-extra)")

    self.refresh_high_contrast_lbl = refresh_high_contrast_lbl
    refresh_high_contrast_lbl()

    btn_hc_install = Gtk.Button(label="Install")
    btn_hc_install.connect("clicked", functools.partial(accessibility.install_high_contrast, self))
    btn_hc_install.set_margin_start(10)
    btn_hc_install.set_margin_end(5)

    btn_hc_themer = Gtk.Button(label="Open Themer")
    btn_hc_themer.set_margin_start(5)
    btn_hc_themer.set_margin_end(10)

    def open_themer(_widget):
        stack = getattr(self, "att_stack", None)
        if stack and stack.get_child_by_name(_THEMER_PAGE) is not None:
            stack.set_visible_child_name(_THEMER_PAGE)
            fn.log_info("Jumped to Themer page from Accessibility")

    btn_hc_themer.connect("clicked", open_themer)

    hbox_hc.append(lbl_hc)
    hbox_hc.append(btn_hc_install)
    hbox_hc.append(btn_hc_themer)
    vboxstack_accessibility.append(hbox_hc)

    # ── Keyboard accessibility (X11) ─────────────────────────────────
    vboxstack_accessibility.append(_section_header(Gtk, "Keyboard accessibility (X11)"))

    xkbset_ready = fn.check_package_installed(accessibility.XKBSET_PKG) or fn.get_aur_helper() is not None
    if not xkbset_ready:
        hbox_note = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl_note = Gtk.Label(xalign=0)
        lbl_note.set_markup("   Requires <b>xkbset</b> — install an AUR helper (e.g. yay) to enable these toggles.")
        lbl_note.set_margin_start(10)
        lbl_note.set_margin_end(10)
        hbox_note.append(lbl_note)
        vboxstack_accessibility.append(hbox_note)

    for feature in accessibility.ACCESSX:
        hbox_feature = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_feature.set_margin_top(4)

        # Label stacks the feature name over the exact xkbset line to drop into run.sh (selectable to copy).
        vbox_label = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        vbox_label.set_margin_start(20)
        vbox_label.set_margin_end(10)
        vbox_label.set_hexpand(True)
        vbox_label.set_valign(Gtk.Align.CENTER)
        lbl_feature = Gtk.Label(xalign=0)
        lbl_feature.set_text(feature["label"])
        lbl_cmd = Gtk.Label(xalign=0)
        lbl_cmd.set_markup(f"<small><tt>{fn.GLib.markup_escape_text(feature['on'])}</tt></small>")
        lbl_cmd.set_selectable(True)
        vbox_label.append(lbl_feature)
        vbox_label.append(lbl_cmd)

        switch = Gtk.Switch()
        switch.set_valign(Gtk.Align.CENTER)
        switch.set_margin_end(10)
        switch.set_sensitive(xkbset_ready)
        if not xkbset_ready:
            switch.set_tooltip_text("Requires xkbset (needs an AUR helper such as yay)")
        setattr(self, f"accessx_switch_{feature['key']}", switch)
        switch.connect("notify::active", functools.partial(_on_accessx_toggled, self, fn, feature, switch))

        hbox_feature.append(vbox_label)
        hbox_feature.append(switch)
        vboxstack_accessibility.append(hbox_feature)

    vboxstack_accessibility.append(_persist_note(Gtk))
    vboxstack_accessibility.append(_legend(Gtk))

    vboxstack_accessibility.connect("map", lambda _w: _refresh(self, fn))
    _refresh(self, fn)


def _persist_note(Gtk):
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label = Gtk.Label(xalign=0)
    label.set_markup(
        "<i>Toggles apply immediately and are saved for next login. On a tiling WM that ignores XDG "
        "autostart, add the equivalent xkbset line to your run.sh (or equivalent autostart script).</i>"
    )
    label.set_wrap(True)
    # margin_start matches the toggle labels (20) so the wrapped second line stays aligned under the first word.
    label.set_margin_start(20)
    label.set_margin_end(10)
    label.set_margin_top(6)
    hbox.append(label)
    return hbox


def _legend(Gtk):
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
    vbox.set_margin_start(20)
    vbox.set_margin_end(10)
    vbox.set_margin_top(12)
    header = Gtk.Label(xalign=0)
    header.set_markup("<b>What these do</b>")
    vbox.append(header)
    entries = [
        ("Sticky Keys", "press modifier keys (Shift, Ctrl, Alt, Super) one at a time instead of holding several together."),
        ("Slow Keys", "a key only registers when held down briefly, so accidental light taps are ignored."),
        ("Bounce Keys", "ignores repeated presses of the same key in quick succession (accidental double-strikes)."),
        ("Mouse Keys", "move the mouse pointer using the numeric keypad instead of a physical mouse."),
    ]
    for name, desc in entries:
        lbl = Gtk.Label(xalign=0)
        lbl.set_markup(f"<small><b>{name}</b> — {desc}</small>")
        lbl.set_wrap(True)
        vbox.append(lbl)
    return vbox
