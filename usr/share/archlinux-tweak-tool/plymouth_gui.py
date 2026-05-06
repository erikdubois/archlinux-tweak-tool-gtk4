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
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hbox_sep.append(hseparator)

    # ── current theme ──────────────────────────────────────────────────────

    hbox_current = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_current.set_margin_start(10)
    hbox_current.set_margin_top(10)
    lbl_current_title = Gtk.Label(xalign=0)
    lbl_current_title.set_markup("<b>Active theme</b>")
    lbl_current_title.set_size_request(120, -1)
    lbl_current = Gtk.Label(xalign=0)
    lbl_current.set_text(plymouth.get_current_theme())
    hbox_current.append(lbl_current_title)
    hbox_current.append(lbl_current)

    # ── theme selector ─────────────────────────────────────────────────────

    hbox_select = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_select.set_margin_start(10)
    hbox_select.set_margin_top(6)
    lbl_select = Gtk.Label(xalign=0)
    lbl_select.set_markup("<b>Select theme</b>")
    lbl_select.set_size_request(120, -1)

    dropdown = Gtk.ComboBoxText()
    for theme in plymouth.list_themes():
        dropdown.append_text(theme)

    current = plymouth.get_current_theme()
    themes = plymouth.list_themes()
    if current in themes:
        dropdown.set_active(themes.index(current))
    else:
        dropdown.set_active(0)

    hbox_select.append(lbl_select)
    hbox_select.append(dropdown)

    # ── apply ──────────────────────────────────────────────────────────────

    hbox_apply = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_apply.set_margin_start(10)
    hbox_apply.set_margin_top(10)

    btn_apply = Gtk.Button(label="Apply theme")
    btn_apply.set_size_request(140, 30)

    hbox_apply.append(btn_apply)

    # ── description ────────────────────────────────────────────────────────

    hbox_desc = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_desc.set_margin_start(10)
    hbox_desc.set_margin_top(10)
    lbl_desc = Gtk.Label(xalign=0)
    lbl_desc.set_markup(
        "Applying a theme runs <tt>plymouth-set-default-theme -R</tt> which\n"
        "rebuilds the initramfs. This takes a few seconds and requires root."
    )
    lbl_desc.set_wrap(True)
    hbox_desc.append(lbl_desc)

    # ── callback ───────────────────────────────────────────────────────────

    def on_apply_clicked(_widget):
        selected = dropdown.get_active_text()
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

        def run_terminal():
            process = fn.subprocess.Popen(
                ["alacritty", "-e", "bash", "-c", script],
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.PIPE,
            )
            process.wait()
            fn.GLib.idle_add(refresh_current)

        fn.threading.Thread(target=run_terminal, daemon=True).start()

    def refresh_current():
        new_theme = plymouth.get_current_theme()
        lbl_current.set_text(new_theme)
        fn.log_success(f"Plymouth theme now: {new_theme}")

    btn_apply.connect("clicked", on_apply_clicked)

    # ── layout ─────────────────────────────────────────────────────────────

    vboxstack_plymouth.append(hbox_title)
    vboxstack_plymouth.append(hbox_sep)
    vboxstack_plymouth.append(hbox_current)
    vboxstack_plymouth.append(hbox_select)
    vboxstack_plymouth.append(hbox_apply)
    vboxstack_plymouth.append(hbox_desc)
