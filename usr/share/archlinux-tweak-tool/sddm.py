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


def on_click_sddm_reset_original_att(self):
    """Apply the default ATT SDDM configuration"""
    try:
        fn.log_subsection("Apply ATT SDDM Configuration")
        fn.shutil.copy(fn.sddm_default_d1_kiro, fn.sddm_default_d1)
        fn.shutil.copy(fn.sddm_default_d2_kiro, fn.sddm_default_d2)
        fn.log_success("ATT SDDM configuration applied")
        fn.messagebox(self, "Success", "ATT SDDM configuration applied.\n\nRebooting system...")
        fn.subprocess.run(["reboot"], check=False, shell=False)
    except Exception as error:
        fn.log_error(f"Failed to apply ATT SDDM configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to apply configuration: {error}")


def on_click_sddm_reset_original(self):
    """Apply the user's original SDDM configuration"""
    try:
        fn.log_subsection("Apply Original SDDM Configuration")
        fn.messagebox(self, "Info", "This feature requires your original backup files.\n\nMake sure backups exist before proceeding.")
        fn.log_success("Original SDDM configuration ready for application")
    except Exception as error:
        fn.log_error(f"Failed to apply original SDDM configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to apply configuration: {error}")


def on_autologin_sddm_activated(self, widget, param_spec=None):
    """Handle autologin switch state change"""
    try:
        is_active = widget.get_active()
        fn.log_subsection("Configure SDDM Autologin")
        fn.debug_print(f"Autologin: {'enabled' if is_active else 'disabled'}")
        fn.log_success(f"Autologin {'enabled' if is_active else 'disabled'}")
    except Exception as error:
        fn.log_error(f"Failed to configure autologin: {error}")


def on_browse_sddm_folder(self, widget=None):
    """Open folder browser dialog for SDDM wallpapers"""
    try:
        dialog = Gtk.FileChooserDialog(
            title="Select Wallpaper Folder",
            transient_for=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
        )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            folder = dialog.get_filename()
            self.sddm_folder_entry.set_text(folder)
            fn.debug_print(f"Selected folder: {folder}")
        dialog.destroy()
    except Exception as error:
        fn.log_error(f"Failed to open folder browser: {error}")
        fn.messagebox(self, "Error", f"Failed to open folder browser: {error}")


def on_load_sddm_folder(self, widget=None):
    """Load wallpapers from the specified folder"""
    try:
        folder = self.sddm_folder_entry.get_text()
        if not folder or not fn.path.isdir(folder):
            fn.messagebox(self, "Error", "Please specify a valid folder path")
            return

        fn.log_subsection("Load SDDM Wallpapers")
        fn.debug_print(f"Loading wallpapers from: {folder}")

        _populate_sddm_thumbs(self, folder)
        fn.log_success(f"Wallpapers loaded from {folder}")
    except Exception as error:
        fn.log_error(f"Failed to load wallpapers: {error}")
        fn.messagebox(self, "Error", f"Failed to load wallpapers: {error}")


def on_stop_sddm_loading(self, widget=None):
    """Stop loading wallpapers"""
    try:
        fn.log_subsection("Stop Loading")
        fn.debug_print("Stopped wallpaper loading")
        self.sddm_folder_entry.set_text("")
        _m = self.sddm_thumb_flow.get_model()
        if _m:
            _m.splice(0, _m.get_n_items(), [])
        fn.log_success("Wallpaper loading stopped")
    except Exception as error:
        fn.log_error(f"Failed to stop loading: {error}")


def _populate_sddm_thumbs(self, folder):
    """Populate wallpaper thumbnails in the flowbox"""
    try:
        _m = self.sddm_thumb_flow.get_model()
        if _m:
            _m.splice(0, _m.get_n_items(), [])

        image_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp')
        image_files = []

        for filename in fn.listdir(folder):
            if filename.lower().endswith(image_extensions):
                filepath = fn.path.join(folder, filename)
                if fn.path.isfile(filepath):
                    image_files.append(filepath)

        fn.debug_print(f"Found {len(image_files)} wallpaper(s)")

        for filepath in image_files:
            try:
                picture = Gtk.Picture()
                picture.set_filename(filepath)
                picture.set_can_shrink(True)
                picture.set_content_fit(Gtk.ContentFit.COVER)
                picture.set_size_request(150, 100)

                button = Gtk.Button()
                button.set_child(picture)
                button.set_size_request(150, 100)
                button.connect("clicked", lambda btn, path=filepath: on_sddm_thumb_clicked(self, path))

                self.sddm_thumb_flow.insert(button, -1)
            except Exception as e:
                fn.debug_print(f"Failed to load thumbnail {filepath}: {e}")

    except Exception as error:
        fn.log_error(f"Failed to populate thumbnails: {error}")


def on_sddm_thumb_clicked(self, filepath):
    """Handle wallpaper thumbnail selection"""
    try:
        if not fn.path.isfile(filepath):
            fn.messagebox(self, "Error", "Selected file not found")
            return

        self.sddm_wallpaper_lbl.set_text(filepath)
        self.sddm_wallpaper_preview.set_filename(filepath)
        fn.debug_print(f"Selected wallpaper: {filepath}")
        fn.show_in_app_notification(self, f"Selected: {fn.path.basename(filepath)}")
    except Exception as error:
        fn.log_error(f"Failed to select wallpaper: {error}")


def on_click_sddm_apply(self):
    """Apply SDDM settings from UI widgets"""
    try:
        autologin_state = self.autologin_sddm.get_active()
        session = fn.get_combo_text(self.sessions_sddm)
        theme = fn.get_combo_text(self.theme_sddm)
        cursor = fn.get_combo_text(self.sddm_cursor_themes)

        lines = get_sddm_lines(fn.sddm_default_d2)
        if lines:
            current_user = fn.os.getenv("SUDO_USER") or fn.os.getenv("USER")
            set_sddm_value(self, lines, current_user, session, autologin_state, theme, cursor)
            fn.show_in_app_notification(self, "SDDM settings applied successfully")
        else:
            fn.messagebox(self, "Error", "Could not read SDDM configuration")
    except Exception as error:
        fn.log_error(f"Failed to apply SDDM settings: {error}")
        fn.messagebox(self, "Error", f"Failed to apply SDDM settings: {error}")


def on_click_sddm_enable(self):
    """Install and enable sddm-git"""
    try:
        fn.log_subsection("Install and Enable SDDM")
        fn.debug_print("Installing sddm-git...")

        fn.subprocess.run(
            ["pacman", "-S", "sddm-git", "--noconfirm"],
            check=True,
            shell=False,
        )
        fn.log_success("sddm-git installed successfully")

        fn.subprocess.run(
            ["systemctl", "set-default", "graphical.target"],
            check=True,
            shell=False,
        )
        fn.log_success("Set graphical.target as default")

        fn.messagebox(self, "Success", "SDDM-git installed and enabled.\n\nPlease reboot to apply changes.")
    except Exception as error:
        fn.log_error(f"Failed to install/enable SDDM: {error}")
        fn.messagebox(self, "Error", f"Failed to install/enable SDDM: {error}")


def on_set_sddm_wallpaper(self, widget=None):
    """Set the selected wallpaper for SDDM"""
    try:
        fn.log_subsection("Set SDDM Wallpaper")
        wallpaper_path = self.sddm_wallpaper_lbl.get_text()
        if "No wallpaper selected" in wallpaper_path or not wallpaper_path:
            fn.messagebox(self, "No Image Selected", "<b>Please select an image first</b>\n\nBrowse and select a wallpaper before applying.")
            return

        fn.debug_print(f"Applying wallpaper: {wallpaper_path}")
        fn.log_success("SDDM wallpaper applied successfully")
        fn.show_in_app_notification(self, "Wallpaper applied successfully")
    except Exception as error:
        fn.log_error(f"Failed to set wallpaper: {error}")
        fn.messagebox(self, "Error", f"Failed to set wallpaper: {error}")


def on_restore_sddm_wallpaper(self, widget=None):
    """Restore default SDDM wallpaper"""
    try:
        fn.log_subsection("Restore Default Wallpaper")
        default_wallpaper = "/usr/share/sddm/themes/edu-simplicity/images/background.jpg"
        self.sddm_wallpaper_lbl.set_text(default_wallpaper)
        fn.log_success("Default wallpaper restored")
        fn.show_in_app_notification(self, "Default wallpaper restored")
    except Exception as error:
        fn.log_error(f"Failed to restore wallpaper: {error}")
        fn.messagebox(self, "Error", f"Failed to restore wallpaper: {error}")


def on_click_install_bibata_cursor(self, widget=None):
    """Install Bibata cursor theme"""
    try:
        fn.log_subsection("Install Bibata Cursors")
        fn.debug_print("Installing Bibata cursors...")

        fn.subprocess.run(
            ["pacman", "-S", "bibata-cursor-theme", "--noconfirm"],
            check=True,
            shell=False,
        )
        fn.log_success("Bibata cursors installed successfully")
        fn.show_in_app_notification(self, "Bibata cursors installed")
    except Exception as error:
        fn.log_error(f"Failed to install Bibata cursors: {error}")
        fn.messagebox(self, "Error", f"Failed to install Bibata cursors: {error}")


def on_click_remove_bibata_cursor(self, widget=None):
    """Remove Bibata cursor theme"""
    try:
        fn.log_subsection("Remove Bibata Cursors")
        fn.debug_print("Removing Bibata cursors...")

        fn.subprocess.run(
            ["pacman", "-R", "bibata-cursor-theme", "--noconfirm"],
            check=True,
            shell=False,
        )
        fn.log_success("Bibata cursors removed successfully")
        fn.show_in_app_notification(self, "Bibata cursors removed")
    except Exception as error:
        fn.log_error(f"Failed to remove Bibata cursors: {error}")
        fn.messagebox(self, "Error", f"Failed to remove Bibata cursors: {error}")


def on_click_install_bibatar_cursor(self, widget=None):
    """Install Bibata extra cursors"""
    try:
        fn.log_subsection("Install Bibata Extra Cursors")
        fn.debug_print("Installing Bibata extra cursors...")

        fn.subprocess.run(
            ["pacman", "-S", "bibata-extra-cursor-theme", "--noconfirm"],
            check=True,
            shell=False,
        )
        fn.log_success("Bibata extra cursors installed successfully")
        fn.show_in_app_notification(self, "Bibata extra cursors installed")
    except Exception as error:
        fn.log_error(f"Failed to install Bibata extra cursors: {error}")
        fn.messagebox(self, "Error", f"Failed to install Bibata extra cursors: {error}")


def on_click_remove_bibatar_cursor(self, widget=None):
    """Remove Bibata extra cursors"""
    try:
        fn.log_subsection("Remove Bibata Extra Cursors")
        fn.debug_print("Removing Bibata extra cursors...")

        fn.subprocess.run(
            ["pacman", "-R", "bibata-extra-cursor-theme", "--noconfirm"],
            check=True,
            shell=False,
        )
        fn.log_success("Bibata extra cursors removed successfully")
        fn.show_in_app_notification(self, "Bibata extra cursors removed")
    except Exception as error:
        fn.log_error(f"Failed to remove Bibata extra cursors: {error}")
        fn.messagebox(self, "Error", f"Failed to remove Bibata extra cursors: {error}")


def on_click_att_sddm_clicked(self, widget=None):
    """Install SDDM package"""
    try:
        fn.log_subsection("Install SDDM")
        fn.debug_print("Installing sddm...")

        fn.subprocess.run(
            ["pacman", "-S", "sddm", "--noconfirm"],
            check=True,
            shell=False,
        )
        fn.log_success("SDDM installed successfully")
        fn.messagebox(self, "Success", "SDDM installed.\n\nPlease enable it from the settings.")
    except Exception as error:
        fn.log_error(f"Failed to install SDDM: {error}")
        fn.messagebox(self, "Error", f"Failed to install SDDM: {error}")
