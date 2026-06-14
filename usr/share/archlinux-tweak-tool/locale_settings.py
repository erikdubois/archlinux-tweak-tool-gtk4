# ============================================================
# Authors: Erik Dubois
# ============================================================

import os
import stat
import tempfile
import threading
import subprocess
import functions as fn
from gi.repository import GLib, Gtk

# Per-category locale overrides exposed in the UI. Each can follow LANG (unset)
# or carry its own generated locale, e.g. English system + European formatting.
LC_SENTINEL = "Use LANG (default)"
LC_CATEGORIES = ["LC_NUMERIC", "LC_MONETARY", "LC_TIME"]


def _fetch(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip().splitlines()


def _set_dropdown(dropdown, items, current):
    model = Gtk.StringList()
    for item in items:
        model.append(item)
    dropdown.set_model(model)
    try:
        idx = items.index(current)
    except ValueError:
        idx = 0
    dropdown.set_selected(idx)


def _parse_localectl():
    result = subprocess.run(["localectl", "status"], capture_output=True, text=True)
    data = {}
    for line in result.stdout.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            data[key.strip()] = val.strip()
    return data


def _read_locale_conf():
    """Parse /etc/locale.conf into a dict of LOCALE variables (authoritative source)."""
    conf = {}
    try:
        with open("/etc/locale.conf") as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                key, _, val = stripped.partition("=")
                conf[key.strip()] = val.strip().strip('"')
    except OSError:
        pass
    return conf


def _apply_locale_vars(self, conf, summary):
    """Re-send the complete locale set; localectl set-locale replaces /etc/locale.conf wholesale."""
    assignments = [f"{k}={v}" for k, v in conf.items() if v]
    if not assignments:
        fn.log_warn("No locale variables to set")
        return
    try:
        subprocess.run(["localectl", "set-locale", *assignments], check=True)
        fn.log_success(summary)
        GLib.idle_add(fn.show_in_app_notification, self, summary)
    except subprocess.CalledProcessError as e:
        fn.log_error(f"Failed to set locale: {e}")
    refresh_status(self)


def get_x11_variants(layout):
    result = subprocess.run(["localectl", "list-x11-keymap-variants", layout], capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()
    return [""] + lines if lines else [""]


def refresh_status(self):
    status = _parse_localectl()
    lang = status.get("System Locale", "LANG=—").replace("LANG=", "")
    vc_keymap = status.get("VC Keymap", "—")
    x11_layout = status.get("X11 Layout", "—")
    x11_variant = status.get("X11 Variant", "")
    x11_display = x11_layout + (f" ({x11_variant})" if x11_variant else "")

    tz_result = subprocess.run(
        ["timedatectl", "show", "--property=Timezone", "--value"], capture_output=True, text=True
    )
    timezone = tz_result.stdout.strip() or "—"

    GLib.idle_add(self.lbl_locale_current.set_text, lang)
    GLib.idle_add(self.lbl_keymap_current.set_text, vc_keymap)
    GLib.idle_add(self.lbl_x11_current.set_text, x11_display)
    GLib.idle_add(self.lbl_timezone_current.set_text, timezone)


def populate_dropdowns(self):
    def _run():
        locales = _fetch(["localectl", "list-locales"]) or ["en_US.UTF-8"]
        keymaps = _fetch(["localectl", "list-keymaps"]) or ["us"]
        x11_layouts = _fetch(["localectl", "list-x11-keymap-layouts"]) or ["us"]
        timezones = _fetch(["timedatectl", "list-timezones"]) or ["UTC"]

        status = _parse_localectl()
        current_locale = status.get("System Locale", "LANG=en_US.UTF-8").replace("LANG=", "")
        current_keymap = status.get("VC Keymap", "")
        current_x11_layout = status.get("X11 Layout", "")
        current_x11_variant = status.get("X11 Variant", "")
        current_tz = subprocess.run(
            ["timedatectl", "show", "--property=Timezone", "--value"], capture_output=True, text=True
        ).stdout.strip()

        variants = get_x11_variants(current_x11_layout) if current_x11_layout else [""]
        x11_display = current_x11_layout + (f" ({current_x11_variant})" if current_x11_variant else "")

        conf = _read_locale_conf()
        lc_items = [LC_SENTINEL] + locales
        lc_current = {cat: conf.get(cat, "") for cat in LC_CATEGORIES}

        def _populate():
            _set_dropdown(self.locale_dropdown, locales, current_locale)
            _set_dropdown(self.keymap_dropdown, keymaps, current_keymap)
            _set_dropdown(self.timezone_dropdown, timezones, current_tz)
            _set_dropdown(self.x11_layout_dropdown, x11_layouts, current_x11_layout)
            _set_dropdown(self.x11_variant_dropdown, variants, current_x11_variant)
            for cat in LC_CATEGORIES:
                _set_dropdown(self.lc_dropdowns[cat], lc_items, lc_current[cat] or LC_SENTINEL)
            self._locale_populating[0] = False
            self.lbl_locale_current.set_text(current_locale or "—")
            self.lbl_keymap_current.set_text(current_keymap or "—")
            self.lbl_x11_current.set_text(x11_display or "—")
            self.lbl_timezone_current.set_text(current_tz or "—")

        GLib.idle_add(_populate)

    threading.Thread(target=_run, daemon=True).start()


def on_apply_locale(self, _widget):
    fn.log_subsection("Locale - Apply System Locale")
    obj = self.locale_dropdown.get_selected_item()
    if obj is None:
        return
    locale_val = obj.get_string()
    fn.log_info(f"Setting LANG={locale_val} (preserving per-category LC_* overrides)")

    def _apply():
        conf = _read_locale_conf()
        conf["LANG"] = locale_val
        _apply_locale_vars(self, conf, f"System locale set to {locale_val}")

    threading.Thread(target=_apply, daemon=True).start()


def on_apply_lc(self, category, _widget):
    fn.log_subsection(f"Locale - Apply {category}")
    dropdown = self.lc_dropdowns.get(category)
    if dropdown is None:
        return
    obj = dropdown.get_selected_item()
    if obj is None:
        return
    choice = obj.get_string()

    def _apply():
        conf = _read_locale_conf()
        if choice == LC_SENTINEL:
            conf.pop(category, None)
            summary = f"{category} reset to follow LANG"
        else:
            conf[category] = choice
            summary = f"{category} set to {choice}"
        fn.log_info(summary)
        _apply_locale_vars(self, conf, summary)

    threading.Thread(target=_apply, daemon=True).start()


def on_reset_lc(self, _widget):
    fn.log_subsection("Locale - Reset per-category overrides to LANG")

    def _reset():
        conf = _read_locale_conf()
        for category in LC_CATEGORIES:
            conf.pop(category, None)
        _apply_locale_vars(self, conf, "Per-category locale overrides reset to LANG")
        for dropdown in self.lc_dropdowns.values():
            GLib.idle_add(dropdown.set_selected, 0)

    threading.Thread(target=_reset, daemon=True).start()


def _do_apply_keymap(self, keymap):
    fn.log_info(f"Setting VC keymap: {keymap}")
    try:
        subprocess.run(["localectl", "set-keymap", keymap], check=True)
        fn.log_success(f"Console keymap set to {keymap}")
        GLib.idle_add(fn.show_in_app_notification, self, f"Console keymap set to {keymap}")
    except subprocess.CalledProcessError as e:
        fn.log_error(f"Failed to set keymap: {e}")
    refresh_status(self)


def on_apply_keymap(self, _widget):
    fn.log_subsection("Locale - Apply Console Keymap")
    obj = self.keymap_dropdown.get_selected_item()
    if obj is None:
        return
    threading.Thread(target=_do_apply_keymap, args=(self, obj.get_string()), daemon=True).start()


def on_sync_keymap(self, _widget):
    fn.log_subsection("Locale - Sync TTY keymap from X11 layout")

    def _sync():
        status = _parse_localectl()
        x11_layout = status.get("X11 Layout", "")
        if not x11_layout:
            fn.log_warn("No X11 layout set, cannot sync")
            return
        model = self.keymap_dropdown.get_model()
        if not model:
            fn.log_warn("Keymap list not loaded yet — cannot sync")
            return
        n = model.get_n_items()
        for i in range(n):
            if model.get_item(i).get_string() == x11_layout:
                GLib.idle_add(self.keymap_dropdown.set_selected, i)
                break
        else:
            fn.log_warn(f"No TTY keymap matching '{x11_layout}' — sync not possible")
            return
        _do_apply_keymap(self, x11_layout)

    threading.Thread(target=_sync, daemon=True).start()


def on_apply_x11(self, _widget):
    fn.log_subsection("Locale - Apply X11 Keyboard Layout")
    layout_obj = self.x11_layout_dropdown.get_selected_item()
    if layout_obj is None:
        return
    layout = layout_obj.get_string()
    variant_obj = self.x11_variant_dropdown.get_selected_item()
    variant = variant_obj.get_string() if variant_obj else ""
    fn.log_info(f"Setting X11 layout: {layout} variant: {variant or '(none)'}")

    def _apply():
        try:
            cmd = ["localectl", "set-x11-keymap", layout]
            if variant:
                cmd.append(variant)
            subprocess.run(cmd, check=True)
            fn.log_success(f"X11 layout set to {layout} {variant}".strip())
            GLib.idle_add(fn.show_in_app_notification, self, f"X11 layout set to {layout}")
        except subprocess.CalledProcessError as e:
            fn.log_error(f"Failed to set X11 layout: {e}")
        refresh_status(self)

    threading.Thread(target=_apply, daemon=True).start()


def get_available_locales():
    try:
        with open("/usr/share/i18n/SUPPORTED") as f:
            lines = f.readlines()
    except OSError:
        return []
    locales = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if parts:
            locales.append(parts[0])
    return sorted(set(locales))


def _update_locale_gen(locale_val):
    try:
        with open("/usr/share/i18n/SUPPORTED") as f:
            supported_map = {}
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                parts = stripped.split()
                if len(parts) >= 2:
                    supported_map[parts[0]] = stripped
    except OSError:
        fn.log_error("Cannot read /usr/share/i18n/SUPPORTED")
        return False

    full_entry = supported_map.get(locale_val)
    if full_entry is None:
        fn.log_warn(f"No SUPPORTED entry for {locale_val} — using bare name (charset may be missing)")
        full_entry = locale_val

    try:
        with open("/etc/locale.gen") as f:
            lines = f.readlines()
    except OSError:
        fn.log_error("Cannot read /etc/locale.gen")
        return False

    if any(line.strip() == full_entry for line in lines):
        fn.log_info(f"{locale_val} already enabled in /etc/locale.gen")
        return True

    new_lines = []
    uncommented = False
    for line in lines:
        stripped = line.strip()
        if stripped in (f"#{full_entry}", f"# {full_entry}"):
            new_lines.append(f"{full_entry}\n")
            uncommented = True
        else:
            new_lines.append(line)

    if not uncommented:
        new_lines.append(f"{full_entry}\n")
        fn.log_info(f"Appended {full_entry} to /etc/locale.gen")
    else:
        fn.log_info(f"Uncommented {locale_val} in /etc/locale.gen")

    try:
        with open("/etc/locale.gen", "w") as f:
            f.writelines(new_lines)
        fn.log_success("Updated /etc/locale.gen")
        return True
    except OSError as e:
        fn.log_error(f"Cannot write /etc/locale.gen: {e}")
        return False


def on_apply_generate_locale(self, _widget):
    fn.log_subsection("Locale - Generate New Locale")
    obj = self.available_locale_dropdown.get_selected_item()
    if obj is None or not obj.get_string():
        fn.log_warn("No locale selected")
        return
    locale_val = obj.get_string()
    fn.log_info(f"Generating locale: {locale_val}")

    script = f"""#!/bin/bash
set -euo pipefail
RESET=$(tput sgr0)
CYAN=$(tput setaf 6)
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
YELLOW=$(tput setaf 3)
separator() {{ printf '%*s\\n' "${{COLUMNS:-80}}" '' | tr ' ' '-'; }}
header()  {{ separator; echo "${{CYAN}}>>> $*${{RESET}}"; separator; }}
success() {{ echo "${{GREEN}}[OK]  $*${{RESET}}"; }}
info()    {{ echo "      $*"; }}
warn()    {{ echo "${{YELLOW}}[!!]  $*${{RESET}}"; }}
error()   {{ echo "${{RED}}[!!]  $*${{RESET}}"; }}

header "Generate Locale: {locale_val}"
info "Running locale-gen..."
locale-gen
success "locale-gen completed"

header "Set System Locale"
localectl set-locale "LANG={locale_val}"
success "System locale set to {locale_val}"

read -p "Press Enter to close..."
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".sh", delete=False) as f:
        f.write(script)
        tmp_path = f.name
    os.chmod(tmp_path, stat.S_IRWXU)
    fn.show_in_app_notification(self, f"Generating locale {locale_val}...")

    def _run():
        if not _update_locale_gen(locale_val):
            os.unlink(tmp_path)
            return
        proc = subprocess.Popen(
            ["alacritty", "-e", "bash", tmp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        proc.wait()
        os.unlink(tmp_path)
        fn.log_success(f"Locale {locale_val} generated and set")
        GLib.idle_add(refresh_status, self)

    threading.Thread(target=_run, daemon=True).start()


def on_apply_timezone(self, _widget):
    fn.log_subsection("Locale - Apply Timezone")
    obj = self.timezone_dropdown.get_selected_item()
    if obj is None:
        return
    tz = obj.get_string()
    fn.log_info(f"Setting timezone: {tz}")

    def _apply():
        try:
            subprocess.run(["timedatectl", "set-timezone", tz], check=True)
            fn.log_success(f"Timezone set to {tz}")
            GLib.idle_add(fn.show_in_app_notification, self, f"Timezone set to {tz}")
        except subprocess.CalledProcessError as e:
            fn.log_error(f"Failed to set timezone: {e}")
        refresh_status(self)

    threading.Thread(target=_apply, daemon=True).start()
