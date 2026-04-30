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

---

## 2026.04.30 - SDDM Wallpaper Section & Dead Code Removal

### What Changed

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

- `setup_sddm_config(self, sys.modules["sddm"])` called at top of `on_click_sddm_apply`; passes already-loaded sddm module to avoid circular import
- Install/remove buttons stored as `self.btn_install_simplicity` / `self.btn_remove_simplicity`; all 5 wallpaper widgets stored as `self.btn_simplicity_*` so post-terminal callbacks can update them from `sddm.py`
- Flowbox clear race condition fixed: `_sddm_load_gen` incremented before removing children so in-flight `load_next` idle callbacks abort immediately
- `on_click_sddm_apply` signature fixed: added `_widget=None` parameter (GTK4 callback requirement)

- **`sddm.py` / `sddm_gui.py`** — autologin switch now reads current state from config on startup (`get_autologin_state()`); switch + 3 dropdowns notify console + in-app on change ("click Apply to save"); `_refresh_cursor_theme_dropdown` fixed (wrong module + wrong attribute); Bibata install/remove buttons guard against already-installed/removed state; `on_click_sddm_enable` missing `_widget` fixed
- **`user.py`** — `on_click_delete_user` and `on_click_delete_all_user` missing `_widget` parameter fixed
- **`maintenance_gui.py`** — label "Get the original ArcoLinux /etc/pacman.conf" renamed to "Get the original ATT /etc/pacman.conf" (naming convention: use ATT not distro names in UI labels)
- **Naming convention established:** replace all distro-specific names in UI labels with "ATT"
- **flake8 installed** and `.flake8` confirmed configured (max-line-length = 120)
- **AI tab** confirmed frozen — no errors on Kiro

### Files Modified

`sddm.py` • `sddm_gui.py` • `archlinux-tweak-tool.py` • `maintenance.py` • `desktopr_gui.py` • `maintenance_gui.py` • `CLAUDE.md` • `support.py` (deleted)

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
