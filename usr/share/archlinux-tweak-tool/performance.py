# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
from functions import GLib


POWER_PACKAGES = ["tuned", "cpupower"]
TLP_PACKAGE = "tlp"
CPU_POWER_PROFILES = {
    "Performance Mode (performance)": "performance",
    "Balanced Mode (schedutil - recommended)": "schedutil",
    "Power Saver Mode (powersave)": "powersave",
}

cpupower_config = "/etc/default/cpupower"
cpupower_governors = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors"
zram_config = "/etc/systemd/zram-generator.conf"
zram_disk_size = "/sys/block/zram0/disksize"
zram_enable_script = "/usr/share/archlinux-tweak-tool/data/any/enable-zram"
zram_disable_script = "/usr/share/archlinux-tweak-tool/data/any/disable-zram"
swapfile_create_script = "/usr/share/archlinux-tweak-tool/data/any/create-swapfile"
swapfile_remove_script = "/usr/share/archlinux-tweak-tool/data/any/remove-swapfile"


def install_power_tools(widget, self):
    """Install performance tools."""
    for package in POWER_PACKAGES:
        fn.install_package(self, package)
    disable_tlp_if_present(self)
    refresh_power_service_buttons(self)
    refresh_performance_status_label(self)


def remove_power_tools(widget, self):
    """Remove performance tools."""
    for package in reversed(POWER_PACKAGES):
        fn.remove_package(self, package)
    refresh_power_service_buttons(self)
    refresh_performance_status_label(self)


def refresh_power_service_buttons(self):
    """Refresh button sensitivity after installing or removing packages."""
    button_groups = {
        "tuned": [
            "enable_tuned",
            "disable_tuned",
            "restart_tuned",
        ],
        "cpupower": [
            "enable_cpupower",
            "disable_cpupower",
            "restart_cpupower",
        ],
    }

    for package, button_names in button_groups.items():
        installed = fn.check_package_installed(package)
        for button_name in button_names:
            if hasattr(self, button_name):
                getattr(self, button_name).set_sensitive(installed)


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


def get_performance_status_markup():
    """Build the service status label text."""
    tuned_status = get_service_status("tuned")
    cpupower_status = get_service_status("cpupower")
    tlp_status = get_service_status("tlp")
    return (
        "Tuned service : "
        + tuned_status
        + "   Cpupower service : "
        + cpupower_status
        + "   TLP service : "
        + tlp_status
    )


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


def enable_cpupower_service(widget, self):
    print("Enabling cpupower service")
    fn.enable_service("cpupower")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Cpupower has been enabled")


def disable_cpupower_service(widget, self):
    print("Disabling cpupower service")
    fn.disable_service("cpupower")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Cpupower has been disabled")


def restart_cpupower_service(widget, self):
    print("Restart cpupower")
    fn.restart_service("cpupower")
    refresh_performance_status_label(self)
    GLib.idle_add(fn.show_in_app_notification, self, "Cpupower has been restarted")


def apply_cpu_power_profile(widget, self):
    """Apply the selected CPU governor profile."""
    choice = fn.get_combo_text(self.cpu_power_choices)
    governor = CPU_POWER_PROFILES.get(choice)

    if governor is None:
        print("Unknown CPU power profile")
        GLib.idle_add(fn.show_in_app_notification, self, "Unknown CPU power profile")
        return

    set_cpupower_governor(self, governor)


def get_available_governors():
    """Return governors exposed by the current kernel/CPU driver."""
    try:
        if fn.path.isfile(cpupower_governors):
            with open(cpupower_governors, "r", encoding="utf-8") as f:
                return f.read().split()
    except Exception as error:
        print(error)
    return []


def get_cpu_power_profile_choices():
    """Return clean profile labels supported by this system."""
    available_governors = get_available_governors()
    if not available_governors:
        return list(CPU_POWER_PROFILES)

    choices = []
    for label, governor in CPU_POWER_PROFILES.items():
        if governor in available_governors:
            choices.append(label)

    return choices if choices else list(CPU_POWER_PROFILES)


def get_cpu_power_profile_default(choices):
    """Prefer Balanced when schedutil is available."""
    balanced = "Balanced Mode (schedutil - recommended)"
    if balanced in choices:
        return choices.index(balanced)
    return 0


def set_cpupower_governor(self, governor):
    """Apply and persist a cpupower CPU governor."""
    if governor not in CPU_POWER_PROFILES.values():
        print("Unknown cpupower governor : " + governor)
        GLib.idle_add(fn.show_in_app_notification, self, "Unknown CPU power profile")
        return

    if not fn.check_package_installed("cpupower"):
        fn.install_package(self, "cpupower")

    if fn.shutil.which("cpupower") is None:
        print("cpupower is not installed")
        GLib.idle_add(fn.show_in_app_notification, self, "cpupower is not installed")
        return

    try:
        result = fn.subprocess.run(
            ["cpupower", "frequency-set", "-g", governor],
            check=False,
            shell=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        if result.returncode != 0:
            print(result.stdout.decode().strip())
            GLib.idle_add(
                fn.show_in_app_notification, self, "Could not set CPU governor"
            )
            return

        governor_line = "governor='" + governor + "'\n"
        lines = []
        if fn.path.isfile(cpupower_config):
            with open(cpupower_config, "r", encoding="utf-8") as f:
                lines = f.readlines()

        governor_found = False
        new_lines = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith("governor=") or stripped_line.startswith(
                "#governor="
            ):
                new_lines.append(governor_line)
                governor_found = True
            else:
                new_lines.append(line)

        if not governor_found:
            new_lines.append(governor_line)

        with open(cpupower_config, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        fn.enable_service("cpupower")
        refresh_performance_status_label(self)
        print("CPU governor set to " + governor)
        GLib.idle_add(
            fn.show_in_app_notification, self, "CPU governor set to " + governor
        )
    except Exception as error:
        print(error)
        GLib.idle_add(fn.show_in_app_notification, self, "Could not set CPU governor")


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
