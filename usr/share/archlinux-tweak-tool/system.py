import functions as fn
from gi.repository import GLib


def on_click_system_cpu(self, widget):
    try:
        fn.log_subsection("Launching CPU info viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.install_package(self, "bat")
        fn.subprocess.call(
            "alacritty -e bash -c 'lscpu | bat --color=always -l conf | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_memory_disk(self, widget):
    try:
        fn.log_subsection("Launching memory and disk usage viewer...")
        fn.install_package(self, "alacritty")
        fn.subprocess.call(
            "alacritty --hold -e bash -c 'echo \"=== MEMORY ===\"; free -h; echo; echo \"=== DISK USAGE ===\"; df -h'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_lsblk(self, widget):
    try:
        fn.log_subsection("Launching block devices viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.subprocess.call(
            "alacritty -e bash -c 'lsblk -f -o+SIZE | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_lspci(self, widget):
    try:
        fn.log_subsection("Launching PCI devices viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.subprocess.call(
            "alacritty -e bash -c 'lspci -vnn | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_lsusb(self, widget):
    try:
        fn.log_subsection("Launching USB devices viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.subprocess.call(
            "alacritty -e bash -c 'lsusb | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_lsmod(self, widget):
    try:
        fn.log_subsection("Launching loaded modules viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.install_package(self, "bat")
        fn.subprocess.call(
            "alacritty -e bash -c 'lsmod | bat --color=always -l conf | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_inxi(self, widget):
    try:
        fn.log_subsection("Launching system information viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.install_package(self, "inxi")
        fn.subprocess.call(
            "alacritty -e bash -c 'inxi -Fxx -c 2 --za | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_hwinfo(self, widget):
    try:
        fn.log_subsection("Launching hardware information viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.install_package(self, "hwinfo")
        fn.install_package(self, "bat")
        fn.subprocess.call(
            "alacritty -e bash -c 'hwinfo --short | bat --color=always -l conf | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_fdisk(self, widget):
    try:
        fn.log_subsection("Launching disk partitioning viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.install_package(self, "bat")
        fn.subprocess.call(
            "alacritty -e bash -c 'sudo fdisk -l | bat --color=always -l conf | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_fstab(self, widget):
    try:
        fn.log_subsection("Launching fstab viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.install_package(self, "bat")
        fn.subprocess.call(
            "alacritty -e bash -c 'bat --color=always /etc/fstab | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_hostnamectl(self, widget):
    try:
        fn.log_subsection("Launching hostname settings viewer...")
        fn.install_package(self, "alacritty")
        fn.subprocess.call(
            "alacritty --hold -e bash -c 'hostnamectl'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_localectl(self, widget):
    try:
        fn.log_subsection("Launching locale settings viewer...")
        fn.install_package(self, "alacritty")
        fn.subprocess.call(
            "alacritty --hold -e bash -c 'localectl'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_services(self, widget):
    try:
        fn.log_subsection("Launching system services viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.subprocess.call(
            "alacritty -e bash -c 'SYSTEMD_COLORS=1 systemctl list-units --type=service | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_services_enabled(self, widget):
    try:
        fn.log_subsection("Launching enabled services viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.subprocess.call(
            "alacritty -e bash -c 'SYSTEMD_COLORS=1 systemctl list-unit-files --type=service --state=enabled | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_services_failed(self, widget):
    try:
        fn.log_subsection("Launching failed services viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.subprocess.call(
            "alacritty -e bash -c 'SYSTEMD_COLORS=1 systemctl list-units --failed | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_timers_enabled(self, widget):
    try:
        fn.log_subsection("Launching enabled timers viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        import pwd
        uid = pwd.getpwnam(fn.sudo_username).pw_uid
        fn.subprocess.call(
            "alacritty -e bash -c '{ echo \"=== System Timers ===\"; "
            "SYSTEMD_COLORS=1 systemctl list-unit-files --type=timer --state=enabled; "
            "echo; "
            "echo \"=== User Timers ===\"; "
            "sudo -u " + fn.sudo_username +
            " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
            " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus"
            " SYSTEMD_COLORS=1"
            " systemctl --user list-unit-files --type=timer --state=enabled; "
            "} | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_dmesg(self, widget):
    try:
        fn.log_subsection("Launching kernel messages viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.subprocess.call(
            "alacritty -e bash -c 'sudo dmesg --color=always | fzf --ansi'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_gparted(self, widget):
    try:
        if fn.path.exists("/usr/bin/gparted"):
            fn.log_subsection("Launching gparted...")
            fn.subprocess.call(
                "sudo gparted &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "GParted launched")
        else:
            fn.log_subsection("Installing gparted...")
            process = fn.launch_pacman_install_in_terminal("gparted")
            GLib.idle_add(fn.show_in_app_notification, self, "gparted installation started")

            def wait_install():
                try:
                    import time
                    fn.debug_print("Waiting for gparted installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/gparted"):
                        fn.log_success("gparted installed successfully")
                        GLib.idle_add(fn.show_in_app_notification, self, "gparted installed")
                        time.sleep(1)
                        fn.log_subsection("Launching gparted...")
                        fn.subprocess.Popen(
                            "sudo gparted &",
                            shell=True,
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        GLib.idle_add(fn.show_in_app_notification, self, "GParted launched")
                    else:
                        fn.log_warn("gparted binary NOT found, installation may have failed")
                except Exception as e:
                    fn.log_error(f"Error during installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        fn.log_error(f"Error with gparted: {error}")
