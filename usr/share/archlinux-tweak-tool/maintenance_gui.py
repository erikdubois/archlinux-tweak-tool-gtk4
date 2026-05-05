# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools
import struct
import pacman


XCURSOR_IMAGE_TYPE = 0xFFFD0002
CURSOR_PREVIEW_SIZE = 24
CURSOR_PREVIEW_NAMES = (
    "left_ptr",
    "default",
    "pointer",
    "arrow",
    "hand1",
    "hand2",
)


def _load_xcursor_pixbuf(path, GdkPixbuf, GLib):
    try:
        with open(path, "rb") as cursor_file:
            data = cursor_file.read()

        magic, header_size, _version, toc_count = struct.unpack_from("<IIII", data, 0)
        if magic != 0x72756358:
            return None

        pixbufs = []
        toc_offset = header_size
        for pos in range(toc_count):
            entry_offset = toc_offset + pos * 12
            chunk_type, _subtype, chunk_pos = struct.unpack_from(
                "<III", data, entry_offset
            )
            if chunk_type != XCURSOR_IMAGE_TYPE:
                continue

            header, chunk_type, _subtype, _version = struct.unpack_from(
                "<IIII", data, chunk_pos
            )
            if chunk_type != XCURSOR_IMAGE_TYPE:
                continue

            width, height, _xhot, _yhot, _delay = struct.unpack_from(
                "<IIIII", data, chunk_pos + 16
            )
            if width <= 0 or height <= 0:
                continue

            pixel_offset = chunk_pos + header
            pixel_count = width * height
            if pixel_offset + pixel_count * 4 > len(data):
                continue

            rgba = bytearray(pixel_count * 4)
            for pixel in range(pixel_count):
                argb = struct.unpack_from("<I", data, pixel_offset + pixel * 4)[0]
                rgba_pos = pixel * 4
                rgba[rgba_pos] = (argb >> 16) & 0xFF
                rgba[rgba_pos + 1] = (argb >> 8) & 0xFF
                rgba[rgba_pos + 2] = argb & 0xFF
                rgba[rgba_pos + 3] = (argb >> 24) & 0xFF

            bytes_data = GLib.Bytes.new(bytes(rgba))
            pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(
                bytes_data,
                GdkPixbuf.Colorspace.RGB,
                True,
                8,
                width,
                height,
                width * 4,
            )
            pixbufs.append(pixbuf)

        if not pixbufs:
            return None

        pixbuf = min(
            pixbufs,
            key=lambda item: abs(
                max(item.get_width(), item.get_height()) - CURSOR_PREVIEW_SIZE
            ),
        )
        scale = CURSOR_PREVIEW_SIZE / max(pixbuf.get_width(), pixbuf.get_height())
        width = max(1, round(pixbuf.get_width() * scale))
        height = max(1, round(pixbuf.get_height() * scale))
        return pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
    except Exception:
        return None


def _cursor_preview_pixbuf(fn, cursor_theme, GdkPixbuf, GLib):
    for cursor_name in CURSOR_PREVIEW_NAMES:
        cursor_path = "/usr/share/icons/" + cursor_theme + "/cursors/" + cursor_name
        if fn.path.isfile(cursor_path):
            pixbuf = _load_xcursor_pixbuf(cursor_path, GdkPixbuf, GLib)
            if pixbuf:
                return pixbuf
    return None


def _update_cursor_preview(self, fn, Gdk, GdkPixbuf, GLib):
    cursor_theme = fn.get_combo_text(self.cursor_themes)
    if not cursor_theme:
        self.cursor_theme_preview.set_paintable(None)
        return

    pixbuf = _cursor_preview_pixbuf(fn, cursor_theme, GdkPixbuf, GLib)
    if pixbuf:
        self.cursor_theme_preview.set_paintable(Gdk.Texture.new_for_pixbuf(pixbuf))
    else:
        self.cursor_theme_preview.set_paintable(None)


def gui(self, Gtk, Gdk, GdkPixbuf, vboxstack19, fn, maintenance):
    fn.debug_print("[DEBUG] Initializing maintenance GUI")

    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_title = Gtk.Label(xalign=0)
    lbl_title.set_text("Maintenance")
    lbl_title.set_name("title")
    lbl_title.set_margin_start(10)
    lbl_title.set_margin_end(10)
    hbox_title.append(lbl_title)

    hbox_separator = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox_separator.append(hseparator)

    hbox_update_system = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_update_system = Gtk.Label(xalign=0)
    lbl_update_system.set_text("Update system")
    btn_update_system = Gtk.Button(label="Update")
    btn_update_system.connect("clicked", functools.partial(maintenance.on_click_update_system, self))
    lbl_update_system.set_margin_start(10)
    lbl_update_system.set_margin_end(10)
    lbl_update_system.set_hexpand(True)
    hbox_update_system.append(lbl_update_system)
    btn_update_system.set_margin_start(10)
    btn_update_system.set_margin_end(10)
    hbox_update_system.append(btn_update_system)

    hbox_clean_cache = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_clean_cache = Gtk.Label(xalign=0)
    lbl_clean_cache.set_text("Clean cache")
    btn_clean_cache = Gtk.Button(label="Clean")
    btn_clean_cache.connect("clicked", functools.partial(maintenance.on_click_clean_cache, self))
    lbl_clean_cache.set_margin_start(10)
    lbl_clean_cache.set_margin_end(10)
    lbl_clean_cache.set_hexpand(True)
    hbox_clean_cache.append(lbl_clean_cache)
    btn_clean_cache.set_margin_start(10)
    btn_clean_cache.set_margin_end(10)
    hbox_clean_cache.append(btn_clean_cache)

    hbox_remove_lock = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_remove_lock = Gtk.Label(xalign=0)
    lbl_remove_lock.set_text("Remove pacman lock")
    btn_remove_pacman_lock = Gtk.Button(label="Remove")
    btn_remove_pacman_lock.connect("clicked", functools.partial(maintenance.on_click_remove_pacman_lock, self))
    lbl_remove_lock.set_margin_start(10)
    lbl_remove_lock.set_margin_end(10)
    lbl_remove_lock.set_hexpand(True)
    hbox_remove_lock.append(lbl_remove_lock)
    btn_remove_pacman_lock.set_margin_start(10)
    btn_remove_pacman_lock.set_margin_end(10)
    hbox_remove_lock.append(btn_remove_pacman_lock)

    hbox_keyring = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_keyring = Gtk.Label(xalign=0)
    lbl_keyring.set_text("Re-install archlinux-keyring")
    btn_install_arch_keyring = Gtk.Button(label="Install keyring (local)")
    btn_install_arch_keyring.connect(
        "clicked", functools.partial(maintenance.on_click_install_arch_keyring, self)
    )
    btn_install_arch_keyring_online = Gtk.Button(label="Install keyring (online)")
    btn_install_arch_keyring_online.connect(
        "clicked", functools.partial(maintenance.on_click_install_arch_keyring_online, self)
    )
    lbl_keyring.set_margin_start(10)
    lbl_keyring.set_margin_end(10)
    lbl_keyring.set_hexpand(True)
    hbox_keyring.append(lbl_keyring)
    btn_install_arch_keyring.set_margin_start(10)
    btn_install_arch_keyring.set_margin_end(10)
    hbox_keyring.append(btn_install_arch_keyring)
    btn_install_arch_keyring_online.set_margin_start(10)
    btn_install_arch_keyring_online.set_margin_end(10)
    hbox_keyring.append(btn_install_arch_keyring_online)

    hbox_fix_keys = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_fix_keys = Gtk.Label(xalign=0)
    lbl_fix_keys.set_text("Reset and reload pacman keys")
    btn_apply_pacman_key_fix = Gtk.Button(label="Fix keys")
    btn_apply_pacman_key_fix.connect("clicked", functools.partial(maintenance.on_click_fix_pacman_keys, self))
    lbl_fix_keys.set_margin_start(10)
    lbl_fix_keys.set_margin_end(10)
    lbl_fix_keys.set_hexpand(True)
    hbox_fix_keys.append(lbl_fix_keys)
    btn_apply_pacman_key_fix.set_margin_start(10)
    btn_apply_pacman_key_fix.set_margin_end(10)
    hbox_fix_keys.append(btn_apply_pacman_key_fix)

    hbox_mainstream_servers = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_mainstream_servers = Gtk.Label(xalign=0)
    lbl_mainstream_servers.set_text("Set the mainstream servers from Arch Linux")
    btn_apply_osbeck = Gtk.Button(label="Set mainstream")
    btn_apply_osbeck.connect("clicked", functools.partial(maintenance.on_click_fix_mainstream, self))
    button_reset_mirrorlist = Gtk.Button(label="Reset your mirrorlist")
    button_reset_mirrorlist.connect("clicked", functools.partial(maintenance.on_click_reset_mirrorlist, self))
    lbl_mainstream_servers.set_margin_start(10)
    lbl_mainstream_servers.set_margin_end(10)
    lbl_mainstream_servers.set_hexpand(True)
    hbox_mainstream_servers.append(lbl_mainstream_servers)
    btn_apply_osbeck.set_margin_start(10)
    btn_apply_osbeck.set_margin_end(10)
    hbox_mainstream_servers.append(btn_apply_osbeck)
    button_reset_mirrorlist.set_margin_start(10)
    button_reset_mirrorlist.set_margin_end(10)
    hbox_mainstream_servers.append(button_reset_mirrorlist)

    hbox_run_mirror_tools = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_run_mirror_tools = Gtk.Label(xalign=0)
    lbl_run_mirror_tools.set_text("Get the best Arch Linux servers (takes a while)")
    self.btn_run_reflector = Gtk.Button(label="Run reflector")
    self.btn_run_reflector.connect("clicked", functools.partial(maintenance.on_click_get_arch_mirrors, self))
    self.btn_run_rate_mirrors = Gtk.Button(label="Run rate-mirrors")
    self.btn_run_rate_mirrors.connect("clicked", functools.partial(maintenance.on_click_get_arch_mirrors2, self))
    lbl_run_mirror_tools.set_margin_start(10)
    lbl_run_mirror_tools.set_margin_end(10)
    lbl_run_mirror_tools.set_hexpand(True)
    hbox_run_mirror_tools.append(lbl_run_mirror_tools)
    self.btn_run_rate_mirrors.set_margin_start(10)
    self.btn_run_rate_mirrors.set_margin_end(10)
    hbox_run_mirror_tools.append(self.btn_run_rate_mirrors)
    self.btn_run_reflector.set_margin_start(10)
    self.btn_run_reflector.set_margin_end(10)
    hbox_run_mirror_tools.append(self.btn_run_reflector)

    hbox_install_mirror_tools = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_install_mirror_tools = Gtk.Label(xalign=0)
    lbl_install_mirror_tools.set_text("Install apps to find the best Arch Linux servers")
    reflector_label = "Remove reflector" if fn.path.exists("/usr/bin/reflector") else "Install reflector"
    self.btn_install_mirrors = Gtk.Button(label=reflector_label)
    self.btn_install_mirrors.connect("clicked", functools.partial(maintenance.on_click_install_arch_mirrors, self))
    rate_mirrors_label = "Remove rate-mirrors" if fn.path.exists("/usr/bin/rate-mirrors") else "Install rate-mirrors"
    self.btn_install_rate_mirrors = Gtk.Button(label=rate_mirrors_label)
    self.btn_install_rate_mirrors.connect(
        "clicked", functools.partial(maintenance.on_click_install_arch_mirrors2, self)
    )
    lbl_install_mirror_tools.set_margin_start(10)
    lbl_install_mirror_tools.set_margin_end(10)
    lbl_install_mirror_tools.set_hexpand(True)
    hbox_install_mirror_tools.append(lbl_install_mirror_tools)
    self.btn_install_rate_mirrors.set_margin_start(10)
    self.btn_install_rate_mirrors.set_margin_end(10)
    hbox_install_mirror_tools.append(self.btn_install_rate_mirrors)
    self.btn_install_mirrors.set_margin_start(10)
    self.btn_install_mirrors.set_margin_end(10)
    hbox_install_mirror_tools.append(self.btn_install_mirrors)

    if not fn.path.exists("/usr/bin/reflector"):
        self.btn_run_reflector.set_sensitive(False)
    if not fn.path.exists("/usr/bin/rate-mirrors"):
        self.btn_run_rate_mirrors.set_sensitive(False)

    hbox_reset_pacman_conf = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_reset_pacman_conf = Gtk.Label(xalign=0)
    lbl_reset_pacman_conf.set_text("Get the original ATT /etc/pacman.conf")
    btn_reset_pacman = Gtk.Button(label="Reset pacman.conf")
    btn_reset_pacman.connect("clicked", functools.partial(maintenance.on_click_fix_pacman_conf, self))
    lbl_reset_pacman_conf.set_margin_start(10)
    lbl_reset_pacman_conf.set_margin_end(10)
    lbl_reset_pacman_conf.set_hexpand(True)
    hbox_reset_pacman_conf.append(lbl_reset_pacman_conf)
    btn_reset_pacman.set_margin_start(10)
    btn_reset_pacman.set_margin_end(10)
    hbox_reset_pacman_conf.append(btn_reset_pacman)

    hbox_gpg_conf = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_gpg_conf = Gtk.Label(xalign=0)
    lbl_gpg_conf.set_text("Get the best keyservers for /etc/pacman.d/gnupg/gpg.conf")
    btn_apply_pacman_gpg_conf = Gtk.Button(label="Backup and reset gpg.conf")
    btn_apply_pacman_gpg_conf.connect("clicked", functools.partial(maintenance.on_click_fix_pacman_gpg_conf, self))
    lbl_gpg_conf.set_margin_start(10)
    lbl_gpg_conf.set_margin_end(10)
    lbl_gpg_conf.set_hexpand(True)
    hbox_gpg_conf.append(lbl_gpg_conf)
    btn_apply_pacman_gpg_conf.set_margin_start(10)
    btn_apply_pacman_gpg_conf.set_margin_end(10)
    hbox_gpg_conf.append(btn_apply_pacman_gpg_conf)

    hbox_gpg_conf_local = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_gpg_conf_local = Gtk.Label(xalign=0)
    lbl_gpg_conf_local.set_text("Get the best keyservers for ~/.gnupg/gpg.conf")
    btn_apply_pacman_gpg_conf_local = Gtk.Button(label="Backup and reset gpg.conf")
    btn_apply_pacman_gpg_conf_local.connect(
        "clicked", functools.partial(maintenance.on_click_fix_pacman_gpg_conf_local, self)
    )
    lbl_gpg_conf_local.set_margin_start(10)
    lbl_gpg_conf_local.set_margin_end(10)
    lbl_gpg_conf_local.set_hexpand(True)
    hbox_gpg_conf_local.append(lbl_gpg_conf_local)
    btn_apply_pacman_gpg_conf_local.set_margin_start(10)
    btn_apply_pacman_gpg_conf_local.set_margin_end(10)
    hbox_gpg_conf_local.append(btn_apply_pacman_gpg_conf_local)

    hbox_parallel_downloads = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_parallel_downloads = Gtk.Label(xalign=0)
    lbl_parallel_downloads.set_text("Choose the number of parallel downloads for pacman")
    self.parallel_downloads = Gtk.DropDown.new_from_strings([])
    numbers = [str(i) for i in range(1, 31)]

    btn_apply_parallel_downloads = Gtk.Button(label="Apply")
    btn_apply_parallel_downloads.connect("clicked", functools.partial(pacman.on_click_apply_parallel_downloads, self))

    if fn.check_content("ParallelDownloads", fn.pacman):
        for number in numbers:
            self.parallel_downloads.get_model().append(number)
        act_number = pacman.pop_parallel_downloads(self)
        self.parallel_downloads.set_selected(act_number)
    else:
        btn_apply_parallel_downloads.set_sensitive(False)

    lbl_parallel_downloads.set_margin_start(10)
    lbl_parallel_downloads.set_margin_end(10)
    lbl_parallel_downloads.set_hexpand(True)
    hbox_parallel_downloads.append(lbl_parallel_downloads)
    self.parallel_downloads.set_margin_start(10)
    self.parallel_downloads.set_margin_end(10)
    hbox_parallel_downloads.append(self.parallel_downloads)
    btn_apply_parallel_downloads.set_margin_start(10)
    btn_apply_parallel_downloads.set_margin_end(10)
    hbox_parallel_downloads.append(btn_apply_parallel_downloads)

    hbox_cursor_theme = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_cursor_theme = Gtk.Label(xalign=0)
    lbl_cursor_theme.set_text("Choose your cursor theme for installed desktops and SDDM")
    self.cursor_themes = Gtk.DropDown.new_from_strings([])
    maintenance.pop_gtk_cursor_names(self.cursor_themes)
    self.cursor_theme_preview = Gtk.Picture()
    self.cursor_theme_preview.set_content_fit(Gtk.ContentFit.SCALE_DOWN)
    self.cursor_theme_preview.set_size_request(CURSOR_PREVIEW_SIZE, CURSOR_PREVIEW_SIZE)
    self.cursor_theme_preview.set_halign(Gtk.Align.END)
    self.cursor_theme_preview.set_valign(Gtk.Align.CENTER)
    self.cursor_themes.connect(
        "notify::selected",
        lambda *_args: _update_cursor_preview(self, fn, Gdk, GdkPixbuf, fn.GLib),
    )
    _update_cursor_preview(self, fn, Gdk, GdkPixbuf, fn.GLib)
    btn_apply_cursor = Gtk.Button(label="Apply")
    btn_apply_cursor.connect("clicked", functools.partial(maintenance.on_click_apply_global_cursor, self))
    lbl_cursor_theme.set_margin_start(10)
    lbl_cursor_theme.set_margin_end(10)
    lbl_cursor_theme.set_hexpand(True)
    hbox_cursor_theme.append(lbl_cursor_theme)
    self.cursor_theme_preview.set_margin_start(10)
    self.cursor_theme_preview.set_margin_end(10)
    hbox_cursor_theme.append(self.cursor_theme_preview)
    self.cursor_themes.set_margin_start(10)
    self.cursor_themes.set_margin_end(10)
    hbox_cursor_theme.append(self.cursor_themes)
    btn_apply_cursor.set_margin_start(10)
    btn_apply_cursor.set_margin_end(10)
    hbox_cursor_theme.append(btn_apply_cursor)

    hbox_probe = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_probe = Gtk.Label(xalign=0)
    lbl_probe.set_markup("Provide probe link")
    btn_probe = Gtk.Button(label="Get probe link")
    btn_probe.connect("clicked", functools.partial(maintenance.on_click_probe, self))
    lbl_probe.set_margin_start(10)
    lbl_probe.set_margin_end(10)
    lbl_probe.set_hexpand(True)
    hbox_probe.append(lbl_probe)
    btn_probe.set_margin_start(10)
    btn_probe.set_margin_end(10)
    hbox_probe.append(btn_probe)

    # ==========================================
    #              Section Labels
    # ==========================================
    hbox_sec_system = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_sec_system = Gtk.Label(xalign=0)
    lbl_sec_system.set_markup("<b>System Maintenance</b>")
    lbl_sec_system.set_margin_start(10)
    lbl_sec_system.set_margin_top(15)
    lbl_sec_system.set_margin_bottom(5)
    hbox_sec_system.append(lbl_sec_system)

    hbox_sec_mirrors = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_sec_mirrors = Gtk.Label(xalign=0)
    lbl_sec_mirrors.set_markup("<b>Mirror Management</b>")
    lbl_sec_mirrors.set_margin_start(10)
    lbl_sec_mirrors.set_margin_top(15)
    lbl_sec_mirrors.set_margin_bottom(5)
    hbox_sec_mirrors.append(lbl_sec_mirrors)

    hbox_sec_keys = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_sec_keys = Gtk.Label(xalign=0)
    lbl_sec_keys.set_markup("<b>Pacman Keys &amp; Keyring</b>")
    lbl_sec_keys.set_margin_start(10)
    lbl_sec_keys.set_margin_top(15)
    lbl_sec_keys.set_margin_bottom(5)
    hbox_sec_keys.append(lbl_sec_keys)

    hbox_sec_pacman_config = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_sec_pacman_config = Gtk.Label(xalign=0)
    lbl_sec_pacman_config.set_markup("<b>Pacman Configuration</b>")
    lbl_sec_pacman_config.set_margin_start(10)
    lbl_sec_pacman_config.set_margin_top(15)
    lbl_sec_pacman_config.set_margin_bottom(5)
    hbox_sec_pacman_config.append(lbl_sec_pacman_config)

    hbox_sec_sys_config = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_sec_sys_config = Gtk.Label(xalign=0)
    lbl_sec_sys_config.set_markup("<b>System Configuration for cursors</b>")
    lbl_sec_sys_config.set_margin_start(10)
    lbl_sec_sys_config.set_margin_top(15)
    lbl_sec_sys_config.set_margin_bottom(5)
    hbox_sec_sys_config.append(lbl_sec_sys_config)

    hbox_bibata_cursors = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    btn_install_bibata = Gtk.Button(label="Install Bibata cursors")
    btn_install_bibata.connect("clicked", functools.partial(maintenance.on_click_install_bibata_cursors, self))
    btn_install_bibata.set_margin_start(10)
    btn_install_bibata.set_margin_end(10)
    btn_remove_bibata = Gtk.Button(label="Remove Bibata cursors")
    btn_remove_bibata.connect("clicked", functools.partial(maintenance.on_click_remove_bibata_cursors, self))
    btn_remove_bibata.set_margin_end(10)
    hbox_bibata_cursors.append(btn_install_bibata)
    hbox_bibata_cursors.append(btn_remove_bibata)

    hbox_sec_diagnostics = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_sec_diagnostics = Gtk.Label(xalign=0)
    lbl_sec_diagnostics.set_markup("<b>Diagnostics</b>")
    lbl_sec_diagnostics.set_margin_start(10)
    lbl_sec_diagnostics.set_margin_top(15)
    lbl_sec_diagnostics.set_margin_bottom(5)
    hbox_sec_diagnostics.append(lbl_sec_diagnostics)

    # ======================================================================
    #                       VBOX STACK
    # ======================================================================

    vboxstack19.append(hbox_title)
    vboxstack19.append(hbox_separator)

    vboxstack19.append(hbox_sec_system)
    vboxstack19.append(hbox_update_system)
    vboxstack19.append(hbox_clean_cache)
    vboxstack19.append(hbox_remove_lock)

    vboxstack19.append(hbox_sec_mirrors)
    vboxstack19.append(hbox_install_mirror_tools)
    vboxstack19.append(hbox_run_mirror_tools)
    vboxstack19.append(hbox_mainstream_servers)

    vboxstack19.append(hbox_sec_keys)
    vboxstack19.append(hbox_keyring)
    vboxstack19.append(hbox_fix_keys)
    vboxstack19.append(hbox_gpg_conf)
    vboxstack19.append(hbox_gpg_conf_local)

    vboxstack19.append(hbox_sec_pacman_config)
    vboxstack19.append(hbox_reset_pacman_conf)
    vboxstack19.append(hbox_parallel_downloads)

    vboxstack19.append(hbox_sec_sys_config)
    vboxstack19.append(hbox_bibata_cursors)
    vboxstack19.append(hbox_cursor_theme)

    hbox_cursor_info = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    cursor_info_label = Gtk.Label(xalign=0, wrap=True)
    cursor_info_label.set_text(
        "Applies cursor theme globally to: System & user xcursor, GTK2/3/4, XFCE, GNOME (gsettings),"
        " KDE Plasma, and SDDM login screen. Affects all applications and SDDM login screen."
    )
    cursor_info_label.set_margin_start(40)
    cursor_info_label.set_margin_end(10)
    cursor_info_label.set_margin_top(0)
    cursor_info_label.set_margin_bottom(5)
    hbox_cursor_info.append(cursor_info_label)
    vboxstack19.append(hbox_cursor_info)

    vboxstack19.append(hbox_sec_diagnostics)
    vboxstack19.append(hbox_probe)
