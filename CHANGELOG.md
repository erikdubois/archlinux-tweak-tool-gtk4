# Arch Linux Tweak Tool — Changelog

## 2026.04.28 - Startup Performance & Responsiveness Optimization

### What Changed

- **Lazy Loading Architecture**: All page switch initialization deferred until page access
- **Eliminated blocking operations** at startup for instant responsiveness
- **Privacy page optimization**: 110x speedup (2.985s → 0.027s)
- **Removed** `init_switch_states()` function entirely
- **Added** comprehensive timing instrumentation with `[RESPONSIVE]` and `[LAZY]` markers
- **Optimized** `hblock_get_state()`: subprocess call → direct Python file I/O

### Performance Results

```text
                        BEFORE      AFTER       IMPROVEMENT
App responsive:         2.7s    →   1.67s       38% faster ✓
Privacy page delay:     4.47s   →   0.027s      165x faster ✓
Total startup:          2.7s    →   1.72s       36% faster ✓
UI frozen duration:     2.7s    →   0s          Instant! ✓
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
- **Software menu** now has standardized installation flow across all package managers
- **Install buttons** check if package is already installed before offering installation
- **All GUI package managers** (Pamac, Octopi, GNOME Software, KDE Discover, Bauh) auto-launch after installation
- **TUI tools** (Pacseek, Pacui) now have full install+launch logic
- **Terminal output** includes verbose [INFO] logging: waiting, completion, binary check, launch status
- **Labels** show `installed` suffix only after successful installation
- **New section**: Logout Managers (archlinux-logout-gtk4-git, edu-powermenu-git from nemesis_repo)

### Additional Details
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
- **New sidebar menu** with two tabs: **Network** and **Samba**
- Network tab: network discovery, nsswitch.conf
- Samba tab: samba server setup, config, user creation, file manager plugins
- Moved out of Services page (which now shows Audio, Bluetooth, Printing only)

### Software Menu
- **New sidebar menu** with four sections:
  - GUI Package Managers (Pamac, Octopi, GNOME Software, KDE Discover, Bauh)
  - AUR Helpers (yay-git, paru-git, trizen, pikaur-git)
  - Flatpak / Snap / AppImage
  - TUI Package Tools (Pacseek, Pacui)
- Labels show `installed` when binary is detected

### AUR Package Detection
- AUR-only packages (snapd, app-manager) detect available AUR helper
- Priority order: yay → paru → trizen → pikaur
- Installs via alacritty with in-app notification if no helper found

### Additional Notes
- GNOME apps require HOME + XDG_RUNTIME_DIR + DBUS_SESSION_BUS_ADDRESS when launched from root
- Flatpak and Snapd terminal output improved with usage hints

### Files Modified
`network_gui.py` • `services_gui.py` • `software_gui.py` • `archlinux-tweak-tool.py`

---

## 2026.04.19 - Kernel Manager Enhancement

### What Changed
- **systemd-boot integration**: Default boot entry selection
- Dropdown lists available boot entries
- Applying selection sets the default boot entry
- Uses in-app notification for feedback (no dialogs)

### Files Modified
`kernel_gui.py` • `archlinux-tweak-tool.py`

---

## 2026.04.18 - AUR Helper Support

### What Changed
- **AUR Helper support** on Pacman page
- Builds yay-git or paru-git from AUR using `makepkg` as real user
- Buttons renamed to yay-git / paru-git with fixed logic
- **chaotic-aur support** added
- `pacman_functions.py` restored

### Files Modified
`pacman_gui.py` • `archlinux-tweak-tool.py`

---

## 2026.04.15 - Maintenance Page Overhaul

### What Changed
- **Fixes page renamed to Maintenance**
- **New features added**:
  - Update system
  - Clean cache
  - Clear orphans
  - Get best servers
  - Set mainstream servers
  - Install apps
  - Remove pacman lock
- Terminal windows show closing message
- Layout rearranged for logical order

### Files Modified
`maintenance_gui.py` • `archlinux-tweak-tool.py`

---
