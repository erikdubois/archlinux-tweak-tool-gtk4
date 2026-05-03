# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================


def gui(self, Gtk, vboxstack_performance, performance, fn):
    """create the performance gui"""
    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_title_label = Gtk.Label(xalign=0)
    hbox_title_label.set_text("Performance")
    hbox_title_label.set_name("title")
    hbox_title_label.set_margin_start(10)
    hbox_title_label.set_margin_end(10)
    hbox_title.append(hbox_title_label)

    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox_sep.append(hseparator)

    # ============================================================
    # Tuned Block
    # ============================================================

    hbox_sep_tuned = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator_tuned = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator_tuned.set_hexpand(True)
    hbox_sep_tuned.append(hseparator_tuned)

    hbox_tuned_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_tuned_title_label = Gtk.Label(xalign=0)
    hbox_tuned_title_label.set_markup("<b>Tuned</b>")
    hbox_tuned_title_label.set_margin_start(10)
    hbox_tuned_title_label.set_margin_end(10)
    hbox_tuned_title.append(hbox_tuned_title_label)

    hbox_tuned_install = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.tuned_package_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("tuned"):
        self.tuned_package_label.set_markup("tuned is <b>installed</b>")
    else:
        self.tuned_package_label.set_text("Install tuned for dynamic system tuning")
    btn_install_tuned = Gtk.Button(label="Install tuned/tuned-ppd")
    btn_install_tuned.connect("clicked", performance.install_tuned_tools, self)
    btn_remove_tuned = Gtk.Button(label="Remove tuned/tuned-ppd")
    btn_remove_tuned.connect("clicked", performance.remove_tuned_tools, self)
    self.tuned_package_label.set_margin_start(10)
    self.tuned_package_label.set_margin_end(10)
    self.tuned_package_label.set_hexpand(True)
    hbox_tuned_install.append(self.tuned_package_label)
    btn_install_tuned.set_margin_start(10)
    btn_install_tuned.set_margin_end(10)
    hbox_tuned_install.append(btn_install_tuned)
    btn_remove_tuned.set_margin_start(10)
    btn_remove_tuned.set_margin_end(10)
    hbox_tuned_install.append(btn_remove_tuned)

    hbox_tuned_desc = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_tuned_desc_label = Gtk.Label(xalign=0)
    hbox_tuned_desc_label.set_markup(
        "<b>Tuned</b> - Dynamic system tuning for power management\n"
        "<b>Tuned-PPD</b> - Power Profiles Daemon integration for desktop environments\n"
        "If <b>TLP</b> is installed, it will be disabled when Tuned is enabled (they conflict).\n"
        "If <b>power-profiles-daemon</b> is installed, it will be removed before installing Tuned-PPD (they conflict)."
    )
    hbox_tuned_desc_label.set_margin_start(10)
    hbox_tuned_desc_label.set_margin_end(10)
    hbox_tuned_desc.append(hbox_tuned_desc_label)

    hbox_tuned_restart = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.tuned_status_label = Gtk.Label(xalign=0)
    self.tuned_status_label.set_markup("tuned service : " + performance.get_service_status("tuned"))
    self.tuned_status_label.set_margin_start(10)
    self.tuned_status_label.set_margin_end(10)
    self.tuned_status_label.set_hexpand(True)
    hbox_tuned_restart.append(self.tuned_status_label)
    self.restart_tuned = Gtk.Button(label="Restart tuned")
    self.restart_tuned.connect("clicked", performance.restart_tuned_service, self)
    self.restart_tuned.set_margin_start(10)
    self.restart_tuned.set_margin_end(10)
    hbox_tuned_restart.append(self.restart_tuned)
    self.restart_tuned_ppd = Gtk.Button(label="Restart tuned-ppd")
    self.restart_tuned_ppd.connect("clicked", performance.restart_tuned_ppd_service, self)
    self.restart_tuned_ppd.set_margin_start(10)
    self.restart_tuned_ppd.set_margin_end(10)
    hbox_tuned_restart.append(self.restart_tuned_ppd)

    hbox_tuned_enable = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.tuned_ppd_status_label = Gtk.Label(xalign=0)
    self.tuned_ppd_status_label.set_markup("tuned-ppd service : " + performance.get_service_status("tuned-ppd"))
    self.tuned_ppd_status_label.set_margin_start(10)
    self.tuned_ppd_status_label.set_margin_end(10)
    self.tuned_ppd_status_label.set_hexpand(True)
    hbox_tuned_enable.append(self.tuned_ppd_status_label)
    self.enable_tuned = Gtk.Button(label="Enable tuned + tuned-ppd")
    self.enable_tuned.connect("clicked", performance.enable_tuned_services, self)
    self.disable_tuned = Gtk.Button(label="Disable tuned + tuned-ppd")
    self.disable_tuned.connect("clicked", performance.disable_tuned_services, self)
    self.enable_tuned.set_margin_start(10)
    self.enable_tuned.set_margin_end(10)
    hbox_tuned_enable.append(self.enable_tuned)
    self.disable_tuned.set_margin_start(10)
    self.disable_tuned.set_margin_end(10)
    hbox_tuned_enable.append(self.disable_tuned)

    hbox_tuned_profile_status = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.tuned_profile_status_label = Gtk.Label(xalign=0)
    self.tuned_profile_status_label.set_markup(performance.get_tuned_profile_status_markup())
    self.tuned_profile_status_label.set_margin_start(10)
    self.tuned_profile_status_label.set_margin_end(10)
    self.tuned_profile_status_label.set_hexpand(True)
    hbox_tuned_profile_status.append(self.tuned_profile_status_label)

    hbox_tuned_profile_select = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    tuned_profile_choices = performance.get_available_tuned_profiles()
    self.tuned_profile_choices = Gtk.DropDown.new_from_strings(tuned_profile_choices)
    active_profile = performance.get_active_tuned_profile()
    if active_profile and active_profile in tuned_profile_choices:
        self.tuned_profile_choices.set_selected(tuned_profile_choices.index(active_profile))
    self.btn_apply_tuned_profile = Gtk.Button(label="Apply Profile")
    self.btn_apply_tuned_profile.connect("clicked", performance.apply_tuned_profile, self)
    hbox_tuned_profile_select_label = Gtk.Label(xalign=0)
    hbox_tuned_profile_select_label.set_text("Select profile:")
    hbox_tuned_profile_select_label.set_margin_start(10)
    hbox_tuned_profile_select_label.set_margin_end(10)
    hbox_tuned_profile_select.append(hbox_tuned_profile_select_label)
    self.tuned_profile_choices.set_margin_start(10)
    self.tuned_profile_choices.set_margin_end(10)
    hbox_tuned_profile_select.append(self.tuned_profile_choices)
    self.btn_apply_tuned_profile.set_margin_start(10)
    self.btn_apply_tuned_profile.set_margin_end(10)
    hbox_tuned_profile_select.append(self.btn_apply_tuned_profile)

    if not fn.check_package_installed("tuned"):
        self.enable_tuned.set_sensitive(False)
        self.disable_tuned.set_sensitive(False)
        self.restart_tuned.set_sensitive(False)
        self.restart_tuned_ppd.set_sensitive(False)
        self.tuned_profile_choices.set_sensitive(False)
        self.btn_apply_tuned_profile.set_sensitive(False)

    # ============================================================
    # Swap Management Block
    # ============================================================

    hbox_sep_swap = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator_zram = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator_zram.set_hexpand(True)
    hbox_sep_swap.append(hseparator_zram)

    hbox_swap_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_swap_title_label = Gtk.Label(xalign=0)
    hbox_swap_title_label.set_markup("<b>Swap Management</b>")
    hbox_swap_title_label.set_margin_start(10)
    hbox_swap_title_label.set_margin_end(10)
    hbox_swap_title.append(hbox_swap_title_label)

    hbox_swapfile = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.swapfile_label = Gtk.Label(xalign=0)
    _swapfile_size = performance.get_swapfile_size_label()
    if _swapfile_size:
        self.swapfile_label.set_markup(
            "Create or manage a swapfile at /swapfile - " + _swapfile_size + " <b>present</b>"
        )
    else:
        self.swapfile_label.set_text("Create or manage a swapfile at /swapfile")
    self.swapfile_label.set_margin_start(10)
    self.swapfile_label.set_margin_end(10)
    self.swapfile_label.set_hexpand(True)
    self.swapfile_size = Gtk.DropDown.new_from_strings(
        ["1G", "2G", "4G", "8G", "16G", "32G"]
    )
    self.swapfile_size.set_selected(1)
    btn_create_swapfile = Gtk.Button(label="Create")
    btn_create_swapfile.connect("clicked", performance.create_swapfile, self)
    btn_remove_swapfile = Gtk.Button(label="Remove")
    btn_remove_swapfile.connect("clicked", performance.remove_swapfile, self)
    hbox_swapfile.append(self.swapfile_label)
    self.swapfile_size.set_margin_start(10)
    self.swapfile_size.set_margin_end(10)
    hbox_swapfile.append(self.swapfile_size)
    btn_create_swapfile.set_margin_start(10)
    btn_create_swapfile.set_margin_end(10)
    hbox_swapfile.append(btn_create_swapfile)
    btn_remove_swapfile.set_margin_start(10)
    btn_remove_swapfile.set_margin_end(10)
    hbox_swapfile.append(btn_remove_swapfile)

    hbox_zram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.zram_status_label = Gtk.Label(xalign=0)
    self.zram_status_label.set_markup(performance.get_zram_status_markup())
    self.zram_status_label.set_margin_start(10)
    self.zram_status_label.set_margin_end(10)
    self.zram_status_label.set_hexpand(True)
    self.zram_size = Gtk.DropDown.new_from_strings(
        ["ram / 4", "ram / 2", "ram * 3 / 4", "ram", "1024", "2048", "4096"]
    )
    self.zram_size.set_selected(1)
    btn_enable_zram = Gtk.Button(label="Enable")
    btn_enable_zram.connect("clicked", performance.enable_zram, self)
    btn_disable_zram = Gtk.Button(label="Disable")
    btn_disable_zram.connect("clicked", performance.disable_zram, self)
    hbox_zram.append(self.zram_status_label)
    self.zram_size.set_margin_start(10)
    self.zram_size.set_margin_end(10)
    hbox_zram.append(self.zram_size)
    btn_enable_zram.set_margin_start(10)
    btn_enable_zram.set_margin_end(10)
    hbox_zram.append(btn_enable_zram)
    btn_disable_zram.set_margin_start(10)
    btn_disable_zram.set_margin_end(10)
    hbox_zram.append(btn_disable_zram)

    # ============================================================
    # SSD/NVMe TRIM Block
    # ============================================================

    hbox_sep_fstrim = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator_fstrim = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator_fstrim.set_hexpand(True)
    hbox_sep_fstrim.append(hseparator_fstrim)

    hbox_fstrim_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_fstrim_title_label = Gtk.Label(xalign=0)
    hbox_fstrim_title_label.set_markup("<b>SSD/NVMe TRIM</b>")
    hbox_fstrim_title_label.set_margin_start(10)
    hbox_fstrim_title_label.set_margin_end(10)
    hbox_fstrim_title.append(hbox_fstrim_title_label)

    hbox_fstrim = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.fstrim_status_label = Gtk.Label(xalign=0)
    self.fstrim_status_label.set_markup(performance.get_fstrim_status_markup())
    self.fstrim_status_label.set_margin_start(10)
    self.fstrim_status_label.set_margin_end(10)
    self.fstrim_status_label.set_hexpand(True)
    btn_enable_fstrim = Gtk.Button(label="Enable fstrim.timer")
    btn_enable_fstrim.connect("clicked", performance.enable_fstrim_timer, self)
    btn_disable_fstrim = Gtk.Button(label="Disable")
    btn_disable_fstrim.connect("clicked", performance.disable_fstrim_timer, self)
    hbox_fstrim.append(self.fstrim_status_label)
    btn_enable_fstrim.set_margin_start(10)
    btn_enable_fstrim.set_margin_end(10)
    hbox_fstrim.append(btn_enable_fstrim)
    btn_disable_fstrim.set_margin_start(10)
    btn_disable_fstrim.set_margin_end(10)
    hbox_fstrim.append(btn_disable_fstrim)

    # ============================================================
    # IRQ Balancing Block
    # ============================================================

    hbox_sep_irqbalance = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator_irqbalance = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator_irqbalance.set_hexpand(True)
    hbox_sep_irqbalance.append(hseparator_irqbalance)

    hbox_irqbalance_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_irqbalance_title_label = Gtk.Label(xalign=0)
    hbox_irqbalance_title_label.set_markup("<b>IRQ Balancing</b>")
    hbox_irqbalance_title_label.set_margin_start(10)
    hbox_irqbalance_title_label.set_margin_end(10)
    hbox_irqbalance_title.append(hbox_irqbalance_title_label)

    hbox_irqbalance_install = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.irqbalance_package_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("irqbalance"):
        self.irqbalance_package_label.set_markup(
            "irqbalance package is <b>installed</b>"
        )
    else:
        self.irqbalance_package_label.set_text("Install irqbalance")
    btn_install_irqbalance = Gtk.Button(label="Install irqbalance")
    btn_install_irqbalance.connect("clicked", performance.install_irqbalance, self)
    btn_remove_irqbalance = Gtk.Button(label="Remove irqbalance")
    btn_remove_irqbalance.connect("clicked", performance.remove_irqbalance, self)
    self.irqbalance_package_label.set_margin_start(10)
    self.irqbalance_package_label.set_margin_end(10)
    self.irqbalance_package_label.set_hexpand(True)
    hbox_irqbalance_install.append(self.irqbalance_package_label)
    btn_install_irqbalance.set_margin_start(10)
    btn_install_irqbalance.set_margin_end(10)
    hbox_irqbalance_install.append(btn_install_irqbalance)
    btn_remove_irqbalance.set_margin_start(10)
    btn_remove_irqbalance.set_margin_end(10)
    hbox_irqbalance_install.append(btn_remove_irqbalance)

    hbox_irqbalance_service = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.irqbalance_status_label = Gtk.Label(xalign=0)
    self.irqbalance_status_label.set_markup(
        performance.get_irqbalance_status_markup()
    )
    self.irqbalance_status_label.set_margin_start(10)
    self.irqbalance_status_label.set_margin_end(10)
    self.irqbalance_status_label.set_hexpand(True)
    self.enable_irqbalance = Gtk.Button(label="Enable irqbalance")
    self.enable_irqbalance.connect(
        "clicked", performance.enable_irqbalance_service, self
    )
    self.disable_irqbalance = Gtk.Button(label="Disable irqbalance")
    self.disable_irqbalance.connect(
        "clicked", performance.disable_irqbalance_service, self
    )
    hbox_irqbalance_service.append(self.irqbalance_status_label)
    self.enable_irqbalance.set_margin_start(10)
    self.enable_irqbalance.set_margin_end(10)
    hbox_irqbalance_service.append(self.enable_irqbalance)
    self.disable_irqbalance.set_margin_start(10)
    self.disable_irqbalance.set_margin_end(10)
    hbox_irqbalance_service.append(self.disable_irqbalance)

    if not fn.check_package_installed("irqbalance"):
        self.enable_irqbalance.set_sensitive(False)
        self.disable_irqbalance.set_sensitive(False)

    # ============================================================
    # Ananicy Block
    # ============================================================

    hbox_sep_ananicy = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator_ananicy = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator_ananicy.set_hexpand(True)
    hbox_sep_ananicy.append(hseparator_ananicy)

    hbox_ananicy_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_ananicy_title_label = Gtk.Label(xalign=0)
    hbox_ananicy_title_label.set_markup("<b>Ananicy</b>")
    hbox_ananicy_title_label.set_margin_start(10)
    hbox_ananicy_title_label.set_margin_end(10)
    hbox_ananicy_title.append(hbox_ananicy_title_label)

    hbox_ananicy_install = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.ananicy_package_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("ananicy-cpp") and fn.check_package_installed("cachyos-ananicy-rules-git"):
        self.ananicy_package_label.set_markup(
            "ananicy-cpp and cachyos-ananicy-rules-git are <b>installed</b>"
        )
    elif fn.check_package_installed("ananicy-cpp"):
        self.ananicy_package_label.set_markup(
            "ananicy-cpp is <b>installed</b> (cachyos-ananicy-rules-git not installed)"
        )
    else:
        self.ananicy_package_label.set_text("Install ananicy-cpp and cachyos-ananicy-rules-git")
    btn_install_ananicy = Gtk.Button(label="Install")
    btn_install_ananicy.connect("clicked", performance.install_ananicy, self)
    btn_remove_ananicy = Gtk.Button(label="Remove")
    btn_remove_ananicy.connect("clicked", performance.remove_ananicy, self)
    self.ananicy_package_label.set_margin_start(10)
    self.ananicy_package_label.set_margin_end(10)
    self.ananicy_package_label.set_hexpand(True)
    hbox_ananicy_install.append(self.ananicy_package_label)
    btn_install_ananicy.set_margin_start(10)
    btn_install_ananicy.set_margin_end(10)
    hbox_ananicy_install.append(btn_install_ananicy)
    btn_remove_ananicy.set_margin_start(10)
    btn_remove_ananicy.set_margin_end(10)
    hbox_ananicy_install.append(btn_remove_ananicy)

    hbox_ananicy_service = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.ananicy_status_label = Gtk.Label(xalign=0)
    self.ananicy_status_label.set_markup(performance.get_ananicy_status_markup())
    self.ananicy_status_label.set_margin_start(10)
    self.ananicy_status_label.set_margin_end(10)
    self.ananicy_status_label.set_hexpand(True)
    self.enable_ananicy = Gtk.Button(label="Enable ananicy-cpp")
    self.enable_ananicy.connect("clicked", performance.enable_ananicy_service, self)
    self.disable_ananicy = Gtk.Button(label="Disable ananicy-cpp")
    self.disable_ananicy.connect("clicked", performance.disable_ananicy_service, self)
    hbox_ananicy_service.append(self.ananicy_status_label)
    self.enable_ananicy.set_margin_start(10)
    self.enable_ananicy.set_margin_end(10)
    hbox_ananicy_service.append(self.enable_ananicy)
    self.disable_ananicy.set_margin_start(10)
    self.disable_ananicy.set_margin_end(10)
    hbox_ananicy_service.append(self.disable_ananicy)

    if not fn.check_package_installed("ananicy-cpp"):
        self.enable_ananicy.set_sensitive(False)
        self.disable_ananicy.set_sensitive(False)

    # ============================================================
    # GameMode Block
    # ============================================================

    hbox_sep_gamemode = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator_gamemode = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator_gamemode.set_hexpand(True)
    hbox_sep_gamemode.append(hseparator_gamemode)

    hbox_gamemode_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_gamemode_title_label = Gtk.Label(xalign=0)
    hbox_gamemode_title_label.set_markup("<b>GameMode</b>")
    hbox_gamemode_title_label.set_margin_start(10)
    hbox_gamemode_title_label.set_margin_end(10)
    hbox_gamemode_title.append(hbox_gamemode_title_label)

    hbox_gamemode_install = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.gamemode_package_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("gamemode"):
        self.gamemode_package_label.set_markup(
            "gamemode package is <b>installed</b>"
        )
    else:
        self.gamemode_package_label.set_text("Install gamemode")
    btn_install_gamemode = Gtk.Button(label="Install")
    btn_install_gamemode.connect("clicked", performance.install_gamemode, self)
    btn_remove_gamemode = Gtk.Button(label="Remove")
    btn_remove_gamemode.connect("clicked", performance.remove_gamemode, self)
    self.gamemode_package_label.set_margin_start(10)
    self.gamemode_package_label.set_margin_end(10)
    self.gamemode_package_label.set_hexpand(True)
    hbox_gamemode_install.append(self.gamemode_package_label)
    btn_install_gamemode.set_margin_start(10)
    btn_install_gamemode.set_margin_end(10)
    hbox_gamemode_install.append(btn_install_gamemode)
    btn_remove_gamemode.set_margin_start(10)
    btn_remove_gamemode.set_margin_end(10)
    hbox_gamemode_install.append(btn_remove_gamemode)

    hbox_gamemode_service = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.gamemode_status_label = Gtk.Label(xalign=0)
    self.gamemode_status_label.set_markup(performance.get_gamemode_status_markup())
    self.gamemode_status_label.set_margin_start(10)
    self.gamemode_status_label.set_margin_end(10)
    self.gamemode_status_label.set_hexpand(True)
    self.enable_gamemode = Gtk.Button(label="Enable gamemode")
    self.enable_gamemode.connect("clicked", performance.enable_gamemode_service, self)
    self.disable_gamemode = Gtk.Button(label="Disable gamemode")
    self.disable_gamemode.connect("clicked", performance.disable_gamemode_service, self)
    hbox_gamemode_service.append(self.gamemode_status_label)
    self.enable_gamemode.set_margin_start(10)
    self.enable_gamemode.set_margin_end(10)
    hbox_gamemode_service.append(self.enable_gamemode)
    self.disable_gamemode.set_margin_start(10)
    self.disable_gamemode.set_margin_end(10)
    hbox_gamemode_service.append(self.disable_gamemode)

    if not fn.check_package_installed("gamemode"):
        self.enable_gamemode.set_sensitive(False)
        self.disable_gamemode.set_sensitive(False)

    # ============================================================
    # Vbox Stack
    # ============================================================

    vboxstack_performance.append(hbox_title)
    vboxstack_performance.append(hbox_sep)
    vboxstack_performance.append(hbox_sep_tuned)
    vboxstack_performance.append(hbox_tuned_title)
    vboxstack_performance.append(hbox_tuned_install)
    vboxstack_performance.append(hbox_tuned_desc)
    vboxstack_performance.append(hbox_tuned_restart)
    vboxstack_performance.append(hbox_tuned_enable)
    vboxstack_performance.append(hbox_tuned_profile_status)
    vboxstack_performance.append(hbox_tuned_profile_select)
    vboxstack_performance.append(hbox_sep_swap)
    vboxstack_performance.append(hbox_swap_title)
    if performance.get_root_filesystem_type() != "btrfs":
        vboxstack_performance.append(hbox_swapfile)
    vboxstack_performance.append(hbox_zram)
    vboxstack_performance.append(hbox_sep_fstrim)
    vboxstack_performance.append(hbox_fstrim_title)
    vboxstack_performance.append(hbox_fstrim)
    vboxstack_performance.append(hbox_sep_irqbalance)
    vboxstack_performance.append(hbox_irqbalance_title)
    vboxstack_performance.append(hbox_irqbalance_install)
    vboxstack_performance.append(hbox_irqbalance_service)
    vboxstack_performance.append(hbox_sep_ananicy)
    vboxstack_performance.append(hbox_ananicy_title)
    vboxstack_performance.append(hbox_ananicy_install)
    vboxstack_performance.append(hbox_ananicy_service)
    vboxstack_performance.append(hbox_sep_gamemode)
    vboxstack_performance.append(hbox_gamemode_title)
    vboxstack_performance.append(hbox_gamemode_install)
    vboxstack_performance.append(hbox_gamemode_service)
