# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0301,I1101,W0104

import pwd
import time

import functions as fn
from gi.repository import GLib


def _run_cmd(cmd):
    fn.threading.Thread(
        target=lambda: fn.subprocess.Popen(
            cmd, shell=True, stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT
        ),
        daemon=True,
    ).start()


def on_click_system_cpu(self, _widget):
    try:
        fn.log_subsection("Launching CPU info viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.install_package(self, "bat")
        _run_cmd("alacritty -e bash -c 'lscpu | bat --color=always -l conf | fzf --ansi'")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_memory_disk(self, _widget):
    try:
        fn.log_subsection("Launching memory and disk usage viewer...")
        fn.install_package(self, "alacritty")
        _run_cmd(
            "alacritty --hold -e bash -c "
            "'echo \"=== MEMORY ===\"; free -h; echo; echo \"=== DISK USAGE ===\"; df -h'"
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_lsblk(self, _widget):
    try:
        fn.log_subsection("Launching block devices viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        _run_cmd("alacritty -e bash -c 'lsblk -f -o+SIZE | fzf --ansi'")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_lspci(self, _widget):
    try:
        fn.log_subsection("Launching PCI devices viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        _run_cmd("alacritty -e bash -c 'lspci -vnn | fzf --ansi'")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_lsusb(self, _widget):
    try:
        fn.log_subsection("Launching USB devices viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        _run_cmd("alacritty -e bash -c 'lsusb | fzf --ansi'")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_lsmod(self, _widget):
    try:
        fn.log_subsection("Launching loaded modules viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.install_package(self, "bat")
        _run_cmd("alacritty -e bash -c 'lsmod | bat --color=always -l conf | fzf --ansi'")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_inxi(self, _widget):
    try:
        fn.log_subsection("Launching system information viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.install_package(self, "inxi")
        _run_cmd("alacritty -e bash -c 'inxi -Fxx -c 2 --za | fzf --ansi'")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_hwinfo(self, _widget):
    try:
        fn.log_subsection("Launching hardware information viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.install_package(self, "hwinfo")
        fn.install_package(self, "bat")
        _run_cmd("alacritty -e bash -c 'hwinfo --short | bat --color=always -l conf | fzf --ansi'")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_fdisk(self, _widget):
    try:
        fn.log_subsection("Launching disk partitioning viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.install_package(self, "bat")
        _run_cmd("alacritty -e bash -c 'sudo fdisk -l | bat --color=always -l conf | fzf --ansi'")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_fstab(self, _widget):
    try:
        fn.log_subsection("Launching fstab viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        fn.install_package(self, "bat")
        _run_cmd("alacritty -e bash -c 'bat --color=always /etc/fstab | fzf --ansi'")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_hostnamectl(self, _widget):
    try:
        fn.log_subsection("Launching hostname settings viewer...")
        fn.install_package(self, "alacritty")
        _run_cmd("alacritty --hold -e bash -c 'hostnamectl'")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_localectl(self, _widget):
    try:
        fn.log_subsection("Launching locale settings viewer...")
        fn.install_package(self, "alacritty")
        _run_cmd("alacritty --hold -e bash -c 'localectl'")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_services(self, _widget):
    try:
        fn.log_subsection("Launching system services viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        _run_cmd(
            "alacritty -e bash -c 'SYSTEMD_COLORS=1 systemctl list-units --type=service | fzf --ansi'"
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_services_enabled(self, _widget):
    try:
        fn.log_subsection("Launching enabled services viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        _run_cmd(
            "alacritty -e bash -c 'SYSTEMD_COLORS=1 systemctl list-unit-files"
            " --type=service --state=enabled | fzf --ansi'"
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_services_failed(self, _widget):
    try:
        fn.log_subsection("Launching failed services viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        _run_cmd(
            "alacritty -e bash -c 'SYSTEMD_COLORS=1 systemctl list-units --failed | fzf --ansi'"
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_timers_enabled(self, _widget):
    try:
        fn.log_subsection("Launching enabled timers viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        uid = pwd.getpwnam(fn.sudo_username).pw_uid
        cmd = (
            "alacritty -e bash -c '{ echo \"=== System Timers ===\"; "
            "SYSTEMD_COLORS=1 systemctl list-unit-files --type=timer --state=enabled; "
            "echo; "
            "echo \"=== User Timers ===\"; "
            "sudo -u " + fn.sudo_username
            + " XDG_RUNTIME_DIR=/run/user/" + str(uid)
            + " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus"
            " SYSTEMD_COLORS=1"
            " systemctl --user list-unit-files --type=timer --state=enabled; "
            "} | fzf --ansi'"
        )
        _run_cmd(cmd)
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_system_dmesg(self, _widget):
    try:
        fn.log_subsection("Launching kernel messages viewer...")
        fn.install_package(self, "alacritty")
        fn.install_package(self, "fzf")
        _run_cmd("alacritty -e bash -c 'sudo dmesg --color=always | fzf --ansi'")
    except Exception as error:
        fn.log_error(f"Error: {error}")


def _refresh_gparted_label(self):
    self.lbl_gparted.set_markup(
        "Inspect with GParted" + (" <b>installed</b>" if fn.path.exists("/usr/bin/gparted") else "")
    )


def _refresh_partitionmanager_label(self):
    self.lbl_partitionmanager.set_markup(
        "Inspect with Partition Manager"
        + (" <b>installed</b>" if fn.path.exists("/usr/bin/partitionmanager") else "")
    )


def _pm_launch_cmd():
    uid = pwd.getpwnam(fn.sudo_username).pw_uid
    return (
        f"sudo -u {fn.sudo_username}"
        f" XDG_RUNTIME_DIR=/run/user/{uid}"
        f" DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{uid}/bus"
        " DISPLAY=$DISPLAY WAYLAND_DISPLAY=$WAYLAND_DISPLAY"
        " partitionmanager"
    )


def on_click_system_partitionmanager(self, _widget):
    try:
        if fn.path.exists("/usr/bin/partitionmanager"):
            fn.log_subsection("Launching Partition Manager...")
            _run_cmd(_pm_launch_cmd())
            GLib.idle_add(fn.show_in_app_notification, self, "Partition Manager launched")
        else:
            fn.log_subsection("Installing partitionmanager...")
            process = fn.launch_pacman_install_in_terminal("partitionmanager")
            GLib.idle_add(fn.show_in_app_notification, self, "partitionmanager installation started")

            def wait_install():
                try:
                    fn.debug_print("Waiting for partitionmanager installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/partitionmanager"):
                        fn.log_success("partitionmanager installed successfully")
                        GLib.idle_add(fn.show_in_app_notification, self, "partitionmanager <b>installed</b>")
                        GLib.idle_add(_refresh_partitionmanager_label, self)
                        time.sleep(1)
                        fn.log_subsection("Launching Partition Manager...")
                        _run_cmd(_pm_launch_cmd())
                        GLib.idle_add(fn.show_in_app_notification, self, "Partition Manager launched")
                    else:
                        fn.log_warn("partitionmanager binary NOT found, installation may have failed")
                except Exception as e:
                    fn.log_error(f"Error during installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        fn.log_error(f"Error with partitionmanager: {error}")


def on_click_system_partitionmanager_remove(self, _widget):
    try:
        if not fn.path.exists("/usr/bin/partitionmanager"):
            fn.log_info("partitionmanager is not installed")
            fn.show_in_app_notification(self, "partitionmanager is not installed")
            return
        fn.log_subsection("Removing partitionmanager...")
        process = fn.launch_pacman_remove_in_terminal("partitionmanager")
        GLib.idle_add(fn.show_in_app_notification, self, "partitionmanager removal started")

        def wait_remove():
            try:
                process.wait()
                GLib.idle_add(_refresh_partitionmanager_label, self)
            except Exception as e:
                fn.log_error(f"Error waiting for partitionmanager removal: {e}")

        fn.threading.Thread(target=wait_remove, daemon=True).start()
    except Exception as error:
        fn.log_error(f"Error removing partitionmanager: {error}")


def on_click_system_gparted(self, _widget):
    try:
        if fn.path.exists("/usr/bin/gparted"):
            fn.log_subsection("Launching gparted...")
            _run_cmd("sudo gparted")
            GLib.idle_add(fn.show_in_app_notification, self, "GParted launched")
        else:
            fn.log_subsection("Installing gparted...")
            process = fn.launch_pacman_install_in_terminal("gparted")
            GLib.idle_add(fn.show_in_app_notification, self, "gparted installation started")

            def wait_install():
                try:
                    fn.debug_print("Waiting for gparted installation to complete...")
                    process.wait()
                    fn.debug_print("Installation process completed")
                    time.sleep(1)
                    if fn.path.exists("/usr/bin/gparted"):
                        fn.log_success("gparted installed successfully")
                        GLib.idle_add(fn.show_in_app_notification, self, "gparted <b>installed</b>")
                        GLib.idle_add(_refresh_gparted_label, self)
                        time.sleep(1)
                        fn.log_subsection("Launching gparted...")
                        _run_cmd("sudo gparted")
                        GLib.idle_add(fn.show_in_app_notification, self, "GParted launched")
                    else:
                        fn.log_warn("gparted binary NOT found, installation may have failed")
                except Exception as e:
                    fn.log_error(f"Error during installation: {e}")

            fn.threading.Thread(target=wait_install, daemon=True).start()
    except Exception as error:
        fn.log_error(f"Error with gparted: {error}")


def on_click_system_gparted_remove(self, _widget):
    try:
        if not fn.path.exists("/usr/bin/gparted"):
            fn.log_info("gparted is not installed")
            fn.show_in_app_notification(self, "gparted is not installed")
            return
        fn.log_subsection("Removing gparted...")
        process = fn.launch_pacman_remove_in_terminal("gparted")
        GLib.idle_add(fn.show_in_app_notification, self, "gparted removal started")

        def wait_remove():
            try:
                process.wait()
                GLib.idle_add(_refresh_gparted_label, self)
            except Exception as e:
                fn.log_error(f"Error waiting for gparted removal: {e}")

        fn.threading.Thread(target=wait_remove, daemon=True).start()
    except Exception as error:
        fn.log_error(f"Error removing gparted: {error}")
