# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import pwd
import shutil
import random as _random

import functions as fn
from gi.repository import GdkPixbuf, Gdk, Gtk, Gio, Pango


_DIR = fn.path.dirname(fn.path.abspath(__file__))
_ATT_WALLPAPERS = fn.path.join(_DIR, "wallpapers")
_VARIETY_CONF_SRC = fn.path.join(_DIR, "data", "variety")
_VARIETY_CONF_DEST = fn.path.join(fn.home, ".config", "variety")

_FEH_FLAGS = {
    "Fill": "--bg-fill",
    "Fit": "--bg-max",
    "Center": "--bg-center",
    "Tile": "--bg-tile",
    "Stretch": "--bg-scale",
}


def on_install_variety(self, _widget=None):
    fn.log_subsection("Install variety")
    fn.show_in_app_notification(self, "Opening terminal to install variety...")
    process = fn.launch_pacman_install_in_terminal("variety")

    def refresh():
        installed = fn.check_package_installed("variety")
        _set_variety_widgets_sensitive(self, installed)
        if installed:
            fn.log_success("variety installed")
        else:
            fn.log_info("variety not found after install")

    def wait_and_refresh():
        if process:
            process.wait()
        fn.GLib.idle_add(refresh)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_remove_variety(self, _widget=None):
    if not fn.check_package_installed("variety"):
        fn.log_info("variety is not installed")
        fn.show_in_app_notification(self, "variety is not installed")
        return
    fn.log_subsection("Remove variety")
    fn.show_in_app_notification(self, "Opening terminal to remove variety...")
    process = fn.launch_pacman_remove_in_terminal("variety")

    def refresh():
        installed = fn.check_package_installed("variety")
        _set_variety_widgets_sensitive(self, installed)
        if not installed:
            fn.log_success("variety removed")
        else:
            fn.log_info("variety still present after remove")

    def wait_and_refresh():
        if process:
            process.wait()
        fn.GLib.idle_add(refresh)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def _set_variety_widgets_sensitive(self, installed):
    self.btn_save_variety_config.set_sensitive(installed)
    self.btn_open_variety_settings.set_sensitive(installed)


def on_save_variety_config(self, _widget=None):
    fn.log_subsection("Save ATT variety config")
    if not fn.path.isdir(_VARIETY_CONF_SRC):
        fn.log_warn(f"ATT variety config folder not found: {_VARIETY_CONF_SRC}")
        fn.show_in_app_notification(self, "ATT variety config not found in data folder")
        return
    try:
        fn.os.makedirs(_VARIETY_CONF_DEST, exist_ok=True)
        for item in fn.os.listdir(_VARIETY_CONF_SRC):
            src = fn.path.join(_VARIETY_CONF_SRC, item)
            dest = fn.path.join(_VARIETY_CONF_DEST, item)
            if fn.path.isdir(src):
                if fn.path.isdir(dest):
                    shutil.rmtree(dest + "-bak", ignore_errors=True)
                    shutil.copytree(dest, dest + "-bak")
                    fn.log_info_concise(f"  Backed up: {dest} → {dest}-bak")
                fn.log_info_concise(f"  From: {src}")
                fn.log_info_concise(f"  To:   {dest}")
                shutil.copytree(src, dest, dirs_exist_ok=True)
                fn.log_info_concise(f"  Done: {fn.path.basename(src)}/")
            else:
                if fn.path.isfile(dest):
                    shutil.copy2(dest, dest + "-bak")
                    fn.log_info_concise(f"  Backed up: {dest} → {dest}-bak")
                fn.log_info_concise(f"  From: {src}")
                fn.log_info_concise(f"  To:   {dest}")
                shutil.copy2(src, dest)
                fn.log_info_concise(f"  Done: {fn.path.basename(src)}")
        fn.log_success("ATT variety config saved to ~/.config/variety/")
        fn.show_in_app_notification(self, "Variety config saved")
    except Exception as error:
        fn.log_error(f"Failed to save variety config: {error}")
        fn.show_in_app_notification(self, f"Error: {error}")


def on_open_variety_settings(self, _widget=None):
    fn.log_subsection("Open variety settings")
    uid = pwd.getpwnam(fn.sudo_username).pw_uid
    cmd = (
        f"sudo -u {fn.sudo_username}"
        f" XDG_RUNTIME_DIR=/run/user/{uid}"
        f" DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{uid}/bus"
        " DISPLAY=$DISPLAY WAYLAND_DISPLAY=$WAYLAND_DISPLAY"
        " variety --preferences"
    )
    fn.threading.Thread(
        target=lambda: fn.subprocess.Popen(cmd, shell=True, stdout=fn.subprocess.PIPE, stderr=fn.subprocess.PIPE),
        daemon=True,
    ).start()


def on_browse_wallpaper_folder(self, _widget=None):
    dialog = Gtk.FileDialog()
    dialog.set_title("Choose a wallpaper folder")
    current = self.wallpaper_folder_entry.get_text().strip()
    start = current if fn.path.isdir(current) else fn.home
    dialog.set_initial_folder(Gio.File.new_for_path(start))
    dialog.select_folder(self, None, lambda d, result: _on_folder_response(self, d, result))


def _on_folder_response(self, dialog, result):
    try:
        folder = dialog.select_folder_finish(result)
        if folder:
            folder_path = folder.get_path()
            self.wallpaper_folder_entry.set_text(folder_path)
            _populate_wallpaper_thumbs(self, folder_path)
    except Exception:
        pass


def on_load_wallpaper_folder(self, _widget=None):
    folder_path = self.wallpaper_folder_entry.get_text().strip()
    if fn.path.isdir(folder_path):
        _populate_wallpaper_thumbs(self, folder_path)
    else:
        fn.show_in_app_notification(self, "Folder not found")


def on_stop_wallpaper_loading(self, _widget=None):
    self._wp_load_gen = getattr(self, "_wp_load_gen", 0) + 1


def _populate_wallpaper_thumbs(self, folder_path):
    fn.log_subsection(f"Loading wallpapers from: {folder_path}")
    self._wp_load_gen = getattr(self, "_wp_load_gen", 0) + 1
    current_gen = self._wp_load_gen

    child = self.wallpaper_thumb_flow.get_first_child()
    while child is not None:
        next_child = child.get_next_sibling()
        self.wallpaper_thumb_flow.remove(child)
        child = next_child

    exts = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
    try:
        entries = sorted(fn.os.listdir(folder_path))
    except Exception:
        return

    image_paths = [fn.path.join(folder_path, n) for n in entries if n.lower().endswith(exts)]
    idx = [0]

    def load_next():
        if self._wp_load_gen != current_gen:
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
            btn.connect("clicked", lambda w, p=path: _on_thumb_clicked(self, w, p))
            self.wallpaper_thumb_flow.append(btn)
        except Exception:
            pass
        return True

    fn.GLib.idle_add(load_next)


def _on_thumb_clicked(self, _widget, path):
    self.selected_wallpaper_path = path
    self.wallpaper_path_lbl.set_text(path)
    self.wallpaper_preview.set_filename(path)
    self.wallpaper_preview.get_parent().set_visible(True)


def on_apply_wallpaper(self, _widget=None):
    path = getattr(self, "selected_wallpaper_path", None)
    if not path or not fn.path.isfile(path):
        fn.show_in_app_notification(self, "Select a wallpaper first")
        return
    scale = fn.get_combo_text(self.wallpaper_scale_combo)
    _apply_feh(self, path, scale)


def on_random_wallpaper(self, _widget=None):
    folder_path = self.wallpaper_folder_entry.get_text().strip()
    exts = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
    try:
        images = [fn.path.join(folder_path, f) for f in fn.os.listdir(folder_path) if f.lower().endswith(exts)]
    except Exception:
        fn.show_in_app_notification(self, "Could not read folder")
        return
    if not images:
        fn.show_in_app_notification(self, "No images in folder")
        return
    path = _random.choice(images)
    scale = fn.get_combo_text(self.wallpaper_scale_combo)
    self.selected_wallpaper_path = path
    self.wallpaper_path_lbl.set_text(path)
    self.wallpaper_preview.set_filename(path)
    self.wallpaper_preview.get_parent().set_visible(True)
    _apply_feh(self, path, scale)


def _apply_feh(self, path, scale):
    flag = _FEH_FLAGS.get(scale, "--bg-fill")
    fn.log_subsection(f"Applying wallpaper — feh {flag}: {path}")
    try:
        fn.subprocess.Popen(
            ["feh", flag, path],
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.PIPE,
        )
        fn.log_success(f"Wallpaper set: {fn.path.basename(path)}")
        fn.show_in_app_notification(self, f"Wallpaper set: {fn.path.basename(path)}")
    except FileNotFoundError:
        fn.log_error("feh not found — install feh to apply wallpapers")
        fn.show_in_app_notification(self, "feh not found — install feh first")
