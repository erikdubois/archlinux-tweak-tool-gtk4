# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

# Desktop preview: decode at this max edge (sharp when scaled); minimum widget size (GTK size_request).
IMAGE_PREVIEW_LOAD = 900
IMAGE_PREVIEW_MIN = 480


def gui(self, Gtk, GdkPixbuf, vboxstack12, desktopr, fn, base_dir, Pango):
    """create a gui"""
    from gi.repository import Gdk

    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    buttonbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    statbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
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
    hbox4.append(hseparator)
    hbox3.append(lbl1)

    # =======================================
    #               DROPDOWN
    # =======================================
    label_warning = Gtk.Label(xalign=0)
    label_warning.set_markup(
        "<b>Make sure the nemesis repo is active \
- see Pacman tab</b>\n\nSome of the desktops can only be installed if we can access \n\
the nemesis and/or chaotic-aur repo"
    )
    label = Gtk.Label(xalign=0.5)
    label.set_text("\nSelect a desktop")
    label.set_halign(Gtk.Align.CENTER)

    self.d_combo = Gtk.DropDown.new_from_strings(list(desktopr.desktops))
    self.d_combo.set_size_request(220, 0)
    self.d_combo.set_selected(0)
    self.d_combo.connect("notify::selected", self.on_d_combo_changed)
    # removed in GTK4: set_wrap_width

    dropbox.append(label_warning)
    # dropbox.pack_start(button_arco_repo, False, False, 0)
    dropbox.append(label)

    combo_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    combo_hbox.set_margin_top(10)
    combo_hbox.set_halign(Gtk.Align.CENTER)
    self.d_combo.set_halign(Gtk.Align.CENTER)
    combo_hbox.append(self.d_combo)
    dropbox.append(combo_hbox)

    # =======================================
    #               STATUS
    # =======================================
    self.desktop_status.set_hexpand(True)
    self.desktop_status.set_vexpand(True)
    statbox.append(self.desktop_status)

    # =======================================
    #               BUTTONS
    # =======================================

    self.button_install = Gtk.Button(label="Install")
    self.button_reinstall = Gtk.Button(label="Re-Install")

    self.button_install.connect("clicked", self.on_install_clicked, "inst")
    self.button_reinstall.connect("clicked", self.on_install_clicked, "reinst")

    self.button_install.set_hexpand(True)
    self.button_install.set_vexpand(False)
    self.button_install.set_sensitive(fn.check_edu_repos_active())
    buttonbox.append(self.button_install)
    self.button_reinstall.set_hexpand(True)
    self.button_reinstall.set_vexpand(False)
    self.button_reinstall.set_sensitive(fn.check_edu_repos_active())
    buttonbox.append(self.button_reinstall)

    # =======================================
    #               BUTTONS
    # =======================================

    self.ch1 = Gtk.CheckButton(label="Select to clear cache before re-install")
    checkbox.append(self.ch1)
    
    # =======================================
    #               TEXTVIEW
    # =======================================
    self.desktopr_prog = Gtk.ProgressBar()
    self.desktopr_stat = Gtk.Label(xalign=0)
    self.desktopr_stat.set_ellipsize(Pango.EllipsizeMode.MIDDLE)

    warning_picom = Gtk.Label(xalign=0)
    message = "We have found picom-ibhagwan-git or picom-jonaburg-git on this system\n\
Know that these packages conflict with picom-git. It will be removed."
    warning_picom.set_markup(
        '<span foreground="red" size="large">' + message + "</span>"
    )
    warning_picom.set_wrap(True)

    noice = Gtk.Label(xalign=0)
    noice.set_markup(
        "We will backup and overwrite your ~/.config when installing desktops\n\
Backup is in ~/.config-att folder\nLog files are located in /var/log/archlinux\n"
    )
    noice.set_wrap(True)
    self.desktopr_error = Gtk.Label(xalign=0)

    if fn.check_package_installed("picom-ibhagwan-git") or fn.check_package_installed(
        "picom-jonaburg-git"
    ):
        vboxprog.append(warning_picom)
    vboxprog.append(noice)
    vboxprog.append(self.desktopr_error)
    vboxprog.append(self.desktopr_stat)
    vboxprog.append(self.desktopr_prog)

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
    except:
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

    lbl = Gtk.Label(xalign=0)
    lbl.set_text("Installation output")

    # =======================================
    #               PACK TO BOXES
    # =======================================
    vbox.append(dropbox)
    frame.set_hexpand(True)
    frame.set_vexpand(False)
    frame.set_margin_start(0)
    frame.set_margin_end(0)
    vbox.append(frame)
    vbox.append(statbox)
    vbox.append(checkbox)
    vbox.append(buttonbox)
    # vbox.pack_start(defaultbox, False, False, 0)

    vbox.set_hexpand(True)
    vbox.set_vexpand(True)
    vbox.set_margin_start(10)
    vbox.set_margin_end(10)

    vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox1.append(vbox)
 
    # =======================================
    #               PACK TO WINDOW
    # =======================================
    vboxstack12.append(hbox3)
    vboxstack12.append(hbox4)
    vbox1.set_hexpand(True)
    vbox1.set_vexpand(True)
    vboxstack12.append(vbox1)


def update_button_state(self, fn):
    """Update install/reinstall button sensitivity based on nemesis repo status."""
    nemesis_active = fn.check_edu_repos_active()
    self.button_install.set_sensitive(nemesis_active)
    self.button_reinstall.set_sensitive(nemesis_active)
