# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================


def gui(self, Gtk, vboxstack22, sddm, lightdm, lxdm, fn, login):
    """create a gui"""
    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox1_lbl = Gtk.Label(xalign=0)
    hbox1_lbl.set_markup("Login Managers")
    hbox1_lbl.set_name("title")
    hbox1_lbl.set_margin_start(10)
    hbox1_lbl.set_margin_end(10)
    hbox1.append(hbox1_lbl)

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox0.append(hseparator)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    vboxstack1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
    stack.set_transition_duration(350)
    stack.set_hhomogeneous(False)
    stack.set_vhomogeneous(False)

    stack_switcher = Gtk.StackSwitcher()
    stack_switcher.set_orientation(Gtk.Orientation.HORIZONTAL)
    stack_switcher.set_stack(stack)

    if fn.check_package_installed("sddm"):

        # ==================================================================
        #                       SDDM
        # ==================================================================

        hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox4_lbl = Gtk.Label(xalign=0)
        hbox4_lbl.set_text("Sddm (inactive)")
        if fn.check_content("sddm", "/etc/systemd/system/display-manager.service"):
            hbox4_lbl.set_text("Sddm (active)")
        hbox4_lbl.set_name("title")
        hbox4_lbl.set_name("title")
        hbox4.append(hbox4_lbl)

        hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox5.append(hseparator)

        # ==================================================================

        hbox14 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label_sddm_config = Gtk.Label(xalign=0)
        label_sddm_config.set_text(
            "We recommend to use the default sddm \
configuration setup\nSddm configuration split into two files : /etc/sddm.conf \
and /etc/sddm.conf.d/kde_settings.conf\n\
/etc/sddm.conf.d/kde_settings.conf contains all the parameters - We will \
backup your files"
        )
        label_sddm_config.set_margin_start(10)
        label_sddm_config.set_margin_end(10)
        hbox14.append(label_sddm_config)

        hbox13 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        reset_sddm_original_att = Gtk.Button(
            label="Apply the Sddm configuration from ATT - auto reboot"
        )
        reset_sddm_original_att.set_size_request(100, 30)
        reset_sddm_original_att.connect(
            "clicked", self.on_click_sddm_reset_original_att
        )
        reset_sddm_original = Gtk.Button(
            label="Apply your original Sddm configuration - auto reboot"
        )
        reset_sddm_original.set_size_request(100, 30)
        reset_sddm_original.connect("clicked", self.on_click_sddm_reset_original)
        reset_sddm_original_att.set_margin_start(10)
        reset_sddm_original_att.set_margin_end(10)
        hbox13.append(reset_sddm_original_att)
        reset_sddm_original.set_margin_start(10)
        reset_sddm_original.set_margin_end(10)
        hbox13.append(reset_sddm_original)

        hbox05 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox05.append(hseparator)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_lbl = Gtk.Label(xalign=0)
        hbox_lbl.set_markup("Auto login")
        self.autologin_sddm = Gtk.Switch()
        self.autologin_sddm.connect("notify::active", self.on_autologin_sddm_activated)
        hbox_lbl.set_margin_start(10)
        hbox_lbl.set_margin_end(10)
        hbox_lbl.set_hexpand(True)
        hbox.append(hbox_lbl)
        self.autologin_sddm.set_margin_start(10)
        self.autologin_sddm.set_margin_end(10)
        hbox.append(self.autologin_sddm)  # pack_end

        hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox3_lbl = Gtk.Label(xalign=0)
        hbox3_lbl.set_text("Choose the desktop you want to auto login to")
        hbox3_lbl.set_margin_start(10)
        hbox3_lbl.set_margin_end(10)
        hbox3.append(hbox3_lbl)

        # sddm
        hbox18 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox18_lbl = Gtk.Label(xalign=0)
        hbox18_lbl.set_markup("Desktop session")
        self.sessions_sddm = Gtk.DropDown.new_from_strings([])
        sddm.pop_box(self, self.sessions_sddm)
        hbox18_lbl.set_margin_start(10)
        hbox18_lbl.set_margin_end(10)
        hbox18_lbl.set_hexpand(True)
        hbox18.append(hbox18_lbl)
        self.sessions_sddm.set_margin_start(10)
        self.sessions_sddm.set_margin_end(10)
        hbox18.append(self.sessions_sddm)  # pack_end

        hbox9 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox9_lbl = Gtk.Label(xalign=0)
        hbox9_lbl.set_text("Theme")
        self.theme_sddm = Gtk.DropDown.new_from_strings([])
        sddm.pop_theme_box(self, self.theme_sddm)
        hbox9_lbl.set_margin_start(10)
        hbox9_lbl.set_margin_end(10)
        hbox9_lbl.set_hexpand(True)
        hbox9.append(hbox9_lbl)
        self.theme_sddm.set_margin_start(10)
        self.theme_sddm.set_margin_end(10)
        hbox9.append(self.theme_sddm)  # pack_end

        hbox11 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        install_sddm_themes = Gtk.Button(label="Install missing ArcoLinux Sddm Themes")
        install_sddm_themes.connect("clicked", self.on_click_install_sddm_themes)
        remove_sddm_themes = Gtk.Button(label="Remove the ArcoLinux Sddm Themes")
        remove_sddm_themes.connect("clicked", self.on_click_remove_sddm_themes)
        install_sddm_themes.set_margin_start(10)
        install_sddm_themes.set_margin_end(10)
        install_sddm_themes.set_hexpand(True)
        hbox11.append(install_sddm_themes)
        remove_sddm_themes.set_margin_start(10)
        remove_sddm_themes.set_margin_end(10)
        hbox11.append(remove_sddm_themes)  # pack_end

        hbox16 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        install_bibata_cursor = Gtk.Button(label="Install Bibata cursors")
        install_bibata_cursor.connect("clicked", self.on_click_install_bibata_cursor)
        remove_bibata_cursor = Gtk.Button(label="Remove Bibata cursors")
        remove_bibata_cursor.connect("clicked", self.on_click_remove_bibata_cursor)
        install_bibata_cursor.set_margin_start(10)
        install_bibata_cursor.set_margin_end(10)
        install_bibata_cursor.set_hexpand(True)
        hbox16.append(install_bibata_cursor)
        remove_bibata_cursor.set_margin_start(10)
        remove_bibata_cursor.set_margin_end(10)
        hbox16.append(remove_bibata_cursor)  # pack_end

        hbox28 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        install_bibata_cursorr = Gtk.Button(label="Install Bibata extra cursors")
        install_bibata_cursorr.connect("clicked", self.on_click_install_bibatar_cursor)
        remove_bibata_cursorr = Gtk.Button(label="Remove Bibata extra cursors")
        remove_bibata_cursorr.connect("clicked", self.on_click_remove_bibatar_cursor)
        install_bibata_cursorr.set_margin_start(10)
        install_bibata_cursorr.set_margin_end(10)
        install_bibata_cursorr.set_hexpand(True)
        hbox28.append(install_bibata_cursorr)
        remove_bibata_cursorr.set_margin_start(10)
        remove_bibata_cursorr.set_margin_end(10)
        hbox28.append(remove_bibata_cursorr)  # pack_end

        hbox12 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox12_lbl = Gtk.Label(xalign=0)
        hbox12_lbl.set_text("Keep the default ArcoLinux theme")
        self.keep_default_theme = Gtk.Switch()
        hbox12_lbl.set_margin_start(10)
        hbox12_lbl.set_margin_end(10)
        hbox12.append(hbox12_lbl)  # pack_end
        self.keep_default_theme.set_margin_start(10)
        self.keep_default_theme.set_margin_end(10)
        hbox12.append(self.keep_default_theme)  # pack_end

        hbox17 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox17_lbl = Gtk.Label(xalign=0)
        hbox17_lbl.set_text(
            "Select your cursor theme for the login screen e.g. Bibata-Modern-Ice"
        )
        hbox17_lbl.set_margin_start(10)
        hbox17_lbl.set_margin_end(10)
        hbox17.append(hbox17_lbl)

        hbox15 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox15_lbl = Gtk.Label(xalign=0)
        hbox15_lbl.set_text("Cursor theme")
        self.sddm_cursor_themes = Gtk.DropDown.new_from_strings([])
        sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        hbox15_lbl.set_margin_start(10)
        hbox15_lbl.set_margin_end(10)
        hbox15_lbl.set_hexpand(True)
        hbox15.append(hbox15_lbl)
        self.sddm_cursor_themes.set_margin_start(10)
        self.sddm_cursor_themes.set_margin_end(10)
        hbox15.append(self.sddm_cursor_themes)  # pack_end

        # reset_sddm = Gtk.Button(label="Apply your backup of sddm.conf")
        # reset_sddm.connect("clicked", self.on_click_sddm_reset)

        # ======================================================================
        #                              BOTTOM
        # ======================================================================

        hbox90 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        enable_sddm = Gtk.Button(label="Enable Sddm")
        enable_sddm.connect("clicked", self.on_click_sddm_enable)
        # btnRefreshAtt = Gtk.Button(label="Refresh the list of Sddm themes")
        # btnRefreshAtt.connect('clicked', self.on_refresh_att_clicked)
        apply_sddm_settings = Gtk.Button(label="Apply settings")
        apply_sddm_settings.connect("clicked", self.on_click_sddm_apply)
        hbox90.append(apply_sddm_settings)  # pack_end
        # hbox90.pack_end(btnRefreshAtt, False, False, 0)
        enable_sddm.set_margin_start(10)
        enable_sddm.set_margin_end(10)
        hbox90.append(enable_sddm)

        # ======================================================================
        #                              PACK TO STACK
        # ======================================================================

        vboxstack1.append(hbox4)
        vboxstack1.append(hbox5)
        vboxstack1.append(hbox14)
        vboxstack1.append(hbox13)
        vboxstack1.append(hbox05)

        if fn.path.isfile(fn.sddm_default_d2):
            vboxstack1.append(hbox)
            vboxstack1.append(hbox3)
            vboxstack1.append(hbox18)
            vboxstack1.append(hbox9)
            vboxstack1.append(hbox11)
            vboxstack1.append(hbox12)
            vboxstack1.append(hbox16)
            vboxstack1.append(hbox28)
            vboxstack1.append(hbox17)
            vboxstack1.append(hbox15)
            vboxstack1.append(hbox90)  # pack_end

    else:
        # no sddm installed
        hbox31 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox31_lbl = Gtk.Label(xalign=0)
        hbox31_lbl.set_text("Sddm is not installed")
        hbox31_lbl.set_name("title")
        hbox31.append(hbox31_lbl)

        hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox41.append(hseparator)

        message = Gtk.Label()
        message.set_markup("<b>Sddm does not seem to be installed</b>")
        install_sddm = Gtk.Button(
            label="Install Sddm - auto reboot - do not forget to enable it"
        )
        install_sddm.connect("clicked", self.on_click_att_sddm_clicked)

        vboxstack1.append(hbox31)
        vboxstack1.append(hbox41)
        vboxstack1.append(message)
        vboxstack1.append(install_sddm)

    # ==================================================================
    #                       LIGHTDM
    # ==================================================================

    if fn.check_package_installed("lightdm"):

        hbox19 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox19_lbl = Gtk.Label(xalign=0)
        hbox19_lbl.set_text("Lightdm (inactive)")
        if fn.check_content("lightdm", "/etc/systemd/system/display-manager.service"):
            hbox19_lbl.set_text("Lightdm (active)")
        if fn.check_content(
            "lightdm", "/etc/systemd/system/display-manager.service"
        ) and fn.check_content("slick-greeter", "/etc/lightdm/lightdm.conf"):
            hbox19_lbl.set_text("Lightdm + slick-greeter (active)")
        hbox19_lbl.set_name("title")
        hbox19.append(hbox19_lbl)

        hbox20 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox20.append(hseparator)

        hbox140 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label_lightdm_config = Gtk.Label(xalign=0)
        label_lightdm_config.set_text(
            "We recommend to use the default ATT lightdm and lightdm-greeter configuration setup"
        )
        label_lightdm_config.set_margin_start(10)
        label_lightdm_config.set_margin_end(10)
        hbox140.append(label_lightdm_config)

        hbox130 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        reset_lightdm_original_att = Gtk.Button(
            label="Apply the Lightdm configuration from ATT - auto reboot"
        )
        reset_lightdm_original_att.set_size_request(100, 30)
        reset_lightdm_original_att.connect(
            "clicked", self.on_click_lightdm_reset_original_att
        )
        reset_lightdm_original = Gtk.Button(
            label="Apply your original Lightdm configuration - auto reboot"
        )
        reset_lightdm_original.set_size_request(100, 30)
        reset_lightdm_original.connect(
            "clicked", self.on_click_reset_lightdm_lightdm_greeter
        )
        reset_lightdm_original_att.set_margin_start(10)
        reset_lightdm_original_att.set_margin_end(10)
        hbox130.append(reset_lightdm_original_att)
        reset_lightdm_original.set_margin_start(10)
        reset_lightdm_original.set_margin_end(10)
        hbox130.append(reset_lightdm_original)

        hbox050 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox050.append(hseparator)

        hbox21 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox21_lbl = Gtk.Label(xalign=0)
        hbox21_lbl.set_text("Autologin")
        self.autologin_lightdm = Gtk.Switch()
        self.autologin_lightdm.connect(
            "notify::active", self.on_autologin_lightdm_activated
        )
        hbox21_lbl.set_margin_start(10)
        hbox21_lbl.set_margin_end(10)
        hbox21_lbl.set_hexpand(True)
        hbox21.append(hbox21_lbl)
        self.autologin_lightdm.set_margin_start(10)
        self.autologin_lightdm.set_margin_end(10)
        hbox21.append(self.autologin_lightdm)  # pack_end

        hbox22 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox22_lbl = Gtk.Label(xalign=0)
        hbox22_lbl.set_text("Choose the desktop you want to autologin to")
        hbox22_lbl.set_margin_start(10)
        hbox22_lbl.set_margin_end(10)
        hbox22.append(hbox22_lbl)

        hbox23 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox23_lbl = Gtk.Label(xalign=0)
        hbox23_lbl.set_text("Use the ATT lightdm-gtk-greeter configuration")
        btn_install_arco_lightdm_greeter = Gtk.Button(label="Set ATT config")
        btn_install_arco_lightdm_greeter.connect(
            "clicked", self.on_click_install_arco_lightdmgreeter
        )
        btn_reset_lightdm_greeter = Gtk.Button(label="Reset back to original config")
        btn_reset_lightdm_greeter.connect(
            "clicked", self.on_click_reset_lightdm_lightdm_greeter
        )
        hbox23_lbl.set_margin_start(10)
        hbox23_lbl.set_margin_end(10)
        hbox23_lbl.set_hexpand(True)
        hbox23.append(hbox23_lbl)
        btn_install_arco_lightdm_greeter.set_margin_start(10)
        btn_install_arco_lightdm_greeter.set_margin_end(10)
        hbox23.append(btn_install_arco_lightdm_greeter)  # pack_end
        btn_reset_lightdm_greeter.set_margin_start(10)
        btn_reset_lightdm_greeter.set_margin_end(10)
        hbox23.append(btn_reset_lightdm_greeter)  # pack_end

        hbox29 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.lbl_slickgreeter = Gtk.Label(xalign=0)
        login.find_slick_greeter_label(self.lbl_slickgreeter)
        btn_install_slick_greeter = Gtk.Button(label="Install/enable slickgreeter")
        btn_install_slick_greeter.connect(
            "clicked", self.on_click_install_slick_greeter
        )
        btn_remove_slick_greeter = Gtk.Button(label="Remove slickgreeter")
        btn_remove_slick_greeter.connect("clicked", self.on_click_remove_slick_greeter)
        self.lbl_slickgreeter.set_margin_start(10)
        self.lbl_slickgreeter.set_margin_end(10)
        self.lbl_slickgreeter.set_hexpand(True)
        hbox29.append(self.lbl_slickgreeter)
        btn_install_slick_greeter.set_margin_start(10)
        btn_install_slick_greeter.set_margin_end(10)
        hbox29.append(btn_install_slick_greeter)  # pack_end
        btn_remove_slick_greeter.set_margin_start(10)
        btn_remove_slick_greeter.set_margin_end(10)
        hbox29.append(btn_remove_slick_greeter)  # pack_end

        # lightdm
        hbox27 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox27_lbl = Gtk.Label(xalign=0)
        hbox27_lbl.set_text("Desktop session")
        self.sessions_lightdm = Gtk.DropDown.new_from_strings([])
        lightdm.pop_box_sessions_lightdm(self, self.sessions_lightdm)
        hbox27_lbl.set_margin_start(10)
        hbox27_lbl.set_margin_end(10)
        hbox27_lbl.set_hexpand(True)
        hbox27.append(hbox27_lbl)
        self.sessions_lightdm.set_margin_start(10)
        self.sessions_lightdm.set_margin_end(10)
        hbox27.append(self.sessions_lightdm)  # pack_end

        hbox30 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox30_lbl = Gtk.Label(xalign=0)
        hbox30_lbl.set_text("Gtk theme")
        self.gtk_theme_names_lightdm = Gtk.DropDown.new_from_strings([])
        lightdm.pop_gtk_theme_names_lightdm(self, self.gtk_theme_names_lightdm)
        hbox30_lbl.set_margin_start(10)
        hbox30_lbl.set_margin_end(10)
        hbox30_lbl.set_hexpand(True)
        hbox30.append(hbox30_lbl)
        self.gtk_theme_names_lightdm.set_margin_start(10)
        self.gtk_theme_names_lightdm.set_margin_end(10)
        hbox30.append(self.gtk_theme_names_lightdm)  # pack_end

        hbox33 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox33_lbl = Gtk.Label(xalign=0)
        hbox33_lbl.set_text("Icon theme name")
        self.gtk_icon_names_lightdm = Gtk.DropDown.new_from_strings([])
        lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)
        hbox33_lbl.set_margin_start(10)
        hbox33_lbl.set_margin_end(10)
        hbox33_lbl.set_hexpand(True)
        hbox33.append(hbox33_lbl)
        self.gtk_icon_names_lightdm.set_margin_start(10)
        self.gtk_icon_names_lightdm.set_margin_end(10)
        hbox33.append(self.gtk_icon_names_lightdm)  # pack_end

        hbox35 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox35_lbl = Gtk.Label(xalign=0)
        hbox35_lbl.set_text("Cursor theme")
        self.cursor_themes_lightdm = Gtk.DropDown.new_from_strings([])
        lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        hbox35_lbl.set_margin_start(10)
        hbox35_lbl.set_margin_end(10)
        hbox35_lbl.set_hexpand(True)
        hbox35.append(hbox35_lbl)
        self.cursor_themes_lightdm.set_margin_start(10)
        self.cursor_themes_lightdm.set_margin_end(10)
        hbox35.append(self.cursor_themes_lightdm)  # pack_end

        hbox34 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox34_label = Gtk.Label(xalign=0)
        hbox34_label.set_text("Background color can be set for both")
        self.slick_greeter_color_checkbutton = Gtk.CheckButton(
            label="Select it to use it"
        )
        hbox34_label.set_margin_start(10)
        hbox34_label.set_margin_end(10)
        hbox34.append(hbox34_label)
        self.slick_greeter_color_checkbutton.set_margin_start(10)
        self.slick_greeter_color_checkbutton.set_margin_end(10)
        hbox34.append(self.slick_greeter_color_checkbutton)

        hbox25 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.slick_greeter_color = Gtk.ColorSelection()
        self.slick_greeter_color.set_margin_start(10)
        self.slick_greeter_color.set_margin_end(10)
        hbox25.append(self.slick_greeter_color)

        hbox24 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox24_lbl = Gtk.Label(xalign=0)
        hbox24_lbl.set_text(
            "You can change more settings with the lightdm-gtk-greeter-settings app"
        )
        hbox24_lbl.set_margin_start(10)
        hbox24_lbl.set_margin_end(10)
        hbox24.append(hbox24_lbl)

        # lightdm
        hbox26 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        enable_lightdm = Gtk.Button(label="Enable Lightdm")
        enable_lightdm.connect("clicked", self.on_click_lightdm_enable)
        apply = Gtk.Button(label="Apply settings")
        apply.connect("clicked", self.on_click_lightdm_apply)
        # reset = Gtk.Button(label="Reset lightdm.conf")
        # reset.connect("clicked", self.on_click_lightdm_reset)
        hbox26.append(apply)  # pack_end
        # hbox26.pack_end(reset, False, False, 0)
        hbox26.append(enable_lightdm)

        vboxstack2.append(hbox19)
        vboxstack2.append(hbox20)
        vboxstack2.append(hbox140)
        vboxstack2.append(hbox130)
        vboxstack2.append(hbox050)
        vboxstack2.append(hbox21)
        vboxstack2.append(hbox22)
        vboxstack2.append(hbox27)
        vboxstack2.append(hbox30)
        vboxstack2.append(hbox33)
        vboxstack2.append(hbox23)
        vboxstack2.append(hbox29)
        vboxstack2.append(hbox35)
        vboxstack2.append(hbox34)
        vboxstack2.append(hbox25)
        vboxstack2.append(hbox26)  # pack_end
        vboxstack2.append(hbox24)

    else:
        # no lightdm installed
        hbox32 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox32_lbl = Gtk.Label(xalign=0)
        hbox32_lbl.set_text("Lightdm is not installed")
        hbox32_lbl.set_name("title")
        hbox32.append(hbox32_lbl)

        hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox41.append(hseparator)

        vboxstack2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vboxstack2.append(hbox32)
        vboxstack2.append(hbox41)
        message = Gtk.Label()
        message.set_markup("<b>Lightdm does not seem to be installed</b>")

        install_lightdm = Gtk.Button(
            label="Install Lightdm - auto reboot - do not forget to enable it"
        )
        install_lightdm.connect("clicked", self.on_click_att_lightdm_clicked)

        vboxstack2.append(message)
        vboxstack2.append(install_lightdm)

    # ==================================================================
    #                       LXDM
    # ==================================================================

    if fn.check_package_installed("lxdm") or fn.check_package_installed("lxdm-gtk3"):

        hbox50 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox50_lbl = Gtk.Label(xalign=0)
        hbox50_lbl.set_text("Lxdm (inactive)")
        if fn.check_content("lxdm", "/etc/systemd/system/display-manager.service"):
            hbox50_lbl.set_text("Lxdm (active)")
        hbox50_lbl.set_name("title")
        hbox50.append(hbox50_lbl)

        hbox51 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox51.append(hseparator)

        hbox160 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label_lxdm_config = Gtk.Label(xalign=0)
        label_lxdm_config.set_text(
            "We recommend to use the default ATT Lxdm configuration setup"
        )
        label_lxdm_config.set_margin_start(10)
        label_lxdm_config.set_margin_end(10)
        hbox160.append(label_lxdm_config)

        hbox170 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        reset_lxdm_original_att = Gtk.Button(
            label="Apply the Lxdm configuration from ATT - auto reboot"
        )
        reset_lxdm_original_att.set_size_request(100, 30)
        reset_lxdm_original_att.connect(
            "clicked", self.on_click_lxdm_reset_original_att
        )
        reset_lxdm_original = Gtk.Button(
            label="Apply your original Lxdm configuration - auto reboot"
        )
        reset_lxdm_original.set_size_request(100, 30)
        reset_lxdm_original.connect("clicked", self.on_click_lxdm_reset)
        reset_lxdm_original_att.set_margin_start(10)
        reset_lxdm_original_att.set_margin_end(10)
        hbox170.append(reset_lxdm_original_att)
        reset_lxdm_original.set_margin_start(10)
        reset_lxdm_original.set_margin_end(10)
        hbox170.append(reset_lxdm_original)

        hbox180 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox180.append(hseparator)

        hbox52 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox52_lbl = Gtk.Label(xalign=0)
        hbox52_lbl.set_text("Autologin")
        self.autologin_lxdm = Gtk.Switch()
        self.autologin_lxdm.connect("notify::active", self.on_autologin_lxdm_activated)
        hbox52_lbl.set_margin_start(10)
        hbox52_lbl.set_margin_end(10)
        hbox52_lbl.set_hexpand(True)
        hbox52.append(hbox52_lbl)
        self.autologin_lxdm.set_margin_start(10)
        self.autologin_lxdm.set_margin_end(10)
        hbox52.append(self.autologin_lxdm)  # pack_end

        hbox54 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox54_lbl = Gtk.Label(xalign=0)
        hbox54_lbl.set_text("Install more Lxdm ATT themes")
        btn_install_arco_lxdm_theme_minimalo = Gtk.Button(label="Install ATT minimalo")
        btn_install_arco_lxdm_theme_minimalo.connect(
            "clicked", self.on_click_install_att_lxdm_minimalo
        )
        btn_remove_arco_lxdm_theme_minimalo = Gtk.Button(label="Remove ATT minimalo")
        btn_remove_arco_lxdm_theme_minimalo.connect(
            "clicked", self.on_click_remove_att_lxdm_minimalo
        )
        hbox54_lbl.set_margin_start(10)
        hbox54_lbl.set_margin_end(10)
        hbox54_lbl.set_hexpand(True)
        hbox54.append(hbox54_lbl)
        btn_install_arco_lxdm_theme_minimalo.set_margin_start(10)
        btn_install_arco_lxdm_theme_minimalo.set_margin_end(10)
        hbox54.append(btn_install_arco_lxdm_theme_minimalo)  # pack_end
        btn_remove_arco_lxdm_theme_minimalo.set_margin_start(10)
        btn_remove_arco_lxdm_theme_minimalo.set_margin_end(10)
        hbox54.append(btn_remove_arco_lxdm_theme_minimalo)  # pack_end

        hbox55 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox55_lbl = Gtk.Label(xalign=0)
        hbox55_lbl.set_text("Install more Lxdm themes")
        btn_install_lxdm_themes = Gtk.Button(label="Install lxdm-themes")
        btn_install_lxdm_themes.connect("clicked", self.on_click_install_lxdm_themes)
        btn_remove_lxdm_themes = Gtk.Button(label="Remove lxdm-themes")
        btn_remove_lxdm_themes.connect("clicked", self.on_click_remove_lxdm_themes)
        hbox55_lbl.set_margin_start(10)
        hbox55_lbl.set_margin_end(10)
        hbox55_lbl.set_hexpand(True)
        hbox55.append(hbox55_lbl)
        btn_install_lxdm_themes.set_margin_start(10)
        btn_install_lxdm_themes.set_margin_end(10)
        hbox55.append(btn_install_lxdm_themes)  # pack_end
        btn_remove_lxdm_themes.set_margin_start(10)
        btn_remove_lxdm_themes.set_margin_end(10)
        hbox55.append(btn_remove_lxdm_themes)  # pack_end

        # lxdm
        hbox57 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox57_lbl = Gtk.Label(xalign=0)
        hbox57_lbl.set_text("Gtk theme")
        self.lxdm_gtk_theme = Gtk.DropDown.new_from_strings([])
        lxdm.pop_gtk_theme_names_lxdm(self.lxdm_gtk_theme)
        hbox57_lbl.set_margin_start(10)
        hbox57_lbl.set_margin_end(10)
        hbox57_lbl.set_hexpand(True)
        hbox57.append(hbox57_lbl)
        self.lxdm_gtk_theme.set_margin_start(10)
        self.lxdm_gtk_theme.set_margin_end(10)
        hbox57.append(self.lxdm_gtk_theme)  # pack_end

        hbox59 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox59_label = Gtk.Label(xalign=0)
        hbox59_label.set_text("Lxdm theme greeter")
        self.lxdm_theme_greeter = Gtk.DropDown.new_from_strings([])
        lxdm.pop_lxdm_theme_greeter(self.lxdm_theme_greeter)
        hbox59_label.set_margin_start(10)
        hbox59_label.set_margin_end(10)
        hbox59_label.set_hexpand(True)
        hbox59.append(hbox59_label)
        self.lxdm_theme_greeter.set_margin_start(10)
        self.lxdm_theme_greeter.set_margin_end(10)
        hbox59.append(self.lxdm_theme_greeter)  # pack_end

        hbox62 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox62_lbl = Gtk.Label(xalign=0)
        hbox62_lbl.set_text(
            "Show the panel at the bottom containing desktops? true/false"
        )
        self.panel_lxdm = Gtk.Switch()
        # self.panel_lxdm.connect("notify::active", self.on_click_lxdm_panel)
        hbox62_lbl.set_margin_start(10)
        hbox62_lbl.set_margin_end(10)
        hbox62_lbl.set_hexpand(True)
        hbox62.append(hbox62_lbl)
        self.panel_lxdm.set_margin_start(10)
        self.panel_lxdm.set_margin_end(10)
        hbox62.append(self.panel_lxdm)  # pack_end

        hbox56 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox56_lbl = Gtk.Label(xalign=0)
        hbox56_lbl.set_text("You can change more settings with the lxdm-config app")
        hbox56_lbl.set_margin_start(10)
        hbox56_lbl.set_margin_end(10)
        hbox56.append(hbox56_lbl)

        hbox58 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        enable_lxdm = Gtk.Button(label="Enable Lxdm")
        enable_lxdm.connect("clicked", self.on_click_lxdm_enable)
        apply = Gtk.Button(label="Apply settings")
        apply.connect("clicked", self.on_click_lxdm_apply)
        # reset = Gtk.Button(label="Reset lxdm.conf")
        # reset.connect("clicked", self.on_click_lxdm_reset)
        hbox58.append(apply)  # pack_end
        # hbox58.pack_end(reset, False, False, 0)
        hbox58.append(enable_lxdm)

        vboxstack3.append(hbox50)
        vboxstack3.append(hbox51)
        vboxstack3.append(hbox160)
        vboxstack3.append(hbox170)
        vboxstack3.append(hbox180)
        vboxstack3.append(hbox52)
        # vboxstack3.pack_start(hbox53, False, False, 0)
        vboxstack3.append(hbox54)
        vboxstack3.append(hbox55)
        vboxstack3.append(hbox57)
        vboxstack3.append(hbox59)
        vboxstack3.append(hbox62)
        vboxstack3.append(hbox56)
        vboxstack3.append(hbox58)  # pack_end

    else:
        # no lxdm installed
        hbox60 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox60_lbl = Gtk.Label(xalign=0)
        hbox60_lbl.set_text("Lxdm is not installed")
        hbox60_lbl.set_name("title")
        hbox60.append(hbox60_lbl)

        hbox61 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox61.append(hseparator)

        vboxstack3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vboxstack3.append(hbox60)
        vboxstack3.append(hbox61)
        message = Gtk.Label()
        message.set_markup("<b>Lxdm does not seem to be installed</b>")

        install_lxdm = Gtk.Button(
            label="Install Lxdm - auto reboot - do not forget to enable it"
        )
        install_lxdm.connect("clicked", self.on_click_att_lxdm_clicked)

        vboxstack3.append(message)
        vboxstack3.append(install_lxdm)

    # ==================================================================
    #                       WALL
    # ==================================================================

    hbox70 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox70_lbl = Gtk.Label(xalign=0)
    hbox70_lbl.set_text("Choose the background of your login manager")
    hbox70_lbl.set_name("title")
    hbox70.append(hbox70_lbl)

    hbox71 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox71.append(hseparator)

    hbox72 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox72_lbl = Gtk.Label(xalign=0)
    hbox72_lbl.set_text("Choose the login manager you want to change")
    hbox72_lbl.set_margin_start(10)
    hbox72_lbl.set_margin_end(10)
    hbox72.append(hbox72_lbl)

    hbox73 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox73_lbl = Gtk.Label(xalign=0)
    hbox73_lbl.set_text("Login Manager")
    self.login_managers_combo = Gtk.DropDown.new_from_strings([])
    sddm.pop_login_managers_combo(self, self.login_managers_combo)
    hbox73_lbl.set_margin_start(10)
    hbox73_lbl.set_margin_end(10)
    hbox73_lbl.set_hexpand(True)
    hbox73.append(hbox73_lbl)
    self.login_managers_combo.set_margin_start(10)
    self.login_managers_combo.set_margin_end(10)
    hbox73.append(self.login_managers_combo)  # pack_end

    hbox111 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label111 = Gtk.Label(label="Import image")
    self.login_image = Gtk.Entry()
    btnsearch = Gtk.Button(label=". . .")
    btnsearch.connect("clicked", self.on_choose_login_wallpaper)
    label111.set_margin_start(10)
    label111.set_margin_end(10)
    hbox111.append(label111)
    self.login_image.set_hexpand(True)
    self.login_image.set_vexpand(True)
    self.login_image.set_margin_start(10)
    self.login_image.set_margin_end(10)
    hbox111.append(self.login_image)
    btnsearch.set_margin_start(10)
    btnsearch.set_margin_end(10)
    hbox111.append(btnsearch)

    hbox113 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label113 = Gtk.Label()
    if fn.check_package_installed("archlinux-login-backgrounds-git"):
        label113.set_text("Install our selection of wallpapers (installed)")
    else:
        label113.set_text("Install our selection of wallpapers")
    btn_att_install = Gtk.Button(label="Install ATT backgrounds")
    btn_att_install.connect("clicked", self.on_install_att_backgrounds)
    btn_att_remove = Gtk.Button(label="Remove ATT backgrounds")
    btn_att_remove.connect("clicked", self.on_remove_att_backgrounds)
    btn_att_install.set_margin_start(10)
    btn_att_install.set_margin_end(10)
    hbox113.append(btn_att_install)  # pack_end
    btn_att_remove.set_margin_start(10)
    btn_att_remove.set_margin_end(10)
    hbox113.append(btn_att_remove)  # pack_end
    label113.set_margin_start(10)
    label113.set_margin_end(10)
    hbox113.append(label113)

    hbox116 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label116 = Gtk.Label()
    if fn.check_package_installed("archlinux-login-backgrounds-git"):
        label116.set_text("Install our selection of wallpapers (installed)")
    else:
        label116.set_text("Install our selection of wallpapers")
    btn_att_plain_install = Gtk.Button(label="Install ATT plain backgrounds")
    btn_att_plain_install.connect("clicked", self.on_install_att_plain_backgrounds)
    btn_att_plain_remove = Gtk.Button(label="Remove ATT plain backgrounds")
    btn_att_plain_remove.connect("clicked", self.on_remove_att_plain_backgrounds)
    btn_att_plain_install.set_margin_start(10)
    btn_att_plain_install.set_margin_end(10)
    hbox116.append(btn_att_plain_install)  # pack_end
    btn_att_plain_remove.set_margin_start(10)
    btn_att_plain_remove.set_margin_end(10)
    hbox116.append(btn_att_plain_remove)  # pack_end
    label116.set_margin_start(10)
    label116.set_margin_end(10)
    hbox116.append(label116)

    hbox112 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    btn_login_import = Gtk.Button(label="Import selected image")
    btn_login_import.connect("clicked", self.on_import_login_wallpaper)
    btn_remove_import = Gtk.Button(label="Remove selected image")
    btn_remove_import.connect("clicked", self.on_import_remove_login_wallpaper)
    btn_login_import.set_margin_start(10)
    btn_login_import.set_margin_end(10)
    hbox112.append(btn_login_import)  # pack_end
    btn_remove_import.set_margin_start(10)
    btn_remove_import.set_margin_end(10)
    hbox112.append(btn_remove_import)  # pack_end

    hbox115 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox115.append(hseparator)

    hbox114 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label114 = Gtk.Label()
    label114.set_text("Select a wallpaper and apply")
    label114.set_margin_start(10)
    label114.set_margin_end(10)
    hbox114.append(label114)

    scrolled = Gtk.ScrolledWindow()
    scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    wallpaper_list = fn.get_login_wallpapers()
    self.login_wallpapers_combo = Gtk.DropDown.new_from_strings([])
    self.pop_login_wallpapers(self.login_wallpapers_combo, wallpaper_list, True)
    self.flowbox_wall.set_valign(Gtk.Align.START)
    self.flowbox_wall.set_max_children_per_line(6)
    self.flowbox_wall.set_selection_mode(Gtk.SelectionMode.SINGLE)
    self.flowbox_wall.connect("child-activated", self.on_login_wallpaper_clicked)
    scrolled.set_child(self.flowbox_wall)
    self.login_wallpapers_combo.connect("notify::selected", self.on_login_wallpaper_change)

    hbox119 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    login_apply = Gtk.Button(label="Select and apply background")
    login_apply.connect("clicked", self.on_set_login_wallpaper)
    login_reset = Gtk.Button(label="Reset to the original background")
    login_reset.connect("clicked", self.on_reset_login_wallpaper)

    login_reset.set_hexpand(True)
    hbox119.append(login_reset)
    hbox119.append(login_apply)  # pack_end

    vboxstack4.append(hbox70)
    vboxstack4.append(hbox71)
    vboxstack4.append(hbox113)
    vboxstack4.append(hbox116)
    vboxstack4.append(hbox72)
    vboxstack4.append(hbox73)
    vboxstack4.append(hbox111)
    vboxstack4.append(hbox112)
    vboxstack4.append(hbox114)
    vboxstack4.append(hbox115)
    scrolled.set_hexpand(True)
    scrolled.set_vexpand(True)
    vboxstack4.append(scrolled)
    vboxstack4.append(hbox119)  # pack_end

    # ==================================================================
    #                       PACK TO STACK
    # ==================================================================
    if not fn.distr == "manjaro":
        stack.add_titled(vboxstack1, "stack1", "SDDM")
    stack.add_titled(vboxstack2, "stack2", "LIGHTDM")
    stack.add_titled(vboxstack3, "stack3", "LXDM")
    stack.add_titled(vboxstack4, "stack4", "WALL")

    vbox.append(stack_switcher)
    stack.set_hexpand(True)
    stack.set_vexpand(True)
    vbox.append(stack)

    vboxstack22.append(hbox1)
    vboxstack22.append(hbox0)
    vbox.set_hexpand(True)
    vbox.set_vexpand(True)
    vboxstack22.append(vbox)
