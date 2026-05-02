# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import datetime
from gi.repository import GLib, Gtk  # noqa
import functions as fn
import os

default_app = ["nano", "ttf-hack"]

# =================================================================
# =                         Desktops                             =
# =================================================================

desktops = [
    "awesome",
    "bspwm",
    "budgie-desktop",
    "cinnamon",
    "chadwm",
    "gnome",
    "i3",
    "leftwm",
    "mate",
    "ohmychadwm",
    "plasma",
    "qtile",
    "xfce",
]
pkexec = ["pkexec", "pacman", "-S", "--needed", "--noconfirm", "--ask=4"]
pkexec_reinstall = ["pkexec", "pacman", "-S", "--noconfirm", "--ask=4"]
copy = ["cp", "-Rv"]

# =================================================================
# =                         Distros                               =
# =================================================================

if fn.distr:
    awesome = [
        "alacritty",
        "edu-awesome-git",
        "awesome",
        "dmenu",
        "edu-xfce-git",
        "feh",
        "lxappearance",
        "noto-fonts",
        "picom-git",
        "polkit-gnome",
        "rofi",
        "thunar",
        "thunar-archive-plugin",
        "thunar-volman",
        "ttf-hack",
        "vicious",
        "volctl",
        "xfce4-terminal",
    ]
    bspwm = [
        "alacritty",
        "edu-bspwm-git",
        "edu-xfce-git",
        "edu-polybar-git",
        "archlinux-logout-gtk4-git",
        "edu-rofi-git",
        "edu-rofi-themes-git",
        "awesome-terminal-fonts",
        "bspwm",
        "dmenu",
        "feh",
        "lxappearance",
        "picom-git",
        "polybar",
        "polkit-gnome",
        "rofi",
        "sxhkd",
        "thunar",
        "thunar-archive-plugin",
        "thunar-volman",
        "ttf-hack",
        "volctl",
        "xfce4-terminal",
    ]
    budgie = [
        "budgie-desktop",
        "budgie-extras",
        "dconf-editor",
        "guake",
        "ttf-hack",
    ]
    cinnamon = [
        "cinnamon",
        "cinnamon-translations",
        "gnome-screenshot",
        "gnome-system-monitor",
        "gnome-terminal",
        "iso-flag-png",
        "mintlocale",
        "nemo-fileroller",
    ]
    chadwm = [
        "alacritty",
        "archlinux-logout-gtk4-git",
        "edu-chadwm-git",
        "edu-rofi-git",
        "edu-rofi-themes-git",
        "edu-xfce-git",
        "dmenu",
        "feh",
        "lxappearance",
        "picom-git",
        "polkit-gnome",
        "rofi",
        "sxhkd",
        "thunar",
        "thunar-archive-plugin",
        "thunar-volman",
        "ttf-hack",
        "ttf-jetbrains-mono-nerd",
        "volctl",
        "xfce4-notifyd",
        "xfce4-power-manager",
        "xfce4-screenshooter",
        "xfce4-settings",
        "xfce4-taskmanager",
        "xfce4-terminal",
    ]
    gnome = [
        "gnome",
        "gnome-tweaks",
        "ttf-hack",
    ]
    gnome_removal = [
        "gnome-session",
        "gnome-shell",
        "gdm",
        "gnome-settings-daemon",
        "gnome-desktop-4",
        "gnome-tweaks",
        "gnome-bluetooth-3.0",
        "decibels",
        "epiphany",
        "gdm",
        "gnome-backgrounds",
        "gnome-calculator",
        "gnome-calendar",
        "gnome-characters",
        "gnome-clocks",
        "gnome-color-manager",
        "gnome-connections",
        "gnome-console",
        "gnome-contacts",
        "gnome-control-center",
        "gnome-font-viewer",
        "gnome-logs",
        "gnome-maps",
        "gnome-music",
        "gnome-remote-desktop",
        "gnome-system-monitor",
        "gnome-text-editor",
        "gnome-tour",
        "gnome-user-docs",
        "gnome-user-share",
        "gnome-weather",
        "grilo-plugins",
        "gst-thumbnailers",
        "loupe",
        "malcontent",
        "nautilus",
        "orca",
        "papers",
        "rygel",
        "showtime",
        "snapshot",
        "sushi",
        "tecla",
        "xdg-desktop-portal-gnome",
        "yelp",
    ]
    i3 = [
        "alacritty",
        "edu-i3-git",
        "archlinux-logout-gtk4-git",
        "edu-rofi-git",
        "edu-rofi-themes-git",
        "edu-xfce-git",
        "autotiling",
        "dmenu",
        "feh",
        "i3blocks",
        "i3-wm",
        "i3status",
        "lxappearance",
        "picom-git",
        "polkit-gnome",
        "rofi",
        "thunar",
        "thunar-archive-plugin",
        "thunar-volman",
        "ttf-hack",
        "volctl",
        "xfce4-terminal",
    ]
    leftwm = [
        "alacritty",
        "archlinux-logout-gtk4-git",
        "edu-leftwm-git",
        "edu-polybar-git",
        "edu-rofi-git",
        "edu-rofi-themes-git",
        "edu-xfce-git",
        "dmenu",
        "feh",
        "leftwm-git",
        "leftwm-theme-git",
        "lxappearance",
        "picom-git",
        "polybar",
        "polkit-gnome",
        "rofi",
        "sxhkd",
        "thunar",
        "thunar-archive-plugin",
        "thunar-volman",
        "ttf-hack",
        "ttf-iosevka-nerd",
        "ttf-material-design-iconic-font",
        "ttf-meslo-nerd-font-powerlevel10k",
        "volctl",
        "xfce4-appfinder",
        "xfce4-screenshooter",
        "xfce4-taskmanager",
        "xfce4-terminal",
    ]
    mate = [
        "mate",
        "mate-extra",
        "mate-tweak",
    ]
    ohmychadwm = [
        "alacritty",
        "archlinux-logout-gtk4-git",
        "ohmychadwm-git",
        "edu-rofi-git",
        "edu-rofi-themes-git",
        "edu-xfce-git",
        "dmenu",
        "feh",
        "lxappearance",
        "picom-git",
        "polkit-gnome",
        "rofi",
        "sxhkd",
        "thunar",
        "thunar-archive-plugin",
        "thunar-volman",
        "ttf-hack",
        "ttf-jetbrains-mono-nerd",
        "volctl",
        "xfce4-notifyd",
        "xfce4-power-manager",
        "xfce4-screenshooter",
        "xfce4-settings",
        "xfce4-taskmanager",
        "xfce4-terminal",
    ]
    plasma = [
        "plasma",
        "kde-system-meta",
        "edu-plasma-keybindings-git",
        "edu-plasma-servicemenus-git",
    ]
    qtile = [
        "alacritty",
        "archlinux-logout-gtk4-git",
        "edu-qtile-git",
        "edu-rofi-git",
        "edu-rofi-themes-git",
        "edu-xfce-git",
        "awesome-terminal-fonts",
        "dmenu",
        "feh",
        "lxappearance",
        "picom-git",
        "polkit-gnome",
        "python-setuptools",
        "python-psutil",
        "qtile",
        "rofi",
        "thunar",
        "thunar-archive-plugin",
        "thunar-volman",
        "ttf-hack",
        "volctl",
        "xfce4-terminal",
    ]
    xfce = [
        "xfce4",
        "xfce4-goodies",
        "xfce4-panel-compiz",
        "catfish",
        "libxfce4ui",
        "alacritty",
        "edu-xfce-git",
        "dmenu",
        "mugshot",
        "polkit-gnome",
        "ttf-hack",
    ]


def check_desktop(desktop):
    """check if desktop is installed"""
    # /usr/share/xsessions/xfce.desktop
    if os.path.exists("/usr/share/xsessions"):
        lst = fn.listdir("/usr/share/xsessions/")
        fn.debug_print(f"[check_desktop] Files in /usr/share/xsessions/: {lst}")
        for xsession in lst:
            if desktop + ".desktop" == xsession:
                return True
    if os.path.exists("/usr/share/wayland-sessions"):
        lst = fn.listdir("/usr/share/wayland-sessions/")
        fn.debug_print(f"[check_desktop] Files in /usr/share/wayland-sessions/: {lst}")
        for wsession in lst:
            if desktop + ".desktop" == wsession:
                return True

    fn.debug_print(f"[check_desktop] Desktop '{desktop}' not found. Looking for: {desktop}.desktop")
    return False


def check_lock(self, desktop):
    """check pacman lock"""
    if fn.path.isfile("/var/lib/pacman/db.lck"):
        mess_dialog = Gtk.MessageDialog(
            transient_for=self,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Lock File Found",
        )
        mess_dialog.props.secondary_text = "pacman lock file found, do you want to remove it and continue?"

        mess_dialog.props.secondary_use_markup = True  # noqa

        result_holder = [None]
        loop = GLib.MainLoop()

        def on_lock_response(d, response_id):
            result_holder[0] = response_id
            loop.quit()
            d.destroy()

        mess_dialog.connect("response", on_lock_response)
        mess_dialog.show()
        loop.run()

        if result_holder[0] in (Gtk.ResponseType.OK, Gtk.ResponseType.YES):
            fn.unlink("/var/lib/pacman/db.lck")
            t1 = fn.threading.Thread(
                target=install_desktop,
                args=(self, fn.get_combo_text(self.d_combo)),
            )
            t1.daemon = True
            t1.start()
    else:
        t1 = fn.threading.Thread(
            target=install_desktop, args=(self, fn.get_combo_text(self.d_combo))
        )
        t1.daemon = True
        t1.start()

    return False


def check_package_and_remove(self, package):
    """remove a package if exists"""
    if fn.check_package_installed(package):
        fn.remove_package(self, package)


def install_desktop(self, desktop):
    fn.log_section(f"Installing {desktop} desktop")
    fn.show_in_app_notification(self, f"Opening terminal for {desktop} installation...")

    src = []
    twm = False
    now = datetime.datetime.now()
    fn.log_info("Backing up ~/.config to ~/.config-att/ -- This might take a while")

    if not fn.path.exists(fn.home + "/.config-att"):
        fn.makedirs(fn.home + "/.config-att")
        fn.permissions(fn.home + "/.config-att")
    if fn.path.exists(fn.home + "/.config-att"):
        fn.permissions(fn.home + "/.config-att")
    fn.copy_func(
        fn.home + "/.config/",
        fn.home + "/.config-att/config-att-" + now.strftime("%Y-%m-%d-%H-%M-%S"),
        isdir=True,
    )
    fn.permissions(
        fn.home + "/.config-att/config-att-" + now.strftime("%Y-%m-%d-%H-%M-%S")
    )

    if fn.distr == "archcraft":
        fn.clear_skel_directory()

    check_package_and_remove(self, "rofi-lbonn-wayland-git")
    check_package_and_remove(self, "rofi-lbonn-wayland-only-git")

    if desktop == "awesome":
        command = awesome + default_app
        src.append("/etc/skel/.config/awesome")
        twm = True
    elif desktop == "bspwm":
        command = bspwm + default_app
        src.append("/etc/skel/.config/bspwm")
        src.append("/etc/skel/.config/polybar")
        twm = True
    elif desktop == "budgie-desktop":
        check_package_and_remove(self, "catfish")
        command = budgie
    elif desktop == "chadwm":
        command = chadwm + default_app
        src.append("/etc/skel/.config/arco-chadwm")
        twm = True
    elif desktop == "cinnamon":
        command = cinnamon
    elif desktop == "gnome":
        command = gnome
    elif desktop == "i3":
        command = i3 + default_app
        src.append("/etc/skel/.config/i3")
        twm = True
    elif desktop == "leftwm":
        command = leftwm + default_app
        src.append("/etc/skel/.config/leftwm")
        twm = True
    elif desktop == "ohmychadwm":
        command = ohmychadwm + default_app
        src.append("/etc/skel/.config/ohmychadwm")
        twm = True
    elif desktop == "mate":
        command = mate
    elif desktop == "plasma":
        check_package_and_remove(self, "qt5ct")
        command = plasma
        src.append("/etc/skel/.config")
        src.append("/etc/skel/.local/share")
        twm = True
    elif desktop == "qtile":
        command = qtile + default_app
        src.append("/etc/skel/.config/qtile")
        twm = True
    elif desktop == "xfce":
        command = xfce + default_app

    fn.log_subsection(f"Installing {len(command)} packages")
    fn.debug_print("Packages to install: " + str(command))

    import tempfile
    log_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.log', delete=False)
    log_path = log_file.name
    log_file.close()

    package_list = "\n".join([f"  • {pkg}" for pkg in command])
    cache_clear = ""
    if self.ch1.get_active():
        cache_clear = "echo 'Clearing package cache...' && yes | pkexec pacman -Scc && echo '' && "

    install_cmd = (
        f"( "
        f"echo 'Installing {desktop} desktop' && "
        f"echo '' && "
        f"echo 'The following packages will be installed:' && "
        f"echo '{package_list}' && "
        f"echo '' && "
        f"{cache_clear}"
        f"read -p 'Press Enter to begin installation... ' && "
        f"echo '' && "
        f"pkexec pacman -S {' '.join(command)} --needed --noconfirm --ask=4 && "
        f"echo '' && "
        f"echo '=== Installation Complete ===' && "
        f"read -p 'Press Enter to close...' "
        f") 2>&1 | tee {log_path}"
    )

    def _do_install():
        fn.log_info(f"Starting package installation for {desktop}...")
        GLib.idle_add(
            self.desktopr_stat.set_text,
            f"Installing {desktop} (see terminal)...",
        )
        process = fn.subprocess.Popen(
            ["alacritty", "-e", "bash", "-c", install_cmd],
        )
        process.wait()
        GLib.idle_add(_after_install)

    def _after_install():
        fn.debug_print(f"Installation terminal closed for {desktop}")
        if check_desktop(desktop):
            fn.log_info(f"Copying {len(src)} config files from /etc/skel to {fn.home}...")
            if twm is True:
                for x in src:
                    if fn.path.isdir(x) or fn.path.isfile(x):
                        fn.debug_print(f"Copying: {x}")
                        dest = x.replace("/etc/skel", fn.home)
                        if fn.path.isdir(x):
                            dest = fn.path.split(dest)[0]
                        l2 = copy + [x, dest]
                        GLib.idle_add(
                            self.desktopr_stat.set_text,
                            f"Copying {x} to {dest}",
                        )
                        with fn.subprocess.Popen(
                            l2,
                            bufsize=1,
                            stdout=fn.subprocess.PIPE,
                            universal_newlines=True,
                        ) as p:
                            for line in p.stdout:
                                GLib.idle_add(
                                    self.desktopr_stat.set_text,
                                    line.strip(),
                                )
                        fn.permissions(dest)

            GLib.idle_add(self.desktopr_stat.set_text, "")
            GLib.idle_add(
                self.desktop_status.set_markup,
                '<span size="x-large"><b>This desktop is installed</b></span>',
            )
            fn.log_success(f"{desktop} desktop has been installed successfully")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                f"{desktop} has been installed",
            )
            fn.debug_print(
                "Installation complete — config backed up to ~/.config-att/"
            )
        else:
            fn.log_error(f"{desktop} installation failed")
            fn.debug_print("========== Installation Output ==========")
            try:
                with open(log_path, 'r') as f:
                    log_content = f.read()
                    if log_content:
                        fn.debug_print(log_content)
                    else:
                        fn.debug_print("(no output captured)")
            except Exception as e:
                fn.debug_print(f"Could not read log file: {e}")
            fn.debug_print("\n========== Package Installation Status ==========")
            failed_packages = []
            for pkg in command:
                installed = fn.check_package_installed(pkg)
                status = '✓ installed' if installed else '✗ NOT installed'
                fn.debug_print(f"  {pkg}: {status}")
                if not installed:
                    failed_packages.append(pkg)
            if failed_packages:
                fn.debug_print(f"\nFailed to install ({len(failed_packages)}): {', '.join(failed_packages)}")
            fn.debug_print("===================================================")
            GLib.idle_add(
                self.desktop_status.set_markup,
                '<span size="x-large"><b>This desktop is NOT installed</b></span>',
            )
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                f"{desktop} has not been installed",
            )
        fn.create_log(self)
        try:
            fn.unlink(log_path)
        except Exception:
            pass

    t1 = fn.threading.Thread(target=_do_install, daemon=True)
    t1.start()

# ====================================================================
# DESKTOPR CALLBACKS
# ====================================================================


def uninstall_desktop(self, desktop):
    fn.log_section(f"Removing {desktop} desktop")
    fn.show_in_app_notification(self, f"Starting removal of {desktop}...")

    # Special handling for plasma: yakuake depends on kwayland (part of plasma group)
    if desktop == "plasma":
        if fn.check_package_installed("yakuake"):
            fn.log_info("yakuake is installed and depends on kwayland (part of plasma)")
            fn.log_info("Consider removing yakuake first, or kwayland will be protected")

    essential_packages = {
        "alacritty", "feh", "dmenu", "noto-fonts", "thunar",
        "thunar-archive-plugin", "thunar-volman",
        "python-psutil", "python-setuptools"
    }

    gnome_critical = {
        "baobab", "gnome-disk-utility", "gnome-software", "simple-scan", "gnome-app-list",
        "gnome-bluetooth", "gnome-desktop", "gnome-desktop-common", "gnome-screenshot", "gnome-themes-extra",
        "gvfs", "gvfs-afc", "gvfs-dnssd", "gvfs-goa", "gvfs-gphoto2",
        "gvfs-mtp", "gvfs-nfs", "gvfs-onedrive", "gvfs-smb", "gvfs-wsdd",
        "gnome-menus", "gnome-keyring",
        "xdg-user-dirs-gtk", "polkit-gnome"
    }

    all_other_packages = set()
    for desk_name in desktops:
        if desk_name != desktop:
            desktop_list = globals().get(desk_name.replace("-", ""))
            if desktop_list:
                all_other_packages.update(desktop_list)

    # Get the install array for this desktop
    desktop_list = globals().get(desktop.replace("-", ""))
    if not desktop_list:
        fn.log_error(f"Desktop '{desktop}' not found in configuration")
        return

    # For GNOME, protect packages with external system dependencies
    critical_set = gnome_critical if desktop == "gnome" else set()

    # Special handling for XFCE: detect which panel is actually installed and adapt the list
    desktop_list_adapted = list(desktop_list)
    if desktop == "xfce":
        # Check which panel variant is actually installed
        has_panel = fn.check_package_installed("xfce4-panel")
        has_panel_compiz = fn.check_package_installed("xfce4-panel-compiz")
        fn.log_info(f"Panel detection: xfce4-panel={has_panel}, xfce4-panel-compiz={has_panel_compiz}")
        fn.debug_print(f"[uninstall_desktop] Panel detection: xfce4-panel={has_panel}, xfce4-panel-compiz={has_panel_compiz}")

        # Replace the panel variant in the list with what's actually installed
        if "xfce4-panel-compiz" in desktop_list_adapted:
            idx = desktop_list_adapted.index("xfce4-panel-compiz")
            # Remove the compiz variant from the list
            desktop_list_adapted.pop(idx)
            # Add the actual installed variant(s) back
            if has_panel:
                desktop_list_adapted.insert(idx, "xfce4-panel")
                fn.log_info("Will remove xfce4-panel (actual installation)")
                fn.debug_print("[uninstall_desktop] Will remove xfce4-panel (actual installation)")
            if has_panel_compiz:
                desktop_list_adapted.insert(idx, "xfce4-panel-compiz")
                fn.log_info("Will remove xfce4-panel-compiz (actual installation)")
                fn.debug_print("[uninstall_desktop] Will remove xfce4-panel-compiz (actual installation)")

    # Filter packages to remove: exclude essentials, packages used by other desktops, and critical packages
    # For XFCE: exclude all xfce4-* EXCEPT the panels (which we adapted above to match actual install)
    panel_to_remove = None
    if desktop == "xfce":
        # Find which panel we're removing
        panel_to_remove = next((pkg for pkg in desktop_list_adapted if pkg in ("xfce4-panel", "xfce4-panel-compiz")), None)

    packages_to_remove = []
    for pkg in desktop_list_adapted:
        is_essential = pkg in essential_packages or (pkg.startswith("xfce4-") and pkg != panel_to_remove)
        is_system_critical = pkg in critical_set
        is_used_elsewhere = pkg in all_other_packages
        if not is_essential and not is_system_critical and not is_used_elsewhere:
            packages_to_remove.append(pkg)

    if not packages_to_remove:
        fn.log_info(f"No packages to safely remove for {desktop} (all are either essential or shared)")
        fn.show_in_app_notification(self, f"No packages to safely remove for {desktop}")
        return

    fn.log_info(f"Found {len(packages_to_remove)} packages to remove (preserving shared + essential packages)")
    fn.debug_print(f"Packages to remove: {packages_to_remove}")

    import tempfile
    log_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.log', delete=False)
    log_path = log_file.name
    log_file.close()

    pacman_flag = "-Rdd" if desktop in ("plasma", "xfce") else "-Rs"
    warning_msg = ""
    confirm_prompt = ""
    if desktop in ("plasma", "xfce"):
        desktop_name = "Plasma" if desktop == "plasma" else "XFCE"
        warning_msg = (
            f"echo 'WARNING: Using force removal (-Rdd) for {desktop_name} packages' && echo '' && "
            "echo 'This will remove packages even if other system utilities depend on them' && echo '' && "
        )
        confirm_prompt = (
            "read -p 'Press Enter to confirm removal (or type anything to cancel): ' confirm && "
            "if [ ! -z \"$confirm\" ]; then echo 'Removal cancelled'; exit 0; fi && echo '' && "
        )

    cleanup_step = ""
    if desktop == "plasma":
        cleanup_step = (
            "echo '' && echo 'Removing leftover KDE packages...' && echo '' && "
            "pkexec pacman -Rdd "
            "signon-kwallet-extension kaccounts-integration "
            "kdeclarative kdesu kded kde-inotify-survey "
            "dolphin kcron khelpcenter kio-admin kio-extras kjournald ksystemlog partitionmanager "
            "--noconfirm 2>/dev/null; "
            "echo 'KDE cleanup complete' && echo '' && "
        )
    elif desktop == "xfce":
        cleanup_step = (
            "echo '' && echo 'Removing leftover XFCE packages and plugins...' && echo '' && "
            "pkexec pacman -Rdd "
            "$(pacman -Q 2>/dev/null | grep '^xfce' | awk '{print $1}') "
            "mousepad parole ristretto xfburn "
            "thunar-archive-plugin thunar-media-tags-plugin "
            "--noconfirm 2>/dev/null; "
            "echo 'XFCE cleanup complete' && echo '' && "
        )

    package_list_str = "\n".join([f"  • {pkg}" for pkg in packages_to_remove])
    remove_cmd = (
        f"( "
        f"echo 'The following packages will be removed:' && echo '' && "
        f"echo '{package_list_str}' && echo '' && "
        f"{warning_msg}"
        f"{confirm_prompt}"
        f"pkexec pacman {pacman_flag} {' '.join(packages_to_remove)} --noconfirm && "
        f"{cleanup_step}"
        f"echo '=== Removal Complete ===' && "
        f"read -p 'Press Enter to close...' "
        f") 2>&1 | tee {log_path}"
    )

    fn.debug_print(f"Remove command: {remove_cmd}")

    def _do_remove():
        fn.log_info(f"Starting package removal for {desktop}...")
        try:
            fn.debug_print(f"Launching alacritty for {desktop} removal")
            process = fn.subprocess.Popen(
                ["alacritty", "-e", "bash", "-c", remove_cmd],
            )
            fn.debug_print(f"Alacritty launched (PID: {process.pid})")
            process.wait()
            fn.debug_print("Alacritty closed")
        except Exception as e:
            fn.log_error(f"Failed to launch alacritty: {e}")
            fn.debug_print(f"Exception details: {type(e).__name__}: {e}")
        GLib.idle_add(_show_removal_dialog)

    def _show_removal_dialog():
        try:
            with open(log_path, 'r') as f:
                log_content = f.read()
                if log_content:
                    fn.debug_print(f"[Removal Log]\n{log_content}")
        except Exception as e:
            fn.debug_print(f"Could not read removal log: {e}")

        removal_text = (
            f"<span size=\"x-large\"><b>{desktop} has been removed</b></span>\n\n"
            "We do not remove code from your home directory,\nonly packages without dependencies"
        )
        GLib.idle_add(self.desktop_status.set_markup, removal_text)
        fn.log_success(f"{desktop} desktop removal complete")
        fn.show_in_app_notification(self, f"{desktop} has been removed")
        fn.debug_print(f"Removal of {desktop} complete — user home directory untouched")

        def _clear_removal_text():
            GLib.idle_add(
                self.desktop_status.set_markup,
                '<span size="x-large"><b>This desktop is NOT installed</b></span>',
            )
            try:
                fn.unlink(log_path)
            except Exception:
                pass
            return False

        GLib.timeout_add(5000, _clear_removal_text)

    t1 = fn.threading.Thread(target=_do_remove, daemon=True)
    t1.start()


def on_d_combo_changed(self, widget, pspec=None):
    from gi.repository import Gdk, GdkPixbuf
    import desktopr_gui

    try:
        pixbuf3 = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.base_dir + "/desktop_data/" + fn.get_combo_text(self.d_combo) + ".jpg",
            desktopr_gui.IMAGE_PREVIEW_LOAD,
            desktopr_gui.IMAGE_PREVIEW_LOAD,
        )
        texture = Gdk.Texture.new_for_pixbuf(pixbuf3)
        self.image_DE.set_paintable(texture)
    except Exception:
        self.image_DE.set_paintable(None)
    if check_desktop(fn.get_combo_text(self.d_combo)):
        self.desktop_status.set_markup('<span size="x-large"><b>This desktop is installed</b></span>')
    else:
        self.desktop_status.set_markup('<span size="x-large"><b>This desktop is NOT installed</b></span>')


def on_install_clicked(self, _widget):
    fn.create_log(self)
    fn.debug_print("installing " + fn.get_combo_text(self.d_combo))
    check_lock(self, fn.get_combo_text(self.d_combo))


def on_uninstall_clicked(self, _widget):
    fn.create_log(self)
    desktop = fn.get_combo_text(self.d_combo)
    fn.debug_print(f"uninstalling {desktop}")
    if not check_desktop(desktop):
        fn.show_in_app_notification(self, f"{desktop} is not installed")
        return
    uninstall_desktop(self, desktop)


def on_default_clicked(self, _widget):
    fn.create_log(self)
    if check_desktop(fn.get_combo_text(self.d_combo)) is True:
        import settings
        secs = settings.read_section()
        if "DESKTOP" in secs:
            settings.write_settings(
                "DESKTOP", "default", fn.get_combo_text(self.d_combo)
            )
        else:
            settings.new_settings(
                "DESKTOP", {"default": fn.get_combo_text(self.d_combo)}
            )
    else:
        fn.show_in_app_notification(self, "That desktop is not installed")
        fn.debug_print("Desktop is not installed")
