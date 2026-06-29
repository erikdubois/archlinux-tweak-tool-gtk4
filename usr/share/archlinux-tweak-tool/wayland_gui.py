# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools
import functions as fn


def _status_markup(wm, desktopr):
    if desktopr.check_desktop(wm["key"]):
        return '<span foreground="#8FBCBB"><b>installed</b></span>'
    if wm.get("disabled"):
        return '<span foreground="#888888">AUR — coming soon</span>'
    if not wm["ready"]:
        return '<span foreground="#888888">no Kiro config yet</span>'
    return '<span foreground="#888888">curated by Kiro</span>'


def _selected_keys(self):
    return [key for key, row in self.wayland_rows.items() if row["check"].get_active() and row["check"].get_sensitive()]


def _update_button(self, wayland, desktopr, fn):
    selected = _selected_keys(self)
    needs_nemesis = wayland.selection_needs_nemesis(selected) and not fn.check_nemesis_repo_active()
    self.wayland_repo_warning.set_visible(needs_nemesis)

    if not selected:
        self.wayland_install_btn.set_sensitive(False)
        self.wayland_install_btn.set_tooltip_text("Select at least one window manager")
    elif needs_nemesis:
        self.wayland_install_btn.set_sensitive(False)
        self.wayland_install_btn.set_tooltip_text("Enable nemesis_repo in the Pacman tab to install Hyprland (kiro-hyprland)")
    else:
        self.wayland_install_btn.set_sensitive(True)
        self.wayland_install_btn.set_tooltip_text("")

    removable = [k for k in selected if wayland.get_wm(k).get("remove") and desktopr.check_desktop(k)]
    self.wayland_remove_btn.set_sensitive(bool(removable))
    self.wayland_remove_btn.set_tooltip_text("" if removable else "Select an installed window manager to remove")


def _refresh(self, wayland, desktopr, fn):
    for wm in wayland.WAYLAND_WMS:
        row = self.wayland_rows.get(wm["key"])
        if row:
            row["status"].set_markup(_status_markup(wm, desktopr))
    sessions = wayland.installed_wayland_sessions()
    text = "Installed Wayland sessions: " + ", ".join(sessions) if sessions else "No Wayland sessions installed yet"
    self.wayland_installed_lbl.set_markup(f'<span foreground="#888888">{text}</span>')
    _update_button(self, wayland, desktopr, fn)
    return False


def _on_toggle(self, _widget, wayland, desktopr, fn):
    _update_button(self, wayland, desktopr, fn)


def _on_install(self, _widget, wayland, desktopr, fn):
    selected = _selected_keys(self)
    if not selected:
        return
    labels = ", ".join(wayland.get_wm(k)["label"] for k in selected)
    fn.log_section(f"Wayland page: install requested for {labels}")
    fn.threading.Thread(target=wayland.install_wayland_selection, args=(self, selected), daemon=True).start()


def _on_remove(self, _widget, wayland, desktopr, fn):
    selected = [k for k in _selected_keys(self) if wayland.get_wm(k).get("remove") and desktopr.check_desktop(k)]
    if not selected:
        return
    labels = ", ".join(wayland.get_wm(k)["label"] for k in selected)
    fn.log_section(f"Wayland page: remove requested for {labels}")
    fn.threading.Thread(target=wayland.remove_wayland_selection, args=(self, selected), daemon=True).start()


def _build_row(self, Gtk, wayland, desktopr, wm):
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox.set_margin_top(4)

    check = Gtk.CheckButton(label=f"{wm['label']}  ·  {wm['backend']}")
    check.set_margin_start(20)
    check.set_hexpand(True)
    # Only curated (ready) WMs are selectable; the rest are visible placeholders.
    if not wm["ready"]:
        check.set_sensitive(False)
    check.connect("toggled", functools.partial(_on_toggle, self, wayland=wayland, desktopr=desktopr, fn=fn))

    status = Gtk.Label(xalign=1)
    status.set_margin_end(20)
    status.set_markup(_status_markup(wm, desktopr))

    hbox.append(check)
    hbox.append(status)
    self.wayland_rows[wm["key"]] = {"check": check, "status": status}
    return hbox


def gui(self, Gtk, vboxstack_wayland, wayland, desktopr, fn, base_dir):
    """Create the Wayland window-manager picker page."""
    from gi.repository import Gdk, GdkPixbuf

    self.wayland_rows = {}

    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_title = Gtk.Label(xalign=0)
    lbl_title.set_text("Desktop - Wayland")
    lbl_title.set_name("title")
    lbl_title.set_margin_start(10)
    hbox_title.append(lbl_title)

    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hbox_sep.append(hseparator)

    intro = Gtk.Label(xalign=0)
    intro.set_margin_start(20)
    intro.set_margin_end(20)
    intro.set_margin_top(8)
    intro.set_wrap(True)
    intro.set_markup(
        "Try a Wayland window manager alongside your current desktop — pick one at the login screen afterwards. "
        "Your current session stays the default. Only Hyprland ships a Kiro config."
    )

    # Hyprland preview — the flagship curated Wayland desktop; the only WM that
    # ships a Kiro config and the only one with a preview image for now.
    preview = Gtk.Picture()
    preview.set_halign(Gtk.Align.CENTER)
    preview.set_size_request(480, 270)
    preview.set_margin_top(10)
    try:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(base_dir + "/desktop_data/hyprland.jpg", 480, 480)
        preview.set_paintable(Gdk.Texture.new_for_pixbuf(pixbuf))
    except Exception as error:
        fn.log_warn(f"Wayland page: could not load Hyprland preview: {error}")

    lbl_preview_caption = Gtk.Label(xalign=0.5)
    lbl_preview_caption.set_halign(Gtk.Align.CENTER)
    lbl_preview_caption.set_markup('<span foreground="#888888">Hyprland — the curated Kiro Wayland desktop</span>')

    hbox_section = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_section = Gtk.Label(xalign=0)
    lbl_section.set_markup("<b>Available Wayland window managers</b>")
    lbl_section.set_margin_start(20)
    lbl_section.set_margin_top(12)
    hbox_section.append(lbl_section)

    self.wayland_installed_lbl = Gtk.Label(xalign=0)
    self.wayland_installed_lbl.set_margin_start(20)
    self.wayland_installed_lbl.set_margin_top(2)
    self.wayland_installed_lbl.set_wrap(True)

    vbox_rows = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    for wm in wayland.WAYLAND_WMS:
        vbox_rows.append(_build_row(self, Gtk, wayland, desktopr, wm))

    self.wayland_repo_warning = Gtk.Label(xalign=0)
    self.wayland_repo_warning.set_margin_start(20)
    self.wayland_repo_warning.set_margin_top(10)
    self.wayland_repo_warning.set_wrap(True)
    self.wayland_repo_warning.set_markup(
        '<span foreground="#FFA500"><b>Hyprland needs nemesis_repo — enable it in the Pacman tab first.</b></span>'
    )
    self.wayland_repo_warning.set_visible(False)

    buttonbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    buttonbox.set_halign(Gtk.Align.CENTER)
    buttonbox.set_margin_top(14)
    self.wayland_install_btn = Gtk.Button(label="Install selected")
    self.wayland_install_btn.connect("clicked", functools.partial(_on_install, self, wayland=wayland, desktopr=desktopr, fn=fn))
    buttonbox.append(self.wayland_install_btn)

    self.wayland_remove_btn = Gtk.Button(label="Remove selected")
    self.wayland_remove_btn.connect("clicked", functools.partial(_on_remove, self, wayland=wayland, desktopr=desktopr, fn=fn))
    buttonbox.append(self.wayland_remove_btn)

    lbl_backup_note = Gtk.Label(xalign=0)
    lbl_backup_note.set_margin_start(20)
    lbl_backup_note.set_margin_top(14)
    lbl_backup_note.set_wrap(True)
    lbl_backup_note.set_markup(
        "Configs the install overwrites are backed up to ~/.config-att first.\n"
        "Uninstalling a WM later leaves its ~/.config subfolder intact — remove it yourself if no longer needed."
    )

    vboxstack_wayland.append(hbox_title)
    vboxstack_wayland.append(hbox_sep)
    vboxstack_wayland.append(intro)
    vboxstack_wayland.append(preview)
    vboxstack_wayland.append(lbl_preview_caption)
    vboxstack_wayland.append(hbox_section)
    vboxstack_wayland.append(self.wayland_installed_lbl)
    vboxstack_wayland.append(vbox_rows)
    vboxstack_wayland.append(self.wayland_repo_warning)
    vboxstack_wayland.append(buttonbox)
    vboxstack_wayland.append(lbl_backup_note)

    self.wayland_refresh = functools.partial(_refresh, self, wayland, desktopr, fn)
    vboxstack_wayland.connect("map", lambda _w: self.wayland_refresh())
    self.wayland_refresh()
