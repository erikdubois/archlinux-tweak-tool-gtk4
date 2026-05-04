# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
from functions import GLib
from gi.repository import Gtk

NSSWITCH_OPTIONS = {
    "Standard (no mdns)":
        "mymachines resolve [!UNAVAIL=return] files myhostname dns",
    "With mdns + wins":
        "mymachines resolve [!UNAVAIL=return] files dns mdns wins myhostname",
    "With mdns_minimal":
        "mymachines mdns_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] files myhostname dns",
    "With mdns4_minimal":
        "mymachines mdns4_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] files myhostname dns",
    "Custom order (no systemd)":
        "files mymachines myhostname mdns_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] dns wins",
}


def choose_nsswitch(self):
    fn.log_subsection("Apply Nsswitch Configuration")
    label = fn.get_combo_text(self.nsswitch_choices)

    if label in NSSWITCH_OPTIONS:
        hosts_line = NSSWITCH_OPTIONS[label]
        fn.log_info(f"  Preset : {label}")
        fn.log_info(f"  hosts: : {hosts_line}")
        fn.debug_print("  File   : /etc/nsswitch.conf")
        fn.copy_nsswitch(hosts_line)
        fn.log_success("Nsswitch configuration applied")
        GLib.idle_add(fn.show_in_app_notification, self, f"Nsswitch: {label}")
    else:
        fn.log_warn(f"Unknown nsswitch preset: {label}")


def choose_smb_conf(self):
    fn.log_subsection("Apply Samba Configuration")
    shared_path = f"/home/{fn.sudo_username}/Shared"

    def _apply():
        fn.debug_print("  Config : example smb.conf")
        fn.copy_samba("example")
        fn.log_success("Samba configuration applied")
        GLib.idle_add(fn.show_in_app_notification, self, "Smb.conf ATT configuration applied")

    if fn.path.isdir(shared_path):
        fn.debug_print(f"  Folder : {shared_path} already exists")
        _apply()
        return

    dialog = Gtk.MessageDialog(
        transient_for=self,
        modal=True,
        message_type=Gtk.MessageType.QUESTION,
        buttons=Gtk.ButtonsType.YES_NO,
        text=(
            f"Create Shared folder?\n\n"
            f"ATT will create {shared_path} as your samba share folder.\n"
            "If you choose No, create the folder yourself before connecting."
        ),
    )

    def on_response(_dialog, response):
        _dialog.destroy()
        if response == Gtk.ResponseType.YES:
            fn.makedirs(shared_path, 0o755)
            fn.permissions(shared_path)
            fn.debug_print(f"  Created : {shared_path}")
        else:
            fn.debug_print("  Skipped : folder creation — user declined")
        _apply()

    dialog.connect("response", on_response)
    dialog.present()


def create_samba_user(self):
    username = fn.sudo_username

    if not username:
        fn.log_warn("Could not determine current user for samba password")
        return

    fn.log_subsection("Create Samba User")
    fn.debug_print(f"  Username : {username}")
    fn.debug_print("  Note     : Samba uses a separate password from Linux user accounts")

    script = f"""
echo 'Creating samba password for user: {username}'
echo 'Samba uses a separate password from your Linux login.'
echo ''

if ! command -v smbpasswd &>/dev/null; then
    echo '✗ smbpasswd not found — please install samba first'
    echo ''
    echo '=== Operation Finished ==='
    read -p 'Press Enter to close...'
    exit 1
fi

smbpasswd -a {username}
RESULT=$?

echo ''
if [ $RESULT -eq 0 ]; then
    echo '✓ Samba password set successfully'
else
    echo '✗ Failed to set samba password'
fi

echo ''
echo '=== Operation Finished ==='
read -p 'Press Enter to close...'
"""

    def _launch():
        try:
            fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script])
            fn.GLib.idle_add(fn.show_in_app_notification, self, f"Setting samba password for {username}...")
        except Exception as error:
            fn.GLib.idle_add(fn.log_error, f"Failed to open terminal: {error}")

    fn.threading.Thread(target=_launch, daemon=True).start()


def check_audio_server(expected):
    try:
        result = fn.subprocess.run(
            ["pactl", "info"],
            capture_output=True,
            text=True,
            timeout=3
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'Server Name' in line:
                    fn.log_info_concise(f"  Active: {line.strip()}")
                    if expected.lower() in line.lower():
                        return True
        return False
    except Exception as e:
        fn.debug_print(f"Could not verify audio server: {e}")
        return None


def restart_smb(self):
    fn.log_subsection("SAMBA SERVICE RESTART - STATUS CHECKLIST")
    fn.debug_print(f"Configuration: {fn.samba_config}")

    smb_active = fn.check_service("smb")
    nmb_active = fn.check_service("nmb")
    avahi_active = fn.check_service("avahi-daemon")

    fn.debug_print(f"✓ Samba (smb):           {'✓ ACTIVE' if smb_active else '✗ INACTIVE'}")
    fn.debug_print(f"✓ NetBIOS (nmb):         {'✓ ACTIVE' if nmb_active else '✗ INACTIVE'}")
    fn.debug_print(f"✓ Avahi (discovery):     {'✓ ACTIVE' if avahi_active else '✗ INACTIVE'}")

    if not smb_active:
        fn.log_error("Samba is not installed or running")
        fn.debug_print("REQUIRED SETUP:")
        fn.debug_print("1. Install samba package: pacman -S samba")
        fn.debug_print("2. Enable services:")
        fn.debug_print("   - systemctl enable smb")
        if not nmb_active:
            fn.debug_print("   - systemctl enable nmb")
        if not avahi_active:
            fn.debug_print("   - systemctl enable avahi-daemon")
        fn.debug_print("3. Start services: systemctl start smb (and nmb/avahi if needed)")
        fn.debug_print("For help, run: sudo systemctl status smb")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "✗ Samba not running. Check terminal output for setup instructions.",
        )
        return

    def _restart():
        fn.debug_print("Restarting samba services...")
        fn.subprocess.run(["systemctl", "restart", "smb"], check=False)
        if nmb_active:
            fn.subprocess.run(["systemctl", "restart", "nmb"], check=False)
        fn.log_success("Samba services restarted successfully")
        GLib.idle_add(update_network_status, self)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "✓ Samba restarted. Check other services in the status bar.",
        )

    fn.threading.Thread(target=_restart, daemon=True).start()


# ====================================================================
# SERVICES CALLBACKS
# ====================================================================

def on_click_switch_to_pulseaudio(self, _widget):
    fn.log_subsection("Switch to PulseAudio — opening terminal")
    cmd = (
        "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/bin/install-pulseaudio.sh;"
        " read -p \"Press Enter to close...\"'"
    )

    def _wait():
        try:
            fn.subprocess.Popen(cmd, shell=True).wait()
            fn.log_success("PulseAudio install completed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "PulseAudio install completed")
        except Exception as error:
            fn.log_error(f"Failed to open terminal: {error}")

    fn.threading.Thread(target=_wait, daemon=True).start()


def on_click_switch_to_pipewire(self, _widget):
    fn.log_subsection("Switch to PipeWire — opening terminal")
    cmd = (
        "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/bin/install-pipewire.sh;"
        " read -p \"Press Enter to close...\"'"
    )

    def _wait():
        try:
            fn.subprocess.Popen(cmd, shell=True).wait()
            fn.log_success("PipeWire install completed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "PipeWire install completed")
        except Exception as error:
            fn.log_error(f"Failed to open terminal: {error}")

    fn.threading.Thread(target=_wait, daemon=True).start()


def on_click_install_bluetooth(self, _widget):
    fn.log_subsection("Install Bluetooth")
    try:
        fn.launch_pacman_install_in_terminal("bluez bluez-utils")
        fn.debug_print("Bluetooth packages installed")
        if fn.check_package_installed("bluez"):
            self.enable_bt.set_sensitive(True)
            self.disable_bt.set_sensitive(True)
            self.restart_bt.set_sensitive(True)
            fn.log_success("Bluetooth installed and controls enabled")
        else:
            fn.log_warn("Bluetooth package not found after installation")
    except Exception as error:
        fn.log_error(f"Failed to install bluetooth: {error}")


def on_click_remove_bluetooth(self, _widget):
    fn.log_subsection("Remove Bluetooth")
    try:
        fn.launch_pacman_remove_in_terminal("bluez bluez-utils")
        fn.debug_print("Bluetooth packages removed")
        if not fn.check_package_installed("bluez"):
            self.enable_bt.set_sensitive(False)
            self.disable_bt.set_sensitive(False)
            self.restart_bt.set_sensitive(False)
            fn.log_success("Bluetooth removed and controls disabled")
        else:
            fn.log_warn("Bluetooth package still present after removal")
    except Exception as error:
        fn.log_error(f"Failed to remove bluetooth: {error}")


def on_click_install_blueberry(self, _widget):
    fn.log_subsection("Install Blueberry")
    try:
        fn.launch_pacman_install_in_terminal("blueberry")
        fn.log_success("Blueberry installed")
    except Exception as error:
        fn.log_error(f"Failed to install blueberry: {error}")


def on_click_remove_blueberry(self, _widget):
    fn.log_subsection("Remove Blueberry")
    try:
        fn.launch_pacman_remove_in_terminal("blueberry")
        fn.log_success("Blueberry removed")
    except Exception as error:
        fn.log_error(f"Failed to remove blueberry: {error}")


def on_click_install_blueman(self, _widget):
    fn.log_subsection("Install Blueman")
    try:
        fn.launch_pacman_install_in_terminal("blueman")
        fn.log_success("Blueman installed")
    except Exception as error:
        fn.log_error(f"Failed to install blueman: {error}")


def on_click_remove_blueman(self, _widget):
    fn.log_subsection("Remove Blueman")
    try:
        fn.launch_pacman_remove_in_terminal("blueman")
        fn.log_success("Blueman removed")
    except Exception as error:
        fn.log_error(f"Failed to remove blueman: {error}")


def on_click_install_bluedevil(self, _widget):
    fn.log_subsection("Install Bluedevil")
    try:
        fn.launch_pacman_install_in_terminal("bluedevil")
        fn.log_success("Bluedevil installed")
    except Exception as error:
        fn.log_error(f"Failed to install bluedevil: {error}")


def on_click_remove_bluedevil(self, _widget):
    fn.log_subsection("Remove Bluedevil")
    try:
        fn.launch_pacman_remove_in_terminal("bluedevil")
        fn.log_success("Bluedevil removed")
    except Exception as error:
        fn.log_error(f"Failed to remove bluedevil: {error}")


def on_click_enable_bluetooth(self, _widget):
    fn.log_subsection("Enable Bluetooth Service")
    try:
        fn.enable_service("bluetooth")
        fn.log_success("Bluetooth service enabled")
        fn.show_in_app_notification(self, "Bluetooth has been enabled")
    except Exception as error:
        fn.log_error(f"Failed to enable bluetooth: {error}")


def on_click_disable_bluetooth(self, _widget):
    fn.log_subsection("Disable Bluetooth Service")
    try:
        fn.disable_service("bluetooth")
        fn.log_success("Bluetooth service disabled")
        fn.show_in_app_notification(self, "Bluetooth has been disabled")
    except Exception as error:
        fn.log_error(f"Failed to disable bluetooth: {error}")


def on_click_restart_bluetooth(self, _widget):
    fn.log_subsection("Restart Bluetooth Service")
    try:
        fn.restart_service("bluetooth")
        fn.log_success("Bluetooth service restarted")
        fn.show_in_app_notification(self, "Bluetooth has been restarted")
    except Exception as error:
        fn.log_error(f"Failed to restart bluetooth: {error}")


def on_click_install_cups(self, _widget):
    fn.log_subsection("Install CUPS")
    try:
        fn.launch_pacman_install_in_terminal("cups")
        fn.log_success("CUPS installed")
    except Exception as error:
        fn.log_error(f"Failed to install CUPS: {error}")


def on_click_remove_cups(self, _widget):
    fn.log_subsection("Remove CUPS")
    try:
        fn.launch_pacman_remove_in_terminal("cups cups-filters")
        fn.log_success("CUPS removed")
    except Exception as error:
        fn.log_error(f"Failed to remove CUPS: {error}")


def on_click_install_cups_pdf(self, _widget):
    fn.log_subsection("Install CUPS PDF")

    def wait_and_update():
        fn.launch_pacman_install_in_terminal("cups-pdf")
        fn.debug_print("Waiting for terminal to close...")
        fn.threading.Event().wait(2)
        if fn.check_package_installed("cups-pdf"):
            GLib.idle_add(
                self.cups_pdf_label.set_markup,
                "Cups-pdf is <b>installed</b>"
            )
            GLib.idle_add(fn.log_success, "CUPS PDF printer installed")

    fn.threading.Thread(target=wait_and_update, daemon=True).start()


def on_click_remove_cups_pdf(self, _widget):
    fn.log_subsection("Remove CUPS PDF")

    def wait_and_update():
        fn.launch_pacman_remove_in_terminal("cups-pdf")
        fn.debug_print("Waiting for terminal to close...")
        fn.threading.Event().wait(2)
        if not fn.check_package_installed("cups-pdf"):
            GLib.idle_add(
                self.cups_pdf_label.set_markup,
                "Install cups-pdf printing"
            )
            GLib.idle_add(fn.log_success, "CUPS PDF printer removed")

    fn.threading.Thread(target=wait_and_update, daemon=True).start()


def update_cups_status(self):
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

    GLib.idle_add(
        self.cups_status_label.set_markup,
        "Cups service : " + status1 + "   Cups socket : " + status2
    )


def on_click_enable_cups(self, _widget):
    fn.log_subsection("Enable CUPS Service")
    try:
        fn.enable_service("cups")
        fn.log_success("CUPS service enabled")
        update_cups_status(self)
    except Exception as error:
        fn.log_error(f"Failed to enable CUPS: {error}")


def on_click_disable_cups(self, _widget):
    fn.log_subsection("Disable CUPS Service")
    try:
        fn.disable_service("cups")
        fn.log_success("CUPS service disabled")
        update_cups_status(self)
    except Exception as error:
        fn.log_error(f"Failed to disable CUPS: {error}")


def on_click_restart_cups(self, _widget):
    fn.log_subsection("Restart CUPS Service")
    try:
        fn.restart_service("cups")
        fn.log_success("CUPS service restarted")
        update_cups_status(self)
    except Exception as error:
        fn.log_error(f"Failed to restart CUPS: {error}")


def on_click_install_printer_drivers(self, _widget):
    fn.log_subsection("Install Printer Drivers")

    def wait_and_update():
        packages = (
            "foomatic-db-engine foomatic-db foomatic-db-ppds "
            "foomatic-db-nonfree foomatic-db-nonfree-ppds "
            "gutenprint foomatic-db-gutenprint-ppds ghostscript gsfonts"
        )
        fn.launch_pacman_install_in_terminal(packages)
        fn.debug_print("Waiting for terminal to close...")
        fn.threading.Event().wait(2)
        if fn.check_package_installed("foomatic-db"):
            GLib.idle_add(
                self.printer_drivers_label.set_markup,
                "   Install common printer drivers (foomatic, gutenprint, ...) - <b>Installed</b>"
            )
            GLib.idle_add(fn.log_success, "Printer drivers installed successfully")

    fn.threading.Thread(target=wait_and_update, daemon=True).start()


def on_click_remove_printer_drivers(self, _widget):
    fn.log_subsection("Remove Printer Drivers")

    def wait_and_update():
        packages = (
            "foomatic-db-engine foomatic-db foomatic-db-ppds "
            "foomatic-db-nonfree foomatic-db-nonfree-ppds "
            "gutenprint foomatic-db-gutenprint-ppds ghostscript gsfonts"
        )
        fn.launch_pacman_remove_in_terminal(packages)
        fn.debug_print("Waiting for terminal to close...")
        fn.threading.Event().wait(2)
        if not fn.check_package_installed("foomatic-db"):
            GLib.idle_add(
                self.printer_drivers_label.set_markup,
                "   Install common printer drivers (foomatic, gutenprint, ...)"
            )
            GLib.idle_add(fn.log_success, "Printer drivers removed successfully")

    fn.threading.Thread(target=wait_and_update, daemon=True).start()


def on_click_install_hplip(self, _widget):
    fn.log_subsection("Install HPLIP")

    def wait_and_update():
        fn.launch_pacman_install_in_terminal("hplip")
        fn.debug_print("Waiting for terminal to close...")
        fn.threading.Event().wait(2)
        if fn.check_package_installed("hplip"):
            GLib.idle_add(
                self.hplip_label.set_markup,
                "   HP drivers have been <b>installed</b>"
            )
            GLib.idle_add(fn.log_success, "HPLIP installed")

    fn.threading.Thread(target=wait_and_update, daemon=True).start()


def on_click_remove_hplip(self, _widget):
    fn.log_subsection("Remove HPLIP")

    def wait_and_update():
        fn.launch_pacman_remove_in_terminal("hplip")
        fn.debug_print("Waiting for terminal to close...")
        fn.threading.Event().wait(2)
        if not fn.check_package_installed("hplip"):
            GLib.idle_add(
                self.hplip_label.set_markup,
                "   Install HP drivers"
            )
            GLib.idle_add(fn.log_success, "HPLIP removed")

    fn.threading.Thread(target=wait_and_update, daemon=True).start()


def on_click_install_system_config_printer(self, _widget):
    fn.log_subsection("Install System Config Printer")
    fn.show_in_app_notification(self, "Installing System-config-printer...")

    def wait_and_update():
        fn.launch_pacman_install_in_terminal("system-config-printer")
        fn.debug_print("Waiting for terminal to close...")
        fn.threading.Event().wait(2)
        if fn.check_package_installed("system-config-printer"):
            GLib.idle_add(
                self.system_config_printer_label.set_markup,
                "Install System-config-printer - <b>Installed</b>"
            )
            GLib.idle_add(fn.log_success, "System Config Printer installed")

    fn.threading.Thread(target=wait_and_update, daemon=True).start()


def on_click_remove_system_config_printer(self, _widget):
    fn.log_subsection("Remove System Config Printer")
    fn.show_in_app_notification(self, "Removing System-config-printer...")

    def wait_and_update():
        fn.launch_pacman_remove_in_terminal("system-config-printer")
        fn.debug_print("Waiting for terminal to close...")
        fn.threading.Event().wait(2)
        if not fn.check_package_installed("system-config-printer"):
            GLib.idle_add(
                self.system_config_printer_label.set_markup,
                "Install System-config-printer"
            )
            GLib.idle_add(fn.log_success, "System Config Printer removed")

    fn.threading.Thread(target=wait_and_update, daemon=True).start()


def update_network_status(self):
    if hasattr(self, 'network_status_label'):
        status1 = fn.check_service("smb")
        status1_text = "<b>active</b>" if status1 else "inactive"
        status2 = fn.check_service("nmb")
        status2_text = "<b>active</b>" if status2 else "inactive"
        status3 = fn.check_service("avahi-daemon")
        status3_text = "<b>active</b>" if status3 else "inactive"
        self.network_status_label.set_markup(
            "Samba: " + status1_text + "   Nmb: " + status2_text + "   Avahi: " + status3_text
        )


def on_install_discovery_clicked(self, _widget):
    def _wait(process):
        if process is None:
            return
        process.wait()
        GLib.idle_add(update_network_status, self)
    proc = fn.install_discovery(self)
    fn.threading.Thread(target=_wait, args=(proc,), daemon=True).start()


def on_remove_discovery_clicked(self, _widget):
    def _wait(process):
        if process is None:
            return
        process.wait()
        GLib.idle_add(update_network_status, self)
    proc = fn.remove_discovery(self)
    fn.threading.Thread(target=_wait, args=(proc,), daemon=True).start()


def on_click_reset_nsswitch(self, _widget):
    fn.log_subsection("Reset Nsswitch Configuration")
    if fn.path.isfile(fn.nsswitch_config + ".bak"):
        try:
            fn.shutil.copy(fn.nsswitch_config + ".bak", fn.nsswitch_config)
            fn.debug_print(f"Restored from backup: {fn.nsswitch_config}.bak")
            fn.log_success("Nsswitch configuration reset to original")
            fn.show_in_app_notification(self, "Nsswitch config reset")
        except Exception as error:
            fn.log_error(f"Failed to reset nsswitch: {error}")
    else:
        fn.log_warn("No backup configuration file found")
        fn.show_in_app_notification(self, "No nsswitch backup available")


def on_click_edit_nsswitch(self, _widget):
    fn.log_subsection("Edit Nsswitch Configuration")
    try:
        fn.subprocess.Popen(
            ["alacritty", "-e", "nano", fn.nsswitch_config],
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.PIPE,
        )
        fn.debug_print(f"File: {fn.nsswitch_config}")
        fn.log_success("Nsswitch configuration opened in nano editor")
        fn.show_in_app_notification(self, "nsswitch.conf opened in terminal")
    except Exception as e:
        fn.log_error(f"Failed to open nsswitch configuration: {e}")


def on_click_apply_nsswitch(self, _widget):
    choose_nsswitch(self)


def on_click_create_samba_user(self, _widget):
    create_samba_user(self)


def on_click_restart_smb(self, _widget):
    restart_smb(self)


def on_click_save_samba_share(self, _widget):
    fn.log_subsection("Save Samba Share Configuration")
    try:
        fn.save_samba_config(self)
        fn.log_success("Samba share configuration saved")
    except Exception as error:
        fn.log_error(f"Failed to save samba configuration: {error}")


def on_click_apply_samba(self, _widget):
    fn.log_subsection("Apply Samba Configuration")
    try:
        choose_smb_conf(self)
        fn.debug_print("Samba configuration applied from selected template")
        fn.log_success("Samba configuration applied successfully")
        fn.show_in_app_notification(self, "Samba configuration applied")
    except Exception as error:
        fn.log_error(f"Failed to apply samba configuration: {error}")


def on_click_reset_samba(self, _widget):
    fn.log_subsection("Reset Samba Configuration")
    if fn.path.isfile(fn.samba_config + ".bak"):
        try:
            fn.shutil.copy(fn.samba_config + ".bak", fn.samba_config)
            fn.debug_print(f"Restored from backup: {fn.samba_config}.bak")
            fn.log_success("Samba configuration reset to original")
            fn.show_in_app_notification(self, "Original smb.conf is applied")
        except Exception as error:
            fn.log_error(f"Failed to reset samba configuration: {error}")
    else:
        fn.log_warn("No backup configuration file found")
        fn.debug_print(f"Missing: {fn.samba_config}.bak")
        fn.show_in_app_notification(self, "No backup configuration present")


def on_click_edit_samba_nano(self, _widget):
    fn.log_subsection("Edit Samba Configuration")
    try:
        fn.subprocess.Popen(
            ["alacritty", "-e", "nano", fn.samba_config],
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.PIPE,
        )
        fn.debug_print(f"File: {fn.samba_config}")
        fn.log_success("Samba configuration opened in nano editor")
        fn.show_in_app_notification(self, "Opening samba.conf in terminal with nano")
    except Exception as error:
        fn.log_error(f"Failed to open samba configuration: {error}")


def on_click_install_samba(self, _widget):
    def _wait(process):
        if process is None:
            return
        process.wait()
        GLib.idle_add(choose_smb_conf, self)
        GLib.idle_add(update_network_status, self)
    proc = fn.install_samba(self)
    fn.threading.Thread(target=_wait, args=(proc,), daemon=True).start()


def on_click_uninstall_samba(self, _widget):
    def _wait(process):
        if process is None:
            return
        process.wait()
        GLib.idle_add(update_network_status, self)
    proc = fn.uninstall_samba(self)
    fn.threading.Thread(target=_wait, args=(proc,), daemon=True).start()
