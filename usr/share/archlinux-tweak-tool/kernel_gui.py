# ============================================================
# Authors: Erik Dubois
# ============================================================

import kernel


def gui(self, Gtk, vboxstack, fn):
    """Create the kernel manager GUI."""

    # ── Title ──────────────────────────────────────────────
    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_title = Gtk.Label(xalign=0)
    lbl_title.set_text("Kernel Manager")
    lbl_title.set_name("title")
    lbl_title.set_margin_start(10)
    lbl_title.set_margin_end(10)
    hbox_title.append(lbl_title)

    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    sep.set_hexpand(True)
    hbox_sep.append(sep)

    # ── Chaotic-AUR notice ────────────────────────────────
    hbox_notice = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_notice = Gtk.Label(xalign=0)
    lbl_notice.set_text("You will see the chaotic-aur kernels only when adding the repo in the Pacman tab.")
    lbl_notice.set_margin_start(10)
    lbl_notice.set_margin_end(10)
    hbox_notice.append(lbl_notice)

    # ── Running kernel info ────────────────────────────────
    hbox_running = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_running = Gtk.Label(xalign=0)
    lbl_running.set_margin_start(10)
    running_pkg = kernel.get_running_kernel()
    running_info = running_pkg or "unknown"
    if running_pkg:
        installed = kernel.get_installed_kernels()
        if running_pkg in installed:
            version = installed.get(running_pkg, "")
            if version:
                running_info = f"{running_pkg} {version}"
    lbl_running.set_markup(f"Running kernel: <b>{running_info}</b>")
    hbox_running.append(lbl_running)

    vboxstack.append(hbox_title)
    vboxstack.append(hbox_sep)
    vboxstack.append(hbox_notice)
    vboxstack.append(hbox_running)

    # ── Default boot entry (systemd-boot only) ────────────
    if kernel.is_systemd_boot():
        refresh_boot = _build_boot_entry_selector(self, Gtk, vboxstack, fn)
    else:
        _build_boot_entry_unavailable(Gtk, vboxstack)
        refresh_boot = None

    # ── Kernel rows ───────────────────────────────────────
    vbox_kernels = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack.append(vbox_kernels)

    last_chaotic = [fn.check_chaotic_aur_active()]
    _populate_kernel_rows(self, Gtk, vbox_kernels, fn, refresh_boot)

    def on_map(_widget):
        current = fn.check_chaotic_aur_active()
        if current == last_chaotic[0]:
            return
        last_chaotic[0] = current
        _clear_box(vbox_kernels)
        _populate_kernel_rows(self, Gtk, vbox_kernels, fn, refresh_boot)

    vbox_kernels.connect("map", on_map)


def _offer_install_packages(self, Gtk, fn, missing):
    pkg_list = "\n".join(f"  • {req['pkg']} ({req['repo']})" for req in missing)
    reasons = "\n".join(f"  • {req['reason']}" for req in missing)

    dialog = Gtk.MessageDialog(
        transient_for=self,
        modal=True,
        message_type=Gtk.MessageType.QUESTION,
        buttons=Gtk.ButtonsType.YES_NO,
        text="Missing required packages",
        secondary_text=(
            f"The following packages are needed for full kernel management:\n\n"
            f"{pkg_list}\n\n"
            f"Reason:\n{reasons}\n\n"
            f"Would you like to install them now?"
        ),
    )

    def on_response(_dialog, response):
        _dialog.destroy()
        if response == Gtk.ResponseType.YES:
            _install_missing_packages(self, fn, [req["pkg"] for req in missing])

    dialog.connect("response", on_response)
    dialog.present()


def _install_missing_packages(self, fn, pkg_names):
    pkgs = " ".join(f'"{p}"' for p in pkg_names)
    script = f"""#!/bin/bash
tput setaf 6
echo "================================================================"
echo "  Installing required packages"
echo "================================================================"
tput sgr0

pacman -S {pkgs} --noconfirm --needed
RESULT=$?

echo
if [ $RESULT -eq 0 ]; then
    tput setaf 2
    echo "================================================================"
    echo "  ✓ Successfully installed required packages"
    echo "================================================================"
    tput sgr0
else
    tput setaf 1
    echo "================================================================"
    echo "  ✗ Installation failed"
    echo "================================================================"
    tput sgr0
fi

echo
echo "###############################################################################"
echo "###                DONE - YOU CAN CLOSE THIS WINDOW                        ####"
echo "###############################################################################"
read -p 'Press Enter to close...'"""
    fn.log_subsection("Installing missing kernel management packages...")
    fn.show_in_app_notification(self, f"Installing {', '.join(pkg_names)}...")
    fn.threading.Thread(
        target=lambda: fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script]).wait(),
        daemon=True,
    ).start()


def _clear_box(box):
    child = box.get_first_child()
    while child:
        nxt = child.get_next_sibling()
        box.remove(child)
        child = nxt


def _populate_kernel_rows(self, Gtk, vbox_kernels, fn, refresh_boot):
    chaotic_enabled = fn.check_chaotic_aur_active()
    installed_pkgs = kernel.get_installed_kernels()
    cpu_info = kernel.get_cpu_info()
    running_pkg = kernel.get_running_kernel()
    current_group = None
    for k in kernel.KERNELS:
        if k.get("requires_chaotic") and not chaotic_enabled:
            continue
        grp = k.get("group", "")
        if grp != current_group:
            current_group = grp
            _build_group_header(Gtk, vbox_kernels, grp)
        _build_kernel_row(self, Gtk, vbox_kernels, fn, k, running_pkg, installed_pkgs, cpu_info, refresh_boot)


def _build_group_header(Gtk, vboxstack, title):
    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    sep.set_hexpand(True)
    hbox_sep.append(sep)

    hbox_hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl = Gtk.Label(xalign=0)
    lbl.set_markup(f"<b>{title}</b>")
    lbl.set_margin_start(10)
    lbl.set_margin_end(10)
    hbox_hdr.append(lbl)

    vboxstack.append(hbox_sep)
    vboxstack.append(hbox_hdr)


def _build_kernel_row(self, Gtk, vboxstack, fn, k, running_pkg, installed_pkgs, cpu_info, refresh_boot=None):
    pkg = k["pkg"]
    headers = k["headers"]
    compatible = kernel.is_kernel_compatible(k, cpu_info)

    # Label row
    hbox_label = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl = Gtk.Label(xalign=0)
    lbl.set_markup(f"<b>{k['label']}</b>  <small>{k['description']}</small>")
    lbl.set_margin_start(25)
    hbox_label.append(lbl)

    url = k.get("url", "")
    if url:
        lbl_link = Gtk.Label(xalign=0)
        lbl_link.set_markup(f'<a href="{url}">more info</a>')
        lbl_link.set_margin_start(10)
        lbl_link.connect(
            "activate-link",
            lambda _lbl, uri: (
                fn.subprocess.Popen(
                    ["sudo", "-u", fn.sudo_username, "xdg-open", uri]
                ),
                True,  # return True to prevent GTK's default handler
            )[-1],
        )
        hbox_label.append(lbl_link)

    # Status + button row
    hbox_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_row.set_margin_start(25)
    hbox_row.set_margin_end(10)

    status_label = Gtk.Label(xalign=0)
    status_label.set_hexpand(True)

    btn = Gtk.Button()
    btn.set_size_request(160, -1)

    handler_id = [None]

    def refresh(sl=status_label, b=btn, p=pkg, h=headers, hid=handler_id, rk=running_pkg, c=compatible):
        pkgs = kernel.get_installed_kernels()
        installed = p in pkgs
        is_running = (rk == p)

        if installed:
            version = pkgs.get(p, "")
            ver_str = f"  <small>{version}</small>" if version else ""
            if is_running:
                sl.set_markup(f"<b>installed</b>{ver_str}  <small>(running)</small>")
            else:
                sl.set_markup(f"<b>installed</b>{ver_str}")
            b.set_label(f"Remove {p}")
            b.set_sensitive(not is_running)
        elif not c:
            sl.set_markup("<small>not compatible with your CPU</small>")
            b.set_label(f"Install {p}")
            b.set_sensitive(False)
            return False
        else:
            sl.set_markup("not installed")
            b.set_label(f"Install {p}")
            b.set_sensitive(True)

        if hid[0]:
            b.disconnect(hid[0])
            hid[0] = None

        def launch_and_wait(process, action, pkg_name):
            process.wait()
            fn.log_success(f"{action} completed for {pkg_name}")
            fn.GLib.idle_add(lambda: (
                fn.show_in_app_notification(self, f"{action} completed for {pkg_name}"),
                refresh(),
                refresh_boot() if refresh_boot else None,
            ))

        if installed and not is_running:
            hid[0] = b.connect(
                "clicked",
                lambda _w: fn.threading.Thread(
                    target=launch_and_wait,
                    args=(kernel.remove_kernel(self, p, h), "Removal", p),
                    daemon=True,
                ).start(),
            )
        elif not installed:
            def on_install_clicked(_w, _p=p, _h=h):
                import kernel_distros
                missing = kernel_distros.get_missing_requirements()
                if missing:
                    for req in missing:
                        fn.log_warn(f"Missing: {req['pkg']} — {req['reason']}")
                    _offer_install_packages(self, Gtk, fn, missing)
                    return
                fn.threading.Thread(
                    target=launch_and_wait,
                    args=(kernel.install_kernel(self, _p, _h), "Installation", _p),
                    daemon=True,
                ).start()
            hid[0] = b.connect("clicked", on_install_clicked)

        return False

    # Initial render using pre-fetched data — no subprocess
    initial_installed = pkg in installed_pkgs
    is_running_init = (running_pkg == pkg)
    if not compatible and not initial_installed:
        status_label.set_markup("<small>not compatible with your CPU</small>")
        btn.set_label(f"Install {pkg}")
        btn.set_sensitive(False)
    elif initial_installed:
        ver = installed_pkgs.get(pkg, "")
        ver_str = f"  <small>{ver}</small>" if ver else ""
        if is_running_init:
            status_label.set_markup(f"<b>installed</b>{ver_str}  <small>(running)</small>")
        else:
            status_label.set_markup(f"<b>installed</b>{ver_str}")
        btn.set_label(f"Remove {pkg}")
        btn.set_sensitive(not is_running_init)
        if not is_running_init:
            def remove_and_notify():
                kernel.remove_kernel(self, pkg, headers).wait()
                fn.log_success(f"Removal completed for {pkg}")
                fn.GLib.idle_add(lambda: (
                    fn.show_in_app_notification(self, f"Removal completed for {pkg}"),
                    refresh(),
                    refresh_boot() if refresh_boot else None,
                ))
            handler_id[0] = btn.connect(
                "clicked",
                lambda _w: fn.threading.Thread(target=remove_and_notify, daemon=True).start(),
            )
    else:
        status_label.set_markup("not installed")
        btn.set_label(f"Install {pkg}")

        def install_and_notify():
            import kernel_distros
            missing = kernel_distros.get_missing_requirements()
            if missing:
                for req in missing:
                    fn.log_warn(f"Missing: {req['pkg']} — {req['reason']}")
                fn.GLib.idle_add(_offer_install_packages, self, Gtk, fn, missing)
                return
            kernel.install_kernel(self, pkg, headers).wait()
            fn.log_success(f"Installation completed for {pkg}")
            fn.GLib.idle_add(lambda: (
                fn.show_in_app_notification(self, f"Installation completed for {pkg}"),
                refresh(),
                refresh_boot() if refresh_boot else None,
            ))
        handler_id[0] = btn.connect(
            "clicked",
            lambda _w: fn.threading.Thread(target=install_and_notify, daemon=True).start(),
        )

    hbox_row.append(status_label)
    hbox_row.append(btn)

    vboxstack.append(hbox_label)
    vboxstack.append(hbox_row)


def _build_boot_entry_selector(self, Gtk, vboxstack, fn):
    boot_entries = kernel.get_boot_entries()
    if not boot_entries:
        return

    current_default = kernel.get_default_boot_entry()

    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    sep.set_hexpand(True)
    hbox_sep.append(sep)

    hbox_hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl = Gtk.Label(xalign=0)
    lbl.set_markup("<b>Default Boot Entry (only systemd-boot)</b>")
    lbl.set_margin_start(10)
    lbl.set_margin_end(10)
    hbox_hdr.append(lbl)

    vboxstack.append(hbox_sep)
    vboxstack.append(hbox_hdr)

    hbox_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_row.set_margin_start(25)
    hbox_row.set_margin_end(10)

    combo = Gtk.ComboBoxText()
    combo.set_hexpand(True)
    combo_active_id = [None]
    id_to_title = {}

    for entry_id, title, kernel_pkg in boot_entries:
        label = f"{title} — {kernel_pkg}" if kernel_pkg else title
        combo.append(entry_id, label)
        id_to_title[entry_id] = label
        if entry_id == current_default:
            combo_active_id[0] = entry_id

    if combo_active_id[0]:
        combo.set_active_id(combo_active_id[0])

    lbl_current = Gtk.Label(xalign=0)
    lbl_current.set_margin_start(25)
    if current_default:
        current_label = id_to_title.get(current_default, current_default)
        lbl_current.set_markup(f"<small>Current: {current_label}</small>")
    else:
        lbl_current.set_markup("<small>Current: unknown</small>")

    def on_set_default(_widget):
        import kernel_distros
        missing = kernel_distros.get_missing_requirements()
        if missing:
            for req in missing:
                fn.log_warn(f"Missing required package: {req['pkg']} from {req['repo']} — {req['reason']}")
            _offer_install_packages(self, Gtk, fn, missing)
            return

        selected_id = combo.get_active_id()
        if selected_id:
            label = id_to_title.get(selected_id, selected_id)
            fn.log_info(f"Setting default boot entry to: {label}")
            success = kernel.set_default_boot_entry(selected_id)
            if success:
                fn.log_success(f"Default boot entry set to: {label} — Reboot to verify")
                _refresh_boot_entry_display(label, lbl_current)
                fn.show_in_app_notification(self, f"Default boot entry set to: {label} — Reboot to verify")
            else:
                fn.log_error(f"Failed to set default boot entry: {label}")
                fn.show_in_app_notification(self, f"Failed to set default boot entry: {label}")

    btn_set = Gtk.Button(label="Set as Default")
    btn_set.set_size_request(160, -1)
    btn_set.connect("clicked", on_set_default)

    hbox_row.append(combo)
    hbox_row.append(btn_set)

    vboxstack.append(hbox_row)
    vboxstack.append(lbl_current)

    def refresh_combo():
        new_entries = kernel.get_boot_entries()
        combo.remove_all()
        id_to_title.clear()
        for entry_id, title, kernel_pkg in new_entries:
            label = f"{title} — {kernel_pkg}" if kernel_pkg else title
            combo.append(entry_id, label)
            id_to_title[entry_id] = label
        new_default = kernel.get_default_boot_entry()
        if new_default:
            combo.set_active_id(new_default)

    return refresh_combo


def _build_boot_entry_unavailable(Gtk, vboxstack):
    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    sep.set_hexpand(True)
    hbox_sep.append(sep)

    hbox_hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_hdr = Gtk.Label(xalign=0)
    lbl_hdr.set_markup("<b>Default Boot Entry</b>")
    lbl_hdr.set_margin_start(10)
    lbl_hdr.set_margin_end(10)
    hbox_hdr.append(lbl_hdr)

    hbox_msg = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_msg = Gtk.Label(xalign=0)
    lbl_msg.set_text("Setting a default boot entry is only available on systemd-boot systems.")
    lbl_msg.set_margin_start(25)
    lbl_msg.set_margin_end(10)
    lbl_msg.set_margin_top(5)
    lbl_msg.set_margin_bottom(10)
    hbox_msg.append(lbl_msg)

    vboxstack.append(hbox_sep)
    vboxstack.append(hbox_hdr)
    vboxstack.append(hbox_msg)


def _refresh_boot_entry_display(entry_id, label_widget):
    label_widget.set_markup(f"<small>Current: {entry_id}</small>")
