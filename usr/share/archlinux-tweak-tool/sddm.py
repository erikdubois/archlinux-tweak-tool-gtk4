# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
import os
from gi.repository import Gtk


def ensure_sddm_config(self):
    """Check if SDDM config files exist. If not, ask user for permission to create them."""
    files_missing = not fn.path.isfile(fn.sddm_default_d1) or not fn.path.isfile(fn.sddm_default_d2)

    if files_missing:
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text="SDDM Configuration Not Found"
        )
        dialog.format_secondary_text(
            "The SDDM configuration files are missing or incomplete:\n"
            "  • /etc/sddm.conf\n"
            "  • /etc/sddm.conf.d/kde_settings.conf\n\n"
            "Do you want to create them with default ATT settings?\n\n"
            "Your current settings (if any) will be backed up."
        )
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            try:
                fn.create_sddm_k_dir()
                fn.shutil.copy(fn.sddm_default_d1_kiro, fn.sddm_default_d1)
                fn.shutil.copy(fn.sddm_default_d2_kiro, fn.sddm_default_d2)
                print("[INFO] SDDM configuration files created successfully")
                return True
            except Exception as error:
                print(f"[ERROR] Failed to create SDDM files: {error}")
                fn.messagebox(self, "Error", f"Failed to create SDDM files: {error}")
                return False
        else:
            fn.show_in_app_notification(self, "SDDM configuration not modified")
            return False

    return True


def check_sddmk_complete():
    """see all variabeles are there"""
    # TODO:make nicer function
    try:
        with open(fn.sddm_default_d2, "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
        flag_a = False
        flag_s = False
        flag_u = False
        flag_t = False
        flag_c = False
        flag_ct = False
        flag_f = False

        for line in lines:
            if "[Autologin]" in line:
                flag_a = True
            if "Session=" in line:
                flag_s = True
            if "User=" in line:
                flag_u = True
            if "[Theme]" in line:
                flag_t = True
            if "Current=" in line:
                flag_c = True
            if "CursorTheme=" in line:
                flag_ct = True
            if "Font=" in line:
                flag_f = True

        if flag_a and flag_s and flag_u and flag_t and flag_c and flag_ct and flag_f:
            return True
        else:
            return False
    except FileNotFoundError:
        print(
            "---------------------------------------------------------------------------"
        )
        print("If ATT does not launch, type 'fix-sddm-conf' in a terminal and restart")
        print(
            "---------------------------------------------------------------------------"
        )


def check_sddmk_session(value):
    """what session in sddm"""
    with open(fn.sddm_default_d2, "r", encoding="utf-8") as myfile:
        lines = myfile.readlines()
        myfile.close()

    for line in lines:
        if value in line:
            return True
    return False


def insert_session(text):
    """insert session"""
    with open(fn.sddm_default_d2, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()
    pos = fn.get_position(lines, "[Autologin]")
    num = pos + 2

    lines.insert(num, text + "\n")

    with open(fn.sddm_default_d2, "w", encoding="utf-8") as f:
        f.writelines(lines)
        f.close()


def check_sddmk_user(value):
    """check user"""
    with open(fn.sddm_default_d2, "r", encoding="utf-8") as myfile:
        lines = myfile.readlines()
        myfile.close()

    for line in lines:
        if value in line:
            return True
    return False


def insert_user(text):
    """insert user"""
    with open(fn.sddm_default_d2, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()
    pos = fn.get_position(lines, "[Autologin]")
    num = pos + 3

    lines.insert(num, text + "\n")

    with open(fn.sddm_default_d2, "w", encoding="utf-8") as f:
        f.writelines(lines)
        f.close()


def check_sddm(lists, value):
    """check value in list"""
    pos = fn.get_position(lists, value)
    val = lists[pos].strip()
    return val


def set_sddm_value(self, lists, value, session, state, theme, cursor):
    """set values in sddm_default_d2"""
    try:
        com = fn.subprocess.run(
            ["sh", "-c", "su - " + fn.sudo_username + " -c groups"],
            check=True,
            shell=False,
            stdout=fn.subprocess.PIPE,
        )
        groups = com.stdout.decode().strip().split(" ")
        if "autologin" not in groups:
            fn.subprocess.run(
                ["gpasswd", "-a", fn.sudo_username, "autologin"],
                check=True,
                shell=False,
            )

        pos = fn.get_position(lists, "Session=")
        pos_session = fn.get_position(lists, "User=")

        if state:
            lists[pos_session] = "User=" + value + "\n"
            lists[pos] = "Session=" + session + "\n"
        else:
            if "#" not in lists[pos]:
                lists[pos] = "#" + lists[pos]
                lists[pos_session] = "#" + lists[pos_session]

        pos_theme = fn.get_position(lists, "Current=")
        lists[pos_theme] = "Current=" + theme + "\n"

        pos_theme = fn.get_position(lists, "CursorTheme=")
        lists[pos_theme] = "CursorTheme=" + cursor + "\n"

        with open(fn.sddm_default_d2, "w", encoding="utf-8") as f:
            f.writelines(lists)
            f.close()

    except Exception as error:
        print(error)
        fn.messagebox(
            self, "Failed!!", 'There seems to have been a problem in "set_sddm_value"'
        )


def set_user_autologin_value(self, lists, value, session, state):
    """set_user_autologin_value in sddm_default_d2"""
    try:
        fn.add_autologin_group(self)
        pos_session = fn.get_positions(lists, "Session=")
        pos_session = pos_session[-1]
        pos_user = fn.get_position(lists, "User=" + value)

        if state:
            lists[pos_user] = "User=" + value + "\n"
            lists[pos_session] = "Session=" + session + "\n"
        else:
            if "#" not in lists[pos_user]:
                lists[pos_user] = "#" + lists[pos_user]
                lists[pos_session] = "#" + lists[pos_session]

        with open(fn.sddm_default_d1, "w", encoding="utf-8") as f:
            f.writelines(lists)
            f.close()

    except Exception as error:
        print(error)
        fn.messagebox(
            self, "Failed!!", 'There seems to have been a problem in "set_sddm_value"'
        )


def get_sddm_lines(files):
    """get all lines"""
    if fn.path.isfile(files):
        with open(files, "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
        return lines


def pop_box(self, combo):
    """populate sddm box"""
    coms = []
    _m = combo.get_model(); _m.splice(0, _m.get_n_items(), [])

    """
    On Sway:
    - FileNotFoundError: [Errno 2] No such file or directory: '/usr/share/xsessions/'
    - Check for path /usr/share/wayland-sessions, also see desktoptr.py in check_desktop()
    """

    if os.path.exists("/usr/share/xsessions"):
        for items in fn.listdir("/usr/share/xsessions/"):
            coms.append(items.split(".")[0].lower())
        lines = get_sddm_lines(fn.sddm_default_d2)
    elif os.path.exists("/usr/share/wayland-sessions"):
        for items in fn.listdir("/usr/share/wayland-sessions/"):
            coms.append(items.split(".")[0].lower())
        lines = get_sddm_lines(fn.sddm_default_d2)

    try:
        if lines is not None:
            name = check_sddm(lines, "Session=").split("=")[1]
    except IndexError:
        name = ""

    coms.sort()
    if "i3-with-shmlog" in coms:
        coms.remove("i3-with-shmlog")
    if "openbox-kde" in coms:
        coms.remove("openbox-kde")
    if "cinnamon2d" in coms:
        coms.remove("cinnamon2d")
    if "icewm-session" in coms:
        coms.remove("icewm-session")

    coms.sort()
    for i, item in enumerate(coms):
        combo.get_model().append(item)
        if name.lower() == item.lower():
            combo.set_selected(i)


def pop_theme_box(self, combo):
    """populate theme box"""
    coms = []
    _m = combo.get_model(); _m.splice(0, _m.get_n_items(), [])

    if (
        fn.path.exists("/usr/share/sddm")
        and fn.path.exists(fn.sddm_default_d2)
        and fn.path.exists(fn.sddm_default_d1)
    ):
        for items in fn.listdir("/usr/share/sddm/themes/"):
            coms.append(items.split(".")[0])
        lines = get_sddm_lines(fn.sddm_default_d2)

        try:
            name = check_sddm(lines, "Current=").split("=")[1]
        except IndexError:
            name = ""

        coms.sort()
        for i, item in enumerate(coms):
            combo.get_model().append(item)
            if name.lower() == item.lower():
                combo.set_selected(i)


def pop_gtk_cursor_names(self, combo):
    """populate cursor names"""
    coms = []
    _m = combo.get_model(); _m.splice(0, _m.get_n_items(), [])

    if fn.path.isfile(fn.sddm_default_d2):
        for item in fn.listdir("/usr/share/icons/"):
            if fn.path_check("/usr/share/icons/" + item + "/cursors/"):
                coms.append(item)
                coms.sort()

        lines = fn.get_lines(fn.sddm_default_d2)
        try:
            cursor_theme = check_sddm(lines, "CursorTheme=").split("=")[1]
        except IndexError:
            cursor_theme = ""

        coms.sort()
        for i, item in enumerate(coms):
            combo.get_model().append(item)
            if cursor_theme.lower() == item.lower():
                combo.set_selected(i)


def pop_login_managers_combo(self, combo):
    """find with the active loginmanager"""
    options = ["sddm"]
    for option in options:
        self.login_managers_combo.get_model().append(option)
        if fn.check_content("sddm", "/etc/systemd/system/display-manager.service"):
            self.login_managers_combo.set_selected(0)
