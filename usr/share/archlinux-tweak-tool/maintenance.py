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
    """Set or append a simple key/value setting."""
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
    """Set Inherits in an XCursor index.theme file."""
    print(f"[INFO] Setting cursor '{cursor}' in {path}")
    lines = []
    found_section = False
    found_inherits = False

    if fn.path.isfile(path):
        print(f"[INFO] File exists: {path}")
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        print(f"[INFO] File does not exist, will create: {path}")

    for pos, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "[Icon Theme]":
            found_section = True
        if stripped.startswith("Inherits="):
            lines[pos] = "Inherits=" + cursor + "\n"
            found_inherits = True
            print(f"[INFO] Updated Inherits line with cursor '{cursor}'")
            break

    if not found_section:
        if lines and lines[-1].strip():
            lines.append("\n")
        lines.append("[Icon Theme]\n")
        print("[INFO] Added [Icon Theme] section")

    if not found_inherits:
        lines.append("Inherits=" + cursor + "\n")
        print(f"[INFO] Added Inherits line with cursor '{cursor}'")

    _write_lines(path, lines)
    print(f"[INFO] Successfully saved cursor '{cursor}' to {path}")
    return path


def _set_xfce_cursor(path, cursor):
    """Set XFCE xsettings CursorThemeName, creating the property if needed."""
    print(f"[INFO] Setting XFCE cursor '{cursor}' in {path}")
    if fn.path.isfile(path):
        print(f"[INFO] File exists: {path}")
        tree = ET.parse(path)
        root = tree.getroot()
    else:
        print(f"[INFO] File does not exist, creating: {path}")
        _ensure_dir(path)
        root = ET.Element("channel", name="xsettings", version="1.0")
        tree = ET.ElementTree(root)

    net = None
    for child in root.findall("property"):
        if child.get("name") == "Net":
            net = child
            break
    if net is None:
        print("[INFO] Creating Net property in XFCE config")
        net = ET.SubElement(root, "property", name="Net", type="empty")

    cursor_prop = None
    for child in net.findall("property"):
        if child.get("name") == "CursorThemeName":
            cursor_prop = child
            break
    if cursor_prop is None:
        print("[INFO] Creating CursorThemeName property in XFCE config")
        cursor_prop = ET.SubElement(net, "property", name="CursorThemeName")

    cursor_prop.set("type", "string")
    cursor_prop.set("value", cursor)
    print(f"[INFO] Set CursorThemeName to '{cursor}'")
    tree.write(path, encoding="unicode", xml_declaration=True)
    if path.startswith(fn.home):
        fn.permissions(path)
    print(f"[INFO] Successfully saved XFCE cursor '{cursor}' to {path}")
    return path


def _set_gsettings_cursor(cursor):
    """Set cursor through gsettings when available."""
    print(f"[INFO] Setting gsettings cursor '{cursor}'")
    username = fn.sudo_username
    pkexec_uid = fn.os.environ.get("PKEXEC_UID")

    if pkexec_uid:
        try:
            username = fn.pwd.getpwuid(int(pkexec_uid)).pw_name
            print(f"[INFO] Using PKEXEC_UID username: {username}")
        except Exception as error:
            print(f"[ERROR] Could not get username from PKEXEC_UID: {error}")

    try:
        user_info = fn.pwd.getpwnam(username)
        uid = user_info.pw_uid
        home = user_info.pw_dir
        print(f"[INFO] Setting cursor for user: {username} (uid: {uid})")
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

        print(f"[INFO] Executing gsettings command for org.gnome.desktop.interface")
        result = fn.subprocess.run(
            command,
            check=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        if result.returncode == 0:
            print(f"[INFO] Successfully set gsettings cursor to '{cursor}'")
            return "gsettings:" + username + ":org.gnome.desktop.interface"
        else:
            output = result.stdout.decode(errors="ignore")
            print(f"[ERROR] gsettings failed: {output}")
    except Exception as error:
        print(f"[ERROR] gsettings error: {error}")
    return None


def _set_plasma_cursor(cursor):
    """Set KDE Plasma cursor configuration."""
    print(f"[INFO] Setting KDE Plasma cursor '{cursor}'")
    path = fn.home + "/.config/kcminputrc"
    print(f"[INFO] Updating KDE Plasma config: {path}")
    result = _set_key_value(path, "cursorTheme", cursor, section="Mouse")
    if result:
        print(f"[INFO] Successfully set KDE Plasma cursor to '{cursor}'")
    return result


def _set_sddm_cursor(cursor):
    """Set SDDM CursorTheme in existing config files."""
    print(f"[INFO] Setting SDDM cursor '{cursor}'")
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

        print(f"[INFO] Processing SDDM config: {path}")
        existing_paths.append(path)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        has_cursor = False
        for pos, line in enumerate(lines):
            stripped = line.strip().lstrip("#").strip()
            if stripped.startswith(key) or stripped.startswith("CursorTheme ="):
                lines[pos] = new_line
                has_cursor = True
                print(f"[INFO] Updated CursorTheme in {path}")

        if has_cursor:
            _write_lines(path, lines)
            changed.append(path)
            print(f"[INFO] Successfully saved SDDM cursor '{cursor}' to {path}")

    if changed or not existing_paths:
        return changed

    path = existing_paths[0]
    return [_set_key_value(path, "CursorTheme", cursor, section="Theme")]


def get_installed_sessions():
    """Read installed X11 and Wayland desktop session names."""
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
                print(error)

    return sessions


def check_cursor_global(lists, value):
    """find name of global cursor"""
    if fn.path.isfile(fn.icons_default):
        try:
            pos = fn.get_position(lists, value)
            val = lists[pos].strip()
            return val
        except Exception as error:
            print(error)


def check_parallel_downloads(lists, value):
    """find number of parellel downloads"""
    if fn.path.isfile(fn.pacman):
        try:
            pos = fn.get_position(lists, value)
            val = lists[pos].strip()
            return val
        except Exception as error:
            print(error)


def set_global_cursor(self, cursor):
    """Set cursor in common user and desktop-specific configuration files."""
    if not cursor:
        fn.show_in_app_notification(self, "Select a cursor theme first")
        return

    print(f"[INFO] Starting global cursor application: {cursor}")
    changed = []
    failed = []
    sessions = get_installed_sessions()
    print(f"[INFO] Detected installed sessions: {', '.join(sorted(sessions)) or 'none'}")

    def apply_target(label, target, *args, **kwargs):
        try:
            print(f"[INFO] Applying cursor to {label}...")
            result = target(*args, **kwargs)
            if result:
                if isinstance(result, list):
                    changed.extend(result)
                else:
                    changed.append(result)
            print(f"[INFO] Successfully applied cursor to {label}")
        except Exception as error:
            failed.append(label)
            print(f"[ERROR] Failed to apply cursor to {label}: {error}")

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

    print("=" * 70)
    print(f"[INFO] Cursor theme successfully saved: {cursor}")
    print(f"[INFO] Modified locations:")
    for target in changed:
        print(f"[INFO]  - {target}")
    if failed:
        print(f"[WARNING] Failed cursor targets: {', '.join(failed)}")
    print("=" * 70)

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
    coms = []
    _m = combo.get_model(); _m.splice(0, _m.get_n_items(), [])
    for item in fn.listdir("/usr/share/icons/"):
        if fn.path_check("/usr/share/icons/" + item + "/cursors/"):
            coms.append(item)
            coms.sort()
    lines = fn.get_lines(fn.icons_default)
    try:
        cursor_theme = check_cursor_global(lines, "Inherits=").split("=")[1]
    except IndexError:
        cursor_theme = ""

    coms.sort()
    for i, item in enumerate(coms):
        combo.get_model().append(item)
        if cursor_theme.lower() == item.lower():
            combo.set_selected(i)


def set_parallel_downloads(self, widget):
    """set number of parallel downloads in pacman.conf"""
    if fn.path.isfile(fn.pacman):
        try:
            with open(fn.pacman, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            par_downloads = fn.get_combo_text(self.parallel_downloads)
            pos_par_down = fn.get_position(lines, "ParallelDownloads")
            lines[pos_par_down] = "ParallelDownloads = " + par_downloads + "\n"

            with open(fn.pacman, "w", encoding="utf-8") as f:
                f.writelines(lines)
                f.close()
            print("Saved to /etc/pacman.conf")
            print(lines[pos_par_down])
            fn.show_in_app_notification(self, "Settings Saved Successfully")

            # GLib.idle_add(fn.messagebox,self, "Success!!", "Settings applied successfully")
        except Exception as error:
            print(error)
            fn.messagebox(
                self,
                "Failed!!",
                'There seems to have been a problem in "set_parallel_downloads"',
            )


def pop_parallel_downloads(self):
    """populate parallel downloads for pacman"""
    if fn.path.isfile(fn.pacman):
        try:
            with open(fn.pacman, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
        except Exception as error:
            print(error)
            fn.messagebox(
                self,
                "Failed!!",
                'There seems to have been a problem in "pop_parallel_downloads"',
            )
    try:
        parallel_downloads = check_parallel_downloads(lines, "ParallelDownloads").split(
            "="
        )[1]
        active_number = int(parallel_downloads) - 1
        return active_number
    except IndexError:
        active_number = ""


# ====================================================================
# ====================================================================
# ====================================================================
#                   CALLBACK FUNCTIONS
# ====================================================================
# ====================================================================
# ====================================================================

# System Maintenance
def on_click_apply_global_cursor(self, widget):
    print("[INFO] Starting global cursor application")
    try:
        cursor = fn.get_combo_text(self.cursor_themes)
        print(f"[INFO] Selected cursor theme: {cursor}")
        print("[INFO] Applying global cursor theme...")
        set_global_cursor(self, cursor)
        print(f"[INFO] Cursor '{cursor}' is saved in /usr/share/icons/default")
        print("[INFO] Global cursor theme applied successfully")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Cursor is saved globally",
        )
    except Exception as error:
        print(f"[ERROR] Failed to apply global cursor: {error}")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            f"Failed to apply cursor: {error}",
        )


def on_click_update_system(self, widget):
    try:
        print("[INFO] Starting system update")
        print("[INFO] Installing alacritty terminal...")
        fn.install_package(self, "alacritty")
        print("[INFO] Launching system update...")
        GLib.idle_add(fn.show_in_app_notification, self, "Starting system update...")
        fn.subprocess.call(
            "alacritty -e bash -c 'sudo pacman -Syu; echo \"\"; echo \"=== Update complete ===\"; read -p \"Press Enter to close...\"'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("[INFO] System update completed")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "System update completed",
        )
    except Exception as error:
        print(f"[ERROR] Update system failed: {error}")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            f"Update failed: {error}",
        )


def on_click_clean_cache(self, widget):
    try:
        print("[INFO] Starting pacman cache cleanup")
        print("[INFO] Installing alacritty terminal...")
        fn.install_package(self, "alacritty")
        print("[INFO] Launching pacman cache cleanup...")
        GLib.idle_add(fn.show_in_app_notification, self, "Starting cache cleanup...")
        fn.subprocess.call(
            "alacritty -e bash -c 'sudo pacman -Sc; echo \"\"; echo \"=== Clean complete ===\"; read -p \"Press Enter to close...\"'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("[INFO] Pacman cache cleanup completed")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Pacman cache cleaned",
        )
    except Exception as error:
        print(f"[ERROR] Clean cache failed: {error}")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            f"Cleanup failed: {error}",
        )


def on_click_remove_pacman_lock(self, widget):
    try:
        print("[INFO] Starting pacman lock removal")
        print("[INFO] Installing alacritty terminal...")
        fn.install_package(self, "alacritty")
        print("[INFO] Checking pacman lock file: /var/lib/pacman/db.lck")
        print("[INFO] Launching pacman lock removal...")
        GLib.idle_add(fn.show_in_app_notification, self, "Removing pacman lock...")
        fn.subprocess.call(
            "alacritty -e bash -c 'sudo rm -f /var/lib/pacman/db.lck; echo \"\"; echo \"=== Lock removed ===\"; read -p \"Press Enter to close...\"'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("[INFO] Pacman lock removal completed")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Pacman lock removed",
        )
    except Exception as error:
        print(f"[ERROR] Remove pacman lock failed: {error}")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            f"Lock removal failed: {error}",
        )


# Pacman Keyring Management
def on_click_install_arch_keyring(self, widget):
    print("[INFO] Starting local archlinux-keyring installation")
    GLib.idle_add(fn.show_in_app_notification, self, "Starting archlinux-keyring installation...")
    try:
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pathway = base_dir + "/data/arch/packages/keyring/"
        print(f"[INFO] Package pathway: {pathway}")
        print("[INFO] Searching for archlinux-keyring package...")
        files = fn.listdir(pathway)
        if not files:
            raise Exception("No package files found in pathway")
        package_file = pathway + str(files).strip("[]'")
        print(f"[INFO] Found package: {package_file}")
        print(f"[INFO] Package size check...")
        if fn.os.path.exists(package_file):
            size = fn.os.path.getsize(package_file)
            print(f"[INFO] Package file size: {size} bytes")
        else:
            raise Exception(f"Package file not found: {package_file}")
        print("[INFO] Starting package installation...")
        GLib.idle_add(fn.show_in_app_notification, self, "Installing archlinux-keyring...")
        fn.install_local_package(self, package_file)
    except Exception as error:
        print(f"[ERROR] Local installation failed: {error}")
        GLib.idle_add(fn.show_in_app_notification, self, f"Installation failed: {error}")


def on_click_install_arch_keyring_online(self, widget):
    print("[INFO] Starting online archlinux-keyring installation")
    pathway = "/tmp/att-installation/"
    print(f"[INFO] Creating temporary directory: {pathway}")
    fn.mkdir(pathway)
    command = (
        "wget https://archlinux.org/packages/core/any/archlinux-keyring/download --content-disposition -P"
        + pathway
    )
    try:
        print("[INFO] Downloading archlinux-keyring package...")
        GLib.idle_add(fn.show_in_app_notification, self, "Downloading archlinux-keyring package...")
        fn.subprocess.call(
            command,
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("[INFO] Download completed successfully")
        GLib.idle_add(fn.show_in_app_notification, self, "Download completed, installing package...")
        print("[INFO] Locating downloaded package file...")
        files = fn.listdir(pathway)
        if not files:
            raise Exception("No files found after download")
        package_file = pathway + str(files).strip("[]'")
        print(f"[INFO] Found package: {package_file}")
        if not fn.os.path.exists(package_file):
            raise Exception(f"Package file not found: {package_file}")
        print("[INFO] Starting package installation...")
        fn.install_local_package(self, package_file)
    except Exception as error:
        print(f"[ERROR] Installation failed: {error}")
        GLib.idle_add(fn.show_in_app_notification, self, f"Installation failed: {error}")
    finally:
        print("[INFO] Cleaning up temporary files...")
        try:
            fn.shutil.rmtree(pathway)
            print("[INFO] Cleanup completed")
        except Exception as error:
            print(f"[WARNING] Cleanup failed: {error}")


def on_click_fix_pacman_keys(self, widget):
    fn.install_package(self, "alacritty")
    try:
        fn.subprocess.call(
            "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/any/fix-pacman-databases-and-keys; read -p \"Press Enter to close...\"'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("Pacman has been reset (gpg, libraries,keys)")
        GLib.idle_add(fn.show_in_app_notification, self, "Pacman keys fixed")
    except Exception as error:
        print(error)


# Mirror & System Management
def on_click_probe(self, widget):
    print("[INFO] Starting hardware probe")
    print("[INFO] Installing hw-probe package...")
    fn.install_package(self, "hw-probe")
    print("[INFO] Installing alacritty terminal...")
    fn.install_package(self, "alacritty")
    try:
        print("[INFO] Launching hardware probe...")
        GLib.idle_add(fn.show_in_app_notification, self, "Running hardware probe...")
        fn.subprocess.call(
            "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/arco/bin/arcolinux-probe; read -p \"Press Enter to close...\"'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("[INFO] Probe link has been created")
        GLib.idle_add(
            fn.show_in_app_notification, self, "Probe link has been created"
        )
    except Exception as error:
        print(f"[ERROR] Hardware probe failed: {error}")
        GLib.idle_add(
            fn.show_in_app_notification, self, f"Probe failed: {error}"
        )


def on_click_fix_mainstream(self, widget):
    fn.install_package(self, "alacritty")
    try:
        command = "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/any/set-mainstream-servers; read -p \"Press Enter to close...\"'"
        fn.subprocess.call(
            command,
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("Mainstream servers have been set")
        GLib.idle_add(
            fn.show_in_app_notification, self, "Mainstream servers have been saved"
        )
    except Exception as error:
        print(error)


def on_click_reset_mirrorlist(self, widget):
    try:
        if fn.path.isfile(fn.mirrorlist + ".bak"):
            fn.shutil.copy(fn.mirrorlist + ".bak", fn.mirrorlist)
    except Exception as error:
        print(error)
    print("Your original mirrorlist is back")
    GLib.idle_add(
        fn.show_in_app_notification, self, "Your original mirrorlist is back"
    )
    fn.install_package(self, "alacritty")
    try:
        fn.subprocess.call(
            f"alacritty -e bash -c 'cat {fn.mirrorlist}; echo \"\"; read -p \"Press Enter to close...\"'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
    except Exception as error:
        print(error)


def on_click_get_arch_mirrors(self, widget):
    fn.install_package(self, "alacritty")
    try:
        fn.install_package(self, "reflector")
        fn.subprocess.call(
            "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/any/archlinux-get-mirrors-reflector; read -p \"Press Enter to close...\"'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("Fastest Arch Linux servers have been set using reflector")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Fastest Arch Linux servers saved - reflector",
        )
    except:
        print("Install alacritty")


def on_click_get_arch_mirrors2(self, widget):
    fn.install_package(self, "alacritty")
    try:
        fn.subprocess.call(
            "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/any/archlinux-get-mirrors-rate-mirrors; read -p \"Press Enter to close...\"'",
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("Fastest Arch Linux servers have been set using rate-mirrors")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Fastest Arch Linux servers saved - rate-mirrors",
        )
    except Exception as error:
        print(error)


# Pacman Configuration
def on_click_fix_sddm_conf(self, widget):
    fn.install_package(self, "alacritty")
    try:
        command = "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/arco/bin/arcolinux-fix-sddm-config"
        fn.subprocess.call(
            command,
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("We use the default setup from plasma")
        print("Two files:")
        print(" - /etc/sddm.conf")
        print(" - /etc/sddm.d.conf/kde_settings.conf")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Saved the original SDDM configuration",
        )
    except:
        print("Install alacritty")


def on_click_fix_pacman_conf(self, widget):
    try:
        command = "alacritty --hold -e /usr/local/bin/arcolinux-fix-pacman-conf"
        fn.subprocess.call(
            command,
            shell=True,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        print("Saved the original /etc/pacman.conf")
        GLib.idle_add(
            fn.show_in_app_notification, self, "Saved the original /etc/pacman.conf"
        )
    except Exception as error:
        print(error)


def on_click_fix_pacman_gpg_conf(self, widget):
    print("[INFO] Starting gpg.conf backup and reset")
    if not fn.path.isfile(fn.gpg_conf + ".bak"):
        print(f"[INFO] Creating backup of current gpg.conf to {fn.gpg_conf}.bak")
        fn.shutil.copy(fn.gpg_conf, fn.gpg_conf + ".bak")
    print(f"[INFO] Restoring original gpg.conf from {fn.gpg_conf_original}")
    print("[INFO] Content of original gpg.conf:")
    print("=" * 70)
    try:
        with open(fn.gpg_conf_original, 'r') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"[ERROR] Could not read gpg.conf: {e}")
    print("=" * 70)
    fn.shutil.copy(fn.gpg_conf_original, fn.gpg_conf)
    print("[INFO] The new /etc/pacman.d/gnupg/gpg.conf has been saved")
    print("[INFO] Backup is in /etc/pacman.d/gnupg/gpg.conf.bak")
    print("[INFO] We only add servers to the config")
    GLib.idle_add(
        fn.show_in_app_notification,
        self,
        "The new /etc/pacman.d/gnupg/gpg.conf has been saved",
    )


def on_click_fix_pacman_gpg_conf_local(self, widget):
    print("[INFO] Starting local gpg.conf backup and reset")
    if not fn.path.isdir(fn.home + "/.gnupg"):
        try:
            print(f"[INFO] Creating directory: {fn.home}/.gnupg")
            fn.makedirs(fn.home + "/.gnupg", 0o766)
            fn.permissions(fn.home + "/.gnupg")
            print("[INFO] Directory created and permissions set")
        except Exception as error:
            print(f"[ERROR] Failed to create directory: {error}")

    if not fn.path.isfile(fn.gpg_conf_local + ".bak"):
        try:
            print(f"[INFO] Creating backup of current gpg.conf to {fn.gpg_conf_local}.bak")
            fn.shutil.copy(fn.gpg_conf_local, fn.gpg_conf_local + ".bak")
            fn.permissions(fn.gpg_conf_local + ".bak")
            print("[INFO] Backup created successfully")
        except Exception as error:
            print(f"[ERROR] Failed to create backup: {error}")

    print(f"[INFO] Restoring original gpg.conf from {fn.gpg_conf_local_original}")
    print("[INFO] Content of original local gpg.conf:")
    print("=" * 70)
    try:
        with open(fn.gpg_conf_local_original, 'r') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"[ERROR] Could not read local gpg.conf: {e}")
    print("=" * 70)
    fn.shutil.copy(fn.gpg_conf_local_original, fn.gpg_conf_local)
    fn.permissions(fn.gpg_conf_local)
    print("[INFO] The new ~/.gnupg/gpg.conf has been saved")
    print("[INFO] Backup is in ~/.gnupg/gpg.conf.bak")
    print("[INFO] We only add servers to the config")
    GLib.idle_add(
        fn.show_in_app_notification,
        self,
        "The new ~/.gnupg/gpg.conf has been saved",
    )


def on_click_install_arch_mirrors(self, widget):
    fn.install_package(self, "reflector")
    self.btn_run_reflector.set_sensitive(True)


def on_click_install_arch_mirrors2(self, widget):
    fn.install_package(self, "rate-mirrors")
    self.btn_run_rate_mirrors.set_sensitive(True)


def on_update_pacman_databases_clicked(self, Widget):
    fn.show_in_app_notification(self, "Opening terminal to update pacman databases")
    fn.subprocess.Popen(
        ["alacritty", "-e", "bash", "-c", "sudo pacman -Sy; read -p 'Press Enter to exit...'"],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )


# Repository Management
def on_arcolinux_clicked(self, widget):
    fn.install_arcolinux(self)
    print("ArcoLinux repo added + activated")
    fn.show_in_app_notification(
        self, "ArcoLinux repo added + activated"
    )
    self.on_pacman_arepo_toggle(self.arepo_button, True)
    self.on_pacman_a3p_toggle(self.a3prepo_button, True)
    fn.update_repos(self)
    fn.restart_program()


def on_pacman_atestrepo_toggle(self, widget, active):
    from pacman_functions import repo_exist, append_repo, toggle_test_repos
    if not repo_exist("[arcolinux_repo_testing]"):
        append_repo(self, fn.atestrepo)
        print("Repo has been added to /etc/pacman.conf")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Repo has been added to /etc/pacman.conf",
        )
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "arco_testing")


def on_pacman_arepo_toggle(self, widget, active):
    if not repo_exist("[arcolinux_repo]"):
        append_repo(self, fn.arepo)
        print("Repo has been added to /etc/pacman.conf")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Repo has been added to /etc/pacman.conf",
        )
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "arco_base")
            if check_arco_repos_active() is True:
                self.button_install.set_sensitive(True)
                self.button_reinstall.set_sensitive(True)
            else:
                self.button_install.set_sensitive(False)
                self.button_reinstall.set_sensitive(False)


def on_pacman_a3p_toggle(self, widget, active):
    if not repo_exist("[arcolinux_repo_3party]"):
        append_repo(self, fn.a3drepo)
        print("Repo has been added to /etc/pacman.conf")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Repo has been added to /etc/pacman.conf",
        )
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "arco_a3p")
            if check_arco_repos_active() is True:
                self.button_install.set_sensitive(True)
                self.button_reinstall.set_sensitive(True)
            else:
                self.button_install.set_sensitive(False)
                self.button_reinstall.set_sensitive(False)


def on_pacman_axl_toggle(self, widget, active):
    if not repo_exist("[arcolinux_repo_xlarge]"):
        append_repo(self, fn.axlrepo)
        print("Repo has been added to /etc/pacman.conf")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Repo has been added to /etc/pacman.conf",
        )
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "arco_axl")


def on_reborn_clicked(self, widget):
    fn.install_reborn(self)
    print("Reborn keyring and mirrors added")
    print("Restart Att and select the repos")
    GLib.idle_add(
        fn.show_in_app_notification, self, "Reborn keyring and mirrors added"
    )
    fn.update_repos(self)


def on_reborn_toggle(self, widget, active):
    if not repo_exist("[Reborn-OS]"):
        append_repo(self, fn.reborn_repo)
        print("Repo has been added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "reborn")


def on_garuda_clicked(self, widget):
    fn.install_chaotics(self)
    print("Chaotics keyring and mirrors added")
    print("Restart Att and select the repos")
    GLib.idle_add(
        fn.show_in_app_notification, self, "Chaotics keyring and mirrors added"
    )
    fn.update_repos(self)


def on_garuda_toggle(self, widget, active):
    if not repo_exist("[garuda]"):
        append_repo(self, fn.garuda_repo)
        print("Repo has been added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "garuda")


def on_chaotics_clicked(self, widget):
    fn.install_chaotics(self)
    print("Chaotics keyring and mirrors added")
    print("Restart Att and select the repos")
    GLib.idle_add(
        fn.show_in_app_notification, self, "Chaotics keyring and mirrors added"
    )
    fn.update_repos(self)


def on_chaotics_toggle(self, widget, active):
    if not repo_exist("[chaotic-aur]"):
        append_repo(self, fn.chaotics_repo)
        print("Repo has been added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "chaotics")
    fn.GLib.timeout_add(100, self.refresh_aur_buttons)


def on_endeavouros_clicked(self, widget):
    fn.install_endeavouros(self)
    print("EndeavourOS keyring and mirrors added")
    print("Restart Att and select the repo")
    fn.show_in_app_notification(self, "Restart Att and select the repo")
    fn.update_repos(self)


def on_endeavouros_toggle(self, widget, active):
    if not repo_exist("[endeavouros]"):
        append_repo(self, fn.endeavouros_repo)
        print("Repo has been added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "endeavouros")


def on_nemesis_toggle(self, widget, active):
    import desktopr_gui
    if not repo_exist("[nemesis_repo]"):
        append_repo(self, fn.nemesis_repo)
        print("Repo has been added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "nemesis")
    fn.update_repos(self)
    desktopr_gui.update_button_state(self, fn)
    fn.GLib.timeout_add(100, self.refresh_aur_buttons)


def on_pacman_toggle1(self, widget, active):
    if not repo_exist("[core-testing]"):
        append_repo(self, fn.arch_testing_repo)
        print("Repo has been added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "testing")


def on_pacman_toggle2(self, widget, active):
    if not repo_exist("[core]"):
        append_repo(self, fn.arch_core_repo)
        print("Repo has been added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "core")


def on_pacman_toggle3(self, widget, active):
    if not repo_exist("[extra]"):
        append_repo(self, fn.arch_extra_repo)
        print("Repo has been added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "extra")


def on_pacman_toggle4(self, widget, active):
    if not repo_exist("[extra-testing]"):
        append_repo(self, fn.arch_community_testing_repo)
        print("Repo has been added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "extra-testing")


def on_pacman_toggle5(self, widget, active):
    if not repo_exist("[extra-testing]"):
        append_repo(self, fn.arch_extra_testing_repo)
        print("Repo has been added to /etc/pacman.conf")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Repo has been added to /etc/pacman.conf",
        )
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "community")


def on_pacman_toggle6(self, widget, active):
    if not repo_exist("[multilib-testing]"):
        append_repo(self, fn.arch_multilib_testing_repo)
        print("Repo has been added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "multilib-testing")


def on_pacman_toggle7(self, widget, active):
    if not repo_exist("[multilib]"):
        append_repo(self, fn.arch_multilib_repo)
        print("Repo has been added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "multilib")


def custom_repo_clicked(self, widget):
    from pacman_functions import append_repo
    custom_repo_text = self.textview_custom_repo.get_buffer()
    startiter, enditer = custom_repo_text.get_bounds()
    repo_content = custom_repo_text.get_text(startiter, enditer, True)

    if len(repo_content.strip()) < 5:
        print("[INFO] No custom repo defined")
        fn.show_in_app_notification(self, "No custom repo defined")
        return

    print(repo_content)
    append_repo(self, repo_content)
    try:
        fn.update_repos(self)
    except Exception as error:
        print(error)
        print("Is the code correct? - check /etc/pacman.conf")


def blank_pacman(source, target):
    fn.shutil.copy(fn.pacman, fn.pacman + ".bak")
    if fn.distr == "arch":
        fn.shutil.copy(fn.blank_pacman_arch, fn.pacman)
    if fn.distr == "arcolinux":
        fn.shutil.copy(fn.blank_pacman_arco, fn.pacman)
    if fn.distr == "endeavouros":
        fn.shutil.copy(fn.blank_pacman_eos, fn.pacman)
    if fn.distr == "garuda":
        fn.shutil.copy(fn.blank_pacman_garuda, fn.pacman)
    print("We have now a blank pacman /etc/pacman.conf depending on the distro")
    print("ATT will reboot automatically")
    print(
        "Now add the repositories in the order you would like them to appear in the /etc/pacman.conf"
    )
    fn.restart_program()


def reset_pacman_local(self, widget):
    if fn.path.isfile(fn.pacman + ".bak"):
        fn.shutil.copy(fn.pacman + ".bak", fn.pacman)
        print("We have used /etc/pacman.conf.bak to reset /etc/pacman.conf")
        fn.show_in_app_notification(
            self, "Default Settings Applied - check in a terminal"
        )
    fn.GLib.timeout_add(500, self.update_repos_switches)


def reset_pacman_online(self, widget):
    if fn.distr == "arch":
        fn.shutil.copy(fn.pacman_arch, fn.pacman)
    if fn.distr == "arcolinux":
        fn.shutil.copy(fn.pacman_arco, fn.pacman)
    if fn.distr == "endeavouros":
        fn.shutil.copy(fn.pacman_eos, fn.pacman)
    if fn.distr == "garuda":
        fn.shutil.copy(fn.blank_pacman_garuda, fn.pacman)
    print("The online version of /etc/pacman.conf is saved")
    fn.show_in_app_notification(
        self, "Default Settings Applied - check in a terminal"
    )
    fn.GLib.timeout_add(500, self.update_repos_switches)


def edit_pacman_conf_clicked(self, widget):
    fn.show_in_app_notification(self, "Opening pacman.conf in terminal")
    fn.subprocess.Popen(
        ["alacritty", "-e", "sudo", "nano", fn.pacman],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )


def update_repos_switches(self):
    from pacman_functions import check_repo
    self.chaotics_switch.set_active(check_repo("[chaotic-aur]"))
    self.nemesis_switch.set_active(check_repo("[nemesis_repo]"))


# Mirror Management
def on_mirror_seed_repo_toggle(self, widget, active):
    from pacman_functions import mirror_exist, append_mirror, toggle_mirrorlist
    if not mirror_exist(
        "Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"
    ):
        append_mirror(self, fn.seedhostmirror)
    else:
        if self.opened is False:
            toggle_mirrorlist(self, widget.get_active(), "arco_mirror_seed")


def on_mirror_gitlab_repo_toggle(self, widget, active):
    if not mirror_exist(
        "Server = https://gitlab.com/arcolinux/$repo/-/raw/main/$arch"
    ):
        append_mirror(self, fn.seedhostmirror)
    else:
        if self.opened is False:
            toggle_mirrorlist(self, widget.get_active(), "arco_mirror_gitlab")


def on_mirror_belnet_repo_toggle(self, widget, active):
    if not mirror_exist(
        "Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"
    ):
        append_mirror(self, fn.seedhostmirror)
    else:
        if self.opened is False:
            toggle_mirrorlist(self, widget.get_active(), "arco_mirror_belnet")


def on_mirror_funami_repo_toggle(self, widget, active):
    if not mirror_exist(
        "Server = https://mirror.funami.tech/arcolinux/$repo/$arch"
    ):
        append_mirror(self, fn.seedhostmirror)
    else:
        if self.opened is False:
            toggle_mirrorlist(self, widget.get_active(), "arco_mirror_funami")


def on_mirror_jingk_repo_toggle(self, widget, active):
    if not mirror_exist(
        "Server = https://mirror.jingk.ai/arcolinux/$repo/$arch"
    ):
        append_mirror(self, fn.seedhostmirror)
    else:
        if self.opened is False:
            toggle_mirrorlist(self, widget.get_active(), "arco_mirror_jingk")


def on_mirror_accum_repo_toggle(self, widget, active):
    if not mirror_exist(
        "Server = https://mirror.accum.se/mirror/arcolinux.info/$repo/$arch"
    ):
        append_mirror(self, fn.seedhostmirror)
    else:
        if self.opened is False:
            toggle_mirrorlist(self, widget.get_active(), "arco_mirror_accum")


def on_mirror_aarnet_repo_toggle(self, widget, active):
    if not mirror_exist(
        "Server = https://mirror.aarnet.edu.au/pub/arcolinux/$repo/$arch"
    ):
        append_mirror(self, fn.aarnetmirror)
    else:
        if self.opened is False:
            toggle_mirrorlist(self, widget.get_active(), "arco_mirror_aarnet")


def on_click_apply_parallel_downloads(self, widget):
    set_parallel_downloads(self, widget)
