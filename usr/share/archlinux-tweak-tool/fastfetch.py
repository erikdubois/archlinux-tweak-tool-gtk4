# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
import re
import json
import utilities

# ====================================================================
#                       Fastfetch
# ====================================================================


def get_fastfetch():
    """Get data from fastfetch config JSONC file."""
    if not fn.path.isfile(fn.fastfetch_config):
        return {}
    try:
        with open(fn.fastfetch_config, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'^\s*//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r',(\s*[}\]])', r'\1', content)
        return json.loads(content)
    except Exception as e:
        fn.debug_print(f"Failed to parse fastfetch config: {e}")
        return {}


def get_position(lists, value):
    """Get position of fastfetch command in list, accounting for lolcat and comments"""
    data = []
    suffixes = [" | lolcat", "\n", " | lolcat\n"]
    prefix = "#"

    for string in lists:
        for item in suffixes:
            if string in (value + item, prefix + value + item, value, prefix + value):
                data.append(string)

    if len(data) > 0:
        position = lists.index(data[0])
        return position
    else:
        return -1


def write_configs(util_enabled, lolcat_enabled):
    """Write fastfetch config to shell rc file"""
    config = utilities.get_config_file()
    if not config:
        return

    with open(config, "r", encoding="utf-8") as f:
        lines = f.readlines()

    reporting_section_start = -1
    for i, line in enumerate(lines):
        if "# reporting tools" in line.lower():
            reporting_section_start = i
            break

    if reporting_section_start == -1:
        return

    fastfetch_line = -1
    for i in range(reporting_section_start, len(lines)):
        if lines[i].strip().startswith(("fastfetch", "#fastfetch")):
            fastfetch_line = i
            break

    if fastfetch_line == -1:
        return

    current_line = lines[fastfetch_line].strip()
    if util_enabled:
        new_state = "fastfetch | lolcat" if lolcat_enabled else "fastfetch"
    else:
        new_state = "#fastfetch"

    if current_line != new_state and fastfetch_line >= reporting_section_start:
        lines[fastfetch_line] = new_state + "\n"

        with open(config, "w", encoding="utf-8") as f:
            f.writelines(lines)


def get_term_rc():
    """Check if fastfetch is enabled in shell config"""
    config_file = ""
    pos = -1
    try:
        config_file = utilities.get_config_file()
    except Exception:
        config_file = ""
    if config_file != "":
        with open(config_file, "r", encoding="utf-8") as myfile:
            lines = myfile.readlines()
            myfile.close()
            pos = get_position(lines, "fastfetch")

    if pos > 0 and lines[pos].startswith("#"):
        return False
    elif pos >= 0:
        return True
    else:
        return False


def check_backend():
    """See if image backend is active."""
    if fn.path.isfile(fn.fastfetch_config):
        config = get_fastfetch()
        if config:
            image_backend = config.get("image_backend", None)
            if image_backend and not image_backend.startswith("#"):
                return image_backend.strip('"')
    return "ascii"


def apply_config(self, backend, ascii_size):
    """Apply fastfetch configuration"""
    if fn.path.isfile(fn.fastfetch_config):
        with open(fn.fastfetch_config, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Mapping keys to checkboxes
        key_to_checkbox = {
            '"os"': self.os,
            '"host"': self.host,
            '"kernel"': self.kernel,
            '"uptime"': self.uptime,
            '"packages"': self.packages,
            '"shell"': self.shell,
            '"display"': self.display,
            '"de"': self.de,
            '"wm"': self.wm,
            '"wmtheme"': self.wmtheme,
            '"theme"': self.themes,
            '"icons"': self.icons,
            '"font"': self.font,
            '"cursor"': self.cursor,
            '"terminal"': self.term,
            '"terminalfont"': self.termfont,
            '"cpu"': self.cpu,
            '"gpu"': self.gpu,
            '"memory"': self.mem,
            '"swap"': self.swap,
            '"disk"': self.disks,
            '"localIP"': self.lIP,
            '"publicip"': self.PIP,
            '"battery"': self.batt,
            '"poweradapter"': self.pwr,
            '"locale"': self.local,
            '"title"': self.title,
            '"underline"': self.title,
            '"colors"': self.cblocks,
        }

        # Comment or uncomment each key based on the checkbox state
        for i in range(len(lines)):
            for key, checkbox in key_to_checkbox.items():
                if key.lower() in lines[i].lower():
                    if checkbox.get_active() and lines[i].strip().startswith("//"):
                        lines[i] = lines[i].replace('//', '', 1)
                    elif not checkbox.get_active() and not lines[i].strip().startswith("//"):
                        lines[i] = "//" + lines[i]

        # Write the updated lines back to the file
        with open(fn.fastfetch_config, "w", encoding="utf-8") as f:
            f.writelines(lines)

        fn.show_in_app_notification(self, "fastfetch settings saved successfully")


def get_checkboxes(self):
    """Read checkbox states from the JSONC config modules list."""
    config = get_fastfetch()
    modules = [m.lower() for m in config.get("modules", []) if isinstance(m, str)]

    self.title.set_active("title" in modules)
    self.os.set_active("os" in modules)
    self.host.set_active("host" in modules)
    self.kernel.set_active("kernel" in modules)
    self.uptime.set_active("uptime" in modules)
    self.packages.set_active("packages" in modules)
    self.shell.set_active("shell" in modules)
    self.display.set_active("display" in modules)
    self.de.set_active("de" in modules)
    self.wm.set_active("wm" in modules)
    self.wmtheme.set_active("wmtheme" in modules)
    self.themes.set_active("theme" in modules)
    self.icons.set_active("icons" in modules)
    self.font.set_active("font" in modules)
    self.cursor.set_active("cursor" in modules)
    self.term.set_active("terminal" in modules)
    self.termfont.set_active("terminalfont" in modules)
    self.cpu.set_active("cpu" in modules)
    self.gpu.set_active("gpu" in modules)
    self.mem.set_active("memory" in modules)
    self.swap.set_active("swap" in modules)
    self.disks.set_active("disk" in modules)
    self.lIP.set_active("localip" in modules)
    self.PIP.set_active("publicip" in modules)
    self.batt.set_active("battery" in modules)
    self.pwr.set_active("poweradapter" in modules)
    self.local.set_active("locale" in modules)
    self.cblocks.set_active("colors" in modules)


def set_checkboxes_normal(self):
    """set the state of the checkboxes and ensure separator is uncommented"""
    self.title.set_active(True)
    self.os.set_active(True)
    self.host.set_active(True)
    self.kernel.set_active(True)
    self.uptime.set_active(True)
    self.packages.set_active(True)
    self.shell.set_active(True)
    self.display.set_active(True)
    self.de.set_active(True)
    self.wm.set_active(True)
    self.wmtheme.set_active(True)
    self.themes.set_active(True)
    self.icons.set_active(True)
    self.font.set_active(True)
    self.cursor.set_active(True)
    self.term.set_active(True)
    self.termfont.set_active(True)
    self.cpu.set_active(True)
    self.gpu.set_active(True)
    self.mem.set_active(True)
    self.swap.set_active(True)
    self.disks.set_active(True)
    self.lIP.set_active(False)
    self.PIP.set_active(False)
    self.batt.set_active(True)
    self.pwr.set_active(True)
    self.local.set_active(False)
    self.cblocks.set_active(False)

    _ensure_separator_uncommented()


def set_checkboxes_small(self):
    """set the state of the checkboxes and ensure separator is uncommented"""
    self.title.set_active(True)
    self.os.set_active(False)
    self.host.set_active(False)
    self.kernel.set_active(True)
    self.uptime.set_active(True)
    self.packages.set_active(True)
    self.shell.set_active(True)
    self.display.set_active(False)
    self.de.set_active(True)
    self.wm.set_active(True)
    self.wmtheme.set_active(True)
    self.themes.set_active(True)
    self.icons.set_active(True)
    self.font.set_active(True)
    self.cursor.set_active(True)
    self.term.set_active(True)
    self.termfont.set_active(False)
    self.cpu.set_active(True)
    self.gpu.set_active(True)
    self.mem.set_active(True)
    self.swap.set_active(True)
    self.disks.set_active(False)
    self.lIP.set_active(False)
    self.PIP.set_active(False)
    self.batt.set_active(True)
    self.pwr.set_active(True)
    self.local.set_active(False)
    self.cblocks.set_active(False)

    _ensure_separator_uncommented()


def set_checkboxes_all(self):
    """set the state of the checkboxes and ensure separator is uncommented"""
    self.title.set_active(True)
    self.os.set_active(True)
    self.host.set_active(True)
    self.kernel.set_active(True)
    self.uptime.set_active(True)
    self.packages.set_active(True)
    self.shell.set_active(True)
    self.display.set_active(True)
    self.de.set_active(True)
    self.wm.set_active(True)
    self.wmtheme.set_active(True)
    self.themes.set_active(True)
    self.icons.set_active(True)
    self.font.set_active(True)
    self.cursor.set_active(True)
    self.term.set_active(True)
    self.termfont.set_active(True)
    self.cpu.set_active(True)
    self.gpu.set_active(True)
    self.mem.set_active(True)
    self.swap.set_active(True)
    self.disks.set_active(True)
    self.lIP.set_active(True)
    self.PIP.set_active(False)
    self.batt.set_active(True)
    self.pwr.set_active(True)
    self.local.set_active(True)
    self.cblocks.set_active(True)

    _ensure_separator_uncommented()


def set_checkboxes_none(self):
    """set the state of the checkboxes and comment out separator in config.jsonc"""
    self.title.set_active(False)
    self.os.set_active(False)
    self.host.set_active(False)
    self.kernel.set_active(False)
    self.uptime.set_active(False)
    self.packages.set_active(False)
    self.shell.set_active(False)
    self.display.set_active(False)
    self.de.set_active(False)
    self.wm.set_active(False)
    self.wmtheme.set_active(False)
    self.themes.set_active(False)
    self.icons.set_active(False)
    self.font.set_active(False)
    self.cursor.set_active(False)
    self.term.set_active(False)
    self.termfont.set_active(False)
    self.cpu.set_active(False)
    self.gpu.set_active(False)
    self.mem.set_active(False)
    self.swap.set_active(False)
    self.disks.set_active(False)
    self.lIP.set_active(False)
    self.PIP.set_active(False)
    self.batt.set_active(False)
    self.pwr.set_active(False)
    self.local.set_active(False)
    self.cblocks.set_active(False)

    _ensure_separator_commented()


def _ensure_separator_uncommented():
    """Ensure the separator in config.jsonc is uncommented"""
    if fn.path.isfile(fn.fastfetch_config):
        with open(fn.fastfetch_config, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if '"separator"' in line and line.strip().startswith('//'):
                lines[i] = line.lstrip('/')

        with open(fn.fastfetch_config, "w", encoding="utf-8") as f:
            f.writelines(lines)


def _ensure_separator_commented():
    """Ensure the separator in config.jsonc is commented out"""
    if fn.path.isfile(fn.fastfetch_config):
        with open(fn.fastfetch_config, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if '"separator"' in line and not line.strip().startswith('//'):
                lines[i] = '//' + line

        with open(fn.fastfetch_config, "w", encoding="utf-8") as f:
            f.writelines(lines)

# ====================================================================
# FASTFETCH CALLBACKS
# ====================================================================


def set_fastfetch_ui_sensitive(self, state):
    for widget in [
        self.fast_lolcat,
        self.hbox_ff_warning,
        self.hbox_ff_checkboxes,
        self.fastfetch_image,
        self.hbox_ff_presets,
        self.hbox_ff_actions,
        self.btn_remove_fastfetch,
    ]:
        widget.set_sensitive(state)


def on_remove_fast(self, _widget):
    fn.log_subsection("Removing fastfetch")
    fn.show_in_app_notification(self, "Opening terminal to remove fastfetch...")
    script = (
        "sudo pacman -Rdd fastfetch-git 2>/dev/null || sudo pacman -Rdd fastfetch 2>/dev/null; "
        "echo; read -p 'Press enter to close'"
    )
    process = fn.subprocess.Popen(
        ["alacritty", "-e", "bash", "-c", script],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )

    def wait_and_update():
        process.wait()
        if not fn.path.exists("/usr/bin/fastfetch"):
            fn.log_success("Fastfetch removed")
            fn.GLib.idle_add(set_fastfetch_ui_sensitive, self, False)
            fn.GLib.idle_add(self.fast_util.set_active, False)

    fn.threading.Thread(target=wait_and_update, daemon=True).start()


def on_install_fast(self, _widget):
    fn.install_package(self, "fastfetch-git")


def on_apply_fast(self, _widget):
    fn.log_subsection("Apply Fastfetch configuration")
    if not self.fast_util.get_active():
        fn.log_info("Fastfetch was not enabled — enabling now")
        self.fast_util.set_active(True)
    small_ascii = "auto"
    backend = "off"
    apply_config(self, backend, small_ascii)
    fn.log_success("Fastfetch configuration applied")


def on_reset_fast_att(self, _widget):
    fn.debug_print("Reset fastfetch to ATT defaults")
    fn.debug_print(f"  Source : {fn.fastfetch_kiro}")
    fn.debug_print(f"  Target : {fn.fastfetch_config}")
    if fn.path.isfile(fn.fastfetch_kiro):
        fn.shutil.copy(fn.fastfetch_kiro, fn.fastfetch_config)
        fn.permissions(fn.fastfetch_config)
        fn.debug_print("  Result : copied and permissions set")
        fn.log_success("Fastfetch ATT defaults applied")
        fn.show_in_app_notification(self, "ATT defaults applied")
        get_checkboxes(self)
    else:
        fn.debug_print("  Result : source file not found - nothing copied")


def on_reset_fast(self, _widget):
    fn.debug_print("Reset fastfetch from backup")
    fn.debug_print(f"  Source : {fn.fastfetch_config}.bak")
    fn.debug_print(f"  Target : {fn.fastfetch_config}")
    if fn.path.isfile(fn.fastfetch_config + ".bak"):
        fn.shutil.copy(fn.fastfetch_config + ".bak", fn.fastfetch_config)
        fn.debug_print("  Result : restored from backup")
        get_checkboxes(self)
        fn.log_success("fastfetch default settings applied")
        fn.show_in_app_notification(self, "Default settings applied")
    else:
        fn.debug_print("  Result : backup file not found - nothing restored")


def lolcat_toggle(self, widget, active, utility):
    lolcat_state = widget.get_active()
    util_state = utilities.get_util_state(self, utility)

    if lolcat_state:
        utilities.install_util(self, "lolcat")
        if not util_state or utility == "fastfetch":
            util_state = True
            utilities.set_util_state(self, utility, True, True)
    elif not lolcat_state and utility == "fastfetch":
        utilities.set_util_state(self, utility, True, False)


def on_fast_util_toggled(self, switch, gparam):
    if getattr(self, 'ff_initializing', False):
        return
    util_state = switch.get_active()
    lolcat_state = self.fast_lolcat.get_active()
    label = "enabled" if util_state else "disabled"
    fn.log_subsection(f"Fastfetch {label}")
    fn.debug_print(f"  Config : {utilities.get_config_file()}")

    if util_state and not fn.path.exists("/usr/bin/fastfetch"):
        fn.log_subsection("Installing fastfetch-git...")
        fn.show_in_app_notification(self, "Opening terminal to install fastfetch...")
        process = fn.launch_pacman_install_in_terminal("fastfetch-git")

        def wait_and_enable():
            if process:
                process.communicate()
            if fn.path.exists("/usr/bin/fastfetch"):
                fn.log_success("fastfetch installed")
                fn.GLib.idle_add(set_fastfetch_ui_sensitive, self, True)
                fn.GLib.idle_add(fn.show_in_app_notification, self, "fastfetch installed")

        fn.threading.Thread(target=wait_and_enable, daemon=True).start()
        return

    if not util_state:
        self.fast_lolcat.set_active(False)
        lolcat_state = False

    write_configs(util_state, lolcat_state)
    self.fast_lolcat.set_sensitive(util_state)
    fn.log_success(f"Fastfetch {label} in shell config")
    fn.GLib.idle_add(fn.show_in_app_notification, self, f"Fastfetch {label}")


def on_fast_lolcat_toggled(self, switch, gparam):
    if getattr(self, 'ff_initializing', False):
        return
    lolcat_state = switch.get_active()
    util_state = self.fast_util.get_active()
    label = "enabled" if lolcat_state else "disabled"
    fn.log_subsection(f"Lolcat {label}")
    fn.debug_print(f"  Config : {utilities.get_config_file()}")

    if util_state:
        write_configs(util_state, lolcat_state)
        fn.log_success(f"Lolcat {label} in shell config")
        fn.GLib.idle_add(fn.show_in_app_notification, self, f"Lolcat {label}")


def util_toggle(self, widget, active, utility):
    util_state = widget.get_active()
    lolcat_state = utilities.get_lolcat_state(self, utility)

    if util_state:
        utilities.install_util(self, utility)
        if utility == "fastfetch":
            utilities.set_util_state(self, utility, True, lolcat_state)
    else:
        if lolcat_state:
            lolcat_state = False
        utilities.set_util_state(self, utility, False, False)


def on_click_fastfetch_all_selection(self, widget):
    fn.log_subsection("All Fastfetch switches selected")
    set_checkboxes_all(self)


def on_click_fastfetch_normal_selection(self, widget):
    fn.log_subsection("Normal Fastfetch selection applied")
    set_checkboxes_normal(self)


def on_click_fastfetch_small_selection(self, widget):
    fn.log_subsection("Small Fastfetch selection applied")
    set_checkboxes_small(self)


def on_click_fastfetch_none_selection(self, widget):
    fn.log_subsection("No Fastfetch switches selected")
    set_checkboxes_none(self)
