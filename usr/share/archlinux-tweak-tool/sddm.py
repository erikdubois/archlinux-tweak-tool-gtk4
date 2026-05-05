# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import sys
import functions as fn
import os
from gi.repository import Gtk, Gio, Gdk, GdkPixbuf, Pango


def _refresh_cursor_theme_dropdown(self):
    try:
        fn.refresh_all_cursor_dropdowns(self)
    except Exception as error:
        fn.debug_print(f"Failed to refresh cursor dropdowns: {error}")


def check_sddmk_complete():
    """see all variabeles are there"""
    try:
        with open(fn.sddm_default_d2, "r", encoding="utf-8") as f:
            lines = f.readlines()
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
        fn.debug_print(
            "If ATT does not launch, type 'fix-sddm-conf' in a terminal and restart"
        )


def check_sddmk_session(value):
    """what session in sddm"""
    with open(fn.sddm_default_d2, "r", encoding="utf-8") as myfile:
        lines = myfile.readlines()

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

    for line in lines:
        if value in line:
            return True
    return False


def get_autologin_state():
    """Return True if SDDM autologin has a non-empty User= in [Autologin] section"""
    try:
        if not fn.path.isfile(fn.sddm_default_d2):
            return False
        with open(fn.sddm_default_d2, "r", encoding="utf-8") as f:
            lines = f.readlines()
        in_autologin = False
        for line in lines:
            if line.strip() == "[Autologin]":
                in_autologin = True
            elif line.startswith("["):
                in_autologin = False
            elif in_autologin and line.startswith("User="):
                return bool(line.split("=", 1)[1].strip())
        return False
    except Exception:
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
        if state:
            fn.subprocess.run(["groupadd", "-f", "autologin"], check=True, shell=False)
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
        fn.log_error(str(error))
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
        fn.log_error(str(error))
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
    _m = combo.get_model()
    _m.splice(0, _m.get_n_items(), [])

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
    _m = combo.get_model()
    _m.splice(0, _m.get_n_items(), [])

    if not fn.path.exists("/usr/share/sddm/themes/"):
        return

    for items in fn.listdir("/usr/share/sddm/themes/"):
        coms.append(items.split(".")[0])

    name = ""
    if fn.path.exists(fn.sddm_default_d2):
        lines = get_sddm_lines(fn.sddm_default_d2)
        try:
            name = check_sddm(lines, "Current=").split("=")[1]
        except (IndexError, TypeError):
            name = ""

    coms.sort()
    for i, item in enumerate(coms):
        combo.get_model().append(item)
        if name.lower() == item.lower():
            combo.set_selected(i)


def pop_gtk_cursor_names(combo):
    """populate cursor names"""
    _m = combo.get_model()
    _m.splice(0, _m.get_n_items(), [])

    if fn.path.isfile(fn.sddm_default_d2):
        lines = fn.get_lines(fn.sddm_default_d2)
        try:
            cursor_theme = check_sddm(lines, "CursorTheme=").split("=")[1]
        except IndexError:
            cursor_theme = ""

        for i, item in enumerate(fn.list_cursor_themes()):
            combo.get_model().append(item)
            if cursor_theme.lower() == item.lower():
                combo.set_selected(i)


def pop_login_managers_combo(self, combo):
    """find with the active loginmanager"""
    options = ["sddm"]
    for option in options:
        self.login_managers_combo.get_model().append(option)
        if fn.check_content("sddm", fn.display_manager_service):
            self.login_managers_combo.set_selected(0)


def on_click_sddm_reset_original_att(self, _widget=None):
    """Apply the default ATT SDDM configuration"""
    try:
        fn.log_subsection("Apply ATT SDDM Configuration")
        fn.create_sddm_k_dir()
        fn.log_info_concise(f"  From: {fn.sddm_default_d1_kiro}")
        fn.log_info_concise(f"  To:   {fn.sddm_default_d1}")
        fn.shutil.copy(fn.sddm_default_d1_kiro, fn.sddm_default_d1)
        fn.log_info_concise(f"  From: {fn.sddm_default_d2_kiro}")
        fn.log_info_concise(f"  To:   {fn.sddm_default_d2}")
        fn.shutil.copy(fn.sddm_default_d2_kiro, fn.sddm_default_d2)
        fn.log_success("ATT SDDM configuration applied")
        fn.messagebox(self, "Success", "ATT SDDM configuration applied.\n\nRestarting ATT...")
        fn.restart_program()
    except Exception as error:
        fn.log_error(f"Failed to apply ATT SDDM configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to apply configuration: {error}")


def on_click_sddm_reset_original(self, _widget=None):
    """Apply the user's original SDDM configuration"""
    try:
        fn.log_subsection("Apply Original SDDM Configuration")
        fn.messagebox(self, "Success", "Original SDDM configuration applied.\n\nRestarting ATT...")
        fn.restart_program()
    except Exception as error:
        fn.log_error(f"Failed to apply original SDDM configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to apply configuration: {error}")


def on_sddm_setting_changed(self, message, *_):
    fn.log_info(f"{message} — click 'Apply the above mentioned settings' to save")
    fn.show_in_app_notification(self, f"{message} — click 'Apply the above mentioned settings' to save")


def on_autologin_sddm_activated(self, widget, param_spec=None):
    """Handle autologin switch state change"""
    try:
        is_active = widget.get_active()
        state_str = "enabled" if is_active else "disabled"
        on_sddm_setting_changed(self, f"Autologin {state_str}")
    except Exception as error:
        fn.log_error(f"Failed to configure autologin: {error}")


def on_browse_sddm_folder(self, _widget=None):
    dialog = Gtk.FileDialog()
    dialog.set_title("Choose a folder with wallpapers")
    current = self.sddm_folder_entry.get_text().strip()
    start = current if fn.path.isdir(current) else fn.home
    dialog.set_initial_folder(Gio.File.new_for_path(start))
    dialog.select_folder(self, None, lambda d, result: _on_sddm_folder_response(self, d, result))


def _on_sddm_folder_response(self, dialog, result):
    try:
        folder = dialog.select_folder_finish(result)
        if folder:
            folder_path = folder.get_path()
            self.sddm_folder_entry.set_text(folder_path)
            _populate_sddm_thumbs(self, folder_path)
    except Exception:
        pass


def on_load_sddm_folder(self, _widget=None):
    folder_path = self.sddm_folder_entry.get_text().strip()
    if fn.path.isdir(folder_path):
        _populate_sddm_thumbs(self, folder_path)
    else:
        fn.show_in_app_notification(self, "Folder not found")


def on_stop_sddm_loading(self, _widget=None):
    self._sddm_load_gen = getattr(self, "_sddm_load_gen", 0) + 1


def _populate_sddm_thumbs(self, folder_path):
    self._sddm_load_gen = getattr(self, "_sddm_load_gen", 0) + 1
    current_gen = self._sddm_load_gen

    child = self.sddm_thumb_flow.get_first_child()
    while child is not None:
        next_child = child.get_next_sibling()
        self.sddm_thumb_flow.remove(child)
        child = next_child

    exts = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
    try:
        entries = sorted(fn.os.listdir(folder_path))
    except Exception:
        return

    image_paths = [
        fn.path.join(folder_path, name)
        for name in entries
        if name.lower().endswith(exts)
    ]

    idx = [0]

    def load_next():
        if self._sddm_load_gen != current_gen:
            return False
        if idx[0] >= len(image_paths):
            return False
        path = image_paths[idx[0]]
        idx[0] += 1
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, 160, 100, True)
            texture = Gdk.Texture.new_for_pixbuf(pixbuf)
            pic = Gtk.Picture.new_for_paintable(texture)
            pic.set_can_shrink(False)
            pic.set_size_request(160, 100)

            lbl = Gtk.Label()
            lbl.set_text(fn.path.basename(path))
            lbl.set_max_width_chars(18)
            lbl.set_ellipsize(Pango.EllipsizeMode.MIDDLE)

            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            box.set_margin_top(4)
            box.set_margin_bottom(4)
            box.set_margin_start(4)
            box.set_margin_end(4)
            box.append(pic)
            box.append(lbl)

            btn = Gtk.Button()
            btn.set_child(box)
            btn.connect("clicked", lambda w, p=path: on_sddm_thumb_clicked(self, w, p))
            self.sddm_thumb_flow.append(btn)
        except Exception:
            pass
        return True

    fn.GLib.idle_add(load_next)


def on_sddm_thumb_clicked(self, _widget, path):
    self.login_wallpaper_path = path
    self.sddm_wallpaper_lbl.set_text(path)
    self.sddm_wallpaper_preview.set_filename(path)
    self.sddm_wallpaper_preview.get_parent().set_visible(True)


def on_click_sddm_apply(self, _widget=None):
    """Apply SDDM settings from UI widgets"""
    import functions_sddm as _fs
    fn.log_subsection("Applying SDDM Settings")
    fn.debug_print("Running setup_sddm_config() from functions_sddm.py")
    _fs.setup_sddm_config(self, sys.modules["sddm"])
    try:
        autologin_state = self.autologin_sddm.get_active()
        session = fn.get_combo_text(self.sessions_sddm)
        theme = fn.get_combo_text(self.theme_sddm)
        cursor = fn.get_combo_text(self.sddm_cursor_themes)

        lines = get_sddm_lines(fn.sddm_default_d2)
        if lines:
            fn.debug_print(f"[DEBUG] Found {len(lines)} lines in config file")
            current_user = fn.sudo_username
            fn.debug_print(f"[DEBUG] Current user: {current_user}")
            set_sddm_value(self, lines, current_user, session, autologin_state, theme, cursor)
            fn.log_info_concise(f"  User:     {current_user}")
            fn.log_info_concise(f"  Session:  {session or 'default'}")
            fn.log_info_concise(f"  Theme:    {theme or 'default'}")
            fn.log_info_concise(f"  Cursor:   {cursor or 'default'}")
            fn.log_info_concise(f"  Autologin: {'enabled' if autologin_state else 'disabled'}")
            fn.log_info_concise(f"  Saved to: {fn.sddm_default_d2}")
            fn.debug_print("[DEBUG] Config file written successfully")
            fn.log_success("SDDM settings applied successfully")
            fn.show_in_app_notification(self, "SDDM settings applied successfully")
        else:
            fn.messagebox(self, "Error", "Could not read SDDM configuration")
    except Exception as error:
        fn.log_error(f"Failed to apply SDDM settings: {error}")
        fn.messagebox(self, "Error", f"Failed to apply SDDM settings: {error}")


def on_click_sddm_enable(self, _widget=None):
    """Install and enable sddm-git"""
    fn.log_subsection("Install and Enable SDDM")
    fn.show_in_app_notification(self, "Opening terminal to install and enable sddm-git...")
    cmd = "sudo pacman -S sddm-git; sudo systemctl set-default graphical.target; read -p 'Press Enter to close'"
    process = fn.subprocess.Popen(
        ["alacritty", "-e", "bash", "-c", cmd],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )

    def wait_and_notify():
        process.wait()
        fn.GLib.idle_add(fn.show_in_app_notification, self, "sddm-git install complete — please reboot")

    fn.threading.Thread(target=wait_and_notify, daemon=True).start()


def on_set_sddm_wallpaper(self, _widget=None):
    fn.log_subsection("Applying SDDM Wallpaper")
    simplicity_images = "/usr/share/sddm/themes/edu-simplicity/images"
    simplicity_conf = "/usr/share/sddm/themes/edu-simplicity/theme.conf"
    dest = simplicity_images + "/background.jpg"
    dest_bak = simplicity_images + "/background.jpg.bak"

    path = getattr(self, "login_wallpaper_path", None)
    if not path or not fn.path.isfile(path):
        fn.show_in_app_notification(self, "First choose a wallpaper image")
        return

    if not fn.path.isdir(simplicity_images):
        fn.show_in_app_notification(self, "Simplicity theme not found - install it first")
        return

    try:
        if fn.path.isfile(dest) and not fn.path.isfile(dest_bak):
            fn.log_info_concise(f"  From: {dest}")
            fn.log_info_concise(f"  To:   {dest_bak}")
            fn.shutil.copy(dest, dest_bak)
            fn.debug_print("[DEBUG] Backup created: " + dest_bak)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
        pixbuf.savev(dest, "jpeg", [], [])
        with open(simplicity_conf, "w", encoding="utf-8") as f:
            f.write("[General]\nbackground=images/background.jpg\n")
        fn.log_info_concise(f"  From: {path}")
        fn.log_info_concise(f"  To:   {dest}")
        fn.log_info_concise("  Theme: edu-simplicity")
        fn.debug_print("[DEBUG] Wallpaper saved and theme config updated")
        fn.log_success("Simplicity wallpaper applied")
        fn.show_in_app_notification(self, "Simplicity wallpaper applied")
    except Exception as error:
        fn.log_error(str(error))
        fn.show_in_app_notification(self, "Failed to apply wallpaper")


def on_restore_sddm_wallpaper(self, _widget=None):
    fn.log_subsection("Restoring Default SDDM Wallpaper")
    simplicity_images = "/usr/share/sddm/themes/edu-simplicity/images"
    simplicity_conf = "/usr/share/sddm/themes/edu-simplicity/theme.conf"
    dest = simplicity_images + "/background.jpg"
    dest_bak = simplicity_images + "/background.jpg.bak"

    if not fn.path.isdir(simplicity_images):
        fn.show_in_app_notification(self, "Simplicity theme not found - install it first")
        return

    if not fn.path.isfile(dest_bak):
        fn.show_in_app_notification(self, "No backup found - apply a wallpaper first")
        return

    try:
        fn.log_info_concise(f"  From: {dest_bak}")
        fn.log_info_concise(f"  To:   {dest}")
        fn.shutil.copy(dest_bak, dest)
        with open(simplicity_conf, "w", encoding="utf-8") as f:
            f.write("[General]\nbackground=images/background.jpg\n")
        self.sddm_wallpaper_lbl.set_text("Default wallpaper restored")
        self.sddm_wallpaper_preview.set_filename(dest)
        self.sddm_wallpaper_preview.get_parent().set_visible(True)
        self.login_wallpaper_path = ""
        fn.debug_print("[DEBUG] Backup restored and theme config updated")
        fn.log_success("Default wallpaper restored")
        fn.show_in_app_notification(self, "Default wallpaper restored")
    except Exception as error:
        fn.log_error(str(error))
        fn.show_in_app_notification(self, "Failed to restore wallpaper")


def on_click_install_bibata_cursor(self, _widget=None):
    """Install Bibata cursor theme"""
    fn.log_subsection("Install Bibata Cursors")
    if fn.check_package_installed("bibata-cursor-theme"):
        fn.log_info("Bibata cursors already installed")
        fn.show_in_app_notification(self, "Bibata cursors already installed")
        return
    fn.show_in_app_notification(self, "Opening terminal to install Bibata cursors...")
    process = fn.launch_pacman_install_in_terminal("bibata-cursor-theme")

    def wait_and_refresh():
        if process:
            process.wait()
        fn.GLib.idle_add(_refresh_cursor_theme_dropdown, self)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_click_remove_bibata_cursor(self, _widget=None):
    """Remove Bibata cursor theme"""
    fn.log_subsection("Remove Bibata Cursors")
    if not fn.check_package_installed("bibata-cursor-theme"):
        fn.log_info("Bibata cursors not installed")
        fn.show_in_app_notification(self, "Bibata cursors not installed")
        return
    fn.show_in_app_notification(self, "Opening terminal to remove Bibata cursors...")
    process = fn.launch_pacman_remove_in_terminal("bibata-cursor-theme")

    def wait_and_refresh():
        if process:
            process.wait()
        fn.GLib.idle_add(_refresh_cursor_theme_dropdown, self)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_click_install_bibatar_cursor(self, _widget=None):
    """Install Bibata extra cursors"""
    fn.log_subsection("Install Bibata Extra Cursors")
    if fn.check_package_installed("bibata-extra-cursor-theme"):
        fn.log_info("Bibata extra cursors already installed")
        fn.show_in_app_notification(self, "Bibata extra cursors already installed")
        return
    fn.show_in_app_notification(self, "Opening terminal to install Bibata extra cursors...")
    process = fn.launch_pacman_install_in_terminal("bibata-extra-cursor-theme")

    def wait_and_refresh():
        if process:
            process.wait()
        fn.GLib.idle_add(_refresh_cursor_theme_dropdown, self)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_click_remove_bibatar_cursor(self, _widget=None):
    """Remove Bibata extra cursors"""
    fn.log_subsection("Remove Bibata Extra Cursors")
    if not fn.check_package_installed("bibata-extra-cursor-theme"):
        fn.log_info("Bibata extra cursors not installed")
        fn.show_in_app_notification(self, "Bibata extra cursors not installed")
        return
    fn.show_in_app_notification(self, "Opening terminal to remove Bibata extra cursors...")
    process = fn.launch_pacman_remove_in_terminal("bibata-extra-cursor-theme")

    def wait_and_refresh():
        if process:
            process.wait()
        fn.GLib.idle_add(_refresh_cursor_theme_dropdown, self)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_click_install_simplicity(self, _widget=None):
    fn.log_subsection("Install edu-sddm-simplicity-git")
    fn.debug_print("Launching terminal to install edu-sddm-simplicity-git...")
    fn.show_in_app_notification(self, "Opening terminal to install Simplicity theme...")
    process = fn.launch_pacman_install_in_terminal("edu-sddm-simplicity-git")

    def refresh():
        if fn.check_package_installed("edu-sddm-simplicity-git"):
            fn.debug_print("Simplicity theme installed — enabling wallpaper widgets")
            for btn in (self.btn_simplicity_browse, self.btn_simplicity_load,
                        self.btn_simplicity_stop, self.btn_simplicity_apply,
                        self.btn_simplicity_restore):
                btn.set_sensitive(True)
            self.sddm_folder_entry.set_sensitive(True)
            self.btn_install_simplicity.set_visible(False)
            self.btn_remove_simplicity.set_visible(True)
            pop_theme_box(self, self.theme_sddm)

    def wait_and_refresh():
        fn.debug_print("Waiting for Simplicity install terminal to close...")
        if process:
            process.wait()
        fn.debug_print("Terminal closed — checking install result")
        fn.GLib.idle_add(refresh)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_click_remove_simplicity(self, _widget=None):
    fn.log_subsection("Remove edu-sddm-simplicity-git")
    fn.debug_print("Launching terminal to remove edu-sddm-simplicity-git...")
    fn.show_in_app_notification(self, "Opening terminal to remove Simplicity theme...")
    process = fn.launch_pacman_remove_in_terminal("edu-sddm-simplicity-git")

    def refresh():
        if not fn.check_package_installed("edu-sddm-simplicity-git"):
            fn.debug_print("Simplicity theme removed — disabling wallpaper widgets")
            for btn in (self.btn_simplicity_browse, self.btn_simplicity_load,
                        self.btn_simplicity_stop, self.btn_simplicity_apply,
                        self.btn_simplicity_restore):
                btn.set_sensitive(False)
            self.sddm_folder_entry.set_sensitive(False)
            self.btn_remove_simplicity.set_visible(False)
            self.btn_install_simplicity.set_visible(True)
            pop_theme_box(self, self.theme_sddm)
            self._sddm_load_gen = getattr(self, "_sddm_load_gen", 0) + 1
            child = self.sddm_thumb_flow.get_first_child()
            while child is not None:
                next_child = child.get_next_sibling()
                self.sddm_thumb_flow.remove(child)
                child = next_child
            self.login_wallpaper_path = ""
            fallback = fn.path.join(fn.path.dirname(fn.path.abspath(__file__)), "data", "wallpaper", "wallpaper.jpg")
            self.sddm_wallpaper_preview.set_paintable(None)
            if fn.path.isfile(fallback):
                self.sddm_wallpaper_preview.set_filename(fallback)
            self.sddm_wallpaper_lbl.set_text("No wallpaper selected")

    def wait_and_refresh():
        fn.debug_print("Waiting for Simplicity remove terminal to close...")
        if process:
            process.wait()
        fn.debug_print("Terminal closed — checking removal result")
        fn.GLib.idle_add(refresh)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_click_att_sddm_clicked(self, _widget=None):
    """Install SDDM package"""
    fn.log_subsection("Install SDDM")
    fn.show_in_app_notification(self, "Opening terminal to install sddm...")
    fn.launch_pacman_install_in_terminal("sddm")


def on_click_fix_sddm_conf(self, _widget):
    message = (
        "This will reset your SDDM configuration to the ATT defaults.\n\n"
        "• Backs up your current /etc/sddm.conf.d/ settings\n"
        "• Applies the default SDDM configuration from Kiro\n\n"
        "Your current settings will be saved as a backup before any changes are made."
    )
    if not fn.confirm_dialog(self, "Fix SDDM Configuration", message):
        return

    fn.log_subsection("Fixing SDDM configuration...")
    fn.show_in_app_notification(self, "Opening terminal to fix SDDM config...")
    process = fn.subprocess.Popen(
        ["alacritty", "-e", "/usr/share/archlinux-tweak-tool/data/bin/fix-sddm-config"],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )

    def refresh():
        pop_box(self, self.sessions_sddm)
        pop_theme_box(self, self.theme_sddm)
        pop_gtk_cursor_names(self.sddm_cursor_themes)
        self.autologin_sddm.set_active(get_autologin_state())
        fn.show_in_app_notification(self, "SDDM configuration fixed")

    def wait_and_notify():
        process.wait()
        fn.log_success("SDDM configuration fixed")
        fn.GLib.idle_add(refresh)

    fn.threading.Thread(target=wait_and_notify, daemon=True).start()
