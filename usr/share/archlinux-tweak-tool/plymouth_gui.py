import plymouth


def gui(self, Gtk, vboxstack_plymouth, fn):
    fn.log_section("Plymouth Boot Theme")

    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_title_label = Gtk.Label(xalign=0)
    hbox_title_label.set_text("Plymouth")
    hbox_title_label.set_name("title")
    hbox_title_label.set_margin_start(10)
    hbox_title_label.set_margin_end(10)
    hbox_title.append(hbox_title_label)

    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hsep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hsep.set_hexpand(True)
    hbox_sep.append(hsep)

    # ── installed themes ───────────────────────────────────────────────────

    hbox_installed_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_installed_header.set_margin_start(10)
    hbox_installed_header.set_margin_top(10)
    lbl_installed_header = Gtk.Label(xalign=0)
    lbl_installed_header.set_markup("<b>Installed themes</b>")
    hbox_installed_header.append(lbl_installed_header)

    hbox_current = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_current.set_margin_start(10)
    hbox_current.set_margin_top(4)
    lbl_current_title = Gtk.Label(xalign=0)
    lbl_current_title.set_markup("<b>Active theme</b>")
    lbl_current_title.set_size_request(120, -1)
    lbl_current = Gtk.Label(xalign=0)
    lbl_current.set_text(plymouth.get_current_theme())
    hbox_current.append(lbl_current_title)
    hbox_current.append(lbl_current)

    hbox_select = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_select.set_margin_start(10)
    hbox_select.set_margin_top(6)
    lbl_select = Gtk.Label(xalign=0)
    lbl_select.set_markup("<b>Select theme</b>")
    lbl_select.set_size_request(120, -1)

    dd_installed = Gtk.ComboBoxText()
    hbox_select.append(lbl_select)
    hbox_select.append(dd_installed)

    hbox_apply = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_apply.set_margin_start(10)
    hbox_apply.set_margin_top(6)
    btn_apply = Gtk.Button(label="Apply theme")
    btn_apply.set_size_request(140, 30)
    hbox_apply.append(btn_apply)

    hbox_apply_desc = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_apply_desc.set_margin_start(10)
    hbox_apply_desc.set_margin_top(4)
    lbl_apply_desc = Gtk.Label(xalign=0)
    lbl_apply_desc.set_markup(
        "Applying a theme runs <tt>plymouth-set-default-theme -R</tt> which\n"
        "rebuilds the initramfs. This takes a few seconds."
    )
    hbox_apply_desc.append(lbl_apply_desc)

    hbox_reset = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_reset.set_margin_start(10)
    hbox_reset.set_margin_top(6)
    btn_reset = Gtk.Button(label="Reset to Omarchy default")
    btn_reset.set_size_request(200, 30)
    hbox_reset.append(btn_reset)

    # ── separator ──────────────────────────────────────────────────────────

    hbox_sep2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_sep2.set_margin_top(14)
    hsep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hsep2.set_hexpand(True)
    hbox_sep2.append(hsep2)

    # ── available themes ───────────────────────────────────────────────────

    hbox_avail_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_avail_header.set_margin_start(10)
    hbox_avail_header.set_margin_top(10)
    lbl_avail_header = Gtk.Label(xalign=0)
    lbl_avail_header.set_markup("<b>Available themes</b>")
    hbox_avail_header.append(lbl_avail_header)

    hbox_avail_select = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_avail_select.set_margin_start(10)
    hbox_avail_select.set_margin_top(6)
    lbl_avail_select = Gtk.Label(xalign=0)
    lbl_avail_select.set_markup("<b>Select package</b>")
    lbl_avail_select.set_size_request(120, -1)

    dd_available = Gtk.ComboBoxText()
    hbox_avail_select.append(lbl_avail_select)
    hbox_avail_select.append(dd_available)

    hbox_install = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_install.set_margin_start(10)
    hbox_install.set_margin_top(6)
    btn_install = Gtk.Button(label="Install theme")
    btn_install.set_size_request(140, 30)
    hbox_install.append(btn_install)

    aur_helper = fn.get_aur_helper()
    if not aur_helper:
        btn_install.set_sensitive(False)
        lbl_no_aur = Gtk.Label(xalign=0)
        lbl_no_aur.set_markup("<i>No AUR helper found (paru/yay required)</i>")
        lbl_no_aur.set_margin_start(10)
        hbox_install.append(lbl_no_aur)

    # ── populate dropdowns ─────────────────────────────────────────────────

    def populate_installed():
        dd_installed.remove_all()
        themes = plymouth.list_themes()
        current = plymouth.get_current_theme()
        for t in themes:
            dd_installed.append_text(t)
        if current in themes:
            dd_installed.set_active(themes.index(current))
        elif themes:
            dd_installed.set_active(0)

    def populate_available():
        dd_available.remove_all()
        pkgs = plymouth.list_available_packages()
        for p in pkgs:
            dd_available.append_text(p)
        if pkgs:
            dd_available.set_active(0)
        btn_install.set_sensitive(bool(pkgs) and aur_helper is not None)

    populate_installed()
    populate_available()

    # ── callbacks ──────────────────────────────────────────────────────────

    def on_apply_clicked(_widget):
        selected = dd_installed.get_active_text()
        if not selected:
            fn.log_warn("No Plymouth theme selected")
            return
        fn.log_subsection(f"Applying Plymouth theme: {selected}")
        fn.show_in_app_notification(self, f"Applying Plymouth theme: {selected}")
        script = (
            f"echo 'Setting Plymouth theme to {selected}...'\n"
            f"plymouth-set-default-theme -R {selected}\n"
            "echo ''\n"
            "read -p 'Done. Press Enter to close...'\n"
        )

        def run_apply():
            process = fn.subprocess.Popen(
                ["alacritty", "-e", "bash", "-c", script],
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.PIPE,
            )
            process.wait()
            fn.os.makedirs("/etc/att", exist_ok=True)
            open("/etc/att/att-omarchy-marker", "w").close()
            fn.log_info("ATT Omarchy marker written to /etc/att/att-omarchy-marker")
            fn.GLib.idle_add(refresh_after_apply)

        fn.threading.Thread(target=run_apply, daemon=True).start()

    def refresh_after_apply():
        new_theme = plymouth.get_current_theme()
        lbl_current.set_text(new_theme)
        fn.log_success(f"Plymouth theme now: {new_theme}")
        populate_installed()

    def on_install_clicked(_widget):
        selected = dd_available.get_active_text()
        if not selected:
            fn.log_warn("No Plymouth package selected")
            return
        fn.log_subsection(f"Installing Plymouth theme package: {selected}")
        fn.show_in_app_notification(self, f"Installing: {selected}")

        def run_install():
            process = fn.launch_aur_install_in_terminal(aur_helper, selected)
            if process:
                process.wait()
            fn.GLib.idle_add(refresh_after_install)

        fn.threading.Thread(target=run_install, daemon=True).start()

    def refresh_after_install():
        populate_installed()
        populate_available()
        fn.log_success("Plymouth theme list refreshed")

    def on_reset_clicked(_widget):
        fn.log_subsection("Resetting Plymouth theme to Omarchy default")
        fn.show_in_app_notification(self, "Resetting Plymouth theme to omarchy...")
        script = (
            "echo 'Resetting Plymouth theme to omarchy...'\n"
            "plymouth-set-default-theme -R omarchy\n"
            "echo ''\n"
            "read -p 'Done. Press Enter to close...'\n"
        )

        def run_reset():
            process = fn.subprocess.Popen(
                ["alacritty", "-e", "bash", "-c", script],
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.PIPE,
            )
            process.wait()
            fn.GLib.idle_add(refresh_after_apply)

        fn.threading.Thread(target=run_reset, daemon=True).start()

    btn_apply.connect("clicked", on_apply_clicked)
    btn_install.connect("clicked", on_install_clicked)
    btn_reset.connect("clicked", on_reset_clicked)

    # ── layout ─────────────────────────────────────────────────────────────

    vboxstack_plymouth.append(hbox_title)
    vboxstack_plymouth.append(hbox_sep)
    vboxstack_plymouth.append(hbox_installed_header)
    vboxstack_plymouth.append(hbox_current)
    vboxstack_plymouth.append(hbox_select)
    vboxstack_plymouth.append(hbox_apply)
    vboxstack_plymouth.append(hbox_apply_desc)
    vboxstack_plymouth.append(hbox_reset)
    vboxstack_plymouth.append(hbox_sep2)
    vboxstack_plymouth.append(hbox_avail_header)
    vboxstack_plymouth.append(hbox_avail_select)
    vboxstack_plymouth.append(hbox_install)
