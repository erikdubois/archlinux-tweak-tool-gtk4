# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
from functions import GLib


# ============================================================
# Tuned Configuration
# ============================================================
TUNED_PACKAGE = "tuned tuned-ppd"
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
    """Refresh the visible tuned status label."""
    if hasattr(self, "tuned_status_label"):
        GLib.idle_add(
            self.tuned_status_label.set_markup,
            get_tuned_status_markup(),
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
    fn.install_package(self, TUNED_PACKAGE)
    disable_tlp_if_present(self)
    refresh_tuned_buttons(self)
    refresh_performance_status_label(self)


def remove_tuned_tools(widget, self):
    """Remove tuned and tuned-ppd."""
    fn.remove_package(self, TUNED_PACKAGE)
    refresh_tuned_buttons(self)
    refresh_performance_status_label(self)


def refresh_tuned_buttons(self):
    """Refresh tuned button sensitivity after installing or removing."""
    tuned_buttons = [
        "enable_tuned",
        "disable_tuned",
        "restart_tuned",
        "enable_tuned_ppd",
        "disable_tuned_ppd",
        "restart_tuned_ppd",
    ]
    installed = fn.check_package_installed(TUNED_PACKAGE)
    for button_name in tuned_buttons:
        if hasattr(self, button_name):
            getattr(self, button_name).set_sensitive(installed)


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


def enable_tuned_service(widget, self):
    print("Enabling tuned service")
    disable_tlp_if_present(self)
    fn.enable_service("tuned")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Tuned has been enabled")


def disable_tuned_service(widget, self):
    print("Disabling tuned service")
    fn.disable_service("tuned")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Tuned has been disabled")


def restart_tuned_service(widget, self):
    print("Restart tuned")
    disable_tlp_if_present(self)
    fn.restart_service("tuned")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Tuned has been restarted")


def enable_tuned_ppd_service(widget, self):
    print("Enabling tuned-ppd service")
    fn.enable_service("tuned-ppd")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Tuned-PPD has been enabled")


def disable_tuned_ppd_service(widget, self):
    print("Disabling tuned-ppd service")
    fn.disable_service("tuned-ppd")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Tuned-PPD has been disabled")


def restart_tuned_ppd_service(widget, self):
    print("Restart tuned-ppd")
    fn.restart_service("tuned-ppd")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Tuned-PPD has been restarted")


# ============================================================
# Tuned Profiles Management
# ============================================================

def get_available_tuned_profiles():
    """Return list of available tuned profiles."""
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
    if not fn.check_package_installed("tuned"):
        fn.install_package(self, "tuned")

    if fn.shutil.which("tuned-adm") is None:
        print("tuned-adm is not installed")
        GLib.idle_add(fn.show_in_app_notification, self, "tuned-adm is not installed")
        return

    try:
        # Ensure tuned service is started before applying profile
        print("Starting tuned service...")
        fn.enable_service("tuned")
        fn.restart_service("tuned")

        result = fn.subprocess.run(
            ["tuned-adm", "profile", profile_name],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        if result.returncode != 0:
            print(result.stdout.decode().strip())
            GLib.idle_add(
                fn.show_in_app_notification, self, f"Could not set tuned profile to {profile_name}"
            )
            return

        refresh_performance_status_label(self)
        refresh_tuned_profile_status(self)
        print(f"Tuned profile set to {profile_name}")
        GLib.idle_add(
            fn.show_in_app_notification, self, f"Tuned profile set to {profile_name}"
        )
    except Exception as error:
        print(error)
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
        "restart_irqbalance",
    ]:
        if hasattr(self, button_name):
            GLib.idle_add(getattr(self, button_name).set_sensitive, installed)


def enable_tuned_service(widget, self):
    print("Enabling tuned service")
    disable_tlp_if_present(self)
    fn.enable_service("tuned")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Tuned has been enabled")


def disable_tuned_service(widget, self):
    print("Disabling tuned service")
    fn.disable_service("tuned")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Tuned has been disabled")


def restart_tuned_service(widget, self):
    print("Restart tuned")
    disable_tlp_if_present(self)
    fn.restart_service("tuned")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Tuned has been restarted")


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


def enable_tuned_ppd_service(widget, self):
    print("Enabling tuned-ppd service")
    fn.enable_service("tuned-ppd")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Tuned-PPD has been enabled")


def disable_tuned_ppd_service(widget, self):
    print("Disabling tuned-ppd service")
    fn.disable_service("tuned-ppd")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Tuned-PPD has been disabled")


def restart_tuned_ppd_service(widget, self):
    print("Restart tuned-ppd")
    fn.restart_service("tuned-ppd")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Tuned-PPD has been restarted")


def enable_zram(widget, self):
    """Enable zram with the selected compressed swap size."""
    try:
        fn.install_package(self, "alacritty")
        size = fn.get_combo_text(self.zram_size)
        fn.subprocess.call(
            ["alacritty", "--hold", "-e", zram_enable_script, size],
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("Enabling zram: " + size)
        refresh_zram_status_label(self)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "zram enabled (" + size + ")",
        )
    except Exception as error:
        print(error)


def disable_zram(widget, self):
    """Disable zram."""
    try:
        fn.install_package(self, "alacritty")
        fn.subprocess.call(
            ["alacritty", "--hold", "-e", zram_disable_script],
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("Disabling zram")
        refresh_zram_status_label(self)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "zram disabled",
        )
    except Exception as error:
        print(error)


def create_swapfile(widget, self):
    """Create a swapfile with the selected size."""
    try:
        fn.install_package(self, "alacritty")
        size = fn.get_combo_text(self.swapfile_size)
        fn.subprocess.call(
            ["alacritty", "--hold", "-e", swapfile_create_script, size],
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("Creating swapfile: " + size)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Swapfile (" + size + ") created at /swapfile",
        )
    except Exception as error:
        print(error)


def remove_swapfile(widget, self):
    """Remove the swapfile."""
    try:
        fn.install_package(self, "alacritty")
        fn.subprocess.call(
            ["alacritty", "--hold", "-e", swapfile_remove_script],
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("Removing swapfile")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Swapfile removed",
        )
    except Exception as error:
        print(error)


def enable_fstrim_timer(widget, self):
    """Enable the weekly fstrim timer."""
    try:
        fn.subprocess.call(
            ["systemctl", "enable", "--now", fstrim_timer],
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("Enabling fstrim.timer")
        refresh_fstrim_status_label(self)
        GLib.idle_add(fn.show_in_app_notification, self, "fstrim.timer enabled")
    except Exception as error:
        print(error)


def disable_fstrim_timer(widget, self):
    """Disable the weekly fstrim timer."""
    try:
        fn.subprocess.call(
            ["systemctl", "disable", "--now", fstrim_timer],
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("Disabling fstrim.timer")
        refresh_fstrim_status_label(self)
        GLib.idle_add(fn.show_in_app_notification, self, "fstrim.timer disabled")
    except Exception as error:
        print(error)


def run_fstrim_now(widget, self):
    """Run fstrim once through the systemd service."""
    try:
        result = fn.subprocess.run(
            ["systemctl", "start", fstrim_service],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        if result.returncode == 0:
            print("Running fstrim.service")
            GLib.idle_add(fn.show_in_app_notification, self, "TRIM run started")
        else:
            print(result.stdout.decode().strip())
            GLib.idle_add(fn.show_in_app_notification, self, "Could not run TRIM")

        refresh_fstrim_status_label(self)
    except Exception as error:
        print(error)
        GLib.idle_add(fn.show_in_app_notification, self, "Could not run TRIM")


def install_irqbalance(widget, self):
    """Install irqbalance."""
    fn.install_package(self, "irqbalance")
    refresh_irqbalance_package_label(self)
    refresh_irqbalance_service_buttons(self)
    refresh_irqbalance_status_label(self)


def remove_irqbalance(widget, self):
    """Remove irqbalance."""
    fn.remove_package(self, "irqbalance")
    refresh_irqbalance_package_label(self)
    refresh_irqbalance_service_buttons(self)
    refresh_irqbalance_status_label(self)


def enable_irqbalance_service(widget, self):
    print("Enabling irqbalance service")
    fn.enable_service("irqbalance")
    refresh_irqbalance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "irqbalance has been enabled")


def disable_irqbalance_service(widget, self):
    print("Disabling irqbalance service")
    fn.disable_service("irqbalance")
    refresh_irqbalance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "irqbalance has been disabled")


def restart_irqbalance_service(widget, self):
    print("Restart irqbalance")
    fn.restart_service("irqbalance")
    refresh_irqbalance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "irqbalance has been restarted")
