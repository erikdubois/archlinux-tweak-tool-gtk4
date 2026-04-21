# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================


def gui(self, Gtk, vboxstack14, fn):
    """create a gui"""
    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox1_label = Gtk.Label(xalign=0)
    hbox1_label.set_text("Services")
    hbox1_label.set_name("title")
    hbox1_label.set_margin_start(10)
    hbox1_label.set_margin_end(10)
    hbox1.append(hbox1_label)

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox0.append(hseparator)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

    vboxstack3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack5 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
    stack.set_transition_duration(350)
    stack.set_hhomogeneous(False)
    stack.set_vhomogeneous(False)

    stack_switcher = Gtk.StackSwitcher()
    stack_switcher.set_orientation(Gtk.Orientation.HORIZONTAL)
    stack_switcher.set_stack(stack)

    # ==================================================================
    #                       CUPS TAB
    # ==================================================================

    hbox15 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox15_label = Gtk.Label(xalign=0)
    hbox15_label.set_markup(
        "Printing can be a challenge. We recommend reading the Arch wiki cups page. Check before you buy.\n\
There are also printer specific pages. Lastly the AUR might contain the driver you need."
    )
    hbox15.append(hbox15_label)

    hbox8 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox8_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("cups"):
        hbox8_label.set_markup("Cups printing is <b>installed</b>")
    else:
        hbox8_label.set_markup("Install cups printing")

    btn_install_cups = Gtk.Button(label="Install cups")
    btn_install_cups.connect("clicked", self.on_click_install_cups)
    btn_remove_cups = Gtk.Button(label="Remove cups")
    btn_remove_cups.connect("clicked", self.on_click_remove_cups)
    hbox8_label.set_margin_start(10)
    hbox8_label.set_margin_end(10)
    hbox8_label.set_hexpand(True)
    hbox8.append(hbox8_label)
    btn_install_cups.set_margin_start(10)
    btn_install_cups.set_margin_end(10)
    hbox8.append(btn_install_cups)  # pack_end
    btn_remove_cups.set_margin_start(10)
    btn_remove_cups.set_margin_end(10)
    hbox8.append(btn_remove_cups)  # pack_end

    hbox20 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox20_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("cups-pdf"):
        hbox20_label.set_markup("Cups-pdf is <b>installed</b>")
    else:
        hbox20_label.set_markup("Install cups-pdf printing")
    btn_install_cups_pdf = Gtk.Button(label="Install cups-pdf")
    btn_install_cups_pdf.connect("clicked", self.on_click_install_cups_pdf)
    btn_remove_cups_pdf = Gtk.Button(label="Remove cups-pdf")
    btn_remove_cups_pdf.connect("clicked", self.on_click_remove_cups_pdf)
    hbox20_label.set_margin_start(10)
    hbox20_label.set_margin_end(10)
    hbox20_label.set_hexpand(True)
    hbox20.append(hbox20_label)
    btn_install_cups_pdf.set_margin_start(10)
    btn_install_cups_pdf.set_margin_end(10)
    hbox20.append(btn_install_cups_pdf)  # pack_end
    btn_remove_cups_pdf.set_margin_start(10)
    btn_remove_cups_pdf.set_margin_end(10)
    hbox20.append(btn_remove_cups_pdf)  # pack_end

    hbox26 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox26_label = Gtk.Label(xalign=0)
    hbox26_label.set_markup("Install drivers")
    hbox26_label.set_margin_start(10)
    hbox26_label.set_margin_end(10)
    hbox26.append(hbox26_label)

    hbox27 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox27_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("foomatic-db"):
        hbox27_label.set_markup(
            "   Install common printer drivers (foomatic, gutenprint, ...) - <b>Installed</b>"
        )
    else:
        hbox27_label.set_markup(
            "   Install common printer drivers (foomatic, gutenprint, ...)"
        )
    btn_install_printer_drivers = Gtk.Button(label="Install drivers")
    btn_install_printer_drivers.connect(
        "clicked", self.on_click_install_printer_drivers
    )
    btn_remove_printer_drivers = Gtk.Button(label="Remove drivers")
    btn_remove_printer_drivers.connect("clicked", self.on_click_remove_printer_drivers)
    hbox27_label.set_margin_start(10)
    hbox27_label.set_margin_end(10)
    hbox27_label.set_hexpand(True)
    hbox27.append(hbox27_label)
    btn_install_printer_drivers.set_margin_start(10)
    btn_install_printer_drivers.set_margin_end(10)
    hbox27.append(btn_install_printer_drivers)  # pack_end
    btn_remove_printer_drivers.set_margin_start(10)
    btn_remove_printer_drivers.set_margin_end(10)
    hbox27.append(btn_remove_printer_drivers)  # pack_end

    hbox21 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox21_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("hplip"):
        hbox21_label.set_markup("   HP drivers have been <b>installed</b>")
    else:
        hbox21_label.set_markup("   Install HP drivers")
    btn_install_hplip = Gtk.Button(label="Install hplip")
    btn_install_hplip.connect("clicked", self.on_click_install_hplip)
    btn_remove_hplip = Gtk.Button(label="Uninstall hplip")
    btn_remove_hplip.connect("clicked", self.on_click_remove_hplip)
    hbox21_label.set_margin_start(10)
    hbox21_label.set_margin_end(10)
    hbox21_label.set_hexpand(True)
    hbox21.append(hbox21_label)
    btn_install_hplip.set_margin_start(10)
    btn_install_hplip.set_margin_end(10)
    hbox21.append(btn_install_hplip)  # pack_end
    btn_remove_hplip.set_margin_start(10)
    btn_remove_hplip.set_margin_end(10)
    hbox21.append(btn_remove_hplip)  # pack_end

    hbox22 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox22_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("system-config-printer"):
        hbox22_label.set_markup(
            "Install configuration tool for cups \nLaunch the app and add your printer  - <b>Installed</b>"
        )
    else:
        hbox22_label.set_markup(
            "Install configuration tool for cups \n(launch the app and add your printer)"
        )
    btn_install_system_config_printer = Gtk.Button(
        label="Install system-config-printer"
    )
    btn_install_system_config_printer.connect(
        "clicked", self.on_click_install_system_config_printer
    )
    btn_remove_system_config_printer = Gtk.Button(label="Remove system-config-printer")
    btn_remove_system_config_printer.connect(
        "clicked", self.on_click_remove_system_config_printer
    )
    hbox22_label.set_margin_start(10)
    hbox22_label.set_margin_end(10)
    hbox22_label.set_hexpand(True)
    hbox22.append(hbox22_label)
    btn_install_system_config_printer.set_margin_start(10)
    btn_install_system_config_printer.set_margin_end(10)
    hbox22.append(btn_install_system_config_printer)  # pack_end
    btn_remove_system_config_printer.set_margin_start(10)
    btn_remove_system_config_printer.set_margin_end(10)
    hbox22.append(btn_remove_system_config_printer)  # pack_end

    # at bottom of page
    hbox29 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    enable_cups = Gtk.Button(label="Enable cups")
    enable_cups.connect("clicked", self.on_click_enable_cups)
    disable_cups = Gtk.Button(label="Disable cups")
    disable_cups.connect("clicked", self.on_click_disable_cups)
    restart_cups = Gtk.Button(label="Start/Restart cups")
    restart_cups.connect("clicked", self.on_click_restart_cups)
    restart_cups.set_margin_start(10)
    restart_cups.set_margin_end(10)
    hbox29.append(restart_cups)  # pack_end
    enable_cups.set_margin_start(10)
    enable_cups.set_margin_end(10)
    hbox29.append(enable_cups)
    disable_cups.set_margin_start(10)
    disable_cups.set_margin_end(10)
    hbox29.append(disable_cups)

    hbox31 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox31_label = Gtk.Label(xalign=0)

    status1 = fn.check_service("cups")
    if status1 is True:
        status1 = "<b>active</b>"
    else:
        status1 = "inactive"

    status2 = fn.check_socket("cups")
    if status2 is True:
        status2 = "<b>active</b>"
    else:
        status2 = "inactive"

    hbox31_label.set_markup("Cups service : " + status1 + "   Cups socket : " + status2)
    hbox31_label.set_margin_start(10)
    hbox31_label.set_margin_end(10)
    hbox31.append(hbox31_label)

    # ==================================================================
    #                       AUDIO CONTROL
    # ==================================================================

    hbox40 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox40_label = Gtk.Label(xalign=0)
    hbox40_label.set_markup(
        "You have two major choices: \n\
- <b>Pulseaudio</b>\n\
- <b>Pipewire</b>\n\
Reboot after installing pulseaudio or pipewire\n\
With an 'inxi -A' in a terminal you can see what sound server is running\n\
There are packages that conflict with each other.\n\
Report them if that is the case"
    )
    hbox40_label.set_margin_start(10)
    hbox40_label.set_margin_end(10)
    hbox40.append(hbox40_label)

    hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox41_label = Gtk.Label(xalign=0)
    hbox41_label.set_markup("Install and switch to Pulseaudio")
    btn_install_pulseaudio = Gtk.Button(label="Install and switch to Pulseaudio")
    btn_install_pulseaudio.connect("clicked", self.on_click_switch_to_pulseaudio)
    hbox41_label.set_margin_start(10)
    hbox41_label.set_margin_end(10)
    hbox41_label.set_hexpand(True)
    hbox41.append(hbox41_label)
    btn_install_pulseaudio.set_margin_start(10)
    btn_install_pulseaudio.set_margin_end(10)
    hbox41.append(btn_install_pulseaudio)  # pack_end

    hbox42 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox42_label = Gtk.Label(xalign=0)
    hbox42_label.set_markup("Install and switch to Pipewire")
    btn_install_pipewire = Gtk.Button(label="Install and switch to Pipewire")
    btn_install_pipewire.connect("clicked", self.on_click_switch_to_pipewire)
    hbox42_label.set_margin_start(10)
    hbox42_label.set_margin_end(10)
    hbox42_label.set_hexpand(True)
    hbox42.append(hbox42_label)
    btn_install_pipewire.set_margin_start(10)
    btn_install_pipewire.set_margin_end(10)
    hbox42.append(btn_install_pipewire)  # pack_end

    hbox48 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox48_label = Gtk.Label(xalign=0)
    text1 = ""
    text2 = ""
    status1 = fn.check_if_process_is_running("pulseaudio")
    if status1 is True:
        text1 = "<b>active</b>"
    else:
        text1 = "inactive"

    status2 = fn.check_if_process_is_running("pipewire")
    if status2 is True:
        text2 = "<b>active</b>"
    else:
        text2 = "inactive"

    hbox48_label.set_markup(
        "Pulseaudio service : " + text1 + "   Pipewire service : " + text2
    )
    hbox48_label.set_margin_start(10)
    hbox48_label.set_margin_end(10)
    hbox48.append(hbox48_label)

    # ==================================================================
    #                       BLUETOOTH CONTROL
    # ==================================================================

    hbox50 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox50_label = Gtk.Label(xalign=0)
    hbox50_label.set_text(
        "You can install all the bluetooth packages here and enable the service."
    )
    hbox50_label.set_margin_start(10)
    hbox50_label.set_margin_end(10)
    hbox50.append(hbox50_label)

    hbox51 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox51_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("bluez") == True:
        hbox51_label.set_markup("Bluez packages are already <b>installed</b>")
    else:
        hbox51_label.set_markup("Install bluetooth packages")
    btn_install_bt = Gtk.Button(label="Install bluetooth")
    btn_install_bt.connect("clicked", self.on_click_install_bluetooth)
    btn_remove_bt = Gtk.Button(label="Remove bluetooth")
    btn_remove_bt.connect("clicked", self.on_click_remove_bluetooth)
    hbox51_label.set_margin_start(10)
    hbox51_label.set_margin_end(10)
    hbox51_label.set_hexpand(True)
    hbox51.append(hbox51_label)
    btn_install_bt.set_margin_start(10)
    btn_install_bt.set_margin_end(10)
    hbox51.append(btn_install_bt)  # pack_end
    btn_remove_bt.set_margin_start(10)
    btn_remove_bt.set_margin_end(10)
    hbox51.append(btn_remove_bt)  # pack_end

    hbox53 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox53_label = Gtk.Label(xalign=0)
    hbox53_label.set_text(
        "Choose one of these tools to connect to your bluetooth devices:"
    )
    hbox53_label.set_margin_start(10)
    hbox53_label.set_margin_end(10)
    hbox53.append(hbox53_label)

    hbox54 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox54_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("blueberry"):
        hbox54_label.set_markup("   Blueberry is already <b>installed</b>")
    else:
        hbox54_label.set_markup("   Install blueberry")
    btn_install_blueberry = Gtk.Button(label="Install blueberry")
    btn_install_blueberry.connect("clicked", self.on_click_install_blueberry)
    btn_remove_blueberry = Gtk.Button(label="Remove blueberry")
    btn_remove_blueberry.connect("clicked", self.on_click_remove_blueberry)
    hbox54_label.set_margin_start(10)
    hbox54_label.set_margin_end(10)
    hbox54_label.set_hexpand(True)
    hbox54.append(hbox54_label)
    btn_install_blueberry.set_margin_start(10)
    btn_install_blueberry.set_margin_end(10)
    hbox54.append(btn_install_blueberry)  # pack_end
    btn_remove_blueberry.set_margin_start(10)
    btn_remove_blueberry.set_margin_end(10)
    hbox54.append(btn_remove_blueberry)  # pack_end

    hbox55 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox55_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("blueman"):
        hbox55_label.set_markup("   Blueman is already <b>installed</b>")
    else:
        hbox55_label.set_markup("   Install blueman")
    btn_install_blueman = Gtk.Button(label="Install blueman")
    btn_install_blueman.connect("clicked", self.on_click_install_blueman)
    btn_remove_blueman = Gtk.Button(label="Remove blueman")
    btn_remove_blueman.connect("clicked", self.on_click_remove_blueman)
    hbox55_label.set_margin_start(10)
    hbox55_label.set_margin_end(10)
    hbox55_label.set_hexpand(True)
    hbox55.append(hbox55_label)
    btn_install_blueman.set_margin_start(10)
    btn_install_blueman.set_margin_end(10)
    hbox55.append(btn_install_blueman)  # pack_end
    btn_remove_blueman.set_margin_start(10)
    btn_remove_blueman.set_margin_end(10)
    hbox55.append(btn_remove_blueman)  # pack_end

    hbox56 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox56_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("bluedevil"):
        hbox56_label.set_markup("   Bluedevil is already <b>installed</b>")
    else:
        hbox56_label.set_markup("   Install bluedevil (Plasma dependencies)")
    btn_install_bluedevil = Gtk.Button(label="Install bluedevil")
    btn_install_bluedevil.connect("clicked", self.on_click_install_bluedevil)
    btn_remove_bluedevil = Gtk.Button(label="Remove bluedevil")
    btn_remove_bluedevil.connect("clicked", self.on_click_remove_bluedevil)
    hbox56_label.set_margin_start(10)
    hbox56_label.set_margin_end(10)
    hbox56_label.set_hexpand(True)
    hbox56.append(hbox56_label)
    btn_install_bluedevil.set_margin_start(10)
    btn_install_bluedevil.set_margin_end(10)
    hbox56.append(btn_install_bluedevil)  # pack_end
    btn_remove_bluedevil.set_margin_start(10)
    btn_remove_bluedevil.set_margin_end(10)
    hbox56.append(btn_remove_bluedevil)  # pack_end

    # at bottom of page

    hbox57 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.enable_bt = Gtk.Button(label="Enable bluetooth")
    self.enable_bt.connect("clicked", self.on_click_enable_bluetooth)
    self.disable_bt = Gtk.Button(label="Disable bluetooth")
    self.disable_bt.connect("clicked", self.on_click_disable_bluetooth)
    self.restart_bt = Gtk.Button(label="Start/Restart bluetooth")
    self.restart_bt.connect("clicked", self.on_click_restart_bluetooth)
    self.restart_bt.set_margin_start(10)
    self.restart_bt.set_margin_end(10)
    hbox57.append(self.restart_bt)  # pack_end
    self.enable_bt.set_margin_start(10)
    self.enable_bt.set_margin_end(10)
    hbox57.append(self.enable_bt)
    self.disable_bt.set_margin_start(10)
    self.disable_bt.set_margin_end(10)
    hbox57.append(self.disable_bt)

    hbox58 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox58_label = Gtk.Label(xalign=0)

    status1 = fn.check_service("bluetooth")
    if status1 is True:
        status1 = "<b>active</b>"
    else:
        status1 = "inactive"

    hbox58_label.set_markup("bluetooth service : " + status1)
    hbox58_label.set_margin_start(10)
    hbox58_label.set_margin_end(10)
    hbox58.append(hbox58_label)

    if not fn.check_package_installed("bluez"):
        self.enable_bt.set_sensitive(False)
        self.disable_bt.set_sensitive(False)
        self.restart_bt.set_sensitive(False)

    # ====================================================================
    #                       STACK
    # ====================================================================

    # cups
    hbox15.set_margin_start(10)
    hbox15.set_margin_end(10)
    vboxstack3.append(hbox15)
    vboxstack3.append(hbox8)
    vboxstack3.append(hbox20)
    vboxstack3.append(hbox26)
    vboxstack3.append(hbox27)
    vboxstack3.append(hbox21)
    hbox22.set_margin_start(10)
    hbox22.set_margin_end(10)
    vboxstack3.append(hbox22)
    hbox31.set_margin_start(10)
    hbox31.set_margin_end(10)
    vboxstack3.append(hbox31)  # pack_end
    hbox29.set_margin_start(10)
    hbox29.set_margin_end(10)
    vboxstack3.append(hbox29)  # pack_end

    # audio
    hbox40.set_margin_start(10)
    hbox40.set_margin_end(10)
    vboxstack4.append(hbox40)
    vboxstack4.append(hbox41)
    vboxstack4.append(hbox42)
    hbox48.set_margin_start(10)
    hbox48.set_margin_end(10)
    vboxstack4.append(hbox48)  # pack_end

    # bluetooth
    vboxstack5.append(hbox50)
    vboxstack5.append(hbox51)
    vboxstack5.append(hbox53)
    vboxstack5.append(hbox54)
    vboxstack5.append(hbox55)
    vboxstack5.append(hbox56)
    hbox58.set_margin_start(10)
    hbox58.set_margin_end(10)
    vboxstack5.append(hbox58)  # pack_end
    hbox57.set_margin_start(10)
    hbox57.set_margin_end(10)
    vboxstack5.append(hbox57)  # pack_end

    # ==================================================================
    #                       PACK TO STACK
    # ==================================================================
    if not (fn.distr == "garuda" or fn.distr == "manjaro"):
        stack.add_titled(vboxstack4, "stack4", "Audio")
    stack.add_titled(vboxstack5, "stack5", "Bluetooth")
    stack.add_titled(vboxstack3, "stack3", "Printing")

    vbox.append(stack_switcher)
    stack.set_hexpand(True)
    stack.set_vexpand(True)
    vbox.append(stack)

    vboxstack14.append(hbox1)
    vboxstack14.append(hbox0)
    vbox.set_hexpand(True)
    vbox.set_vexpand(True)
    vboxstack14.append(vbox)
