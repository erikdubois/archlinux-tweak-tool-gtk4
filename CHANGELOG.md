# Arch Linux Tweak Tool — Changelog

## 2026.05.02 - Code Quality: Themer Refactoring, Linting, Brand Cleanup

### What Changed

#### Themer Module Refactoring (themer.py / themer_gui.py)

- **GTK4 StringList population optimized** — dropdown initialization changed from one-by-one `append()` to batch `splice()` with full list; resolves empty dropdowns on first load
- **qtile theme detection fixed** — `isfile()` check replaced with `path_check()` for directory validation (line 54 and 353); UnboundLocalError on qtile theme load now resolved
- **on_polybar_toggle callback signature corrected** — changed from `(self, widget, active)` to `(self, _widget, _pspec=None)` to match GTK4 notify::active signal; polybar checkbox now functions
- **Theme name extraction refactored** — replaced `range(len(...))` loops with `enumerate()` pattern per PEP 8; removed accompanying TODO comments
- **Dead debug output removed** — removed temporary debug print statements used during troubleshooting
- **fn.readlink corrected** — changed incorrect `fn.readlink` to `fn.os.readlink` (line 354)

#### Brand Name Cleanup (4 Files)

- **shell_gui.py** — UI message updated: "Activate the ArcoLinux repos" → "Activate the nemesis repo (when needed)" (line 154)
- **functions_startup.py** — Startup message updated: "installing default from ARCO template" → "installing default from ATT template"
- **desktopr_gui.py** — Removed non-existent `button_reinstall.set_sensitive()` call that was causing AttributeError (only `button_install` exists)
- **gui.py** — Removed deprecated `fastfetch_message.set_markup()` call entirely (fastfetch config section now message-free)

#### Linting & Code Quality (Multiple Files)

- **E241 fixed** — `shell.py` and `shell.py`: Removed alignment spaces after commas in package tuples (lines 326-334)
- **E226 fixed** — `functions.py`: Added whitespace around operators (`i+1` → `i + 1`)
- **E128 fixed** — `functions.py`: Reformatted multi-line `subprocess.run()` calls with proper indentation
- **E501 fixed** — `desktopr.py`: Split long lines at 637 and 659 to ≤120 characters
- **flake8 audit complete** — all remaining violations addressed; codebase now lint-clean

#### Startup Timer Refinement (archlinux-tweak-tool.py)

- Removed `print()` statement for total startup time; kept debug-only output via `fn.debug_print()`
- Added `[RESPONSIVE]` timer message marking when initialization completes and UI is ready for interaction

#### Documentation Updates (CLAUDE.md)

- **Requirements section added** — Python 3.8+, GTK4 4.6+, system tools, optional features documented
- **Objective 12 clarified** — "Data Folder Consolidation: Transition to Kiro-only data folder; update all paths before removing other distro-specific directories"

#### Memory & Developer Notes

- Created `distro_guards_intentional.md` — documents that `fn.distr` detection guards throughout codebase are intentional multi-distro support features, not code to be removed

### Technical Details

- GTK4 StringList splice pattern: build complete list with `[item1, item2, ...]`, then `model.splice(0, 0, full_list)` to populate in one operation
- enumerate() pattern: `for i, item in enumerate(items):` replaces `for i in range(len(items)):`
- qtile_config_theme is a directory (`~/.config/qtile/config.py`), not a file; requires `fn.path_check()` not `fn.isfile()`
- Brand reference policy: remove brand names from user-facing UI messages ("ArcoLinux" → "ATT", "ARCO template" → "ATT template"); preserve real package names (arcolinux-arc-*) and real folder names (/etc/skel/.config/arco-chadwm)

### Files Modified

`themer.py` • `themer_gui.py` • `shell_gui.py` • `shell.py` • `functions.py` • `functions_startup.py` • `desktopr_gui.py` • `gui.py` • `archlinux-tweak-tool.py` • `CLAUDE.md` • `CHANGELOG.md`

---

## Frozen Files — Do Not Edit Without Explicit Permission

These files are tested and working. Any change requires user confirmation first.

| File | Covers |
| ---- | ------ |
| `pacman_gui.py` | Pacman page UI — switches, AUR buttons, custom repo, blank pacman, reset/edit row |
| `pacman.py` | Pacman toggle callbacks, update_repos_switches, parallel downloads |
| `pacman_functions.py` | Repo read/write helpers, AUR helper install/remove, toggle_test_repos |
| `ai.py` | AI tools callbacks — install/remove ollama, LLM runners |
| `ai_gui.py` | AI Tools page UI — Local LLM Runners section |
| `packages.py` | Package export/import/install logic |
| `packages_gui.py` | Packages page UI — export, import, install from list |
| `sddm.py` | SDDM callbacks — apply settings, wallpaper, install/remove Simplicity theme |
| `sddm_gui.py` | SDDM page UI — theme, session, cursor, autologin, wallpaper section |
| `icons.py` | Icon theme callbacks — Sardi, Surfn, Neo Candy install/remove/find |
| `icons_gui.py` | Icons page UI — three sub-tabs with FlowBox checkboxes, preview lightbox, centred action buttons |
| `shell.py` | Shell switching callbacks — bash, fish, zsh, oh-my-zsh, oh-my-fish install/remove |
| `shell_gui.py` | Shells page UI — shell switcher, ZSH theme selector, preview images |
| `kernel.py` | Kernel list, CPU compatibility checks, install/remove via Alacritty, boot entry management |
| `kernel_gui.py` | Kernels page UI — per-kernel rows with status/install/remove, systemd-boot default selector |
| `log_callbacks.py` | Logging callbacks — journalctl, dmesg, pacman log, Xorg log, systemd-analyze viewers |
| `logging_gui.py` | Logging page UI — nine log viewer button rows |
| `maintenance.py` | Maintenance callbacks — cache clean, orphan remove, pacman lock, mirrors, hw-probe, cursors |
| `maintenance_gui.py` | Maintenance page UI — all button rows and section layout |
| `autostart.py` | Autostart callbacks — enable/disable autostart entries |
| `autostart_gui.py` | Autostart page UI |
| `network_gui.py` | Network page UI — nsswitch, network discovery, samba, samba user |
| `services.py` | Services callbacks — nsswitch, discovery install/disable, samba install/remove/user |
| `fastfetch.py` | Fastfetch callbacks — install/remove, config apply |
| `fastfetch_gui.py` | Fastfetch page UI |
| `performance.py` | Performance callbacks — tuned, irqbalance, ananicy, gamemode, zram, swapfile, fstrim |
| `performance_gui.py` | Performance page UI — all sections and button rows |
| `privacy.py` | Privacy callbacks — uBlock Origin install/remove, hblock install/remove/enable/disable |
| `privacy_gui.py` | Privacy page UI — Content Blocking and Network &amp; Tracking Protection sections |
| `themes.py` | Arc theme callbacks — install/remove/find, preset selections (all/blue/dark/none) |
| `themes_gui.py` | Themes page UI — FlowBox checkboxes, preset buttons, action buttons, preview image |
| `software.py` | Software callbacks — launch/install/remove for GUI managers, AUR helpers, Flatpak/Snap/AppImage, TUI tools, logout managers |
| `software_gui.py` | Software page UI — five sections with install/remove rows |
| `user.py` | User account callbacks — create user, delete user, delete user + home folder, populate dropdown |
| `user_gui.py` | User page UI — create user form, delete user section, arch visudo note |
| `system.py` | System info callbacks — CPU, memory, block/PCI/USB/block devices, inxi, hwinfo, fdisk, fstab, hostnamectl, localectl, systemd services/timers, dmesg, gparted, partitionmanager |
| `system_gui.py` | System page UI — 20 viewer rows; gparted and partitionmanager show installed status |

---

## 2026.05.02 - XFCE Removal: Force Removal with Smart Cleanup

### What Changed

- **XFCE now uses `-Rdd` (force removal)** like Plasma, since XFCE has complex inter-package and external dependencies
- **Detects installed panel variant** — checks for both `xfce4-panel` (default) and `xfce4-panel-compiz`, removes only what's installed
- **Two-stage cleanup** — main removal of core packages + cleanup step that removes all plugins and ecosystem apps
- **Comprehensive package removal** includes:
  - All `xfce4-*` plugins (30+ variants: battery, clipman, cpufreq, cpugraph, dict, diskperf, eyes, fsguard, genmon, mailwatch, mount, mpc, netload, notes, notifyd, places, pulseaudio, screenshooter, sensors, smartbookmark, systemload, time-out, timer, verve, wavelan, weather, whiskermenu, xkb, etc.)
  - XFCE ecosystem apps: mousepad, parole, ristretto, xfburn
  - Thunar derivatives: thunar-archive-plugin, thunar-media-tags-plugin
- **UX improvements**: backup warning shows "might take a while", package list displayed before removal confirmation

### Technical Details

- Panel detection: `fn.check_package_installed("xfce4-panel")` and `fn.check_package_installed("xfce4-panel-compiz")`
- Panel replacement: removes compiz variant from list, inserts actual installed variant
- Filter logic: protects all `xfce4-*` except the detected panel variant + other package categories
- Cleanup: two-pronged approach:
  - `pacman -Rdd $(pacman -Q | grep '^xfce' | awk '{print $1}')` for all xfce4-* packages
  - Explicit removal of mousepad, parole, ristretto, xfburn, thunar plugins
- All in one `-Rdd` command with `--noconfirm` to bypass dependency checks

### Why `-Rdd` for XFCE

Like Plasma, XFCE has many plugins and ecosystem apps that create a complex dependency web:

- 30+ xfce4-*-plugin packages require xfce4-panel
- parole (media player) requires xfconf, tumbler, libxfce4ui
- ristretto (image viewer) requires exo, xfconf, tumbler, libxfce4ui
- xfburn (CD/DVD) requires libxfce4ui, exo
- Thunar plugins require thunar
- User may have additional packages (xfce4-screensaver, xfce4-taskmanager, etc.)

Using `-Rs` (respects dependencies) fails due to circular dependencies and external references. Force removal (`-Rdd`) cleanly removes the entire environment in one operation.

### Files Modified

`desktopr.py`, `CHANGELOG.md`

---

## 2026.05.02 - Desktop UI: Consolidate Install/Re-Install into Single Button

### What Changed

- **Merged Install and Re-Install buttons** into single "Install" button in `desktopr_gui.py`:
  - Removed `self.button_reinstall` entirely (was redundant after terminal-first refactor)
  - Updated install button connection to use new `on_install_clicked(self, _widget)` signature (no state parameter)
  - Changed checkbox label from "Select to clear cache before re-install" to "Clear package cache before installation"
  - Checkbox is always visible and functional for both install and reinstall workflows
- **Simplified install flow in desktopr.py**:
  - Removed `state` parameter from `on_install_clicked()`, `check_lock()`, and `install_desktop()` functions
  - All install paths now use same branch (unified logic)
  - Cache clearing still available via always-visible checkbox
- **Rationale:** After terminal-first refactor, Install and Re-Install had identical logic; consolidation removes duplication and simplifies UX

### Technical Details

- `check_lock()` signature changed: `def check_lock(self, desktop, state):` → `def check_lock(self, desktop):`
- `install_desktop()` signature changed: `def install_desktop(self, desktop, state):` → `def install_desktop(self, desktop):`
- `on_install_clicked()` signature changed: `def on_install_clicked(self, widget, state):` → `def on_install_clicked(self, _widget):`
- Removed all conditional `if state == "reinst":` branches; cache clear logic now uniform: `if self.ch1.get_active(): cache_clear = ...`
- Updated both Thread argument tuples in `check_lock()` to pass only `(self, fn.get_combo_text(self.d_combo))`

### Files Modified

`desktopr.py`, `desktopr_gui.py`, `CHANGELOG.md`

---

## 2026.05.02 - Desktop Uninstall: Label Feedback Instead of Messagebox

### What Changed

- **uninstall_desktop() UX improved** — removed messagebox, replaced with label feedback:
  - After removal completes, display removal message directly in `desktop_status` label
  - Message shows: "[desktop] has been removed" + "We do not remove code from your home directory..."
  - Message auto-clears after 5 seconds (GLib.timeout_add)
  - Label updates to "This desktop is NOT installed" after timeout
- **Rationale:** Less intrusive than modal dialog; user sees result inline with UI; automatic cleanup

### Files Modified

`desktopr.py`, `CHANGELOG.md`

---

## 2026.05.02 - Install Desktop: Terminal-First Pattern with Transparency

### What Changed

- **install_desktop() refactored** to use alacritty terminal-first pattern (like uninstall):
  - Opens alacritty terminal before installation begins
  - Shows complete list of packages to be installed
  - Displays actual `pacman -S` command
  - User reviews and presses Enter to confirm
  - Installation runs visibly in terminal (not in background)
  - Shows "=== Installation Complete ===" and waits for Enter to close
- **Backup happens first** — ~/.config backed up to ~/.config-att/ BEFORE terminal opens (early, safe)
- **Cache clear option preserved** — if "Re-Install" + checkbox enabled, cache cleared in terminal before install
- **Config copy still happens after** — only if installation succeeds (check_desktop confirms)
- **3-channel logging preserved** — console output shows progress at key milestones; debug output shows implementation details

### Technical Details

- Build bash script string with full package list displayed + install command visible
- Launch via `alacritty -e bash -c` in daemon thread so ATT stays responsive
- After terminal closes, check if desktop installed before copying configs
- Uses `GLib.idle_add` for UI updates from daemon thread
- Console logging unchanged: log_section, log_subsection, log_info, log_success preserved

### Files Modified

`desktopr.py`, `CHANGELOG.md`

---

## 2026.05.02 - 3-Channel Communication in Desktop Install/Uninstall

### What Changed

- **install_desktop() communication enhanced** with 3-channel logging:
  - **In-app notification** — "Starting installation...", "[package] installed", completion status
  - **Console (always-visible)** — `log_section` at start, `log_subsection` for package count, `log_info` for backup/copy operations, `log_success` on completion, `log_error` on failure
  - **Debug output** — detailed package list, return codes, copy paths, error details (via `fn.debug_print`)
- **uninstall_desktop() communication enhanced** with same 3-channel pattern:
  - **In-app notification** — removal start/completion status
  - **Console** — `log_section` at start, `log_info` for package filtering details, `log_success` on completion
  - **Debug output** — package lists, filtering logic, completion notes
- **Transparency principle:** User can now follow the entire install/uninstall process in console without needing `--debug` flag; debug output provides implementation details

### Technical Details

- Install flow: backup notification → package count subsection → per-package info lines → completion success
- Uninstall flow: removal start section → filtered package count → removal completion
- All operations show source→target details in debug mode but only key milestones in normal console output
- Alacritty terminal still uses "Press Enter to close" pattern for user confirmation

### Files Modified

`desktopr.py`, `CHANGELOG.md`

---

## 2026.05.02 - Desktop Uninstall Feature

### What Changed

- **New uninstall_desktop() function** in `desktopr.py` — safely removes desktop environment packages while preserving:
  - Essential packages: alacritty, feh, dmenu, noto-fonts, thunar (and all thunar plugins), xfce4-* family
  - Packages used by other installed desktops (no breaking dependencies)
  - User home directory (never modified)
- **on_uninstall_clicked() callback** — checks if desktop is installed before uninstall; shows notification if not installed
- **Remove Desktop button** in `desktopr_gui.py` — new uninstall_hbox with single button, reuses existing dropdown selector
- **Terminal display** — alacritty shows `pacman -R [packages]` with user confirmation
- **Completion messagebox** — displays "The desktop [name] has been removed. We do not remove code from your home directory, only apps without dependencies"
- **Daemon threading** — terminal launches in background thread, ATT stays responsive

### Technical Details

- Package filtering: iterate through all desktops, build set of "packages used elsewhere", exclude those from removal list
- Essential list is hardcoded (never changes); regex check for xfce4-* prefix handles all xfce metapackages
- Uses same terminal pattern as install: Popen + daemon thread + messagebox completion dialog
- Remove command shown to user first (transparency principle)

### Files Modified

`desktopr.py`, `desktopr_gui.py`, `CHANGELOG.md`

---

## 2026.05.02 - Final F401 Cleanup — Unused Imports Removed & Intentional Exports Restored

### What Changed

- **F401 unused imports removed** — achieved flake8 compliance by distinguishing truly unused imports from intentional re-exports
- `archlinux-tweak-tool.py` — removed: `subprocess`, `datetime`, `desktopr_gui`, `utilities`; removed `Gio` from `gi.repository`; removed `from os import readlink`; removed unused global `att`
- `functions.py` — removed truly unused: `rmdir`, `walk` from os; removed duplicate `import sys` and `import subprocess`
- **Intentional re-exports restored with `# noqa: F401`** — marked imports that are deliberately exported for dependent modules to use via `fn.*` pattern:
  - `getpid` — used by `archlinux-tweak-tool.py` as `fn.getpid()`
  - `stat` — used by `functions_startup.py` as `fn.stat()`
  - `system` — used by `user.py`, `services.py` as `fn.system()`
  - `readlink` — used by `themer_gui.py` as `fn.readlink()`
  - `Queue` — used by `packages_gui.py` as `fn.Queue`

### Technical Details

- Re-exports are intentional module design: import something into functions.py namespace so dependent code can access it via `fn.*` without knowing the original module
- Distinguishing re-exports from truly unused imports prevents breaking runtime code during lint cleanup
- All marked with `# noqa: F401` to suppress flake8 checks

### Files Modified

`archlinux-tweak-tool.py`, `functions.py`, `CHANGELOG.md`

**Objective 13 (Remove Dead Code) & Objective 23 (Lint) status: COMPLETE**

---

## 2026.05.01 - Project-wide Lint Pass

### What Changed

- **E722** bare `except` → `except Exception`: `autostart.py`, `functions.py` (×2), `themer_gui.py` (×3)
- **E702** semicolons split to separate lines: `themer.py` (×3)
- **F821** undefined `readlink` → `fn.os.readlink`: `themer.py`
- **E306** missing blank line before nested `def`: `ai.py` (×7)
- **E501** lines wrapped to ≤120 chars: `ai.py`, `ai_gui.py`, `autostart.py`, `packages.py`, `packages_gui.py`, `sddm_gui.py`, `shell_gui.py`, `zsh_theme.py`, `functions.py`, `archlinux-tweak-tool.py`
- **E305** missing blank lines after function: `functions.py`, `archlinux-tweak-tool.py`
- **E265** malformed block comment: `pacman_gui.py`
- **W293** whitespace in blank lines: `fastfetch.py`, `utilities.py`, `pacman_gui.py`
- **W391** trailing blank line: `fastfetch_gui.py`
- **F841** unused local variables removed: `packages.py` (×4), `pacman_gui.py` (×3)
- **F401** unused imports removed: `fastfetch.py` (×2), `functions_makedir.py`, `gui.py`, `packages.py`, `packages_gui.py`
- Skipped: `E402` (intentional import order), `E128` (style preference), `E203` (slice style), F401 in `functions.py` (exports used via `fn.*`), F401 in `archlinux-tweak-tool.py` (startup imports)

### Files Modified

`ai.py`, `ai_gui.py`, `archlinux-tweak-tool.py`, `autostart.py`, `fastfetch.py`, `fastfetch_gui.py`, `functions.py`, `functions_makedir.py`, `gui.py`, `packages.py`, `packages_gui.py`, `pacman_gui.py`, `sddm_gui.py`, `shell_gui.py`, `themer.py`, `themer_gui.py`, `utilities.py`, `zsh_theme.py`, `CHANGELOG.md`

---

## 2026.05.01 - Privacy Tab Rewrite

### What Changed

- `privacy.py` — replaced stub `set_ublock_firefox` and blocking `set_hblock` switch callbacks with six button callbacks: install/remove for uBlock Origin, install/remove for hblock, enable/disable for hblock; enable/disable run in daemon threads with pulsing progress bar
- `privacy_gui.py` — replaced switches with install/remove button rows for both uBlock and hblock; added enable/disable row for hblock with live enabled/disabled status label; sections separated by horizontal separator; progress bar restored

### Files Modified

`privacy.py`, `privacy_gui.py`, `CHANGELOG.md`

---

## 2026.05.01 - Services and Desktopr Tab Cleanup

### What Changed

- `services_gui.py` — E712 fixed: `== True` comparison changed to bare truthiness check
- `desktopr.py` — E722 fixed: bare `except` → `except Exception`
- `desktopr_gui.py` — E722 fixed: bare `except` → `except Exception`; W293 fixed: whitespace-only blank lines stripped
- Both tabs pass `flake8 --max-line-length=120` with zero errors

### Files Modified

`services_gui.py`, `desktopr.py`, `desktopr_gui.py`, `CHANGELOG.md`

---

## 2026.05.01 - Kernel Tab Cleanup

### What Changed

- `kernel.py` — 1× E501 fixed: `subprocess.Popen(...)` call wrapped
- `kernel_gui.py` — E306 fixed: missing blank line before nested `install_and_notify` definition
- Both files pass `flake8 --max-line-length=120` with zero errors

### Files Modified

`kernel.py`, `kernel_gui.py`, `CHANGELOG.md`

---

## 2026.05.01 - Icons Tab Cleanup

### What Changed

- `icons_gui.py` — 1× E501 fixed: `_att_preview_picture(...)` call for surfn.jpg wrapped
- `icons.py` — no changes required; no flake8 errors, all callbacks already use `_widget`
- Both files pass `flake8 --max-line-length=120` with zero errors

### Files Modified

`icons_gui.py`, `CHANGELOG.md`

---

## 2026.05.01 - Performance Tab Cleanup

### What Changed

- `performance_gui.py` — 1× E501 fixed: `swapfile_label.set_markup(...)` line wrapped
- `performance.py` — no changes required; all callbacks already use `_widget`, no flake8 errors
- Both files pass `flake8 --max-line-length=120` with zero errors

### Files Modified

`performance_gui.py`, `CHANGELOG.md`

---

## 2026.05.01 - Maintenance Tab Cleanup

### What Changed

- `maintenance_gui.py` — F821 fixed: `_load_xcursor_pixbuf` called `fn.log_error()` but `fn` is not in scope in that function; replaced with bare `except Exception: return None`
- `maintenance_gui.py` — 4× E501 fixed: `btn_install_arch_keyring.connect`, `btn_install_arch_keyring_online.connect`, `btn_apply_pacman_gpg_conf_local.connect`, and `cursor_info_label.set_text` lines wrapped
- `maintenance.py` — no changes required; all callbacks already use `_widget`, no flake8 errors
- Both files pass `flake8 --max-line-length=120` with zero errors

### Files Modified

`maintenance_gui.py`, `CHANGELOG.md`

---

## 2026.05.01 - System Tab New Features

### What Changed

- `system.py` — added `hbox_partitionmanager` row: Launch/install button (installs via alacritty terminal then auto-launches) + Remove button with install guard
- `system.py` — added `hbox_gparted` Remove button with install guard
- `system_gui.py` — `self.lbl_gparted` and `self.lbl_partitionmanager` use `set_markup()` with conditional `<b>installed</b>` suffix — status visible on load
- `system.py` — `_refresh_gparted_label` and `_refresh_partitionmanager_label` helpers refresh label markup after install and after remove terminal closes (daemon thread + `GLib.idle_add`)
- `system.py` — `_pm_launch_cmd()` helper builds the partitionmanager launch command as the real user (`sudo -u username` + `XDG_RUNTIME_DIR` + `DBUS_SESSION_BUS_ADDRESS` + `DISPLAY` + `WAYLAND_DISPLAY`) — required because KDE/Qt apps need the user session environment and fail silently when launched as root
- Both files pass `flake8 --max-line-length=120` with zero errors

### Files Modified

`system.py`, `system_gui.py`, `CHANGELOG.md`

---

## 2026.05.01 - System Tab Cleanup

### What Changed

- `system.py` — `widget` → `_widget` in all 18 callbacks
- `system.py` — all `fn.subprocess.call()` replaced with `_run_cmd()` helper (Popen in daemon thread) — keeps ATT responsive while terminal viewers are open
- `system.py` — added module-level `_run_cmd(cmd)` helper to avoid repeating the Popen+daemon-thread pattern 18 times
- `system.py` — `import pwd` and `import time` moved from inside functions to top-level imports
- `system.py` — `on_click_system_gparted`: removed `&` from gparted launch command (unnecessary with Popen); `import time` removed from nested function
- `system.py` — E501 fixed: services_enabled and memory_disk command strings split across lines
- `system_gui.py` — `hbox1`–`hbox18` renamed to descriptive names: `hbox_cpu`, `hbox_memory_disk`, `hbox_lsblk`, `hbox_lspci`, `hbox_lsusb`, `hbox_lsmod`, `hbox_inxi`, `hbox_hwinfo`, `hbox_fdisk`, `hbox_fstab`, `hbox_hostnamectl`, `hbox_localectl`, `hbox_services`, `hbox_services_enabled`, `hbox_services_failed`, `hbox_timers_enabled`, `hbox_dmesg`, `hbox_gparted`
- `system_gui.py` — label variables renamed from `hbox1_label` pattern to `lbl_*` prefix; button variables renamed from `btn1` to `btn_*` with descriptive suffix
- Both files pass `flake8 --max-line-length=120` with zero errors

### Files Modified

`system.py`, `system_gui.py`, `CHANGELOG.md`

---

## 2026.05.01 - User Tab Cleanup

### What Changed

- `user.py` — critical bug fixed: `on_click_delete_user` and `on_click_delete_all_user` were each defined twice; the outer callback shadowed the inner implementation, causing the inner logic to be unreachable and the callback to call itself recursively. Inner implementations renamed to `_do_delete_user` and `_do_delete_all_user`; callbacks now call those
- `user.py` — `widget` → `_widget` in all 3 callbacks
- `user.py` — `pop_cbt_users` line 117: two statements on one line split to two; local variable renamed `_m` → `model` for clarity
- `user.py` — redundant duplicate `if password == confirm_password` guard removed
- `user_gui.py` — dead `import user` removed (module is passed as parameter, shadowed the import)
- `user_gui.py` — parameter `vboxStack10` → `vboxstack_user` (snake_case)
- `user_gui.py` — all numbered box variables renamed to descriptive names: `hbox_title`, `hbox_separator`, `hbox_admin_info`, `hbox_apply`, `hbox_delete_title`, `hbox_delete_separator`, `hbox_delete_warning`, `hbox_user_select`, `hbox_delete_all`, `hbox_delete_only`, `hbox_visudo`
- Both files pass `flake8 --max-line-length=120` with zero errors

### Files Modified

`user.py`, `user_gui.py`, `CHANGELOG.md`

---

## 2026.05.01 - Software Tab Cleanup

### What Changed

- `software.py` — all 22 callback signatures fixed: `widget` → `_widget`
- `software.py` — `fn.subprocess.call()` → `fn.subprocess.Popen()` in `on_click_software_appimagelauncher` launch path
- `software.py` — all 37 E501 line-length violations fixed (long `wait_install_and_update`, `wait_remove_and_update`, and `GLib.idle_add` calls wrapped to multiple lines)
- `software_gui.py` — `hbox1`–`hbox16` renamed to descriptive names: `hbox_pamac`, `hbox_octopi`, `hbox_gnome`, `hbox_discover`, `hbox_bauh`, `hbox_yay`, `hbox_paru`, `hbox_trizen`, `hbox_pikaur`, `hbox_flatpak`, `hbox_snapd`, `hbox_appimage`, `hbox_pacseek`, `hbox_pacui`, `hbox_archlinux_logout`, `hbox_powermenu`
- `software_gui.py` — all E501 violations fixed (long markup/connect lines wrapped)
- Both files pass `flake8 --max-line-length=120` with zero errors

### Files Modified

`software.py`, `software_gui.py`, `CHANGELOG.md`

---

## 2026.05.01 - Themes Tab Cleanup

### What Changed

- `themes.py` — all 7 callback signatures fixed: `widget` → `_widget`
- `themes_gui.py` — typo fixed: `"arcolinux-arc-tangerinex"` → `"arcolinux-arc-tangerine"`
- `themes_gui.py` — local box variables renamed to descriptive names: `hbox10` → `hbox_info`, `hbox11` → `hbox_checkboxes`, `hbox18` → `hbox_presets`, `hbox19` → `hbox_actions`

### Technical Details

- `self.arcolinux_arc_*` widget attributes are intentionally named after real AUR packages (`arcolinux-arc-*-git`) — not renamed
- All helper calls (`fn.wait_and_notify`, `fn.launch_pacman_install_in_terminal`, `fn.launch_pacman_remove_in_terminal`) confirmed present and correct

### Files Modified

`themes.py`, `themes_gui.py`, `CHANGELOG.md`

---

## 2026.04.30 - Frozen: Network, Fastfetch, Services GUI

### What Changed

- `network_gui.py` and `services.py` (network callbacks) frozen — network tab tested and working
- `fastfetch.py` and `fastfetch_gui.py` frozen — fastfetch tab tested and working
- `services_gui.py` inspected — single `fn.distr` guard (`garuda`, `manjaro`) confirmed correct and intentional; no changes made; tab not yet frozen pending audit of `services.py` (cups/audio/bluetooth callbacks)

### Files Modified

`CHANGELOG.md`

---

## 2026.04.30 - Performance Tab Overhaul

### What Changed

#### `performance.py` — full terminal pattern migration

- **Template applied to all packages with services** — tuned, irqbalance, ananicy, gamemode now all follow the single-terminal pattern: install = `pacman -S` + `systemctl enable --now` in one window; remove = `systemctl disable --now` + `pacman -R` in one window
- **`install_tuned_tools`** — rewritten as `_do_install` daemon thread; removes power-profiles-daemon first (waits for terminal to close), then installs tuned + tuned-ppd and enables both services in one combined terminal; already-installed guard added
- **`remove_tuned_tools`** — `_do_remove` daemon thread; disables and removes tuned + tuned-ppd in one combined terminal
- **`enable_tuned_services` / `disable_tuned_services` / `restart_tuned_service` / `restart_tuned_ppd_service`** — all converted from silent `fn.enable_service` calls to alacritty inline scripts with daemon `_wait_` threads
- **`self.tuned_package_label`** — renamed from local `hbox7_label` so callbacks can refresh it after install/remove; `refresh_tuned_package_label` added
- **`install_irqbalance`** — rewritten as daemon thread with combined install+enable terminal; already-installed guard added
- **`remove_irqbalance`** — daemon thread with combined disable+remove terminal; not-installed guard added
- **`enable_irqbalance_service` / `disable_irqbalance_service`** — converted to alacritty terminals with `_wait_` daemon threads
- **`install_ananicy`** — daemon thread with combined install+enable terminal; already-installed guard
- **`remove_ananicy`** — daemon thread with combined disable+remove terminal; not-installed guard
- **`enable_ananicy_service` / `disable_ananicy_service`** — alacritty terminals with `_wait_` daemon threads
- **`install_gamemode`** — daemon thread with combined install+enable terminal; bash user-detection block (`PKEXEC_UID` → `SUDO_USER` → `logname`) for gamemoded user service; already-installed guard
- **`remove_gamemode`** — daemon thread with disable+remove terminal; bash user-detection for gamemoded; not-installed guard
- **`enable_gamemode_service` / `disable_gamemode_service`** — alacritty terminals with bash user-detection and `_wait_` daemon threads
- **`run_gamemoded_user_command`** — removed (dead code; superseded by inline bash scripts)
- **`enable_fstrim_timer` / `disable_fstrim_timer` / `run_fstrim_now`** — converted from silent `subprocess.call` to alacritty inline scripts with `read -p`
- **`enable_zram` / `disable_zram` / `create_swapfile` / `remove_swapfile`** — all inlined into `bash -c` Popen calls; removed dependency on external script files; `trap 'read -p "Press Enter to close..."' EXIT` added so window stays open on any exit path including errors and unsupported filesystem
- **External script constants removed** — `zram_enable_script`, `zram_disable_script`, `swapfile_create_script`, `swapfile_remove_script` removed from module-level constants

#### `data/bin/` — defensive hardening

- **`create-swapfile`**, **`remove-swapfile`**, **`enable-zram`**, **`disable-zram`** — all four scripts now have `trap 'echo; read -p "Press Enter to close..."' EXIT` at the top; explicit `read -p` at end removed (trap handles it); scripts remain usable standalone

### Technical Details

- External script paths (`/usr/share/archlinux-tweak-tool/data/bin/`) fail silently in dev environments (scripts not installed there); inlining avoids the path issue entirely
- `trap ... EXIT` in bash fires on any exit — normal, `exit 1`, unhandled error — guaranteeing the terminal window stays open
- Gamemode uses `systemctl --user --machine="${REAL_USER}@.host"` because gamemoded is a user service; bash chain detects real user via `$PKEXEC_UID` (getent) → `$SUDO_USER` → `logname`
- All `GLib.timeout_add(500, ...)` replaced with `GLib.idle_add(...)` for immediate refresh after `proc.wait()`

- **`--debug` detail added** — all irqbalance, ananicy, and gamemode functions now emit `fn.debug_print()` calls showing: which terminal commands are about to run, real user detected (gamemode), "Waiting for X terminal to close...", "Terminal closed — refreshing labels"; enable/disable service functions also show their `systemctl` command before the terminal opens
- **Performance tab frozen** — `performance.py` and `performance_gui.py` added to frozen files list

### Files Modified

`performance.py` • `data/bin/create-swapfile` • `data/bin/remove-swapfile` • `data/bin/enable-zram` • `data/bin/disable-zram` • `CHANGELOG.md`

---

## 2026.04.30 - Network Tab Overhaul

### What Changed

#### Network tab (`network_gui.py` / `services.py` / `functions.py`)

- **Thunar plugin removed** — `install_arco_thunar_plugin` button, `hbox19` block, `on_click_install_arco_thunar_plugin` callback and broken `fn.install_arco_thunar_plugin` ref all deleted; ATT no longer uses thunar/nemo share plugins
- **nsswitch dropdown** — replaced raw `hosts:` strings with short labels (`Standard (no mdns)`, `With mdns + wins`, etc.); mapping label → hosts: string lives in `choose_nsswitch`; dropdown is now readable
- **`copy_nsswitch` bug fixed** — was writing values without `hosts:` prefix, corrupting the file after first apply; now writes `hosts: <values>` so all five presets save correctly
- **`choose_nsswitch` logging** — added `log_subsection`, `debug_print` (preset name + hosts: line being written), `log_success`, `show_in_app_notification`; unknown preset now logs a `log_warn` instead of silently doing nothing
- **Install/uninstall network discovery** — both rewritten to open alacritty terminal with all commands visible (pacman + systemctl); Popen in daemon thread; ATT stays responsive
- **Uninstall discovery** — no longer attempts package removal (avahi is often a shared dependency); shows note in terminal with manual removal command; wording corrected from "removed" to "disabled"
- **Install/uninstall samba** — both rewritten to match discovery pattern: alacritty terminal, all commands visible, daemon thread, `log_subsection` + notification inside function
- **Create samba user** — rewrote to use bash script in alacritty with `smbpasswd`; terminal now stays open with `read -p`; guards against missing smbpasswd (samba not installed); Popen + daemon thread
- **Shared folder dialog** — `choose_smb_conf` now checks if `~/Shared` exists; if not, shows YES/NO `Gtk.MessageDialog` before creating it; folder creation removed from `copy_samba` and moved to the confirmed response handler

#### Memory

- **Install/uninstall pattern** saved to memory — all future install/uninstall operations must use alacritty terminal with all commands visible, daemon thread, `log_subsection` inside function; transparency is a core project principle
- **`change_distro_label()`** added to do-not-touch memory — display-only function covering all Arch-based distros ATT runs on; never remove entries

### Technical Details

- `nsswitch_options` dict in `choose_nsswitch` maps short label → full `hosts:` string; `copy_nsswitch` receives only the values, prepends `"hosts: "` before writing
- All terminal scripts follow: commands → result echo → `=== Operation Finished ===` → `read -p 'Press Enter to close...'`
- `set_secondary_text` removed (not available in GTK4); dialog text consolidated into `text=` parameter
- `create_samba_user` uses `command -v smbpasswd` check in bash — cleaner than hardcoded path

### Files Modified

`network_gui.py` • `services.py` • `functions.py` • `CHANGELOG.md`

---

## 2026.04.30 - Maintenance Tab Freeze, SDDM Fix Keys Script, Keyring & GPG Fixes

### What Changed

#### Maintenance tab (maintenance.py)

- **`_run_terminal` helper added** — all 9 alacritty `subprocess.call` launches converted to `Popen` + daemon thread; ATT no longer freezes while terminal is open
- **`widget` → `_widget`** — all callback parameters renamed project-wide convention
- **`fn.install_package` removed** from callbacks for tools assumed present (alacritty, hw-probe, reflector)
- **Pacman cache cleanup** — `on_click_clean_cache` now removes leftover `download-*` temp directories before `pacman -Sc`; uses `compgen -G` to check existence first so the "Temp download files removed" line only prints when files actually existed; console `log_info` likewise only fires when temp files are present
- **Keyring local install fixed** — `str(files).strip("[]'")` replaced with proper list filter (`f.endswith(".pkg.tar.zst")`) + `os.path.join`; same fix applied to online download path
- **GPG conf reset cleaned up** — removed noisy content dump and stacked `"=" * 70` separators from both `on_click_fix_pacman_gpg_conf` and `on_click_fix_pacman_gpg_conf_local`; output is now three lines: subsection header, optional backup line, success

#### `functions.py` — `install_local_package`

- `debug_print` on success/failure replaced with `log_success` / `log_error` so result is always visible without `--debug`

#### Fix keys script (`data/bin/fix-pacman-databases-and-keys`)

- Full rewrite with colour helpers (`separator`, `header`, `success`, `warn`, `info`) matching `fix-sddm-config` style
- `pacman -Sy` and keyring download now guarded by `$Online` flag — both steps skipped with a `warn` when offline

#### SDDM page — Fix SDDM config button

- **`on_click_fix_sddm_conf`** added to `sddm.py` with `confirm_dialog` before running the script
- **"Fix SDDM config" button** added to `sddm_gui.py` right-aligned in `hbox_wp_btns` via expanding spacer
- **`data/bin/fix-sddm-config`** rewritten with colour/structure, online/offline fallback, live-user setting patch

### Technical Details

- `_run_terminal(self, cmd, done_msg, start_msg=None)`: `Popen(cmd, shell=True).wait()` in daemon thread; `GLib.idle_add` fires notification on GTK thread when done
- `compgen -G "/var/cache/pacman/pkg/download-*"` used in bash to test glob match without triggering errors on no-match
- `rm -rf` (not `-f`) required because `download-*` entries are directories, not files
- Keyring filter: `[f for f in fn.listdir(pathway) if f.endswith(".pkg.tar.zst")]` — rejects `.pkg.tar.zst.1` partial download fragments

### Files Modified

`maintenance.py` • `maintenance_gui.py` • `sddm.py` • `sddm_gui.py` • `functions.py` • `data/bin/fix-pacman-databases-and-keys` • `data/bin/fix-sddm-config` • `CHANGELOG.md`

---

## 2026.04.30 - Icons Tab, Fastfetch Startup Fix, Codebase Flake8, SDDM Wallpaper

### What Changed

#### Icons tab (icons.py / icons_gui.py)

- **Layout restructured** — all three sub-tabs (Sardi, Surfn, Neo Candy) now share the same consistent layout pattern:
  - Info label row
  - FlowBox of checkboxes (`set_column_spacing(4)`, `set_row_spacing(4)` for tighter grid)
  - Preview image (with lightbox — click to open full-size modal)
  - "Choose icon theme(s)" label + buttons on their own centred row
  - "Choose family / type" label + buttons on their own centred row (where applicable)
  - Centred action buttons row (install)
  - Centred uninstall button on its own separate row
- **Lightbox added** — clicking the preview image in any sub-tab opens a `Gtk.Window` (modal, 960×720) showing the full-size image; Escape key or click on image closes it
- **Dead code removed** — two never-called Surfn callbacks (`on_click_att_surfn_theming_normal_selection`, `on_click_att_surfn_theming_minimal_selection`) deleted; commented-out Normal/Minimal button blocks removed
- **`_widget` convention applied** — all 18 callback `widget` parameters renamed to `_widget` across `icons.py`
- **`log_info` added** — all 6 early-return paths in `icons.py` (empty package list) now log before returning so the user knows why nothing happened
- **All 26 generic widget names renamed** to descriptive names throughout `icons_gui.py` (e.g. `hbox20` → `hbox_sardi_title`, `hbox29` → `hbox_surfn_actions`, `vboxstack4` → `vbox_neocandy_tab`)

#### Fastfetch startup fix (fastfetch.py / fastfetch_gui.py)

- **Initializing flag pattern applied** — `self.ff_initializing = True` set before programmatic `set_active()` calls in the lazy-load function; `on_fast_util_toggled` and `on_fast_lolcat_toggled` return immediately if flag is set
- Startup no longer prints "Fastfetch enabled/disabled" when the page is first loaded; user-triggered toggles still log normally

#### Codebase-wide flake8 fixes (19 files)

- **autopep8** fixed 104 E302 (missing 2 blank lines between functions) and 9 E303 (too many blank lines) violations across 19 Python source files
- **36 F541 bare f-strings** fixed — f-strings with no `{}` placeholders had the `f` prefix stripped
- **`functions.py` `wait_and_notify`** — changed `debug_print(notification)` → `log_success(notification)` so install/remove completion messages are always visible (two-street logging pattern)

#### SDDM Wallpaper Section & Dead Code Removal (earlier in same day)

- **SDDM page — Simplicity theme wallpaper section fully wired:**
  - Browse folder, Load, Stop, folder entry, Apply wallpaper, Restore default — all greyed out when `edu-sddm-simplicity-git` is not installed
  - "Install Simplicity theme" button shown right-aligned when not installed; hidden after install
  - "Remove Simplicity theme" button shown after install; hidden after removal
  - Both buttons use `wait_and_refresh` daemon thread — re-enables or disables all widgets after terminal closes, no reboot required (objective 2: In-App Updating)
  - On remove: flowbox thumbnails cleared, loader cancelled via `_sddm_load_gen` increment, preview reset to `data/wallpaper/wallpaper.jpg` fallback, `login_wallpaper_path` cleared
  - Fallback wallpaper path derived from `__file__` so it resolves correctly in both dev and installed environments
  - `set_paintable(None)` called before `set_filename()` to force GTK4 to clear the cached image
- **`functions_sddm.py` wired correctly:** `setup_sddm_config()` now called only when user clicks "Apply the above mentioned settings" — not at startup (non-invasive, objective 9)
- **`support.py` deleted** — `Support` dialog was never instantiated; all dead references removed from `archlinux-tweak-tool.py`
- **`maintenance.py`** — fixed script path: `arcolinux-fix-pacman-conf` → `att-fix-pacman-conf` at ATT data path
- **`desktopr_gui.py`** — removed dead commented-out arco repo button line
- **`CLAUDE.md` objective 11** — corrected from "Kiro-only" to multi-distro scope: ATT targets all Arch-based systems; `fn.distr` guards are intentional and must not be removed

### Technical Details

- Lightbox uses `Gtk.GestureClick` on the preview frame; opens a `Gtk.Window` with `set_transient_for`, `set_modal(True)`, `Gtk.EventControllerKey` for Escape close
- `frame.set_cursor(Gdk.Cursor.new_from_name("pointer"))` signals the frame is clickable without any extra label
- `ff_initializing` guard: `if getattr(self, 'ff_initializing', False): return` at top of both toggle handlers — safe even if attribute doesn't exist yet
- F541 multi-line string fix: adjacent string literals where `f""` prefix was on a leading empty string were rewritten as plain `set_markup()` calls
- `setup_sddm_config(self, sys.modules["sddm"])` called at top of `on_click_sddm_apply`; passes already-loaded sddm module to avoid circular import
- `sddm.py` / `sddm_gui.py` — autologin switch reads current state from config on startup; Bibata install/remove buttons guard against already-installed/removed state
- `user.py` — `on_click_delete_user` and `on_click_delete_all_user` missing `_widget` parameter fixed
- `maintenance_gui.py` — label renamed to "Get the original ATT /etc/pacman.conf" (naming convention: use ATT not distro names in UI labels)
- **flake8 installed** and `.flake8` confirmed configured (max-line-length = 120)
- **AI tab** confirmed frozen — no errors on Kiro

### Files Modified

`icons.py` • `icons_gui.py` • `fastfetch.py` • `fastfetch_gui.py` • `functions.py` • `sddm.py` • `sddm_gui.py` • `archlinux-tweak-tool.py` • `maintenance.py` • `desktopr_gui.py` • `maintenance_gui.py` • `user.py` • `CLAUDE.md` • `support.py` (deleted) • 14 additional files (autopep8/F541 fixes)

---

## 2026.04.29 - Pacman Page — Full Fix & Freeze

### What Changed

- All pacman repo switches now work correctly — toggling enables/disables repos in `/etc/pacman.conf`
- AUR helper buttons (Install/Remove yay-git, paru-git) update their labels immediately after terminal closes
- Reset pacman ATT and Reset pacman local now refresh all switches after applying
- Blank pacman button restored — was disappearing due to GTK4 double-parent conflict
- Bottom button row (reset/edit) left-aligned to match "Apply custom repo" button above
- `chaotic_aur_repo` constant added to `functions.py`
- `arch_community_testing_repo` reference removed — that repo does not exist
- Pacman files marked frozen: `pacman_gui.py`, `pacman.py`, `pacman_functions.py`

### Technical Details

- Root cause of non-functional switches: `self.opened` always `True` (dead code blocking `toggle_test_repos`); `self.initializing` never cleared (stuck `True` after startup)
- Fix: removed `if self.opened is False:` guards; added `self.initializing = False` at end of `_finish_background_init()`
- Blank pacman disappearance: `blank_pacman` appended to `hboxstack4` first, second append to `hboxstack_blank_pacman` silently failed (widget already had parent), then `hboxstack4.remove()` orphaned it; fixed by only adding to `hboxstack_blank_pacman`
- AUR label refresh: install/remove functions now return `Popen` object; GUI uses `wait_and_refresh` daemon thread that calls `process.wait()` then `GLib.idle_add(refresh_aur_buttons)`
- `init_repos_lazy_load` and `update_repos_switches` both guard `set_active()` calls with `self.initializing = True/finally: False` to suppress spurious toggle callbacks

### Files Modified

`pacman_gui.py` • `pacman.py` • `pacman_functions.py` • `archlinux-tweak-tool.py` • `functions.py` • `CHANGELOG.md`

---

## 2026.04.29 - Project Planning & Developer Objectives

### What Changed

- Developer Objectives expanded — added objectives 15–24 covering GTK4 best practices, consistent naming, no duplicate functions, effective Claude usage, model selection guidance, plan mode policy, project-driven development, lint standards, and automatic changelog maintenance
- Project Plan added to CLAUDE.md — 5-milestone roadmap targeting v1.0 release by 2026-05-29; includes current state snapshot, per-milestone deliverables, packaging checkpoints, and a risk register
- Workflow section added to CLAUDE.md — priority task checklist (must-do before any real work), session start/end checklists, task size guide, and full S/M/L task list with checkboxes

### Technical Details

- Priority tasks identified: install flake8, commit ~100 pending deletions, verify app launches, audit data/kiro/ gaps, tag `pre-m1` baseline
- Task inventory based on live codebase analysis: 723 arco/garuda refs remaining across 14 modules; `themes.py` alone has 547 refs (largest single task) - eos needs to be removed too
- `functions_backup.py` confirmed NOT dead code — imported in `archlinux-tweak-tool.py`; marked for consolidation into `functions.py` instead
- Markdownlint config created: `siblings_only: true` for MD024 (CHANGELOG duplicate headings), MD013 line-length disabled

### S1 — Install flake8 ✓

- `python-flake8` installed via VS Code extension + `sudo pacman -S python-flake8` (v7.3.0)
- `.flake8` config created: `max-line-length = 120`, `functions_backup.py` excluded
- Baseline run: **436 issues** across all modules

| Count | Code | Issue |
| ----- | ---- | ----- |
| 133 | E302 | Missing 2 blank lines between functions |
| 111 | E501 | Lines over 120 chars |
| 40 | F541 | f-strings with no `{}` placeholders |
| 24 | E402 | Module-level imports not at top of file |
| 22 | F401 | Unused imports |
| 22 | E722 | Bare `except:` clauses |
| 17 | W293 | Blank lines containing whitespace |
| 15 | F811 | Duplicate imports |
| 11 | F841 | Variables assigned but never used |
| 6 | F821 | **Undefined name `arepo`** — real bug, needs investigation |
| 6 | E203 | Whitespace before `:` |
| 8 | E702 | Multiple statements on one line |

### F821 Undefined Names — pending fix

`arepo` confirmed removed (no references found — already cleaned up with deleted arco files).
Four remaining F821 bugs to fix next session:

| File | Line | Undefined name | Likely cause |
| ---- | ---- | -------------- | ------------ |
| `icons.py` | 89 | `set_att_checkboxes_theming_surfn_icons_normal` | Function removed or renamed |
| `icons.py` | 96 | `set_att_checkboxes_theming_surfn_icons_minimal` | Function removed or renamed |
| `maintenance_gui.py` | 93 | `fn` | Missing `import functions as fn` |
| `themer.py` | 596 | `readlink` | Should be `os.readlink` |

### Files Modified

`CLAUDE.md` • `CHANGELOG.md` • `.markdownlint.json` • `.flake8`

---

## 2026.04.28 - Startup Performance & Responsiveness Optimization

### What Changed

- Lazy Loading Architecture: All page switch initialization deferred until page access
- Eliminated blocking operations at startup for instant responsiveness
- Privacy page optimization: 110x speedup (2.985s → 0.027s)
- Removed `init_switch_states()` function entirely
- Added comprehensive timing instrumentation with `[RESPONSIVE]` and `[LAZY]` markers
- Optimized `hblock_get_state()`: subprocess call → direct Python file I/O

### Performance Results

```text
                        BEFORE      AFTER       IMPROVEMENT
App responsive:         2.7s    →   1.67s       38% faster
Privacy page delay:     4.47s   →   0.027s      165x faster
Total startup:          2.7s    →   1.72s       36% faster
UI frozen duration:     2.7s    →   0s          Instant
```

### Technical Details

- Privacy callbacks now return early when `initializing=True` to skip expensive `fn.set_hblock()` and similar operations
- All lazy load messages unified under `fn.debug_print()` for consistent behavior
- Each page (Privacy, Themer, Fastfetch, Pacman repos, SDDM) loads switches asynchronously with `GLib.idle_add(PRIORITY_LOW)`
- Debug output respects `--debug` flag for clean console

### Files Modified

`privacy_gui.py` • `privacy.py` • `themer_gui.py` • `fastfetch_gui.py` • `pacman_gui.py` • `sddm_gui.py` • `archlinux-tweak-tool.py` • `functions.py` • `functions_startup.py`

---

## 2026.04.26 - Software Menu Enhancement

### What Changed

- Software menu now has standardized installation flow across all package managers
- Install buttons check if package is already installed before offering installation
- All GUI package managers (Pamac, Octopi, GNOME Software, KDE Discover, Bauh) auto-launch after installation
- TUI tools (Pacseek, Pacui) now have full install+launch logic
- Terminal output includes verbose [INFO] logging: waiting, completion, binary check, launch status
- Labels show `installed` suffix only after successful installation
- New section: Logout Managers (archlinux-logout-gtk4-git, edu-powermenu-git from nemesis_repo)

### Technical Details

- AUR helpers, Flatpak, Snapd, App-manager all updated with verbose logging
- Pre-check for already-installed packages prevents redundant installs
- Missing repository notifications specify repo names (nemesis_repo, chaotic-aur)
- Removal process logs final completion message
- gparted gains install+launch logic with logging

### Files Modified

`software_gui.py` • `archlinux-tweak-tool.py` • `functions.py` • `system_gui.py`

---

## 2026.04.21 - Network & Software Menus Added

### Network Menu

- New sidebar menu with two tabs: Network and Samba
- Network tab: network discovery, nsswitch.conf
- Samba tab: samba server setup, config, user creation, file manager plugins
- Moved out of Services page (which now shows Audio, Bluetooth, Printing only)

### Software Menu

- New sidebar menu with four sections:
  - GUI Package Managers (Pamac, Octopi, GNOME Software, KDE Discover, Bauh)
  - AUR Helpers (yay-git, paru-git, trizen, pikaur-git)
  - Flatpak / Snap / AppImage
  - TUI Package Tools (Pacseek, Pacui)
- Labels show `installed` when binary is detected

### Technical Details

- AUR-only packages (snapd, app-manager) detect available AUR helper; priority order: yay → paru → trizen → pikaur
- Installs via alacritty with in-app notification if no helper found
- GNOME apps require HOME + XDG_RUNTIME_DIR + DBUS_SESSION_BUS_ADDRESS when launched from root
- Flatpak and Snapd terminal output improved with usage hints

### Files Modified

`network_gui.py` • `services_gui.py` • `software_gui.py` • `archlinux-tweak-tool.py`

---

## 2026.04.19 - Kernel Manager Enhancement

### What Changed

- systemd-boot integration: Default boot entry selection
- Dropdown lists available boot entries
- Applying selection sets the default boot entry
- Uses in-app notification for feedback (no dialogs)

### Files Modified

`kernel_gui.py` • `archlinux-tweak-tool.py`

---

## 2026.04.18 - AUR Helper Support

### What Changed

- AUR Helper support on Pacman page
- Builds yay-git or paru-git from AUR using `makepkg` as real user
- Buttons renamed to yay-git / paru-git with fixed logic
- chaotic-aur support added
- `pacman_functions.py` restored

### Files Modified

`pacman_gui.py` • `archlinux-tweak-tool.py`

---

## 2026.04.15 - Maintenance Page Overhaul

### What Changed

- Fixes page renamed to Maintenance
- New features added: Update system, Clean cache, Clear orphans, Get best servers, Set mainstream servers, Install apps, Remove pacman lock
- Terminal windows show closing message
- Layout rearranged for logical order

### Files Modified

`maintenance_gui.py` • `archlinux-tweak-tool.py`

---
