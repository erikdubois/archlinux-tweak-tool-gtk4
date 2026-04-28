# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
from gi.repository import GLib

def on_click_software_pamac(self, widget):
    try:
        if fn.path.exists("/usr/bin/pamac-manager"):
            print("\n[INFO] Launching pamac-manager")
            fn.subprocess.Popen(
                "sudo -E -u " + fn.sudo_username + " pamac-manager &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "Pamac launched")
        else:
            print("\n[INFO] pamac-aur not installed, starting installation")
            process = fn.launch_pacman_install_in_terminal("pamac-aur")
            GLib.idle_add(fn.show_in_app_notification, self, "pamac-aur installation started")

            def wait_install():
                try:
                    import time
                    print("[INFO] Waiting for pamac-aur installation to complete...")
                    process.wait()
                    print("[INFO] Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/pamac-manager"):
                        print("[INFO] Binary exists at /usr/bin/pamac-manager, installation successful")
                        GLib.idle_add(self.lbl_software_pamac.set_markup, "Pamac - GUI package manager <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "pamac-aur installed")
                        time.sleep(1)
                        print("[INFO] Launching pamac-manager")
                        fn.subprocess.Popen(
                            "sudo -E -u " + fn.sudo_username + " pamac-manager &",
                            shell=True,
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "Pamac launched")
                    else:
                        print("[INFO] Binary NOT found at /usr/bin/pamac-manager, checking for errors...")
                        fn.check_missing_repo_error(self, "", "pamac-aur")
                except Exception as e:
                    print(f"Error: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        print(error)


def on_click_software_octopi(self, widget):
    try:
        if fn.path.exists("/usr/bin/octopi"):
            print("\n[INFO] Launching octopi")
            fn.subprocess.Popen(
                "sudo -E -u " + fn.sudo_username + " octopi &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "Octopi launched")
        else:
            print("\n[INFO] octopi not installed, starting installation")
            process = fn.launch_pacman_install_in_terminal("octopi")
            GLib.idle_add(fn.show_in_app_notification, self, "octopi installation started")

            def wait_install():
                try:
                    import time
                    print("[INFO] Waiting for octopi installation to complete...")
                    process.wait()
                    print("[INFO] Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/octopi"):
                        print("[INFO] Binary exists at /usr/bin/octopi, installation successful")
                        GLib.idle_add(self.lbl_software_octopi.set_markup, "Octopi - GUI package manager <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "octopi installed")
                        time.sleep(1)
                        print("[INFO] Launching octopi")
                        fn.subprocess.Popen(
                            "sudo -E -u " + fn.sudo_username + " octopi &",
                            shell=True,
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "Octopi launched")
                    else:
                        print("[INFO] Binary NOT found at /usr/bin/octopi, checking for errors...")
                        fn.check_missing_repo_error(self, "", "octopi")
                except Exception as e:
                    print(f"Error: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        print(error)

def on_click_software_gnome(self, widget):
    try:
        if fn.path.exists("/usr/bin/gnome-software"):
            print("\n[INFO] Launching gnome-software")
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
            print("\n[INFO] gnome-software not installed, starting installation")
            process = fn.launch_pacman_install_in_terminal("gnome-software")
            GLib.idle_add(fn.show_in_app_notification, self, "gnome-software installation started")

            def wait_install():
                try:
                    import time
                    import pwd
                    print("[INFO] Waiting for gnome-software installation to complete...")
                    process.wait()
                    print("[INFO] Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/gnome-software"):
                        print("[INFO] Binary exists at /usr/bin/gnome-software, installation successful")
                        GLib.idle_add(self.lbl_software_gnome.set_markup, "GNOME Software - GUI package manager <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "gnome-software installed")
                        time.sleep(1)
                        print("[INFO] Launching gnome-software")
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
                        print("[INFO] Binary NOT found at /usr/bin/gnome-software, checking for errors...")
                        fn.check_missing_repo_error(self, "", "gnome-software")
                except Exception as e:
                    print(f"Error: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        print(error)

def on_click_software_discover(self, widget):
    try:
        if not fn.path.exists("/usr/bin/plasma-discover"):
            print("\n[INFO] plasma-discover not installed, starting installation")
            process = fn.launch_pacman_install_in_terminal("discover packagekit-qt6")
            GLib.idle_add(fn.show_in_app_notification, self, "discover installation started")

            def wait_install():
                try:
                    import time
                    import pwd
                    print("[INFO] Waiting for discover installation to complete...")
                    process.wait()
                    print("[INFO] Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/plasma-discover"):
                        print("[INFO] Binary exists at /usr/bin/plasma-discover, installation successful")
                        GLib.idle_add(self.lbl_software_discover.set_markup, "KDE Discover - KDE software center (pulls KDE deps) <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "plasma-discover installed")
                        print("[INFO] Launching plasma-discover")
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
                        print("[INFO] Binary NOT found at /usr/bin/plasma-discover, checking for errors...")
                except Exception as e:
                    print(f"Error: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
        else:
            print("\n[INFO] Launching plasma-discover")
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
        print(error)

def on_click_software_bauh(self, widget):
    try:
        if fn.path.exists("/usr/bin/bauh"):
            print("\n[INFO] Launching bauh")
            fn.subprocess.Popen(
                "sudo -E -u " + fn.sudo_username + " bauh &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "Bauh launched")
        else:
            print("\n[INFO] bauh not installed, starting installation")
            process = fn.launch_pacman_install_in_terminal("bauh")
            GLib.idle_add(fn.show_in_app_notification, self, "bauh installation started")
            fn.wait_install_and_update(process, "/usr/bin/bauh", self.lbl_software_bauh, "Bauh - Multi-format package manager <b>installed</b>", self, "bauh installation complete", "bauh")
    except Exception as error:
        print(error)

def on_click_software_yay(self, widget):
    try:
        if fn.path.exists("/usr/bin/yay"):
            print("\n[INFO] yay-git already installed")
            GLib.idle_add(fn.show_in_app_notification, self, "yay-git already installed")
            return
        process = fn.launch_pacman_install_in_terminal("yay-git")
        GLib.idle_add(fn.show_in_app_notification, self, "yay-git installation started")
        fn.wait_install_and_update(process, "/usr/bin/yay", self.lbl_software_yay, "Yay-git - AUR helper (Go-based) <b>installed</b>", self, "yay-git installed", "yay-git")
    except Exception as error:
        print(error)

def on_click_software_paru(self, widget):
    try:
        if fn.path.exists("/usr/bin/paru"):
            print("\n[INFO] paru-git already installed")
            GLib.idle_add(fn.show_in_app_notification, self, "paru-git already installed")
            return
        process = fn.launch_pacman_install_in_terminal("paru-git")
        GLib.idle_add(fn.show_in_app_notification, self, "paru-git installation started")
        fn.wait_install_and_update(process, "/usr/bin/paru", self.lbl_software_paru, "Paru-git - AUR helper (Rust-based) <b>installed</b>", self, "paru-git installed", "paru-git")
    except Exception as error:
        print(error)

def on_click_software_trizen(self, widget):
    try:
        if fn.path.exists("/usr/bin/trizen"):
            print("\n[INFO] trizen already installed")
            GLib.idle_add(fn.show_in_app_notification, self, "trizen already installed")
            return
        print("\n[INFO] trizen not installed, starting installation")
        process = fn.launch_pacman_install_in_terminal("trizen")
        GLib.idle_add(fn.show_in_app_notification, self, "trizen installation started")
        fn.wait_install_and_update(process, "/usr/bin/trizen", self.lbl_software_trizen, "Trizen - AUR helper (Perl-based) <b>installed</b>", self, "trizen installed", "trizen")
    except Exception as error:
        print(error)

def on_click_software_pikaur(self, widget):
    try:
        if fn.path.exists("/usr/bin/pikaur"):
            print("\n[INFO] pikaur-git already installed")
            GLib.idle_add(fn.show_in_app_notification, self, "pikaur-git already installed")
            return
        print("\n[INFO] pikaur-git not installed, starting installation")
        process = fn.launch_pacman_install_in_terminal("pikaur-git")
        GLib.idle_add(fn.show_in_app_notification, self, "pikaur-git installation started")
        fn.wait_install_and_update(process, "/usr/bin/pikaur", self.lbl_software_pikaur, "Pikaur-git - AUR helper (Python-based) <b>installed</b>", self, "pikaur-git installed")
    except Exception as error:
        print(error)

def on_click_software_yay_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("yay-git")
        GLib.idle_add(fn.show_in_app_notification, self, "yay-git removal started")
        fn.wait_remove_and_update(process, "/usr/bin/yay", self.lbl_software_yay, "Yay-git - AUR helper (Go-based)", self, "yay-git removal complete")
    except Exception as error:
        print(error)

def on_click_software_paru_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("paru-git")
        GLib.idle_add(fn.show_in_app_notification, self, "paru-git removal started")
        fn.wait_remove_and_update(process, "/usr/bin/paru", self.lbl_software_paru, "Paru-git - AUR helper (Rust-based)", self, "paru-git removal complete")
    except Exception as error:
        print(error)

def on_click_software_trizen_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("trizen")
        GLib.idle_add(fn.show_in_app_notification, self, "trizen removal started")
        fn.wait_remove_and_update(process, "/usr/bin/trizen", self.lbl_software_trizen, "Trizen - AUR helper (Perl-based)", self, "trizen removal complete")
    except Exception as error:
        print(error)

def on_click_software_pikaur_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("pikaur-git")
        GLib.idle_add(fn.show_in_app_notification, self, "pikaur-git removal started")
        fn.wait_remove_and_update(process, "/usr/bin/pikaur", self.lbl_software_pikaur, "Pikaur-git - AUR helper (Python-based)", self, "pikaur-git removal complete")
    except Exception as error:
        print(error)

def on_click_software_pacui_open(self, widget):
    try:
        if not fn.path.exists("/usr/bin/pacui"):
            print("\n[INFO] pacui not installed, starting installation")
            script = "pacman -S --noconfirm pacui; echo ''; echo '=== Installation complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
            process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
            GLib.idle_add(fn.show_in_app_notification, self, "pacui installation started")

            def wait_install():
                try:
                    import time
                    print("[INFO] Waiting for pacui installation to complete...")
                    process.wait()
                    print("[INFO] Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/pacui"):
                        print("[INFO] Binary exists at /usr/bin/pacui, installation successful")
                        GLib.idle_add(self.lbl_software_pacui.set_markup, "Pacui - TUI pacman wrapper <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "pacui installed")
                        time.sleep(1)
                        print("[INFO] Launching pacui")
                        fn.subprocess.Popen(
                            ["alacritty", "-e", "sudo", "-u", fn.sudo_username, "pacui"],
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "pacui launched")
                    else:
                        print("[INFO] Binary NOT found at /usr/bin/pacui, checking for errors...")
                except Exception as e:
                    print(f"Error: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
        else:
            print("\n[INFO] Launching pacui")
            fn.subprocess.Popen(
                ["alacritty", "-e", "sudo", "-u", fn.sudo_username, "pacui"],
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "pacui launched")
    except Exception as error:
        print(error)

def on_click_software_pacui_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("pacui")
        GLib.idle_add(fn.show_in_app_notification, self, "pacui removal started")
        fn.wait_remove_and_update(process, "/usr/bin/pacui", self.lbl_software_pacui, "Pacui - TUI pacman wrapper", self, "pacui removal complete")
    except Exception as error:
        print(error)

def on_click_software_flatpak(self, widget):
    try:
        if not fn.path.exists("/usr/bin/flatpak"):
            print("\n[INFO] flatpak not installed, starting installation")
            script = "pacman -S --noconfirm flatpak; echo ''; echo '=== Installation complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
            process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
            GLib.idle_add(fn.show_in_app_notification, self, "flatpak installation started")

            def wait_install():
                try:
                    import time
                    print("[INFO] Waiting for flatpak installation to complete...")
                    process.wait()
                    print("[INFO] Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/flatpak"):
                        print("[INFO] Binary exists at /usr/bin/flatpak, installation successful")
                        GLib.idle_add(self.lbl_software_flatpak.set_markup, "Flatpak - Manage Flatpak apps <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "flatpak installed")
                        time.sleep(1)
                        print("[INFO] Launching flatpak")
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
                        print("[INFO] Binary NOT found at /usr/bin/flatpak, checking for errors...")
                except Exception as e:
                    print(f"Error: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
        else:
            print("\n[INFO] Launching flatpak")
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
        print(error)

def on_click_software_flatpak_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("flatpak")
        GLib.idle_add(fn.show_in_app_notification, self, "flatpak removal started")
        fn.wait_remove_and_update(process, "/usr/bin/flatpak", self.lbl_software_flatpak, "Flatpak - Manage Flatpak apps", self, "flatpak removal complete")
    except Exception as error:
        print(error)

def on_click_software_snapd(self, widget):
    try:
        if not fn.path.exists("/usr/bin/snap"):
            aur_helper = fn.get_aur_helper()
            if aur_helper is None:
                GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found - install yay, paru, trizen or pikaur first")
                return
            print("\n[INFO] snapd not installed, starting installation")
            process = fn.launch_aur_install_in_terminal(aur_helper, "snapd")
            GLib.idle_add(fn.show_in_app_notification, self, "snapd installation started")

            def wait_install():
                try:
                    import time
                    print("[INFO] Waiting for snapd installation to complete...")
                    process.wait()
                    print("[INFO] Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/snap"):
                        print("[INFO] Binary exists at /usr/bin/snap, installation successful")
                        GLib.idle_add(self.lbl_software_snapd.set_markup, "Snapd - Manage Snap apps <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "snapd installed")
                    else:
                        print("[INFO] Binary NOT found at /usr/bin/snap, checking for errors...")
                except Exception as e:
                    print(f"Error: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
        else:
            print("\n[INFO] Launching snapd")
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
        print(error)

def on_click_software_snapd_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("snapd")
        GLib.idle_add(fn.show_in_app_notification, self, "snapd removal started")
        fn.wait_remove_and_update(process, "/usr/bin/snap", self.lbl_software_snapd, "Snapd - Manage Snap apps", self, "snapd removal complete")
    except Exception as error:
        print(error)

def on_click_software_appimagelauncher(self, widget):
    try:
        if not fn.path.exists("/usr/bin/app-manager"):
            aur_helper = fn.get_aur_helper()
            if aur_helper is None:
                GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found - install yay, paru, trizen or pikaur first")
                return
            print("\n[INFO] appmanager not installed, starting installation")
            process = fn.launch_aur_install_in_terminal(aur_helper, "appmanager")
            GLib.idle_add(fn.show_in_app_notification, self, "appmanager installation started")

            def wait_install():
                try:
                    import time
                    import pwd
                    print("[INFO] Waiting for appmanager installation to complete...")
                    process.wait()
                    print("[INFO] Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/app-manager"):
                        print("[INFO] Binary exists at /usr/bin/app-manager, installation successful")
                        GLib.idle_add(self.lbl_software_appimagelauncher.set_markup, "App-manager - Manage AppImages <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "appmanager installed")
                        time.sleep(1)
                        print("[INFO] Launching app-manager")
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
                        print("[INFO] Binary NOT found at /usr/bin/app-manager, checking for errors...")
                except Exception as e:
                    print(f"Error: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
            return
        print("\n[INFO] Launching app-manager")
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
        print(error)

def on_click_software_appimagelauncher_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("appmanager")
        GLib.idle_add(fn.show_in_app_notification, self, "appmanager removal started")
        fn.wait_remove_and_update(process, "/usr/bin/app-manager", self.lbl_software_appimagelauncher, "App-manager - Manage AppImages", self, "appmanager removal complete")
    except Exception as error:
        print(error)

def on_click_software_pacseek(self, widget):
    try:
        if not fn.path.exists("/usr/bin/pacseek"):
            print("\n[INFO] pacseek not installed, starting installation")
            script = "pacman -S --noconfirm pacseek; echo ''; echo '=== Installation complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
            process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
            GLib.idle_add(fn.show_in_app_notification, self, "pacseek installation started")

            def wait_install():
                try:
                    import time
                    print("[INFO] Waiting for pacseek installation to complete...")
                    process.wait()
                    print("[INFO] Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/pacseek"):
                        print("[INFO] Binary exists at /usr/bin/pacseek, installation successful")
                        GLib.idle_add(self.lbl_software_pacseek.set_markup, "Pacseek - TUI package searcher <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "pacseek installed")
                        time.sleep(1)
                        print("[INFO] Launching pacseek")
                        fn.subprocess.Popen(
                            ["alacritty", "-e", "sudo", "-u", fn.sudo_username, "pacseek"],
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "pacseek launched")
                    else:
                        print("[INFO] Binary NOT found at /usr/bin/pacseek, checking for errors...")
                except Exception as e:
                    print(f"Error: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
        else:
            print("\n[INFO] Launching pacseek")
            fn.subprocess.Popen(
                ["alacritty", "-e", "sudo", "-u", fn.sudo_username, "pacseek"],
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "pacseek launched")
    except Exception as error:
        print(error)

def on_click_software_pacseek_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("pacseek")
        GLib.idle_add(fn.show_in_app_notification, self, "pacseek removal started")
        fn.wait_remove_and_update(process, "/usr/bin/pacseek", self.lbl_software_pacseek, "Pacseek - TUI package searcher", self, "pacseek removal complete")
    except Exception as error:
        print(error)

def on_click_software_pamac_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("pamac-aur")
        GLib.idle_add(fn.show_in_app_notification, self, "pamac-aur removal started")

        fn.wait_remove_and_update(process, "/usr/bin/pamac-manager", self.lbl_software_pamac, "Pamac - GUI package manager", self, "pamac-aur removal complete")
    except Exception as error:
        print(error)

def on_click_software_octopi_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("octopi")
        GLib.idle_add(fn.show_in_app_notification, self, "octopi removal started")

        fn.wait_remove_and_update(process, "/usr/bin/octopi", self.lbl_software_octopi, "Octopi - GUI package manager", self, "octopi removal complete")
    except Exception as error:
        print(error)

def on_click_software_gnome_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("gnome-software")
        GLib.idle_add(fn.show_in_app_notification, self, "gnome-software removal started")

        fn.wait_remove_and_update(process, "/usr/bin/gnome-software", self.lbl_software_gnome, "GNOME Software - GUI package manager", self, "gnome-software removal complete")
    except Exception as error:
        print(error)

def on_click_software_discover_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("discover")
        GLib.idle_add(fn.show_in_app_notification, self, "plasma-discover removal started")

        fn.wait_remove_and_update(process, "/usr/bin/plasma-discover", self.lbl_software_discover, "KDE Discover - GUI package manager", self, "plasma-discover removal complete")
    except Exception as error:
        print(error)

def on_click_software_bauh_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("bauh")
        GLib.idle_add(fn.show_in_app_notification, self, "bauh removal started")

        fn.wait_remove_and_update(process, "/usr/bin/bauh", self.lbl_software_bauh, "Bauh - GUI package manager", self, "bauh removal complete")
    except Exception as error:
        print(error)

def on_click_software_archlinux_logout(self, widget):
    try:
        if fn.path.exists("/usr/bin/archlinux-logout-gtk4"):
            print("\n[INFO] Launching archlinux-logout-gtk4")
            fn.subprocess.Popen(
                "archlinux-logout-gtk4 &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "ArchLinux Logout launched")
        else:
            print("\n[INFO] archlinux-logout-gtk4-git not installed, starting installation")
            process = fn.launch_pacman_install_in_terminal("archlinux-logout-gtk4-git")
            GLib.idle_add(fn.show_in_app_notification, self, "archlinux-logout-gtk4-git installation started")

            def wait_install():
                try:
                    import time
                    print("[INFO] Waiting for archlinux-logout-gtk4-git installation to complete...")
                    process.wait()
                    print("[INFO] Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/archlinux-logout-gtk4"):
                        print("[INFO] Binary exists at /usr/bin/archlinux-logout-gtk4, installation successful")
                        GLib.idle_add(self.lbl_software_archlinux_logout.set_markup, "ArchLinux Logout - Session logout tool <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "archlinux-logout-gtk4-git installed")
                        time.sleep(1)
                        print("[INFO] Launching archlinux-logout-gtk4")
                        fn.subprocess.Popen(
                            "archlinux-logout-gtk4 &",
                            shell=True,
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "ArchLinux Logout launched")
                    else:
                        print("[INFO] Binary NOT found at /usr/bin/archlinux-logout-gtk4, checking for errors...")
                        fn.check_missing_repo_error(self, "", "archlinux-logout-gtk4-git")
                except Exception as e:
                    print(f"Error: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        print(error)

def on_click_software_archlinux_logout_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("archlinux-logout-gtk4-git")
        GLib.idle_add(fn.show_in_app_notification, self, "archlinux-logout-gtk4-git removal started")

        fn.wait_remove_and_update(process, "/usr/bin/archlinux-logout-gtk4", self.lbl_software_archlinux_logout, "ArchLinux Logout - Session logout tool", self, "archlinux-logout-gtk4-git removal complete")
    except Exception as error:
        print(error)

def on_click_software_powermenu(self, widget):
    try:
        if fn.path.exists("/usr/local/bin/edu-powermenu"):
            print("\n[INFO] Launching edu-powermenu")
            fn.subprocess.Popen(
                "edu-powermenu &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "powermenu launched")
        else:
            print("\n[INFO] edu-powermenu-git not installed, starting installation")
            process = fn.launch_pacman_install_in_terminal("edu-powermenu-git")
            GLib.idle_add(fn.show_in_app_notification, self, "edu-powermenu-git installation started")

            def wait_install():
                try:
                    import time
                    print("[INFO] Waiting for edu-powermenu-git installation to complete...")
                    process.wait()
                    print("[INFO] Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/local/bin/edu-powermenu"):
                        print("[INFO] Binary exists at /usr/local/bin/edu-powermenu, installation successful")
                        GLib.idle_add(self.lbl_software_powermenu.set_markup, "powermenu - Power menu for i3/sway <b>installed</b>")
                        GLib.idle_add(fn.show_in_app_notification, self, "edu-powermenu-git installed")
                        time.sleep(1)
                        print("[INFO] Launching edu-powermenu")
                        fn.subprocess.Popen(
                            "edu-powermenu &",
                            shell=True,
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "powermenu launched")
                    else:
                        print("[INFO] Binary NOT found at /usr/local/bin/edu-powermenu, checking for errors...")
                        fn.check_missing_repo_error(self, "", "edu-powermenu-git")
                except Exception as e:
                    print(f"Error: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        print(error)

def on_click_software_powermenu_remove(self, widget):
    try:
        process = fn.launch_pacman_remove_in_terminal("edu-powermenu-git")
        GLib.idle_add(fn.show_in_app_notification, self, "edu-powermenu-git removal started")

        fn.wait_remove_and_update(process, "/usr/local/bin/edu-powermenu", self.lbl_software_powermenu, "powermenu - Power menu for i3/sway", self, "edu-powermenu-git removal complete")
    except Exception as error:
        print(error)
