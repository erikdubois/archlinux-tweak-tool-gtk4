# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools

# Desktop preview: decode at this max edge (sharp when scaled); minimum widget size (GTK size_request).
IMAGE_PREVIEW_LOAD = 855
IMAGE_PREVIEW_MIN = 456


def gui(self, Gtk, GdkPixbuf, vboxstack12, desktopr, fn, base_dir):
    """create a gui"""
    from gi.repository import Gdk

    self.base_dir = base_dir

    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_separator = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    buttonbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    checkbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    vboxprog = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)

    dropbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)

    lbl1 = Gtk.Label(xalign=0)
    lbl1.set_text("Desktop Installer")
    lbl1.set_name("title")
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox_separator.append(hseparator)
    hbox_title.append(lbl1)

    # =======================================
    #               DROPDOWN
    # =======================================
    label_warning = Gtk.Label(xalign=0.5)
    label_warning.set_markup(
        "<big>Make sure the chaotic-aur and nemesis repo are both enabled \
- see Pacman tab</big>"
    )
    label = Gtk.Label(xalign=0.5)
    label.set_text("\nSelect a desktop")
    label.set_halign(Gtk.Align.CENTER)

    self.d_combo = Gtk.DropDown.new_from_strings(list(desktopr.desktops))
    self.d_combo.set_name("desktop_combo")
    self.d_combo.set_size_request(220, 0)
    self.d_combo.set_selected(0)
    self.d_combo.connect("notify::selected", functools.partial(desktopr.on_d_combo_changed, self))
    # removed in GTK4: set_wrap_width

    dropbox.append(label_warning)

    dropbox.append(label)

    combo_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    combo_hbox.set_margin_top(10)
    combo_hbox.set_halign(Gtk.Align.CENTER)
    self.d_combo.set_halign(Gtk.Align.CENTER)
    combo_hbox.append(self.d_combo)
    dropbox.append(combo_hbox)

    self.label_installed_desktops = Gtk.Label(xalign=0.5)
    self.label_installed_desktops.set_halign(Gtk.Align.CENTER)
    self.label_installed_desktops.set_margin_top(6)
    dropbox.append(self.label_installed_desktops)
    desktopr.refresh_installed_desktops(self)

    # =======================================
    #               BUTTONS
    # =======================================

    self.button_install = Gtk.Button(label="Install desktop")

    self.button_install.connect("clicked", functools.partial(desktopr.on_install_clicked, self))

    self.button_install.set_hexpand(False)
    self.button_install.set_vexpand(False)
    self.button_install.set_sensitive(fn.check_nemesis_repo_active())
    buttonbox.set_halign(Gtk.Align.CENTER)
    buttonbox.append(self.button_install)

    # =======================================
    #               UNINSTALL BUTTON
    # =======================================

    uninstall_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.button_uninstall = Gtk.Button(label="Remove desktop")
    self.button_uninstall.connect("clicked", functools.partial(desktopr.on_uninstall_clicked, self))
    self.button_uninstall.set_hexpand(False)
    self.button_uninstall.set_vexpand(False)
    uninstall_hbox.set_halign(Gtk.Align.CENTER)
    uninstall_hbox.append(self.button_uninstall)

    # =======================================
    #               CHECKBOX
    # =======================================

    self.ch1 = Gtk.CheckButton(label="Clear package cache before installation")
    checkbox.append(self.ch1)

    # =======================================
    #               TEXTVIEW
    # =======================================
    warning_picom = Gtk.Label(xalign=0.5)
    warning_picom.set_halign(Gtk.Align.CENTER)
    warning_picom.set_justify(Gtk.Justification.CENTER)
    message = "We have found picom-ibhagwan-git or picom-jonaburg-git on this system\n\
Know that these packages conflict with picom-git. It will be removed."
    warning_picom.set_markup(
        '<span foreground="red" size="large">' + message + "</span>"
    )
    warning_picom.set_wrap(True)

    noice = Gtk.Label(xalign=0.5)
    noice.set_halign(Gtk.Align.CENTER)
    noice.set_justify(Gtk.Justification.CENTER)
    noice.set_markup(
        "We will backup and overwrite your ~/.config when installing desktops\n\
Backup is in ~/.config-att folder\n\
Uninstalling a desktop leaves its ~/.config subfolder intact\n\
Remove it yourself if no longer needed\n"
    )
    noice.set_wrap(True)
    if fn.check_package_installed("picom-ibhagwan-git") or fn.check_package_installed(
        "picom-jonaburg-git"
    ):
        vboxprog.append(warning_picom)
    vboxprog.append(noice)

    # =======================================
    #               FRAME PREVIEW
    # =======================================
    try:
        pixbuf3 = GdkPixbuf.Pixbuf.new_from_file_at_size(
            base_dir + "/desktop_data/" + fn.get_combo_text(self.d_combo) + ".jpg",
            IMAGE_PREVIEW_LOAD,
            IMAGE_PREVIEW_LOAD,
        )
        texture = Gdk.Texture.new_for_pixbuf(pixbuf3)
        self.image_DE.set_paintable(texture)
    except Exception:
        pass
    self.image_DE.set_content_fit(Gtk.ContentFit.SCALE_DOWN)
    # size_request = minimum allocation; Picture inside ScrolledWindow often got 0×0 and hid the image.
    self.image_DE.set_size_request(IMAGE_PREVIEW_MIN, IMAGE_PREVIEW_MIN)
    self.image_DE.set_hexpand(True)
    self.image_DE.set_vexpand(False)
    self.image_DE.set_halign(Gtk.Align.CENTER)
    self.image_DE.set_valign(Gtk.Align.CENTER)

    frame = Gtk.Frame(label="Preview")
    frame.set_child(self.image_DE)

    # =======================================
    #               PACK TO BOXES
    # =======================================
    vbox.append(dropbox)
    frame.set_hexpand(True)
    frame.set_vexpand(False)
    frame.set_margin_start(0)
    frame.set_margin_end(0)
    vbox.append(frame)
    vbox.append(checkbox)
    vbox.append(buttonbox)
    vbox.append(uninstall_hbox)
    vbox.append(vboxprog)

    vbox.set_hexpand(True)
    vbox.set_vexpand(True)
    vbox.set_margin_start(10)
    vbox.set_margin_end(10)

    # =======================================
    #               PACK TO WINDOW
    # =======================================
    vboxstack12.append(hbox_title)
    vboxstack12.append(hbox_separator)
    vboxstack12.append(vbox)


def update_button_state(self, fn):
    """Update install button sensitivity based on nemesis repo status."""
    nemesis_active = fn.check_nemesis_repo_active()
    self.button_install.set_sensitive(nemesis_active)
