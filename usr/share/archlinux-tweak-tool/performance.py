# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
from functions import GLib


# ============================================================
# Tuned Configuration
# ============================================================
TUNED_PACKAGE = "tuned"
TUNED_PPD_PACKAGE = "tuned-ppd"
TLP_PACKAGE = "tlp"
tuned_ppd_config = "/etc/tuned/ppd.conf"

# ============================================================
# Other Features Configuration
# ============================================================
zram_config = "/etc/systemd/zram-generator.conf"
zram_disk_size = "/sys/block/zram0/disksize"
zram_enable_script = "/usr/share/archlinux-tweak-tool/data/any/enable-zram"
zram_disable_script = "/usr/share/archlinux-tweak-tool/data/any/disable-zram"
swapfile_create_script = "/usr/share/archlinux-tweak-tool/data/any/create-swapfile"
swapfile_remove_script = "/usr/share/archlinux-tweak-tool/data/any/remove-swapfile"
fstrim_timer = "fstrim.timer"
fstrim_service = "fstrim.service"


# ============================================================
# Helper Functions (Service Status)
# ============================================================

def get_service_status(service):
    """Return a status label that includes enabled oneshot services."""
    if fn.check_service(service):
        return "<b>enabled</b>"

    try:
        output = fn.subprocess.run(
            ["systemctl", "is-enabled", service + ".service"],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        status = output.stdout.decode().strip()
        if status == "enabled":
            return "<b>enabled</b>"
        if status:
            return status
    except Exception as error:
        print(error)

    return "disabled"


def get_tuned_status_markup():
    """Build the tuned block status label text."""
    tuned_status = get_service_status("tuned")
    tuned_ppd_status = get_service_status("tuned-ppd")
    return (
        "Tuned service : "
        + tuned_status
        + "   Tuned-PPD service : "
        + tuned_ppd_status
    )


def refresh_tuned_status_label(self):
    """Refresh the visible tuned status labels."""
    if hasattr(self, "tuned_status_label"):
        GLib.idle_add(
            self.tuned_status_label.set_markup,
            "tuned service : " + get_service_status("tuned"),
        )
    if hasattr(self, "tuned_ppd_status_label"):
        GLib.idle_add(
            self.tuned_ppd_status_label.set_markup,
            "tuned-ppd service : " + get_service_status("tuned-ppd"),
        )


def get_performance_status_markup():
    """Build the combined service status label text."""
    return get_tuned_status_markup()


def refresh_performance_status_label(self):
    """Refresh the visible performance service status label."""
    refresh_tuned_status_label(self)
    if hasattr(self, "performance_status_label"):
        GLib.idle_add(
            self.performance_status_label.set_markup,
            get_performance_status_markup(),
        )


# ============================================================
# Tuned Block (includes Tuned and Tuned-PPD)
# ============================================================

def install_tuned_tools(widget, self):
    """Install tuned for dynamic power management."""
    fn.log_subsection("Install Tuned")
    try:
        conflicting_files = [
            "/etc/modprobe.d/tuned.conf",
        ]
        for file_path in conflicting_files:
            if fn.path.exists(file_path):
                try:
                    fn.debug_print(f"Removing conflicting file: {file_path}")
                    fn.unlink(file_path)
                except Exception as e:
                    fn.log_warn(f"Could not remove {file_path}: {e}")

        remove_power_profiles_daemon_if_present(self)
        fn.debug_print("Installing tuned and tuned-ppd packages")
        fn.install_package(self, TUNED_PACKAGE + " " + TUNED_PPD_PACKAGE)
        disable_tlp_if_present(self)
        fn.log_success("Tuned installed successfully")
        GLib.timeout_add(500, refresh_tuned_buttons, self)
        GLib.timeout_add(500, refresh_tuned_profile_choices, self)
        GLib.timeout_add(500, refresh_tuned_status_label, self)
        GLib.idle_add(fn.show_in_app_notification, self, "Tuned has been installed")
    except Exception as error:
        fn.log_error(f"Failed to install tuned: {error}")


def remove_tuned_tools(widget, self):
    """Remove tuned and tuned-ppd."""
    fn.log_subsection("Remove Tuned")
    try:
        fn.debug_print("Disabling tuned services before removal")
        fn.disable_service("tuned")
        fn.disable_service("tuned-ppd")
        fn.remove_package(self, TUNED_PACKAGE + " " + TUNED_PPD_PACKAGE)
        fn.log_success("Tuned removed successfully")
        GLib.idle_add(refresh_tuned_buttons, self)
        GLib.idle_add(refresh_tuned_profile_status, self)
        GLib.idle_add(refresh_tuned_status_label, self)
    except Exception as error:
        fn.log_error(f"Failed to remove tuned: {error}")


def refresh_tuned_buttons(self):
    """Refresh tuned button sensitivity after installing or removing."""
    tuned_buttons = [
        "enable_tuned",
        "disable_tuned",
        "restart_tuned",
        "restart_tuned_ppd",
        "tuned_profile_choices",
        "btn_apply_tuned_profile",
    ]
    # Check for the main tuned package - if installed, buttons should be enabled
    installed = fn.check_package_installed("tuned")
    for button_name in tuned_buttons:
        if hasattr(self, button_name):
            GLib.idle_add(getattr(self, button_name).set_sensitive, installed)


def remove_power_profiles_daemon_if_present(self):
    """power-profiles-daemon conflicts with tuned-ppd and must be removed first."""
    if not fn.check_package_installed("power-profiles-daemon"):
        return
    print("power-profiles-daemon is installed - removing before installing tuned-ppd")
    fn.disable_service("power-profiles-daemon")
    fn.remove_package(self, "power-profiles-daemon")
    GLib.idle_add(
        fn.show_in_app_notification,
        self,
        "power-profiles-daemon removed (conflicts with tuned-ppd)",
    )


def disable_tlp_if_present(self):
    """Tuned and TLP should not manage power settings at the same time."""
    if not fn.check_package_installed(TLP_PACKAGE):
        return

    print("TLP is installed - disabling tlp service before using tuned")
    fn.disable_service("tlp")
    refresh_performance_status_label(self)
    GLib.idle_add(
        fn.show_in_app_notification,
        self,
        "TLP service disabled because it conflicts with Tuned",
    )


def enable_tuned_services(widget, self):
    fn.log_subsection("Enable Tuned Services")
    try:
        disable_tlp_if_present(self)
        fn.debug_print("Enabling tuned and tuned-ppd services")
        fn.enable_service("tuned")
        fn.enable_service("tuned-ppd")
        fn.log_success("Tuned and Tuned-PPD enabled successfully")
        GLib.timeout_add(500, refresh_tuned_status_label, self)
        GLib.idle_add(fn.show_in_app_notification, self, "Tuned and Tuned-PPD have been enabled and started")
    except Exception as error:
        fn.log_error(f"Failed to enable tuned services: {error}")


def disable_tuned_services(widget, self):
    fn.log_subsection("Disable Tuned Services")
    try:
        fn.debug_print("Disabling tuned and tuned-ppd services")
        fn.disable_service("tuned")
        fn.disable_service("tuned-ppd")
        fn.log_success("Tuned and Tuned-PPD disabled successfully")
        GLib.timeout_add(500, refresh_tuned_status_label, self)
        GLib.idle_add(fn.show_in_app_notification, self, "Tuned and Tuned-PPD have been disabled and stopped")
    except Exception as error:
        fn.log_error(f"Failed to disable tuned services: {error}")


def restart_tuned_service(widget, self):
    fn.log_subsection("Restart Tuned Service")
    try:
        fn.restart_service("tuned")
        fn.log_success("Tuned service restarted")
        GLib.timeout_add(500, refresh_performance_status_label, self)
        GLib.idle_add(fn.show_in_app_notification, self, "Tuned has been restarted")
    except Exception as error:
        fn.log_error(f"Failed to restart tuned: {error}")


def restart_tuned_ppd_service(widget, self):
    fn.log_subsection("Restart Tuned-PPD Service")
    try:
        fn.restart_service("tuned-ppd")
        fn.log_success("Tuned-PPD service restarted")
        GLib.timeout_add(500, refresh_performance_status_label, self)
        GLib.idle_add(fn.show_in_app_notification, self, "Tuned-PPD has been restarted")
    except Exception as error:
        fn.log_error(f"Failed to restart tuned-ppd: {error}")


# ============================================================
# Tuned Profiles Management
# ============================================================

def get_available_tuned_profiles():
    """Return list of available tuned profiles."""
    if not fn.check_package_installed("tuned"):
        return []

    try:
        result = fn.subprocess.run(
            ["tuned-adm", "list"],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        if result.returncode == 0:
            output = result.stdout.decode().strip()
            # Parse output: "Available profiles:" followed by profile names
            lines = output.split('\n')
            profiles = []
            found_available = False
            for line in lines:
                if "Available profiles:" in line:
                    found_available = True
                    continue
                if found_available and line.strip():
                    # Format: "- profile-name    - description"
                    # Extract profile name (the word after the leading dash, before description dash)
                    line = line.strip()
                    if line.startswith("- "):
                        line = line[2:].strip()  # Remove leading "- "
                        # Split on whitespace and take first token (profile name)
                        profile_name = line.split()[0] if line.split() else ""
                        if profile_name:
                            profiles.append(profile_name)
            return profiles
    except Exception as error:
        print(f"Error getting tuned profiles: {error}")
    return []


def get_active_tuned_profile():
    """Return the currently active tuned profile."""
    if not fn.check_package_installed("tuned"):
        return None

    try:
        result = fn.subprocess.run(
            ["tuned-adm", "active"],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        if result.returncode == 0:
            output = result.stdout.decode().strip()
            # Output format: "Current active profile: <profile_name>"
            if "Current active profile:" in output:
                profile = output.split("Current active profile:")[-1].strip()
                return profile
    except Exception as error:
        print(f"Error getting active tuned profile: {error}")
    return None


def get_tuned_profile_status_markup():
    """Build the tuned profile status label text."""
    active_profile = get_active_tuned_profile()
    tuned_enabled = get_service_status("tuned")

    if active_profile:
        status_text = f"Active profile: <b>{active_profile}</b> ({tuned_enabled})"
    else:
        status_text = "No active profile"

    return status_text


def refresh_tuned_profile_status(self):
    """Refresh the visible tuned profile status label."""
    if hasattr(self, "tuned_profile_status_label"):
        GLib.idle_add(
            self.tuned_profile_status_label.set_markup,
            get_tuned_profile_status_markup(),
        )


def refresh_tuned_profile_choices(self):
    """Refresh the tuned profile dropdown with available profiles."""
    if not hasattr(self, "tuned_profile_choices"):
        return

    try:
        import gi
        gi.require_version("Gtk", "4.0")
        from gi.repository import Gtk

        tuned_profile_choices = get_available_tuned_profiles()
        if tuned_profile_choices:
            # Create a new dropdown with updated profiles
            new_dropdown = Gtk.DropDown.new_from_strings(tuned_profile_choices)
            new_dropdown.set_margin_start(10)
            new_dropdown.set_margin_end(10)

            # Set the currently active profile if available
            active_profile = get_active_tuned_profile()
            if active_profile and active_profile in tuned_profile_choices:
                new_dropdown.set_selected(tuned_profile_choices.index(active_profile))

            # Replace the old dropdown in the parent container
            def update_dropdown():
                parent = self.tuned_profile_choices.get_parent()
                if parent:
                    parent.remove(self.tuned_profile_choices)
                    parent.append(new_dropdown)
                    self.tuned_profile_choices = new_dropdown

            GLib.idle_add(update_dropdown)
    except Exception as e:
        print(f"Error refreshing tuned profile choices: {e}")


def apply_tuned_profile(widget, self):
    """Apply the selected tuned profile."""
    choice = fn.get_combo_text(self.tuned_profile_choices)

    if not choice:
        print("No profile selected")
        GLib.idle_add(fn.show_in_app_notification, self, "No profile selected")
        return

    set_tuned_profile(self, choice)


def set_tuned_profile(self, profile_name):
    """Set and enable a tuned profile."""
    fn.log_subsection("Apply Tuned Profile")
    try:
        if not fn.check_package_installed("tuned"):
            fn.debug_print("Installing tuned package")
            fn.install_package(self, "tuned")

        if fn.shutil.which("tuned-adm") is None:
            fn.log_error("tuned-adm is not installed")
            GLib.idle_add(fn.show_in_app_notification, self, "tuned-adm is not installed")
            return

        fn.debug_print("Starting tuned service")
        fn.enable_service("tuned")
        fn.restart_service("tuned")

        fn.debug_print(f"Applying profile: {profile_name}")
        result = fn.subprocess.run(
            ["tuned-adm", "profile", profile_name],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        if result.returncode != 0:
            fn.log_error(f"Could not set tuned profile to {profile_name}")
            GLib.idle_add(
                fn.show_in_app_notification, self, f"Could not set tuned profile to {profile_name}"
            )
            return

        refresh_performance_status_label(self)
        refresh_tuned_profile_status(self)
        fn.log_success(f"Tuned profile set to {profile_name}")
        GLib.idle_add(
            fn.show_in_app_notification, self, f"Tuned profile set to {profile_name}"
        )
    except Exception as error:
        fn.log_error(f"Failed to set tuned profile: {error}")
        GLib.idle_add(fn.show_in_app_notification, self, "Could not set tuned profile")


def get_service_status(service):
    """Return a status label that includes enabled oneshot services."""
    if fn.check_service(service):
        return "<b>enabled</b>"

    try:
        output = fn.subprocess.run(
            ["systemctl", "is-enabled", service + ".service"],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        status = output.stdout.decode().strip()
        if status == "enabled":
            return "<b>enabled</b>"
        if status:
            return status
    except Exception as error:
        print(error)

    return "disabled"


def refresh_performance_status_label(self):
    """Refresh the visible performance service status label."""
    if hasattr(self, "performance_status_label"):
        GLib.idle_add(
            self.performance_status_label.set_markup,
            get_performance_status_markup(),
        )


def get_zram_size_label():
    """Return the current zram size in GB, or its configured expression."""
    try:
        if fn.path.isfile(zram_disk_size):
            with open(zram_disk_size, "r", encoding="utf-8") as f:
                size_bytes = int(f.read().strip())
            return format(size_bytes / 1024 / 1024 / 1024, ".2f") + " GB"

        if fn.path.isfile(zram_config):
            with open(zram_config, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if line.strip().startswith("zram-size"):
                        return line.split("=", 1)[1].strip()
    except Exception as error:
        print(error)

    return ""


def get_zram_status_markup():
    """Build the zram status label text."""
    zram_status = (
        "<b>enabled</b>" if fn.check_service("systemd-zram-setup@zram0") else "disabled"
    )
    zram_size = get_zram_size_label()
    if zram_size:
        zram_status = zram_status + " (" + zram_size + ")"
    return (
        "Enable zram compressed RAM swap - installs zram-generator\n"
        "ZRAM service : " + zram_status
    )


def refresh_zram_status_label(self):
    """Refresh the visible zram status label."""
    if hasattr(self, "zram_status_label"):
        GLib.idle_add(self.zram_status_label.set_markup, get_zram_status_markup())


def get_unit_state(unit, command):
    """Return a systemd unit state for services, timers, and other unit types."""
    try:
        output = fn.subprocess.run(
            ["systemctl", command, unit],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        status = output.stdout.decode().strip()
        if status:
            return status
    except Exception as error:
        print(error)

    return "unknown"


def get_fstrim_status_markup():
    """Build the fstrim timer status label text."""
    active_status = get_unit_state(fstrim_timer, "is-active")
    enabled_status = get_unit_state(fstrim_timer, "is-enabled")

    if active_status == "active":
        active_status = "<b>active</b>"

    if enabled_status == "enabled":
        enabled_status = "<b>enabled</b>"

    return (
        "Enable weekly TRIM for SSD/NVMe drives with fstrim.timer\n"
        "fstrim.timer : " + active_status + " / " + enabled_status
    )


def refresh_fstrim_status_label(self):
    """Refresh the visible fstrim timer status label."""
    if hasattr(self, "fstrim_status_label"):
        GLib.idle_add(self.fstrim_status_label.set_markup, get_fstrim_status_markup())


def get_irqbalance_status_markup():
    """Build the irqbalance service status label text."""
    irqbalance_status = get_service_status("irqbalance")
    return (
        "Balance hardware interrupts across CPUs\n"
        "irqbalance service : " + irqbalance_status
    )


def refresh_irqbalance_status_label(self):
    """Refresh the visible irqbalance status label."""
    if hasattr(self, "irqbalance_status_label"):
        GLib.idle_add(
            self.irqbalance_status_label.set_markup,
            get_irqbalance_status_markup(),
        )


def refresh_irqbalance_package_label(self):
    """Refresh the visible irqbalance package status label."""
    if not hasattr(self, "irqbalance_package_label"):
        return

    if fn.check_package_installed("irqbalance"):
        GLib.idle_add(
            self.irqbalance_package_label.set_markup,
            "irqbalance package is <b>installed</b>",
        )
    else:
        GLib.idle_add(self.irqbalance_package_label.set_text, "Install irqbalance")


def refresh_irqbalance_service_buttons(self):
    """Refresh irqbalance button sensitivity after installing or removing it."""
    installed = fn.check_package_installed("irqbalance")
    for button_name in [
        "enable_irqbalance",
        "disable_irqbalance",
    ]:
        if hasattr(self, button_name):
            GLib.idle_add(getattr(self, button_name).set_sensitive, installed)


def disable_tlp_if_present(self):
    """Tuned and TLP should not manage power settings at the same time."""
    if not fn.check_package_installed(TLP_PACKAGE):
        return

    print("TLP is installed - disabling tlp service before using tuned")
    fn.disable_service("tlp")
    refresh_performance_status_label(self)
    GLib.idle_add(
        fn.show_in_app_notification,
        self,
        "TLP service disabled because it conflicts with Tuned",
    )


def enable_zram(widget, self):
    """Enable zram with the selected compressed swap size."""
    fn.log_subsection("Enable zram")
    try:
        fn.install_package(self, "alacritty")
        size = fn.get_combo_text(self.zram_size)
        fn.debug_print(f"Enabling zram with size: {size}")
        fn.subprocess.call(
            ["alacritty", "--hold", "-e", zram_enable_script, size],
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        fn.log_success(f"zram enabled ({size})")
        refresh_zram_status_label(self)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "zram enabled (" + size + ")",
        )
    except Exception as error:
        fn.log_error(f"Failed to enable zram: {error}")


def disable_zram(widget, self):
    """Disable zram."""
    fn.log_subsection("Disable zram")
    try:
        fn.install_package(self, "alacritty")
        fn.debug_print("Disabling zram")
        fn.subprocess.call(
            ["alacritty", "--hold", "-e", zram_disable_script],
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        fn.log_success("zram disabled")
        refresh_zram_status_label(self)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "zram disabled",
        )
    except Exception as error:
        fn.log_error(f"Failed to disable zram: {error}")


def get_root_filesystem_type():
    """Return the filesystem type of the root partition."""
    try:
        with open("/proc/mounts", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 3 and parts[1] == "/":
                    return parts[2]
    except Exception as error:
        print(error)
    return ""


def get_swapfile_size_label():
    """Return the current swapfile size in GB if /swapfile exists."""
    try:
        if fn.path.isfile("/swapfile"):
            size_bytes = fn.path.getsize("/swapfile")
            return format(size_bytes / 1024 / 1024 / 1024, ".0f") + " GB"
    except Exception as error:
        print(error)
    return None


def refresh_swapfile_label(self):
    """Refresh the swapfile label with current size."""
    if not hasattr(self, "swapfile_label"):
        return
    size = get_swapfile_size_label()
    if size:
        GLib.idle_add(
            self.swapfile_label.set_markup,
            "Create or manage a swapfile at /swapfile - " + size + " <b>present</b>",
        )
    else:
        GLib.idle_add(
            self.swapfile_label.set_text,
            "Create or manage a swapfile at /swapfile",
        )


def create_swapfile(widget, self):
    """Create a swapfile with the selected size."""
    fn.log_subsection("Create Swapfile")
    try:
        fn.install_package(self, "alacritty")
        size = fn.get_combo_text(self.swapfile_size)
        fn.debug_print(f"Creating swapfile with size: {size}")
        fn.subprocess.call(
            ["alacritty", "--hold", "-e", swapfile_create_script, size],
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        fn.log_success(f"Swapfile ({size}) created at /swapfile")
        GLib.idle_add(refresh_swapfile_label, self)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Swapfile (" + size + ") created at /swapfile",
        )
    except Exception as error:
        fn.log_error(f"Failed to create swapfile: {error}")


def remove_swapfile(widget, self):
    """Remove the swapfile."""
    fn.log_subsection("Remove Swapfile")
    try:
        fn.install_package(self, "alacritty")
        fn.debug_print("Removing swapfile at /swapfile")
        fn.subprocess.call(
            ["alacritty", "--hold", "-e", swapfile_remove_script],
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        fn.log_success("Swapfile removed")
        GLib.idle_add(refresh_swapfile_label, self)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Swapfile removed",
        )
    except Exception as error:
        fn.log_error(f"Failed to remove swapfile: {error}")


def enable_fstrim_timer(widget, self):
    """Enable the weekly fstrim timer."""
    fn.log_subsection("Enable fstrim Timer")
    try:
        fn.subprocess.call(
            ["systemctl", "enable", "--now", fstrim_timer],
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        fn.log_success("fstrim.timer enabled for weekly TRIM")
        refresh_fstrim_status_label(self)
        GLib.idle_add(fn.show_in_app_notification, self, "fstrim.timer enabled")
    except Exception as error:
        fn.log_error(f"Failed to enable fstrim.timer: {error}")


def disable_fstrim_timer(widget, self):
    """Disable the weekly fstrim timer."""
    fn.log_subsection("Disable fstrim Timer")
    try:
        fn.subprocess.call(
            ["systemctl", "disable", "--now", fstrim_timer],
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        fn.log_success("fstrim.timer disabled")
        refresh_fstrim_status_label(self)
        GLib.idle_add(fn.show_in_app_notification, self, "fstrim.timer disabled")
    except Exception as error:
        fn.log_error(f"Failed to disable fstrim.timer: {error}")


def run_fstrim_now(widget, self):
    """Run fstrim once through the systemd service."""
    fn.log_subsection("Run fstrim Now")
    try:
        fn.debug_print("Starting fstrim.service for immediate TRIM")
        result = fn.subprocess.run(
            ["systemctl", "start", fstrim_service],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        if result.returncode == 0:
            fn.log_success("TRIM operation started")
            GLib.idle_add(fn.show_in_app_notification, self, "TRIM run started")
        else:
            fn.log_error(f"Failed to run TRIM: {result.stdout.decode().strip()}")
            GLib.idle_add(fn.show_in_app_notification, self, "Could not run TRIM")

        refresh_fstrim_status_label(self)
    except Exception as error:
        fn.log_error(f"Failed to run fstrim: {error}")
        GLib.idle_add(fn.show_in_app_notification, self, "Could not run TRIM")


def install_irqbalance(widget, self):
    """Install irqbalance."""
    fn.log_subsection("Install irqbalance")
    try:
        fn.install_package(self, "irqbalance")
        fn.log_success("irqbalance installed")
        GLib.timeout_add(500, refresh_irqbalance_package_label, self)
        GLib.timeout_add(500, refresh_irqbalance_service_buttons, self)
        GLib.timeout_add(500, refresh_irqbalance_status_label, self)
    except Exception as error:
        fn.log_error(f"Failed to install irqbalance: {error}")


def remove_irqbalance(widget, self):
    """Remove irqbalance."""
    fn.log_subsection("Remove irqbalance")
    try:
        fn.disable_service("irqbalance")
        fn.remove_package(self, "irqbalance")
        fn.log_success("irqbalance removed")
        GLib.timeout_add(500, refresh_irqbalance_package_label, self)
        GLib.timeout_add(500, refresh_irqbalance_service_buttons, self)
        GLib.timeout_add(500, refresh_irqbalance_status_label, self)
    except Exception as error:
        fn.log_error(f"Failed to remove irqbalance: {error}")


def enable_irqbalance_service(widget, self):
    fn.log_subsection("Enable irqbalance Service")
    try:
        fn.enable_service("irqbalance")
        fn.log_success("irqbalance service enabled")
        GLib.timeout_add(500, refresh_irqbalance_status_label, self)
        GLib.idle_add(fn.show_in_app_notification, self, "irqbalance has been enabled and started")
    except Exception as error:
        fn.log_error(f"Failed to enable irqbalance: {error}")


def disable_irqbalance_service(widget, self):
    fn.log_subsection("Disable irqbalance Service")
    try:
        fn.disable_service("irqbalance")
        fn.log_success("irqbalance service disabled")
        GLib.timeout_add(500, refresh_irqbalance_status_label, self)
        GLib.idle_add(fn.show_in_app_notification, self, "irqbalance has been disabled and stopped")
    except Exception as error:
        fn.log_error(f"Failed to disable irqbalance: {error}")


# ============================================================
# Ananicy Block
# ============================================================

ANANICY_PACKAGE = "ananicy-cpp"
ANANICY_RULES_PACKAGE = "cachyos-ananicy-rules-git"


def get_ananicy_status_markup():
    """Build the ananicy-cpp service status label text."""
    ananicy_status = get_service_status("ananicy-cpp")
    return (
        "Auto nice daemon for CPU and I/O scheduling\n"
        "ananicy-cpp service : " + ananicy_status
    )


def refresh_ananicy_status_label(self):
    """Refresh the visible ananicy status label."""
    if hasattr(self, "ananicy_status_label"):
        GLib.idle_add(
            self.ananicy_status_label.set_markup,
            get_ananicy_status_markup(),
        )


def refresh_ananicy_package_label(self):
    """Refresh the ananicy package status label."""
    if not hasattr(self, "ananicy_package_label"):
        return

    ananicy_installed = fn.check_package_installed(ANANICY_PACKAGE)
    rules_installed = fn.check_package_installed(ANANICY_RULES_PACKAGE)

    if ananicy_installed and rules_installed:
        GLib.idle_add(
            self.ananicy_package_label.set_markup,
            "ananicy-cpp and cachyos-ananicy-rules-git are <b>installed</b>",
        )
    elif ananicy_installed:
        GLib.idle_add(
            self.ananicy_package_label.set_markup,
            "ananicy-cpp is <b>installed</b> (cachyos-ananicy-rules-git not installed)",
        )
    else:
        GLib.idle_add(
            self.ananicy_package_label.set_text,
            "Install ananicy-cpp and cachyos-ananicy-rules-git",
        )


def refresh_ananicy_service_buttons(self):
    """Refresh ananicy button sensitivity after installing or removing it."""
    installed = fn.check_package_installed(ANANICY_PACKAGE)
    for button_name in ["enable_ananicy", "disable_ananicy"]:
        if hasattr(self, button_name):
            GLib.idle_add(getattr(self, button_name).set_sensitive, installed)


def install_ananicy(widget, self):
    """Install ananicy-cpp and cachyos-ananicy-rules-git."""
    fn.log_subsection("Install ananicy")
    try:
        fn.install_package(self, ANANICY_PACKAGE + " " + ANANICY_RULES_PACKAGE)
        fn.log_success("ananicy-cpp and cachyos-ananicy-rules-git installed")
        refresh_ananicy_package_label(self)
        refresh_ananicy_service_buttons(self)
        refresh_ananicy_status_label(self)
    except Exception as error:
        fn.log_error(f"Failed to install ananicy: {error}")


def remove_ananicy(widget, self):
    """Remove ananicy-cpp and cachyos-ananicy-rules-git."""
    fn.log_subsection("Remove ananicy")
    try:
        fn.disable_service(ANANICY_PACKAGE)
        fn.remove_package(self, ANANICY_PACKAGE + " " + ANANICY_RULES_PACKAGE)
        fn.log_success("ananicy-cpp and cachyos-ananicy-rules-git removed")
        refresh_ananicy_package_label(self)
        refresh_ananicy_service_buttons(self)
        refresh_ananicy_status_label(self)
    except Exception as error:
        fn.log_error(f"Failed to remove ananicy: {error}")


def enable_ananicy_service(widget, self):
    fn.log_subsection("Enable ananicy Service")
    try:
        fn.enable_service(ANANICY_PACKAGE)
        fn.log_success("ananicy-cpp service enabled")
        GLib.timeout_add(500, refresh_ananicy_status_label, self)
        GLib.idle_add(fn.show_in_app_notification, self, "ananicy-cpp has been enabled and started")
    except Exception as error:
        fn.log_error(f"Failed to enable ananicy: {error}")


def disable_ananicy_service(widget, self):
    fn.log_subsection("Disable ananicy Service")
    try:
        fn.disable_service(ANANICY_PACKAGE)
        fn.log_success("ananicy-cpp service disabled")
        GLib.timeout_add(500, refresh_ananicy_status_label, self)
        GLib.idle_add(fn.show_in_app_notification, self, "ananicy-cpp has been disabled and stopped")
    except Exception as error:
        fn.log_error(f"Failed to disable ananicy: {error}")


# ============================================================
# GameMode Block
# ============================================================

GAMEMODE_PACKAGE = "gamemode"


def get_real_user():
    """Return the real (non-root) username running the app."""
    import os
    import pwd
    pkexec_uid = os.environ.get("PKEXEC_UID")
    if pkexec_uid:
        try:
            return pwd.getpwuid(int(pkexec_uid)).pw_name
        except Exception:
            pass
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        return sudo_user
    try:
        return fn.subprocess.run(
            ["logname"],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        ).stdout.decode().strip()
    except Exception:
        pass
    return None


def get_gamemoded_user_status():
    """Check gamemoded user service status via --machine flag."""
    real_user = get_real_user()
    if not real_user:
        return "disabled"
    try:
        output = fn.subprocess.run(
            ["systemctl", "--user", f"--machine={real_user}@.host", "is-enabled", "gamemoded.service"],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        status = output.stdout.decode().strip()
        if status == "enabled":
            return "<b>enabled</b>"
    except Exception as error:
        print(error)
    return "disabled"


def get_gamemode_status_markup():
    """Build the gamemode service status label text."""
    gamemode_status = get_gamemoded_user_status()
    return (
        "Optimize system performance for gaming\n"
        "gamemoded service : " + gamemode_status
    )


def refresh_gamemode_status_label(self):
    """Refresh the visible gamemode status label."""
    if hasattr(self, "gamemode_status_label"):
        GLib.idle_add(
            self.gamemode_status_label.set_markup,
            get_gamemode_status_markup(),
        )


def refresh_gamemode_package_label(self):
    """Refresh the gamemode package status label."""
    if not hasattr(self, "gamemode_package_label"):
        return

    if fn.check_package_installed(GAMEMODE_PACKAGE):
        GLib.idle_add(
            self.gamemode_package_label.set_markup,
            "gamemode package is <b>installed</b>",
        )
    else:
        GLib.idle_add(
            self.gamemode_package_label.set_text,
            "Install gamemode",
        )


def refresh_gamemode_service_buttons(self):
    """Refresh gamemode button sensitivity after installing or removing it."""
    installed = fn.check_package_installed(GAMEMODE_PACKAGE)
    for button_name in ["enable_gamemode", "disable_gamemode"]:
        if hasattr(self, button_name):
            GLib.idle_add(getattr(self, button_name).set_sensitive, installed)


def install_gamemode(widget, self):
    """Install gamemode."""
    fn.log_subsection("Install gamemode")
    try:
        fn.install_package(self, GAMEMODE_PACKAGE)
        fn.log_success("gamemode installed")
        refresh_gamemode_package_label(self)
        refresh_gamemode_service_buttons(self)
        refresh_gamemode_status_label(self)
    except Exception as error:
        fn.log_error(f"Failed to install gamemode: {error}")


def remove_gamemode(widget, self):
    """Remove gamemode."""
    fn.log_subsection("Remove gamemode")
    try:
        fn.disable_service(GAMEMODE_PACKAGE)
        fn.remove_package(self, GAMEMODE_PACKAGE)
        fn.log_success("gamemode removed")
        refresh_gamemode_package_label(self)
        refresh_gamemode_service_buttons(self)
        refresh_gamemode_status_label(self)
    except Exception as error:
        fn.log_error(f"Failed to remove gamemode: {error}")


def run_gamemoded_user_command(action):
    """Run systemctl --user enable/disable for gamemoded via --machine flag."""
    real_user = get_real_user()
    if not real_user:
        print("Could not determine real user for gamemoded service")
        return
    try:
        fn.subprocess.run(
            ["systemctl", "--user", f"--machine={real_user}@.host", action, "gamemoded.service"],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        print(error)


def enable_gamemode_service(widget, self):
    fn.log_subsection("Enable gamemode Service")
    try:
        run_gamemoded_user_command("enable")
        fn.log_success("gamemode service enabled")
        GLib.timeout_add(500, refresh_gamemode_status_label, self)
        GLib.idle_add(fn.show_in_app_notification, self, "gamemode has been enabled and started")
    except Exception as error:
        fn.log_error(f"Failed to enable gamemode: {error}")


def disable_gamemode_service(widget, self):
    fn.log_subsection("Disable gamemode Service")
    try:
        run_gamemoded_user_command("disable")
        fn.log_success("gamemode service disabled")
        GLib.timeout_add(500, refresh_gamemode_status_label, self)
        GLib.idle_add(fn.show_in_app_notification, self, "gamemode has been disabled and stopped")
    except Exception as error:
        fn.log_error(f"Failed to disable gamemode: {error}")
