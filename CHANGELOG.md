# Arch Linux Tweak Tool — Changelog

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
