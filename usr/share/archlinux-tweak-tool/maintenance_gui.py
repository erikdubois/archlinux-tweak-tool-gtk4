# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================


def gui(self, Gtk, vboxstack19, fn, maintenance):
    """create a gui"""
    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox1_label = Gtk.Label(xalign=0)
    hbox1_label.set_text("Maintenance")
    hbox1_label.set_name("title")
    hbox1_label.set_margin_start(10)
    hbox1_label.set_margin_end(10)
    hbox1.append(hbox1_label)

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox0.append(hseparator)

    hbox22 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox22_label = Gtk.Label(xalign=0)
    hbox22_label.set_text("Update system")
    btn_update_system = Gtk.Button(label="Update")
    btn_update_system.connect("clicked", self.on_click_update_system)
    hbox22_label.set_margin_start(10)
    hbox22_label.set_margin_end(10)
    hbox22_label.set_hexpand(True)
    hbox22.append(hbox22_label)
    btn_update_system.set_margin_start(10)
    btn_update_system.set_margin_end(10)
    hbox22.append(btn_update_system)  # pack_end

    hbox23 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox23_label = Gtk.Label(xalign=0)
    hbox23_label.set_text("Clean cache")
    btn_clean_cache = Gtk.Button(label="Clean")
    btn_clean_cache.connect("clicked", self.on_click_clean_cache)
    hbox23_label.set_margin_start(10)
    hbox23_label.set_margin_end(10)
    hbox23_label.set_hexpand(True)
    hbox23.append(hbox23_label)
    btn_clean_cache.set_margin_start(10)
    btn_clean_cache.set_margin_end(10)
    hbox23.append(btn_clean_cache)  # pack_end

    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox5_label = Gtk.Label(xalign=0)
    hbox5_label.set_text("Re-install archlinux-keyring")
    btn_install_arch_keyring = Gtk.Button(label="Install keyring (local)")
    btn_install_arch_keyring.connect("clicked", self.on_click_install_arch_keyring)
    btn_install_arch_keyring_online = Gtk.Button(label="Install keyring (online)")
    btn_install_arch_keyring_online.connect(
        "clicked", self.on_click_install_arch_keyring_online
    )
    hbox5_label.set_margin_start(10)
    hbox5_label.set_margin_end(10)
    hbox5_label.set_hexpand(True)
    hbox5.append(hbox5_label)
    btn_install_arch_keyring.set_margin_start(10)
    btn_install_arch_keyring.set_margin_end(10)
    hbox5.append(btn_install_arch_keyring)  # pack_end
    btn_install_arch_keyring_online.set_margin_start(10)
    btn_install_arch_keyring_online.set_margin_end(10)
    hbox5.append(btn_install_arch_keyring_online)  # pack_end

    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox2_label = Gtk.Label(xalign=0)
    hbox2_label.set_text("Reset and reload pacman keys")
    btn_apply_pacman_key_fix = Gtk.Button(label="Fix keys")
    btn_apply_pacman_key_fix.connect("clicked", self.on_click_fix_pacman_keys)
    hbox2_label.set_margin_start(10)
    hbox2_label.set_margin_end(10)
    hbox2_label.set_hexpand(True)
    hbox2.append(hbox2_label)
    btn_apply_pacman_key_fix.set_margin_start(10)
    btn_apply_pacman_key_fix.set_margin_end(10)
    hbox2.append(btn_apply_pacman_key_fix)  # pack_end

    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox3_label = Gtk.Label(xalign=0)
    hbox3_label.set_text("Set the mainstream servers from Arch Linux")
    btn_apply_osbeck = Gtk.Button(label="Set mainstream")
    btn_apply_osbeck.connect("clicked", self.on_click_fix_mainstream)
    button_reset_mirrorlist = Gtk.Button(label="Reset mirrorlist")
    button_reset_mirrorlist.connect("clicked", self.on_click_reset_mirrorlist)
    hbox3_label.set_margin_start(10)
    hbox3_label.set_margin_end(10)
    hbox3_label.set_hexpand(True)
    hbox3.append(hbox3_label)
    btn_apply_osbeck.set_margin_start(10)
    btn_apply_osbeck.set_margin_end(10)
    hbox3.append(btn_apply_osbeck)  # pack_end
    button_reset_mirrorlist.set_margin_start(10)
    button_reset_mirrorlist.set_margin_end(10)
    hbox3.append(button_reset_mirrorlist)  # pack_end

    # if all installed
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4_label = Gtk.Label(xalign=0)
    hbox4_label.set_text("Get the best Arch Linux servers (takes a while)")
    self.btn_run_reflector = Gtk.Button(label="Run reflector")
    self.btn_run_reflector.connect("clicked", self.on_click_get_arch_mirrors)
    self.btn_run_rate_mirrors = Gtk.Button(label="Run rate-mirrors")
    self.btn_run_rate_mirrors.connect("clicked", self.on_click_get_arch_mirrors2)
    hbox4_label.set_margin_start(10)
    hbox4_label.set_margin_end(10)
    hbox4_label.set_hexpand(True)
    hbox4.append(hbox4_label)
    self.btn_run_rate_mirrors.set_margin_start(10)
    self.btn_run_rate_mirrors.set_margin_end(10)
    hbox4.append(self.btn_run_rate_mirrors)  # pack_end
    self.btn_run_reflector.set_margin_start(10)
    self.btn_run_reflector.set_margin_end(10)
    hbox4.append(self.btn_run_reflector)  # pack_end

    # if not installed
    hbox40 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox40_label = Gtk.Label(xalign=0)
    hbox40_label.set_text("Install apps to find the best Arch Linux servers")
    btn_install_mirrors = Gtk.Button(label="Install reflector")
    btn_install_mirrors.connect("clicked", self.on_click_install_arch_mirrors)
    btn_install_rate_mirrors = Gtk.Button(label="Install rate mirrors")
    btn_install_rate_mirrors.connect("clicked", self.on_click_install_arch_mirrors2)
    hbox40_label.set_margin_start(10)
    hbox40_label.set_margin_end(10)
    hbox40_label.set_hexpand(True)
    hbox40.append(hbox40_label)
    btn_install_rate_mirrors.set_margin_start(10)
    btn_install_rate_mirrors.set_margin_end(10)
    hbox40.append(btn_install_rate_mirrors)  # pack_end
    btn_install_mirrors.set_margin_start(10)
    btn_install_mirrors.set_margin_end(10)
    hbox40.append(btn_install_mirrors)  # pack_end

    if not fn.path.exists("/usr/bin/reflector"):
        self.btn_run_reflector.set_sensitive(False)
    if not fn.path.exists("/usr/bin/rate-mirrors"):
        self.btn_run_rate_mirrors.set_sensitive(False)

    hbox6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox6_label = Gtk.Label(xalign=0)
    hbox6_label.set_text("Get the original ArcoLinux /etc/pacman.conf")
    btn_reset_pacman = Gtk.Button(label="Reset pacman.conf")
    btn_reset_pacman.connect("clicked", self.on_click_fix_pacman_conf)
    hbox6_label.set_margin_start(10)
    hbox6_label.set_margin_end(10)
    hbox6_label.set_hexpand(True)
    hbox6.append(hbox6_label)
    btn_reset_pacman.set_margin_start(10)
    btn_reset_pacman.set_margin_end(10)
    hbox6.append(btn_reset_pacman)  # pack_end

    hbox7 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox7_label = Gtk.Label(xalign=0)
    hbox7_label.set_text("Get the best keyservers for /etc/pacman.d/gnupg/gpg.conf")
    btn_apply_pacman_gpg_conf = Gtk.Button(label="Backup and reset gpg.conf")
    btn_apply_pacman_gpg_conf.connect("clicked", self.on_click_fix_pacman_gpg_conf)
    hbox7_label.set_margin_start(10)
    hbox7_label.set_margin_end(10)
    hbox7_label.set_hexpand(True)
    hbox7.append(hbox7_label)
    btn_apply_pacman_gpg_conf.set_margin_start(10)
    btn_apply_pacman_gpg_conf.set_margin_end(10)
    hbox7.append(btn_apply_pacman_gpg_conf)  # pack_end

    hbox8 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox8_label = Gtk.Label(xalign=0)
    hbox8_label.set_text("Get the best keyservers for ~/.gnupg/gpg.conf")
    btn_apply_pacman_gpg_conf_local = Gtk.Button(label="Backup and reset gpg.conf")
    btn_apply_pacman_gpg_conf_local.connect(
        "clicked", self.on_click_fix_pacman_gpg_conf_local
    )
    hbox8_label.set_margin_start(10)
    hbox8_label.set_margin_end(10)
    hbox8_label.set_hexpand(True)
    hbox8.append(hbox8_label)
    btn_apply_pacman_gpg_conf_local.set_margin_start(10)
    btn_apply_pacman_gpg_conf_local.set_margin_end(10)
    hbox8.append(btn_apply_pacman_gpg_conf_local)  # pack_end

    hbox12 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox12_label = Gtk.Label(xalign=0)
    hbox12_label.set_text("Choose the number of parallel downloads for pacman")
    self.parallel_downloads = Gtk.DropDown.new_from_strings([])
    numbers = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
    ]

    btn_apply_parallel_downloads = Gtk.Button(label="Apply")
    btn_apply_parallel_downloads.connect(
        "clicked", self.on_click_apply_parallel_downloads
    )

    if fn.check_content("ParallelDownloads", fn.pacman):
        for number in numbers:
            self.parallel_downloads.get_model().append(number)  # string
        act_number = maintenance.pop_parallel_downloads(self)
        self.parallel_downloads.set_selected(act_number)

    else:
        btn_apply_parallel_downloads.set_sensitive(False)

    hbox12_label.set_margin_start(10)
    hbox12_label.set_margin_end(10)
    hbox12_label.set_hexpand(True)
    hbox12.append(hbox12_label)
    self.parallel_downloads.set_margin_start(10)
    self.parallel_downloads.set_margin_end(10)
    hbox12.append(self.parallel_downloads)  # pack_end
    btn_apply_parallel_downloads.set_margin_start(10)
    btn_apply_parallel_downloads.set_margin_end(10)
    hbox12.append(btn_apply_parallel_downloads)  # pack_end

    hbox13 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox13_label = Gtk.Label(xalign=0)
    hbox13_label.set_text("Choose your cursor globally - /usr/share/icons/default")
    self.cursor_themes = Gtk.DropDown.new_from_strings([])
    maintenance.pop_gtk_cursor_names(self.cursor_themes)
    btn_apply_cursor = Gtk.Button(label="Apply")
    btn_apply_cursor.connect("clicked", self.on_click_apply_global_cursor)
    hbox13_label.set_margin_start(10)
    hbox13_label.set_margin_end(10)
    hbox13_label.set_hexpand(True)
    hbox13.append(hbox13_label)
    self.cursor_themes.set_margin_start(10)
    self.cursor_themes.set_margin_end(10)
    hbox13.append(self.cursor_themes)  # pack_end
    btn_apply_cursor.set_margin_start(10)
    btn_apply_cursor.set_margin_end(10)
    hbox13.append(btn_apply_cursor)  # pack_end

    hbox9 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox9_label = Gtk.Label(xalign=0)
    hbox9_label.set_markup(
        "<b>Distro specific:  </b>" + fn.change_distro_label(fn.distr)
    )
    hbox9_label.set_margin_start(10)
    hbox9_label.set_margin_end(10)
    hbox9.append(hbox9_label)

    hbox10 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox10_label = Gtk.Label(xalign=0)
    hbox10_label.set_markup("<b>For any Arch Linux based system</b>")
    hbox10_label.set_margin_start(10)
    hbox10_label.set_margin_end(10)
    hbox10.append(hbox10_label)

    hbox14 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox14_label = Gtk.Label(xalign=0)
    hbox14_label.set_markup("Provide probe link")
    btn_probe = Gtk.Button(label="Get probe link")
    btn_probe.connect("clicked", self.on_click_probe)
    hbox14_label.set_margin_start(10)
    hbox14_label.set_margin_end(10)
    hbox14_label.set_hexpand(True)
    hbox14.append(hbox14_label)
    btn_probe.set_margin_start(10)
    btn_probe.set_margin_end(10)
    hbox14.append(btn_probe)  # pack_end

    hbox11 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox11_label = Gtk.Label(xalign=0)
    hbox11_label.set_markup(
        "We install Alacritty to show you what changes - close the terminal and ATT continues"
    )
    hbox11_label.set_margin_start(10)
    hbox11_label.set_margin_end(10)
    hbox11.append(hbox11_label)

    hbox15 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox15_label = Gtk.Label(xalign=0)
    hbox15_label.set_text("Remove all variety packages")
    btn_apply_remove_all_variety_packages = Gtk.Button(label="Apply")
    btn_apply_remove_all_variety_packages.connect(
        "clicked", self.on_click_remove_all_variety_packages
    )
    hbox15_label.set_margin_start(10)
    hbox15_label.set_margin_end(10)
    hbox15_label.set_hexpand(True)
    hbox15.append(hbox15_label)
    btn_apply_remove_all_variety_packages.set_margin_start(10)
    btn_apply_remove_all_variety_packages.set_margin_end(10)
    hbox15.append(btn_apply_remove_all_variety_packages)  # pack_end

    hbox16 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox16_label = Gtk.Label(xalign=0)
    hbox16_label.set_text("Remove all conky packages")
    btn_apply_remove_all_conky_packages = Gtk.Button(label="Apply")
    btn_apply_remove_all_conky_packages.connect(
        "clicked", self.on_click_remove_all_conky_packages
    )
    hbox16_label.set_margin_start(10)
    hbox16_label.set_margin_end(10)
    hbox16_label.set_hexpand(True)
    hbox16.append(hbox16_label)
    btn_apply_remove_all_conky_packages.set_margin_start(10)
    btn_apply_remove_all_conky_packages.set_margin_end(10)
    hbox16.append(btn_apply_remove_all_conky_packages)  # pack_end

    hbox17 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox17_label = Gtk.Label(xalign=0)
    hbox17_label.set_text("Remove all kernel(s) and keep the Linux kernel")
    btn_apply_remove_all_kernels_but_linux = Gtk.Button(label="Apply")
    btn_apply_remove_all_kernels_but_linux.connect(
        "clicked", self.on_click_remove_all_kernels_but_linux
    )
    hbox17_label.set_margin_start(10)
    hbox17_label.set_margin_end(10)
    hbox17_label.set_hexpand(True)
    hbox17.append(hbox17_label)
    btn_apply_remove_all_kernels_but_linux.set_margin_start(10)
    btn_apply_remove_all_kernels_but_linux.set_margin_end(10)
    hbox17.append(btn_apply_remove_all_kernels_but_linux)  # pack_end

    hbox18 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox18_label = Gtk.Label(xalign=0)
    hbox18_label.set_text("Remove all kernel(s) and keep the Linux Cachyos kernel")
    btn_apply_remove_all_kernels_but_linux_cachyos = Gtk.Button(label="Apply")
    btn_apply_remove_all_kernels_but_linux_cachyos.connect(
        "clicked", self.on_click_remove_all_kernels_but_linux_cachyos
    )
    hbox18_label.set_margin_start(10)
    hbox18_label.set_margin_end(10)
    hbox18_label.set_hexpand(True)
    hbox18.append(hbox18_label)
    btn_apply_remove_all_kernels_but_linux_cachyos.set_margin_start(10)
    btn_apply_remove_all_kernels_but_linux_cachyos.set_margin_end(10)
    hbox18.append(btn_apply_remove_all_kernels_but_linux_cachyos)  # pack_end

    hbox19 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox19_label = Gtk.Label(xalign=0)
    hbox19_label.set_text("Remove all kernel(s) and keep the Linux LTS kernel")
    btn_apply_remove_all_kernels_but_linux_lts = Gtk.Button(label="Apply")
    btn_apply_remove_all_kernels_but_linux_lts.connect(
        "clicked", self.on_click_remove_all_kernels_but_linux_lts
    )
    hbox19_label.set_margin_start(10)
    hbox19_label.set_margin_end(10)
    hbox19_label.set_hexpand(True)
    hbox19.append(hbox19_label)
    btn_apply_remove_all_kernels_but_linux_lts.set_margin_start(10)
    btn_apply_remove_all_kernels_but_linux_lts.set_margin_end(10)
    hbox19.append(btn_apply_remove_all_kernels_but_linux_lts)  # pack_end

    hbox20 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox20_label = Gtk.Label(xalign=0)
    hbox20_label.set_text("Remove all kernel(s) and keep the Linux Zen kernel")
    btn_apply_remove_all_kernels_but_linux_zen = Gtk.Button(label="Apply")
    btn_apply_remove_all_kernels_but_linux_zen.connect(
        "clicked", self.on_click_remove_all_kernels_but_linux_zen
    )
    hbox20_label.set_margin_start(10)
    hbox20_label.set_margin_end(10)
    hbox20_label.set_hexpand(True)
    hbox20.append(hbox20_label)
    btn_apply_remove_all_kernels_but_linux_zen.set_margin_start(10)
    btn_apply_remove_all_kernels_but_linux_zen.set_margin_end(10)
    hbox20.append(btn_apply_remove_all_kernels_but_linux_zen)  # pack_end


    hbox21 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox21_label = Gtk.Label(xalign=0)
    hbox21_label.set_text("Change debug to !debug in /etc/makepkg.conf")
    btn_apply_change_debug = Gtk.Button(label="Apply")
    btn_apply_change_debug.connect(
        "clicked", self.on_click_change_debug
    )
    hbox21_label.set_margin_start(10)
    hbox21_label.set_margin_end(10)
    hbox21_label.set_hexpand(True)
    hbox21.append(hbox21_label)
    btn_apply_change_debug.set_margin_start(10)
    btn_apply_change_debug.set_margin_end(10)
    hbox21.append(btn_apply_change_debug)  # pack_end

    # ======================================================================
    #                       VBOX STACK
    # ======================================================================

    vboxstack19.append(hbox1)
    vboxstack19.append(hbox0)
    vboxstack19.append(hbox22)
    vboxstack19.append(hbox23)
    #vboxstack19.append(hbox10)
    vboxstack19.append(hbox14)
    # vboxstack19.pack_start(hbox11, False, False, 0)
    if not (fn.distr == "manjaro" or fn.distr == "biglinux" or fn.distr == "artix"):
        vboxstack19.append(hbox5)
    vboxstack19.append(hbox2)
    if not (fn.distr == "manjaro" or fn.distr == "biglinux" or fn.distr == "artix"):
        vboxstack19.append(hbox3)
    if not (fn.distr == "manjaro" or fn.distr == "biglinux" or fn.distr == "artix"):
        vboxstack19.append(hbox4)
    if not (fn.distr == "manjaro" or fn.distr == "biglinux" or fn.distr == "artix"):
        vboxstack19.append(hbox40)
    vboxstack19.append(hbox7)
    vboxstack19.append(hbox8)
    vboxstack19.append(hbox12)
    vboxstack19.append(hbox13)

    if fn.distr == "arcolinux":
        hbox9.set_margin_start(20)
        hbox9.set_margin_end(20)
        vboxstack19.append(hbox9)
        vboxstack19.append(hbox15)
        vboxstack19.append(hbox16)
        vboxstack19.append(hbox17)
        vboxstack19.append(hbox18)
        vboxstack19.append(hbox19)
        vboxstack19.append(hbox20)
        vboxstack19.append(hbox21)
