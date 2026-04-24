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
    lines = []
    found_section = False
    found_inherits = False

    if fn.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    for pos, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "[Icon Theme]":
            found_section = True
        if stripped.startswith("Inherits="):
            lines[pos] = "Inherits=" + cursor + "\n"
            found_inherits = True
            break

    if not found_section:
        if lines and lines[-1].strip():
            lines.append("\n")
        lines.append("[Icon Theme]\n")

    if not found_inherits:
        lines.append("Inherits=" + cursor + "\n")

    _write_lines(path, lines)
    return path


def _set_xfce_cursor(path, cursor):
    """Set XFCE xsettings CursorThemeName, creating the property if needed."""
    if fn.path.isfile(path):
        tree = ET.parse(path)
        root = tree.getroot()
    else:
        _ensure_dir(path)
        root = ET.Element("channel", name="xsettings", version="1.0")
        tree = ET.ElementTree(root)

    net = None
    for child in root.findall("property"):
        if child.get("name") == "Net":
            net = child
            break
    if net is None:
        net = ET.SubElement(root, "property", name="Net", type="empty")

    cursor_prop = None
    for child in net.findall("property"):
        if child.get("name") == "CursorThemeName":
            cursor_prop = child
            break
    if cursor_prop is None:
        cursor_prop = ET.SubElement(net, "property", name="CursorThemeName")

    cursor_prop.set("type", "string")
    cursor_prop.set("value", cursor)
    tree.write(path, encoding="unicode", xml_declaration=True)
    if path.startswith(fn.home):
        fn.permissions(path)
    return path


def _set_gsettings_cursor(cursor):
    """Set cursor through gsettings when available."""
    username = fn.sudo_username
    pkexec_uid = fn.os.environ.get("PKEXEC_UID")

    if pkexec_uid:
        try:
            username = fn.pwd.getpwuid(int(pkexec_uid)).pw_name
        except Exception as error:
            print(error)

    try:
        user_info = fn.pwd.getpwnam(username)
        uid = user_info.pw_uid
        home = user_info.pw_dir
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

        result = fn.subprocess.run(
            command,
            check=False,
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.STDOUT,
        )
        if result.returncode == 0:
            return "gsettings:" + username + ":org.gnome.desktop.interface"
        print(result.stdout.decode(errors="ignore"))
    except Exception as error:
        print(error)
    return None


def _set_plasma_cursor(cursor):
    """Set KDE Plasma cursor configuration."""
    path = fn.home + "/.config/kcminputrc"
    return _set_key_value(path, "cursorTheme", cursor, section="Mouse")


def _set_sddm_cursor(cursor):
    """Set SDDM CursorTheme in existing config files."""
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

        existing_paths.append(path)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        has_cursor = False
        for pos, line in enumerate(lines):
            stripped = line.strip().lstrip("#").strip()
            if stripped.startswith(key) or stripped.startswith("CursorTheme ="):
                lines[pos] = new_line
                has_cursor = True

        if has_cursor:
            _write_lines(path, lines)
            changed.append(path)

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

    changed = []
    failed = []
    sessions = get_installed_sessions()

    def apply_target(label, target, *args, **kwargs):
        try:
            result = target(*args, **kwargs)
            if result:
                if isinstance(result, list):
                    changed.extend(result)
                else:
                    changed.append(result)
        except Exception as error:
            failed.append(label)
            print(label + ":", error)

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

    print("Cursor theme saved:", cursor)
    print("Installed sessions:", ", ".join(sorted(sessions)) or "none detected")
    for target in changed:
        print(" -", target)
    if failed:
        print("Failed cursor targets:", ", ".join(failed))

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
