# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================


def gui(self, Gtk, vboxstack27, performance, fn):
    """create the performance gui"""
    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox1_label = Gtk.Label(xalign=0)
    hbox1_label.set_text("Performance")
    hbox1_label.set_name("title")
    hbox1_label.set_margin_start(10)
    hbox1_label.set_margin_end(10)
    hbox1.append(hbox1_label)

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox0.append(hseparator)

    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox2_label = Gtk.Label(xalign=0)
    hbox2_label.set_markup(
        "Use <b>tuned</b> for system tuning and <b>cpupower</b> for CPU governor profiles.\n"
        "Balanced Mode is recommended for most users.\n"
        "If <b>TLP</b> is installed, it will be disabled before Tuned is enabled."
    )
    hbox2_label.set_margin_start(10)
    hbox2_label.set_margin_end(10)
    hbox2.append(hbox2_label)

    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox3_label = Gtk.Label(xalign=0)
    if (
        fn.check_package_installed("tuned")
        and fn.check_package_installed("cpupower")
    ):
        hbox3_label.set_markup("Performance packages are <b>installed</b>")
    else:
        hbox3_label.set_text("Install performance packages")
    btn_install_power = Gtk.Button(label="Install performance tools")
    btn_install_power.connect("clicked", performance.install_power_tools, self)
    btn_remove_power = Gtk.Button(label="Remove performance tools")
    btn_remove_power.connect("clicked", performance.remove_power_tools, self)
    hbox3_label.set_margin_start(10)
    hbox3_label.set_margin_end(10)
    hbox3_label.set_hexpand(True)
    hbox3.append(hbox3_label)
    btn_install_power.set_margin_start(10)
    btn_install_power.set_margin_end(10)
    hbox3.append(btn_install_power)
    btn_remove_power.set_margin_start(10)
    btn_remove_power.set_margin_end(10)
    hbox3.append(btn_remove_power)

    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4_label = Gtk.Label(xalign=0)
    hbox4_label.set_markup(
        "<b>CPU Power Profiles</b>\n"
        "Performance Mode keeps the CPU at max speed for desktops, VMs, compiling, and gaming.\n"
        "Balanced Mode uses schedutil for smart scaling when available.\n"
        "Power Saver Mode keeps frequencies lower for laptop battery life.\n"
        "Only profiles supported by your CPU driver are shown."
    )
    hbox4_label.set_margin_start(10)
    hbox4_label.set_margin_end(10)
    hbox4.append(hbox4_label)

    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    cpu_power_profile_choices = performance.get_cpu_power_profile_choices()
    self.cpu_power_choices = Gtk.DropDown.new_from_strings(cpu_power_profile_choices)
    self.cpu_power_choices.set_selected(
        performance.get_cpu_power_profile_default(cpu_power_profile_choices)
    )
    btn_apply_cpu_power = Gtk.Button(label="Apply CPU profile")
    btn_apply_cpu_power.connect("clicked", performance.apply_cpu_power_profile, self)
    self.cpu_power_choices.set_margin_start(10)
    self.cpu_power_choices.set_margin_end(10)
    hbox5.append(self.cpu_power_choices)
    btn_apply_cpu_power.set_margin_start(10)
    btn_apply_cpu_power.set_margin_end(10)
    hbox5.append(btn_apply_cpu_power)

    hbox6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.restart_cpupower = Gtk.Button(label="Start/Restart cpupower")
    self.restart_cpupower.connect("clicked", performance.restart_cpupower_service, self)
    self.enable_cpupower = Gtk.Button(label="Enable cpupower")
    self.enable_cpupower.connect("clicked", performance.enable_cpupower_service, self)
    self.disable_cpupower = Gtk.Button(label="Disable cpupower")
    self.disable_cpupower.connect("clicked", performance.disable_cpupower_service, self)
    self.restart_cpupower.set_margin_start(10)
    self.restart_cpupower.set_margin_end(10)
    hbox6.append(self.restart_cpupower)
    self.enable_cpupower.set_margin_start(10)
    self.enable_cpupower.set_margin_end(10)
    hbox6.append(self.enable_cpupower)
    self.disable_cpupower.set_margin_start(10)
    self.disable_cpupower.set_margin_end(10)
    hbox6.append(self.disable_cpupower)

    hbox7 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.restart_tuned = Gtk.Button(label="Start/Restart tuned")
    self.restart_tuned.connect("clicked", performance.restart_tuned_service, self)
    self.enable_tuned = Gtk.Button(label="Enable tuned")
    self.enable_tuned.connect("clicked", performance.enable_tuned_service, self)
    self.disable_tuned = Gtk.Button(label="Disable tuned")
    self.disable_tuned.connect("clicked", performance.disable_tuned_service, self)
    self.restart_tuned.set_margin_start(10)
    self.restart_tuned.set_margin_end(10)
    hbox7.append(self.restart_tuned)
    self.enable_tuned.set_margin_start(10)
    self.enable_tuned.set_margin_end(10)
    hbox7.append(self.enable_tuned)
    self.disable_tuned.set_margin_start(10)
    self.disable_tuned.set_margin_end(10)
    hbox7.append(self.disable_tuned)

    hbox9 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.performance_status_label = Gtk.Label(xalign=0)
    self.performance_status_label.set_markup(
        performance.get_performance_status_markup()
    )
    self.performance_status_label.set_margin_start(10)
    self.performance_status_label.set_margin_end(10)
    hbox9.append(self.performance_status_label)

    if not fn.check_package_installed("tuned"):
        self.enable_tuned.set_sensitive(False)
        self.disable_tuned.set_sensitive(False)
        self.restart_tuned.set_sensitive(False)

    if not fn.check_package_installed("cpupower"):
        self.enable_cpupower.set_sensitive(False)
        self.disable_cpupower.set_sensitive(False)
        self.restart_cpupower.set_sensitive(False)

    hbox10 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator_zram = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator_zram.set_hexpand(True)
    hbox10.append(hseparator_zram)

    hbox11 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox11_label = Gtk.Label(xalign=0)
    hbox11_label.set_markup("<b>Swap Management</b>")
    hbox11_label.set_margin_start(10)
    hbox11_label.set_margin_end(10)
    hbox11.append(hbox11_label)

    hbox12 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox12_label = Gtk.Label(xalign=0)
    hbox12_label.set_text("Create or manage a swapfile at /swapfile")
    hbox12_label.set_margin_start(10)
    hbox12_label.set_margin_end(10)
    hbox12_label.set_hexpand(True)
    self.swapfile_size = Gtk.DropDown.new_from_strings(
        ["1G", "2G", "4G", "8G", "16G", "32G"]
    )
    self.swapfile_size.set_selected(1)
    btn_create_swapfile = Gtk.Button(label="Create")
    btn_create_swapfile.connect("clicked", performance.create_swapfile, self)
    btn_remove_swapfile = Gtk.Button(label="Remove")
    btn_remove_swapfile.connect("clicked", performance.remove_swapfile, self)
    hbox12.append(hbox12_label)
    self.swapfile_size.set_margin_start(10)
    self.swapfile_size.set_margin_end(10)
    hbox12.append(self.swapfile_size)
    btn_create_swapfile.set_margin_start(10)
    btn_create_swapfile.set_margin_end(10)
    hbox12.append(btn_create_swapfile)
    btn_remove_swapfile.set_margin_start(10)
    btn_remove_swapfile.set_margin_end(10)
    hbox12.append(btn_remove_swapfile)

    hbox13 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
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
    hbox13.append(self.zram_status_label)
    self.zram_size.set_margin_start(10)
    self.zram_size.set_margin_end(10)
    hbox13.append(self.zram_size)
    btn_enable_zram.set_margin_start(10)
    btn_enable_zram.set_margin_end(10)
    hbox13.append(btn_enable_zram)
    btn_disable_zram.set_margin_start(10)
    btn_disable_zram.set_margin_end(10)
    hbox13.append(btn_disable_zram)

    vboxstack27.append(hbox1)
    vboxstack27.append(hbox0)
    vboxstack27.append(hbox2)
    vboxstack27.append(hbox3)
    vboxstack27.append(hbox4)
    vboxstack27.append(hbox5)
    vboxstack27.append(hbox6)
    vboxstack27.append(hbox7)
    vboxstack27.append(hbox9)
    vboxstack27.append(hbox10)
    vboxstack27.append(hbox11)
    vboxstack27.append(hbox12)
    vboxstack27.append(hbox13)
