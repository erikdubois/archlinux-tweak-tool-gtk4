# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
from functions import GLib


def choose_nsswitch(self):
    """choose a nsswitch based on hosts: line"""
    choice = fn.get_combo_text(self.nsswitch_choices)

    # Map hosts: lines to config directories
    hosts_to_config = {
        "mymachines resolve [!UNAVAIL=return] files myhostname dns": ("arch", "Standard (no mdns)"),
        "mymachines resolve [!UNAVAIL=return] files dns mdns wins myhostname": ("arco", "With mdns + wins"),
        "mymachines mdns_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] files myhostname dns": ("biglinux", "With mdns_minimal"),
        "mymachines mdns4_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] files myhostname dns": ("manjaro", "With mdns4_minimal"),
        "files mymachines myhostname mdns_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] dns wins": ("garuda", "Custom order (no systemd)"),
    }

    if choice in hosts_to_config:
        label = hosts_to_config[choice][1]
        fn.debug_print(f"Applying nsswitch configuration: {label}")
        fn.copy_nsswitch(choice)
        fn.log_success(f"Nsswitch configuration applied: {label}")
        GLib.idle_add(fn.show_in_app_notification, self, f"Nsswitch: {label}")


def choose_smb_conf(self):
    """Apply the Easy samba configuration"""
    fn.debug_print("Applying Easy samba configuration")
    fn.copy_samba("example")
    fn.log_success("Easy samba configuration applied")
    GLib.idle_add(
        fn.show_in_app_notification, self, "Smb.conf easy configuration applied"
    )


def create_samba_user(self):
    """create a new user for samba"""

    username = fn.sudo_username

    if username:
        fn.log_subsection("Create Samba User")
        fn.install_package(self, "alacritty")
        fn.debug_print(f"Username: {username}")
        fn.debug_print("Samba uses a separate password from Linux user accounts")
        try:
            fn.subprocess.call(
                "alacritty -e /usr/bin/smbpasswd -a " + username,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            fn.log_success("Samba user created successfully")
            fn.show_in_app_notification(self, "Created a password for the current user")
        except Exception as error:
            fn.log_error(f"Failed to create samba user: {error}")
            fn.show_in_app_notification(self, f"Error creating samba user: {error}")


def add_autoconnect_pulseaudio(self):
    if fn.file_check(fn.pulse_default):
        if fn.check_content("load-module module-switch-on-connect\n", fn.pulse_default):
            fn.debug_print("We have already enabled your headset to autoconnect")
        else:
            try:
                with open(fn.pulse_default, "r", encoding="utf-8") as f:
                    lists = f.readlines()
                    f.close()

                lists.append("\nload-module module-switch-on-connect\n")

                with open(fn.pulse_default, "w", encoding="utf-8") as f:
                    f.writelines(lists)
                    f.close()
                fn.debug_print("We have added this line to /etc/pulse/default.pa")
                fn.debug_print("load-module module-switch-on-connect")
                fn.show_in_app_notification(
                    self, "Pulseaudio bluetooth autoconnection enabled"
                )
            except Exception as error:
                fn.log_error(str(error))


def restart_smb(self):
    """restart samba with detailed status checklist"""
    fn.log_subsection("SAMBA SERVICE RESTART - STATUS CHECKLIST")
    fn.debug_print(f"Configuration: {fn.samba_config}")

    smb_active = fn.check_service("smb")
    nmb_active = fn.check_service("nmb")
    avahi_active = fn.check_service("avahi-daemon")

    fn.debug_print(f"✓ Samba (smb):           {'✓ ACTIVE' if smb_active else '✗ INACTIVE'}")
    fn.debug_print(f"✓ NetBIOS (nmb):         {'✓ ACTIVE' if nmb_active else '✗ INACTIVE'}")
    fn.debug_print(f"✓ Avahi (discovery):     {'✓ ACTIVE' if avahi_active else '✗ INACTIVE'}")

    if smb_active:
        fn.debug_print("Restarting samba services...")
        fn.system("systemctl restart smb")
        if nmb_active:
            fn.system("systemctl restart nmb")
        fn.log_success("Samba services restarted successfully")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "✓ Samba restarted. Check other services in the status bar.",
        )
    else:
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


# ====================================================================
# SERVICES CALLBACKS
# ====================================================================

def on_click_switch_to_pulseaudio(self, widget):
    fn.log_subsection("Switch to PulseAudio")
    try:
        if fn.check_package_installed("pipewire-pulse"):
            fn.debug_print("Removing Pipewire packages")
            fn.remove_package_dd(self, "pipewire-pulse")
            fn.remove_package_dd(self, "wireplumber")

        fn.debug_print("Installing PulseAudio packages")
        fn.install_package(self, "pulseaudio")
        fn.install_package(self, "pulseaudio-bluetooth")
        fn.install_package(self, "pulseaudio-alsa")
        fn.install_package(self, "pavucontrol")
        fn.install_package(self, "alsa-utils")
        fn.install_package(self, "alsa-plugins")
        fn.install_package(self, "alsa-lib")
        fn.install_package(self, "alsa-firmware")
        fn.install_package(self, "gstreamer")
        fn.install_package(self, "gst-plugins-good")
        fn.install_package(self, "gst-plugins-bad")
        fn.install_package(self, "gst-plugins-base")
        fn.install_package(self, "gst-plugins-ugly")

        add_autoconnect_pulseaudio(self)
        fn.log_success("Switched to PulseAudio successfully")

    except Exception as error:
        fn.log_error(f"Failed to switch to PulseAudio: {error}")


def on_click_switch_to_pipewire(self, widget):
    fn.log_subsection("Switch to Pipewire")
    blueberry_installed = False

    try:
        if fn.check_package_installed("pulseaudio"):
            fn.debug_print("Removing PulseAudio packages")
            fn.remove_package_dd(self, "pulseaudio")
            fn.remove_package_dd(self, "pulseaudio-bluetooth")

        fn.debug_print("Installing Pipewire packages")
        fn.install_package(self, "pipewire")
        fn.install_package(self, "pipewire-pulse")
        fn.install_package(self, "pipewire-alsa")

        fn.install_package(self, "pavucontrol")

        fn.install_package(self, "alsa-utils")
        fn.install_package(self, "alsa-plugins")
        fn.install_package(self, "alsa-lib")
        fn.install_package(self, "alsa-firmware")
        fn.install_package(self, "gstreamer")
        fn.install_package(self, "gst-plugins-good")
        fn.install_package(self, "gst-plugins-bad")
        fn.install_package(self, "gst-plugins-base")
        fn.install_package(self, "gst-plugins-ugly")

        if blueberry_installed:
            fn.install_package(self, "blueberry")

        if fn.check_package_installed("pipewire-media-session"):
            fn.debug_print("Configuring wireplumber")
            fn.remove_package_dd(self, "pipewire-media-session")
            fn.install_package(self, "pipewire-pulse")
            fn.install_package(self, "wireplumber")

        fn.log_success("Switched to Pipewire successfully")

    except Exception as error:
        fn.log_error(f"Failed to switch to Pipewire: {error}")


def on_click_install_bluetooth(self, widget):
    fn.log_subsection("Install Bluetooth")
    try:
        fn.install_package(self, "bluez")
        fn.install_package(self, "bluez-utils")
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


def on_click_remove_bluetooth(self, widget):
    fn.log_subsection("Remove Bluetooth")
    try:
        fn.remove_package_dd(self, "bluez")
        fn.remove_package_dd(self, "bluez-utils")
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


def on_click_install_blueberry(self, widget):
    fn.log_subsection("Install Blueberry")
    try:
        fn.install_package(self, "blueberry")
        fn.log_success("Blueberry installed")
    except Exception as error:
        fn.log_error(f"Failed to install blueberry: {error}")


def on_click_remove_blueberry(self, widget):
    fn.log_subsection("Remove Blueberry")
    try:
        fn.remove_package(self, "blueberry")
        fn.log_success("Blueberry removed")
    except Exception as error:
        fn.log_error(f"Failed to remove blueberry: {error}")


def on_click_install_blueman(self, widget):
    fn.log_subsection("Install Blueman")
    try:
        fn.install_package(self, "blueman")
        fn.log_success("Blueman installed")
    except Exception as error:
        fn.log_error(f"Failed to install blueman: {error}")


def on_click_remove_blueman(self, widget):
    fn.log_subsection("Remove Blueman")
    try:
        fn.remove_package(self, "blueman")
        fn.log_success("Blueman removed")
    except Exception as error:
        fn.log_error(f"Failed to remove blueman: {error}")


def on_click_install_bluedevil(self, widget):
    fn.log_subsection("Install Bluedevil")
    try:
        fn.install_package(self, "bluedevil")
        fn.log_success("Bluedevil installed")
    except Exception as error:
        fn.log_error(f"Failed to install bluedevil: {error}")


def on_click_remove_bluedevil(self, widget):
    fn.log_subsection("Remove Bluedevil")
    try:
        fn.remove_package_s(self, "bluedevil")
        fn.log_success("Bluedevil removed")
    except Exception as error:
        fn.log_error(f"Failed to remove bluedevil: {error}")


def on_click_enable_bluetooth(self, widget):
    fn.log_subsection("Enable Bluetooth Service")
    try:
        fn.enable_service("bluetooth")
        fn.log_success("Bluetooth service enabled")
        fn.show_in_app_notification(self, "Bluetooth has been enabled")
    except Exception as error:
        fn.log_error(f"Failed to enable bluetooth: {error}")


def on_click_disable_bluetooth(self, widget):
    fn.log_subsection("Disable Bluetooth Service")
    try:
        fn.disable_service("bluetooth")
        fn.log_success("Bluetooth service disabled")
        fn.show_in_app_notification(self, "Bluetooth has been disabled")
    except Exception as error:
        fn.log_error(f"Failed to disable bluetooth: {error}")


def on_click_restart_bluetooth(self, widget):
    fn.log_subsection("Restart Bluetooth Service")
    try:
        fn.restart_service("bluetooth")
        fn.log_success("Bluetooth service restarted")
        fn.show_in_app_notification(self, "Bluetooth has been restarted")
    except Exception as error:
        fn.log_error(f"Failed to restart bluetooth: {error}")


def on_click_install_cups(self, widget):
    fn.log_subsection("Install CUPS")
    try:
        fn.install_package(self, "cups")
        fn.log_success("CUPS installed")
    except Exception as error:
        fn.log_error(f"Failed to install CUPS: {error}")


def on_click_remove_cups(self, widget):
    fn.log_subsection("Remove CUPS")
    try:
        fn.remove_package(self, "cups")
        fn.log_success("CUPS removed")
    except Exception as error:
        fn.log_error(f"Failed to remove CUPS: {error}")


def on_click_install_cups_pdf(self, widget):
    fn.log_subsection("Install CUPS PDF")
    try:
        fn.install_package(self, "cups-pdf")
        fn.log_success("CUPS PDF printer installed")
    except Exception as error:
        fn.log_error(f"Failed to install CUPS PDF: {error}")


def on_click_remove_cups_pdf(self, widget):
    fn.log_subsection("Remove CUPS PDF")
    try:
        fn.remove_package(self, "cups-pdf")
        fn.log_success("CUPS PDF printer removed")
    except Exception as error:
        fn.log_error(f"Failed to remove CUPS PDF: {error}")


def on_click_enable_cups(self, widget):
    fn.log_subsection("Enable CUPS Service")
    try:
        fn.enable_service("cups")
        fn.log_success("CUPS service enabled")
    except Exception as error:
        fn.log_error(f"Failed to enable CUPS: {error}")


def on_click_disable_cups(self, widget):
    fn.log_subsection("Disable CUPS Service")
    try:
        fn.disable_service("cups")
        fn.log_success("CUPS service disabled")
    except Exception as error:
        fn.log_error(f"Failed to disable CUPS: {error}")


def on_click_restart_cups(self, widget):
    fn.log_subsection("Restart CUPS Service")
    try:
        fn.restart_service("cups")
        fn.log_success("CUPS service restarted")
    except Exception as error:
        fn.log_error(f"Failed to restart CUPS: {error}")


def on_click_install_printer_drivers(self, widget):
    fn.log_subsection("Install Printer Drivers")
    try:
        packages = [
            "foomatic-db-engine", "foomatic-db", "foomatic-db-ppds",
            "foomatic-db-nonfree", "foomatic-db-nonfree-ppds",
            "gutenprint", "foomatic-db-gutenprint-ppds",
            "ghostscript", "gsfonts"
        ]
        for package in packages:
            fn.install_package(self, package)
        fn.debug_print(f"Installed {len(packages)} printer driver packages")
        fn.log_success("Printer drivers installed successfully")
    except Exception as error:
        fn.log_error(f"Failed to install printer drivers: {error}")


def on_click_remove_printer_drivers(self, widget):
    fn.log_subsection("Remove Printer Drivers")
    try:
        packages = [
            "foomatic-db-engine", "foomatic-db", "foomatic-db-ppds",
            "foomatic-db-nonfree", "foomatic-db-nonfree-ppds",
            "gutenprint", "foomatic-db-gutenprint-ppds",
            "ghostscript", "gsfonts"
        ]
        for package in packages:
            fn.remove_package(self, package)
        fn.debug_print(f"Removed {len(packages)} printer driver packages")
        fn.log_success("Printer drivers removed successfully")
    except Exception as error:
        fn.log_error(f"Failed to remove printer drivers: {error}")


def on_click_install_hplip(self, widget):
    fn.log_subsection("Install HPLIP")
    try:
        fn.install_package(self, "hplip")
        fn.log_success("HPLIP installed")
    except Exception as error:
        fn.log_error(f"Failed to install HPLIP: {error}")


def on_click_remove_hplip(self, widget):
    fn.log_subsection("Remove HPLIP")
    try:
        fn.remove_package(self, "hplip")
        fn.log_success("HPLIP removed")
    except Exception as error:
        fn.log_error(f"Failed to remove HPLIP: {error}")


def on_click_install_system_config_printer(self, widget):
    fn.log_subsection("Install System Config Printer")
    try:
        fn.install_package(self, "system-config-printer")
        fn.log_success("System Config Printer installed")
    except Exception as error:
        fn.log_error(f"Failed to install system-config-printer: {error}")


def on_click_remove_system_config_printer(self, widget):
    fn.log_subsection("Remove System Config Printer")
    try:
        fn.remove_package(self, "system-config-printer")
        fn.log_success("System Config Printer removed")
    except Exception as error:
        fn.log_error(f"Failed to remove system-config-printer: {error}")


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


def on_install_discovery_clicked(self, widget):
    fn.log_subsection("Install Network Discovery")
    try:
        fn.install_discovery(self)
        fn.debug_print("Network discovery packages installed")
        update_network_status(self)
        fn.log_success("Network discovery installed successfully")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Network discovery is installed - a good nsswitch_config is needed",
        )
    except Exception as error:
        fn.log_error(f"Failed to install network discovery: {error}")


def on_remove_discovery_clicked(self, widget):
    fn.log_subsection("Remove Network Discovery")
    try:
        fn.remove_discovery(self)
        fn.debug_print("Network discovery packages removed")
        update_network_status(self)
        fn.log_success("Network discovery removed successfully")
        GLib.idle_add(fn.show_in_app_notification, self, "Network discovery is removed")
    except Exception as error:
        fn.log_error(f"Failed to remove network discovery: {error}")


def on_click_reset_nsswitch(self, widget):
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


def on_click_edit_nsswitch(self, widget):
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


def on_click_apply_nsswitch(self, widget):
    choose_nsswitch(self)


def on_click_create_samba_user(self, widget):
    create_samba_user(self)


def on_click_restart_smb(self, widget):
    restart_smb(self)
    update_network_status(self)


def on_click_save_samba_share(self, widget):
    fn.log_subsection("Save Samba Share Configuration")
    try:
        fn.save_samba_config(self)
        fn.log_success("Samba share configuration saved")
    except Exception as error:
        fn.log_error(f"Failed to save samba configuration: {error}")


def on_click_install_arco_thunar_plugin(self, widget):
    fn.install_arco_thunar_plugin(self, widget)


def on_click_apply_samba(self, widget):
    fn.log_subsection("Apply Samba Configuration")
    try:
        choose_smb_conf(self)
        fn.debug_print("Samba configuration applied from selected template")
        fn.log_success("Samba configuration applied successfully")
        fn.show_in_app_notification(self, "Samba configuration applied")
    except Exception as error:
        fn.log_error(f"Failed to apply samba configuration: {error}")


def on_click_reset_samba(self, widget):
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


def on_click_edit_samba_nano(self, widget):
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


def on_click_install_samba(self, widget):
    fn.log_subsection("Install Samba")
    try:
        fn.debug_print("Installing samba package")
        fn.install_samba(self)
        fn.debug_print("Samba package installed successfully")
        fn.debug_print("Applying Easy configuration with automatic Shared folder setup")
        choose_smb_conf(self)
        fn.debug_print("Easy configuration applied")
        update_network_status(self)
        fn.log_success("Samba installed with Easy configuration")
        fn.show_in_app_notification(
            self, "Samba installed with Easy configuration. Restart smb to apply."
        )
    except Exception as error:
        fn.log_error(f"Failed to install samba: {error}")


def on_click_uninstall_samba(self, widget):
    fn.log_subsection("Uninstall Samba")
    try:
        fn.debug_print("Uninstalling samba package")
        fn.uninstall_samba(self)
        fn.debug_print("Samba package uninstalled successfully")
        update_network_status(self)
        fn.log_success("Samba uninstalled")
        fn.show_in_app_notification(self, "Samba has been uninstalled")
    except Exception as error:
        fn.log_error(f"Failed to uninstall samba: {error}")
