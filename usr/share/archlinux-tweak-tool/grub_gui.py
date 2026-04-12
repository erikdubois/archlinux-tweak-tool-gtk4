# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================


def gui(self, Gtk, vboxstack4, fn):
    """create a gui"""
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl1 = Gtk.Label(xalign=0)
    lbl1.set_text("Grub Themes")
    lbl1.set_name("title")
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(True)
    hbox4.append(hseparator)
    hbox3.append(lbl1)

    self.install_arco_vimix = Gtk.Button(
        label="Install the grub Vimix theme and ATT will reboot automatically"
    )

    # ==========================================================
    #                       GRUB
    # ==========================================================

    if fn.check_package_installed("arcolinux-grub-theme-vimix-git"):

        hbox10 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label10 = Gtk.Label(label="Grub timeout in seconds")
        self.scale = Gtk.Scale().new(Gtk.Orientation.HORIZONTAL)
        self.scale.set_draw_value(True)
        self.scale.set_value_pos(Gtk.PositionType.BOTTOM)
        self.scale.set_range(0, 30)
        self.scale.set_digits(0)
        self.scale.set_inverted(False)
        self.scale.set_size_request(200, 10)
        self.scale.set_tooltip_text("Seconds")
        btnsave = Gtk.Button(label="Save")
        btnsave.connect("clicked", self.on_clicked_grub_timeout)
        label10.set_margin_start(10)
        label10.set_margin_end(10)
        label10.set_hexpand(True)
        hbox10.append(label10)
        self.scale.set_margin_start(10)
        self.scale.set_margin_end(10)
        hbox10.append(self.scale)  # pack_end
        btnsave.set_margin_start(10)
        btnsave.set_margin_end(10)
        hbox10.append(btnsave)  # pack_end

        hbox11 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        label11 = Gtk.Label(label="Import image")
        self.tbimage = Gtk.Entry()
        btnsearch = Gtk.Button(label=". . .")
        btnsearch.connect("clicked", self.on_choose_wallpaper)
        label11.set_margin_start(10)
        label11.set_margin_end(10)
        hbox11.append(label11)
        self.tbimage.set_hexpand(True)
        self.tbimage.set_vexpand(True)
        self.tbimage.set_margin_start(10)
        self.tbimage.set_margin_end(10)
        hbox11.append(self.tbimage)
        btnsearch.set_margin_start(10)
        btnsearch.set_margin_end(10)
        hbox11.append(btnsearch)

        hbox12 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        label12 = Gtk.Label()
        label12.set_text("Select a wallpaper and apply")
        btnimport = Gtk.Button(label="Import selected image")
        btnimport.connect("clicked", self.on_import_wallpaper)
        btnimport.set_margin_start(10)
        btnimport.set_margin_end(10)
        hbox12.append(btnimport)  # pack_end
        label12.set_margin_start(10)
        label12.set_margin_end(10)
        hbox12.append(label12)

        hbox13 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        btnremove = Gtk.Button(label="Remove wallpaper")
        btnremove.set_size_request(180, 0)
        btnremove.connect("clicked", self.on_remove_wallpaper)
        btnremove.set_margin_start(10)
        btnremove.set_margin_end(10)
        hbox13.append(btnremove)  # pack_end

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        wallpaper_list = fn.get_grub_wallpapers()
        self.grub_theme_combo = Gtk.DropDown.new_from_strings([])
        self.pop_themes_grub(self.grub_theme_combo, wallpaper_list, True)
        self.fb.set_valign(Gtk.Align.START)
        self.fb.set_max_children_per_line(6)
        self.fb.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.fb.connect("child-activated", self.on_grub_item_clicked)
        scrolled.set_child(self.fb)
        self.grub_theme_combo.connect("notify::selected", self.on_grub_theme_change)

        hbox16 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        install_rebornos_grub = Gtk.Button(
            label="Install original grub theme of RebornOS - auto reboot"
        )
        install_rebornos_grub.connect(
            "clicked", self.on_click_install_orignal_grub_rebornos
        )
        install_rebornos_grub.set_margin_start(10)
        install_rebornos_grub.set_margin_end(10)
        hbox16.append(install_rebornos_grub)  # pack_end

        hbox9 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        grub_apply = Gtk.Button(label="2. Choose and apply wallpaper")
        grub_apply.connect("clicked", self.on_set_grub_wallpaper)
        grub_reset = Gtk.Button(label="Reset to default Vimix wallpaper")
        grub_reset.connect("clicked", self.on_reset_grub_wallpaper)
        grub_reset_grub = Gtk.Button(label="Reset to the original grub theme")
        grub_reset_grub.connect("clicked", self.on_reset_grub)
        grub_reset_vimix = Gtk.Button(label="1. Apply the Vimix theme")
        grub_reset_vimix.connect("clicked", self.on_reset_grub_vimix)
        hbox9.append(grub_reset_vimix)  # pack_end
        hbox9.append(grub_apply)  # pack_end
        hbox9.append(grub_reset_grub)  # pack_end

        vboxstack4.append(hbox3)  # title
        vboxstack4.append(hbox4)  # seperator
        vboxstack4.append(hbox10)  # scale
        vboxstack4.append(hbox11)  # import
        vboxstack4.append(hbox12)  # select wallpaper
        vboxstack4.append(hbox13)  # select wallpaper
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)
        vboxstack4.append(scrolled)  # Preview
        vboxstack4.append(hbox9)  # pack_end  # Buttons
        if fn.distr == "rebornos":
            vboxstack4.append(hbox16)  # pack_end  # Buttons

    else:
        hbox31 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl1 = Gtk.Label(xalign=0)
        lbl1.set_text("Grub")
        lbl1.set_name("title")
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(True)
        hbox41.append(hseparator)
        hbox31.append(lbl1)
        vboxstack4.append(hbox31)
        vboxstack4.append(hbox41)
        grub_message = Gtk.Label()
        grub_message.set_markup(
            "<b>We did not find the application arcolinux-grub-theme-vimix-git</b>\n\
<b>First activate the ArcoLinux repos in the Pacman tab</b>\n\
Then you can choose all kinds of wallpapers\n\
We will reload the ATT automatically"
        )

        if fn.check_systemd_boot():
            grub_message.set_markup(
                "<b>We believe you are on a system that uses systemd boot</b>\n\
<b>Grub can not be used</b>"
            )

        self.install_arco_vimix = Gtk.Button(
            label="Install the grub Vimix theme and ATT will reboot automatically"
        )
        if fn.check_arco_repos_active() is True:
            self.install_arco_vimix.set_sensitive(True)
        else:
            self.install_arco_vimix.set_sensitive(False)

        self.install_arco_vimix.connect(
            "clicked", self.on_click_install_arco_vimix_clicked
        )
        if fn.check_systemd_boot():
            grub_message.set_hexpand(True)
            grub_message.set_vexpand(True)
            vboxstack4.append(grub_message)
        else:
            grub_message.set_hexpand(True)
            grub_message.set_vexpand(True)
            vboxstack4.append(grub_message)
            vboxstack4.append(self.install_arco_vimix)
