# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
from gi.repository import GLib


def on_click_software_pamac(self, _widget):
    try:
        if fn.path.exists("/usr/bin/pamac-manager"):
            fn.log_subsection("Launching pamac-manager...")
            fn.subprocess.Popen(
                "sudo -E -u " + fn.sudo_username + " pamac-manager &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "Pamac launched")
        else:
            fn.log_subsection("Installing pamac-aur...")
            process = fn.launch_pacman_install_in_terminal("pamac-aur")
            GLib.idle_add(fn.show_in_app_notification, self, "pamac-aur installation started")

            def wait_install():
                try:
                    import time
                    fn.debug_print("Waiting for pamac-aur installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/pamac-manager"):
                        fn.log_success("pamac-aur installed successfully")
                        GLib.idle_add(self.lbl_software_pamac.set_markup, "Pamac - GUI package manager <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "pamac-aur installed")
                        time.sleep(1)
                        fn.log_subsection("Launching pamac-manager...")
                        fn.subprocess.Popen(
                            "sudo -E -u " + fn.sudo_username + " pamac-manager &",
                            shell=True,
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "Pamac launched")
                    else:
                        fn.log_warn("pamac-aur binary NOT found, installation may have failed")
                        fn.check_missing_repo_error(self, "", "pamac-aur")
                except Exception as e:
                    fn.log_error(f"Error during installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        fn.log_error(f"Error with pamac: {error}")


def on_click_software_octopi(self, _widget):
    try:
        if fn.path.exists("/usr/bin/octopi"):
            fn.log_subsection("Launching octopi...")
            fn.subprocess.Popen(
                "sudo -E -u " + fn.sudo_username + " octopi &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "Octopi launched")
        else:
            fn.log_subsection("Installing octopi...")
            process = fn.launch_pacman_install_in_terminal("octopi")
            GLib.idle_add(fn.show_in_app_notification, self, "octopi installation started")

            def wait_install():
                try:
                    import time
                    fn.debug_print("Waiting for octopi installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/octopi"):
                        fn.log_success("octopi installed successfully")
                        GLib.idle_add(self.lbl_software_octopi.set_markup, "Octopi - GUI package manager <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "octopi installed")
                        time.sleep(1)
                        fn.log_subsection("Launching octopi...")
                        fn.subprocess.Popen(
                            "sudo -E -u " + fn.sudo_username + " octopi &",
                            shell=True,
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "Octopi launched")
                    else:
                        fn.log_warn("octopi binary NOT found, installation may have failed")
                        fn.check_missing_repo_error(self, "", "octopi")
                except Exception as e:
                    fn.log_error(f"Error during installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        fn.log_error(f"Error with octopi: {error}")


def on_click_software_gnome(self, _widget):
    try:
        if fn.path.exists("/usr/bin/gnome-software"):
            fn.log_subsection("Launching gnome-software...")
            import pwd
            uid = pwd.getpwnam(fn.sudo_username).pw_uid
            fn.subprocess.Popen(
                "sudo -E -u " + fn.sudo_username +
                " HOME=/home/" + fn.sudo_username +
                " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
                " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus" +
                " gnome-software &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "GNOME Software launched")
        else:
            fn.log_subsection("Installing gnome-software...")
            process = fn.launch_pacman_install_in_terminal("gnome-software")
            GLib.idle_add(fn.show_in_app_notification, self, "gnome-software installation started")

            def wait_install():
                try:
                    import time
                    import pwd
                    fn.debug_print("Waiting for gnome-software installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/gnome-software"):
                        fn.log_success("gnome-software installed successfully")
                        GLib.idle_add(self.lbl_software_gnome.set_markup, "GNOME Software - GUI package manager <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "gnome-software installed")
                        time.sleep(1)
                        fn.log_subsection("Launching gnome-software...")
                        uid = pwd.getpwnam(fn.sudo_username).pw_uid
                        fn.subprocess.Popen(
                            "sudo -E -u " + fn.sudo_username +
                            " HOME=/home/" + fn.sudo_username +
                            " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
                            " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus" +
                            " gnome-software &",
                            shell=True,
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "gnome-software launched")
                    else:
                        fn.log_warn("gnome-software binary NOT found, installation may have failed")
                        fn.check_missing_repo_error(self, "", "gnome-software")
                except Exception as e:
                    fn.log_error(f"Error during installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        fn.log_error(f"Error with gnome-software: {error}")


def on_click_software_discover(self, _widget):
    try:
        if not fn.path.exists("/usr/bin/plasma-discover"):
            fn.log_subsection("Installing discover...")
            process = fn.launch_pacman_install_in_terminal("discover packagekit-qt6")
            GLib.idle_add(fn.show_in_app_notification, self, "discover installation started")

            def wait_install():
                try:
                    import time
                    import pwd
                    fn.debug_print("Waiting for discover installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/plasma-discover"):
                        fn.log_success("discover installed successfully")
                        GLib.idle_add(self.lbl_software_discover.set_markup, "KDE Discover - KDE software center (pulls KDE deps) <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "plasma-discover installed")
                        fn.log_subsection("Launching plasma-discover...")
                        uid = pwd.getpwnam(fn.sudo_username).pw_uid
                        fn.subprocess.Popen(
                            "DISPLAY=:0 sudo -E -u " + fn.sudo_username +
                            " HOME=/home/" + fn.sudo_username +
                            " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
                            " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus" +
                            " plasma-discover",
                            shell=True,
                            stdout=fn.subprocess.DEVNULL,
                            stderr=fn.subprocess.DEVNULL,
                        )
                    else:
                        fn.log_warn("discover binary NOT found, installation may have failed")
                except Exception as e:
                    fn.log_error(f"Error during installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
        else:
            fn.log_subsection("Launching plasma-discover...")
            import pwd
            uid = pwd.getpwnam(fn.sudo_username).pw_uid
            fn.subprocess.Popen(
                "DISPLAY=:0 sudo -E -u " + fn.sudo_username +
                " HOME=/home/" + fn.sudo_username +
                " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
                " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus" +
                " plasma-discover",
                shell=True,
                stdout=fn.subprocess.DEVNULL,
                stderr=fn.subprocess.DEVNULL,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "KDE Discover launched")
    except Exception as error:
        fn.log_error(f"Error with discover: {error}")


def on_click_software_bauh(self, _widget):
    try:
        if fn.path.exists("/usr/bin/bauh"):
            fn.log_subsection("Launching bauh...")
            fn.subprocess.Popen(
                "sudo -E -u " + fn.sudo_username + " bauh &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "Bauh launched")
        else:
            fn.log_subsection("Installing bauh...")
            process = fn.launch_pacman_install_in_terminal("bauh")
            GLib.idle_add(fn.show_in_app_notification, self, "bauh installation started")
            fn.wait_install_and_update(process, "/usr/bin/bauh", self.lbl_software_bauh, "Bauh - Multi-format package manager <b>installed</b>", self, "bauh installation complete", "bauh")
    except Exception as error:
        fn.log_error(f"Error with bauh: {error}")


def on_click_software_yay(self, _widget):
    try:
        if fn.path.exists("/usr/bin/yay"):
            fn.log_subsection("yay-git already installed")
            GLib.idle_add(fn.show_in_app_notification, self, "yay-git already installed")
            return
        fn.log_subsection("Installing yay-git...")
        process = fn.launch_pacman_install_in_terminal("yay-git")
        GLib.idle_add(fn.show_in_app_notification, self, "yay-git installation started")
        fn.wait_install_and_update(process, "/usr/bin/yay", self.lbl_software_yay, "Yay-git - AUR helper (Go-based) <b>installed</b>", self, "yay-git installed", "yay-git")
    except Exception as error:
        fn.log_error(f"Error with yay-git: {error}")


def on_click_software_paru(self, _widget):
    try:
        if fn.path.exists("/usr/bin/paru"):
            fn.log_subsection("paru-git already installed")
            GLib.idle_add(fn.show_in_app_notification, self, "paru-git already installed")
            return
        fn.log_subsection("Installing paru-git...")
        process = fn.launch_pacman_install_in_terminal("paru-git")
        GLib.idle_add(fn.show_in_app_notification, self, "paru-git installation started")
        fn.wait_install_and_update(process, "/usr/bin/paru", self.lbl_software_paru, "Paru-git - AUR helper (Rust-based) <b>installed</b>", self, "paru-git installed", "paru-git")
    except Exception as error:
        fn.log_error(f"Error with paru-git: {error}")


def on_click_software_trizen(self, _widget):
    try:
        if fn.path.exists("/usr/bin/trizen"):
            fn.log_subsection("trizen already installed")
            GLib.idle_add(fn.show_in_app_notification, self, "trizen already installed")
            return
        fn.log_subsection("Installing trizen...")
        process = fn.launch_pacman_install_in_terminal("trizen")
        GLib.idle_add(fn.show_in_app_notification, self, "trizen installation started")
        fn.wait_install_and_update(process, "/usr/bin/trizen", self.lbl_software_trizen, "Trizen - AUR helper (Perl-based) <b>installed</b>", self, "trizen installed", "trizen")
    except Exception as error:
        fn.log_error(f"Error with trizen: {error}")


def on_click_software_pikaur(self, _widget):
    try:
        if fn.path.exists("/usr/bin/pikaur"):
            fn.log_subsection("pikaur-git already installed")
            GLib.idle_add(fn.show_in_app_notification, self, "pikaur-git already installed")
            return
        fn.log_subsection("Installing pikaur-git...")
        process = fn.launch_pacman_install_in_terminal("pikaur-git")
        GLib.idle_add(fn.show_in_app_notification, self, "pikaur-git installation started")
        fn.wait_install_and_update(process, "/usr/bin/pikaur", self.lbl_software_pikaur, "Pikaur-git - AUR helper (Python-based) <b>installed</b>", self, "pikaur-git installed", "pikaur-git")
    except Exception as error:
        fn.log_error(f"Error with pikaur-git: {error}")


def on_click_software_yay_remove(self, _widget):
    try:
        fn.log_subsection("Removing yay-git...")
        process = fn.launch_pacman_remove_in_terminal("yay-git")
        GLib.idle_add(fn.show_in_app_notification, self, "yay-git removal started")
        fn.wait_remove_and_update(process, "/usr/bin/yay", self.lbl_software_yay, "Yay-git - AUR helper (Go-based)", self, "yay-git removal complete")
    except Exception as error:
        fn.log_error(f"Error with yay-git removal: {error}")


def on_click_software_paru_remove(self, _widget):
    try:
        fn.log_subsection("Removing paru-git...")
        process = fn.launch_pacman_remove_in_terminal("paru-git")
        GLib.idle_add(fn.show_in_app_notification, self, "paru-git removal started")
        fn.wait_remove_and_update(process, "/usr/bin/paru", self.lbl_software_paru, "Paru-git - AUR helper (Rust-based)", self, "paru-git removal complete")
    except Exception as error:
        fn.log_error(f"Error with paru-git removal: {error}")


def on_click_software_trizen_remove(self, widget):
    try:
        fn.log_subsection("Removing trizen...")
        process = fn.launch_pacman_remove_in_terminal("trizen")
        GLib.idle_add(fn.show_in_app_notification, self, "trizen removal started")
        fn.wait_remove_and_update(process, "/usr/bin/trizen", self.lbl_software_trizen, "Trizen - AUR helper (Perl-based)", self, "trizen removal complete")
    except Exception as error:
        fn.log_error(f"Error with trizen removal: {error}")


def on_click_software_pikaur_remove(self, widget):
    try:
        fn.log_subsection("Removing pikaur-git...")
        process = fn.launch_pacman_remove_in_terminal("pikaur-git")
        GLib.idle_add(fn.show_in_app_notification, self, "pikaur-git removal started")
        fn.wait_remove_and_update(process, "/usr/bin/pikaur", self.lbl_software_pikaur, "Pikaur-git - AUR helper (Python-based)", self, "pikaur-git removal complete")
    except Exception as error:
        fn.log_error(f"Error with pikaur-git removal: {error}")


def on_click_software_pacui_open(self, widget):
    try:
        if not fn.path.exists("/usr/bin/pacui"):
            fn.log_subsection("Installing pacui...")
            script = "pacman -S --noconfirm pacui; echo ''; echo '=== Installation complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
            process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
            GLib.idle_add(fn.show_in_app_notification, self, "pacui installation started")

            def wait_install():
                try:
                    import time
                    fn.debug_print("Waiting for pacui installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/pacui"):
                        fn.log_success("pacui installed successfully")
                        GLib.idle_add(self.lbl_software_pacui.set_markup, "Pacui - TUI pacman wrapper <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "pacui installed")
                        time.sleep(1)
                        fn.log_subsection("Launching pacui...")
                        fn.subprocess.Popen(
                            ["alacritty", "-e", "sudo", "-u", fn.sudo_username, "pacui"],
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "pacui launched")
                    else:
                        fn.log_warn("pacui binary NOT found, installation may have failed")
                except Exception as e:
                    fn.log_error(f"Error during installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
        else:
            fn.log_subsection("Launching pacui...")
            fn.subprocess.Popen(
                ["alacritty", "-e", "sudo", "-u", fn.sudo_username, "pacui"],
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "pacui launched")
    except Exception as error:
        fn.log_error(f"Error with pacui: {error}")


def on_click_software_pacui_remove(self, widget):
    try:
        fn.log_subsection("Removing pacui...")
        process = fn.launch_pacman_remove_in_terminal("pacui")
        GLib.idle_add(fn.show_in_app_notification, self, "pacui removal started")
        fn.wait_remove_and_update(process, "/usr/bin/pacui", self.lbl_software_pacui, "Pacui - TUI pacman wrapper", self, "pacui removal complete")
    except Exception as error:
        fn.log_error(f"Error with pacui removal: {error}")


def on_click_software_flatpak(self, widget):
    try:
        if not fn.path.exists("/usr/bin/flatpak"):
            fn.log_subsection("Installing flatpak...")
            script = "pacman -S --noconfirm flatpak; echo ''; echo '=== Installation complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
            process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
            GLib.idle_add(fn.show_in_app_notification, self, "flatpak installation started")

            def wait_install():
                try:
                    import time
                    fn.debug_print("Waiting for flatpak installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/flatpak"):
                        fn.log_success("flatpak installed successfully")
                        GLib.idle_add(self.lbl_software_flatpak.set_markup, "Flatpak - Manage Flatpak apps <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "flatpak installed")
                        time.sleep(1)
                        fn.debug_print("Launching flatpak")
                        script = (
                            "echo '=== Installed Flatpak apps ===' && "
                            "sudo -u " + fn.sudo_username + " flatpak list && "
                            "echo '' && "
                            "echo 'To install an app: flatpak install flathub <app-id>'"
                        )
                        fn.subprocess.Popen(
                            ["alacritty", "--hold", "-e", "bash", "-c", script],
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "flatpak launched")
                    else:
                        fn.log_warn("flatpak binary NOT found, installation may have failed")
                except Exception as e:
                    fn.log_error(f"Error during flatpak installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
        else:
            fn.log_subsection("Launching flatpak...")
            script = (
                "echo '=== Installed Flatpak apps ===' && "
                "sudo -u " + fn.sudo_username + " flatpak list && "
                "echo '' && "
                "echo 'To install an app: flatpak install flathub <app-id>'"
            )
            fn.subprocess.Popen(
                ["alacritty", "--hold", "-e", "bash", "-c", script],
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "flatpak launched")
    except Exception as error:
        fn.log_error(f"Error with flatpak: {error}")


def on_click_software_flatpak_remove(self, widget):
    try:
        fn.log_subsection("Removing flatpak...")
        process = fn.launch_pacman_remove_in_terminal("flatpak")
        GLib.idle_add(fn.show_in_app_notification, self, "flatpak removal started")
        fn.wait_remove_and_update(process, "/usr/bin/flatpak", self.lbl_software_flatpak, "Flatpak - Manage Flatpak apps", self, "flatpak removal complete")
    except Exception as error:
        fn.log_error(f"Error with flatpak removal: {error}")


def on_click_software_snapd(self, widget):
    try:
        if not fn.path.exists("/usr/bin/snap"):
            aur_helper = fn.get_aur_helper()
            if aur_helper is None:
                GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found - install yay, paru, trizen or pikaur first")
                return
            fn.log_subsection("Installing snapd...")
            process = fn.launch_aur_install_in_terminal(aur_helper, "snapd")
            GLib.idle_add(fn.show_in_app_notification, self, "snapd installation started")

            def wait_install():
                try:
                    import time
                    fn.debug_print("Waiting for snapd installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/snap"):
                        fn.log_success("snapd installed successfully")
                        GLib.idle_add(self.lbl_software_snapd.set_markup, "Snapd - Manage Snap apps <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "snapd installed")
                    else:
                        fn.log_warn("snapd binary NOT found, installation may have failed")
                except Exception as e:
                    fn.log_error(f"Error during snapd installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
        else:
            fn.log_subsection("Launching snapd...")
            script = (
                "echo '=== Installed Snap apps ===' && "
                "sudo -u " + fn.sudo_username + " snap list && "
                "echo '' && "
                "echo 'To install an app: snap install <app-name>'"
            )
            fn.subprocess.Popen(
                ["alacritty", "--hold", "-e", "bash", "-c", script],
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "snapd launched")
    except Exception as error:
        fn.log_error(f"Error with snapd: {error}")


def on_click_software_snapd_remove(self, widget):
    try:
        fn.log_subsection("Removing snapd...")
        process = fn.launch_pacman_remove_in_terminal("snapd")
        GLib.idle_add(fn.show_in_app_notification, self, "snapd removal started")
        fn.wait_remove_and_update(process, "/usr/bin/snap", self.lbl_software_snapd, "Snapd - Manage Snap apps", self, "snapd removal complete")
    except Exception as error:
        fn.log_error(f"Error with snapd removal: {error}")


def on_click_software_appimagelauncher(self, widget):
    try:
        if not fn.path.exists("/usr/bin/app-manager"):
            aur_helper = fn.get_aur_helper()
            if aur_helper is None:
                GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found - install yay, paru, trizen or pikaur first")
                return
            fn.log_subsection("Installing appmanager...")
            process = fn.launch_aur_install_in_terminal(aur_helper, "appmanager")
            GLib.idle_add(fn.show_in_app_notification, self, "appmanager installation started")

            def wait_install():
                try:
                    import time
                    import pwd
                    fn.debug_print("Waiting for appmanager installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/app-manager"):
                        fn.log_success("appmanager installed successfully")
                        GLib.idle_add(self.lbl_software_appimagelauncher.set_markup, "App-manager - Manage AppImages <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "appmanager installed")
                        time.sleep(1)
                        fn.debug_print("Launching app-manager")
                        uid = pwd.getpwnam(fn.sudo_username).pw_uid
                        fn.subprocess.Popen(
                            "sudo -E -u " + fn.sudo_username +
                            " HOME=/home/" + fn.sudo_username +
                            " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
                            " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus" +
                            " app-manager &",
                            shell=True,
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "app-manager launched")
                    else:
                        fn.log_warn("appmanager binary NOT found, installation may have failed")
                except Exception as e:
                    fn.log_error(f"Error during installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
            return
        fn.log_subsection("Launching app-manager...")
        import pwd
        uid = pwd.getpwnam(fn.sudo_username).pw_uid
        fn.subprocess.call(
            "sudo -E -u " + fn.sudo_username +
            " HOME=/home/" + fn.sudo_username +
            " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
            " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus" +
            " app-manager &",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        GLib.idle_add(fn.show_in_app_notification, self, "App-manager launched")
    except Exception as error:
        fn.log_error(f"Error with app-manager: {error}")


def on_click_software_appimagelauncher_remove(self, widget):
    try:
        fn.log_subsection("Removing appmanager...")
        process = fn.launch_pacman_remove_in_terminal("appmanager")
        GLib.idle_add(fn.show_in_app_notification, self, "appmanager removal started")
        fn.wait_remove_and_update(process, "/usr/bin/app-manager", self.lbl_software_appimagelauncher, "App-manager - Manage AppImages", self, "appmanager removal complete")
    except Exception as error:
        fn.log_error(f"Error with appmanager removal: {error}")


def on_click_software_pacseek(self, widget):
    try:
        if not fn.path.exists("/usr/bin/pacseek"):
            fn.log_subsection("Installing pacseek...")
            script = "pacman -S --noconfirm pacseek; echo ''; echo '=== Installation complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
            process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
            GLib.idle_add(fn.show_in_app_notification, self, "pacseek installation started")

            def wait_install():
                try:
                    import time
                    fn.debug_print("Waiting for pacseek installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/pacseek"):
                        fn.log_success("pacseek installed successfully")
                        GLib.idle_add(self.lbl_software_pacseek.set_markup, "Pacseek - TUI package searcher <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "pacseek installed")
                        time.sleep(1)
                        fn.log_subsection("Launching pacseek...")
                        fn.subprocess.Popen(
                            ["alacritty", "-e", "sudo", "-u", fn.sudo_username, "pacseek"],
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "pacseek launched")
                    else:
                        fn.log_warn("pacseek binary NOT found, installation may have failed")
                except Exception as e:
                    fn.log_error(f"Error during installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
        else:
            fn.log_subsection("Launching pacseek...")
            fn.subprocess.Popen(
                ["alacritty", "-e", "sudo", "-u", fn.sudo_username, "pacseek"],
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "pacseek launched")
    except Exception as error:
        fn.log_error(f"Error with pacseek: {error}")


def on_click_software_pacseek_remove(self, widget):
    try:
        fn.log_subsection("Removing pacseek...")
        process = fn.launch_pacman_remove_in_terminal("pacseek")
        GLib.idle_add(fn.show_in_app_notification, self, "pacseek removal started")
        fn.wait_remove_and_update(process, "/usr/bin/pacseek", self.lbl_software_pacseek, "Pacseek - TUI package searcher", self, "pacseek removal complete")
    except Exception as error:
        fn.log_error(f"Error with pacseek removal: {error}")


def on_click_software_pamac_remove(self, widget):
    try:
        fn.log_subsection("Removing pamac-aur...")
        process = fn.launch_pacman_remove_in_terminal("pamac-aur")
        GLib.idle_add(fn.show_in_app_notification, self, "pamac-aur removal started")

        fn.wait_remove_and_update(process, "/usr/bin/pamac-manager", self.lbl_software_pamac, "Pamac - GUI package manager", self, "pamac-aur removal complete")
    except Exception as error:
        fn.log_error(f"Error with pamac removal: {error}")


def on_click_software_octopi_remove(self, widget):
    try:
        fn.log_subsection("Removing octopi...")
        process = fn.launch_pacman_remove_in_terminal("octopi")
        GLib.idle_add(fn.show_in_app_notification, self, "octopi removal started")

        fn.wait_remove_and_update(process, "/usr/bin/octopi", self.lbl_software_octopi, "Octopi - GUI package manager", self, "octopi removal complete")
    except Exception as error:
        fn.log_error(f"Error with octopi removal: {error}")


def on_click_software_gnome_remove(self, widget):
    try:
        fn.log_subsection("Removing gnome-software...")
        process = fn.launch_pacman_remove_in_terminal("gnome-software")
        GLib.idle_add(fn.show_in_app_notification, self, "gnome-software removal started")

        fn.wait_remove_and_update(process, "/usr/bin/gnome-software", self.lbl_software_gnome, "GNOME Software - GUI package manager", self, "gnome-software removal complete")
    except Exception as error:
        fn.log_error(f"Error with gnome-software removal: {error}")


def on_click_software_discover_remove(self, widget):
    try:
        fn.log_subsection("Removing discover...")
        process = fn.launch_pacman_remove_in_terminal("discover")
        GLib.idle_add(fn.show_in_app_notification, self, "plasma-discover removal started")

        fn.wait_remove_and_update(process, "/usr/bin/plasma-discover", self.lbl_software_discover, "KDE Discover - GUI package manager", self, "plasma-discover removal complete")
    except Exception as error:
        fn.log_error(f"Error with discover removal: {error}")


def on_click_software_bauh_remove(self, widget):
    try:
        fn.log_subsection("Removing bauh...")
        process = fn.launch_pacman_remove_in_terminal("bauh")
        GLib.idle_add(fn.show_in_app_notification, self, "bauh removal started")

        fn.wait_remove_and_update(process, "/usr/bin/bauh", self.lbl_software_bauh, "Bauh - GUI package manager", self, "bauh removal complete")
    except Exception as error:
        fn.log_error(f"Error with bauh removal: {error}")


def on_click_software_archlinux_logout(self, widget):
    try:
        if fn.path.exists("/usr/bin/archlinux-logout"):
            fn.log_subsection("Launching archlinux-logout...")
            fn.subprocess.Popen(
                "archlinux-logout &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "ArchLinux Logout launched")
        else:
            fn.log_subsection("Installing archlinux-logout-gtk4-git...")
            process = fn.launch_pacman_install_in_terminal("archlinux-logout-gtk4-git")
            GLib.idle_add(fn.show_in_app_notification, self, "archlinux-logout-gtk4-git installation started")

            def wait_install():
                try:
                    import time
                    fn.debug_print("Waiting for archlinux-logout-gtk4-git installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/archlinux-logout"):
                        fn.log_success("archlinux-logout-gtk4-git installed successfully")
                        GLib.idle_add(self.lbl_software_archlinux_logout.set_markup, "ArchLinux Logout - Session logout tool <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "archlinux-logout-gtk4-git installed")
                        time.sleep(1)
                        fn.log_subsection("Launching archlinux-logout...")
                        fn.subprocess.Popen(
                            "archlinux-logout &",
                            shell=True,
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "ArchLinux Logout launched")
                    else:
                        fn.log_warn("archlinux-logout binary NOT found, installation may have failed")
                        fn.check_missing_repo_error(self, "", "archlinux-logout-gtk4-git")
                except Exception as e:
                    fn.log_error(f"Error during installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        fn.log_error(f"Error with archlinux-logout: {error}")


def on_click_software_archlinux_logout_remove(self, widget):
    try:
        fn.log_subsection("Removing archlinux-logout-gtk4-git...")
        process = fn.launch_pacman_remove_in_terminal("archlinux-logout-gtk4-git")
        GLib.idle_add(fn.show_in_app_notification, self, "archlinux-logout-gtk4-git removal started")

        fn.wait_remove_and_update(process, "/usr/bin/archlinux-logout", self.lbl_software_archlinux_logout, "ArchLinux Logout - Session logout tool", self, "archlinux-logout-gtk4-git removal complete")
    except Exception as error:
        fn.log_error(f"Error with archlinux-logout removal: {error}")


def on_click_software_powermenu(self, widget):
    try:
        if fn.path.exists("/usr/local/bin/edu-powermenu"):
            fn.log_subsection("Launching edu-powermenu...")
            fn.subprocess.Popen(
                "edu-powermenu &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "powermenu launched")
        else:
            fn.log_subsection("Installing edu-powermenu-git...")
            process = fn.launch_pacman_install_in_terminal("edu-powermenu-git")
            GLib.idle_add(fn.show_in_app_notification, self, "edu-powermenu-git installation started")

            def wait_install():
                try:
                    import time
                    fn.debug_print("Waiting for edu-powermenu-git installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/local/bin/edu-powermenu"):
                        fn.log_success("edu-powermenu-git installed successfully")
                        GLib.idle_add(self.lbl_software_powermenu.set_markup, "powermenu - Power menu for i3/sway <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "edu-powermenu-git installed")
                        time.sleep(1)
                        fn.log_subsection("Launching edu-powermenu...")
                        fn.subprocess.Popen(
                            "edu-powermenu &",
                            shell=True,
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "powermenu launched")
                    else:
                        fn.log_warn("edu-powermenu binary NOT found, installation may have failed")
                        fn.check_missing_repo_error(self, "", "edu-powermenu-git")
                except Exception as e:
                    fn.log_error(f"Error during installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        fn.log_error(f"Error with edu-powermenu: {error}")


def on_click_software_powermenu_remove(self, widget):
    try:
        fn.log_subsection("Removing edu-powermenu-git...")
        process = fn.launch_pacman_remove_in_terminal("edu-powermenu-git")
        GLib.idle_add(fn.show_in_app_notification, self, "edu-powermenu-git removal started")

        fn.wait_remove_and_update(process, "/usr/local/bin/edu-powermenu", self.lbl_software_powermenu, "powermenu - Power menu for i3/sway", self, "edu-powermenu-git removal complete")
    except Exception as error:
        fn.log_error(f"Error with edu-powermenu removal: {error}")
