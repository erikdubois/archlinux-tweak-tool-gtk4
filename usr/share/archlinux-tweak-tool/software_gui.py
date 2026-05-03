# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools
import software


def gui(self, Gtk, vboxstack_software, fn):
    """create a gui"""
    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_title_label = Gtk.Label(xalign=0)
    hbox_title_label.set_text("Software Installers")
    hbox_title_label.set_name("title")
    hbox_title_label.set_margin_start(10)
    hbox_title_label.set_margin_end(10)
    hbox_title.append(hbox_title_label)

    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox_sep.append(hseparator)

    # Section 1: GUI Package Managers
    hbox_section1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_section1_label = Gtk.Label(xalign=0)
    hbox_section1_label.set_markup("<b>GUI Package Managers</b>")
    hbox_section1_label.set_margin_start(10)
    hbox_section1_label.set_margin_top(15)
    hbox_section1_label.set_margin_bottom(10)
    hbox_section1.append(hbox_section1_label)

    # Pamac
    hbox_pamac = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_pamac = Gtk.Label(xalign=0)
    self.lbl_software_pamac.set_markup(
        "Pamac Aur" + (" <b>installed</b>" if fn.path.exists("/usr/bin/pamac-manager") else "")
    )
    btn_pamac_launch = Gtk.Button(label="Launch/Install")
    btn_pamac_launch.connect("clicked", functools.partial(software.on_click_software_pamac, self))
    self.btn_software_pamac_remove = Gtk.Button(label="Remove")
    self.btn_software_pamac_remove.connect(
        "clicked", functools.partial(software.on_click_software_pamac_remove, self)
    )
    self.lbl_software_pamac.set_margin_start(20)
    self.lbl_software_pamac.set_margin_end(10)
    self.lbl_software_pamac.set_hexpand(True)
    hbox_pamac.append(self.lbl_software_pamac)
    btn_pamac_launch.set_margin_start(10)
    btn_pamac_launch.set_margin_end(5)
    hbox_pamac.append(btn_pamac_launch)
    self.btn_software_pamac_remove.set_margin_start(5)
    self.btn_software_pamac_remove.set_margin_end(10)
    hbox_pamac.append(self.btn_software_pamac_remove)

    # Octopi
    hbox_octopi = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_octopi = Gtk.Label(xalign=0)
    self.lbl_software_octopi.set_markup(
        "Octopi - Qt package manager"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/octopi") else "")
    )
    btn_octopi_launch = Gtk.Button(label="Launch/Install")
    btn_octopi_launch.connect("clicked", functools.partial(software.on_click_software_octopi, self))
    self.btn_software_octopi_remove = Gtk.Button(label="Remove")
    self.btn_software_octopi_remove.connect(
        "clicked", functools.partial(software.on_click_software_octopi_remove, self)
    )
    self.lbl_software_octopi.set_margin_start(20)
    self.lbl_software_octopi.set_margin_end(10)
    self.lbl_software_octopi.set_hexpand(True)
    hbox_octopi.append(self.lbl_software_octopi)
    btn_octopi_launch.set_margin_start(10)
    btn_octopi_launch.set_margin_end(5)
    hbox_octopi.append(btn_octopi_launch)
    self.btn_software_octopi_remove.set_margin_start(5)
    self.btn_software_octopi_remove.set_margin_end(10)
    hbox_octopi.append(self.btn_software_octopi_remove)

    # GNOME Software
    hbox_gnome = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_gnome = Gtk.Label(xalign=0)
    self.lbl_software_gnome.set_markup(
        "GNOME Software - GTK software center"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/gnome-software") else "")
    )
    btn_gnome_launch = Gtk.Button(label="Launch/Install")
    btn_gnome_launch.connect("clicked", functools.partial(software.on_click_software_gnome, self))
    self.btn_software_gnome_remove = Gtk.Button(label="Remove")
    self.btn_software_gnome_remove.connect(
        "clicked", functools.partial(software.on_click_software_gnome_remove, self)
    )
    self.lbl_software_gnome.set_margin_start(20)
    self.lbl_software_gnome.set_margin_end(10)
    self.lbl_software_gnome.set_hexpand(True)
    hbox_gnome.append(self.lbl_software_gnome)
    btn_gnome_launch.set_margin_start(10)
    btn_gnome_launch.set_margin_end(5)
    hbox_gnome.append(btn_gnome_launch)
    self.btn_software_gnome_remove.set_margin_start(5)
    self.btn_software_gnome_remove.set_margin_end(10)
    hbox_gnome.append(self.btn_software_gnome_remove)

    # KDE Discover
    hbox_discover = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_discover = Gtk.Label(xalign=0)
    self.lbl_software_discover.set_markup(
        "KDE Discover - KDE software center (pulls KDE deps)"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/plasma-discover") else "")
    )
    btn_discover_launch = Gtk.Button(label="Launch/Install")
    btn_discover_launch.connect(
        "clicked", functools.partial(software.on_click_software_discover, self)
    )
    self.btn_software_discover_remove = Gtk.Button(label="Remove")
    self.btn_software_discover_remove.connect(
        "clicked", functools.partial(software.on_click_software_discover_remove, self)
    )
    self.lbl_software_discover.set_margin_start(20)
    self.lbl_software_discover.set_margin_end(10)
    self.lbl_software_discover.set_hexpand(True)
    hbox_discover.append(self.lbl_software_discover)
    btn_discover_launch.set_margin_start(10)
    btn_discover_launch.set_margin_end(5)
    hbox_discover.append(btn_discover_launch)
    self.btn_software_discover_remove.set_margin_start(5)
    self.btn_software_discover_remove.set_margin_end(10)
    hbox_discover.append(self.btn_software_discover_remove)

    # Bauh
    hbox_bauh = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_bauh = Gtk.Label(xalign=0)
    self.lbl_software_bauh.set_markup(
        "Bauh - Multi-format package manager"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/bauh") else "")
    )
    btn_bauh_launch = Gtk.Button(label="Launch/Install")
    btn_bauh_launch.connect("clicked", functools.partial(software.on_click_software_bauh, self))
    self.btn_software_bauh_remove = Gtk.Button(label="Remove")
    self.btn_software_bauh_remove.connect(
        "clicked", functools.partial(software.on_click_software_bauh_remove, self)
    )
    self.lbl_software_bauh.set_margin_start(20)
    self.lbl_software_bauh.set_margin_end(10)
    self.lbl_software_bauh.set_hexpand(True)
    hbox_bauh.append(self.lbl_software_bauh)
    btn_bauh_launch.set_margin_start(10)
    btn_bauh_launch.set_margin_end(5)
    hbox_bauh.append(btn_bauh_launch)
    self.btn_software_bauh_remove.set_margin_start(5)
    self.btn_software_bauh_remove.set_margin_end(10)
    hbox_bauh.append(self.btn_software_bauh_remove)

    # Section 2: AUR Helpers
    hbox_section2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_section2_label = Gtk.Label(xalign=0)
    hbox_section2_label.set_markup("<b>AUR Helpers</b>")
    hbox_section2_label.set_margin_start(10)
    hbox_section2_label.set_margin_top(15)
    hbox_section2_label.set_margin_bottom(10)
    hbox_section2.append(hbox_section2_label)

    # Yay-git
    hbox_yay = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_yay = Gtk.Label(xalign=0)
    self.lbl_software_yay.set_markup(
        "Yay-git - AUR helper (Go-based)"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/yay") else "")
    )
    self.btn_software_yay_install = Gtk.Button(label="Install")
    self.btn_software_yay_install.connect(
        "clicked", functools.partial(software.on_click_software_yay, self)
    )
    self.btn_software_yay_remove = Gtk.Button(label="Remove")
    self.btn_software_yay_remove.connect(
        "clicked", functools.partial(software.on_click_software_yay_remove, self)
    )
    self.lbl_software_yay.set_margin_start(20)
    self.lbl_software_yay.set_margin_end(10)
    self.lbl_software_yay.set_hexpand(True)
    hbox_yay.append(self.lbl_software_yay)
    self.btn_software_yay_install.set_margin_start(10)
    self.btn_software_yay_install.set_margin_end(5)
    hbox_yay.append(self.btn_software_yay_install)
    self.btn_software_yay_remove.set_margin_start(5)
    self.btn_software_yay_remove.set_margin_end(10)
    hbox_yay.append(self.btn_software_yay_remove)

    # Paru-git
    hbox_paru = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_paru = Gtk.Label(xalign=0)
    self.lbl_software_paru.set_markup(
        "Paru-git - AUR helper (Rust-based)"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/paru") else "")
    )
    self.btn_software_paru_install = Gtk.Button(label="Install")
    self.btn_software_paru_install.connect(
        "clicked", functools.partial(software.on_click_software_paru, self)
    )
    self.btn_software_paru_remove = Gtk.Button(label="Remove")
    self.btn_software_paru_remove.connect(
        "clicked", functools.partial(software.on_click_software_paru_remove, self)
    )
    self.lbl_software_paru.set_margin_start(20)
    self.lbl_software_paru.set_margin_end(10)
    self.lbl_software_paru.set_hexpand(True)
    hbox_paru.append(self.lbl_software_paru)
    self.btn_software_paru_install.set_margin_start(10)
    self.btn_software_paru_install.set_margin_end(5)
    hbox_paru.append(self.btn_software_paru_install)
    self.btn_software_paru_remove.set_margin_start(5)
    self.btn_software_paru_remove.set_margin_end(10)
    hbox_paru.append(self.btn_software_paru_remove)

    # Trizen
    hbox_trizen = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_trizen = Gtk.Label(xalign=0)
    self.lbl_software_trizen.set_markup(
        "Trizen - AUR helper (Perl-based)"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/trizen") else "")
    )
    self.btn_software_trizen_install = Gtk.Button(label="Install")
    self.btn_software_trizen_install.connect(
        "clicked", functools.partial(software.on_click_software_trizen, self)
    )
    self.btn_software_trizen_remove = Gtk.Button(label="Remove")
    self.btn_software_trizen_remove.connect(
        "clicked", functools.partial(software.on_click_software_trizen_remove, self)
    )
    self.lbl_software_trizen.set_margin_start(20)
    self.lbl_software_trizen.set_margin_end(10)
    self.lbl_software_trizen.set_hexpand(True)
    hbox_trizen.append(self.lbl_software_trizen)
    self.btn_software_trizen_install.set_margin_start(10)
    self.btn_software_trizen_install.set_margin_end(5)
    hbox_trizen.append(self.btn_software_trizen_install)
    self.btn_software_trizen_remove.set_margin_start(5)
    self.btn_software_trizen_remove.set_margin_end(10)
    hbox_trizen.append(self.btn_software_trizen_remove)

    # Pikaur-git
    hbox_pikaur = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_pikaur = Gtk.Label(xalign=0)
    self.lbl_software_pikaur.set_markup(
        "Pikaur-git - AUR helper (Python-based)"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/pikaur") else "")
    )
    self.btn_software_pikaur_install = Gtk.Button(label="Install")
    self.btn_software_pikaur_install.connect(
        "clicked", functools.partial(software.on_click_software_pikaur, self)
    )
    self.btn_software_pikaur_remove = Gtk.Button(label="Remove")
    self.btn_software_pikaur_remove.connect(
        "clicked", functools.partial(software.on_click_software_pikaur_remove, self)
    )
    self.lbl_software_pikaur.set_margin_start(20)
    self.lbl_software_pikaur.set_margin_end(10)
    self.lbl_software_pikaur.set_hexpand(True)
    hbox_pikaur.append(self.lbl_software_pikaur)
    self.btn_software_pikaur_install.set_margin_start(10)
    self.btn_software_pikaur_install.set_margin_end(5)
    hbox_pikaur.append(self.btn_software_pikaur_install)
    self.btn_software_pikaur_remove.set_margin_start(5)
    self.btn_software_pikaur_remove.set_margin_end(10)
    hbox_pikaur.append(self.btn_software_pikaur_remove)

    # Section 3: Flatpak / Snap / AppImage
    hbox_section3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_section3_label = Gtk.Label(xalign=0)
    hbox_section3_label.set_markup("<b>Flatpak / Snap / AppImage</b>")
    hbox_section3_label.set_margin_start(10)
    hbox_section3_label.set_margin_top(15)
    hbox_section3_label.set_margin_bottom(10)
    hbox_section3.append(hbox_section3_label)

    # Flatpak
    hbox_flatpak = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_flatpak = Gtk.Label(xalign=0)
    self.lbl_software_flatpak.set_markup(
        "Flatpak - Manage Flatpak apps"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/flatpak") else "")
    )
    self.btn_software_flatpak_install = Gtk.Button(label="Launch/Install")
    self.btn_software_flatpak_install.connect(
        "clicked", functools.partial(software.on_click_software_flatpak, self)
    )
    self.btn_software_flatpak_remove = Gtk.Button(label="Remove")
    self.btn_software_flatpak_remove.connect(
        "clicked", functools.partial(software.on_click_software_flatpak_remove, self)
    )
    self.lbl_software_flatpak.set_margin_start(20)
    self.lbl_software_flatpak.set_margin_end(10)
    self.lbl_software_flatpak.set_hexpand(True)
    hbox_flatpak.append(self.lbl_software_flatpak)
    self.btn_software_flatpak_install.set_margin_start(10)
    self.btn_software_flatpak_install.set_margin_end(5)
    hbox_flatpak.append(self.btn_software_flatpak_install)
    self.btn_software_flatpak_remove.set_margin_start(5)
    self.btn_software_flatpak_remove.set_margin_end(10)
    hbox_flatpak.append(self.btn_software_flatpak_remove)

    # Snapd
    hbox_snapd = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_snapd = Gtk.Label(xalign=0)
    self.lbl_software_snapd.set_markup(
        "Snapd - Manage Snap apps"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/snap") else "")
    )
    self.btn_software_snapd_install = Gtk.Button(label="Launch/Install")
    self.btn_software_snapd_install.connect(
        "clicked", functools.partial(software.on_click_software_snapd, self)
    )
    self.btn_software_snapd_remove = Gtk.Button(label="Remove")
    self.btn_software_snapd_remove.connect(
        "clicked", functools.partial(software.on_click_software_snapd_remove, self)
    )
    self.lbl_software_snapd.set_margin_start(20)
    self.lbl_software_snapd.set_margin_end(10)
    self.lbl_software_snapd.set_hexpand(True)
    hbox_snapd.append(self.lbl_software_snapd)
    self.btn_software_snapd_install.set_margin_start(10)
    self.btn_software_snapd_install.set_margin_end(5)
    hbox_snapd.append(self.btn_software_snapd_install)
    self.btn_software_snapd_remove.set_margin_start(5)
    self.btn_software_snapd_remove.set_margin_end(10)
    hbox_snapd.append(self.btn_software_snapd_remove)

    # AppImageLauncher
    hbox_appimage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_appimagelauncher = Gtk.Label(xalign=0)
    self.lbl_software_appimagelauncher.set_markup(
        "App-manager - Manage AppImages"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/app-manager") else "")
    )
    self.btn_software_appimagelauncher_install = Gtk.Button(label="Launch/Install")
    self.btn_software_appimagelauncher_install.connect(
        "clicked", functools.partial(software.on_click_software_appimagelauncher, self)
    )
    self.btn_software_appimagelauncher_remove = Gtk.Button(label="Remove")
    self.btn_software_appimagelauncher_remove.connect(
        "clicked", functools.partial(software.on_click_software_appimagelauncher_remove, self)
    )
    self.lbl_software_appimagelauncher.set_margin_start(20)
    self.lbl_software_appimagelauncher.set_margin_end(10)
    self.lbl_software_appimagelauncher.set_hexpand(True)
    hbox_appimage.append(self.lbl_software_appimagelauncher)
    self.btn_software_appimagelauncher_install.set_margin_start(10)
    self.btn_software_appimagelauncher_install.set_margin_end(5)
    hbox_appimage.append(self.btn_software_appimagelauncher_install)
    self.btn_software_appimagelauncher_remove.set_margin_start(5)
    self.btn_software_appimagelauncher_remove.set_margin_end(10)
    hbox_appimage.append(self.btn_software_appimagelauncher_remove)

    # Section 4: TUI Package Tools
    hbox_section4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_section4_label = Gtk.Label(xalign=0)
    hbox_section4_label.set_markup("<b>TUI Package Tools</b>")
    hbox_section4_label.set_margin_start(10)
    hbox_section4_label.set_margin_top(15)
    hbox_section4_label.set_margin_bottom(10)
    hbox_section4.append(hbox_section4_label)

    # Pacseek
    hbox_pacseek = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_pacseek = Gtk.Label(xalign=0)
    self.lbl_software_pacseek.set_markup(
        "Pacseek - TUI package searcher"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/pacseek") else "")
    )
    self.btn_software_pacseek_install = Gtk.Button(label="Launch/Install")
    self.btn_software_pacseek_install.connect(
        "clicked", functools.partial(software.on_click_software_pacseek, self)
    )
    self.btn_software_pacseek_remove = Gtk.Button(label="Remove")
    self.btn_software_pacseek_remove.connect(
        "clicked", functools.partial(software.on_click_software_pacseek_remove, self)
    )
    self.lbl_software_pacseek.set_margin_start(20)
    self.lbl_software_pacseek.set_margin_end(10)
    self.lbl_software_pacseek.set_hexpand(True)
    hbox_pacseek.append(self.lbl_software_pacseek)
    self.btn_software_pacseek_install.set_margin_start(10)
    self.btn_software_pacseek_install.set_margin_end(5)
    hbox_pacseek.append(self.btn_software_pacseek_install)
    self.btn_software_pacseek_remove.set_margin_start(5)
    self.btn_software_pacseek_remove.set_margin_end(10)
    hbox_pacseek.append(self.btn_software_pacseek_remove)

    # Pacui
    hbox_pacui = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_pacui = Gtk.Label(xalign=0)
    self.lbl_software_pacui.set_markup(
        "Pacui - TUI pacman wrapper"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/pacui") else "")
    )
    self.btn_software_pacui_install = Gtk.Button(label="Launch/Install")
    self.btn_software_pacui_install.connect(
        "clicked", functools.partial(software.on_click_software_pacui_open, self)
    )
    self.btn_software_pacui_remove = Gtk.Button(label="Remove")
    self.btn_software_pacui_remove.connect(
        "clicked", functools.partial(software.on_click_software_pacui_remove, self)
    )
    self.lbl_software_pacui.set_margin_start(20)
    self.lbl_software_pacui.set_margin_end(10)
    self.lbl_software_pacui.set_hexpand(True)
    hbox_pacui.append(self.lbl_software_pacui)
    self.btn_software_pacui_install.set_margin_start(10)
    self.btn_software_pacui_install.set_margin_end(5)
    hbox_pacui.append(self.btn_software_pacui_install)
    self.btn_software_pacui_remove.set_margin_start(5)
    self.btn_software_pacui_remove.set_margin_end(10)
    hbox_pacui.append(self.btn_software_pacui_remove)

    # Section 5: Logout Managers
    hbox_section5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_section5_label = Gtk.Label(xalign=0)
    hbox_section5_label.set_markup("<b>Logout Managers</b>")
    hbox_section5_label.set_margin_start(10)
    hbox_section5_label.set_margin_top(15)
    hbox_section5_label.set_margin_bottom(10)
    hbox_section5.append(hbox_section5_label)

    # ArchLinux Logout
    hbox_archlinux_logout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_archlinux_logout = Gtk.Label(xalign=0)
    self.lbl_software_archlinux_logout.set_markup(
        "ArchLinux Logout - Session logout tool"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/archlinux-logout") else "")
    )
    self.btn_software_archlinux_logout_install = Gtk.Button(label="Launch/Install")
    self.btn_software_archlinux_logout_install.connect(
        "clicked", functools.partial(software.on_click_software_archlinux_logout, self)
    )
    self.btn_software_archlinux_logout_remove = Gtk.Button(label="Remove")
    self.btn_software_archlinux_logout_remove.connect(
        "clicked", functools.partial(software.on_click_software_archlinux_logout_remove, self)
    )
    self.lbl_software_archlinux_logout.set_margin_start(20)
    self.lbl_software_archlinux_logout.set_margin_end(10)
    self.lbl_software_archlinux_logout.set_hexpand(True)
    hbox_archlinux_logout.append(self.lbl_software_archlinux_logout)
    self.btn_software_archlinux_logout_install.set_margin_start(10)
    self.btn_software_archlinux_logout_install.set_margin_end(5)
    hbox_archlinux_logout.append(self.btn_software_archlinux_logout_install)
    self.btn_software_archlinux_logout_remove.set_margin_start(5)
    self.btn_software_archlinux_logout_remove.set_margin_end(10)
    hbox_archlinux_logout.append(self.btn_software_archlinux_logout_remove)

    # Powermenu
    hbox_powermenu = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.lbl_software_powermenu = Gtk.Label(xalign=0)
    self.lbl_software_powermenu.set_markup(
        "powermenu - Power menu for i3/sway"
        + (" <b>installed</b>" if fn.path.exists("/usr/local/bin/edu-powermenu") else "")
    )
    self.btn_software_powermenu_install = Gtk.Button(label="Launch/Install")
    self.btn_software_powermenu_install.connect(
        "clicked", functools.partial(software.on_click_software_powermenu, self)
    )
    self.btn_software_powermenu_remove = Gtk.Button(label="Remove")
    self.btn_software_powermenu_remove.connect(
        "clicked", functools.partial(software.on_click_software_powermenu_remove, self)
    )
    self.lbl_software_powermenu.set_margin_start(20)
    self.lbl_software_powermenu.set_margin_end(10)
    self.lbl_software_powermenu.set_hexpand(True)
    hbox_powermenu.append(self.lbl_software_powermenu)
    self.btn_software_powermenu_install.set_margin_start(10)
    self.btn_software_powermenu_install.set_margin_end(5)
    hbox_powermenu.append(self.btn_software_powermenu_install)
    self.btn_software_powermenu_remove.set_margin_start(5)
    self.btn_software_powermenu_remove.set_margin_end(10)
    hbox_powermenu.append(self.btn_software_powermenu_remove)

    # ======================================================================
    #                       VBOX STACK
    # ======================================================================

    vboxstack_software.append(hbox_title)
    vboxstack_software.append(hbox_sep)
    vboxstack_software.append(hbox_section1)
    vboxstack_software.append(hbox_pamac)
    vboxstack_software.append(hbox_octopi)
    vboxstack_software.append(hbox_gnome)
    vboxstack_software.append(hbox_discover)
    vboxstack_software.append(hbox_bauh)
    vboxstack_software.append(hbox_section2)
    vboxstack_software.append(hbox_yay)
    vboxstack_software.append(hbox_paru)
    vboxstack_software.append(hbox_trizen)
    vboxstack_software.append(hbox_pikaur)
    vboxstack_software.append(hbox_section3)
    vboxstack_software.append(hbox_flatpak)
    vboxstack_software.append(hbox_snapd)
    vboxstack_software.append(hbox_appimage)
    vboxstack_software.append(hbox_section4)
    vboxstack_software.append(hbox_pacseek)
    vboxstack_software.append(hbox_pacui)
    vboxstack_software.append(hbox_section5)
    vboxstack_software.append(hbox_archlinux_logout)
    vboxstack_software.append(hbox_powermenu)
