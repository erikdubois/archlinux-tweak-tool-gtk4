# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools
import struct


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
    except Exception as error:
        print(error)
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
    """create a gui"""
    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox1_label = Gtk.Label(xalign=0)
    hbox1_label.set_text("Maintenance")
    hbox1_label.set_name("title")
    hbox1_label.set_margin_start(10)
    hbox1_label.set_margin_end(10)
    hbox1.append(hbox1_label)

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox0.append(hseparator)

    hbox22 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox22_label = Gtk.Label(xalign=0)
    hbox22_label.set_text("Update system")
    btn_update_system = Gtk.Button(label="Update")
    btn_update_system.connect("clicked", functools.partial(maintenance.on_click_update_system, self))
    hbox22_label.set_margin_start(10)
    hbox22_label.set_margin_end(10)
    hbox22_label.set_hexpand(True)
    hbox22.append(hbox22_label)
    btn_update_system.set_margin_start(10)
    btn_update_system.set_margin_end(10)
    hbox22.append(btn_update_system)  # pack_end

    hbox23 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox23_label = Gtk.Label(xalign=0)
    hbox23_label.set_text("Clean cache")
    btn_clean_cache = Gtk.Button(label="Clean")
    btn_clean_cache.connect("clicked", functools.partial(maintenance.on_click_clean_cache, self))
    hbox23_label.set_margin_start(10)
    hbox23_label.set_margin_end(10)
    hbox23_label.set_hexpand(True)
    hbox23.append(hbox23_label)
    btn_clean_cache.set_margin_start(10)
    btn_clean_cache.set_margin_end(10)
    hbox23.append(btn_clean_cache)  # pack_end

    hbox25 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox25_label = Gtk.Label(xalign=0)
    hbox25_label.set_text("Remove pacman lock")
    btn_remove_pacman_lock = Gtk.Button(label="Remove")
    btn_remove_pacman_lock.connect("clicked", functools.partial(maintenance.on_click_remove_pacman_lock, self))
    hbox25_label.set_margin_start(10)
    hbox25_label.set_margin_end(10)
    hbox25_label.set_hexpand(True)
    hbox25.append(hbox25_label)
    btn_remove_pacman_lock.set_margin_start(10)
    btn_remove_pacman_lock.set_margin_end(10)
    hbox25.append(btn_remove_pacman_lock)  # pack_end

    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox5_label = Gtk.Label(xalign=0)
    hbox5_label.set_text("Re-install archlinux-keyring")
    btn_install_arch_keyring = Gtk.Button(label="Install keyring (local)")
    btn_install_arch_keyring.connect("clicked", functools.partial(maintenance.on_click_install_arch_keyring, self))
    btn_install_arch_keyring_online = Gtk.Button(label="Install keyring (online)")
    btn_install_arch_keyring_online.connect("clicked", functools.partial(maintenance.on_click_install_arch_keyring_online, self))
    hbox5_label.set_margin_start(10)
    hbox5_label.set_margin_end(10)
    hbox5_label.set_hexpand(True)
    hbox5.append(hbox5_label)
    btn_install_arch_keyring.set_margin_start(10)
    btn_install_arch_keyring.set_margin_end(10)
    hbox5.append(btn_install_arch_keyring)  # pack_end
    btn_install_arch_keyring_online.set_margin_start(10)
    btn_install_arch_keyring_online.set_margin_end(10)
    hbox5.append(btn_install_arch_keyring_online)  # pack_end

    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox2_label = Gtk.Label(xalign=0)
    hbox2_label.set_text("Reset and reload pacman keys")
    btn_apply_pacman_key_fix = Gtk.Button(label="Fix keys")
    btn_apply_pacman_key_fix.connect("clicked", functools.partial(maintenance.on_click_fix_pacman_keys, self))
    hbox2_label.set_margin_start(10)
    hbox2_label.set_margin_end(10)
    hbox2_label.set_hexpand(True)
    hbox2.append(hbox2_label)
    btn_apply_pacman_key_fix.set_margin_start(10)
    btn_apply_pacman_key_fix.set_margin_end(10)
    hbox2.append(btn_apply_pacman_key_fix)  # pack_end

    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox3_label = Gtk.Label(xalign=0)
    hbox3_label.set_text("Set the mainstream servers from Arch Linux")
    btn_apply_osbeck = Gtk.Button(label="Set mainstream")
    btn_apply_osbeck.connect("clicked", functools.partial(maintenance.on_click_fix_mainstream, self))
    button_reset_mirrorlist = Gtk.Button(label="Reset mirrorlist")
    button_reset_mirrorlist.connect("clicked", functools.partial(maintenance.on_click_reset_mirrorlist, self))
    hbox3_label.set_margin_start(10)
    hbox3_label.set_margin_end(10)
    hbox3_label.set_hexpand(True)
    hbox3.append(hbox3_label)
    btn_apply_osbeck.set_margin_start(10)
    btn_apply_osbeck.set_margin_end(10)
    hbox3.append(btn_apply_osbeck)  # pack_end
    button_reset_mirrorlist.set_margin_start(10)
    button_reset_mirrorlist.set_margin_end(10)
    hbox3.append(button_reset_mirrorlist)  # pack_end

    # if all installed
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4_label = Gtk.Label(xalign=0)
    hbox4_label.set_text("Get the best Arch Linux servers (takes a while)")
    self.btn_run_reflector = Gtk.Button(label="Run reflector")
    self.btn_run_reflector.connect("clicked", functools.partial(maintenance.on_click_get_arch_mirrors, self))
    self.btn_run_rate_mirrors = Gtk.Button(label="Run rate-mirrors")
    self.btn_run_rate_mirrors.connect("clicked", functools.partial(maintenance.on_click_get_arch_mirrors2, self))
    hbox4_label.set_margin_start(10)
    hbox4_label.set_margin_end(10)
    hbox4_label.set_hexpand(True)
    hbox4.append(hbox4_label)
    self.btn_run_rate_mirrors.set_margin_start(10)
    self.btn_run_rate_mirrors.set_margin_end(10)
    hbox4.append(self.btn_run_rate_mirrors)  # pack_end
    self.btn_run_reflector.set_margin_start(10)
    self.btn_run_reflector.set_margin_end(10)
    hbox4.append(self.btn_run_reflector)  # pack_end

    # if not installed
    hbox40 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox40_label = Gtk.Label(xalign=0)
    hbox40_label.set_text("Install apps to find the best Arch Linux servers")
    btn_install_mirrors = Gtk.Button(label="Install reflector")
    btn_install_mirrors.connect("clicked", functools.partial(maintenance.on_click_install_arch_mirrors, self))
    btn_install_rate_mirrors = Gtk.Button(label="Install rate mirrors")
    btn_install_rate_mirrors.connect("clicked", functools.partial(maintenance.on_click_install_arch_mirrors2, self))
    hbox40_label.set_margin_start(10)
    hbox40_label.set_margin_end(10)
    hbox40_label.set_hexpand(True)
    hbox40.append(hbox40_label)
    btn_install_rate_mirrors.set_margin_start(10)
    btn_install_rate_mirrors.set_margin_end(10)
    hbox40.append(btn_install_rate_mirrors)  # pack_end
    btn_install_mirrors.set_margin_start(10)
    btn_install_mirrors.set_margin_end(10)
    hbox40.append(btn_install_mirrors)  # pack_end

    if not fn.path.exists("/usr/bin/reflector"):
        self.btn_run_reflector.set_sensitive(False)
    if not fn.path.exists("/usr/bin/rate-mirrors"):
        self.btn_run_rate_mirrors.set_sensitive(False)

    hbox6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox6_label = Gtk.Label(xalign=0)
    hbox6_label.set_text("Get the original ArcoLinux /etc/pacman.conf")
    btn_reset_pacman = Gtk.Button(label="Reset pacman.conf")
    btn_reset_pacman.connect("clicked", functools.partial(maintenance.on_click_fix_pacman_conf, self))
    hbox6_label.set_margin_start(10)
    hbox6_label.set_margin_end(10)
    hbox6_label.set_hexpand(True)
    hbox6.append(hbox6_label)
    btn_reset_pacman.set_margin_start(10)
    btn_reset_pacman.set_margin_end(10)
    hbox6.append(btn_reset_pacman)  # pack_end

    hbox7 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox7_label = Gtk.Label(xalign=0)
    hbox7_label.set_text("Get the best keyservers for /etc/pacman.d/gnupg/gpg.conf")
    btn_apply_pacman_gpg_conf = Gtk.Button(label="Backup and reset gpg.conf")
    btn_apply_pacman_gpg_conf.connect("clicked", functools.partial(maintenance.on_click_fix_pacman_gpg_conf, self))
    hbox7_label.set_margin_start(10)
    hbox7_label.set_margin_end(10)
    hbox7_label.set_hexpand(True)
    hbox7.append(hbox7_label)
    btn_apply_pacman_gpg_conf.set_margin_start(10)
    btn_apply_pacman_gpg_conf.set_margin_end(10)
    hbox7.append(btn_apply_pacman_gpg_conf)  # pack_end

    hbox8 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox8_label = Gtk.Label(xalign=0)
    hbox8_label.set_text("Get the best keyservers for ~/.gnupg/gpg.conf")
    btn_apply_pacman_gpg_conf_local = Gtk.Button(label="Backup and reset gpg.conf")
    btn_apply_pacman_gpg_conf_local.connect("clicked", functools.partial(maintenance.on_click_fix_pacman_gpg_conf_local, self))
    hbox8_label.set_margin_start(10)
    hbox8_label.set_margin_end(10)
    hbox8_label.set_hexpand(True)
    hbox8.append(hbox8_label)
    btn_apply_pacman_gpg_conf_local.set_margin_start(10)
    btn_apply_pacman_gpg_conf_local.set_margin_end(10)
    hbox8.append(btn_apply_pacman_gpg_conf_local)  # pack_end

    hbox12 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox12_label = Gtk.Label(xalign=0)
    hbox12_label.set_text("Choose the number of parallel downloads for pacman")
    self.parallel_downloads = Gtk.DropDown.new_from_strings([])
    numbers = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
    ]

    btn_apply_parallel_downloads = Gtk.Button(label="Apply")
    btn_apply_parallel_downloads.connect("clicked", functools.partial(maintenance.on_click_apply_parallel_downloads, self))

    if fn.check_content("ParallelDownloads", fn.pacman):
        for number in numbers:
            self.parallel_downloads.get_model().append(number)  # string
        act_number = maintenance.pop_parallel_downloads(self)
        self.parallel_downloads.set_selected(act_number)

    else:
        btn_apply_parallel_downloads.set_sensitive(False)

    hbox12_label.set_margin_start(10)
    hbox12_label.set_margin_end(10)
    hbox12_label.set_hexpand(True)
    hbox12.append(hbox12_label)
    self.parallel_downloads.set_margin_start(10)
    self.parallel_downloads.set_margin_end(10)
    hbox12.append(self.parallel_downloads)  # pack_end
    btn_apply_parallel_downloads.set_margin_start(10)
    btn_apply_parallel_downloads.set_margin_end(10)
    hbox12.append(btn_apply_parallel_downloads)  # pack_end

    hbox13 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox13_label = Gtk.Label(xalign=0)
    hbox13_label.set_text("Choose your cursor theme for installed desktops and SDDM")
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
    hbox13_label.set_margin_start(10)
    hbox13_label.set_margin_end(10)
    hbox13_label.set_hexpand(True)
    hbox13.append(hbox13_label)
    self.cursor_themes.set_margin_start(10)
    self.cursor_themes.set_margin_end(10)
    hbox13.append(self.cursor_themes)  # pack_end
    btn_apply_cursor.set_margin_start(10)
    btn_apply_cursor.set_margin_end(10)
    hbox13.append(btn_apply_cursor)  # pack_end
    self.cursor_theme_preview.set_margin_start(10)
    self.cursor_theme_preview.set_margin_end(10)
    hbox13.append(self.cursor_theme_preview)

    hbox14 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox14_label = Gtk.Label(xalign=0)
    hbox14_label.set_markup("Provide probe link")
    btn_probe = Gtk.Button(label="Get probe link")
    btn_probe.connect("clicked", functools.partial(maintenance.on_click_probe, self))
    hbox14_label.set_margin_start(10)
    hbox14_label.set_margin_end(10)
    hbox14_label.set_hexpand(True)
    hbox14.append(hbox14_label)
    btn_probe.set_margin_start(10)
    btn_probe.set_margin_end(10)
    hbox14.append(btn_probe)  # pack_end

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
    lbl_sec_sys_config.set_markup("<b>System Configuration</b>")
    lbl_sec_sys_config.set_margin_start(10)
    lbl_sec_sys_config.set_margin_top(15)
    lbl_sec_sys_config.set_margin_bottom(5)
    hbox_sec_sys_config.append(lbl_sec_sys_config)

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

    vboxstack19.append(hbox1)
    vboxstack19.append(hbox0)

    vboxstack19.append(hbox_sec_system)
    vboxstack19.append(hbox22)
    vboxstack19.append(hbox23)
    vboxstack19.append(hbox25)

    vboxstack19.append(hbox_sec_mirrors)
    vboxstack19.append(hbox40)
    vboxstack19.append(hbox4)
    vboxstack19.append(hbox3)

    vboxstack19.append(hbox_sec_keys)
    vboxstack19.append(hbox5)
    vboxstack19.append(hbox2)
    vboxstack19.append(hbox7)
    vboxstack19.append(hbox8)

    vboxstack19.append(hbox_sec_pacman_config)
    vboxstack19.append(hbox12)

    vboxstack19.append(hbox_sec_sys_config)
    vboxstack19.append(hbox13)

    vboxstack19.append(hbox_sec_diagnostics)
    vboxstack19.append(hbox14)
