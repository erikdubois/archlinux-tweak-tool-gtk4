# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools


def gui(self, Gtk, Pango, vboxstack_sddm, sddm, fn):
    """create the sddm gui"""
    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox1_lbl = Gtk.Label(xalign=0)
    if fn.check_content("sddm", "/etc/systemd/system/display-manager.service"):
        hbox1_lbl.set_text("Sddm (active)")
    else:
        hbox1_lbl.set_text("Sddm (inactive)")
    hbox1_lbl.set_name("title")
    hbox1_lbl.set_margin_start(10)
    hbox1.append(hbox1_lbl)

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox0.append(hseparator)

    if fn.check_package_installed("sddm"):

        hbox14 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label_sddm_config = Gtk.Label(xalign=0)
        label_sddm_config.set_text(
            "We recommend to use the default sddm configuration setup\n"
            "Sddm configuration split into two files: /etc/sddm.conf "
            "and /etc/sddm.conf.d/kde_settings.conf\n"
            "/etc/sddm.conf.d/kde_settings.conf contains all the parameters - We will backup your files\n"
            "You can also restore your own original configuration if you want to - auto reboot\n"
        )
        label_sddm_config.set_margin_start(10)
        hbox14.append(label_sddm_config)

        hbox13 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        reset_sddm_original_att = Gtk.Button(
            label="Apply the Sddm configuration from ATT - auto reboot"
        )
        reset_sddm_original_att.connect("clicked", functools.partial(sddm.on_click_sddm_reset_original_att, self))
        reset_sddm_original_att.set_margin_start(10)
        reset_sddm_original_att.set_margin_end(10)
        hbox13.append(reset_sddm_original_att)
        reset_sddm_original = Gtk.Button(
            label="Apply your original Sddm configuration - auto reboot"
        )
        reset_sddm_original.connect("clicked", functools.partial(sddm.on_click_sddm_reset_original, self))
        reset_sddm_original.set_margin_end(10)
        hbox13.append(reset_sddm_original)

        hbox05 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hsep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hsep2.set_hexpand(True)
        hbox05.append(hsep2)

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

        hbox18 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox18_lbl = Gtk.Label(xalign=0)
        hbox18_lbl.set_text("Autologin into this desktop")
        hbox18_lbl.set_margin_start(10)
        hbox18_lbl.set_hexpand(True)
        self.sessions_sddm = Gtk.DropDown.new_from_strings([])
        sddm.pop_box(self, self.sessions_sddm)
        self.sessions_sddm.set_margin_end(10)
        self.sessions_sddm.connect(
            "notify::selected",
            functools.partial(sddm.on_sddm_setting_changed, self, "Session changed"),
        )
        hbox18.append(hbox18_lbl)
        hbox18.append(self.sessions_sddm)

        hbox9 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox9_lbl = Gtk.Label(xalign=0)
        hbox9_lbl.set_text("Theme")
        hbox9_lbl.set_margin_start(10)
        hbox9_lbl.set_hexpand(True)
        self.theme_sddm = Gtk.DropDown.new_from_strings([])
        sddm.pop_theme_box(self, self.theme_sddm)
        self.theme_sddm.set_margin_end(10)
        self.theme_sddm.connect(
            "notify::selected",
            functools.partial(sddm.on_sddm_setting_changed, self, "Theme changed"),
        )
        hbox9.append(hbox9_lbl)
        hbox9.append(self.theme_sddm)

        simplicity_installed = fn.check_package_installed("edu-sddm-simplicity-git")

        hbox_wp_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hsep_wp = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hsep_wp.set_hexpand(True)
        hbox_wp_sep.append(hsep_wp)
        hbox_wp_sep.set_margin_top(32)

        hbox_wp_lbl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        wp_lbl = Gtk.Label(xalign=0)
        wp_lbl.set_text("Set background wallpaper for the Simplicity Sddm theme")
        wp_lbl.set_margin_start(10)
        wp_lbl.set_hexpand(True)
        hbox_wp_lbl.append(wp_lbl)
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
        self.sddm_folder_entry = Gtk.Entry()
        self.sddm_folder_entry.set_hexpand(True)
        self.sddm_folder_entry.set_placeholder_text("Paste or type a folder path")
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

        hbox16 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        install_bibata_cursor = Gtk.Button(label="Install Bibata cursors")
        install_bibata_cursor.connect("clicked", functools.partial(sddm.on_click_install_bibata_cursor, self))
        install_bibata_cursor.set_margin_start(10)
        install_bibata_cursor.set_margin_end(10)
        remove_bibata_cursor = Gtk.Button(label="Remove Bibata cursors")
        remove_bibata_cursor.connect("clicked", functools.partial(sddm.on_click_remove_bibata_cursor, self))
        remove_bibata_cursor.set_margin_end(10)
        hbox16.append(install_bibata_cursor)
        hbox16.append(remove_bibata_cursor)

        hbox28 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        install_bibata_cursorr = Gtk.Button(label="Install Bibata extra cursors")
        install_bibata_cursorr.connect("clicked", functools.partial(sddm.on_click_install_bibatar_cursor, self))
        install_bibata_cursorr.set_margin_start(10)
        install_bibata_cursorr.set_margin_end(10)
        remove_bibata_cursorr = Gtk.Button(label="Remove Bibata extra cursors")
        remove_bibata_cursorr.connect("clicked", functools.partial(sddm.on_click_remove_bibatar_cursor, self))
        remove_bibata_cursorr.set_margin_end(10)
        hbox28.append(install_bibata_cursorr)
        hbox28.append(remove_bibata_cursorr)

        hbox17 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox17_lbl = Gtk.Label(xalign=0)
        hbox17_lbl.set_text(
            "Select your cursor theme for the login screen e.g. Bibata-Modern-Ice"
        )
        hbox17_lbl.set_margin_start(10)
        hbox17.append(hbox17_lbl)

        hbox15 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox15_lbl = Gtk.Label(xalign=0)
        hbox15_lbl.set_text("Cursor theme SDDM (in tab maintenance you can set the cursor for your whole system)")
        hbox15_lbl.set_margin_start(10)
        hbox15_lbl.set_hexpand(True)
        self.sddm_cursor_themes = Gtk.DropDown.new_from_strings([])
        sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        self.sddm_cursor_themes.set_margin_end(10)
        self.sddm_cursor_themes.connect(
            "notify::selected",
            functools.partial(sddm.on_sddm_setting_changed, self, "Cursor theme changed"),
        )
        hbox15.append(hbox15_lbl)
        hbox15.append(self.sddm_cursor_themes)

        hbox90 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        apply_sddm_settings = Gtk.Button(label="Apply the above mentioned settings")
        apply_sddm_settings.connect("clicked", functools.partial(sddm.on_click_sddm_apply, self))
        apply_sddm_settings.set_margin_start(10)
        apply_sddm_settings.set_margin_end(10)
        enable_sddm = Gtk.Button(label="Install and enable sddm-git (when not yet active)")
        enable_sddm.connect("clicked", functools.partial(sddm.on_click_sddm_enable, self))
        enable_sddm.set_margin_end(10)
        hbox90.append(apply_sddm_settings)
        hbox90.append(enable_sddm)

        vboxstack_sddm.append(hbox1)
        vboxstack_sddm.append(hbox0)
        vboxstack_sddm.append(hbox14)
        vboxstack_sddm.append(hbox13)
        vboxstack_sddm.append(hbox05)

        if fn.path.isfile(fn.sddm_default_d2):
            vboxstack_sddm.append(hbox_auto)
            vboxstack_sddm.append(hbox18)
            vboxstack_sddm.append(hbox9)
            vboxstack_sddm.append(hbox16)
            vboxstack_sddm.append(hbox28)
            vboxstack_sddm.append(hbox17)
            vboxstack_sddm.append(hbox15)
            vboxstack_sddm.append(hbox90)
            vboxstack_sddm.append(hbox_wp_sep)
            vboxstack_sddm.append(hbox_wp_lbl)
            vboxstack_sddm.append(hbox_wp_folder)
            vboxstack_sddm.append(hbox_wp_selected)
            vboxstack_sddm.append(hbox_wp_preview)
            vboxstack_sddm.append(hbox_wp_btns)
            vboxstack_sddm.append(hbox_wp_scroll)

    else:
        hbox31 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl_not_installed = Gtk.Label(xalign=0)
        lbl_not_installed.set_text("Sddm is not installed")
        lbl_not_installed.set_name("title")
        lbl_not_installed.set_margin_start(10)
        hbox31.append(lbl_not_installed)

        hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hsep3 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hsep3.set_hexpand(True)
        hbox41.append(hsep3)

        message = Gtk.Label()
        message.set_markup("<b>Sddm does not seem to be installed</b>")
        message.set_margin_start(10)

        install_sddm = Gtk.Button(
            label="Install Sddm - auto reboot - do not forget to enable it"
        )
        install_sddm.connect("clicked", functools.partial(sddm.on_click_att_sddm_clicked, self))
        install_sddm.set_margin_start(10)
        install_sddm.set_margin_end(10)

        vboxstack_sddm.append(hbox1)
        vboxstack_sddm.append(hbox0)
        vboxstack_sddm.append(hbox31)
        vboxstack_sddm.append(hbox41)
        vboxstack_sddm.append(message)
        vboxstack_sddm.append(install_sddm)
