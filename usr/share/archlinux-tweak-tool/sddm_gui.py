# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools


def gui(self, Gtk, Pango, vboxstack_sddm, sddm, fn):
    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_title = Gtk.Label(xalign=0)
    if fn.check_content("sddm", "/etc/systemd/system/display-manager.service"):
        lbl_title.set_text("Sddm (active)")
    else:
        lbl_title.set_text("Sddm (inactive)")
    lbl_title.set_name("title")
    lbl_title.set_margin_start(10)
    hbox_title.append(lbl_title)

    hbox_sep_top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hsep_top = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hsep_top.set_hexpand(True)
    hsep_top.set_vexpand(False)
    hbox_sep_top.append(hsep_top)

    if fn.check_package_installed("sddm"):

        hbox_section_config = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl_section_config = Gtk.Label(xalign=0)
        lbl_section_config.set_markup("<b>Configuration Setup</b>")
        lbl_section_config.set_margin_start(10)
        lbl_section_config.set_margin_top(6)
        hbox_section_config.append(lbl_section_config)

        hbox_config_info = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl_config_info = Gtk.Label(xalign=0)
        lbl_config_info.set_text(
            "We recommend to use the default sddm configuration setup\n"
            "Sddm configuration split into two files: /etc/sddm.conf "
            "and /etc/sddm.conf.d/kde_settings.conf\n"
            "/etc/sddm.conf.d/kde_settings.conf contains all the parameters - We will backup your files\n"
            "You can also restore your own original configuration if you want to - auto reboot\n"
        )
        lbl_config_info.set_margin_start(10)
        hbox_config_info.append(lbl_config_info)

        hbox_config_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_apply_att_config = Gtk.Button(label="Apply the Sddm configuration from ATT - auto reboot")
        btn_apply_att_config.connect("clicked", functools.partial(sddm.on_click_sddm_reset_original_att, self))
        btn_apply_att_config.set_margin_start(10)
        btn_apply_att_config.set_margin_end(10)
        hbox_config_btns.append(btn_apply_att_config)
        btn_apply_original_config = Gtk.Button(label="Apply your original Sddm configuration - auto reboot")
        btn_apply_original_config.connect("clicked", functools.partial(sddm.on_click_sddm_reset_original, self))
        btn_apply_original_config.set_margin_end(10)
        hbox_config_btns.append(btn_apply_original_config)

        hbox_sep_config = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hsep_config = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hsep_config.set_hexpand(True)
        hbox_sep_config.append(hsep_config)

        vboxstack_sddm.append(hbox_title)
        vboxstack_sddm.append(hbox_sep_top)
        vboxstack_sddm.append(hbox_section_config)
        vboxstack_sddm.append(hbox_config_info)
        vboxstack_sddm.append(hbox_config_btns)
        vboxstack_sddm.append(hbox_sep_config)

        if fn.path.isfile(fn.sddm_default_d2):
            simplicity_installed = fn.check_package_installed("edu-sddm-simplicity-git")

            hbox_section_login = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            lbl_section_login = Gtk.Label(xalign=0)
            lbl_section_login.set_markup("<b>Login Settings</b>")
            lbl_section_login.set_margin_start(10)
            lbl_section_login.set_margin_top(6)
            hbox_section_login.append(lbl_section_login)

            hbox_auto = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            hbox_auto_lbl = Gtk.Label(xalign=0)
            hbox_auto_lbl.set_text("Auto login enabled or disabled")
            hbox_auto_lbl.set_margin_start(10)
            hbox_auto_lbl.set_hexpand(True)
            self.autologin_sddm = Gtk.Switch()
            self.autologin_sddm.set_active(sddm.get_autologin_state())
            self.autologin_sddm.connect("notify::active", functools.partial(sddm.on_autologin_sddm_activated, self))
            self.autologin_sddm.set_margin_end(10)
            hbox_auto.append(hbox_auto_lbl)
            hbox_auto.append(self.autologin_sddm)

            hbox_session = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            lbl_session = Gtk.Label(xalign=0)
            lbl_session.set_text("Autologin into this desktop")
            lbl_session.set_margin_start(10)
            lbl_session.set_hexpand(True)
            self.sessions_sddm = Gtk.DropDown.new_from_strings([])
            sddm.pop_box(self, self.sessions_sddm)
            self.sessions_sddm.set_margin_end(10)
            self.sessions_sddm.connect(
                "notify::selected",
                functools.partial(sddm.on_sddm_setting_changed, self, "Session changed"),
            )
            hbox_session.append(lbl_session)
            hbox_session.append(self.sessions_sddm)

            hbox_theme = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            lbl_theme = Gtk.Label(xalign=0)
            lbl_theme.set_text("Theme")
            lbl_theme.set_margin_start(10)
            lbl_theme.set_hexpand(True)
            self.theme_sddm = Gtk.DropDown.new_from_strings([])
            sddm.pop_theme_box(self, self.theme_sddm)
            self.theme_sddm.set_margin_end(10)
            self.theme_sddm.connect(
                "notify::selected",
                functools.partial(sddm.on_sddm_setting_changed, self, "Theme changed"),
            )
            hbox_theme.append(lbl_theme)
            hbox_theme.append(self.theme_sddm)

            hbox_section_cursor = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            lbl_section_cursor = Gtk.Label(xalign=0)
            lbl_section_cursor.set_markup("<b>Cursor Settings</b>")
            lbl_section_cursor.set_margin_start(10)
            lbl_section_cursor.set_margin_top(6)
            hbox_section_cursor.append(lbl_section_cursor)

            hbox_bibata = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            btn_install_bibata = Gtk.Button(label="Install Bibata cursors")
            btn_install_bibata.connect("clicked", functools.partial(sddm.on_click_install_bibata_cursor, self))
            btn_install_bibata.set_margin_start(10)
            btn_install_bibata.set_margin_end(10)
            btn_remove_bibata = Gtk.Button(label="Remove Bibata cursors")
            btn_remove_bibata.connect("clicked", functools.partial(sddm.on_click_remove_bibata_cursor, self))
            btn_remove_bibata.set_margin_end(10)
            hbox_bibata.append(btn_install_bibata)
            hbox_bibata.append(btn_remove_bibata)

            hbox_bibata_extra = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            btn_install_bibata_extra = Gtk.Button(label="Install Bibata extra cursors")
            btn_install_bibata_extra.connect("clicked", functools.partial(sddm.on_click_install_bibatar_cursor, self))
            btn_install_bibata_extra.set_margin_start(10)
            btn_install_bibata_extra.set_margin_end(10)
            btn_remove_bibata_extra = Gtk.Button(label="Remove Bibata extra cursors")
            btn_remove_bibata_extra.connect("clicked", functools.partial(sddm.on_click_remove_bibatar_cursor, self))
            btn_remove_bibata_extra.set_margin_end(10)
            hbox_bibata_extra.append(btn_install_bibata_extra)
            hbox_bibata_extra.append(btn_remove_bibata_extra)

            hbox_cursor_hint = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            lbl_cursor_hint = Gtk.Label(xalign=0)
            lbl_cursor_hint.set_text("Select your cursor theme for the login screen e.g. Bibata-Modern-Ice")
            lbl_cursor_hint.set_margin_start(10)
            hbox_cursor_hint.append(lbl_cursor_hint)

            hbox_cursor = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            lbl_cursor = Gtk.Label(xalign=0)
            lbl_cursor.set_text("Cursor theme SDDM (in tab maintenance you can set the cursor for your whole system)")
            lbl_cursor.set_margin_start(10)
            lbl_cursor.set_hexpand(True)
            self.sddm_cursor_themes = Gtk.DropDown.new_from_strings([])
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
            self.sddm_cursor_themes.set_margin_end(10)
            self.sddm_cursor_themes.connect(
                "notify::selected",
                functools.partial(sddm.on_sddm_setting_changed, self, "Cursor theme changed"),
            )
            hbox_cursor.append(lbl_cursor)
            hbox_cursor.append(self.sddm_cursor_themes)

            hbox_apply = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            btn_apply_settings = Gtk.Button(label="Apply the above mentioned settings")
            btn_apply_settings.connect("clicked", functools.partial(sddm.on_click_sddm_apply, self))
            btn_apply_settings.set_margin_start(10)
            btn_apply_settings.set_margin_end(10)
            btn_enable_sddm = Gtk.Button(label="Install and enable sddm-git (when not yet active)")
            btn_enable_sddm.connect("clicked", functools.partial(sddm.on_click_sddm_enable, self))
            btn_enable_sddm.set_margin_end(10)
            hbox_apply.append(btn_apply_settings)
            hbox_apply.append(btn_enable_sddm)

            hbox_section_wallpaper = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            lbl_section_wallpaper = Gtk.Label(xalign=0)
            lbl_section_wallpaper.set_markup("<b>Wallpaper</b>")
            lbl_section_wallpaper.set_margin_start(10)
            lbl_section_wallpaper.set_margin_top(16)
            hbox_section_wallpaper.append(lbl_section_wallpaper)

            hbox_wp_lbl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            lbl_wp_desc = Gtk.Label(xalign=0)
            lbl_wp_desc.set_text("Set background wallpaper for the Simplicity Sddm theme")
            lbl_wp_desc.set_margin_start(10)
            lbl_wp_desc.set_hexpand(True)
            hbox_wp_lbl.append(lbl_wp_desc)
            self.btn_install_simplicity = Gtk.Button(label="Install Simplicity theme")
            self.btn_install_simplicity.connect("clicked", functools.partial(sddm.on_click_install_simplicity, self))
            self.btn_install_simplicity.set_margin_end(10)
            self.btn_install_simplicity.set_visible(not simplicity_installed)
            hbox_wp_lbl.append(self.btn_install_simplicity)
            self.btn_remove_simplicity = Gtk.Button(label="Remove Simplicity theme")
            self.btn_remove_simplicity.connect("clicked", functools.partial(sddm.on_click_remove_simplicity, self))
            self.btn_remove_simplicity.set_margin_end(10)
            self.btn_remove_simplicity.set_visible(simplicity_installed)
            hbox_wp_lbl.append(self.btn_remove_simplicity)

            hbox_wp_folder = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            self.btn_simplicity_browse = Gtk.Button(label="Select folder")
            self.btn_simplicity_browse.connect("clicked", functools.partial(sddm.on_browse_sddm_folder, self))
            self.btn_simplicity_browse.set_margin_start(10)
            self.btn_simplicity_browse.set_margin_end(10)
            self.btn_simplicity_browse.set_sensitive(simplicity_installed)
            default_wp_folder = "/usr/share/archlinux-tweak-tool/wallpapers"
            self.sddm_folder_entry = Gtk.Entry()
            self.sddm_folder_entry.set_hexpand(True)
            self.sddm_folder_entry.set_text(default_wp_folder)
            self.sddm_folder_entry.set_sensitive(simplicity_installed)
            self.btn_simplicity_load = Gtk.Button(label="Load")
            self.btn_simplicity_load.connect("clicked", functools.partial(sddm.on_load_sddm_folder, self))
            self.btn_simplicity_load.set_margin_start(10)
            self.btn_simplicity_load.set_margin_end(10)
            self.btn_simplicity_load.set_sensitive(simplicity_installed)
            self.btn_simplicity_stop = Gtk.Button(label="Stop")
            self.btn_simplicity_stop.connect("clicked", functools.partial(sddm.on_stop_sddm_loading, self))
            self.btn_simplicity_stop.set_margin_end(10)
            self.btn_simplicity_stop.set_sensitive(simplicity_installed)
            hbox_wp_folder.append(self.btn_simplicity_browse)
            hbox_wp_folder.append(self.sddm_folder_entry)
            hbox_wp_folder.append(self.btn_simplicity_load)
            hbox_wp_folder.append(self.btn_simplicity_stop)

            self.sddm_thumb_flow = Gtk.FlowBox()
            self.sddm_thumb_flow.set_valign(Gtk.Align.START)
            self.sddm_thumb_flow.set_max_children_per_line(20)
            self.sddm_thumb_flow.set_selection_mode(Gtk.SelectionMode.NONE)
            self.sddm_thumb_flow.set_homogeneous(True)
            wp_scroll = Gtk.ScrolledWindow()
            wp_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            wp_scroll.set_hexpand(True)
            wp_scroll.set_size_request(-1, 280)
            wp_scroll.set_margin_start(10)
            wp_scroll.set_margin_end(10)
            wp_scroll.set_child(self.sddm_thumb_flow)
            hbox_wp_scroll = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            hbox_wp_scroll.append(wp_scroll)

            hbox_wp_selected = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            self.sddm_wallpaper_lbl = Gtk.Label(xalign=0)
            self.sddm_wallpaper_lbl.set_text("No wallpaper selected")
            self.sddm_wallpaper_lbl.set_margin_start(10)
            self.sddm_wallpaper_lbl.set_hexpand(True)
            self.sddm_wallpaper_lbl.set_ellipsize(Pango.EllipsizeMode.START)
            hbox_wp_selected.append(self.sddm_wallpaper_lbl)

            hbox_wp_preview = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            self.sddm_wallpaper_preview = Gtk.Picture()
            self.sddm_wallpaper_preview.set_margin_start(10)
            self.sddm_wallpaper_preview.set_margin_end(10)
            self.sddm_wallpaper_preview.set_margin_top(4)
            self.sddm_wallpaper_preview.set_margin_bottom(4)
            self.sddm_wallpaper_preview.set_can_shrink(True)
            self.sddm_wallpaper_preview.set_content_fit(Gtk.ContentFit.CONTAIN)
            self.sddm_wallpaper_preview.set_size_request(-1, 150)
            self.sddm_wallpaper_preview.set_hexpand(True)
            hbox_wp_preview.append(self.sddm_wallpaper_preview)
            default_sddm_wallpaper = "/usr/share/sddm/themes/edu-simplicity/images/background.jpg"
            fallback_wallpaper = "/usr/share/archlinux-tweak-tool/data/wallpaper/wallpaper.jpg"
            if fn.path.isfile(default_sddm_wallpaper):
                self.sddm_wallpaper_lbl.set_text(default_sddm_wallpaper)
                self.sddm_wallpaper_preview.set_filename(default_sddm_wallpaper)
            elif fn.path.isfile(fallback_wallpaper):
                self.sddm_wallpaper_preview.set_filename(fallback_wallpaper)
            else:
                hbox_wp_preview.set_visible(False)

            hbox_wp_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            self.btn_simplicity_apply = Gtk.Button(label="Apply wallpaper")
            self.btn_simplicity_apply.connect("clicked", functools.partial(sddm.on_set_sddm_wallpaper, self))
            self.btn_simplicity_apply.set_margin_start(10)
            self.btn_simplicity_apply.set_margin_end(10)
            self.btn_simplicity_apply.set_sensitive(simplicity_installed)
            self.btn_simplicity_restore = Gtk.Button(label="Restore default")
            self.btn_simplicity_restore.connect("clicked", functools.partial(sddm.on_restore_sddm_wallpaper, self))
            self.btn_simplicity_restore.set_margin_end(10)
            self.btn_simplicity_restore.set_sensitive(simplicity_installed)
            btn_fix_sddm_conf = Gtk.Button(label="Fix SDDM config")
            btn_fix_sddm_conf.set_margin_end(10)
            btn_fix_sddm_conf.connect("clicked", functools.partial(sddm.on_click_fix_sddm_conf, self))
            hbox_wp_btns_spacer = Gtk.Box()
            hbox_wp_btns_spacer.set_hexpand(True)
            hbox_wp_btns.append(self.btn_simplicity_apply)
            hbox_wp_btns.append(self.btn_simplicity_restore)
            hbox_wp_btns.append(hbox_wp_btns_spacer)
            hbox_wp_btns.append(btn_fix_sddm_conf)

            vboxstack_sddm.append(hbox_section_login)
            vboxstack_sddm.append(hbox_auto)
            vboxstack_sddm.append(hbox_session)
            vboxstack_sddm.append(hbox_theme)
            vboxstack_sddm.append(hbox_section_cursor)
            vboxstack_sddm.append(hbox_bibata)
            vboxstack_sddm.append(hbox_bibata_extra)
            vboxstack_sddm.append(hbox_cursor_hint)
            vboxstack_sddm.append(hbox_cursor)
            vboxstack_sddm.append(hbox_apply)
            vboxstack_sddm.append(hbox_section_wallpaper)
            vboxstack_sddm.append(hbox_wp_lbl)
            vboxstack_sddm.append(hbox_wp_folder)
            vboxstack_sddm.append(hbox_wp_selected)
            vboxstack_sddm.append(hbox_wp_preview)
            vboxstack_sddm.append(hbox_wp_btns)
            vboxstack_sddm.append(hbox_wp_scroll)

            if simplicity_installed and fn.path.isdir(default_wp_folder):
                fn.GLib.idle_add(
                    lambda: sddm._populate_sddm_thumbs(self, default_wp_folder),
                    priority=fn.GLib.PRIORITY_LOW,
                )

    else:
        hbox_not_installed = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl_not_installed = Gtk.Label(xalign=0)
        lbl_not_installed.set_text("Sddm is not installed")
        lbl_not_installed.set_name("title")
        lbl_not_installed.set_margin_start(10)
        hbox_not_installed.append(lbl_not_installed)

        hbox_sep_not_installed = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hsep_not_installed = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hsep_not_installed.set_hexpand(True)
        hbox_sep_not_installed.append(hsep_not_installed)

        message = Gtk.Label()
        message.set_markup("<b>Sddm does not seem to be installed</b>")
        message.set_margin_start(10)

        install_sddm = Gtk.Button(label="Install Sddm - auto reboot - do not forget to enable it")
        install_sddm.connect("clicked", functools.partial(sddm.on_click_att_sddm_clicked, self))
        install_sddm.set_margin_start(10)
        install_sddm.set_margin_end(10)

        vboxstack_sddm.append(hbox_title)
        vboxstack_sddm.append(hbox_sep_top)
        vboxstack_sddm.append(hbox_not_installed)
        vboxstack_sddm.append(hbox_sep_not_installed)
        vboxstack_sddm.append(message)
        vboxstack_sddm.append(install_sddm)
