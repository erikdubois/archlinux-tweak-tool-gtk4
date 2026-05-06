# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
from functions import GLib
import xml.etree.ElementTree as ET


XSESSION_DIRS = ["/usr/share/xsessions", "/usr/share/wayland-sessions"]


def _ensure_dir(path):
    directory = fn.path.dirname(path)
    if directory and not fn.path.isdir(directory):
        fn.makedirs(directory, 0o766)
        fn.permissions(directory)


def _write_lines(path, lines):
    _ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    if path.startswith(fn.home):
        fn.permissions(path)


def _set_key_value(path, key, value, sep="=", quoted=False, section=None):
    lines = []
    key_line = key + sep
    line_value = '"' + value + '"' if quoted else value
    new_line = key + sep + line_value + "\n"

    if fn.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    if not section:
        for pos, line in enumerate(lines):
            if line.strip().startswith(key_line):
                lines[pos] = new_line
                _write_lines(path, lines)
                return path
        lines.append(new_line)
        _write_lines(path, lines)
        return path

    section_header = "[" + section + "]"
    section_start = None
    section_end = len(lines)

    for pos, line in enumerate(lines):
        stripped = line.strip()
        if stripped == section_header:
            section_start = pos
            continue
        if section_start is not None and pos > section_start and stripped.startswith("["):
            section_end = pos
            break

    if section_start is None:
        if lines and lines[-1].strip():
            lines.append("\n")
        lines.append(section_header + "\n")
        lines.append(new_line)
        _write_lines(path, lines)
        return path

    for pos in range(section_start + 1, section_end):
        if lines[pos].strip().startswith(key_line):
            lines[pos] = new_line
            _write_lines(path, lines)
            return path

    lines.insert(section_end, new_line)

    _write_lines(path, lines)
    return path


def _set_index_theme(path, cursor):
    fn.debug_print(f"[INFO] Setting cursor '{cursor}' in {path}")
    lines = []
    found_section = False
    found_inherits = False

    if fn.path.isfile(path):
        fn.debug_print(f"[INFO] File exists: {path}")
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        fn.debug_print(f"[INFO] File does not exist, will create: {path}")

    for pos, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "[Icon Theme]":
            found_section = True
        if stripped.startswith("Inherits="):
            lines[pos] = "Inherits=" + cursor + "\n"
            found_inherits = True
            fn.debug_print(f"[INFO] Updated Inherits line with cursor '{cursor}'")
            break

    if not found_section:
        if lines and lines[-1].strip():
            lines.append("\n")
        lines.append("[Icon Theme]\n")
        fn.debug_print("[INFO] Added [Icon Theme] section")

    if not found_inherits:
        lines.append("Inherits=" + cursor + "\n")
        fn.debug_print(f"[INFO] Added Inherits line with cursor '{cursor}'")

    _write_lines(path, lines)
    fn.debug_print(f"[INFO] Successfully saved cursor '{cursor}' to {path}")
    return path


def _set_xfce_cursor(path, cursor):
    fn.debug_print(f"[INFO] Setting XFCE cursor '{cursor}' in {path}")
    if fn.path.isfile(path):
        fn.debug_print(f"[INFO] File exists: {path}")
        tree = ET.parse(path)
        root = tree.getroot()
    else:
        fn.debug_print(f"[INFO] File does not exist, creating: {path}")
        _ensure_dir(path)
        root = ET.Element("channel", name="xsettings", version="1.0")
        tree = ET.ElementTree(root)

    net = None
    for child in root.findall("property"):
        if child.get("name") == "Net":
            net = child
            break
    if net is None:
        fn.debug_print("[INFO] Creating Net property in XFCE config")
        net = ET.SubElement(root, "property", name="Net", type="empty")

    cursor_prop = None
    for child in net.findall("property"):
        if child.get("name") == "CursorThemeName":
            cursor_prop = child
            break
    if cursor_prop is None:
        fn.debug_print("[INFO] Creating CursorThemeName property in XFCE config")
        cursor_prop = ET.SubElement(net, "property", name="CursorThemeName")

    cursor_prop.set("type", "string")
    cursor_prop.set("value", cursor)
    fn.debug_print(f"[INFO] Set CursorThemeName to '{cursor}'")
    tree.write(path, encoding="unicode", xml_declaration=True)
    if path.startswith(fn.home):
        fn.permissions(path)
    fn.debug_print(f"[INFO] Successfully saved XFCE cursor '{cursor}' to {path}")
    return path


def _set_gsettings_cursor(cursor):
    fn.debug_print(f"[INFO] Setting gsettings cursor '{cursor}'")
    username = fn.sudo_username
    pkexec_uid = fn.os.environ.get("PKEXEC_UID")

    if pkexec_uid:
        try:
            username = fn.pwd.getpwuid(int(pkexec_uid)).pw_name
            fn.debug_print(f"[INFO] Using PKEXEC_UID username: {username}")
        except Exception as error:
            fn.debug_print(f"[ERROR] Could not get username from PKEXEC_UID: {error}")

    try:
        user_info = fn.pwd.getpwnam(username)
        uid = user_info.pw_uid
        home = user_info.pw_dir
        fn.debug_print(f"[INFO] Setting cursor for user: {username} (uid: {uid})")
        env = [
            "HOME=" + home,
            "XDG_RUNTIME_DIR=/run/user/" + str(uid),
            "DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus",
        ]
        command = [
            "gsettings",
            "set",
            "org.gnome.desktop.interface",
            "cursor-theme",
            cursor,
        ]
        if fn.os.geteuid() != uid:
            command = ["sudo", "-u", username, "env"] + env + command
        else:
            command = ["env"] + env + command

        fn.debug_print("[INFO] Executing gsettings command for org.gnome.desktop.interface")
        result = fn.subprocess.run(
            command,
            check=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        if result.returncode == 0:
            fn.debug_print(f"[INFO] Successfully set gsettings cursor to '{cursor}'")
            return "gsettings:" + username + ":org.gnome.desktop.interface"
        else:
            output = result.stdout.decode(errors="ignore")
            fn.debug_print(f"[ERROR] gsettings failed: {output}")
    except Exception as error:
        fn.debug_print(f"[ERROR] gsettings error: {error}")
    return None


def _set_plasma_cursor(cursor):
    fn.debug_print(f"[INFO] Setting KDE Plasma cursor '{cursor}'")
    path = fn.home + "/.config/kcminputrc"
    fn.debug_print(f"[INFO] Updating KDE Plasma config: {path}")
    result = _set_key_value(path, "cursorTheme", cursor, section="Mouse")
    if result:
        fn.debug_print(f"[INFO] Successfully set KDE Plasma cursor to '{cursor}'")
    return result


def _set_sddm_cursor(cursor):
    fn.debug_print(f"[INFO] Setting SDDM cursor '{cursor}'")
    paths = [
        fn.sddm_default_d2,
        fn.sddm_default_d1,
        "/usr/lib/sddm/sddm.conf.d/default.conf",
    ]
    key = "CursorTheme="
    new_line = key + cursor + "\n"
    changed = []
    existing_paths = []

    for path in paths:
        if not fn.path.isfile(path):
            continue

        fn.debug_print(f"[INFO] Processing SDDM config: {path}")
        existing_paths.append(path)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        has_cursor = False
        for pos, line in enumerate(lines):
            stripped = line.strip().lstrip("#").strip()
            if stripped.startswith(key) or stripped.startswith("CursorTheme ="):
                lines[pos] = new_line
                has_cursor = True
                fn.debug_print(f"[INFO] Updated CursorTheme in {path}")

        if has_cursor:
            _write_lines(path, lines)
            changed.append(path)
            fn.debug_print(f"[INFO] Successfully saved SDDM cursor '{cursor}' to {path}")

    if changed or not existing_paths:
        return changed

    path = existing_paths[0]
    return [_set_key_value(path, "CursorTheme", cursor, section="Theme")]


def get_installed_sessions():
    sessions = set()
    aliases = {
        "gnome-wayland": "gnome",
        "gnome-classic": "gnome",
        "kde-plasma": "plasma",
        "plasmawayland": "plasma",
        "xfce4": "xfce",
    }

    for session_dir in XSESSION_DIRS:
        if not fn.path.isdir(session_dir):
            continue
        for item in fn.listdir(session_dir):
            if not item.endswith(".desktop"):
                continue
            name = item[:-8].lower()
            sessions.add(aliases.get(name, name))
            desktop_file = fn.path.join(session_dir, item)
            try:
                with open(desktop_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith(("Name=", "Exec=", "DesktopNames=")):
                            value = line.split("=", 1)[1].strip().lower()
                            for key in aliases:
                                if key in value:
                                    sessions.add(aliases[key])
                            for desktop in (
                                "awesome",
                                "bspwm",
                                "budgie",
                                "cinnamon",
                                "gnome",
                                "hyprland",
                                "i3",
                                "leftwm",
                                "mate",
                                "plasma",
                                "qtile",
                                "sway",
                                "wayfire",
                                "xfce",
                            ):
                                if desktop in value:
                                    sessions.add(desktop)
            except Exception as error:
                fn.debug_print(error)

    return sessions


def check_cursor_global(lists, value):
    if fn.path.isfile(fn.icons_default):
        try:
            pos = fn.get_position(lists, value)
            val = lists[pos].strip()
            return val
        except Exception as error:
            fn.debug_print(error)


def set_global_cursor(self, cursor):
    if not cursor:
        fn.show_in_app_notification(self, "Select a cursor theme first")
        return

    fn.debug_print(f"[INFO] Starting global cursor application: {cursor}")
    changed = []
    failed = []
    sessions = get_installed_sessions()
    fn.debug_print(f"[INFO] Detected installed sessions: {', '.join(sorted(sessions)) or 'none'}")

    def apply_target(label, target, *args, **kwargs):
        try:
            fn.debug_print(f"[INFO] Applying cursor to {label}...")
            result = target(*args, **kwargs)
            if result:
                if isinstance(result, list):
                    changed.extend(result)
                else:
                    changed.append(result)
            fn.debug_print(f"[INFO] Successfully applied cursor to {label}")
        except Exception as error:
            failed.append(label)
            fn.debug_print(f"[ERROR] Failed to apply cursor to {label}: {error}")

    apply_target("system xcursor", _set_index_theme, fn.icons_default, cursor)
    apply_target(
        "user xcursor",
        _set_index_theme,
        fn.home + "/.icons/default/index.theme",
        cursor,
    )
    apply_target(
        "gtk3",
        _set_key_value,
        fn.home + "/.config/gtk-3.0/settings.ini",
        "gtk-cursor-theme-name",
        cursor,
        section="Settings",
    )
    apply_target(
        "gtk4",
        _set_key_value,
        fn.home + "/.config/gtk-4.0/settings.ini",
        "gtk-cursor-theme-name",
        cursor,
        section="Settings",
    )
    apply_target(
        "gtk2",
        _set_key_value,
        fn.home + "/.gtkrc-2.0",
        "gtk-cursor-theme-name",
        cursor,
        quoted=True,
    )

    if "xfce" in sessions or fn.path.isfile(fn.xfce_config):
        apply_target("xfce", _set_xfce_cursor, fn.xfce_config, cursor)

    apply_target("gsettings", _set_gsettings_cursor, cursor)

    if "plasma" in sessions:
        apply_target("plasma", _set_plasma_cursor, cursor)

    if fn.path.exists("/usr/bin/sddm"):
        apply_target("sddm", _set_sddm_cursor, cursor)

    fn.debug_print("=" * 75)
    fn.debug_print(f"[INFO] Cursor theme successfully saved: {cursor}")
    fn.debug_print("[INFO] Modified locations:")
    for target in changed:
        fn.debug_print(f"[INFO]  - {target}")
    if failed:
        fn.debug_print(f"[WARNING] Failed cursor targets: {', '.join(failed)}")
    fn.debug_print("=" * 75)

    fn.log_info_concise(f"Cursor theme '{cursor}' applied to:")
    for target in changed:
        fn.log_info_concise(f"  ✓ {target}")
    if failed:
        fn.log_info_concise(f"Failed targets: {', '.join(failed)}")

    if changed:
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Cursor saved for " + str(len(changed)) + " setting(s)",
        )
    else:
        fn.messagebox(
            self,
            "Failed!!",
            'There seems to have been a problem in "set_global_cursor"',
        )


def pop_gtk_cursor_names(combo):
    """populate cursor names"""
    _m = combo.get_model()
    _m.splice(0, _m.get_n_items(), [])
    lines = fn.get_lines(fn.icons_default)
    try:
        raw = check_cursor_global(lines, "Inherits=")
        cursor_theme = raw.split("=")[1] if raw else ""
    except (IndexError, AttributeError):
        cursor_theme = ""

    for i, item in enumerate(fn.list_cursor_themes()):
        combo.get_model().append(item)
        if cursor_theme.lower() == item.lower():
            combo.set_selected(i)


# ====================================================================
# ====================================================================
# ====================================================================
#                   CALLBACK FUNCTIONS
# ====================================================================
# ====================================================================
# ====================================================================


def _run_terminal(self, cmd, done_msg, start_msg=None):
    if start_msg:
        GLib.idle_add(fn.show_in_app_notification, self, start_msg)
    fn.debug_print(f"Terminal cmd: {cmd}")

    def _wait():
        try:
            fn.subprocess.Popen(cmd, shell=True, env=fn.get_terminal_env()).wait()
            fn.log_success(done_msg)
            GLib.idle_add(fn.show_in_app_notification, self, done_msg)
        except Exception as error:
            fn.log_error(f"Error: {error}")

    fn.threading.Thread(target=_wait, daemon=True).start()


# System Maintenance
def on_click_apply_global_cursor(self, _widget):
    cursor = fn.get_combo_text(self.cursor_themes)
    if not cursor:
        fn.show_in_app_notification(self, "Please select a cursor theme first")
        return

    message = (
        "This will apply the cursor theme globally to:\n\n"
        "• System xcursor configuration\n"
        "• User xcursor configuration\n"
        "• GTK2, GTK3, and GTK4 settings\n"
        "• XFCE settings (if installed)\n"
        "• GNOME settings (gsettings)\n"
        "• KDE Plasma settings (if installed)\n"
        "• SDDM login screen (if installed)\n\n"
        "This affects all applications and the SDDMlogin screen."
    )

    if not fn.confirm_dialog(self, "Apply Global Cursor Theme", message):
        return

    fn.log_subsection("Applying global cursor theme...")
    try:
        fn.debug_print(f"Selected cursor theme: {cursor}")
        set_global_cursor(self, cursor)
        fn.log_success(f"Cursor '{cursor}' saved globally")
    except Exception as error:
        fn.log_error(f"Error: {error}")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            f"Failed to apply cursor: {error}",
        )


def on_click_update_system(self, _widget):
    fn.log_subsection("Starting system update...")
    cmd = (
        "alacritty -e bash -c 'sudo pacman -Syu; echo \"\";"
        " echo \"=== Update complete ===\"; read -p \"Press Enter to close...\"'"
    )
    _run_terminal(self, cmd, "System update completed", "Starting system update...")


def on_click_clean_cache(self, _widget):
    fn.log_subsection("Launching pacman cache cleanup...")
    pkg_dir = "/var/cache/pacman/pkg/"
    temp_dirs = [f for f in fn.os.listdir(pkg_dir) if f.startswith("download-")]
    part_files = [f for f in fn.os.listdir(pkg_dir) if f.endswith(".part")]
    if temp_dirs:
        fn.log_info("Removing leftover temp download folders from /var/cache/pacman/pkg/")
    if part_files:
        fn.log_info("Removing partial download files (.part) from /var/cache/pacman/pkg/")
    cmd = (
        "alacritty -e bash -c '"
        "if compgen -G \"/var/cache/pacman/pkg/download-*\" > /dev/null 2>&1; then "
        "sudo rm -rf /var/cache/pacman/pkg/download-*; "
        "echo \"  Temp download folders removed\"; "
        "fi; "
        "if compgen -G \"/var/cache/pacman/pkg/*.part\" > /dev/null 2>&1; then "
        "sudo rm -f /var/cache/pacman/pkg/*.part; "
        "echo \"  Partial download files (.part) removed\"; "
        "fi; "
        "sudo pacman -Sc; echo \"\"; "
        "echo \"=== Clean complete ===\"; read -p \"Press Enter to close...\"'"
    )
    _run_terminal(self, cmd, "Pacman cache cleaned", "Removing temp files and cleaning cache...")


def on_click_remove_pacman_lock(self, _widget):
    fn.log_subsection("Removing pacman lock...")
    fn.debug_print("Checking pacman lock file: /var/lib/pacman/db.lck")
    cmd = (
        "alacritty -e bash -c 'sudo rm -f /var/lib/pacman/db.lck; echo \"\";"
        " echo \"=== Lock removed ===\"; read -p \"Press Enter to close...\"'"
    )
    _run_terminal(self, cmd, "Pacman lock removed", "Removing pacman lock...")


# Pacman Keyring Management
def on_click_install_arch_keyring(self, _widget):
    fn.log_subsection("Installing local archlinux-keyring...")

    def _install():
        base_dir = fn.os.path.dirname(fn.os.path.abspath(__file__))
        pathway = base_dir + "/data/packages/keyring/"
        files = [f for f in fn.listdir(pathway) if f.endswith(".pkg.tar.zst")]
        if not files:
            fn.log_error("No package files found in keyring pathway")
            GLib.idle_add(fn.show_in_app_notification, self, "No keyring package found")
            return
        package_file = fn.os.path.join(pathway, files[0])
        fn.debug_print(f"Found package: {package_file}")
        cmd = f"sudo pacman -U {package_file}; read -p 'Press Enter to close...'"
        fn.subprocess.Popen(
            ["alacritty", "-e", "bash", "-c", cmd],
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.PIPE,
        ).wait()
        fn.log_success("archlinux-keyring installed")
        GLib.idle_add(fn.show_in_app_notification, self, "archlinux-keyring installed")

    GLib.idle_add(fn.show_in_app_notification, self, "Starting archlinux-keyring installation...")
    fn.threading.Thread(target=_install, daemon=True).start()


def on_click_install_arch_keyring_online(self, _widget):
    fn.log_subsection("Installing archlinux-keyring online...")
    pathway = "/tmp/att-installation/"
    fn.debug_print(f"Creating temporary directory: {pathway}")
    fn.mkdir(pathway)
    GLib.idle_add(fn.show_in_app_notification, self, "Downloading archlinux-keyring package...")

    def _download_and_install():
        try:
            command = (
                "wget https://archlinux.org/packages/core/any/archlinux-keyring/download"
                " --content-disposition -P" + pathway
            )
            fn.subprocess.Popen(command, shell=True).wait()
            fn.log_info("archlinux-keyring download completed")
            GLib.idle_add(fn.show_in_app_notification, self, "Download completed, installing package...")
            files = [f for f in fn.listdir(pathway) if f.endswith(".pkg.tar.zst")]
            if not files:
                raise Exception("No files found after download")
            package_file = fn.os.path.join(pathway, files[0])
            fn.debug_print(f"Found package: {package_file}")
            if not fn.os.path.exists(package_file):
                raise Exception(f"Package file not found: {package_file}")
            script = f"sudo pacman -U {package_file} --noconfirm; read -p 'Press Enter to close...'"
            process = fn.subprocess.Popen(
                ["alacritty", "-e", "bash", "-c", script],
                env=fn.get_terminal_env(),
            )
            GLib.idle_add(fn.show_in_app_notification, self, "Installation started...")
            process.wait()
            fn.log_success("archlinux-keyring installed")
            GLib.idle_add(fn.show_in_app_notification, self, "archlinux-keyring installed")
        except Exception as error:
            fn.log_error(f"Error: {error}")
            GLib.idle_add(fn.show_in_app_notification, self, f"Installation failed: {error}")
        finally:
            try:
                fn.shutil.rmtree(pathway)
                fn.debug_print("Temporary files cleaned up")
            except Exception as error:
                fn.log_warn(f"Cleanup failed: {error}")

    fn.threading.Thread(target=_download_and_install, daemon=True).start()


def on_click_fix_pacman_keys(self, _widget):
    fn.log_subsection("Fixing pacman keys...")
    cmd = "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/bin/fix-pacman-databases-and-keys'"
    _run_terminal(self, cmd, "Pacman keys fixed")


# Mirror & System Management
def on_click_probe(self, _widget):
    fn.log_subsection("Running hardware probe...")
    cmd = "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/bin/probe'"
    _run_terminal(self, cmd, "Probe link has been created", "Running hardware probe...")


def on_click_fix_mainstream(self, _widget):
    fn.log_subsection("Setting mainstream servers...")

    def _wait():
        fn.subprocess.Popen(
            ["alacritty", "-e", "/usr/share/archlinux-tweak-tool/data/bin/set-mainstream-servers"]
        ).wait()
        fn.log_success("Mainstream servers have been saved")
        try:
            with open(fn.mirrorlist, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        fn.log_info_concise(f"  {line}")
        except Exception as error:
            fn.log_warn(f"Could not read mirrorlist: {error}")
        GLib.idle_add(fn.show_in_app_notification, self, "Mainstream servers have been saved")

    fn.threading.Thread(target=_wait, daemon=True).start()


def on_click_reset_mirrorlist(self, _widget):
    fn.log_subsection("Resetting mirrorlist...")
    try:
        if fn.path.isfile(fn.mirrorlist + "-bak"):
            fn.log_info_concise(f"  From: {fn.mirrorlist}-bak")
            fn.log_info_concise(f"  To:   {fn.mirrorlist}")
            fn.shutil.copy(fn.mirrorlist + "-bak", fn.mirrorlist)
    except Exception as error:
        fn.log_warn(f"Restore from backup failed: {error}")
    fn.log_success("Original mirrorlist restored")
    GLib.idle_add(
        fn.show_in_app_notification, self, "Your original mirrorlist is back"
    )
    cmd = f"alacritty -e bash -c 'cat {fn.mirrorlist}; echo \"\"; read -p \"Press Enter to close...\"'"
    _run_terminal(self, cmd, "Mirrorlist displayed")


def on_click_get_arch_mirrors(self, _widget):
    fn.log_subsection("Setting fastest Arch Linux mirrors with reflector...")
    cmd = "alacritty -e /usr/share/archlinux-tweak-tool/data/bin/archlinux-get-mirrors-reflector"
    _run_terminal(self, cmd, "Fastest Arch Linux servers saved - reflector")


def on_click_get_arch_mirrors2(self, _widget):
    fn.log_subsection("Setting fastest Arch Linux mirrors with rate-mirrors...")
    cmd = "alacritty -e /usr/share/archlinux-tweak-tool/data/bin/archlinux-get-mirrors-rate-mirrors"
    _run_terminal(self, cmd, "Fastest Arch Linux servers saved - rate-mirrors")


# Pacman Configuration
def on_click_fix_pacman_conf(self, _widget):
    fn.log_subsection("Fixing pacman.conf...")
    cmd = "alacritty -e /usr/share/archlinux-tweak-tool/data/bin/att-fix-pacman-conf"
    _run_terminal(self, cmd, "Saved the original /etc/pacman.conf")


def on_click_fix_pacman_gpg_conf(self, _widget):
    fn.log_subsection("Resetting gpg.conf...")
    base_dir = fn.os.path.dirname(fn.os.path.abspath(__file__))
    gpg_conf_path = base_dir + "/data/gpg.conf"
    fn.log_info_concise(f"  From: {gpg_conf_path}")
    fn.log_info_concise(f"  To:   {fn.gpg_conf}")
    if not fn.path.isfile(fn.gpg_conf + "-bak"):
        fn.log_info_concise(f"  From: {fn.gpg_conf}")
        fn.log_info_concise(f"  To:   {fn.gpg_conf}-bak")
        fn.shutil.copy(fn.gpg_conf, fn.gpg_conf + "-bak")
        fn.log_info(f"Backup created: {fn.gpg_conf}-bak")
    fn.debug_print(f"Restoring from: {gpg_conf_path}")
    try:
        fn.shutil.copy(gpg_conf_path, fn.gpg_conf)
    except Exception as e:
        fn.log_error(f"Error restoring gpg.conf: {e}")
        return
    fn.log_success("/etc/pacman.d/gnupg/gpg.conf saved")
    GLib.idle_add(
        fn.show_in_app_notification,
        self,
        "The new /etc/pacman.d/gnupg/gpg.conf has been saved",
    )


def on_click_fix_pacman_gpg_conf_local(self, _widget):
    fn.log_subsection("Resetting local gpg.conf...")
    if not fn.path.isdir(fn.home + "/.gnupg"):
        try:
            fn.debug_print(f"Creating directory: {fn.home}/.gnupg")
            fn.makedirs(fn.home + "/.gnupg", 0o700)
            fn.permissions(fn.home + "/.gnupg")
        except Exception as error:
            fn.log_error(f"Error creating directory: {error}")

    if not fn.path.isfile(fn.gpg_conf_local):
        fn.log_info("No ~/.gnupg/gpg.conf found — no backup needed; a fresh copy will be created")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "No ~/.gnupg/gpg.conf found — a fresh copy will be created",
        )
    elif not fn.path.isfile(fn.gpg_conf_local + "-bak"):
        try:
            fn.log_info_concise(f"  From: {fn.gpg_conf_local}")
            fn.log_info_concise(f"  To:   {fn.gpg_conf_local}-bak")
            fn.shutil.copy(fn.gpg_conf_local, fn.gpg_conf_local + "-bak")
            fn.permissions(fn.gpg_conf_local + "-bak")
            fn.log_info(f"Backup created: {fn.gpg_conf_local}-bak")
        except Exception as error:
            fn.log_error(f"Error creating backup: {error}")

    base_dir = fn.os.path.dirname(fn.os.path.abspath(__file__))
    gpg_conf_local_path = base_dir + "/data/gpg.conf"
    fn.log_info_concise(f"  From: {gpg_conf_local_path}")
    fn.log_info_concise(f"  To:   {fn.gpg_conf_local}")
    try:
        fn.shutil.copy(gpg_conf_local_path, fn.gpg_conf_local)
        fn.os.chmod(fn.gpg_conf_local, 0o600)
        fn.permissions(fn.gpg_conf_local)
    except Exception as e:
        fn.log_error(f"Error restoring local gpg.conf: {e}")
        return
    fn.log_success("~/.gnupg/gpg.conf saved")
    GLib.idle_add(
        fn.show_in_app_notification,
        self,
        "The new ~/.gnupg/gpg.conf has been saved",
    )


def on_click_install_arch_mirrors(self, _widget):
    if fn.path.exists("/usr/bin/reflector"):
        fn.log_subsection("Removing reflector...")

        def _remove():
            fn.subprocess.Popen(
                "alacritty -e bash -c 'sudo pacman -Rns reflector; read -p \"Press Enter to close...\"'",
                shell=True,
            ).wait()
            fn.log_success("reflector removed")
            GLib.idle_add(fn.show_in_app_notification, self, "reflector removed")
            GLib.idle_add(self.btn_run_reflector.set_sensitive, False)
            GLib.idle_add(self.btn_install_mirrors.set_label, "Install reflector")

        GLib.idle_add(fn.show_in_app_notification, self, "Removing reflector...")
        fn.threading.Thread(target=_remove, daemon=True).start()
    else:
        fn.log_subsection("Installing reflector...")

        def _install():
            fn.subprocess.Popen(
                "alacritty -e bash -c 'sudo pacman -S --needed reflector; read -p \"Press Enter to close...\"'",
                shell=True,
            ).wait()
            fn.log_success("reflector installed")
            GLib.idle_add(fn.show_in_app_notification, self, "reflector installed")
            if fn.path.exists("/usr/bin/reflector"):
                GLib.idle_add(self.btn_run_reflector.set_sensitive, True)
                GLib.idle_add(self.btn_install_mirrors.set_label, "Remove reflector")

        GLib.idle_add(fn.show_in_app_notification, self, "Installing reflector...")
        fn.threading.Thread(target=_install, daemon=True).start()


def on_click_install_arch_mirrors2(self, _widget):
    if fn.path.exists("/usr/bin/rate-mirrors"):
        fn.log_subsection("Removing rate-mirrors...")

        def _remove():
            fn.subprocess.Popen(
                "alacritty -e bash -c 'sudo pacman -Rns rate-mirrors; read -p \"Press Enter to close...\"'",
                shell=True,
            ).wait()
            fn.log_success("rate-mirrors removed")
            GLib.idle_add(fn.show_in_app_notification, self, "rate-mirrors removed")
            GLib.idle_add(self.btn_run_rate_mirrors.set_sensitive, False)
            GLib.idle_add(self.btn_install_rate_mirrors.set_label, "Install rate-mirrors")

        GLib.idle_add(fn.show_in_app_notification, self, "Removing rate-mirrors...")
        fn.threading.Thread(target=_remove, daemon=True).start()
    else:
        fn.log_subsection("Installing rate-mirrors...")

        def _install():
            fn.subprocess.Popen(
                "alacritty -e bash -c 'sudo pacman -S --needed rate-mirrors; read -p \"Press Enter to close...\"'",
                shell=True,
            ).wait()
            fn.log_success("rate-mirrors installed")
            GLib.idle_add(fn.show_in_app_notification, self, "rate-mirrors installed")
            if fn.path.exists("/usr/bin/rate-mirrors"):
                GLib.idle_add(self.btn_run_rate_mirrors.set_sensitive, True)
                GLib.idle_add(self.btn_install_rate_mirrors.set_label, "Remove rate-mirrors")

        GLib.idle_add(fn.show_in_app_notification, self, "Installing rate-mirrors...")
        fn.threading.Thread(target=_install, daemon=True).start()


def on_update_pacman_databases_clicked(self, _widget):
    fn.log_subsection("Updating pacman databases...")
    cmd = "alacritty -e bash -c 'sudo pacman -Sy; read -p \"Press Enter to close...\"'"
    _run_terminal(self, cmd, "Pacman databases updated", "Updating pacman databases...")


def on_click_install_bibata_cursors(self, _widget):
    fn.log_subsection("Install Bibata Cursors")
    GLib.idle_add(fn.show_in_app_notification, self, "Installing Bibata cursors...")

    def _wait():
        fn.subprocess.Popen(
            "alacritty -e bash -c 'sudo pacman -S bibata-cursor-theme; read -p \"Press Enter to close...\"'",
            shell=True,
        ).wait()
        fn.log_success("Bibata cursors installed")
        GLib.idle_add(fn.show_in_app_notification, self, "Bibata cursors installed")
        GLib.idle_add(fn.refresh_all_cursor_dropdowns, self)

    fn.threading.Thread(target=_wait, daemon=True).start()


def on_click_remove_bibata_cursors(self, _widget):
    fn.log_subsection("Remove Bibata Cursors")
    if not fn.check_package_installed("bibata-cursor-theme"):
        fn.log_info("bibata-cursor-theme is not installed")
        fn.show_in_app_notification(self, "bibata-cursor-theme is not installed")
        return
    GLib.idle_add(fn.show_in_app_notification, self, "Removing Bibata cursors...")

    def _wait():
        fn.subprocess.Popen(
            "alacritty -e bash -c 'sudo pacman -R bibata-cursor-theme; read -p \"Press Enter to close...\"'",
            shell=True,
        ).wait()
        fn.log_success("Bibata cursors removed")
        GLib.idle_add(fn.show_in_app_notification, self, "Bibata cursors removed")
        GLib.idle_add(fn.refresh_all_cursor_dropdowns, self)

    fn.threading.Thread(target=_wait, daemon=True).start()
