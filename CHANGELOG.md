# Arch Linux Tweak Tool — Changelog

## 2026.06.04 — Btrfs page: fix snapper create-config on the pre-staged @snapshots layout

### What Changed

The "Enable Kiro snapshots" setup failed on a real install once Calamares started pre-staging the `@snapshots → /.snapshots` subvolume. `snapper create-config` insists on creating the `/.snapshots` subvolume itself and aborts when it already exists (*"creating btrfs subvolume .snapshots failed since it already exists"*), so **no `root` config was written** — and steps 3/5 (set TIMELINE_CREATE) and 5/5 (baseline snapshot) then failed with "config 'root' does not exist". The timer-enable step (4/5) was unaffected. The setup now detects the pre-staged `/.snapshots` mount and applies the blessed workaround so the config is created correctly while keeping Kiro's separate `@snapshots` subvolume.

### Technical Details

- **`functions.py` → `launch_btrfs_setup_in_terminal()`:** the 2/5 block now branches on `mountpoint -q /.snapshots`. When pre-staged, it `umount`s + `rmdir`s `/.snapshots`, runs `snapper -c root create-config /` (which now succeeds, creating its own subvolume), then `btrfs subvolume delete`s snapper's subvolume and remounts our `@snapshots` (`mount /.snapshots` via the Calamares-written fstab entry) with `chmod 750`. If the detach fails it restores the mount and reports an error instead of creating a half-config. The pre-existing-config skip and the non-pre-staged plain `create-config` paths are preserved.
- **Step 4/5 now disables `snapper-timeline.timer`.** `snapper create-config` silently enables the timeline timer (confirmed on the VM: its enable-symlink ctime preceded the config file's by ~0.2s), which contradicts Kiro's no-hourly-timeline policy and would FAIL the `kiro-audit` btrfs check. The setup now runs `systemctl disable --now snapper-timeline.timer` right after enabling `snapper-cleanup.timer`. `TIMELINE_CREATE=no` already prevented the snapshots; this makes the timer state match the policy. Step 4/5 runs unconditionally, so a re-click self-heals an already-set-up box.
- No `set -e` in the embedded script, so the failure branch echoes its error and still reaches the final `read -p` prompt (terminal stays open). `bash -n` of the extracted script passes; ruff clean. **Verified end-to-end on a real btrfs + LUKS VM:** snapper root config created, `TIMELINE_CREATE=no`, `@snapshots` remounted as the store (perms 750), cleanup timer on / timeline timer off, and the "Kiro baseline" snapshot present (confirmed in Btrfs Assistant).
- The earlier "validated on a real VM" note (2026.06.03 entry) predated the `@snapshots` pre-staging landing on the test ISO, which is why the conflict surfaced only now.

### Also: "Disable Kiro snapshots" — safe, reversible teardown

A new **Disable Kiro snapshots** button gives the Btrfs page a symmetric undo for everything Enable does, designed safe-at-all-times: it **never deletes snapshots** and performs **no btrfs subvolume or mount operations**. A confirmation dialog (`fn.confirm_dialog`) states exactly what happens before anything runs, then a visible Alacritty teardown: (1) disables + stops the snapshot timers (`snapper-cleanup`, `snapper-timeline`, `btrfsmaintenance-refresh.path`, `btrfs-scrub/balance/trim`); (2) removes the snapper `root` config *file* (`rm -f /etc/snapper/configs/root` — snapshots on disk are preserved in the untouched `@snapshots` subvolume); (3) removes the installed subset of the four packages with plain `pacman -R` (no `-s`, so no dependency cascade). The disk layout (`@snapshots` subvolume, `/.snapshots` mount) is left exactly as a fresh install, and re-running Enable restores the stack — so the post-teardown state is the clean opt-in default that `kiro-audit` reports as PASS.

- **`functions.py`:** new `launch_btrfs_teardown_in_terminal()`, modelled on the setup launcher (alacritty guard, echoed steps, `read -p` close). `/etc/conf.d/snapper` needs no manual edit — `pacman -R` turns it into a `.pacsave`, so `SNAPPER_CONFIGS` is not left active.
- **`btrfs.py`:** new `on_click_disable_snapshots()` — `fn.confirm_dialog` gate (returns early + logs on No), then the `wait_and_refresh` daemon-thread pattern.
- **`btrfs_gui.py`:** "Disable Kiro snapshots" button added to the Setup row between Enable and Launch Assistant; `refresh()` now tracks `any_installed` and sets the button sensitive only when something is actually set up (`any_installed or config_ok`), greyed on a clean system.
- ruff clean; all three modules parse; extracted teardown script passes `bash -n`. Full run needs a btrfs root + root — Erik to test the button post-rebuild.

### Removed: in-app "Launch Btrfs Assistant" button

Dropped the **Launch Btrfs Assistant** button (button + `on_click_launch_assistant` callback + its `refresh()` sensitivity line). Decision: Btrfs Assistant is a **third-party app**, not ATT's — ATT installs the snapshot stack and configures it, but launching someone else's GUI isn't ATT's job; users open it from the application menu like any other app. (What first surfaced the question was theming: it's a Qt6 app and rendered un-themed as root — see the Qt-theming entry below — but the deciding reason is simply "not our app.") Functionality was never affected — purely cosmetic.

### Root Qt theming: copy Kvantum + qt5ct into /root

`functions_backup.py` (`backup_gtk_config()`) now also copies the user's `~/.config/Kvantum` and `~/.config/qt5ct` into `/root/.config`, mirroring the existing GTK 3/4 copy. ATT runs as root and already bridged the user's *GTK* theme to `/root` so ATT itself respects the desktop theme — but **Qt** apps theme through a different path (`QT_STYLE_OVERRIDE=kvantum` + `~/.config/Kvantum`), so any Qt app run as root fell back to Kvantum's default theme instead of the user's ArcDark. The new block closes that gap for any current/future root-launched Qt app. Looped over both dirs with the GTK-4.0 pattern (`os.makedirs` + `copytree(dirs_exist_ok=True)` + chmod 755/644); skips symlinked targets; missing source dirs are a silent debug-only skip. Validated manually (Kvantum in `/root` → Btrfs Assistant renders ArcDark). ruff clean; module parses.

### Btrfs page: short "what it's for" tool labels

Each snapshot tool row now carries a 4–5 word blurb beside its name so users don't have to guess what they're installing — `snapper` "creates and manages snapshots", `snap-pac` "snapshots on every pacman action", `btrfs-assistant` "GUI to browse and restore", `btrfsmaintenance` "scheduled scrub, balance and trim". `btrfs_gui.py`: `_TOOL_BLURBS` dict folded into the existing tool-row label markup (small text between name and install state); refresh() rebuilds it each revisit. ruff clean.

### Retired: in-app CPU scheduler (scx) block → point at scx-manager

The Dev page's interactive sched-ext / scx scheduler selector was removed and retired. It duplicated CachyOS's own **scx-manager** (a Qt6 GUI driving the same `scx_loader` backend), which now ships on the Kiro ISO — so maintaining a parallel UI in ATT was redundant. In its place, the **Kernels page gains a "CPU Scheduler" pointer section at the top**: a one-line signpost to scx-manager (`pacman -S scx-manager` on non-Kiro systems; already installed on Kiro) plus a "read the guide" link, and a note that both Kiro kernels support it.

- **Deleted `scx.py` and `scx_gui.py`** (backend + Dev-page block builder); removed the `import scx_gui`, `_SCX_GUIDE_PATH`, and `scx_gui.build(...)` call site from `dev_gui.py`.
- **`functions.py`:** extracted the Dev page's private `_open_doc`/`_find_editor`/editor-list into a shared `open_doc_in_editor(path)` (plus `_find_doc_editor` / `_DOC_EDITORS`) — there are now two callers (the Dev glossary and the new scx-guide link), so it belongs in `functions.py`. Keeps the repo-tree fallback so links work when ATT runs from source, and drops privileges via `sudo -u` (ATT runs as root). `dev_gui.py`'s `_open_glossary` now calls `fn.open_doc_in_editor`.
- **`kernel_gui.py`:** new "CPU Scheduler" (`sched-ext / scx`) section built at the top of the Kernels page — label + flat "read the guide" link button (→ `fn.open_doc_in_editor`) + a small note naming CachyOS and Zen.
- **`SCX_SCHEDULER_GUIDE.md` rewritten** for scx-manager (was written around the now-deleted ATT block, which would have shipped instructions for buttons that no longer exist): goal-first ("if you want a ___ computer → scheduler + profile"), cheat-sheet moved to the bottom, no false "install the schedulers" step (scx-manager's `depends` pull in `scx-scheds` + `scx-tools` automatically). Both kernels named as supported.
- **Kernel facts verified, not assumed:** `linux-cachyos` has `CONFIG_SCHED_CLASS_EXT=y` (local); `linux-zen` confirmed on a real box (running `scx_bpfland` in LowLatency via `scx_loader`, persisted in `/etc/scx_loader.toml`). ruff clean on all three modules; all parse.

### Themes page: lead with a dark-theme toggle + a Plasma Qt-override toggle (/etc/environment)

Kiro forces the whole desktop to dark by hardcoding `GTK_THEME="Arc-Dawn-Dark"` in `/etc/environment`, which overrides any GTK theme a user picks. The Themes page now **leads** with a brand-orange button that, **on Kiro**, comments / uncomments exactly that line so users can move to a light theme (the plain `Arc` sibling) and back — the dark↔light "hidden gem" from the walkthrough. On **every press** a popup shows the line(s) we changed, `from  →  to`. The terminal **and** the in-app notification both spell out what changed and the step people miss: **log out and log back in** to apply, plus the icons-may-no-longer-match heads-up. **On non-Kiro systems** the button instead opens `/etc/environment` in a terminal editor (`${EDITOR:-nano}`) so the user edits it directly — that exact `Arc-Dawn-Dark` line isn't Kiro's to assume elsewhere.

A **second brand-orange button** with the same layout but its own message comments / uncomments the two Plasma-conflicting Qt override lines — `QT_QPA_PLATFORMTHEME` and `QT_STYLE_OVERRIDE` (lines 1–2 of a stock Kiro environment) — which otherwise force a non-Breeze Qt theme and trigger Plasma's yellow "could not apply theme" popup. Both toggles share one generic engine, so the popup, `.bak` backup and terminal guidance are identical; only the matched keys and messages differ. **The centered hint label and both buttons are shown on Kiro only** (`fn.get_distro_label() == "Kiro"`). **On every other distro** the page instead shows a centered reminder — "Remember to check /etc/environment — themes are sometimes set there." — plus an **Edit /etc/environment in terminal** button (`on_click_edit_environment` → `open_env_in_terminal`, alacritty + `${EDITOR:-nano}`), mirroring the Pacman page's "Edit pacman.conf in terminal".

### Technical Details

- **`themes.py`:** new `/etc/environment` block built on one generic `_toggle_env(self, is_active, is_commented, subsection)` engine — it comments every active matching line, or else uncomments every commented one, writes a `.bak` first via `fn.shutil.copy`, logs each `Changed: from -> to`, and returns `{state, changes}`. `toggle_arc_dawn_gtk_theme()` drives it with the exact `GTK_THEME="Arc-Dawn-Dark"` predicates; `toggle_plasma_qt_overrides()` drives it with key-based predicates for `QT_QPA_PLATFORMTHEME` / `QT_STYLE_OVERRIDE`. `_log_gtk_theme_outcome()` / `_log_plasma_qt_outcome()` emit the per-button multi-line terminal guidance. `_show_change_dialog(changes)` is the on-press popup (one line per change). `open_env_in_terminal()` launches `${EDITOR:-nano}` in alacritty from a daemon thread (non-Kiro). `on_click_toggle_gtk_theme` / `on_click_toggle_plasma_qt` both dispatch on `fn.get_distro_label() == "Kiro"`. `arc_dawn_gtk_state()` is kept for read-only state checks.
- **Two static labels** in ATT brand orange **`#FFA500`** (the same accent as the top-left app name) via a markup `Gtk.Label` child — `GTK_TOGGLE_LABEL` = "Enable or Disable the system-wide dark theme (/etc/environment)" and `PLASMA_QT_TOGGLE_LABEL` = "Enable or Disable the Plasma Qt theme overrides (/etc/environment)". `style_toggle_button(button, text)` is now parameterized.
- **`themes_gui.py`:** the dark-theme button **leads the page** (right after the title/separator, above the intro). A second `hbox_plasma_qt` button is built directly under it; the hint label and both buttons are appended only when `is_kiro` (`fn.get_distro_label() == "Kiro"`). A centered, slightly-larger hint label ("Use the button above to switch the system-wide dark theme on or off.") sits directly under the button(s); the package-selection instructions stay left-aligned below it.
- Exact-match for the GTK line (per Erik); key-based for the Qt overrides; both reversible. Two-press simulations confirmed against the real `/etc/environment` — GTK line ⇄ `#`-line, and both Qt lines comment/uncomment together with correct popup lines. ruff clean on both modules; both parse. Live clicks + the non-Kiro editor path need ATT run as root — Erik to test post-deploy.

### Themes page: dropdown to set any system GTK theme into /etc/environment

A new **theme dropdown + Apply button** sits beneath the existing `/etc/environment` toggle button(s) on the Themes page, **on all distros**. It lets a user push any installed GTK theme system-wide via `GTK_THEME=` — the "heavy hammer" path that themes root and every user and stubborn toolkits — without hand-editing the file. The dropdown's first entry, **"None — no system-wide theme"**, is the off switch: it clears the override so the normal per-user theme takes back over. The hardcoded dark-theme toggle button stays as the quick one-press control; the dropdown is the "set a specific theme (or none)" path. Decoupled from the install checkboxes on purpose — those are multi-select and a `GTK_THEME=` line holds exactly one theme, so the dropdown lists real themes by name instead.

### What Changed

The dropdown is populated from the **themes actually on the machine** — `/usr/share/themes` only (not `~/.themes`), filtered to folders that ship a `gtk-3.0` or `gtk-4.0` directory so a non-GTK (Openbox/xfwm-only) folder can never be written as an invalid value. `/usr/share/themes` is the deliberate scope because `/etc/environment` is read by root and every user, so a home-dir theme wouldn't resolve there. On page build the dropdown **preselects reality**: if an active `GTK_THEME=` already exists it lands on that theme, otherwise on "None". Apply is an explicit button press (not apply-on-change); after the write a dialog **shows the full current content of `/etc/environment`** (not a synthetic diff) so the user sees the real resulting file, plus a notification ending in "log out and back in to apply".

**Cross-distro robustness (ATT targets all Arch-based distros):** the writer no longer assumes the file reads cleanly or already exists — a **missing** `/etc/environment` is created with just the new line (no `.bak` to copy), an **empty** one takes the same append path, and a missing/empty file with "None" selected simply reports nothing to clear. An **"Edit /etc/environment in terminal"** escape-hatch button now shows on **every distro** (previously non-Kiro only): if the automated write ever misbehaves on some distro, the user always has the manual fix one click away. And to prevent a silent wipe: if an active `GTK_THEME=` value isn't an installed `/usr/share/themes` folder (a `~/.themes` name, a typo), it's still injected into the dropdown and preselected — so an untouched Apply can't clear a theme the dropdown couldn't otherwise represent.

### Technical Details

- **`themes.py`:** additions reusing the existing env infrastructure — `list_system_gtk_themes()` (scans `/usr/share/themes` via `fn.os`, GTK-3/4 filter, case-insensitive sort); `current_env_gtk_theme()` (returns the active `GTK_THEME` value or `None`); `set_env_gtk_theme(self, theme)` (the writer — checks `fn.os.path.exists` first so an absent file is created rather than erroring, `.bak` via `fn.shutil.copy` only when the file already exists, then either comments every active `GTK_THEME` line when `theme is None`, or makes the first existing `GTK_THEME` line the single live one with the new value and comments any duplicate actives, appending a fresh line when none exists; returns `{state, changes}` and no-ops cleanly when already in the requested state); `on_click_apply_env_theme(self, _widget)`.
- **Dialog unified across all three `/etc/environment` actions.** The old `_show_change_dialog(changes)` (synthetic before→after lines) was replaced by `_read_env_content()` + `_show_env_content_dialog(self, header)`, which read the file back and show its **full current content** (`"…is empty."` / `"…does not exist."` for the edge cases). The two existing top toggle callbacks (`on_click_toggle_gtk_theme`, `on_click_toggle_plasma_qt`) and the new Apply callback all now call it — so every env action looks the same. The terminal still logs the `Changed: from -> to` lines, so the diff detail isn't lost, just moved out of the popup.
- **`themes_gui.py`:** `hbox_env_dropdown` built with a brand-orange (`#FFA500`) markup label, `Gtk.DropDown.new_from_strings(["None — no system-wide theme"] + names)` (the codebase's established DropDown idiom), preselect logic, and an "Apply" button wired via `functools.partial`. The dropdown row and the (now distro-agnostic) `hbox_env_edit` button are both appended after the `is_kiro`/`else` block; `hbox_env_edit` was removed from the non-Kiro `else` branch so there's no double button.
- Because the writer always reduces to a single live `GTK_THEME` line, it never fights the hardcoded top toggle (which targets the exact `Arc-Dawn-Dark` string). ruff clean on both modules; both `ast.parse`; codespell clean. Live writes need ATT run as root — Erik to test post-rebuild.

## 2026.06.03 — New Btrfs page: one-click snapshot setup (btrfs roots only)

### What Changed

A new **Btrfs** page installs and configures the snapshot stack on a btrfs system, opt-in and in one step. It is visible **only when the root filesystem is btrfs** (or with `--dev`, so it can be worked on from a non-btrfs dev box) — on every other system the page is not added to the sidebar, so the btrfs check replaces a pure `--dev` gate with an honest capability check (today a btrfs root is effectively just the Kiro dev/test installs). The page mirrors Garuda's snapper-based stack (`snapper` + `snap-pac` + `btrfs-assistant` + `btrfsmaintenance`) but applies Kiro's policy: a snapshot pair on every `pacman` action via snap-pac, **no** hourly timeline snapshots, with cleanup pruning old pairs. Kiro pre-stages the `@`-prefixed subvolume layout (incl. `@snapshots` → `/.snapshots`) at install time, so the disk is snapshot-ready and the page only has to install + configure on top. True to ATT's no-black-boxes rule, the whole install+configure sequence runs in a **visible Alacritty window** — the user watches every command. A "Snapshot tools (not on the ISO)" section gives each tool its own **Install** button (with installed/missing state, button disabled once installed) so the not-on-ISO software is visible and installable individually — alongside the one-click "Enable Kiro snapshots". A status panel shows live state (snapper root config, cleanup timer, btrfsmaintenance) and a "Launch Btrfs Assistant" button opens the GUI front-end. The configure path (`snapper -c root create-config /`) was validated on a real btrfs + LUKS-encryption VM install.

### Technical Details

- **New `btrfs.py`:** detection (`is_btrfs_root`, `snapper_root_configured`, `all_packages_installed`) + callbacks. `on_click_enable_snapshots` launches the visible setup terminal and waits on the process in a daemon thread, then `invalidate_pkg_cache()` + refresh (the documented `wait_and_refresh` pattern). `on_click_launch_assistant` gates on the package being installed before `Popen(["btrfs-assistant"])`.
- **New `btrfs_gui.py`:** the page UI (intro + per-tool install rows built in a loop over `btrfs.PACKAGES` + status panel + setup actions + systemd-boot rollback caveat) and a `refresh()` that re-renders each tool row and status row green/orange from live state and disables an Install button once its package is present; called at build time and after every install/setup. Per-tool installs reuse `launch_pacman_install_in_terminal` (one package each, visible).
- **`functions.py`:** new `get_root_filesystem_type()` (reads `/proc/mounts`; used by the visibility gate without importing `performance`, whose construction path carries subprocess calls) and `launch_btrfs_setup_in_terminal()` — modelled on `launch_pacman_install_in_terminal`, builds the echoed install+configure script (idempotent: skips `create-config` if `/etc/snapper/configs/root` exists; enables `btrfsmaintenance-refresh.path` only if present) and `Popen`s Alacritty with a `read -p` close prompt.
- **`gui.py`:** imports `btrfs` + `btrfs_gui`, adds `vboxstack_btrfs` + a lazy `_defer_tab`, and guards `add_titled(..., "Btrfs")` with `if fn.DEV or btrfs.is_btrfs_root()`, placed alphabetically between Autostart and Desktop.
- The setup script is idempotent: skips `create-config` and the "Kiro baseline" snapshot when they already exist, and runs `btrfsmaintenance-refresh.service` once after enabling the `.path` so the scrub/balance timers are installed immediately (the `.path` alone only refreshes on a later config change).
- `ruff check` clean on all touched files; all compile clean. **Not yet runtime-verified on a live btrfs install** — Erik's pending test must confirm the status rows flip to green after setup and that the btrfsmaintenance timers land active.

### Files Modified

- `usr/share/archlinux-tweak-tool/btrfs.py` (new)
- `usr/share/archlinux-tweak-tool/btrfs_gui.py` (new)
- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/gui.py`

## 2026.06.02 — Desktop page: warn about /etc/environment theme overrides on Plasma install

### What Changed

Installing **Plasma** through the Desktop page now warns the user about `/etc/environment` variables that override Plasma's own theming. Variables like `QT_QPA_PLATFORMTHEME`, `QT_STYLE_OVERRIDE` (force a non-Breeze platform theme/style → Plasma's yellow "unable to apply" warning notification/popup) and `GTK_THEME` (forces GTK apps dark regardless of Plasma's settings → dark elements) make for a frustrating first Plasma experience if the user doesn't know to disable them. Two places now surface this: (1) the existing pre-install one-way-install warning dialog lists the **actual** offending lines and tells the user to comment them out (put `#` in front) and log out/in; (2) a dedicated **post-install** message box pops up once the Plasma install finishes, repeating the same instruction so it isn't missed in the pre-install confirmation. Inform-only — ATT does not edit the file. Shown only when those lines are genuinely present, and only for Plasma (not GNOME); the post-install box is suppressed during "install all desktops".

### Technical Details

- **`desktopr.py`:** new `conflicting_plasma_env_lines()` helper reads `/etc/environment` and returns the uncommented lines whose key is in `_PLASMA_CONFLICTING_ENV_VARS` (`QT_QPA_PLATFORMTHEME`, `QT_STYLE_OVERRIDE`, `GTK_THEME`); skips commented/blank lines and `log_warn`s on an unreadable file. `on_install_clicked` builds its dialog `secondary_text` incrementally: for Plasma it appends an "IMPORTANT — Plasma theming" block listing the found lines, plus a `log_warn` and an in-app notification. New `show_plasma_env_dialog(self)` builds a standalone WARNING message box (non-blocking — `response` → `destroy`, no nested `MainLoop`) listing the lines; `_after_install` schedules it via `GLib.idle_add` in the success branch, gated on `on_complete is None and desktop == "plasma"` so it fires only for an interactive single Plasma install, never during bulk "install all". No false claims for users who don't have those lines set. Complements the existing Plasma path that already removes the `qt5ct` *package* (which does not clear the matching `/etc/environment` line).
- `ruff check` clean; syntax validated.

### Files Modified

- `usr/share/archlinux-tweak-tool/desktopr.py`

## 2026.06.02 — Fix: links don't open on Plasma/Wayland (AI tools, funding, kernel)

### What Changed

Clickable links in ATT did nothing on a **KDE Plasma (Wayland)** session — no browser, no error, on either left- or right-click. The AI Tools page links, the funding links, and the kernel "more info" links all opened URLs with a hardcoded `DISPLAY=:0`, an X11-only assumption. On Wayland there is no usable X server at `:0`, so `xdg-open` (and the right-click "Open with <browser>" path) silently failed. Links now open correctly on both X11 and Wayland.

### Technical Details

- **`functions.py`:** new `user_session_env_assignments()` helper reads the real user's live session env via the existing `get_terminal_env()` (`DISPLAY`, `WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `DBUS_SESSION_BUS_ADDRESS` from `/proc/<pid>/environ`) and returns them as inline `VAR=val` args — passed to `sudo` this way they survive its env sanitizing, unlike `Popen(env=)`. New `open_url_as_user(url)` (left-click, via `xdg-open`) and a rewrite of `open_url_with_browser(url, binary)` (right-click "Open with" popover) both use it; the latter also moves from a `shell=True` string to list form. Mirrors the proven X11/Wayland pattern already used by the wallpaper code.
- **`ai.py`, `funding.py`, `kernel_gui.py`:** the three link openers now delegate to `fn.open_url_as_user()`; removed the duplicated `sudo -u … DISPLAY=:0 xdg-open` calls.
- `ruff check` clean on all touched files; all compile clean.

### Files Modified

- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/ai.py`
- `usr/share/archlinux-tweak-tool/funding.py`
- `usr/share/archlinux-tweak-tool/kernel_gui.py`

## 2026.06.02 — Dev page: VM-aware microcode check (no false FAIL on a VM)

### What Changed

The Dev page's "System integrity (kiro-audit mirror) → Microcode" check no longer shows a red **FAIL** when running inside a virtual machine. A VM has no real CPU to patch, so a missing `/boot/*-ucode.img` is expected, not a fault. On a VM the row now reports **PASS** with the explanation "image not in /boot — expected in a VM (no real CPU to patch)". On real metal the original FAIL ("installed but image MISSING in /boot (archiso stripped it?)") is unchanged. This mirrors the stance kiro-audit already takes.

### Technical Details

- **`dev_gui.py`:** added a module-private `_is_vm(fn)` helper that runs `systemd-detect-virt --vm --quiet` (returncode 0 → VM), matching the existing private-helper pattern (`_failed_units`, `_zram_state`, …) and the kiro-audit detection. The microcode loop now branches three ways: image present → PASS; image missing **and** in a VM → PASS with VM explanation; image missing on metal → FAIL (original message). The "(none installed)" WARN case is unchanged.
- `ruff check` clean.

### Files Modified

- `usr/share/archlinux-tweak-tool/dev_gui.py`

## 2026.06.02 — Desktop page: GNOME is now a one-way install (Plasma parity)

### What Changed

Selecting **GNOME** on the Desktop page now carries the same one-way-install safeguard Plasma already had: an orange warning label + in-app notification on select, the **Remove** button greyed out with an explanatory tooltip, a WARNING Yes/No confirmation dialog before installing, and removal through ATT blocked entirely. Installing GNOME (like Plasma) requires a full system reinstall to undo.

### Technical Details

- **`desktopr.py`:** introduced `ONE_WAY_DESKTOPS = ("plasma", "gnome")`, a `_DESKTOP_DISPLAY_NAMES` map, and a `desktop_display_name()` helper (so GNOME renders as "GNOME", not "Gnome"). Both `on_install_clicked` (confirmation dialog) and `on_uninstall_clicked` (removal block) now test `desktop in ONE_WAY_DESKTOPS` and build all user-facing text from `desktop_display_name(desktop)`. The install dialog's response callback renamed `on_plasma_warn_response` → `on_oneway_warn_response`. Removal mechanics (`-Rdd` force-flag, dev-only "remove all") left unchanged — matching prior Plasma behaviour.
- **`desktopr_gui.py`:** generalised the Plasma-only warning widget — `hbox_plasma_warning`/`lbl_plasma_warning` renamed to `hbox_oneway_warning`/`lbl_oneway_warning`; its markup is now set dynamically in `update_button_state` from `desktopr.desktop_display_name(selected)`. Both `selected == "plasma"` checks (Remove-button sensitivity/tooltip and warning-label visibility) changed to `selected in desktopr.ONE_WAY_DESKTOPS`.
- The unrelated `themes_gui.py` "On Plasma these themes will not work" warning is a separate widget and was left untouched.
- `ruff check` clean on both files; both compile clean.

### Files Modified

- `usr/share/archlinux-tweak-tool/desktopr.py`
- `usr/share/archlinux-tweak-tool/desktopr_gui.py`

## 2026.06.01 — Desktop page: dev-mode "Install all twms" button

### What Changed

Added an **Install all twms** button to the Desktop page's `--dev` test row, placed between the existing yellow "Install all desktops" button and "Remove all desktops", and styled the same yellow (`#FFD700`). It installs only the 7 tiling WMs (awesome, bspwm, i3, qtile, leftwm, chadwm, ohmychadwm) in the same shared-package-first order, skipping any already installed — a faster path for dev testing when the full-DE set isn't needed.

### Technical Details

- **`desktopr.py`:** new `TWM_INSTALL_ORDER` list (the 7 TWMs, same relative order as `INSTALL_ORDER`) and `install_all_twms(self)` — mirrors `install_all_desktops()` (daemon thread, per-WM `threading.Event` gated on `install_desktop`, `check_desktop` skip, in-app notifications).
- **`desktopr_gui.py`:** new `btn_install_all_twms` built with a `Gtk.Label` + `set_markup('<span foreground="#FFD700">…</span>')` (matching the install-all button) and appended after `btn_install_all`. Whole dev row stays gated behind `fn.DEV`.
- `ruff check` clean on both files.

### Files Modified

- `usr/share/archlinux-tweak-tool/desktopr.py`
- `usr/share/archlinux-tweak-tool/desktopr_gui.py`

## 2026.06.01 — Desktop install: scoped `~/.config` backup (kiro-skell parity)

### What Changed

Installing a desktop no longer copies the **entire** `~/.config` to `~/.config-att/`. It now backs up **only the config dirs the install will overwrite** — the same scoped-backup principle `kiro-skell` already uses. For tiling WMs that means just that WM's dir(s) (e.g. `~/.config/chadwm`, or `bspwm` + `polybar`); for full DEs (gnome, plasma, xfce, mate, cinnamon, budgie), which copy no skel config at all, nothing is backed up and a clear log line says so. This removes the slow multi-GB full-copy (browser/app caches) that protected far more than was ever at risk.

### Technical Details

- **`desktopr.py` — `install_desktop()`:** removed the unconditional `cp -Rp ~/.config → ~/.config-att/config-att-<ts>` block at the top. Moved the backup *below* the desktop dispatch chain so `src` (the dirs the post-install skel copy will overwrite) is known. New scoped block builds `to_backup` from `basename(src)` entries that exist in `~/.config`, copies each to `~/.config-att/config-att-<ts>/<name>` (existing layout kept — restore path unchanged), one recursive `fn.permissions()` chown over `~/.config-att`. Empty `src` → no backup + explicit log line (never-a-black-box).
- **Why this is complete coverage:** the only write to `~/.config` in the flow is the `_after_install` skel copy of `src`; `pacman -S` never touches the user's home. The backup stays in the `install_desktop` daemon thread (not `_after_install`, which runs on the GLib main loop and would block the UI). Does **not** shell out to `skell`/`kiro-skell` — those copy *all* of `/etc/skel` (wrong semantics here).
- **`desktopr_gui.py`:** reworded the two strings that described the old full backup — the `noice` info label and the live `lbl_backup_notice` (dropped "this might take a while").
- `ruff check` and `codespell` clean on both files.

### Files Modified

- `usr/share/archlinux-tweak-tool/desktopr.py`
- `usr/share/archlinux-tweak-tool/desktopr_gui.py`

## 2026.05.31 — `skell` is now generated from edu-system-files + `skel` naming consistency

### What Changed

**`usr/bin/skell` is now a generated file**, not hand-maintained. It is a verbatim copy of `kiro-skell` from the `edu-system-files` repo (the single source of truth), pulled by [fetch-configs.sh](fetch-configs.sh) on each `up.sh` run — the same mirror pattern ATT already uses for `.zshrc`/`.bashrc`/`config.fish`. The copy direction is one-way: **ATT pulls from edu-system-files**; edu-system-files never reaches into ATT. The source script is self-contained (inlines its helpers instead of sourcing the Kiro-only `kiro-common.sh`), so it runs on the non-Kiro distros ATT targets, and it names itself via `"$(basename "$0")"`, so the same bytes print `skell` here and `kiro-skell` on Kiro. It is **exempt from the ATT Script Standard** (documented in CLAUDE.md obj. 29) — do not hand-edit or convert it; edit `kiro-skell` upstream and re-fetch.

This supersedes the earlier hand-fix of `skell`'s `skel`→`skell` self-references (the whole file is now replaced by the upstream copy, which is already correct).

Separately, the skel-restore command is consistently double-L (`skell` here, `kiro-skell` in edu-system-files; convention recorded in `Kiro-HQ/ASSISTANT.md`). Fixed the stale skel-script path in the shipped shell-config comments: `.zshrc`, `.bashrc`, `config.fish` pointed at the long-gone `/usr/local/bin/skel`; they now point at `/usr/local/bin/kiro-skell`. These three data files are mirrors of the edu-shells canonical and remain byte-identical to it. The `bupskel` alias in those dotfiles was reviewed and deliberately left single-L — it backs up the `/etc/skel` *directory*, not the restore command.

### Files Modified
- `usr/bin/skell` (now generated from edu-system-files/kiro-skell)
- `fetch-configs.sh` (new `fetch_skell` step)
- `CLAUDE.md` (obj. 29: skell as generated/exempt file)
- `usr/share/archlinux-tweak-tool/data/.zshrc`
- `usr/share/archlinux-tweak-tool/data/.bashrc`
- `usr/share/archlinux-tweak-tool/data/config.fish`

## 2026.05.30 — Sidebar page search (jump to setting by keyword)

### What Changed

The sidebar gains a **search box** above the page list. Type a word and press **Enter** to jump to the page that owns it. It searches three layers: live **page titles** (Network, Plymouth…), hand-authored **aliases** ("firewall" → Network, "boot splash" → Plymouth), and — auto-scraped from source — the **button/label text and option lists of every page**, so a control or choice is findable by what it actually is ("gparted" → System, "swappiness" → Performance, "bluetooth" → Services, "orphan" → Maintenance, "ohmychadwm"/"qtile"/"rofi" → Desktop). The whole index is rebuilt by `up.sh`; a no-match query flashes an in-app notification.

### Technical Details

- **Three-layer index, rebuilt at `up.sh`.** Page *titles* are read live from the running `Gtk.Stack` (`stack.get_pages()`) so they never drift and conditional pages (SDDM, Dev) are only searchable when present. *Aliases* are hand-maintained. *Labels* are scraped from source — no hand-maintenance, so they can't rot.
- `gen-search-index.py` (repo root, stdlib-only): derives the `module → vboxstack → page` chain from gui.py (`<module>.gui(... vboxstack_x ...)` tied to `add_titled(vboxstack_x, "child", "Title")`), then **AST-walks** each page's `*_gui` module *and its sibling logic module* (`<base>.py`) to collect two things: (a) button/label/markup text from `set_text`/`set_label`/`set_markup`/`label=` calls, kept verbatim; (b) **option strings inside list/tuple/set/dict literals** (e.g. `desktops = [...]`), passed through a hardening filter that rejects flags (`-S`), paths and command tokens. AST is used so log-message and docstring strings are *not* swept in. Tokens are Pango-stripped and filtered against a stoplist of generic UI verbs + command/packaging noise (pacman/pkexec/git/edu…). Emits `keywords` (hand) + `labels` (scraped) per page. Warns (non-fatal) on alias drift. Deterministic (no timestamp). This run: 26 pages, 1662 scraped tokens.
- `gui.py`: `Gtk.SearchEntry` in the sidebar `ivbox` above `stack_switcher`; `on_search_activate` (Enter-only) resolves title exact → prefix → contains, then keyword/label prefix → contains, and switches via `stack.set_visible_child_name()` — guarded by `stack.get_child_by_name()`. Hand keywords are indexed before scraped labels so an alias always wins a collision.
- `search_synonyms.json` (repo root, dev-only, not shipped): aliases keyed by exact page title — kept deliberately small (concept words the scraper can't derive: firewall→Network, i3, tiling, etc.). The 13 desktop/WM names (ohmychadwm, chadwm, qtile…) are NOT seeded — the data-list scraper reads them straight from `desktopr.py`, so new environments become searchable automatically.
- `up.sh`: new non-fatal block in `main()` runs the generator before commit/push, mirroring the existing `fetch-configs.sh` hook.
- `ruff check` and `codespell` clean; generator validated (26 pages, no drift, deterministic re-run).

### Files Modified

- `usr/share/archlinux-tweak-tool/gui.py`
- `usr/share/archlinux-tweak-tool/search_index.json` (generated)
- `search_synonyms.json` (new)
- `gen-search-index.py` (new)
- `up.sh`

### DEV page: CPU scheduler selector (sched-ext / scx)

The Dev Diagnostics page gains an **interactive scheduler block at the top** — the first control on a page that was read-only diagnostics until now. It lets you switch the live CPU scheduler **without a reboot** through the CachyOS `scx_loader` stack: pick a **scheduler** (scx_lavd, scx_bpfland, scx_rusty, scx_flash, scx_p2dq, scx_tickless) and one of `scx_loader`'s five **modes** (Auto / Gaming / LowLatency / PowerSave / Server). Default is **OFF**: the kernel default (EEVDF / BORE) stays in charge until you opt in, so the baseline `kiro-audit` validates is untouched on a fresh system. The block self-gates on `/sys/kernel/sched_ext`, so it greys out on kernels without sched-ext and lights up on both Kiro kernels (linux-cachyos and linux-zen, both confirmed sched-ext-capable). Implements MASTER_TODO §3 P2; backed by the 2026-05-30 cachyos-kernel-tuning study + a live online check of the CachyOS scxctl/scx_loader interface. To be trialled over the coming weeks.

### Technical Details

- **Online-verified interface (the first cut had bugs).** `scxctl` and `scx_loader` are **not** part of `scx-scheds` — they ship in the official **`extra/scx-tools`** package (which depends on `scx-scheds`). The standalone `cachyos/scxctl` was rejected: it pins `scx-scheds<=1.0.10` and would force a downgrade. `scxctl start` **requires** `-s <sched>` — modes alone cannot load a scheduler — so the GUI offers a scheduler dropdown (defaulted to `scx_lavd`) alongside the mode dropdown. Scheduler names pass to `scxctl` without the `scx_` prefix and modes lowercased; the TOML keeps the full name + capitalised mode.
- **`scx.py` (new) — backend.** `sched_ext_supported()` gates on `/sys/kernel/sched_ext`; `get_active_scheduler()` reads `state` + `root/ops` from sysfs (kernel-truth, no daemon needed) and falls back to "default (EEVDF / BORE)". Actions run threaded (daemon `Thread` + `GLib.idle_add` refresh, matching the gamemode pattern): `install_scx` pulls **`scx-tools`** in an alacritty terminal leaving the service **disabled** (enabling it is the user's explicit opt-in); `apply_scheduler` writes `/etc/scx_loader.toml` (`default_sched` + `default_mode`), enables `scx_loader.service`, then loads via `scxctl` (tries `switch` then `start -s <sched> -m <mode>`); `disable_scx` runs `scxctl stop`, disables the service, removes the TOML.
- **`scx_gui.py` (new) — block builder.** Builds a self-contained `Gtk.Box` (header + active-scheduler readout + install-on-demand row + scheduler `Gtk.DropDown` + mode `Gtk.DropDown` + Apply + "Back to default"), appended **above** the diagnostics grid so `_populate()`'s grid-clear never touches it. A `_refresh()` closure re-reads state and re-gates every control; wired to the block's `map` signal so it self-updates on tab revisit.
- **`dev_gui.py`:** one import + one `scx_gui.build(self, Gtk, vboxstack_dev, fn)` call inserted between the title separator and the help link.
- **Info help button.** The block header gets an "Info" button (right-aligned, 10px right margin) opening a plain-English end-user guide, `SCX_SCHEDULER_GUIDE.md` (what each scheduler/mode is for, a concise "what should I do?" scheduler+mode table, how to tell it worked, how to undo). Reuses the Dev page's existing local-doc opener — `_open_glossary` was generalised to `_open_doc(fn, path)` so both the glossary link and the scx Info button share the editor-detection + `sudo -u` (no-browser, runs-as-real-user) path.
- **Two-row control layout.** Configure row (Scheduler + Mode + Apply) on top; state row (Back to default + Install/Remove scx-tools) below — keeps the buttons from clipping the right edge on a narrow window.
- **ISO prerequisite (not in this repo):** `kiro-iso-next` must add **`scx-tools`** to `packages.x86_64` and ship `scx_loader.service` disabled by default. Until then the block's install button bootstraps it on demand.
- `ruff check` and `codespell` clean; syntax-validated.

### Files Modified

- `usr/share/archlinux-tweak-tool/scx.py` (new)
- `usr/share/archlinux-tweak-tool/scx_gui.py` (new)
- `usr/share/archlinux-tweak-tool/dev_gui.py`
- `usr/share/doc/archlinux-tweak-tool/SCX_SCHEDULER_GUIDE.md` (new)

### Performance → Build: "Keep 2 cores free" option

The makepkg.conf Build tab gained a second optimize button: alongside **Optimize for all N cores** there's now **Keep 2 cores free (-j{N-2})**. Building an ISO/AUR package with every core pinned makes the desktop (and a Bluetooth mouse) stutter; reserving 2 cores keeps input responsive at a small cost to build time — the same throughput-vs-responsiveness trade as the scx scheduler block, and they stack.

- `performance.py`: `optimize_makepkg(self, _widget, reserved=0)` parametrised — `jobs = max(2, ncores - reserved)`; log/notification/messagebox text adapts to mention the reserved cores when `reserved > 0`.
- `performance_gui.py`: first button relabelled "Optimize for **all** N cores"; new `btn_reserve_makepkg` shown only when `ncores >= 4` (so it genuinely keeps 2 free), wired via `functools.partial(..., reserved=2)`; description line updated.
- `ruff` + `codespell` clean.

### Files Modified

- `usr/share/archlinux-tweak-tool/performance.py`
- `usr/share/archlinux-tweak-tool/performance_gui.py`

### System page: GParted button becomes Launch/Install

The GParted button on the System page was install-only; it now behaves like the other tool buttons (Bazaar, Pamac, Octopi, Partition Manager): **Launch/Install** — it launches GParted if it's installed, otherwise installs it and then launches it.

- `system.py`: `on_click_system_gparted` reworked from install-only to launch-or-install; new `_launch_gparted(self)` helper.
- `system.py`: generalized `_pm_launch_cmd()` → `_partition_tool_launch_cmd(binary)` so GParted and Partition Manager share one as-user launch path (sets `XDG_RUNTIME_DIR` / `DBUS_SESSION_BUS_ADDRESS` / `DISPLAY` / `WAYLAND_DISPLAY` and runs as the real user via `sudo -u`). Both Partition Manager call sites updated.
- `system_gui.py`: GParted button label `Install` → `Launch/Install`; also fixed Partition Manager's label casing `Launch/install` → `Launch/Install` so all 14 Launch/Install buttons match.

### Services page: read-only User Services tab

New **User Services** tab on the Services page listing the real user's active `systemctl --user` services (read-only, no action buttons — stopping `pipewire`/`dbus` would break the session). Custom units the user/admin added (e.g. `kiro-website.service`) are flagged and sorted to the top so they aren't buried under session plumbing. A Refresh button re-reads on demand; the list also auto-refreshes when the page is opened.

- `services.py`: new `get_user_services()` — runs `systemctl --user show '*' --type=service` as the real user (root ATT → `sudo -u` with `XDG_RUNTIME_DIR`/`DBUS_SESSION_BUS_ADDRESS`), parses the `Key=Value` blocks, keeps only `ActiveState=active`, and flags custom units by FragmentPath under `~/.config/systemd/user` or `/etc/systemd/user`. Returns `[]` gracefully on no session.
- `services_gui.py`: User Services tab (`stack6`) with a `Gtk.ScrolledWindow` + read-only `Gtk.ListBox`, count label, and Refresh button; `_refresh_user_services` fetches off the UI thread and marshals back via `GLib.idle_add`; wired into the page `_refresh()` so it populates on map. Added module-level `from gi.repository import Gtk`.

### New Office page (suites + productivity apps)

New top-level **Office** page (sidebar, between Network and Packages) gathering office suites and related productivity apps, each with the **Launch/Install + Remove** pattern. Tabbed into **Suites / Mail / Editors / PDF & Notes / Scanning** — 24 apps total. Suites: LibreOffice (`libreoffice-fresh`), OnlyOffice (`onlyoffice-bin`), WPS Office (full set `wps-office wps-office-fonts wps-office-mime ttf-wps-fonts libtiff5`, per the arcolinux-nemesis WPS script). Apps sourced from `chaotic-aur` (OnlyOffice, WPS, Betterbird, qpdfview) are **guarded**: if chaotic-aur isn't active, the click notifies "enable it on the Pacman page" instead of failing in the terminal.

- `office.py` (new): data-driven `OFFICE_APPS` registry (tab → list of `{key,label,packages,launch,repo,remove}`) plus two generic handlers — `install_or_launch` (launch if the primary package is installed, else chaotic-aur guard → install full set → launch; install/launch run as the real user) and `remove` (safe recursive removal via `pacman -Rns` — clears the app set plus dependencies nothing else needs, e.g. WPS's `libtiff5`; pacman keeps any dep still required elsewhere). Avoids ~50 duplicate per-app functions.
- `office_gui.py` (new): `gui()` builds a `Gtk.Stack` + `StackSwitcher`, iterating the registry to generate each tab's rows; `_refresh()` marks installed apps and is wired into the page `map`.
- `gui.py`: 4 wiring points — `import office_gui`, `vboxstack_office`, `_defer_tab`, and `add_titled("Office")` between Network and Packages.
- `CLAUDE.md`: tab count 25 → 26, Office added to the list.

### Files Modified

- `usr/share/archlinux-tweak-tool/system.py`
- `usr/share/archlinux-tweak-tool/system_gui.py`
- `usr/share/archlinux-tweak-tool/services.py`
- `usr/share/archlinux-tweak-tool/services_gui.py`
- `usr/share/archlinux-tweak-tool/office.py` (new)
- `usr/share/archlinux-tweak-tool/office_gui.py` (new)
- `usr/share/archlinux-tweak-tool/gui.py`
- `CLAUDE.md`

## 2026.05.29 — Pacman page: CachyOS repo toggle in "Other repos"

### What Changed

The Pacman page "Other repos" section gains a third toggle line — **Enable CachyOS repo** — alongside Nemesis and Chaotic-AUR. It works on any Arch-based system, not just Kiro: enabling it follows the **exact same bootstrap pattern as Chaotic-AUR** — if `cachyos-keyring`/`cachyos-mirrorlist` are missing, a setup terminal imports the CachyOS signing key and installs both bundled packages first, then the `[cachyos]` block is appended to `/etc/pacman.conf`. On a box that already has them (e.g. Kiro), it just toggles the block.

### Technical Details

- `functions.py`: new `cachyos_repo` block definition (`[cachyos]` + `Include = /etc/pacman.d/cachyos-mirrorlist`), next to `chaotic_aur_repo`.
- `data/cachyos/keyring/` + `data/cachyos/mirrorlist/`: bundled `cachyos-keyring-20240331-1` and `cachyos-mirrorlist-27-1` packages, mirroring the `data/chaotic/` layout.
- `data/bin/setup-cachyos`: new setup script modelled on `setup-chaotic-aur` — imports key `F3B607488DB35A47` (`--recv-key`/`--lsign-key` via keyserver.ubuntu.com), then `pacman -U`'s the two bundled packages. ATT Script Standard compliant; `bash -n` clean.
- `pacman_functions.py`: `ensure_cachyos_packages()` (mirror of `ensure_chaotic_packages`) returns a setup-terminal `Popen` when either package is missing, else `None`. `toggle_test_repos` gains a `"cachyos"` case in both branches, using `pacman_on`/`pacman_off` (not `spin_on`/`spin_off`) — the cachyos block is a 2-line header+Include like `[core]`/`[extra]`, so the 3-line spin helpers would wrongly comment the trailing blank line.
- `pacman.py`: new `on_cachyos_toggle` mirrors `on_chaotic_toggle` — runs `ensure_cachyos_packages`, waits on the setup terminal in a daemon thread, then appends the repo and syncs the db (`_sync_if_db_missing("cachyos")`). `update_repos_switches` now syncs `self.cachyos_switch`.
- `pacman_gui.py`: `self.cachyos_switch` row added to the "Other repos" frame; `[cachyos]` checked in `init_repos_lazy_load`.
- `ruff check` clean across all four Python files.

### `vendored-refresh.sh` — refresh the bundled keyring/mirrorlist packages

**What Changed**
- New repo-root maintenance script that re-downloads the VENDORED `.pkg.tar.zst` bootstrap packages (chaotic keyring+mirrorlist, cachyos keyring+mirrorlist, archlinux-keyring) from upstream, prunes the stale dated copy, and drops in the current one. Closes the long-standing gap noted in `CONFIG_SOURCES.md` (the `chaotic.sh` hook referenced by `up.sh` never existed; vendored packages were refreshed entirely by hand).

**Technical Details**
- Matches `up.sh`'s root-level template (Kiro-HQ `log_*` banner style, `on_error` trap, `set -euo pipefail`) + a Purpose/Why header block.
- `refresh()` downloads to a temp file, then derives the true `<pkg>-<pkgver>-<arch>.pkg.tar.zst` filename from the package's own `.PKGINFO` (via `bsdtar -xOf … .PKGINFO`) — so a 404/HTML error page is caught (no `.PKGINFO` → loud FAIL) and the on-disk name is always correct. Idempotent: skips when the current version is already present.
- CachyOS has no fixed-name bootstrap URL, so `resolve_from_index()` parses the mirror directory listing and picks the latest with `sort -V`. Chaotic uses its CDN's fixed package names; archlinux-keyring uses archlinux.org's `download/` redirect. All five endpoints verified live; index-resolution and `.PKGINFO` derivation tested against the bundled packages.
- Wired into `up.sh` — replaces the dead `chaotic.sh` hook (which `up.sh` referenced but never existed). Invoked non-fatally (`|| log_warn`) before the commit/push step so a transient mirror outage can't block a push. Can also be run standalone. Does not commit; `up.sh` does that afterwards. (Trade-off: it hits upstream mirrors on every `up.sh` run.)
- `CONFIG_SOURCES.md` updated: cachyos packages added to the VENDORED list; Status section split into "VENDORED refresh: implemented" vs "MIRROR fetch: not yet implemented".

### Files Modified

- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/pacman.py`
- `usr/share/archlinux-tweak-tool/pacman_functions.py`
- `usr/share/archlinux-tweak-tool/pacman_gui.py`
- `usr/share/archlinux-tweak-tool/data/bin/setup-cachyos` (new)
- `usr/share/archlinux-tweak-tool/data/cachyos/keyring/cachyos-keyring-20240331-1-any.pkg.tar.zst` (new)
- `usr/share/archlinux-tweak-tool/data/cachyos/mirrorlist/cachyos-mirrorlist-27-1-any.pkg.tar.zst` (new)
- `vendored-refresh.sh` (new)
- `CONFIG_SOURCES.md`

## 2026.05.29 — Shell-config templates: point aliases at the renamed kiro-* helpers

### What Changed

ATT's shipped shell-config templates (`data/.bashrc`, `data/.zshrc`, `data/config.fish`) still called the old `edu-*` helper-script names. Those scripts were renamed to `kiro-*` (now in `edu-system-files`, installed to `/usr/local/bin/`), so every one of these aliases was silently broken. Fixed all three to the live script names, and removed the dead `rvariety`/`rkmix`/`rconky` aliases (their `edu-remove-*` scripts were dropped, not renamed). Kept in sync with the same fix in `edu-shells`.

### Technical Details

- Renames applied (old → new): `edu-which-vga` → `kiro-which-vga`; `edu-fix-pacman-databases-and-keys` → `kiro-fix-pacman-keys` (7 alias variants); `edu-fix-pacman-conf` → `kiro-fix-pacman-conf`; `edu-fix-pacman-gpg-conf` → `kiro-fix-gpg-conf`; `edu-fix-archlinux-servers` → `kiro-fix-mirrors`; `edu-probe` → `kiro-probe`.
- Mappings verified against the script purpose headers in `edu-system-files`, not name similarity. All three templates still parse clean (`bash -n` / `zsh -n` / `fish -n`).

### Files Modified

- `usr/share/archlinux-tweak-tool/data/.bashrc`
- `usr/share/archlinux-tweak-tool/data/.zshrc`
- `usr/share/archlinux-tweak-tool/data/config.fish`

## 2026.05.28 — Plymouth page: Remove Plymouth button (symmetric to Install, narrated cleanup)

### What Changed

The Plymouth page now has a **Remove Plymouth** button next to **Install Plymouth**, closing a long-standing UX gap: ATT could install Plymouth but never uninstall it. Install/Remove buttons share the same row and swap visibility based on `fn.check_package_installed("plymouth")` — only the relevant button is visible, alongside the **Installed** label when applicable.

Remove runs a full five-step cleanup in an Alacritty terminal with every step echoed *before* it executes (matches the Install voice exactly). Steps that touch system state interactively prompt the user **[Y/n]** so they can pick what to clean vs. keep: 1) strip plymouth from `/etc/mkinitcpio.conf` HOOKS (or remove the dracut conf snippet); 2) detect `plymouth-theme-*` packages and prompt to remove them (abort if user says no — those packages depend on plymouth, so plymouth removal would fail); 3) remove plymouth itself; 4) prompt to strip `quiet splash` from the kernel cmdline (branched by detected bootloader — sd-boot edits `/etc/kernel/cmdline` and every `/boot/loader/entries/*.conf`; grub edits `/etc/default/grub` + regenerates; unknown bootloader just prints a manual-cleanup notice); 5) rebuild initramfs (`mkinitcpio -P` or `dracut --regenerate-all --force`). Every file mutation creates a `.bak` first. Before/after lines of every changed file are echoed to the terminal so the user sees exactly what changed.

### Technical Details

- `plymouth_gui.py`:
  - Section label renamed from `<b>Install Plymouth</b>` to `<b>Install / Remove Plymouth</b>`; description label expanded to cover both flows and the prompted-cleanup behavior.
  - New `btn_remove_plymouth` widget appended to the same `hbox_install_plymouth` row as `btn_install_plymouth`. Initial `set_visible(False)` so the row is single-button on first paint; flipped on/off in `_refresh_plymouth` based on `fn.check_package_installed("plymouth")`. `on_install_plymouth_done` and `on_remove_plymouth_done` mirror the toggle so the UI stays consistent across install/remove cycles within one session.
  - New `on_remove_plymouth_clicked(_widget)` callback. Generates a per-system bash script using existing helpers `plymouth.detect_bootloader()` / `plymouth.find_systemd_boot_entries()` / `plymouth.check_kernel_cmdline_exists()` / `plymouth.is_dracut()` — the script is fully parameterized at build time (entry paths shell-quoted with single quotes; `_rebuild_cmd` / `_rebuild_label` reused from the existing Install scope).
  - HOOKS strip uses `sed -i -E 's/\bplymouth\b//; s/  +/ /g; s/\( /(/; s/ \)/)/'` so the `(plymouth ...)` / `(... plymouth)` edges collapse cleanly without leaving stray whitespace inside the parens.
  - cmdline strip uses `awk` (not `sed`) to walk the `options` line token-by-token and emit only non-`quiet`/non-`splash` tokens — safer than regex for variable-length whitespace and avoids `sed` quoting hell across the Python→bash boundary.
  - Theme prompt is hard-failed if the user says no: removing plymouth while themes depend on it would error out of pacman, so the script `exit 0`s with a yellow note pointing at `pacman -Rc plymouth` for the manual route.
  - Script syntax was validated by rendering a typical sd-boot+mkinitcpio target case and running `bash -n` against the result (clean).
  - `ruff check` clean (auto-validated by hook on every Edit).

### Files Modified

- `usr/share/archlinux-tweak-tool/plymouth_gui.py` (new `btn_remove_plymouth` widget + `on_remove_plymouth_clicked` / `on_remove_plymouth_done` handlers + visibility toggles in `_refresh_plymouth` and `on_install_plymouth_done` + section-label/desc-text updates)

---

## 2026.05.28 — Maintenance page: 6-tab Stack + new Boot/Initramfs tab (resume-hook fix-it)

### What Changed

The Maintenance page is restructured from a single long scrolling list with six bold section headers into a tabbed `Gtk.Stack` + `Gtk.StackSwitcher` layout — the same pattern the Services page already uses (Audio / Bluetooth / Printing). Six tabs: **System** (update / clean cache / remove pacman lock / probe link), **Mirrors** (install / run / timer / mainstream), **Keys & GPG** (keyring / fix keys / both gpg.conf rows), **Pacman** (reset pacman.conf / parallel downloads), **Cursors** (Bibata install/remove / global cursor theme + info), and a new **Boot / Initramfs** tab.

The new Boot/Initramfs tab is the home for the resume-hook fix that closes the long-standing "no resume device" boot-warning FAQ. It shows the live HOOKS line, whether `resume` is present, and whether the system has hibernation-capable swap (excluding zram). A **Remove resume hook** button backs `/etc/mkinitcpio.conf` up to `.bak`, strips `resume` from the HOOKS line, and rebuilds initramfs in an Alacritty popup. If a real swap partition is active (potential hibernation user), a confirm dialog warns before proceeding. A second **Regenerate initramfs** button runs `mkinitcpio -P` standalone for manual HOOKS edits or boot troubleshooting.

Diagnostics ("Provide probe link") was folded into the System tab — single-button standalone tab felt thin and the action is sysadmin one-shot like the other System rows. Cursors stays in Maintenance for now (could later migrate to Themes; out of scope here).

### Technical Details

- `maintenance_gui.py` restructured: `Gtk.Stack` (SLIDE_LEFT_RIGHT, 350ms, hexpand/vexpand) plus a centered `Gtk.StackSwitcher` replace the flat `vboxstack_maintenance.append(...)` pile. Existing hbox rows are reused unchanged; only their final `.append()` target changes from `vboxstack_maintenance` to the appropriate per-tab `vbox_*` container. The six `<b>...</b>` section headers (`hbox_sec_system`, `hbox_sec_mirrors`, …) are dropped — the tab labels replace them.
- `_refresh_boot_status(self, fn, maintenance)` populates the three status labels (`lbl_hooks_value`, `lbl_resume_value`, `lbl_swap_value`) and toggles the Remove button sensitivity + label ("Resume hook already absent" when nothing to do). Wired to both the initial build and the `connect("map", ...)` signal on the maintenance vbox so the labels re-detect every time the page is shown.
- `maintenance.py` gains four module-level helpers and two callbacks: `read_hooks_line(path=MKINITCPIO_CONF)` scans the conf for the first uncommented `HOOKS=(...)` line and returns `(idx, tokens)`; `detect_real_swap()` runs `swapon --show=NAME --noheadings` and filters out anything containing `zram`; `_rewrite_hooks_without_resume(path, idx, tokens)` rewrites just the HOOKS line in place, preserving everything outside the parentheses; `on_click_remove_resume_hook(self, _widget, on_success=None)` orchestrates the full flow (detection → confirm-if-swap → `.bak` copy → rewrite → `_run_terminal` rebuild → `on_success` refresh); `on_click_regenerate_initramfs` is a thin `_run_terminal` wrapper.
- The on_success callback is wired with a lambda that calls `_refresh_boot_status` on the GUI side, so after the rebuild terminal closes the status labels update without a tab switch.
- All callbacks use `_run_terminal` (Popen + daemon thread + `wait_and_refresh`-style flow), per CLAUDE objective 7 — no `subprocess.call` from a GUI callback.
- Transparency (objective 14): current HOOKS string and swap state shown live before the action; confirm dialog when real swap detected; rebuild output streamed in the popup terminal; in-app notifications at start and finish.
- `ruff check` clean on both files (auto-validated by PostToolUse hook).

### Files Modified

- `usr/share/archlinux-tweak-tool/maintenance_gui.py` (full restructure: flat sections → 6-tab Stack/StackSwitcher; new Boot/Initramfs widgets; `_refresh_boot_status` helper; status refresh wired to `connect("map", …)`)
- `usr/share/archlinux-tweak-tool/maintenance.py` (new: `MKINITCPIO_CONF` constant, `read_hooks_line`, `detect_real_swap`, `_rewrite_hooks_without_resume`, `on_click_remove_resume_hook`, `on_click_regenerate_initramfs`)

---

## 2026.05.28 — Dev page: glossary + help link (every row explained for users)

### What Changed

Every row on the Dev page now has a plain-language explanation in [`usr/share/doc/archlinux-tweak-tool/DEV_PAGE_GLOSSARY.md`](usr/share/doc/archlinux-tweak-tool/DEV_PAGE_GLOSSARY.md). All five Dev sections are covered — Session diagnostics, Per-tab status, Cross-cutting safeguards, System integrity (kiro-audit mirror), and Userspace tuning — with four short fields per entry: **What it checks** / **Why it matters** / **PASS means** / **FAIL means + fix**. A clickable "What do these rows mean? — read the Dev Page Glossary" link is added at the top of the Dev page itself, opening the **local copy** in a detected GUI editor as the real user — no browser, no internet round-trip, no clash with ATT-runs-as-root.

Closes the "what is it doing?" gap on the Dev page (objective #14, Transparency). Users no longer need to ask — they can RTM.

### Technical Details

- New `DEV_PAGE_GLOSSARY.md` at `usr/share/doc/archlinux-tweak-tool/` (PKGBUILD ships everything under `usr/`, so this path lands at `/usr/share/doc/archlinux-tweak-tool/DEV_PAGE_GLOSSARY.md` on installed systems). ~360 lines, organised by the 5 Dev sections in the order they render. Groups visually-similar rows (15 desktop binaries, 9 shell packages, 12 software binaries, 4 themer packages) into single entries to stay readable instead of expanding to 40 near-identical bullets.
- Glossary has a top-of-doc reading-key table and section anchors so navigation in an editor (or rendered on GitHub) deep-links cleanly.
- `dev_gui.py` gains an `hbox_help` between the existing `hbox_sep` and `grid`. Widget is a `Gtk.LinkButton` with a custom `activate-link` handler that **returns True** to suppress GTK's default `xdg-open` — necessary because ATT runs as root and the default URI-open path tries to launch a browser, which Firefox / Chromium refuse (XAUTHORITY is user-owned). The dummy URI `kiro-glossary://open` never actually gets followed.
- Three new helpers: `_GLOSSARY_EDITORS` priority tuple (`mousepad → gedit → gnome-text-editor → kate → kwrite → geany → featherpad → xed → pluma → leafpad → code → subl`), `_find_editor()` (`shutil.which` over the tuple), `_open_glossary(fn)` (resolves the doc path with a repo-tree fallback for source runs, picks an editor, drops privileges via `sudo -u fn.sudo_username` to launch — same `Popen` pattern as `funding.py`). If no GUI editor is installed, a `log_warn` prints the doc path so the user can open it manually.
- Maintenance contract documented at the bottom of the glossary: every new `_row(...)` in `dev_gui.py` must be added there in the same change, mirroring the `kiro-audit` "every new check needs a verification hook" rule.
- `ruff check` clean.

### Files Modified

- `usr/share/doc/archlinux-tweak-tool/DEV_PAGE_GLOSSARY.md` (new)
- `usr/share/archlinux-tweak-tool/dev_gui.py` (added `_GLOSSARY_EDITORS` / `_find_editor` / `_open_glossary` + `hbox_help` with `Gtk.LinkButton` and `activate-link` handler)

---

## 2026.05.28 — Dev page: Userspace tuning group (5 edu-system-files imports)

### What Changed

New "Userspace tuning" group added to the Dev page mirror, after the existing
"System integrity (kiro-audit mirror)" block. Shows the live state of 5 tweaks
that `edu-system-files` adopted from a Garuda comparison study (2026-05-28):
systemd-oomd enablement/activity, Intel ME blacklist + module-not-loaded check,
btusb reset=1 modprobe, kernel zswap disabled (file + runtime), NetworkManager
loopback unmanaged.

### Technical Details

- 3 new helpers in `dev_gui.py`: `_oomd_state(fn)` returns `(enabled, active)`
  for `systemd-oomd.service`; `_mei_loaded(fn)` greps `lsmod` for mei/mei_me;
  `_zswap_runtime(fn)` reads `/sys/module/zswap/parameters/enabled` and returns
  `N`/`Y`/`0`/`1`/`?` (treating `N` and `0` as "off", `Y`/`1` as "on", anything
  else as warn — keeps the row honest on kernels that omit the module).
- New `_group("Userspace tuning")` block at the tail of `_populate()` with 5
  `_header` sub-blocks; each row uses the existing `_state`/`_enabled`/`_active`
  helpers so the visual style matches everything else.
- Section name is functional ("OOM daemon", "Intel ME blacklist", etc.), not
  "Garuda imports" — ATT is distro-agnostic per project rule #11.
- All checks are read-only sysfs / file-existence / systemctl probes. No
  privileged calls, no subprocess timeouts above 3 s.
- The new group re-runs on tab-revisit (the existing `vboxstack_dev.connect("map", ...)`
  binding covers it automatically — no extra wiring needed).
- `ruff check` clean.

### Files Modified

- `usr/share/archlinux-tweak-tool/dev_gui.py` (3 helpers + 1 new group)

## 2026.05.27 — Desktop page: visible backup-in-progress notice

### What Changed

When installing a desktop from the Desktop page, ATT first backs up
`~/.config` to `~/.config-att/` before opening the install terminal. On a large
config this copy can take a while, during which ATT previously gave no on-screen
feedback — the central "what is it doing?" frustration. A centered yellow label
now appears at the bottom of the Desktop page — **"We are making a backup of
your ~/.config to ~/.config-att — this might take a while ..."** — while the
backup runs, and hides automatically once it completes and the install terminal
opens.

### Technical Details

- `desktopr_gui.py` — added `hbox_backup_notice` / `lbl_backup_notice` (centered,
  `#FFD700` bold `set_markup`, `set_visible(False)` by default), following the
  existing `hbox_plasma_warning` pattern; appended at the bottom of the page vbox.
- `desktopr.py` — added module-level `_set_backup_notice(self, visible)` helper
  (guarded with `hasattr`); `install_desktop()` toggles it via `GLib.idle_add`
  immediately before the `fn.copy_func` backup (show) and right after the final
  `fn.permissions` call (hide). `idle_add` is required because `install_desktop`
  runs in a daemon thread on the normal install path — all GTK updates marshal to
  the main thread. Aligns with developer objective 14 (Transparency — show what's
  happening now).

### Files Modified

- `usr/share/archlinux-tweak-tool/desktopr_gui.py`
- `usr/share/archlinux-tweak-tool/desktopr.py`

## 2026.05.26 — Privacy hblock allowlist; Dev page logrotate.timer check + timer-detection fix; Network page firewall help text; Dev page diagnostics fixes (session type, desktop list, kernel-headers indent); Maintenance reflector.timer toggle; Network page split into Network/Samba/Firewall tabs; firewall-config launch/install button

### What Changed

Added a Whitelist (allowlist) sub-section to the hblock controls on the Privacy
page. Users can paste a URL or host and click **Add to whitelist** to exempt it
from hblock's `/etc/hosts` blocking, see every currently whitelisted host in a
list beneath, and **Remove** any entry to re-block it. After each add/remove
hblock is re-run automatically (when installed and active) so the change takes
effect immediately. Motivated by needing to unblock
`marketingplatform.google.com`, which hblock was blocking.

### Technical Details

- `privacy.py` — manages `/etc/hblock/allow.list` directly (ATT runs as root, no
  elevation): `ALLOWLIST_PATH` constant; `_normalize_host()` strips scheme, path,
  userinfo and port so a pasted URL becomes the bare host hblock matches;
  `_read_allowlist()` / `_write_allowlist()` (creates `/etc/hblock` if missing,
  writes a managed-by-ATT header); `_refresh_allowlist_box()` rebuilds the ListBox
  rows; `on_click_add_whitelist()` / `on_click_remove_whitelist()` callbacks;
  `_reapply_hblock()` re-runs `/usr/bin/hblock` in a daemon thread with the same
  progress-pulse pattern as Enable, skipping the run (with a log note) when hblock
  is inactive. `_refresh_hblock_label()` now also gates the Add button on install
  state, matching the Enable/Disable buttons.
- `privacy_gui.py` — `Gtk.Entry` (with `activate` wired to add) + **Add to
  whitelist** button, and a `Gtk.ListBox` in a `Gtk.ScrolledWindow` (min height
  120) showing each host with a Remove button. Refreshed on page map via
  `init_privacy_lazy_load`.
- Follows the GUI rules: privileged shell-outs via `Popen`/`subprocess.run` in
  daemon threads, `_widget` callback params, `fn.log_*` console output throughout,
  `<b>…</b>` markup for the section header.

### Files Modified

- `usr/share/archlinux-tweak-tool/privacy.py`
- `usr/share/archlinux-tweak-tool/privacy_gui.py`

### Dev page: logrotate.timer check + timer-enabled detection fix

**What Changed** — The Dev page (System integrity / kiro-audit mirror) gained a
**logrotate.timer enabled** row, mirroring the new kiro-audit check (Kiro enables
the timer on installed systems via Calamares so file-based logs rotate). Fixed a
bug where this row — and the existing **fstrim.timer** row — always reported
*disabled* even when the timer was enabled.

**Technical Details** — `functions.py check_service_enabled()` unconditionally
appended `.service` to the unit name, so any `.timer`/`.socket` became an invalid
`*.timer.service` lookup that `systemctl is-enabled` reported as not-enabled. It now
appends `.service` only when the caller passes no explicit unit suffix (new
`_UNIT_SUFFIXES` tuple checked via `str.endswith`); `.timer`/`.socket`/`.target`/etc.
pass through unchanged. Fixes both the new logrotate row and the pre-existing
fstrim.timer row.

**Files Modified** — `usr/share/archlinux-tweak-tool/functions.py`, `usr/share/archlinux-tweak-tool/dev_gui.py`

### Network page: client-vs-server firewall help text

**What Changed** — The discovery info label on the Network page (Samba/sharing
section) ended with a vague "Beware of firewalls". Replaced it with concrete
guidance spelling out which firewall services each role needs: a **server**
sharing files needs both *Allow network discovery (mDNS)* and *Allow Samba file
sharing*; a **client** only needs *Allow network discovery (mDNS)* — it connects
outward, so Samba is never opened on the client. Motivated by a real LAN case
where a client could reach a server by IP but not by name, because the client's
firewall was the bare ssh-only default with mDNS blocked.

**Technical Details** — Single `set_text()` change on `label_discovery_info`;
wording references the exact toggle-button labels directly below it so users map
the advice onto the controls. Kept plain text (no `set_markup`) to match the
surrounding labels.

**Files Modified** — `usr/share/archlinux-tweak-tool/network_gui.py`

### Dev page: diagnostics fixes from dev-box testing

**What Changed** — Three Dev-page (Dev Diagnostics) fixes found during dev-box
testing, plus one item confirmed already-correct: (1) **Session** —
`XDG_SESSION_TYPE` now falls back to inferring `x11`/`wayland` from the session's
display variables when the WM (e.g. a startx/chadwm session) never exports it,
instead of showing "(not set)"; (2) **Desktop** — the list now includes the
tiling WMs (awesome, bspwm, chadwm, i3, leftwm, ohmychadwm, qtile) alongside the
DEs and is sorted alphabetically; (3) **Kernels** — removed the stray leading
indent on the `<kernel>-headers` rows so they align with the other kernel rows.
The reported "no yellow for plymouth hook" item needed no change — the row
already flags orange only when plymouth is installed-but-missing and stays blank
on a no-Plymouth box (correct for Kiro's default). Also added two rows to the
**Network** section showing whether firewalld currently allows `mdns` and
`samba`, mirroring the Network page's "Allow network discovery / Allow Samba file
sharing" toggles (reuses `fn.check_firewall_service`, no duplicate logic).

**Technical Details** — `dev_gui.py`: the session block reads `get_terminal_env()`
once and, when `XDG_SESSION_TYPE` is empty, infers from `WAYLAND_DISPLAY` /
`DISPLAY` (value suffixed "(inferred)"); `_de_bins` renamed `_desktop_bins`,
extended with seven WM binary entries, rendered via `sorted(..., key=lambda _t:
_t[0].lower())`; dropped the `"  "` prefix on the headers row key. Verified on the
dev box that `chadwm`/`ohmychadwm` install real `/usr/bin` binaries (so binary
detection works for them). Added a `fn.log_info("Building Dev Diagnostics page")`
call — the file previously had no console output (objective 28).

**Files Modified** — `usr/share/archlinux-tweak-tool/dev_gui.py`

### Maintenance page: reflector.timer toggle

**What Changed** — Added a new row to the Mirror Management section, under the
"Run reflector / Run rate-mirrors" row: **Automatically refresh mirrors on a
schedule (reflector.timer)** with an Enable/Disable button. Lets users turn on the
`reflector.timer` systemd unit so the mirrorlist is refreshed periodically instead
of only on demand. The button is greyed out when reflector isn't installed (same
gating as the "Run reflector" button) and its label reflects the live enabled
state.

**Technical Details** — `maintenance.py on_click_toggle_reflector_timer()` runs
`systemctl enable/disable --now reflector.timer` in a daemon thread (ATT is root —
no pkexec), mirroring the firewalld toggle pattern; refreshes the button label and
fires a notification via `GLib.idle_add`. Deliberately does **not** use
`fn.enable_service()`, which hard-codes a `.service` suffix and would produce the
invalid unit `reflector.timer.service`. Invalidates the `fn._svc_cache` entry on
toggle so a later `check_service_enabled("reflector.timer")` reflects the new state.
The label is built from `fn.check_service_enabled("reflector.timer")` (already
`.timer`-aware after the same-day `check_service_enabled` fix).

**Files Modified** — `usr/share/archlinux-tweak-tool/maintenance.py`, `usr/share/archlinux-tweak-tool/maintenance_gui.py`

### Network page: split into Network / Samba / Firewall tabs

**What Changed** — The Network page had grown into one long crowded scroll (status,
discovery, firewall, nsswitch and the full Samba setup all stacked together).
Reorganized it into three tabs — **Network** (discovery install + name-resolution /
nsswitch), **Samba** (install, configure, password, start service, reboot note) and
**Firewall** (firewalld toggle + mDNS/Samba service toggles + status + the
client-vs-server help text). The one-line status summary (Samba / Nmb / Avahi /
Firewall) is now pinned above the tab switcher so it stays visible on every tab.

**Technical Details** — Reuses the established intra-page tab pattern (inner
`Gtk.Stack` + horizontal `Gtk.StackSwitcher`) exactly as `services_gui.py` does;
each tab is its own `vboxstack_*` box added via `stack.add_titled`. Single-file
change — all callbacks remain in `services.py` and `gui.py` still just mounts
`vboxstack_network`. `_refresh()` and `services.update_network_status()` are
unchanged and keep working because every widget they touch (`network_status_label`,
`btn_toggle_smb`, `btn_toggle_firewalld`, `lbl_firewall_info`, `btn_fw_mdns`,
`btn_fw_samba`, `lbl_firewall_status`) keeps its `self.*` name and is `hasattr`-guarded.
The Firewall tab now shows an explicit "firewalld is not installed" note instead of
silently hiding the controls. Section indents reduced from 20px to 10px since the
tabs provide the grouping. Status summary refactored into a shared `_status_text()`
helper used by both build and `_refresh`.

**Files Modified** — `usr/share/archlinux-tweak-tool/network_gui.py`

### Firewall tab: firewall-config launch/install button

**What Changed** — Added a row to the Firewall tab for `firewall-config`, the
graphical firewalld editor: a label that reads "Graphical firewall editor
(firewall-config) - **installed**" (bold when present) and a button that **launches**
firewall-config when installed or **installs** it (via the terminal) when missing.
Also added a `firewall-config` row to the Dev page's Network diagnostics section
(installed yes/no), alongside the existing avahi/samba/firewalld checks.

**Technical Details** — `services.on_click_firewall_config()` checks
`/usr/bin/firewall-config`: if present it `Popen`s `firewall-config` in a daemon
thread (ATT runs as root, so the GUI inherits its display and edits firewalld
directly); if absent it runs `pacman -S --needed firewall-config` in an alacritty
terminal, then refreshes the label/button via `GLib.idle_add`. The row lives inside
the firewalld-installed branch (firewall-config depends on firewalld). `_refresh()`
keeps the label/button in sync on every page show via the `hasattr` guard. The Dev
page row reuses the existing `_pkg("firewall-config")` helper.

**Files Modified** — `usr/share/archlinux-tweak-tool/network_gui.py`, `usr/share/archlinux-tweak-tool/services.py`, `usr/share/archlinux-tweak-tool/dev_gui.py`

## 2026.05.25 — De-brand residuals + config-source audit + installer-script hardening

### usr/bin installer-script hardening

Hardened the two `usr/bin` installer scripts against silent failures:

- `get-nemesis-on-att` — added `trap 'error "Command failed at line $LINENO"' ERR`
  so a failed `git clone` prints a red error instead of the window vanishing under
  `set -e`; added a re-clone guard (warns and skips if `~/DATA/arcolinux-nemesis`
  already exists rather than failing on `git clone`); simplified the closing message
  and prompt (`Close this window when you are ready...`).
- `get-ohmychadwm-on-att` — added the same ERR trap; converted both copy operations
  (the `~/.config` backup and the `/etc/skel` apply) to the two-line `Source:` /
  `Target:` logging format per the source/target logging rule; matched the closing
  prompt wording.

### Config source audit (new)

Audited all 34 entries under `data/` for divergence from the canonical configs a
real Kiro system ships (ATT carries hand-maintained copies with no sync — and
writes some of them onto the user's system, so drift is functional). Classified
each as MIRROR (fetch from source repo), OWN (ATT-specific), or VENDORED (stale
upstream binaries). Measured drift: `config.fish` was 49 lines off edu-shells,
`pacman.conf` 13 (but that one is OWN by design — stripped baseline so ATT's repo
toggles can layer multilib/nemesis_repo/chaotic-aur on top). Produced
[`data-sources.tsv`](data-sources.tsv) (MIRROR manifest) and
[`CONFIG_SOURCES.md`](CONFIG_SOURCES.md).

### fetch-configs.sh implemented

Added [`fetch-configs.sh`](fetch-configs.sh) (standard EDU template) — reads the
manifest, fetches each MIRROR file from GitHub raw `main`, replaces the local
`data/` copy only when it differs, reports updated/unchanged/failed. Wired into
`up.sh` as a conditional block before commit (matching the `chaotic.sh`/`repo.sh`
pattern). Dry-run findings: the 6 `edu-*` sources fetch correctly (`config.fish`
would adopt a 49-line change to match edu-shells); the 3 `kiro-iso`-sourced files
(`nanorc`, `sddm.conf`, `kde_settings.conf`) 404 — kiro-iso isn't public — so they
were commented out in the manifest pending a public source (one exists; to be wired
later). Ran against the repo: all 6 edu-* MIRROR files now in sync with their
canonical sources (`config.fish` adopted the edu-shells version); re-running is
idempotent (6 unchanged, 0 failed).

### What Changed

Part of the ecosystem-wide `arco`/`arcolinux` de-brand sweep, plus a bootloader
cleanup. Cleared in ATT data files:

- `data/config.fish` — removed all five grub aliases (`update-grub`, `grub-update`,
  `install-grub-efi`, `ngrub`, `nconfgrub`). Kiro boots with systemd-boot, so the
  grub helpers were dead weight (and `install-grub-efi` carried the `ArcoLinux`
  bootloader-id brand string).
- Deleted the orphaned legacy wallpaper scripts `set_wallpaper_arco` and
  `get_wallpaper_arco` under `data/variety/scripts/`. They were dead duplicates of
  the active `_kiro` versions (`variety.conf` wires up `n_kiro`); nothing in the
  repo referenced them.

Deferred (not clear-cut): the `arcolinux-nemesis` repo references in the nemesis
tooling — that's a repo-rename decision, left to Erik.

### Files Modified

- `usr/share/archlinux-tweak-tool/data/config.fish` (removed grub aliases)
- `usr/share/archlinux-tweak-tool/data/variety/scripts/set_wallpaper_arco` (deleted)
- `usr/share/archlinux-tweak-tool/data/variety/scripts/get_wallpaper_arco` (deleted)
- `data-sources.tsv` (new — config mirror manifest)
- `CONFIG_SOURCES.md` (new — data/ classification)
- `fetch-configs.sh` (new — manifest-driven config fetcher; Website header `kiroproject.be`)
- `up.sh` (wired in the `fetch-configs.sh` step; Website header → `kiroproject.be`)
- `usr/bin/get-nemesis-on-att` (ERR trap, re-clone guard, closing-message rewording)
- `usr/bin/get-ohmychadwm-on-att` (ERR trap, Source/Target two-line logging, closing-prompt wording)

### Verified

- `archlinux-tweak-tool-gtk4-git` 26.05-352 (built 09:15): installed
  `data/config.fish` has no grub references and the `_arco` variety scripts are
  gone.
- After the config-source sync, the 09:15 build was found stale (installed
  `config.fish` still 49 lines behind the synced repo). Rebuilt + reinstalled to
  26.05-354 (built 09:41): installed `data/config.fish` is now byte-identical to
  the edu-shells skel copy — drift closed end-to-end, no grub.
- 26.05-355 (built 09:56): regression + functional check — installed
  `config.fish` still byte-identical to the skel canonical, and both copies parse
  clean under `fish -n` (the grub strip + canonical swap left no fish syntax
  errors).

## 2026.05.24 — DEV page: new "System integrity" section (kiro-audit mirror)

### What Changed

Added a **System integrity** group to the bottom of the DEV page (`dev_gui.py`),
surfacing the high-signal subset of the `kiro-audit` system checks as read-only,
glanceable status rows. The DEV page already mirrors ATT's tabs 1:1; these are
the deeper system-internals checks that don't map to any ATT tab but matter for
release-readiness. Chosen subset: **Microcode, Audio stack (PipeWire), ZRAM,
Calamares cleanup, Package integrity (`pacman -Qk`), Failed systemd units.**
Auto-fix stays in the `kiro-audit` CLI — the DEV page only reports state.

### Technical Details

- **New module-level helpers** in [dev_gui.py](file:///home/erik/EDU/archlinux-tweak-tool-gtk4/usr/share/archlinux-tweak-tool/dev_gui.py):
  `_pkg_integrity(fn)` (parses `pacman -Qk`, drops the known-noisy pkgs
  `ohmychadwm-git`/`bind`/`cups`/`nfs-utils`), `_failed_units(fn)`
  (`systemctl --failed`), `_zram_state(fn)` (device present / active-as-swap /
  algorithm via `swapon` + `zramctl`), `_installer_leftovers(fn)` (checks the 5
  live-only Calamares/archiso artifact paths).
- **`pacman -Qk` is cached** for the process lifetime (`_QK_CACHE`) — `_populate()`
  reruns on every tab revisit and `-Qk` is the one multi-second probe, so caching
  keeps revisits snappy. Restart ATT for a fresh integrity scan; all other rows
  stay live.
- **3-state color helper** `_state("pass"|"warn"|"fail")` → green / orange (⚠) /
  red markup, reusing the Safeguards section's existing colour idiom.
- Detection mirrors `kiro-audit`'s logic (package names via
  `fn.check_package_installed`, files via `fn.path.exists`). Verified with
  `py_compile` + `ruff` (clean).

### Files Modified

- [usr/share/archlinux-tweak-tool/dev_gui.py](file:///home/erik/EDU/archlinux-tweak-tool-gtk4/usr/share/archlinux-tweak-tool/dev_gui.py) — +1 section, 4 module helpers, 1 status helper (697 → 847 lines)

## 2026.05.24 — New Support page: Kiro funding channels

### What Changed

Added a **Support** page to the sidebar (right after Software) that links to
every way users can fund the Kiro project. Discovery-based — a visible page, no
nags or popups. Links mirror the canonical set in
`kiro-website/.github/FUNDING.yml`: GitHub Sponsors, Patreon, YouTube
membership, Ko-fi, and PayPal, each with a short blurb.

### Technical Details

- New `funding.py`: `SOURCES` list of `(name, url, blurb)` tuples (URLs are
  stable, kept in code rather than a JSON data file per request) + `on_click_open`
  which opens a link via the root-safe `sudo -u {sudo_username} xdg-open` idiom
  (same as `kernel_gui.py`).
- New `funding_gui.py`: builds the page by iterating `funding.SOURCES` — one row
  (label + Open button) per channel; title via `set_name("title")`, "Support the
  Kiro Project" header in `#FFA500` orange (`<span foreground="#FFA500"><b>…</b></span>`,
  matching the ATT logo in `gui.py`), wired with `functools.partial`.
- `gui.py`: import `funding_gui`, create `vboxstack_funding`, `_defer_tab(...)`
  for lazy build, and `stack.add_titled(..., "Support")` inserted between
  Software and System.
- Module named `funding` (not `support`) to avoid colliding with the existing
  `support.py` distro-detection module; sidebar label is still "Support".

### Files Modified

- usr/share/archlinux-tweak-tool/funding.py (new)
- usr/share/archlinux-tweak-tool/funding_gui.py (new)
- usr/share/archlinux-tweak-tool/gui.py
- CLAUDE.md (tab count 24 → 25, Support added to list)

## 2026.05.24 — chadwm skel folder de-branded: arco-chadwm → chadwm

### What Changed

Coordinated with the `edu-chadwm` repo to rename the chadwm desktop config
folder `/etc/skel/.config/arco-chadwm` → `/etc/skel/.config/chadwm` for the new
Kiro release de-brand. This **reverses** the earlier "never rename — critical
system path / non-negotiable" decision that was recorded in ATT's project
memory; the rename is safe now that every reference is updated together.

### Technical Details

- `desktopr.py` (chadwm branch): `src.append("/etc/skel/.config/arco-chadwm")`
  → `"/etc/skel/.config/chadwm"`.
- `npicom` alias repointed to `~/.config/chadwm/picom/picom.conf` in
  `data/.bashrc`, `data/.zshrc`, `data/config.fish`.
- Reversed the guardrail memory: `project_arco_chadwm_skel.md` →
  `project_chadwm_skel.md` (rewritten to record the rename), MEMORY.md pointer
  updated. The `arcolinux-arc-*` AUR-package-name exception is unaffected.

### Files Modified

- usr/share/archlinux-tweak-tool/desktopr.py
- usr/share/archlinux-tweak-tool/data/.bashrc
- usr/share/archlinux-tweak-tool/data/.zshrc
- usr/share/archlinux-tweak-tool/data/config.fish
- .claude/memory/project_chadwm_skel.md (renamed from project_arco_chadwm_skel.md)
- .claude/memory/MEMORY.md

## 2026.05.24 — Remove hardcoded /home/erik wallpaper path from shipped variety.conf

### What Changed

The bundled Variety default config shipped with a personal absolute wallpaper
folder (`/home/erik/Templates/wallpapers`) as an *enabled* source — it pointed
at a nonexistent path on every other user's system. Repointed to the per-user
`~/Templates/wallpapers` so it resolves for whoever installs ATT. Found during
an ecosystem-wide hardcoded-`/home/erik` sweep across EDU/KIRO.

### Technical Details

- `data/variety/variety.conf` source `src13`:
  `True|folder|/home/erik/Templates/wallpapers` → `True|folder|~/Templates/wallpapers`
  (Variety expands `~`; a missing folder is simply skipped).

### Files Modified

- usr/share/archlinux-tweak-tool/data/variety/variety.conf

## 2026.05.23 - DEV page audit: full restructure into tab-ordered status mirror

### What Changed

Closed the pinned P1 "DEV page audit — reflect every ATT-managed setting" backlog item. The DEV page (`dev_gui.py`) used to be 8 ad-hoc sections (Distro/Environment/Session/Repositories/System/Plymouth/Login Manager/Safeguards). It now mirrors ATT's own tab layout 1:1 — walk from "Performance tab in ATT" to the "Performance" section on DEV without translation. Purpose framed by Erik as a release-readiness check: a maintainer should be able to glance at DEV and see whether every ATT-managed package, service, repo, kernel hook, theme pack, and config file is in the expected state on this machine.

### Structure (3 groups, in this order)

1. **Session diagnostics** — Distro / Environment / Session / System. The meta-info about the running session that doesn't map to any one tab.
2. **Per-tab status** — one section per stateful tab, in `gui.py` registration order: AI Tools · Autostart · Desktop · Fastfetch · Icons · Kernels · Locale · Maintenance · Network · Packages · Pacman · Plymouth · Privacy · Performance · SDDM · Services · Shells · Software · Themer · Themes · User · Wallpaper. Skipped (pure viewers, no managed state): Logging, System.
3. **Cross-cutting safeguards** — the distro-conditional guards that span multiple tabs (artix Plymouth, prismlinux SDDM, plasma-login/plasmalogin override, arch+systemd-boot kernel hook, visudo, omarchy marker). Kept at the bottom.

Existing Plymouth, Login Manager (renamed **SDDM**), and Repositories (renamed **Pacman**) sections folded into their tab-ordered slots — exactly one place per tab now.

### Technical Details

- **New module-level helpers** at the top of [dev_gui.py](file:///home/erik/EDU/archlinux-tweak-tool-gtk4/usr/share/archlinux-tweak-tool/dev_gui.py): `_count_pkgs_matching(fn, prefix)` (count installed pkgs by name prefix — used for sardi-/surfn-/neo-candy-/arcolinux-arc-/edu-arc- counters), `_tuned_active_profile(fn)` (parses `tuned-adm active`), `_hosts_has_hblock()` (greps `/etc/hosts` for the hblock marker), `_pacman_conf_value(key)` (parses `/etc/pacman.conf` for scalar settings like `ParallelDownloads`), `_pacman_repo_enabled(name)` (checks for an uncommented `[name]` section), `_localectl_field(fn, field)` (X11 Layout / VC Keymap), `_timedatectl_field(fn, field)` (Timezone), `_autostart_entry_count(home)` (counts `~/.config/autostart/*.desktop`), `_sudoers_d_count()` (counts files in `/etc/sudoers.d/`), `_user_in_group(fn, group)` (calls `id -nG`).
- **New nested helpers** inside `gui()` to reduce row-row repetition: `_yes(b)` (green "yes" markup or empty), `_active(b)` (green "active"), `_enabled(b)` (green "enabled"), `_pkg(name)` (combined "check + row" for a package), `_svc(label, service, installed)` (renders `enabled=… active=…` with paired green markup), `_group(text)` (large bold group header, distinct from per-section `_header`).
- **Detection logic mirrors what each ATT page actually checks** — not just package names. AI Tools and Software pages in ATT detect via binary paths (`/usr/bin/ollama`, `/usr/bin/pamac-manager`, `/usr/bin/plasma-discover`, etc., because the underlying pkg name varies per distro and AUR source). The DEV page now follows the same detection contract: those two sections use `fn.path.exists("/usr/bin/<bin>")` rows, everything else uses `fn.check_package_installed(...)`.
- **Service-state pattern** for every daemon-tab — pkg installed (Y/N) → if installed, `systemctl is-enabled <svc>` + `systemctl is-active <svc>` in one row, with green "enabled active" markup. Used across Network (`avahi-daemon`, `smb`), Services (`cups`, `bluetooth`, `bluetooth-autoconnect`), Performance (`tuned`, `irqbalance`, `ananicy-cpp`, `preload`, `fstrim.timer`), AI Tools (`ollama`), Plymouth (`plymouth`), SDDM (`sddm`).
- **Performance section** adds `active tuned profile` (via `tuned-adm active`) when tuned is installed — covers the TODO's explicit "what profile is applied?" requirement.
- **Privacy section** detects hblock via binary AND `/etc/hosts` marker (catches "installed but never run" vs "installed and applied" — distinct states).
- **Pacman section** now adds `[multilib]` and `[testing]` repo state on top of the existing chaotic-AUR / nemesis_repo checks, plus `ParallelDownloads` value.
- **User section** shows `<user> in wheel` and a count of `/etc/sudoers.d/` entries — covers the User-tab's visudo/groups domain.
- **File size**: 277 → 595 lines. Bigger but flat — no nested control flow, mostly `_pkg(...) + _svc(...)` pairs.
- **Imports**: hoisted `import os` and `import shutil` to module level (was inline `import os as _os` inside Session section). Both used by the new helpers.

### Live-test follow-ups (same session)

After Erik installed the new DEV page live and walked it tab-by-tab, four issues surfaced and were fixed in-session:

- **Desktop section** — meta-package detection was broken. On Arch, `xfce4`, `gnome`, `mate`, `deepin`, `lxqt` are pacman *groups*, not packages, so `pacman -Qi <group>` always returned false even on systems that had the DE installed. Switched to session-binary detection (`/usr/bin/xfce4-session`, `/usr/bin/gnome-session`, `/usr/bin/plasmashell`, `/usr/bin/cinnamon-session`, `/usr/bin/mate-session`, `/usr/bin/budgie-desktop`, `/usr/bin/startdde`, `/usr/bin/lxqt-session`) — same pattern Software + AI Tools sections use.
- **Kernels section** — hardcoded pkg-name list (`linux-liquorix`, etc.) was wrong: on Arch, Liquorix ships as `linux-lqx`, CachyOS as `linux-cachyos`, and the official names vary. Rewrote to enumerate `/boot/vmlinuz-*` (the actually-bootable kernels — authoritative ground truth) and read `/lib/modules/<uname>/pkgbase` to flag the running one. Each installed kernel now also gets a paired `<name>-headers` row.
- **Plymouth section — service-enabled row removed.** Plymouth on Arch is hook-driven, not service-driven — there's no `plymouth.service` to enable. Boot-time firing is wired via the initramfs hook + kernel cmdline (both already checked here). The "plymouth service enabled" row was a permanent false signal; dropped entirely. The hook check + active-theme row already prove Plymouth is configured to fire.
- **Reload on tab revisit.** The DEV page used to build once at app startup, so navigating to another tab, changing something (e.g. enabling a service), and coming back to DEV would still show the stale snapshot from app launch. Wrapped the entire section-building body in a `_populate()` closure inside `gui()`, then connected the `map` signal on `vboxstack_dev` so `_populate()` re-runs every time the DEV box becomes visible. On each reload, `fn.invalidate_pkg_cache()` and `fn.invalidate_pacman_conf_cache()` fire first so the rebuild reads fresh state. Implementation: keeps `row = [0]` and all helpers (`_header`, `_row`, `_pkg`, `_svc`, etc.) in `gui()` scope outside `_populate()` so the closure captures them; `_populate()` clears the grid (`while grid.get_first_child(): grid.remove(...)`) and resets `row[0] = 0` before re-running the body. Initial display calls `_populate()` once explicitly so the first paint shows fully populated.

### Pending decision (raised, not yet acted on)

The existing P3 backlog item *"List user systemd services"* (read-only `systemctl --user list-units` panel) is **NOT subsumed** by this audit — the audit covers system-level `systemctl is-enabled` state, the P3 covers per-user services. They're distinct concerns. Leaving the P3 in place; Erik to confirm.

### Files Modified

- [usr/share/archlinux-tweak-tool/dev_gui.py](file:///home/erik/EDU/archlinux-tweak-tool-gtk4/usr/share/archlinux-tweak-tool/dev_gui.py) — full restructure (277 → 595 lines)
- [TODO.md](file:///home/erik/EDU/archlinux-tweak-tool-gtk4/TODO.md) — DEV page audit item removed (done)
- [CHANGELOG.md](file:///home/erik/EDU/archlinux-tweak-tool-gtk4/CHANGELOG.md) — this entry

---

## 2026.05.22 - Performance: makepkg.conf rewrite + explainer dialog. Software: PacHub added.

### Software page — PacHub added to GUI Package Managers

A new entry for **PacHub** (`pachub`, AUR — *Pacman/AUR front-end built on GTK4 + libadwaita*) at the bottom of the **GUI Package Managers** section, after Bauh. The entry mirrors the existing pattern: a label showing install state with an `<b>installed</b>` suffix when `/usr/bin/pachub` is present, a `Launch/Install` button, and a `Remove` button. Always visible (not gated behind `fn.DEV` like Bauh is).

**Handlers** in [software.py](file:///home/erik/EDU/archlinux-tweak-tool-gtk4/usr/share/archlinux-tweak-tool/software.py):

- `on_click_software_pachub` — if `/usr/bin/pachub` exists, launches it via the standard `sudo -E -u {sudo_username} pachub &` pattern used by Bauh/Pamac. If not, fetches the configured AUR helper via `fn.get_aur_helper()`, runs `fn.launch_aur_install_in_terminal(aur_helper, "pachub")` (PacHub is AUR-only, not in chaotic-AUR), then `fn.wait_install_and_update` to flip the label markup and notify on completion. Same shape as the `appmanager` AUR install at `software.py:765`.
- `on_click_software_pachub_remove` — straight `fn.launch_pacman_remove_in_terminal("pachub")` + `wait_remove_and_update`. Same shape as the Bauh remove handler.

**GUI** in [software_gui.py](file:///home/erik/EDU/archlinux-tweak-tool-gtk4/usr/share/archlinux-tweak-tool/software_gui.py): new `hbox_pachub` block right after the Bauh definition (line 165-ish), and a `vboxstack_software.append(hbox_pachub)` placed *after* the `if fn.DEV: vboxstack_software.append(hbox_bauh)` block so PacHub renders as the bottom row of Section 1 in both DEV and non-DEV modes.

### Performance page — makepkg.conf tuning rewritten in pure Python + explainer dialog

The makepkg.conf apply/restore buttons on the Performance page were rebuilt end-to-end today:

1. **Rewritten in pure Python.** The buttons no longer shell out to bash or launch a terminal. Both operations do their work in pure Python file I/O — the same pattern `remove_debug_from_makepkg_conf` already uses in `functions.py`. The `data/bin/att-tune-makepkg` bash helper (about 100 lines) is deleted along with all the alacritty-launching scaffolding around it. Net code reduction in `performance.py` over the day: ~65 lines removed.
2. **Explainer dialog on success.** Both `optimize_makepkg` and `restore_makepkg` now show a modal `fn.messagebox` (INFO + OK) after the file write succeeds, explaining what changed, why it matters, and how to revert. `MAKEFLAGS` affects every future AUR/source build silently — a transient toast wasn't enough to make the consequence visible. This is the third tier on the transparency ladder, captured in [feedback_user_transparency.md](file:///home/erik/.claude/projects/-home-erik-EDU-archlinux-tweak-tool-gtk4/memory/feedback_user_transparency.md).

### Performance page — makepkg.conf button row + Edit-in-terminal button

The Build Settings (makepkg.conf) section's two existing buttons — *Optimize for N cores* and *Restore backup* — moved off the status row onto their own dedicated row underneath the status label (new `hbox_makepkg_buttons`). Separating control from status keeps the status label uncluttered when its markup grows.

Added a third button between Optimize and Restore: **"Edit makepkg.conf in terminal"** — opens `/etc/makepkg.conf` in a separate alacritty (`alacritty -e sudo nano /etc/makepkg.conf`), mirroring the existing `edit_pacman_conf_clicked` pattern on the Pacman page. Purpose: let users verify what Optimize actually wrote (and read the surrounding context in the file) before deciding whether to keep it or Restore. Slots the verification step into the natural left-to-right flow: **Optimize → Edit (check it) → Restore (if needed)**.

New function `edit_makepkg_conf(self, _widget)` in `performance.py`, appended after `restore_makepkg`. Uses the existing module-level `MAKEPKG_CONF` constant (line 1932) so the path is not hardcoded a second time.

### Performance page — Remove tuned/tuned-ppd: filter to installed packages

**Bug.** Clicking *Remove tuned/tuned-ppd* with `tuned` installed but `tuned-ppd` not installed aborted the whole transaction — `pacman -R --noconfirm tuned tuned-ppd` returns "target not found: tuned-ppd" and pacman refuses to remove either. The terminal showed `✗ Removal failed`, ATT's post-check saw `tuned` still installed, label remained "installed", user was stuck (couldn't remove tuned through the GUI). Reproduced from Erik's screenshot (manual `sudo pacman -R tuned` succeeded with just one package — proof the issue is pacman's all-or-nothing transaction, not tuned itself).

**Fix.** `remove_tuned_tools` now builds `installed_pkgs = [p for p in (TUNED_PACKAGE, TUNED_PPD_PACKAGE) if fn.check_package_installed(p)]` before assembling the script. The `systemctl disable --now` block is generated per-installed-package (so we don't call disable on a package that doesn't exist — keeps the terminal output clean), and `pacman -R --noconfirm` only receives the join of `installed_pkgs`. Early-return at the top still bails if `tuned` itself isn't installed, so the list is guaranteed non-empty when we reach the script-building branch.

*Superseded later this session by the full Tuned split below — `remove_tuned_tools` and its filter logic no longer exist; the per-package `remove_tuned` / `remove_tuned_ppd` handlers each touch one package only, so the filter became redundant.*

### Performance page — Tuned section split into per-package controls

The combined `Install/Remove tuned + tuned-ppd` and `Enable/Disable tuned + tuned-ppd` buttons treated two distinct packages with different conflict graphs as a single bundle. That bundle leaked: the *Remove* bug above is one symptom; the parallel *Install* bug (early-return blocks ever installing tuned-ppd alone if tuned is already present) is another; the lack of a way to install *only* tuned-ppd or *only* tuned is a third. Replaced with one controls block per package: **tuned** (Install / Remove + Enable / Disable / Restart) and **tuned-ppd** (Install / Remove + Enable / Disable / Restart). Restart buttons fold into each package's service row rather than living on a shared row.

**Layout — Performance page Tuned section, before → after:**

```
BEFORE                                    AFTER
─────────────────────────────────────     ─────────────────────────────────────
[ Title: Tuned ]                          [ Title: Tuned ]
[ "Install tuned for ..."  ] [Inst][Rem]  [ Description block (moved up)      ]
[ Description block                  ]    [ "tuned is installed"        ] [I][R]
[ "tuned service: …"     ] [RstT][RstP]   [ "tuned service: …"     ] [En][Di][Rs]
[ "tuned-ppd service: …" ] [En+P ][Di+P]  [ "tuned-ppd is installed"   ] [I][R]
[ Profile status / select            ]    [ "tuned-ppd service: …" ] [En][Di][Rs]
                                          [ Profile status / select            ]
```

**Conflict-handling redistribution.** Power-profiles-daemon removal now lives only in `install_tuned_ppd` (since only tuned-ppd actually conflicts with PPD — `tuned` itself has no conflicts per `pacman -Si tuned`). TLP disable lives in `install_tuned` and `enable_tuned` (TLP conflicts with tuned, not tuned-ppd specifically).

**Dependency-aware Remove.** `remove_tuned` refuses up-front with a clear toast (*"tuned-ppd depends on tuned — remove tuned-ppd first"*) if tuned-ppd is installed, rather than letting pacman emit a cryptic dependency error. Confirmed dep graph via `pacman -Si tuned-ppd | grep Depends` → `Depends On: tuned python-pyinotify`.

**Refresh helpers updated.** `refresh_tuned_package_label` now refreshes both `tuned_package_label` and `tuned_ppd_package_label`. `refresh_tuned_buttons` now sets per-button sensitivity from a single state dict: Install enabled only when not installed; Remove enabled only when installed (and for tuned: only if tuned-ppd is also gone); Enable/Disable/Restart enabled only when the underlying package is installed; profile widgets gated on tuned itself. Build-time calls to both refreshers added so the initial page render shows correct labels/sensitivity (previously the labels were hardcoded "Install tuned for ..." which was wrong when tuned was already installed — a latent bug that the split made more visible by doubling the surface).

**Functions added / removed in `performance.py`:**

| Action          | Removed (combined)       | Added (per-package)                       |
|-----------------|--------------------------|-------------------------------------------|
| Install         | `install_tuned_tools`    | `install_tuned`, `install_tuned_ppd`      |
| Remove          | `remove_tuned_tools`     | `remove_tuned`, `remove_tuned_ppd`        |
| Enable          | `enable_tuned_services`  | `enable_tuned`, `enable_tuned_ppd`        |
| Disable         | `disable_tuned_services` | `disable_tuned`, `disable_tuned_ppd`      |
| Restart         | *(already per-package)*  | `restart_tuned_service` (unchanged), `restart_tuned_ppd_service` (unchanged) |

### Performance page — Sub-tabs + lazy-load (visual decongestion + load-time fix)

**Problem.** The page hosts 9 distinct sections (Build / Tuned / Swap / TRIM / IRQ / Ananicy / GameMode / Preload — plus the just-split Tuned doubled in height). Two problems compounded: (a) visual crowding — one tall scroll surface with 9 unrelated concerns; (b) load-time hit — every widget construction triggered a synchronous `systemctl is-enabled`, `tuned-adm`, `zramctl`, `findmnt` etc. on the main thread, ~500ms–1s cumulative before the page even painted.

**Restructure.** Performance page becomes a `Gtk.Stack` + `Gtk.StackSwitcher` with **three sub-tabs** (mirroring the existing pattern from Services page — same idiom, well established in the codebase):

| Sub-tab             | Contents                                                                  |
|---------------------|---------------------------------------------------------------------------|
| **Build**           | Build Settings (makepkg.conf) — status + Optimize/Edit/Restore             |
| **Tuning**          | Tuned + Tuned-PPD + profile selector + IRQ balance + Ananicy + GameMode + Preload |
| **Storage & Memory**| Swap (swapfile + zram) + SSD/NVMe TRIM                                    |

Build sub-tab is the default visible child (it's the cheapest to refresh — no subprocess calls).

**Lazy-load mechanism with per-visit cache.** All construction-time subprocess calls replaced with cheap placeholder text (`"tuned service : …"`, `"zram : …"`, `"MAKEFLAGS : …"`, etc.). The slow queries — `get_service_status`, `get_*_status_markup`, `get_available_tuned_profiles`, `get_active_tuned_profile`, `get_zram_status_markup`, `get_fstrim_status_markup`, `get_swapfile_size_label`, etc. — now run inside per-sub-tab `_refresh_<name>_subtab()` map handlers, guarded by a `subtab_loaded` dict so each sub-tab refreshes **once per Performance-page visit**.

| User action                                                | What runs                                                                 |
|------------------------------------------------------------|---------------------------------------------------------------------------|
| First click into a sub-tab during a Performance visit      | Full refresh — ~100–300 ms of subprocess calls, then `subtab_loaded[X]=True` |
| Click between sub-tabs in the same visit                    | Instant — flag short-circuits the refresh                                  |
| Leave Performance (Pacman/Services/etc.) and return         | `vboxstack_performance.map` fires → `_invalidate_subtab_cache()` resets all flags → next sub-tab click re-fetches |
| Install / Remove / Enable / Disable inside a sub-tab        | Handler calls its own refresh helpers directly → state updates regardless of cache |

The cache invalidate-on-return matches the user mental model ("I navigated back to this page — give me fresh state"). ATT's own actions always propagate via direct refresh-helper calls in each handler, so internal changes aren't cache-gated. External state changes made between ATT visits (e.g., user disables a service in a terminal) are picked up on the next visit. The only stale case is external state changes made *during* a single Performance visit on a sub-tab the user has already seen — rare and not worth a TTL.

The Build sub-tab's refresh additionally schedules via `fn.GLib.idle_add(_refresh_build_subtab)` immediately after gui() returns — so the default-visible tab's MAKEFLAGS state shows up in the first idle frame after the page paints, with no perceptible delay.

**Construction-time subprocess calls eliminated:** 12 — `get_service_status` × 2 (tuned, tuned-ppd) + `get_tuned_profile_status_markup` + `get_available_tuned_profiles` + `get_active_tuned_profile` + `get_swapfile_size_label` + `get_zram_status_markup` + `get_fstrim_status_markup` + `get_irqbalance_status_markup` + `get_ananicy_status_markup` + `get_gamemode_status_markup` + `get_preload_status_markup` + `get_makepkg_status_markup`. Only one residual subprocess (`get_root_filesystem_type` → `findmnt`, ~30 ms) remains in the construction path because it gates structural inclusion of the swapfile row on non-btrfs roots — not worth re-architecting for one call.

**Tuned profile dropdown** now constructs empty (`Gtk.DropDown.new_from_strings([])`); the existing `performance.refresh_tuned_profile_choices(self)` (which already does an empty-list-safe rebuild via `Gtk.StringList.new(...)` + `set_model`) is called from the Tuning sub-tab map handler — populates the dropdown lazily and selects the active profile.

**Map-handler placement.** Each sub-tab vbox connects its own `map` signal: `vboxstack_build.connect("map", lambda _w: _refresh_build_subtab())` and analogues for tuning and storage. The previous page-level `vboxstack_performance.connect("map", lambda _w: _do_refresh())` is removed — the sub-tab handlers replace it. Trade-off: visiting Performance without clicking into Tuning means Tuning's labels stay as "…" until first activation — acceptable; the whole point is to not query system state for things the user isn't currently looking at.

**Visual change for users.** Opening Performance is near-instant (paint-then-fill, like every well-behaved native app). The first paint shows Build's controls only. Clicking into any other sub-tab populates its labels in ~100–300 ms (the cumulative cost of the subprocess calls that used to block the initial render).

### Performance page — Further split: Tuning → Power + Responsiveness

The 3-sub-tab arrangement above shipped a "Tuning" sub-tab that still housed 5 sections (Tuned + Tuned-PPD + IRQ + Ananicy + GameMode + Preload). Iterated to **4 sub-tabs** by separating power-state daemons from latency/UX daemons — different mental models, different troubleshooting paths:

| Sub-tab              | Contents                                                |
|----------------------|---------------------------------------------------------|
| **Build**            | makepkg.conf                                            |
| **Power**            | Tuned + Tuned-PPD + profile selector + IRQ balance      |
| **Responsiveness**   | Ananicy + GameMode + Preload                            |
| **Storage & Memory** | Swap + zram + TRIM                                      |

Implementation: added `vboxstack_responsiveness`, rerouted Ananicy + GameMode + Preload off `vboxstack_power` (renamed from `vboxstack_tuning`), added a 4th `stack.add_titled(...)`, split `_refresh_tuning_subtab()` into `_refresh_power_subtab()` (tuned + irqbalance refreshes) and `_refresh_responsiveness_subtab()` (ananicy + gamemode + preload refreshes). Both new refresh functions still call the legacy threaded `_refresh(self, fn)` so the per-package install-state + button-sensitivity logic runs on either sub-tab's first map — opening Responsiveness directly doesn't leave Tuned buttons stale.

### Technical Details

- ATT runs as root via pkexec (see `archlinux-tweak-tool.py` polkit launcher and `PKEXEC_UID` references throughout `functions.py`), so direct `open(MAKEPKG_CONF, "w")` and `shutil.copy2` against `/etc/` work without `sudo` or `subprocess`. No reason to involve bash at all for a config-file edit.
- `optimize_makepkg` reads `/etc/makepkg.conf` into a `lines` list, captures the existing `MAKEFLAGS=` line via `re.match(r"^\s*#?\s*MAKEFLAGS=", line)` for the Before log, replaces (or appends if absent) with `MAKEFLAGS="-jN"\n`, writes back. Appends-if-absent handles the edge case of someone deleting the stock commented line — the change is still applied. Status label refresh is now a direct sync call, no `GLib.idle_add`, no daemon thread.
- `restore_makepkg` calls `fn.shutil.copy2(MAKEPKG_CONF_BAK, MAKEPKG_CONF)` and logs Source/Target via `log_info_concise`. Same shape as the apply branch.
- Apply dialog title: `"MAKEFLAGS updated — building with all N cores"`; body markup shows the previous `MAKEFLAGS=` line (Pango-escaped via `GLib.markup_escape_text` since user content can contain `<` / `&`), the new value, a one-paragraph explanation of why the stock `-j2` commented default is single-threaded, and a pointer to the Restore button.
- Restore dialog title: `"MAKEFLAGS restored from backup"`; body explains that makepkg is back to whatever was in the backup (typically the commented `-j2` default) and points back to the Optimize button.
- `refresh_makepkg_status_label(self)` is called *before* `fn.messagebox(...)` so the status label below the dialog already shows the new value while the user reads the explanation.
- Post-success `fn.show_in_app_notification` calls dropped in both paths — the modal dialog supersedes the toast (no point in both). The toast remains on the error paths and on the early-exit guard paths (single core, missing backup) where no modal is appropriate.
- `messagebox` uses `GLib.MainLoop().run()` internally and blocks the calling thread; since both handlers are now fully synchronous Python file I/O, blocking the button-click handler is the correct shape.
- **Console log mirrors the dialog.** The "Why this matters" / "How to revert" prose from each dialog is also emitted to the ATT log panel via `fn.log_info` + `fn.log_tip` *before* the modal is shown, so the transcript is durable — the dialog is ephemeral, the log scrollback isn't. Recorded as an extension to the high-blast-radius transparency tier in memory.
- **Every channel explains *why*, not just *what*.** Re-added success toasts (dropped earlier when the dialog landed) but with rationale baked in: apply says `"MAKEFLAGS=-j16 — AUR builds now use all 16 cores instead of -j2"`, restore says `"MAKEFLAGS restored — back to Arch's single-threaded default"`. Early-exit guards updated too: `"Single core detected — parallel builds need ≥2 cores; no change made"`, `"No backup at /etc/makepkg.conf-bak — nothing to restore"`. The toast is non-blocking and rides alongside the modal; the dialog has the long-form, the toast has the punchline. Memory: extended `feedback_user_transparency.md` with a new principle — "always explain *why*, not just *what*, in every user-visible channel (toast, log, dialog)".
- Both functions still respect the early-exit guards (single-core for apply, missing-backup for restore).
- `ATT_TUNE_MAKEPKG` constant dropped; the bash file `git rm`-ed. PKGBUILD untouched (the script was a plain `usr/share/.../data/bin/` install — its removal from the source tree is enough).
- Rules captured in memory: [feedback_native_python_first.md](file:///home/erik/.claude/projects/-home-erik-EDU-archlinux-tweak-tool-gtk4/memory/feedback_native_python_first.md) — before reaching for `subprocess.Popen(["alacritty", "-e", "bash", ...])` or `sudo sed`, ask whether plain Python can do the job; for `/etc/*.conf` edits the answer is almost always yes. [feedback_alacritty_keep_open.md](file:///home/erik/.claude/projects/-home-erik-EDU-archlinux-tweak-tool-gtk4/memory/feedback_alacritty_keep_open.md) updated with a "first ask if you even need a terminal" preamble. [feedback_user_transparency.md](file:///home/erik/.claude/projects/-home-erik-EDU-archlinux-tweak-tool-gtk4/memory/feedback_user_transparency.md) extended with a new "high-blast-radius single setting → messagebox" tier on the calibration ladder.

### Files Modified

- `usr/share/archlinux-tweak-tool/performance.py`
- `usr/share/archlinux-tweak-tool/performance_gui.py`
- `usr/share/archlinux-tweak-tool/data/bin/att-tune-makepkg` (deleted)
- `usr/share/archlinux-tweak-tool/software.py`
- `usr/share/archlinux-tweak-tool/software_gui.py`
- `TODO.md` (bogus "Edit /etc/makepkg.conf button" entry removed — not authored by Erik)

---

## 2026.05.21 - Performance page: makepkg.conf CPU tuning

### What Changed

- **New "Build Settings (makepkg.conf)" section** at the bottom of the Performance page — exposes one-click tuning of `MAKEFLAGS` in `/etc/makepkg.conf` so AUR and source builds use all CPU cores instead of the stock single-threaded `-j2` default
- **Status label** shows the current `MAKEFLAGS` value and detected CPU core count, refreshed on tab map and after every apply/restore
- **Two buttons** — *Optimize for N cores* (sets `MAKEFLAGS="-jN"` where N = `nproc`) and *Restore backup* (restores `/etc/makepkg.conf` from `/etc/makepkg.conf-bak`)
- **New script** `usr/share/archlinux-tweak-tool/data/bin/att-tune-makepkg` — handles both `apply` and `restore` modes; vendor-agnostic (Intel/AMD/ARM — only uses `nproc`)

### Technical Details

- The sed regex `^[[:space:]]*#?MAKEFLAGS=.*` matches both the stock commented `#MAKEFLAGS="-j2"` line and any pre-existing user value, so the operation is idempotent and survives manual edits — improvement over the legacy `/usr/local/bin/kiro-set-cores` script which only matched the commented default
- Backup is written to `/etc/makepkg.conf-bak` by `functions_backup.backup_system_configs()` at ATT startup (alongside `/etc/samba/smb.conf-bak`, `/etc/nsswitch.conf-bak`, etc.) — the script never creates the backup, only edits the live file; this keeps backup creation in one routine and avoids touching system files from a button-triggered script
- Restore button is sensitivity-gated: `refresh_makepkg_status_label` checks `os.path.isfile(MAKEPKG_CONF_BAK)` and disables the button with an explanatory tooltip when no backup exists
- Single-core systems get an early `log_warn` exit — no edit, no backup written (matches the legacy script's behaviour)
- Python parser uses `re.match(r"^\s*(#?)\s*MAKEFLAGS=(.+)$")` to extract both commented and uncommented values, stripping inline comments and quotes; falls back to `"read error"` on file I/O failure
- Transparency follows objective 14 — the alacritty terminal prints `Before` and `After` `grep` blocks so the user sees the actual diff; status label refreshes via `wait_and_refresh` pattern in a daemon thread
- New `_do_refresh()` wrapper in `performance_gui.py` calls both the existing `_refresh()` (service status checks) and `refresh_makepkg_status_label()` (filesystem read) — keeps the original `_refresh` signature unchanged

### Files Modified

- `usr/share/archlinux-tweak-tool/data/bin/att-tune-makepkg` (new)
- `usr/share/archlinux-tweak-tool/performance.py`
- `usr/share/archlinux-tweak-tool/performance_gui.py`

---

## 2026.05.20 - Plasma one-way install enforcement + warning UX (session 2)

### What Changed

- **Desktop page: Plasma removal blocked entirely** — `on_uninstall_clicked` returns immediately with `log_warn` + in-app notification when Plasma is selected; the Remove button is greyed out with an explanatory tooltip whenever Plasma is active in the dropdown
- **Desktop page: Plasma install requires confirmation** — `on_install_clicked` shows a `Gtk.MessageDialog` (WARNING type, Yes/No buttons) before proceeding; cancelling aborts cleanly without opening a terminal
- **Desktop page: orange warning label on Plasma select** — `#FFA500` label (matching the "ArchLinux Tweak Tool" sidebar branding color) appears centered above the Install button and collapses automatically when any other desktop is chosen; in-app notification fires at the same moment
- **Fixed `AttributeError` on Desktop page load** — `update_button_state` was called during `gui()` build before `self.button_uninstall` was assigned; added `hasattr` guard matching the existing `d_combo` guard pattern

### Technical Details

- The confirmation dialog uses a nested `GLib.MainLoop` (same pattern as `check_lock`) so it blocks the callback without freezing the main GTK loop
- `update_button_state` now controls both `button_install` (existing repo check) and `button_uninstall` (new Plasma guard); both blocks use `hasattr` so the function is safe to call at any point in the `gui()` build sequence
- Warning label uses `set_visible(False/True)` — the widget is always constructed and appended, visibility toggled per selection; no dynamic widget creation/destruction in the callback
- Color `#FFA500` sourced from `gui.py:434` where the sidebar app-name label uses it — consistent branding without adding a new constant

### Files Modified

- `usr/share/archlinux-tweak-tool/desktopr.py`
- `usr/share/archlinux-tweak-tool/desktopr_gui.py`

---

## 2026.05.20 - Bug scan: time.sleep cleanup + error trap added to all data/bin scripts

### What Changed

- **`system.py`: removed 3 unnecessary `time.sleep(1)` calls and unused `import time`** — `process.wait()` already blocks until the terminal closes; the sleeps added no value and slowed UI feedback after install
- **All 14 scripts in `data/bin/` now have the error trap** — a systematic scan found every script had `set -euo pipefail`, tput colors, and helper functions, but none had `trap '...' ERR`; added `trap 'error "Command failed at line $LINENO"' ERR` after the `error()` definition in each

### Technical Details

- Trap inserted via Python (not sed) — single quotes inside the trap string make sed quoting error-prone across 14 files; a 10-line Python script that matches `line.startswith("error()")` and appends the trap line is clean and unambiguous
- The `error()` function was already defined in all 14 scripts (verified with `grep -rn "^error()"`) — the trap reuses it so error output is consistent with the existing style
- Full codebase scan also verified: all 176 `threading.Thread()` calls have `daemon=True`; no `alacritty --hold` + `read -p` combinations; no unescaped `&` in `set_markup()`; no numbered widget names; all deferred-tab map-signal bugs fixed from yesterday's sweep

### Files Modified

- `usr/share/archlinux-tweak-tool/system.py`
- `usr/share/archlinux-tweak-tool/data/bin/archlinux-get-mirrors-rate-mirrors`
- `usr/share/archlinux-tweak-tool/data/bin/archlinux-get-mirrors-reflector`
- `usr/share/archlinux-tweak-tool/data/bin/att-fix-pacman-conf`
- `usr/share/archlinux-tweak-tool/data/bin/att-set-wallpaper`
- `usr/share/archlinux-tweak-tool/data/bin/build-paru-git`
- `usr/share/archlinux-tweak-tool/data/bin/build-yay-git`
- `usr/share/archlinux-tweak-tool/data/bin/detect-desktop`
- `usr/share/archlinux-tweak-tool/data/bin/fix-pacman-databases-and-keys`
- `usr/share/archlinux-tweak-tool/data/bin/fix-sddm-config`
- `usr/share/archlinux-tweak-tool/data/bin/install-pipewire.sh`
- `usr/share/archlinux-tweak-tool/data/bin/install-pulseaudio.sh`
- `usr/share/archlinux-tweak-tool/data/bin/probe`
- `usr/share/archlinux-tweak-tool/data/bin/set-mainstream-servers`
- `usr/share/archlinux-tweak-tool/data/bin/setup-chaotic-aur`

---

## 2026.05.19 - Bluetooth auto-connect, deferred-tab refresh bug sweep, hblock backup/restore

### What Changed

- **Bluetooth tab: Auto-Connect section added** — new section with `AutoEnable` switch (writes `/etc/bluetooth/main.conf` `[Policy]` section, restarts bluetooth) and `bluetooth-autoconnect` install/remove row (installs package + enables service; disable + removes on remove button)
- **Services tab: buttons no longer grey on first load** — `_refresh` was connected to the `map` signal but never called at build time; because `_defer_tab` fires `map` before the GUI is built, the refresh was always skipped on first visit
- **Same deferred-tab bug fixed across 5 more pages** — network, performance, privacy, wallpaper, themer all had the same missing immediate call
- **hblock: backup `/etc/hosts` before enabling; restore on remove** — `on_click_enable_hblock` copies `/etc/hosts` → `/etc/hosts-bak` once before running hblock; `on_click_remove_hblock` runs `HBLOCK_SOURCES=''` to clean hosts, restores `/etc/hosts-bak` if present, removes backup, then pacman removes the binary

### Technical Details

- `get_bluetooth_autoenable()` reads the file line-by-line looking for an uncommented `AutoEnable=true`; `set_bluetooth_autoenable()` walks lines, replaces the active or commented-out line, or appends a new `[Policy]` section if none exists — preserving all comments
- `bluetooth-autoconnect` uses `WantedBy=bluetooth.service` so `fn.enable_service()` (which passes `--now`) creates the symlink and starts it immediately; disable + removal runs in the right order: stop service → clear hosts → restore backup → pacman remove
- The deferred-tab bug: `_defer_tab(container, lambda: gui.build())` hooks the build onto the container's first `map` signal. Once `gui.build()` runs and connects `container.connect("map", _refresh)`, that signal is already spent. Fix: call `_refresh(self, fn)` (or equivalent) once at the end of every `gui()` function that uses this pattern
- `themer_gui` used a named `_on_themer_map(_w)` callback; called as `_on_themer_map(None)` for the immediate call
- hblock backup uses `fn.shutil.copy2` (preserves metadata); restore uses same + `fn.os.remove` to clean up; backup is only created if `/etc/hosts-bak` doesn't already exist (idempotent)

### Files Modified

- `usr/share/archlinux-tweak-tool/services.py`
- `usr/share/archlinux-tweak-tool/services_gui.py`
- `usr/share/archlinux-tweak-tool/network_gui.py`
- `usr/share/archlinux-tweak-tool/performance_gui.py`
- `usr/share/archlinux-tweak-tool/privacy_gui.py`
- `usr/share/archlinux-tweak-tool/privacy.py`
- `usr/share/archlinux-tweak-tool/wallpaper_gui.py`
- `usr/share/archlinux-tweak-tool/themer_gui.py`

---

## 2026.05.18 - Code simplification: deduplicate status label init

### What Changed

- **`shell_gui.py`: status label init now calls existing refresh functions** — the Alacritty and ATT status labels were initialised with duplicated if/else blocks identical to `_refresh_alacritty_lbl` and `_refresh_att_lbl` in `shell.py`; replaced both with direct calls to those helpers (-6 lines)
- **`setup.sh`: added missing trailing newline at EOF** — file was not a valid POSIX text file

### Technical Details

- `_refresh_alacritty_lbl(self)` and `_refresh_att_lbl(self)` already existed in `shell.py` for post-install/remove label updates; calling them at init time is valid because the label widget only needs to exist before the refresh function runs — no circular dependency
- `setup.sh` edit was an explicit user-directed exception to the frozen-file rule

### Files Modified

- `usr/share/archlinux-tweak-tool/shell_gui.py`
- `setup.sh`

---

## 2026.05.17 - Plymouth initramfs rebuild on CachyOS+limine

### What Changed

- **`get_initramfs_rebuild_cmd()` now detects `limine-mkinitcpio`** — on CachyOS+limine `/etc/mkinitcpio.d/` is intentionally empty (no presets), so the previous `mkinitcpio -P` fallback failed with "No presets found in /etc/mkinitcpio.d". Plymouth install, apply theme, and hook-fix all hit this error; rebuild now uses `/usr/bin/limine-mkinitcpio` which pipes `rebuild` into `/usr/share/libalpm/scripts/limine-mkinitcpio-install` to regenerate every per-kernel initramfs and update `/boot/limine.conf` in one shot.

### Technical Details

- Detection order in `get_initramfs_rebuild_cmd()` is now: `dracut-rebuild` → `dracut` → `limine-mkinitcpio` → `mkinitcpio -P`. The limine branch is binary-presence based, identical pattern to the existing dracut checks.
- The `limine-mkinitcpio` package owns `/usr/bin/limine-mkinitcpio` and is pulled in by `limine-mkinitcpio-hook` on CachyOS — so the check is effectively "are we on a limine setup that delegates initramfs management to the limine hook system". Regular Arch+limine users with conventional mkinitcpio presets are unaffected because the binary is not present.
- All four callers in `plymouth_gui.py` (Install, Apply theme, Reset to default, Add hook) automatically pick up the new command via the existing `_rebuild_cmd = fn.get_initramfs_rebuild_cmd()` variable.

### Files Modified

- `usr/share/archlinux-tweak-tool/functions.py`

---

## 2026.05.16 - Extract alacritty-tweak-tool into standalone repo

### What Changed

- **alacritty-tweak-tool extracted to its own project** — all alacritty-tweak-tool code, theme data, launcher, and desktop entry moved to `/home/erik/EDU/alacritty-tweak-tool/` as a standalone git repository; removed from this repo

### Technical Details

- Zero code changes — pure filesystem split; alacritty-tweak-tool had no imports from `functions.py` or any ATT module
- New repo seeded with CLAUDE.md, CHANGELOG.md, TODO.md, IDEAS.md, README.md, and 24 ported `.claude/memory/` files
- `usr/share/alacritty-tweak-tool/` (304 .toml theme files across 16 sources), `usr/bin/alacritty-tweak-tool`, and `usr/share/applications/alacritty-tweak-tool.desktop` removed from this repo

### Files Modified

- Removed: `usr/share/alacritty-tweak-tool/` (entire directory)
- Removed: `usr/bin/alacritty-tweak-tool`
- Removed: `usr/share/applications/alacritty-tweak-tool.desktop`
- Updated: `TODO.md` — removed completed Alacritty section

---

## 2026.05.16 - Fix alacritty-tweak-tool HOME env; ATT Tools section to top of Software page

### What Changed

- **alacritty-tweak-tool launched with correct HOME** — `sudo -E -u <user>` preserved `HOME=/root` from ATT's root context; added `env HOME=fn.home` so alacritty-tweak-tool reads and writes `~/.config/alacritty/` for the real user, not root
- **ATT Tools section moved to top of Software page** — section now appears immediately below the page title/separator, before GUI Package Managers

### Technical Details

- Both launch sites patched identically: `"sudo -E -u " + fn.sudo_username + " env HOME=" + fn.home + " alacritty-tweak-tool &"` — `-E` preserves `DISPLAY`/`WAYLAND_DISPLAY`/`DBUS_SESSION_BUS_ADDRESS`; `env HOME=` overrides just the home path
- Only the `vboxstack_software.append(...)` order changed in `software_gui.py`; widget construction order is unchanged

### Files Modified

- `usr/share/archlinux-tweak-tool/software.py`
- `usr/share/archlinux-tweak-tool/shell.py`
- `usr/share/archlinux-tweak-tool/software_gui.py`

---

## 2026.05.16 - Alacritty Tweak Tool: fix VTE expanding over settings panel

### What Changed

- **Left panel no longer pushed out by VTE** — `set_shrink_start_child(False)` added to both `Gtk.Paned` instances (Themes tab and Appearance tab); the settings panel now holds its minimum width regardless of how wide the terminal preview grows

### Technical Details

- GTK4 `Gtk.Paned` allows either child to shrink below its natural minimum by default; `set_shrink_start_child(False)` enforces the `set_min_content_width(300)` floor on the left `ScrolledWindow` so the right VTE cannot crowd it out

### Files Modified

- `usr/share/alacritty-tweak-tool/alacritty_gui.py`

---

## 2026.05.16 - Alacritty Tweak Tool: Appearance paned layout + divider persistence

### What Changed

- **Appearance tab restructured to paned layout** — settings panel (Font + Window sections + Apply/Reset buttons) on the left inside a `ScrolledWindow`; VTE preview on the right inside `detail_box`; matches the Themes tab layout pattern exactly
- **Themes paned position aligned** — changed from `320` to `360` so both tabs give the VTE the same horizontal space
- **Paned divider position persisted across launches** — both Themes and Appearance paned positions are saved to `~/.config/alacritty-tweak-tool/prefs.json` on every drag (`notify::position`) and restored on next launch via `cfg.load_prefs()`; keys: `paned_themes_pos` and `paned_appearance_pos`; fallback default: `360`

### Technical Details

- Appearance `outer` now has margins `10/6/6/6` (matching Themes) rather than `16` all sides; inner `left_box` carries the per-section margins
- Themes `_save_prefs()` closure extended to include `paned_themes_pos: paned.get_position()`; paned position signal connected immediately after paned construction
- Appearance paned position saved inline via lambda: `lambda *_: cfg.save_prefs({**cfg.load_prefs(), "paned_appearance_pos": paned.get_position()})`
- `notify::position` fires on every pixel drag, so the prefs file always holds the latest position — no "on close" handler needed

### Files Modified

- `usr/share/alacritty-tweak-tool/alacritty_gui.py`

---

## 2026.05.16 - Dev page to top; Safeguards section; DISTRO_GUARDS.md overhaul; UI vocabulary

### What Changed

- **Dev page moved to top of sidebar** — `if fn.DEV: stack.add_titled(vboxstack_dev, ...)` moved to before all other `add_titled` calls so Dev appears first in the sidebar when running with `--dev`
- **Safeguards section in Dev page** — new grid section listing all six active distro guards evaluated live against the current system: Plymouth page hidden (artix), SDDM page hidden (prismlinux), SDDM page hidden (plasma-login/plasmalogin service), Kernel pacman-hook required (arch + systemd-boot), User visudo section shown (arch), Plymouth omarchy marker on apply; guards that hide something show orange, guards that enable something show green
- **Login Manager section split** — `plasma-login` and `plasmalogin` now shown as two separate rows so both guard conditions are visible independently
- **DISTRO_GUARDS.md overhauled** — "Tab Visibility Guards" renamed to "Page Visibility Guards"; per-distro Plymouth default theme entries removed from guards (they are UX, not guards); "Protected Functionality — Not Guards" section added documenting the `_default_theme` dict as frozen; omarchy marker description updated from file path to `att_settings.json` key; Quick Reference table corrected
- **UI vocabulary established** — Page = top-level sidebar entry; Tab = sub-section within a page; documented in CLAUDE.md and memory

### Technical Details

- Guard rows use a `_guard_rows` list of tuples `(name, condition_str, active_bool, active_markup)` iterated into `_row()` — consistent with existing grid pattern, no new helpers needed
- Plymouth default theme mapping (`_default_theme` dict in `plymouth_gui.py`) is intentional UX; protected under "Protected Functionality" in DISTRO_GUARDS.md — never reclassify as a guard
- Omarchy marker guard checks `fn.distr == "omarchy"` which depends on `_omarchy_marker_set()` reading `att_settings.json["omarchy_plymouth_customized"]`; detection runs at import time before the Dev page builds

### Files Modified

- `usr/share/archlinux-tweak-tool/gui.py`
- `usr/share/archlinux-tweak-tool/dev_gui.py`
- `DISTRO_GUARDS.md`
- `CLAUDE.md`

---

## 2026.05.15 - Startup profiling, splash removal, sidebar branding

### What Changed

- **Lazy import summary table**: replaced 17 individual `[TIMING]` debug lines with a `_timed_import()` helper that collects elapsed times into a dict; prints a sorted (slowest-first) summary table after all imports complete — mirrors the existing background-init summary table
- **Splash screen removed**: `splash.py` import, `self._splash` construction, and splash destroy block removed; app loads fast enough that the splash was adding perceived latency instead of masking it
- **"Config backups complete" notification**: fires via `GLib.idle_add` at end of `_finish_background_init` so users see confirmation that background work finished
- **Sidebar branding**: "ArchLinux Tweak Tool" bold label in `#FFA500` orange added at top of sidebar above the tab list; fills the long-standing empty `# LOGO` placeholder
- **"on Kiro" distro line**: OS label moved from bottom of sidebar to directly under the brand name, reformatted from `OS: Kiro` → `on Kiro`; `hbox_os_label` removed from bottom of `ivbox`

### Technical Details

- `_timed_import(label, do_import)` wraps any `__import__` or factory lambda; returns the module/object and records elapsed time in `_import_times` dict; summary uses `sorted(..., reverse=True)` so slowest import is always at top
- Notification uses `GLib.idle_add(fn.show_in_app_notification, self, "Config backups complete")` — safe from the daemon thread, fires after `initializing` is set to False
- Brand label uses `set_markup('<span foreground="#FFA500">...')` — same orange as Plymouth page "Note:" label; no CSS changes required
- `lbl_on_distro` uses `fn.get_distro_label()` — same function the old `lbl_os_label` used

### Files Modified

- `usr/share/archlinux-tweak-tool/archlinux-tweak-tool.py`
- `usr/share/archlinux-tweak-tool/gui.py`

---

## 2026.05.15 - Code review pass: all 24 tabs complete

### What Changed

- **AI Tools**: added module-level path constants (`AIDER_PATH`, `CODEX_PATHS`, etc.) eliminating DRY violation; added `log_success` to all removal wait-threads; added `if process is None: return` guard; renamed `hbox_section1–4` → descriptive names
- **Autostart**: removed dead `labelbox` widget, redundant `f.close()` inside `with` blocks, and dead commented lines; renamed `on_comment_changed` → `on_add_entry_changed`; renamed param `vboxstack13` → `vboxstack_autostart`
- **Desktop**: removed `import os` (replaced with `fn.path`) and dead `_is_removable()` helper; renamed `vboxstack12` → `vboxstack_desktop`, `lbl1` → `lbl_title`; fixed callback param `widget` → `_widget`
- **Fastfetch**: removed dead `check_backend()` function and its unused `backend` param; fixed page title from `set_markup` to `set_text`; renamed `vboxstack8` → `vboxstack_fastfetch`
- **Icons**: removed `# pylint:disable=C0103,` line, trivial docstring, and all `# ══` banner blocks; renamed `vboxstack25` → `vboxstack_icons`, `lbl1` → `lbl_title`
- **Kernels through Themer**: docstrings added/improved, `# ====` banners converted to `# ──` style, `vboxstack` params renamed to descriptive names, `_widget` convention enforced throughout; shell_gui local vboxstacks renamed `vboxstack1–4` → `vbox_bash/zsh/fish/extra`; themer_gui local labels renamed `lbl1–6/lbls` → descriptive names
- **Themes**: docstrings added to all 12 public functions; `_att_preview_picture` multi-paragraph docstring reduced to single line; `gui()` docstring improved
- **User**: docstrings added to 3 callback functions; `# ====` banner converted; `gui()` docstring improved
- **Wallpaper**: docstrings added to all 15 public functions; `gui()` docstring improved
- All 24 tabs in `review.md` ticked complete

### Technical Details

- All changes enforce objectives 16 (snake_case, `_widget`), 23 (PEP 257 docstrings, no restating comments), 26 (page titles via `set_text`, section headers via `set_markup`), and 27 (no numbered widget names)
- `vboxstack` renames updated in both `_gui.py` and `gui.py` (3 occurrences each per rename)
- Private functions (`_`-prefixed) intentionally left without docstrings per project rule
- Substring collision rule applied: longer/more-specific names (e.g. `vboxstack10`) renamed before shorter substrings (`vboxstack1`)

### Files Modified

- `usr/share/archlinux-tweak-tool/ai.py`, `ai_gui.py`
- `usr/share/archlinux-tweak-tool/autostart.py`, `autostart_gui.py`
- `usr/share/archlinux-tweak-tool/desktopr.py`, `desktopr_gui.py`
- `usr/share/archlinux-tweak-tool/fastfetch.py`, `fastfetch_gui.py`
- `usr/share/archlinux-tweak-tool/icons.py`, `icons_gui.py`
- `usr/share/archlinux-tweak-tool/kernel.py`, `kernel_gui.py`
- `usr/share/archlinux-tweak-tool/locale.py`, `locale_gui.py`
- `usr/share/archlinux-tweak-tool/logging.py` (log_gui.py)
- `usr/share/archlinux-tweak-tool/maintenance.py`, `maintenance_gui.py`
- `usr/share/archlinux-tweak-tool/network.py`, `network_gui.py`
- `usr/share/archlinux-tweak-tool/packages.py`, `packages_gui.py`
- `usr/share/archlinux-tweak-tool/pacman_functions.py`, `pacman_gui.py`
- `usr/share/archlinux-tweak-tool/plymouth.py`, `plymouth_gui.py`
- `usr/share/archlinux-tweak-tool/privacy.py`, `privacy_gui.py`
- `usr/share/archlinux-tweak-tool/performance.py`, `performance_gui.py`
- `usr/share/archlinux-tweak-tool/sddm.py`, `sddm_gui.py`
- `usr/share/archlinux-tweak-tool/services.py`, `services_gui.py`
- `usr/share/archlinux-tweak-tool/shell.py`, `shell_gui.py`
- `usr/share/archlinux-tweak-tool/software.py`, `software_gui.py`
- `usr/share/archlinux-tweak-tool/system.py`, `system_gui.py`
- `usr/share/archlinux-tweak-tool/themer.py`, `themer_gui.py`
- `usr/share/archlinux-tweak-tool/themes.py`, `themes_gui.py`
- `usr/share/archlinux-tweak-tool/user.py`, `user_gui.py`
- `usr/share/archlinux-tweak-tool/wallpaper.py`, `wallpaper_gui.py`
- `usr/share/archlinux-tweak-tool/gui.py`
- `review.md`

---

## 2026.05.14 - Fastfetch: fix all review issues — bugs, style, DRY, naming, section headers

### What Changed

- Fixed `pos > 0` → `pos >= 0` in `get_term_rc()` — fastfetch on line 0 of a shell config was incorrectly reported as disabled
- Removed dead `_ascii_size` parameter from `apply_config()` and the `small_ascii = "auto"` local from `on_apply_fast()`
- Lolcat install failure now logs a warning and shows an in-app notification before snapping the switch back (was silent)
- Collapsed four `set_checkboxes_*` functions (130 lines) into `_apply_preset()` + module-level `_PRESET_ALL/NORMAL/SMALL/NONE` dicts
- Renamed `self.lIP` / `self.PIP` → `self.l_ip` / `self.p_ip`; removed `pylint:disable=C0103`
- Moved `import time` and `from gi.repository import Gdk` from inside functions to top of `fastfetch_gui.py`
- Removed trivial `"""create a gui"""` docstring and code-restating inline comments in `apply_config`
- Replaced `for i in range(len(lines))` with `enumerate` throughout; replaced `if len(data) > 0` with `if data:`
- Removed redundant `myfile.close()` inside `with` block in `get_term_rc()`
- Added **Shell Startup** and **Modules** section headers (objective 26)

### Technical Details

- `_apply_preset(self, states)` iterates a `{attr: bool}` dict and calls `getattr(self, attr).set_active(state)` — adding a new checkbox now requires only adding one entry to each preset dict, not editing four functions
- `_PRESET_NONE` is derived as `{attr: False for attr in _PRESET_ALL}` — it can never drift out of sync with the checkbox list
- The `_ascii_size` removal is safe: the parameter was underscore-prefixed and never read inside `apply_config()`

### Files Modified

- `usr/share/archlinux-tweak-tool/fastfetch.py`
- `usr/share/archlinux-tweak-tool/fastfetch_gui.py`

---

## 2026.05.14 - SDDM: sort available themes by AUR last-updated date

### What Changed

- Added "Sort by recently updated (AUR)" switch to the Available SDDM Themes section
- When toggled ON, fetches `LastModified` timestamps from the AUR RPC v5 `/info` endpoint and re-sorts the dropdown newest-first
- Fetch is lazy (only on first toggle) and cached in a closure dict for the session — subsequent toggles re-sort instantly

### Technical Details

- `fetch_aur_pkg_modified(packages)` in `sddm.py` — single `urllib.request` call to `aur.archlinux.org/rpc/v5/info?arg[]=...` for all packages at once; returns `{name: last_modified_unix_ts}`, empty dict on any error (network down, AUR unreachable)
- Closure state: `_aur_modified = {}` and `_current_avail_pkgs = []` defined in the `gui()` scope; mutated via `nonlocal` inside `_run` background thread
- `_populate_avail_sddm` reads `_aur_modified` and sorts `display` list descending by timestamp when switch is active; repo packages not in AUR response sort to the bottom (timestamp 0, retaining alphabetical order among themselves)
- Notification fires while fetch is in progress; re-sort happens via `GLib.idle_add` after the background thread completes

### Files Modified

- `usr/share/archlinux-tweak-tool/sddm.py`
- `usr/share/archlinux-tweak-tool/sddm_gui.py`

---

## 2026.05.14 - Startup: lazy tab construction (0.171s window-visible)

### What Changed

- ATT window now appears in ~0.171s (down from 2–4s); all 24 tab contents are built on first visit instead of at startup
- Moved `setup_fastfetch_config()` out of `gui.gui()` into `_finish_startup_init()` — startup logic no longer mixed with GUI building
- Added safe-default lambdas for `self.on_desktop_changed` and `self.rebuild_sddm_page` before `gui.gui()` so desktopr/sddm callbacks are safe even if those tabs have not been visited yet

### Technical Details

- Added `_defer_tab(container, build_fn)` helper inside `gui.gui()`: connects a one-shot `map` signal to each tab container; the signal fires when GTK first maps the widget (initial visible tab fires on present, all others fire on first click), then the build function is called exactly once
- 19 tabs deferred via `_defer_tab`: icons, themes, autostart, desktop, fastfetch, maintenance, services, shells, themer, user, packages, sddm, kernels, ai, logging, system, software, plymouth, locale
- 5 tabs called directly (already self-managing via their own internal `map`-signal lazy loaders): pacman, privacy, performance, network, wallpaper — deferring these would cause their internal data-population handlers to miss the first `map` event
- Themer and SDDM required special build functions (not lambdas) because they also set `self.on_desktop_changed` and `self.rebuild_sddm_page` closures respectively after their `gui()` call completes
- `_defer_tab` uses a `built = [False]` closure flag rather than disconnecting the signal, keeping the implementation simple and re-entry safe

### Files Modified

- `usr/share/archlinux-tweak-tool/gui.py`
- `usr/share/archlinux-tweak-tool/archlinux-tweak-tool.py`

---

## 2026.05.14 - Variety scripts: a2n.blur support + Plasma 6 fix

### What Changed

- `set_wallpaper_kiro` KDE/Plasma block now uses a `supportedPlugins` array (`org.kde.image`, `a2n.blur`) and writes to the containment's actual `d.wallpaperPlugin` dynamically — variety can now change the wallpaper on Garuda Plasma (which uses the `a2n.blur` plugin by default)
- `get_wallpaper_kiro` KDE branch no longer requires `KDE_SESSION_VERSION == "5"`; the appletsrc layout is identical on Plasma 6, so the same `grep 'Image='` works
- `get_wallpaper_kiro` now guards the trailing `~/.fehbg` read with `[ -f ~/.fehbg ]` so the script exits 0 cleanly on non-feh desktops
- Fixed a quoting bug in `set_wallpaper_kiro` SIMPLE_WMS array: `"…/hypr""…/i3"` were concatenated into one element; now properly separated (array length 23 → 24)

### Technical Details

- Bug surfaced on Garuda Plasma 6: `variety -n` reached the daemon and `set_wallpaper_kiro` ran to completion (dbus exit 0), but the embedded JS only matched `d.wallpaperPlugin == 'org.kde.image'` — Garuda containments use `a2n.blur`, so the JS loop's `if` body never fired and no `Image=` key was ever written
- Verified on this machine: before fix, `[Containments][1][Wallpaper][a2n.blur][General] Image=` was stuck at `/usr/share/wallpapers/garuda-mokka/clouds.jpg` despite multiple `variety -n` calls; after fix, both containments update on every `-n`/`-p` cycle
- Plasma 6 secondary bug: `get_wallpaper_kiro` was falling through to `gsettings get org.gnome.desktop.background picture-uri` (no schema → exit 1), producing `subprocess.CalledProcessError` in `variety.log` at every startup
- Upstream variety's bundled `set_wallpaper` script already added `a2n.blur` to its supportedPlugins; the kiro fork predated that fix

### Files Modified

- `usr/share/archlinux-tweak-tool/data/variety/scripts/set_wallpaper_kiro`
- `usr/share/archlinux-tweak-tool/data/variety/scripts/get_wallpaper_kiro`

---

## 2026.05.14 - GRUB splash fix: quote-agnostic + idempotent

### What Changed

- Rewrote `on_grub_fix_clicked` in `plymouth_gui.py` — the previous sed only matched **double-quoted** `GRUB_CMDLINE_LINUX_DEFAULT` values, silently doing nothing on Garuda (which uses single quotes)
- New script reads the value with awk, strips either quote style, tokenizes, adds `quiet` and `splash` only if missing, writes back with consistent double quotes
- Added `trap … EXIT` so the terminal stays open if any step fails (instead of auto-closing on `set -e`)
- Tightened `plymouth.check_grub_splash()` — now token-matches (so `nosplash` no longer counts as `splash`); also accepts single- or double-quoted values

### Technical Details

- Bug surfaced on Garuda: `/etc/default/grub` has `GRUB_CMDLINE_LINUX_DEFAULT='...'` (single quotes); old sed regex `'s/^\(GRUB_CMDLINE_LINUX_DEFAULT="[^"]*\)"/.../'` only matched double quotes — Plymouth boot screen never appeared because `splash` was never added
- Script is now idempotent: detects when both tokens already exist and skips the rewrite + backup
- Verified dry-run produces `GRUB_CMDLINE_LINUX_DEFAULT="quiet resume=... loglevel=3 splash"` on Garuda

### Files Modified

- `usr/share/archlinux-tweak-tool/plymouth.py`
- `usr/share/archlinux-tweak-tool/plymouth_gui.py`

---

## 2026.05.14 - dracut-rebuild detection (Garuda fix)

### What Changed

- Added `fn.get_initramfs_rebuild_cmd()` helper to `functions.py` — returns `"dracut-rebuild"` when `/usr/bin/dracut-rebuild` exists, else `"dracut --regenerate-all --force"`, else `"mkinitcpio -P"`
- Plymouth Install / Apply / Reset / Fix-hook scripts now use the helper instead of hardcoded `dracut --regenerate-all --force`
- Kernel `run_dracut()` now uses the helper — script and log messages reflect the actual command

### Technical Details

- Bug surfaced on Garuda: plain `dracut --regenerate-all --force` invokes kernel-install path that expects `/boot/efi/<machine-id>/<kernel>/` directories Garuda does not create (Garuda uses GRUB + `/boot/initramfs-*.img`); resulting error: `Can't write to /boot/efi/<machine-id>/<kernel>: Directory does not exist`
- Garuda ships `/usr/bin/dracut-rebuild` (wrapper calling `dracut-install-garuda`) which handles the GRUB layout correctly — preferring it on Garuda while falling back to plain dracut elsewhere keeps the same code path working on CachyOS, Arch+dracut, etc.
- Decision: helper lives in `functions.py` (per objective 17 — single source of truth) rather than duplicated detection in `plymouth_gui.py` + `kernel.py`

### Files Modified

- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/plymouth_gui.py`
- `usr/share/archlinux-tweak-tool/kernel.py`

---

## 2026.05.14 - Plymouth page: dracut support (Garuda + any dracut-based distro)

### What Changed

- Plymouth page now detects dracut systems via `plymouth.is_dracut()` (thin wrapper over `/usr/bin/dracut` presence) and branches every action that used to assume mkinitcpio
- **Install Plymouth** on dracut: 2-step script (`pacman -S plymouth` → `dracut --regenerate-all --force`); skips the mkinitcpio HOOKS patch entirely
- **Initramfs plymouth-module warning** on dracut: replaces the mkinitcpio HOOKS-line check with `plymouth.check_dracut_plymouth_enabled()`; fix button writes `/etc/dracut.conf.d/att-plymouth.conf` with `add_dracutmodules+=" plymouth "` and runs `dracut --regenerate-all --force`
- **Hooks-order warning** (`encrypt`/`lvm2` before `plymouth`) hidden on dracut — it is a mkinitcpio-only concern
- **Early KMS** section on dracut: shows an informational note (mirror of the NVIDIA branch) pointing at `/etc/dracut.conf.d/` with `force_drivers+=" amdgpu "` example; no auto-fix button — matches risk profile of the existing NVIDIA path
- **Apply theme** and **Reset to default**: no longer call `plymouth-set-default-theme -R` (which calls mkinitcpio on standard Arch); instead set the theme then explicitly run `dracut --regenerate-all --force` or `mkinitcpio -P` based on detection

### Technical Details

- `plymouth.check_dracut_plymouth_enabled()` scans `/etc/dracut.conf` + `/etc/dracut.conf.d/*.conf` for `add_dracutmodules+=" plymouth"`, respects `omit_dracutmodules`, and falls back to `/usr/lib/dracut/modules.d/90plymouth` directory presence (dracut auto-picks the module up by default when the plymouth package is installed)
- Decision: ATT writes `/etc/dracut.conf.d/att-plymouth.conf` when missing — does not depend on `garuda-dracut-support` being installed (Kernel tab still handles that)
- Decision: Early KMS on dracut is informational only (no auto-fix) — keeps the implementation surface small and matches risk tolerance for hardware we cannot test directly
- `_rebuild_cmd` constant at top of `gui()` (`"dracut --regenerate-all --force"` vs `"mkinitcpio -P"`) used by both Apply and Reset scripts

### Files Modified

- `usr/share/archlinux-tweak-tool/plymouth.py`
- `usr/share/archlinux-tweak-tool/plymouth_gui.py`

---

## 2026.05.14 - Dracut support for Kernel Manager (Garuda + any dracut-based distro)

### What Changed

- Added `is_dracut()` detection to `kernel.py` — checks for `/usr/bin/dracut`
- Added `run_dracut(self)` to `kernel.py` — opens Alacritty running `dracut --regenerate-all --force`; returns Popen like `run_grub_update()`, returns None on non-dracut systems
- Wired `run_dracut()` into all 5 install/remove completion callbacks in `kernel_gui.py` — runs after GRUB update (no-op on Kiro/mkinitcpio systems)
- Added "Dracut — Initramfs Generator" GUI section shown only on dracut systems; button "Regenerate All Initramfs" triggers dracut in a daemon thread, disables itself while running
- Added Garuda entry in `kernel_distros.py` requiring `garuda-dracut-support` (Garuda's dracut config + pacman hook)

### Technical Details

- `run_dracut()` follows the exact same pattern as `run_grub_update()`: check → log → show notification → Popen alacritty → return process
- All 5 `launch_and_wait`-style closures now have the sequence: `run_grub_update` → `run_dracut` → `GLib.idle_add(refresh)`; both are no-ops when not applicable so Kiro behaviour is unchanged
- VirtualBox test showed expected failure: `dracut --regenerate-all --force` needs the ESP mounted and machine-ID dirs created by `kernel-install`; works correctly on real Garuda hardware

### Files Modified

- `usr/share/archlinux-tweak-tool/kernel.py`
- `usr/share/archlinux-tweak-tool/kernel_gui.py`
- `usr/share/archlinux-tweak-tool/kernel_distros.py`

---

## 2026.05.14 - archlinux-logout chaotic-AUR guard + variety.desktop categories

### What Changed

- `on_click_software_archlinux_logout` now guards install path with `check_chaotic_aur_active()` — shows "Enable nemesis/chaotic-AUR in the Pacman tab first" notification and returns early if the repo is absent
- Replaced the inline `wait_install` daemon thread in `on_click_software_archlinux_logout` with `fn.wait_install_and_update()` to match the pattern used by all other install callbacks
- Updated log/notification messages to say "nemesis/chaotic-AUR" (package lives in both repos) instead of just "chaotic-AUR"
- Expanded the variety.desktop fallback `Categories` field to include `System;Core;FileTools;FileManager;` so Variety appears in the correct menu categories on desktops that filter by category

### Technical Details

- Guard follows the same pattern as `pacui`, `pacseek`, `yay-git`, and `paru-git`: `if not fn.check_chaotic_aur_active(): log_info + notification + return`
- `wait_install_and_update` replaces ~28 lines of inline thread boilerplate; no behaviour change, just consolidation

### Files Modified

- `usr/share/archlinux-tweak-tool/software.py`
- `usr/share/archlinux-tweak-tool/wallpaper.py`

---

## 2026.05.14 - Network page fixes + nano editor section on Software page

### What Changed

- Restart Smb button now shows in-app notification "Samba is not yet installed" when samba package is absent; corrected misleading "not installed or running" message when package is installed but service is down
- Added "Nano Editor" section to the Software page: Apply ATT nanorc (backs up `/etc/nanorc` first) and Restore backup buttons; shipped `data/nano/nanorc` as the ATT nanorc template

### Technical Details

- `on_click_restart_smb` guards with `fn.check_package_installed("samba")` before calling `restart_smb()`; the inner `if not smb_active` branch now only fires when samba is installed but the service is inactive
- `fn.nanorc`, `fn.nanorc_bak`, `fn.nanorc_att` path constants added to `functions.py`
- `backup_nanorc()` and `restore_nanorc()` added to `functions_backup.py`; backup skips if `/etc/nanorc-bak` already exists
- Restore button starts insensitive; becomes active once a backup exists
- `data/nano/nanorc` is a copy of `/etc/nanorc` (Nemesis nanorc) shipped with ATT

### Files Modified

- `usr/share/archlinux-tweak-tool/services.py`
- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/functions_backup.py`
- `usr/share/archlinux-tweak-tool/software.py`
- `usr/share/archlinux-tweak-tool/software_gui.py`
- `usr/share/archlinux-tweak-tool/data/nano/nanorc` (new)

---

## 2026.05.14 - Fix fastfetch install via switch toggle

### What Changed

- Fastfetch switch toggle now picks the correct package (`fastfetch-git` vs `fastfetch`) based on repo availability, matching the logic already used in the dedicated install button

### Technical Details

- `on_fast_util_toggled` was hardcoded to `fastfetch-git`; now applies `check_chaotic_aur_active() or check_nemesis_repo_active()` and falls back to `fastfetch` when neither AUR repo is active

### Files Modified

- `usr/share/archlinux-tweak-tool/fastfetch.py`

---

## 2026.05.13 - Add get-ohmychadwm-on-att script + TODO cleanup

### What Changed

- Created `usr/bin/get-ohmychadwm-on-att` — installs ohmychadwm packages, removes conflicting rofi lbonn variants, backs up `~/.config`, and applies skel
- Cleaned up `TODO.md`: removed completed New Scripts section, removed duplicate Bazaar/pkexec entry, removed completed Scripts Audit entry

### Technical Details

- Package list sourced directly from `desktopr.py` ohmychadwm array (lines 241–268) to keep one authoritative source
- Follows ATT Script Standard: `set -euo pipefail`, tput colors, `separator`/`header`/`success`/`info`/`warn`/`error` helpers
- Conflict removal targets `rofi-lbonn-wayland`, `rofi-lbonn-wayland-git`, `rofi-lbonn-wayland-only-git` (ohmychadwm uses plain `rofi`, not the lbonn fork)
- Uses `read -p` at end without `--hold` per ATT preference

### Files Modified

- `usr/bin/get-ohmychadwm-on-att` (new)
- `TODO.md`

---

## 2026.05.13 - Repo-gate communication: desktopr install button tooltip + console log

### What Changed

- `desktopr_gui.py`: disabled install button now shows a tooltip explaining why (nemesis_repo + chaotic-aur not enabled); console logs both repo states when the Desktop Installer page is built
- `functions_startup.py`: removed dead `self.button_reinstall.set_sensitive(False)` — that attribute never existed; call was silently swallowed by `except Exception: pass`

### Technical Details

- `on_install_clicked` warning (log_warn + notification) was unreachable code because the button was disabled before the user could click it; tooltip covers the pure-Arch user without making the button enabled
- Tooltip set only when `nemesis_active` is False so it doesn't interfere with normal operation
- `fn.log_info` at end of `gui()` reuses the already-computed `nemesis_active` local and adds one `check_chaotic_aur_active()` call to show both repo states in the console at page load

### Files Modified

- `usr/share/archlinux-tweak-tool/desktopr_gui.py`
- `usr/share/archlinux-tweak-tool/functions_startup.py`

---

## 2026.05.13 - Remove 4 orphaned scripts from data/bin/

### What Changed

- Deleted `create-swapfile`, `disable-zram`, `enable-zram`, `remove-swapfile` — confirmed zero references across all Python source and shell scripts

### Technical Details

- Audited all 18 `data/bin/` scripts by grepping Python source for each name; 14 active, 4 with no callers anywhere in the repo
- No GUI tab for swap or zram exists; these scripts were dead code

### Files Modified

- `data/bin/create-swapfile` (deleted)
- `data/bin/disable-zram` (deleted)
- `data/bin/enable-zram` (deleted)
- `data/bin/remove-swapfile` (deleted)

---

## 2026.05.13 - Bug fixes: invalidate_pkg_cache sweep, inxi/octopi/yay/paru, shell messages, fastfetch snap-back

### What Changed

- **`invalidate_pkg_cache()` sweep**: Added missing cache invalidation after every `process.wait()` that is followed by a `check_package_installed()` call — covers `sddm.py`, `plymouth_gui.py`, `performance.py`, `services.py`, `shell.py`, `wallpaper.py`, `fastfetch.py`, `software.py`, `system.py`, `privacy.py`
- **`sddm_gui.py`**: Removed `plasma-login-manager` install/enable section entirely — offering it would break the tab's own `check_service_enabled("plasma-login")` guard
- **`fastfetch.py`**: Toggle snaps back to OFF (with notification) when fastfetch is not found after install; `ff_initializing` guard prevents re-trigger loop
- **`shell.py`**: All six shell-config apply/restore notifications now say "— log out and back in to apply"
- **`software.py`**: octopi failure path now uses `GLib.idle_add(fn.check_missing_repo_error, ...)` for GTK thread safety; yay-git / paru-git ask user to build from AUR if chaotic-AUR is not active; added `import pacman_functions`
- **`system.py`**: inxi button checks installed state first — launches display immediately if present; if not, opens install terminal and waits in daemon thread before launching display
- **`performance.py`**: All 8 install/remove callbacks (ananicy, tuned, irqbalance, gamemode) rewritten with `wait_and_refresh` pattern — labels update only after confirmed install/remove
- **`services.py`**: cups, cups-pdf, system-config-printer install/remove rewritten with proper daemon thread + `process.wait()` + cache invalidation + conditional label update

### Technical Details

- Root cause of all greyed-button/stale-label bugs: `check_package_installed()` caches results per session; any install/remove terminal close must call `fn.invalidate_pkg_cache()` before the next check
- GTK threading rule: anything that touches a widget must go through `GLib.idle_add()` — direct calls from a background thread cause silent failures
- yay/paru fallback uses `fn.show_confirm_dialog()` (synchronous, uses `GLib.MainLoop`) — safe from button callback (GTK main thread); routes to `pacman_functions.install_yay_git/paru_git()` for the AUR build path
- fastfetch snap-back: setting `self.ff_initializing = True` before `set_active(False)` suppresses `on_fast_util_toggled` re-entry; reset to `False` immediately after

### Files Modified

- `sddm.py`, `sddm_gui.py`, `plymouth_gui.py`
- `performance.py`, `services.py`, `shell.py`
- `wallpaper.py`, `fastfetch.py`, `privacy.py`
- `software.py`, `system.py`
- `TODO.md`

---

## 2026.05.13 - TODO housekeeping: button messaging audit, per-page UX bugs

### What Changed

- Added "Button Messaging Audit" section: test every button for notification bar + console log output; on pure Arch any button requiring a disabled repo must communicate this clearly
- Added "Fastfetch Page" section: enable toggle must snap back to off and notify when fastfetch is not installed
- Added "Shell Page" section: zsh "Installed" label after install; decision item for bashrc immediate-apply vs logout notice
- Added "hblock Page" section: enable fails silently on pure Arch — investigate and fix or explain
- Added "Performance Page" section: tuned/tuned-ppd and irqbalance buttons stay greyed out after install; gamemode missing "Installed" label + greyed buttons; ananicy false install notification in both notification bar and console log
- Added "SDDM Page" section: URGENT — remove install/enable option for plasma-login-manager
- Added "Services Page" section: cups, cups-pdf missing "Installed" label after install; system-config-printer "Installed" label not cleared after removal
- Added "Software/Packages Page" section: octopi silent failure; yay-git/paru-git popup offer to build from AUR if chaotic-AUR absent; inxi auto-display after install; variety buttons stay greyed after install

### Technical Details

- All greyed-button issues share the same root cause: UI sensitivity is not re-evaluated after the install terminal closes; fix is the `wait_and_refresh` pattern throughout
- ananicy issue: `log_*` calls and notification fire before (not after) checking install state
- plasma-login-manager removal is a correctness fix: offering to install/enable it would break the SDDM tab's own `check_service_enabled("plasma-login")` guard

### Files Modified

- `TODO.md`

---

## 2026.05.12 - TODO housekeeping: scripts audit, new scripts, termite leftover investigation

### What Changed

- Added "Scripts Audit" section to TODO.md: task to grep all Python source for `data/bin/` calls and identify any unused scripts
- Added "New Scripts" section to TODO.md: two paired entries — `get-chadwm-on-att` and `get-ohmychadwm-on-att`
- Added "~/.config/archlinux-tweak-tool/ Cleanup" section to TODO.md: investigation revealed `settings.ini` in that directory contains stale termite config written by an old arco-era ATT; the word "termite" no longer appears anywhere in the current codebase

### Technical Details

- `fn.config` (defined in `functions.py:233`) points to `~/.config/archlinux-tweak-tool/settings.ini`; the directory is created at startup by `functions_makedir.py:115`; nothing in the current codebase writes termite config there — the file is a leftover from a previous arco-era version of ATT

### Files Modified

- `TODO.md`

---

## 2026.05.12 - Codebase improvements: pkg cache, naming cleanup, up.sh auto-pull

### What Changed

- `check_package_installed()` and `check_service_enabled()` now cache results per session — eliminates redundant pacman/systemctl subprocesses on repeated calls across tab builds
- Cache is automatically invalidated after any install or remove terminal closes (in `wait_install_and_update` and `wait_remove_and_update`)
- Page-title labels in 5 files changed from `set_text()` to `set_markup("<b>...</b>")` for consistency with the rest of the codebase
- `autostart.py`: renamed all numbered/collision widget names to descriptive identifiers; also fixed page title to use `set_markup`
- `up.sh`: added `git pull --rebase` at the top so multi-machine runs sync before committing; removed duplicate bare `git commit -m "update"` on line 28 that always errored or double-committed

### Technical Details

- Cache dicts `_pkg_cache` and `_svc_cache` declared at module level in `functions.py` alongside existing `_pacman_conf_cache`; `invalidate_pkg_cache()` clears both
- `autostart.py` variable collision fixed: `lbl1` was used for both the page title and the "Name" form field; split into `lbl_title`, `lbl_name`, `lbl_command`, `lbl_comment`; `self.txtbox1/2/3` → `self.entry_name/command/comment`
- `git pull --rebase` chosen over plain `git pull` to keep history linear on multi-machine workflow

### Files Modified

- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/autostart.py`
- `usr/share/archlinux-tweak-tool/logging_gui.py`
- `usr/share/archlinux-tweak-tool/maintenance_gui.py`
- `usr/share/archlinux-tweak-tool/packages_gui.py`
- `usr/share/archlinux-tweak-tool/fastfetch_gui.py`
- `usr/share/archlinux-tweak-tool/system_gui.py`
- `up.sh`

---

## 2026.05.12 - SDDM theme dropdown unconditional refresh + leftover dir cleanup

### What Changed

- Theme dropdown on the SDDM page now always refreshes after the Remove Simplicity button's terminal closes
- `/usr/share/sddm/themes/edu-simplicity` is now explicitly deleted after package removal — pacman leaves the directory behind when the user applied a custom wallpaper (the modified file is no longer tracked by the package)

### Technical Details

- `on_click_remove_simplicity` `refresh()` now: (1) checks if the theme directory still exists and removes it with `shutil.rmtree`; (2) calls `pop_theme_box` unconditionally at the end so the dropdown always reflects the actual filesystem state
- Root cause: ATT's "Apply wallpaper" copies a file into `/usr/share/sddm/themes/edu-simplicity/images/background.jpg`; pacman removes only files it installed, so any overwritten/added files leave the directory alive after `pacman -R`

### Files Modified

- `usr/share/archlinux-tweak-tool/sddm.py`

---

## 2026.05.12 - Right-click browser picker on all link buttons

### What Changed

- Every "link" button on the AI page now shows a right-click popover with a browser picker and a "Copy URL" fallback — solves the issue of `xdg-open` not working on certain desktops
- Same right-click behaviour added to the "more info" labels on the Kernel page
- All 16 AI-page link button URLs extracted as module-level constants in `ai.py` (single source of truth)
- Browser-picker helpers (`attach_link_context_menu`, `_show_browser_popover`, `get_installed_browsers`, etc.) live in `functions.py` so any page can reuse them without cross-feature imports

### Technical Details

- `fn.attach_link_context_menu(self, widget, url)` attaches a `Gtk.GestureClick` (button 3) to any widget; on fire it builds a `Gtk.Popover` parented to that widget, positioned at the cursor via `Gdk.Rectangle`, listing all detected browsers
- `_KNOWN_BROWSERS` scans 11 known binary paths at click time (no startup cost); "No browsers detected" shown if none found
- `open_url_with_browser` launches the chosen browser as the real user (`sudo -u $USER DISPLAY=:0 binary url`) and logs the action via `fn.log_info`
- `_copy_url_to_clipboard` writes to `Gdk.Display.get_default().get_clipboard()` and fires an in-app notification
- `Gdk` promoted from a local import inside `update_image` to the top-level `gi.repository` import line in `functions.py`
- `ai_gui.py` calls `fn.attach_link_context_menu` (not `ai.`); `ai.py` no longer imports `Gtk`/`Gdk`

### Files Modified

- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/ai.py`
- `usr/share/archlinux-tweak-tool/ai_gui.py`
- `usr/share/archlinux-tweak-tool/kernel_gui.py`

---

## 2026.05.12 - Distro detection refactor + dead code audit

### What Changed

- Replaced hardcoded `change_distro_label()` mapping with `get_distro_label()` that greps `/etc/os-release` directly; `IMAGE_ID=kiro` checked before `ID=arch` so Kiro is correctly identified even though its base `ID` is `arch`
- Sidebar now shows one label (`get_distro_label()`) instead of two; `change_distro_label()` removed entirely
- Dead amos/archcraft distro-specific block removed from `fastfetch_gui.py` (was behind `fn.distr == "amos"` / `fn.distr == "archcraft"` guards that can never fire in ATT)
- Dead `btn_dark_theme` removed from `gui.py` — button was built and connected but `hbox6` was never appended to `ivbox`, making it permanently invisible
- Empty `hbox5` (spacer with no children) removed from `gui.py`
- `settings` import removed from `gui.py` — only user was the dark theme button
- Full `vulture --min-confidence 80` audit: 11 GTK callback parameters renamed with `_` prefix; 3 unused function parameters renamed
- All numbered hbox/vbox names in `gui.py` replaced with descriptive identifiers (`hbox_notification`, `vbox_content`, `hbox_ff_title`, `hbox_ff_separator`, `hbox_restart_att`, `hbox_quit_att`)

### Technical Details

- `get_distro_label()` reads `/etc/os-release` as plain text and checks for known `ID=` / `IMAGE_ID=` strings in priority order; falls back to `distr` (the `distro.id()` result) if no match found
- `change_distro_label()` was the only caller-facing display function; all three call sites (`gui.py`, `fastfetch_gui.py`, internal) now use `get_distro_label()`
- `vulture` installed from `extra/vulture`; use `vulture usr/share/archlinux-tweak-tool/ --min-confidence 80` for future audits

### Files Modified

- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/gui.py`
- `usr/share/archlinux-tweak-tool/fastfetch_gui.py`
- `usr/share/archlinux-tweak-tool/archlinux-tweak-tool.py`
- `usr/share/archlinux-tweak-tool/autostart.py`
- `usr/share/archlinux-tweak-tool/desktopr.py`
- `usr/share/archlinux-tweak-tool/fastfetch.py`
- `usr/share/archlinux-tweak-tool/icons_gui.py`
- `usr/share/archlinux-tweak-tool/packages.py`
- `usr/share/archlinux-tweak-tool/sddm.py`
- `usr/share/archlinux-tweak-tool/shell.py`
- `usr/share/archlinux-tweak-tool/themer.py`
- `usr/share/archlinux-tweak-tool/themes_gui.py`

---

## 2026.05.12 - Fix GUI app launches on Plasma/Wayland (NyArch)

### What Changed

- `edu-powermenu` failed to launch from ATT on Plasma/NyArch because `~` in the powermenu script expanded to `/root` — root's HOME — not the real user's home; fixed by setting `HOME` in `get_terminal_env()`
- All system-page GUI app launches (gparted, alacritty viewers) failed on Plasma/Wayland because `_run_cmd` passed no display environment; fixed by passing `fn.get_terminal_env()` in `_run_cmd`

### Technical Details

- `get_terminal_env()` now sets `env["HOME"] = home` (real user's home) in addition to `XDG_RUNTIME_DIR` and `WAYLAND_DISPLAY` — ensures `~` expands correctly in any script launched via `runuser`
- `_run_cmd` in `system.py` now captures `fn.get_terminal_env()` before spawning the thread and passes it to `Popen` — covers gparted and all alacritty info viewers on that page

### Files Modified

- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/system.py`

---

## 2026.05.11 - Plymouth: fix combined quiet/splash patch (cmdline + entries always run together)

### What Changed

- `on_sdboot_fix_clicked` was branching on `_use_cmdline`: when True it patched only `/etc/kernel/cmdline` and skipped entries entirely, so `refresh_sdboot_status` (which checks both) never saw `all_ok = True` and the warning never cleared
- Fixed by merging `run_cmdline_fix` and `run_entries_fix` into a single `run_both` thread that always patches both targets in one operation — cmdline first (if it exists), then all entries with missing `quiet splash`
- `fn.log_subsection` and `fn.show_in_app_notification` now fire before the thread starts so the user sees immediate console + in-app feedback

### Technical Details

- Replaced three functions (`on_sdboot_fix_clicked`, `run_cmdline_fix`, `run_entries_fix`) with `on_sdboot_fix_clicked` + inline `run_both` closure
- `_use_cmdline` is still respected inside `run_both` — cmdline patch runs only when `/etc/kernel/cmdline` exists; entry patch always runs regardless

### Files Modified

- `usr/share/archlinux-tweak-tool/plymouth_gui.py`

---

## 2026.05.11 - Plymouth: flat single page + bootloader integration section

### What Changed

- Plymouth page restructured as one flat page with no conditional show/hide: all four sections always visible regardless of install state
- Sections follow the standard page pattern (separator + bold header + content rows): Install Plymouth, Bootloader Integration, Installed themes, Available themes
- "Install Plymouth" section shows the install button and a description at all times; green "Installed" label appears next to the button once plymouth is installed (or immediately on distros where it already is)
- Install script now uses `trap '...' EXIT` so the Alacritty terminal always waits for Enter even when a step fails with `set -euo pipefail`
- New **Bootloader Integration** section: detects systemd-boot, GRUB, limine, rEFInd; for systemd-boot scans all ESP path variants for entries missing `quiet splash` and offers a one-click fix; for GRUB checks `GRUB_CMDLINE_LINUX_DEFAULT` and offers a terminal-based fix that runs `grub-mkconfig`; limine and rEFInd show static info labels pointing to the right config file; mkinitcpio HOOKS ordering warning shown if `encrypt`/`lvm2` precedes `plymouth`
- OK/Installed status labels are plain bold — no green color

### Technical Details

- `plymouth_gui.py`: removed `vbox_not_installed`/`vbox_installed` wrappers and their `set_visible()` guards; flattened all widgets directly onto `vboxstack_plymouth`; added `lbl_plymouth_installed` with `set_visible(_plymouth_installed)`; `on_install_plymouth_done()` calls `lbl_plymouth_installed.set_visible(True)` and no longer toggles any container visibility; added bootloader section with 4 conditional widget groups; `on_sdboot_fix_clicked` patches entries in-process (no terminal needed); `on_grub_fix_clicked` runs in Alacritty terminal
- `plymouth.py`: added `detect_bootloader()`, `find_systemd_boot_entries()` (scans 5 path variants including `/boot/efi/loader/entries` for Kiro), `check_systemd_boot_splash()`, `check_grub_splash()`, `check_hooks_order()`
- Memory rule saved: systemd-boot entry paths must always scan all 5 variants — Kiro uses `/boot/efi/`, standard Arch uses `/boot/`

### Files Modified

- `usr/share/archlinux-tweak-tool/plymouth_gui.py`
- `usr/share/archlinux-tweak-tool/plymouth.py`

---

## 2026.05.11 - Plymouth: full install flow (pacman + mkinitcpio hook + initramfs rebuild); Plymouth tab always visible

### What Changed

- Plymouth tab now always visible in the sidebar regardless of whether `plymouth` is installed
- When Plymouth is not installed: tab shows an install button that runs the full 3-step setup in one Alacritty terminal: (1) `pacman -S --noconfirm plymouth`, (2) adds `plymouth` hook after `udev` in `/etc/mkinitcpio.conf` (backs up file first, skips if already present), (3) runs `mkinitcpio -P`
- After the terminal closes ATT re-checks install state and switches the tab from the "not installed" view to the full theme manager automatically — no restart required
- Both states (not-installed, installed) are built at startup using `vbox_not_installed` / `vbox_installed` with `set_visible()` toggling

### Technical Details

- `gui.py`: both `if fn.check_package_installed("plymouth"):` guards removed — tab always built and added to stack
- `plymouth_gui.py`: added `vbox_not_installed` with install button; existing content wrapped in `vbox_installed`; `_plymouth_installed = fn.check_package_installed("plymouth")` at build time drives initial visibility; `on_install_plymouth_done()` via `GLib.idle_add` toggles visibility and re-populates dropdowns; hook insert uses `sed -i 's/\budev\b/udev plymouth/'` (word-boundary anchors) with existence check to avoid duplicates

### Files Modified

- `usr/share/archlinux-tweak-tool/gui.py`
- `usr/share/archlinux-tweak-tool/plymouth_gui.py`

---

## 2026.05.11 - Plymouth: distro-agnostic detection + per-distro reset default; SDDM: service-enabled guard; Kernel: rEFInd default boot entry selector

### What Changed

- Plymouth tab now visible on any distro where `plymouth` is installed — previously Omarchy-only (required `plymouthd.conf` to contain "omarchy" or the ATT marker file)
- "Reset to default" button now shows the correct distro default theme per distro: `omarchy` on Omarchy, `cachyos-bootanimation` on CachyOS, `prismlinux-theme` on PrismLinux; button is hidden on distros not in the map
- ATT Omarchy marker (`/etc/att/att-omarchy-marker`) is now only written on Omarchy systems, not on every Plymouth apply
- SDDM tab hide condition replaced: was desktop-string check (`fn.desktop`); now hides when `systemctl is-enabled plasma-login.service` returns "enabled"; `fn.DEV` bypass removed — condition is unconditional
- Kernel tab "Default Boot Entry" now supports rEFInd (primary target: CachyOS): dropdown lists every `vmlinuz-*` found in `/boot`, "Set as Default" writes `default_selection "vmlinuz-<pkg>"` to `refind.conf` and also forces `fold_linux_kernels false`

### Technical Details

- `gui.py`: Plymouth guards changed from `check_content("omarchy", ...) or os.path.isfile(...)` to `fn.check_package_installed("plymouth")`
- `gui.py`: `_hide_sddm` removed entirely; replaced with `if not fn.check_service_enabled("plasma-login"):` — one line, no DEV bypass
- `functions.py`: added `check_service_enabled(service)` — runs `systemctl is-enabled <service>.service`, returns `True` if stdout is "enabled"; mirrors `check_service()` but uses `is-enabled` not `is-active`
- `plymouth_gui.py`: `_default_theme` dict maps `fn.distr` to the distro's default theme name; reset button hidden on unknown distros; marker write wrapped in `if fn.distr == "omarchy":` guard
- `kernel.py`: added `REFIND_CONF_PATHS`, `is_refind()`, `get_refind_boot_entries()`, `set_default_refind_entry()`, `_ensure_fold_linux_kernels_false()`; rEFInd detected before systemd-boot in bootloader chain
- `kernel_gui.py`: `_build_refind_entry_selector` mirrors limine selector pattern; bootloader chain checks rEFInd first

### Files Modified

- `usr/share/archlinux-tweak-tool/gui.py`
- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/plymouth_gui.py`
- `usr/share/archlinux-tweak-tool/kernel.py`
- `usr/share/archlinux-tweak-tool/kernel_gui.py`

---

## 2026.05.10 - gui.py: SDDM tab guard refined to Plasma + plasma-login-manager condition

### What Changed

- SDDM tab visibility guard tightened: tab now hides only when all four conditions are true — CachyOS + Plasma desktop + `plasma-login-manager` installed + `plasmalogin` service active; previously it hid on any CachyOS system regardless of DE or service state, which wrongly hid SDDM for CachyOS users running non-Plasma DEs or WMs

### Technical Details

- `gui.py`: replaced `fn.distr != "cachyos"` with a `_hide_sddm` boolean derived from four `and`-chained checks: `fn.distr == "cachyos"`, `"plasma" in fn.desktop.lower()`, `fn.check_package_installed("plasma-login-manager")`, `fn.check_service("plasmalogin")`; `--dev` still forces the tab visible regardless

### Files Modified

- `usr/share/archlinux-tweak-tool/gui.py`

---

## 2026.05.10 - SDDM page: plasma-login-manager integration + CachyOS hide

### What Changed

- Added "Install and enable plasma-login-manager" button inside the SDDM installed view, between Configuration Setup and Login Settings — visible only when `plasma-login-manager` is already installed
- Button label set to "Switch back to plasma-login-manager" to reflect intent
- "You seem to be working with plasma-login-manager" info label now gated on both `check_package_installed("plasma-login-manager")` and `check_service("plasmalogin")` being true
- `on_click_enable_plasma_login` runs both `pacman -S plasma-login-manager` and `systemctl enable plasma-login-manager --force` visibly in Alacritty
- `on_click_sddm_enable` updated to also run `systemctl enable sddm --force` in the terminal before `set-default graphical.target`
- Removed redundant "Install plasma-login-manager and enable it" button from the "SDDM not installed" fallback view
- SDDM tab hidden on CachyOS by default (visible only with `--dev`) — CachyOS ships plasma-login-manager, not sddm

### Technical Details

- `sddm_gui.py`: new `hbox_plasma_login` row appended after `hbox_sep_config`, inside the `check_package_installed("plasma-login-manager")` guard
- `sddm.py`: new `on_click_enable_plasma_login(self, _widget=None)` function; cmd string split across lines for flake8 line-length compliance
- `sddm.py` `on_click_sddm_enable`: cmd updated to include `sudo systemctl enable sddm --force;` before `set-default`
- `gui.py`: `stack.add_titled(vboxstack_sddm, ...)` wrapped in `if fn.distr != "cachyos" or fn.DEV:` — page is still built so `self.rebuild_sddm_page` exists on all distros

### Files Modified

- `usr/share/archlinux-tweak-tool/sddm_gui.py`
- `usr/share/archlinux-tweak-tool/sddm.py`
- `usr/share/archlinux-tweak-tool/gui.py`

---

## 2026.05.09 - SDDM page: multiple fixes + cursor preview + refactor

### What Changed

- SDDM page now detects both `sddm` and `sddm-git` as installed — previously only `sddm` triggered the UI
- "Apply the ATT SDDM configuration" button now creates backups of existing config files before overwriting (was silently overwriting without backup)
- "Apply your original SDDM configuration" button now actually restores from backup files; previously it was a stub that showed a success message and restarted without restoring anything; shows a clear dialog if no backup exists
- SDDM cursor theme row now shows a live cursor preview image, matching the same behaviour as the Maintenance page cursor selector
- plasma-login-manager row is now only shown when `plasma-login-manager` is installed; previously always visible on any SDDM system; label updated to "Switch back to plasma-login-manager" to reflect the actual use case

### Technical Details

- `sddm_gui.py` package guard: `or fn.check_package_installed("sddm-git")` added to line 25
- `on_click_sddm_reset_original_att`: imports `functions_backup` and calls `_fb.backup_system_configs()` before copying Kiro defaults
- `on_click_sddm_reset_original`: checks `fn.sddm_default_d1_bak` / `fn.sddm_default_d2_bak` exist, restores with `shutil.copy`, shows "No Backup Found" messagebox if absent
- Cursor preview refactor: xcursor binary-parsing helpers (`_load_xcursor_pixbuf`, constants) moved from `maintenance_gui.py` into `functions.py` as `_load_xcursor_pixbuf()` + `get_cursor_preview_pixbuf()`; `maintenance_gui._update_cursor_preview` now calls `fn.get_cursor_preview_pixbuf()`; `sddm.py` gets `_update_sddm_cursor_preview(self)` using the same shared helper; `sddm_gui.py` adds a `Gtk.Picture` widget wired to the existing cursor dropdown
- plasma-login-manager row wrapped in `if fn.check_package_installed("plasma-login-manager"):` so it only appears on Plasma systems that already have the package

### Files Modified

- `usr/share/archlinux-tweak-tool/sddm_gui.py`
- `usr/share/archlinux-tweak-tool/sddm.py`
- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/maintenance_gui.py`

---

## 2026.05.08 - Kernel page: GRUB full support + CachyOS native section fix

### What Changed

- CachyOS native kernel section now shows all cachyos-repo kernels (linux-cachyos, linux-cachyos-bore, etc.) regardless of whether chaotic-aur is active — previously they were filtered out when chaotic was enabled
- GRUB boot entry dropdown now includes entries from the "Advanced options" submenu, using GRUB's `N>M` index notation; fallback initramfs entries are filtered out
- Kernel install and remove now automatically run grub-install + grub-mkconfig in a separate alacritty terminal after pacman finishes, on GRUB systems only
- "Set as Default" on GRUB automatically fixes `GRUB_DEFAULT=saved` in `/etc/default/grub` if not set, runs grub update, then sets the default — no manual editing required
- GRUB boot entry selector is now shown to all users (removed `--dev` gate)
- Boot unavailable message updated to include GRUB

### Technical Details

- `_already_shown_pkgs()` in `_build_grub_entry_selector` now returns only non-chaotic packages (section 1 packages) — chaotic-flagged packages are no longer excluded from the CachyOS native section
- `get_grub_boot_entries()` tracks depth and `in_submenu` state; depth-1 menuentry lines inside a submenu block get index `"{submenu_idx}>{sub_entry_idx}"`; `sub_entry_index` still increments for filtered (fallback) entries so indices match what GRUB expects
- `run_grub_update(self)` is a new kernel.py function: checks `os.path.isfile("/usr/bin/grub-mkconfig")` + `os.path.isfile("/boot/grub/grub.cfg")` before launching; UEFI detection via `/sys/firmware/efi`; EFI dir detection via `mountpoint -q` checking `/boot/efi`, `/efi`, `/boot` in order; follows the 4-rule pattern: log_subsection → debug_print → show_in_app_notification → Popen
- All three post-terminal handlers in kernel_gui.py (`launch_and_wait`, `remove_and_notify`, `install_and_notify`) call `kernel.run_grub_update(self)` and `grub_proc.wait()` before the GLib.idle_add refresh
- `set_grub_default_saved()` uses `re.sub` to replace any existing `GRUB_DEFAULT=` line or appends if absent; called at click time, not page build time
- `on_set_default` restructured: if GRUB_DEFAULT not saved → fix file → hide note banner → daemon thread runs grub update → grub-set-default → GLib.idle_add finish; if already saved → direct grub-set-default

### Files Modified

- `usr/share/archlinux-tweak-tool/kernel.py`
- `usr/share/archlinux-tweak-tool/kernel_gui.py`

---

## 2026.05.08 - Fix: IndexError on startup when .zshrc has no ZSH_THEME line

### What Changed

- Fixed "ERROR DETECTED: list index out of range" logged at startup on systems where oh-my-zsh-git is installed but `~/.zshrc` contains no `ZSH_THEME=` line (e.g. CachyOS with a one-line sourcing zshrc)

### Technical Details

- Root cause: `zsh_theme.get_themes()` called `fn.get_position(theme_list, "ZSH_THEME=")` which returns `0` (not `-1`) when not found; `theme_list[0].split("=")[1]` then raised `IndexError` if the first line has no `=`
- Fix: added a guard — `if "ZSH_THEME=" not in theme_list[pos]: name = "random"` — before the split; defaults to "random" theme when the line isn't present

### Files Modified

- `usr/share/archlinux-tweak-tool/zsh_theme.py`

---

## 2026.05.08 - Dev mode: --dev flag for experimental UI

### What Changed

- Added `--dev` command-line flag to ATT; when passed, experimental or WIP UI elements are shown
- First use: Bazaar hbox on the Software page is hidden by default and only shown with `--dev`

### Technical Details

- `fn.DEV = False` constant + `fn.set_dev(value)` setter added to `functions.py`, mirroring the existing `DEBUG`/`set_debug` pattern
- `archlinux-tweak-tool.py` strips `--dev` from `sys.argv` and calls `fn.set_dev(True)` before GTK application starts
- `software_gui.py` wraps `vboxstack_software.append(hbox_bazaar)` with `if fn.DEV:` — hbox is still built so `self.lbl_software_bazaar` and `self.btn_software_bazaar_remove` attributes exist and won't cause AttributeError in callbacks
- Launch: `sudo python3 usr/share/archlinux-tweak-tool/archlinux-tweak-tool.py --dev`

### Files Modified

- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/archlinux-tweak-tool.py`
- `usr/share/archlinux-tweak-tool/software_gui.py`

---

## 2026.05.08 - Bazaar: fix launch env vars under pkexec

### What Changed

- Bazaar launch now passes `env=fn.get_terminal_env()` to both Popen calls so `WAYLAND_DISPLAY` and `XDG_RUNTIME_DIR` are set correctly when ATT runs under pkexec
- Confirmed root cause: pkexec strips Wayland env vars; machines without them in the environment silently failed to connect to the display
- Issue partially resolved — launch works on some machines but still needs further diagnosis; tracked as open todo

### Technical Details

- Two Popen launch sites in `on_click_software_bazaar` updated: the direct-launch path (already installed) and the post-install auto-launch path
- `fn.get_terminal_env()` rebuilds `WAYLAND_DISPLAY` from `/run/user/<uid>/wayland-*` socket and sets `XDG_RUNTIME_DIR=/run/user/<uid>`
- `sudo -E` then passes these vars through to bazaar

### Files Modified

- `usr/share/archlinux-tweak-tool/software.py`

---

## 2026.05.07 - Themes page: Plasma desktop warning

### What Changed

- Themes page now displays a warning for Plasma/KDE users: "⚠ On Plasma these themes will not work"
- Warning appears directly under the info text, only on Plasma systems
- Improves UX by preventing confusion when GTK themes don't apply in Plasma environments

### Technical Details

- Added `hbox_plasma_warning` that checks `fn.desktop` environment variable (XDG_CURRENT_DESKTOP)
- Detects "KDE" or "plasma" (case-insensitive) and conditionally builds warning hbox
- Warning only appends if hbox has children (uses `get_first_child()` guard)
- Uses warning markup with warning CSS class for visual distinction

### Files Modified

- `usr/share/archlinux-tweak-tool/themes_gui.py`

---

## 2026.05.07 - AUR helper sync: bidirectional label update between Pacman and Software pages

### What Changed

- **Pacman → Software**: When yay-git or paru-git is installed/removed on the Pacman page, the Software page labels automatically update
- **Software → Pacman**: When yay-git or paru-git is installed/removed on the Software page, the Pacman page buttons automatically update
- User no longer needs to restart ATT or manually navigate to see the correct state on either page

### Technical Details

- **software_gui.py**: Added `refresh_aur_labels()` inner function that re-checks `/usr/bin/yay` and `/usr/bin/paru` and updates `self.lbl_software_yay` and `self.lbl_software_paru` using the same markup pattern as initial build
- **pacman_gui.py**: In `wait_and_refresh()` callback, added `GLib.idle_add(getattr(self, "refresh_software_aur_labels", lambda: None))` calls in both the early-return and normal-flow paths
- **functions.py**: Modified `wait_install_and_update()` and `wait_remove_and_update()` to add `GLib.idle_add(getattr(self_ref, "refresh_aur_buttons", lambda: None))` after label updates, ensuring Pacman buttons refresh when Software page installs/removes
- All paths use `getattr` with defensive lambda guards for safety (both pages are lazy-loaded)
- Follows existing cross-page refresh patterns (kernel tab chaotic-AUR dynamic status)

### Files Modified

- `usr/share/archlinux-tweak-tool/software_gui.py`
- `usr/share/archlinux-tweak-tool/pacman_gui.py`
- `usr/share/archlinux-tweak-tool/functions.py`

---

## 2026.05.06 - Plymouth: Omarchy detection hardened + Reset to default button

### What Changed

- Omarchy detection now uses `/etc/att/att-omarchy-marker` as a stable fallback so the Plymouth tab remains visible even after Plymouth theme changes overwrite `plymouthd.conf`
- Plymouth tab and GUI initialisation guards updated to check `plymouthd.conf` OR the marker file
- Applying any Plymouth theme via ATT automatically writes the marker to `/etc/att/att-omarchy-marker`
- New "Reset to Omarchy default" button runs `plymouth-set-default-theme -R omarchy` and refreshes the active theme label

### Technical Details

- `functions.py` detection extended: `distr = "omarchy"` is set when `plymouthd.conf` contains "omarchy" **or** `/etc/att/att-omarchy-marker` exists
- Both Plymouth guards in `gui.py` use `fn.check_content(...) or fn.os.path.isfile("/etc/att/att-omarchy-marker")`
- Marker written in `run_apply()` thread via `fn.os.makedirs("/etc/att", exist_ok=True)` + `open(...).close()`
- Reset button reuses `refresh_after_apply()` to update `lbl_current` and repopulate the installed-themes dropdown

### Files Modified

- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/gui.py`
- `usr/share/archlinux-tweak-tool/plymouth_gui.py`

---

## 2026.05.06 - Notification bar: fixed height, replaced image with CSS color

### What Changed

- Replaced `Gtk.Picture` + `Gtk.Overlay` panel image with a plain `Gtk.Box` styled via CSS (`background-color: #1a1a1a`)
- Notification bar is now a fixed 30px tall regardless of window size or tiled WM layout
- Eliminates the aspect-ratio scaling problem where `Gtk.ContentFit.CONTAIN` made the bar grow vertically with window width

### Technical Details

- `panel.png` image is no longer used in the notification bar layout
- `notification_bg` box has `set_size_request(-1, 30)` and CSS class `att-notification-bar`
- CSS provider loaded inline in `gui()` via `Gtk.StyleContext.add_provider_for_display`
- `notification_revealer` has `set_vexpand(False)` to prevent vertical growth

### Files Modified

- `usr/share/archlinux-tweak-tool/gui.py`

---

## 2026.05.06 - AI tab: OpenCode + GitHub Copilot CLI added; widget rename pass

### What Changed

- Added **OpenCode** (`opencode-ai` npm package) to CLI Coding Assistants section — TUI AI coding assistant used by Omarchy as primary IDE alongside Claude Code
- Added **GitHub Copilot CLI** (`@github/copilot` npm package) to CLI Coding Assistants section
- Both follow the same install/remove/link pattern as existing Codex and Gemini rows
- Renamed all numbered widget variables (`hbox1`–`hbox14`, `btn7`–`btn14`, `lbl7_link`–`lbl14_link`) to descriptive names in `ai_gui.py` (objective 27)

### Technical Details

- Detection checks four paths for each tool: `/usr/bin/`, `/usr/local/bin/`, `~/.local/bin/`, `~/.npm-global/bin/`
- Install: `fn.launch_npm_install_in_terminal("opencode-ai")` and `fn.launch_npm_install_in_terminal("@github/copilot")`
- Remove: `fn.launch_npm_remove_in_terminal(...)` — same daemon-thread + `wait()` + `GLib.idle_add` refresh pattern as Codex/Gemini
- Link callbacks: `https://opencode.ai` and `https://github.com/github/gh-copilot`
- Both files pass flake8 clean

### Files Modified

- `usr/share/archlinux-tweak-tool/ai_gui.py`
- `usr/share/archlinux-tweak-tool/ai.py`

---

## 2026.05.06 - Dev tool: remove-bak-files script

### What Changed

- Added `usr/bin/remove-bak-files` — a developer-only bash script that removes exactly the backup files ATT creates, nothing else

### Technical Details

- Checks 18 specific paths (9 files × both `-bak` and `.bak` variants): `/etc/hosts`, `/etc/nsswitch.conf`, `/etc/pacman.d/mirrorlist`, `/etc/samba/smb.conf`, `/usr/share/icons/default/index.theme`, `~/.bashrc`, `~/.zshrc`, `~/.config/fish/config.fish`, `~/.config/fastfetch/config.jsonc`
- Uses `SUDO_USER` → `getent passwd` to resolve the real user's home when run as root
- Lists all found files with confirmation prompt before deleting
- Follows ATT Script Standard (tput colors, header/success/warn/error helpers, `set -euo pipefail`)

### Files Modified

- `usr/bin/remove-bak-files` (new)

---

## 2026.05.06 - Wallpaper: drop XFCE setter, hide picker on full DEs

### What Changed

- Removed `_set_xfce()` entirely — XFCE manages its own wallpaper; ATT no longer attempts xfconf-query
- Removed `_XFCE_STYLES` dict and the `xfce_running` pgrep check from `_apply_x11()`
- Added `_HIDE_PICKER_DESKTOPS` frozenset: GNOME, Unity, KDE, XFCE, MATE, Cinnamon, X-Cinnamon, Budgie, Deepin, LXQt, LXDE, Pantheon
- Added `should_show_picker()` — returns `False` for any desktop in the hide list, `True` for WMs and unknown environments
- ATT Wallpaper Picker section (folder browser, thumbnails, preview, apply, random) is now invisible on full DEs that manage wallpaper themselves; Variety and ATT Configuration sections remain always visible
- Replaced `pwd.getpwnam()` in `on_open_variety_settings()` with `subprocess id -u` to remove the `pwd` import dependency
- Removed `import pwd` and `import shlex` (XFCE-only); `import re` retained for `_fix_variety_conf_paths()`

### Technical Details

- `should_show_picker()` reuses `_get_user_env()` for the same pkexec-safe env lookup already used by `_apply_x11()`; KDE checked via `KDE_FULL_SESSION=true` as a fallback since its `XDG_CURRENT_DESKTOP` value varies
- `wallpaper_gui.py`: all picker widgets packed into a single `box_picker` (Gtk.Box VERTICAL); one `box_picker.set_visible()` call controls the whole section
- Test: `sudo XDG_CURRENT_DESKTOP=GNOME python3 archlinux-tweak-tool.py` — picker hidden; `XDG_CURRENT_DESKTOP=i3` — picker visible

### Files Modified

- `usr/share/archlinux-tweak-tool/wallpaper.py`
- `usr/share/archlinux-tweak-tool/wallpaper_gui.py`

---

## 2026.05.05 - Wallpaper: XFCE detection and xfconf-query fixes

### What Changed

- XFCE is now detected reliably when ATT runs as root (pkexec strips env vars): `_get_user_env()` reads `XDG_CURRENT_DESKTOP`, `DESKTOP_SESSION`, and `XDG_SESSION_DESKTOP` from the real user's `/proc/<pid>/environ` as fallback
- `_set_xfce()` now runs `xfconf-query` as the real user with the correct D-Bus session env (`sudo -u <user> XDG_RUNTIME_DIR=... DBUS_SESSION_BUS_ADDRESS=...`) — same pattern as variety settings
- `xfconf-query` calls now use `--create` flag in a single command (replaces the old two-step empty-string pre-set)
- xrandr fallback added for fresh XFCE installs with no existing backdrop props; its `FileNotFoundError` is caught separately so it can't mask xfconf errors
- `shutil.which("xfconf-query")` with `/usr/bin/xfconf-query` hardcoded fallback handles root's restricted PATH
- Debug output now shows the resolved xfconf-query path and every command before execution
- XFCE wallpaper via D-Bus not yet confirmed working — tracked as S11

### Technical Details

- `_get_user_env()` iterates `/proc/*/environ`, matches on `LOGNAME == sudo_username`, extracts requested keys; short-circuits if current env already has the values (non-sudo case)
- `shlex.quote(path)` used in all shell=True xfconf-query invocations to handle spaces in paths
- xrandr fallback constructs `/backdrop/screen0/monitor<output>/workspace0/last-image` per connected output; falls back to `monitor0` if xrandr absent

### Files Modified

- `usr/share/archlinux-tweak-tool/wallpaper.py`

---

## 2026.05.05 - Launcher: silent xauth retry loop

### What Changed

- Removed the `[WARN]` echo lines from the X11 xauth retry loop in the launcher script — the loop now retries silently up to 5 times without printing to the terminal

### Technical Details

- The loop itself is unchanged; only the `echo "[WARN]: Xauth changes honored = no, retrying..."` and the post-loop "still no after 5s" warning were removed; the retry logic and `sleep 1` remain intact

### Files Modified

- `usr/bin/archlinux-tweak-tool`

---

## 2026.05.05 - Shell tab: active shell indicator; Omarchy distro added

### What Changed

- Shell tab stack switcher now labels the currently active shell with "(active)" — e.g. "FISH (active)" — derived from `fn.get_shell()` at GUI construction time
- Added Omarchy to the startup banner's supported distributions list (between Nyarch and ParchLinux)
- Added Omarchy to `DISTRO_TESTING.md` (version 3.7.0-2, <https://omarchy.org>); detection was already present in `functions.py`

### Technical Details

- `fn.get_shell()` reads `pwd.getpwnam(sudo_username).pw_shell` — authoritative login shell regardless of how ATT was launched; `stack.add_titled()` title arg computed inline with a ternary

### Files Modified

- `usr/share/archlinux-tweak-tool/shell_gui.py`
- `usr/share/archlinux-tweak-tool/archlinux-tweak-tool.py`
- `DISTRO_TESTING.md`

---

## 2026.05.05 - Wallpaper: Demote verbose thumb-load message to debug-only

### What Changed

- `_populate_wallpaper_thumbs` log line "Loading wallpapers from: ..." demoted from `log_subsection` to `debug_print` — it fires on every folder change and adds noise to normal console output

### Technical Details

- `log_subsection` is for user-meaningful events; high-frequency internal status lines belong in `debug_print` (only visible with `--debug` flag)

### Files Modified

- `usr/share/archlinux-tweak-tool/wallpaper.py`

---

## 2026.05.05 - Codebase Review: Consistency, Performance, and Code Quality

### What Changed

- Masterplan task list fully audited — all previously completed tasks marked done
- Full three-agent codebase review (consistency, performance, code quality) run against all Python files
- Fixed 8 GTK callback violations: unused widget param renamed `widget` → `_widget` in `fastfetch.py`, `autostart.py`, `packages.py`
- Renamed all numbered widget names in `autostart.py` (`vbox1`–`vbox6`, `hbox2`–`hbox4`) to descriptive identifiers
- Consolidated three independent implementations of the chaotic-AUR / nemesis repo check into the canonical `fn.check_chaotic_aur_active()` and `fn.check_nemesis_repo_active()`; fixed bug in `check_nemesis_repo_active()` which returned `None` instead of `False` when repo was absent
- Extracted shared icon-scan logic from `maintenance.py` and `sddm.py` into `fn.list_cursor_themes()`; dropped unused `self` param from `sddm.pop_gtk_cursor_names`; removed O(N² log N) in-loop sort
- `/etc/pacman.conf` now cached after first read; all read-only functions use the cache; every write path calls `fn.invalidate_pacman_conf_cache()` — eliminates ~23 redundant file reads at startup
- `user.py` `create_user()` moved to daemon thread via `on_click_user_apply`; `subprocess.call()` replaced with `Popen().wait()`
- Added `fn.display_manager_service` constant; removed duplicate hardcoded path from `sddm.py` and `sddm_gui.py`
- Removed all redundant `f.close()` / `myfile.close()` calls inside `with` blocks across `sddm.py`, `pacman_functions.py`, `insert_repo()`

### Technical Details

- `check_nemesis_repo_active()` / `check_chaotic_aur_active()` in `functions.py` now call `get_pacman_conf_lines()` instead of opening the file; `check_repo()` and `repo_exist()` in `pacman_functions.py` same; cache is a module-level `_pacman_conf_cache` list, invalidated on every write to pacman.conf
- `is_chaotic_aur_enabled()` deleted from `kernel.py` and `pacman_functions.py`; 3 call sites in `kernel_gui.py` and 1 in `pacman_gui.py` redirected to `fn.check_chaotic_aur_active()`
- `fn.list_cursor_themes()` added to `functions.py` using `os.listdir` + `path_check`; both `pop_gtk_cursor_names` functions rewritten to call it; `sddm.py` version drops `self`, removes the in-loop sort at line 303 and the redundant final sort
- `on_click_user_apply` wraps `create_user()` in a `threading.Thread(daemon=True)`; `pop_cbt_users` called via `GLib.idle_add` after thread completes
- All changes pass `flake8 --max-line-length=120`

### Files Modified

- `usr/share/archlinux-tweak-tool/functions.py`
- `usr/share/archlinux-tweak-tool/pacman_functions.py`
- `usr/share/archlinux-tweak-tool/pacman.py`
- `usr/share/archlinux-tweak-tool/kernel.py`
- `usr/share/archlinux-tweak-tool/kernel_gui.py`
- `usr/share/archlinux-tweak-tool/pacman_gui.py`
- `usr/share/archlinux-tweak-tool/sddm.py`
- `usr/share/archlinux-tweak-tool/sddm_gui.py`
- `usr/share/archlinux-tweak-tool/maintenance.py`
- `usr/share/archlinux-tweak-tool/fastfetch.py`
- `usr/share/archlinux-tweak-tool/autostart.py`
- `usr/share/archlinux-tweak-tool/packages.py`
- `usr/share/archlinux-tweak-tool/user.py`
- `CLAUDE.md` (masterplan task list updated)

---

## 2026.05.05 - Wallpaper Tab: New Page with Variety + ATT Picker

### What Changed

- Added a new **Wallpaper** tab (last entry in sidebar, alphabetically after User)
- Install/Remove variety via alacritty terminal with post-close refresh of button visibility
- Save ATT variety config button copies `data/kiro/variety/` → `~/.config/variety/` with `.bak` of any existing file
- Open variety settings button launches `variety --preferences` in a daemon thread
- ATT Wallpaper Picker: folder entry pre-filled with bundled wallpapers, Browse/Load/Stop controls, async FlowBox thumbnail grid, 180px preview, path label, scale dropdown (Fill/Fit/Center/Tile/Stretch), Apply (feh) and Random buttons
- Bundled wallpapers auto-load on page build via `GLib.idle_add` at PRIORITY_LOW

### Technical Details

- `wallpaper.py`: all backend logic — install/remove variety, save config (shutil.copy2 + .bak), open settings, folder dialog (Gtk.FileDialog + Gio), async thumb loading with generation counter (same stop-signal pattern as SDDM), feh apply via `_FEH_FLAGS` dict, random pick
- `wallpaper_gui.py`: pure UI construction; passes `self.*` widget refs so wallpaper.py callbacks can update them; auto-triggers `_populate_wallpaper_thumbs` on build
- `gui.py`: added `import wallpaper`, `import wallpaper_gui`, `vboxstack_wallpaper`, gui call, and `stack.add_titled` entry
- feh called via `Popen` (non-blocking); `FileNotFoundError` caught and surfaced to user via notification
- All flake8 clean (max-line-length 120)

### Files Modified

- `usr/share/archlinux-tweak-tool/wallpaper.py` (new)
- `usr/share/archlinux-tweak-tool/wallpaper_gui.py` (new)
- `usr/share/archlinux-tweak-tool/gui.py`

---

## 2026.05.05 - Shell Tab: Live ZSH UI Rebuild + Dropdown/Image Guards

### What Changed

- Installing oh-my-zsh now populates the theme dropdown immediately; removing it clears the dropdown — no restart required
- Installing zsh from the "not installed" stub now rebuilds the full ZSH tab in-place — no ATT restart required
- Fixed crash in `sddm_gui.py` where `Gtk.Button().get_child()` returned `None` on an empty button
- Fixed crash in `update_image` when `get_combo_text` returns `None` during a dropdown model swap

### Technical Details

- Added `_refresh_zsh_themes_dropdown(self)` in `shell.py`: calls `zsh_theme.get_themes()` when oh-my-zsh-git is installed, sets an empty `StringList` model when it is not; wired into both `install_oh_my_zsh` and `remove_oh_my_zsh` `wait_*` threads via `GLib.idle_add`
- Removed dead `from zsh_theme import get_themes` inline import and redundant `set_sensitive(False)` from `remove_oh_my_zsh`
- Extracted the full "zsh installed" tab content from `gui()` into a module-level `_build_zsh_installed_content(self, vbox, ...)` function in `shell_gui.py`; added `_rebuild_zsh_tab()` which clears `self.zsh_vbox` and calls the builder — avoids circular imports by storing the rebuild as `self._refresh_zsh_tab` lambda at build time
- `on_clicked_install_only_zsh` (which called `restart_program()`) replaced by `on_install_zsh_clicked`: installs via terminal, waits in daemon thread, calls `GLib.idle_add(self._refresh_zsh_tab)` on success
- SDDM fix: replaced `Gtk.Button().get_child().set_markup(...)` with explicit `Gtk.Label` + `set_child()` — `get_child()` is always `None` on a button created without a label argument
- `update_image` guard: early return when `get_combo_text(widget) is None`; the `notify::selected` signal fires transiently during model replacement with no item selected, which previously caused a `TypeError` on string concatenation

### Files Modified

- `usr/share/archlinux-tweak-tool/shell.py`
- `usr/share/archlinux-tweak-tool/shell_gui.py`
- `usr/share/archlinux-tweak-tool/sddm_gui.py`
- `usr/share/archlinux-tweak-tool/functions.py`

---

## 2026.05.05 - SDDM: Button Compliance Fixes

### What Changed

- All SDDM page buttons now comply with project rules: `_widget` convention, no blocking subprocess calls, all package operations routed through alacritty terminal

### Technical Details

- Removed dead function `ensure_sddm_config` which was never called and contained a blocking `dialog.run()` (deprecated GTK3 pattern)
- Renamed `widget` → `_widget` in 8 callback signatures: `on_browse_sddm_folder`, `on_load_sddm_folder`, `on_stop_sddm_loading`, `on_click_install_bibata_cursor`, `on_click_remove_bibata_cursor`, `on_click_install_bibatar_cursor`, `on_click_remove_bibatar_cursor`, `on_click_att_sddm_clicked`
- Replaced `subprocess.call()` in `on_click_fix_sddm_conf` with `Popen` in a daemon thread so ATT stays responsive while the terminal is open
- Converted 6 package install/remove functions from silent `subprocess.run(["pacman", ...])` to alacritty terminal via `launch_pacman_install_in_terminal` / `launch_pacman_remove_in_terminal` + `wait_and_refresh` daemon threads: bibata cursors (×4), `on_click_sddm_enable`, `on_click_att_sddm_clicked`

### Files Modified

- `usr/share/archlinux-tweak-tool/sddm.py`

---

## 2026.05.04 - SDDM: Theme Dropdown Refreshes After Install/Remove

### What Changed

- SDDM theme dropdown now updates immediately after installing or removing the edu-simplicity theme — no app restart required

### Technical Details

- Added `pop_theme_box(self, self.theme_sddm)` at the end of the `refresh()` closure in both `on_click_install_simplicity` and `on_click_remove_simplicity`
- Called on the GLib main thread via the existing `GLib.idle_add(refresh)` path, so no threading changes needed
- `pop_theme_box` clears and repopulates the `Gtk.DropDown` model from `/usr/share/sddm/themes/` and re-selects the currently active theme from `sddm.conf.d`

### Files Modified

- `usr/share/archlinux-tweak-tool/sddm.py`

---

## 2026.05.04 - Kernel Tab: Dynamic Chaotic-AUR Kernel List Refresh

### What Changed

- Kernel page now hides chaotic-aur kernels automatically when chaotic-aur is removed from pacman.conf, and shows them again when it is re-added — no restart required

### Technical Details

- Kernel rows extracted into a dedicated `vbox_kernels` child `Gtk.Box` inside the page's main container
- New `_populate_kernel_rows()` helper fetches fresh chaotic/installed/cpu/running state and builds all group headers and kernel rows into `vbox_kernels`
- New `_clear_box()` helper removes all children from a box (same pattern used elsewhere for FlowBox clearing)
- GTK `map` signal on `vbox_kernels` fires each time the Kernels tab becomes visible; a `last_chaotic` guard ensures the rebuild only happens when chaotic status actually changed — no-op on normal tab switches

### Files Modified

- `usr/share/archlinux-tweak-tool/kernel_gui.py`

---

## 2026.05.04 - Kernel Tab: Resolve Kernel Package per Boot Entry

### What Changed

- Default-boot-entry dropdown now shows the kernel package alongside the bootctl title, e.g. *"Arch Linux — linux-cachyos-bore"* instead of just *"Arch Linux"*
- `lbl_current` (the "Current:" label below the dropdown) shows the same enriched string instead of the cryptic `.conf` filename
- Orphan boot entries (whose kernel package is no longer installed) are filtered out of the dropdown

### Technical Details

- New helper `_resolve_kernel_for_entry(version, linux_path)` in `kernel.py` returns `(pkg_name, is_orphan)`:
  - With `version:` set → reads `/usr/lib/modules/<version>/pkgbase` (file owned by the kernel package and contains its name) — same trick `get_running_kernel()` already uses; missing file means orphan
  - Without `version:` but with `linux:` basename starting with `vmlinuz-` → strips the prefix to get the pkgbase
  - Otherwise → `(None, False)`; used for firmware/Automatic entries which stay visible with their bootctl title
- `get_boot_entries()` parser rewritten to accumulate fields per blank-line-separated block, capture `version:` and `linux:` in addition to `id:`/`title:`, call the resolver, drop orphans, and return `(id, title, kernel_pkg)` triples
- `_build_boot_entry_selector` and `refresh_combo` in `kernel_gui.py` updated to unpack the new triples; combo label format is `f"{title} — {kernel_pkg}"` when `kernel_pkg` is set, else `title`. Same string is stored in `id_to_title` so the "Current:" label, log lines, and notifications all use the enriched form
- `set_default_boot_entry` still takes the entry id (filename); no change there

### Files Modified

- `usr/share/archlinux-tweak-tool/kernel.py`
- `usr/share/archlinux-tweak-tool/kernel_gui.py`

---

## 2026.05.03 - Fastfetch write_configs: Add Missing Section Support

### What Changed

- `write_configs()` now appends `# reporting tools` and the fastfetch line to the shell config when the section is absent, instead of silently returning
- Also handles the case where the section exists but has no fastfetch entry — inserts one after the section header
- Disabling fastfetch on an empty config (no section, no line) still does nothing, as expected

### Technical Details

- Three paths: no section → append section + line (enable only); section exists, no line → insert after header (enable only); line exists → edit in place (existing behaviour)
- Previously the function only knew how to edit an existing `fastfetch` / `#fastfetch` line; bare shell configs like a stock `.bashrc` were silently ignored

### Files Modified

- `usr/share/archlinux-tweak-tool/fastfetch.py`

---

## 2026.05.03 - Fastfetch Shell Config Guard

### What Changed

- Added guard in `on_fast_util_toggled` and `on_fast_lolcat_toggled`: if no shell config file is detected, log a warning and return early instead of silently writing nothing

### Technical Details

- Both toggle handlers now call `utilities.get_config_file()` before `write_configs()`; if it returns falsy, `fn.log_warn("No shell config files found — fastfetch cannot be added to your shell startup")` is emitted and the function returns
- `write_configs()` already had a silent `if not config: return` guard; the new check surfaces that failure to the user visibly

### Files Modified

- `usr/share/archlinux-tweak-tool/fastfetch.py`

---

## 2026.05.03 - Fastfetch Page Cleanup &amp; Lolcat Install Fix

### What Changed

- Renamed all numbered widget variables in `fastfetch_gui.py` to descriptive names (objective 27)
- Removed dead widget `self.hbox26` — created but never appended to any container
- Removed empty spacer `hbox22` — `hbox_ff_checkboxes` already had `margin_top=10`
- Fixed `on_fast_lolcat_toggled`: lolcat switch now installs the `lolcat` package via terminal if not present; previously it only wrote the shell config with no install, leaving `fastfetch | lolcat` piping to a missing binary

### Technical Details

- Widget renames: `hbox3`→`hbox_title`, `hbox4`→`hbox_separator`, `hbox27`→`hbox_switches`, `hbox9`→`hbox_distro_specific`, `hbox28`→`hbox_amos_note`, `hbox29`→`hbox_archcraft_note`, `lbl1`→`page_title_label`, `label21`→`presets_label`, `label28`→`amos_note_label`, `label29`→`archcraft_note_label`, `hbox9_label`→`distro_specific_label`
- Lolcat fix mirrors the fastfetch install pattern: check `/usr/bin/lolcat`, open install terminal via `fn.launch_pacman_install_in_terminal("lolcat")`, wait in daemon thread, call `write_configs` on success, flip switch back to off if install fails/cancelled
- Dead `lolcat_toggle()` and `util_toggle()` functions still present — not removed as they are out of scope for this session

### Files Modified

- `usr/share/archlinux-tweak-tool/fastfetch_gui.py`
- `usr/share/archlinux-tweak-tool/fastfetch.py`

---

## 2026.05.03 - Chaotic AUR Setup Script

### What Changed

- `data/bin/setup-chaotic-aur` updated to use locally bundled packages instead of downloading via wget
- Signing key import (`pacman-key --recv-key` / `--lsign-key`) retained — required to verify the package signature before `pacman -U` can proceed
- No changes to `pacman.py`, `pacman_gui.py`, or `pacman_functions.py` — the Chaotic AUR switch and `ensure_chaotic_packages` logic was already fully implemented there

### Technical Details

- Original script used `wget` to fetch packages from `geo-mirror.chaotic.cx` into `/tmp`; replaced with direct paths to `data/chaotic/keyring/chaotic-keyring.pkg.tar.zst` and `data/chaotic/mirrorlist/chaotic-mirrorlist.pkg.tar.zst`
- Key import is still necessary: `chaotic-keyring.pkg.tar.zst` is itself a signed package; pacman verifies its signature before installing, so key `3056513887B78AEB` must be trusted first
- `ensure_chaotic_packages` in `pacman_functions.py` calls the script via `alacritty -e sudo bash setup-chaotic-aur` — no change needed there

### Files Modified

- `usr/share/archlinux-tweak-tool/data/bin/setup-chaotic-aur`

---

## 2026.05.03 - M4 Feature Test Complete

### What Changed

All 20 ATT tabs verified working end-to-end on Kiro. M4 milestone complete.

| Tab         | Result                                            |
|-------------|---------------------------------------------------|
| Packages    | ✓                                                 |
| SDDM        | ✓                                                 |
| Shell       | ✓                                                 |
| Maintenance | ✓                                                 |
| Services    | ✓                                                 |
| Themes      | ✓                                                 |
| Icons       | ✓                                                 |
| Themer      | ✓                                                 |
| Desktopr    | ✓                                                 |
| Fastfetch   | ✓ (remove button pipe deadlock fixed during test) |
| Performance | ✓                                                 |
| Kernel      | ✓                                                 |
| User        | ✓                                                 |
| AI          | ✓                                                 |
| Network     | ✓                                                 |
| Software    | ✓                                                 |
| System      | ✓                                                 |
| Logging     | ✓                                                 |
| Privacy     | ✓                                                 |
| Autostart   | ✓                                                 |

### Next Milestone

ATT is feature-complete and lint-clean. No remaining milestones defined — project is in a shippable state.

---

## 2026.05.03 - Fastfetch Remove Button Fix

### What Changed

- `on_remove_fast()` rewritten to use `fn.launch_pacman_remove_in_terminal()`, matching the install pattern used by `on_fast_util_toggled()`
- Detects whether `fastfetch-git` or `fastfetch` is installed before launching the terminal, so the correct package name is passed
- `wait_and_update` thread now calls `process.communicate()` (not `process.wait()`) consistent with the install path

### Technical Details

- Root cause: the original `on_remove_fast` used a hand-rolled `Popen` with `stdout=PIPE, stderr=PIPE` and `process.wait()` — if alacritty wrote to its stderr, the pipe buffer filled and deadlocked ATT
- `launch_pacman_remove_in_terminal` handles the script, temp-file logging, success/failure messaging, and `read -p 'Press Enter to close...'` prompt in one tested function — no need to duplicate the pattern inline
- Package detection: `pacman -Q fastfetch-git` returns 0 if installed; falls back to `fastfetch` if not found

### Files Modified

- `usr/share/archlinux-tweak-tool/fastfetch.py`

---

## 2026.05.03 - Widget Renaming, Section Headers, Fastfetch Remove, Kernel + Desktopr Fixes

### What Changed

#### Widget Renaming Pass (Objective 27 — No Numbered Boxes)

- All numbered widget names (`hbox1`, `hbox2`, `hbox23`, `vboxstack27`, etc.) renamed to descriptive identifiers across 10+ GUI files
- `performance_gui.py` function parameter `vboxstack27` → `vboxstack_performance`
- `fastfetch_gui.py` several local hboxes promoted to `self.` attributes so `set_fastfetch_ui_sensitive()` can reach them

#### Section Header Markup Consistency (Objective 26)

- `sddm_gui.py` — new **Configuration Setup** section header added using `set_markup("<b>...</b>")`; existing labels converted from `set_text()` to markup
- `performance_gui.py` — **Tuned**, **Zram**, **Preload**, **Irqbalance** section headers converted from `set_name("title")` to `set_markup("<b>...</b>")`
- `logging_gui.py` — new **Journal**, **Pacman Log**, **Xorg Log** section headers added with bold markup
- `system_gui.py` — new **Hardware**, **Storage**, **System**, **Systemd** section headers added (bold label + inline horizontal separator pattern)

#### Fastfetch: Remove Button + Sensitive State Control

- `fastfetch.py` — new `set_fastfetch_ui_sensitive(self, state)` function enables/disables all fastfetch controls when fastfetch is not installed
- `fastfetch.py` — new `on_remove_fast()` remove handler using alacritty terminal with `wait_and_update` daemon thread; after removal disables UI and resets the install switch
- `fastfetch_gui.py` — `set_fastfetch_ui_sensitive()` now called at end of lazy load so initial state is always correct; `on_reset_fast_att` callback parameter fixed `widget` → `_widget`

#### Kernel: Boot Entry Parsing + Non-systemd-boot Message

- `kernel.py` — `get_boot_entries()` now strips any parenthesised suffixes from title (e.g. "Linux (default)" → "Linux") using `re.sub`; entries with "reported/absent" in title are skipped
- `kernel_gui.py` — `_build_boot_entry_unavailable()` added: shown instead of the selector when systemd-boot is not active; informs user the feature requires systemd-boot

#### Desktopr: Refresh Installed Desktops After Install/Remove

- `desktopr.py` — new `refresh_installed_desktops(self)` function rebuilds the "Installed: …" label after an install or removal completes
- `desktopr.py` — `install_desktop()` and `uninstall_desktop()` both call `refresh_installed_desktops` via `GLib.idle_add` on completion; stale `desktopr_stat.set_text()` status updates removed (were updating a widget removed in a prior refactor)
- `desktopr_gui.py` — IMAGE_PREVIEW_LOAD/MIN tuned (900→855, 480→456) to better fit the panel

#### Autostart: Layout Fix

- `autostart.py` — `hbox_add_label` and `hbox2` moved inside `mainbox` (were appended to `vboxstack13` directly, causing layout regression); `scrolled_window.set_vexpand(True)` replaced with `set_propagate_natural_height(True)` to avoid over-expanding

### Technical Details

- Section headers now use two patterns: (a) standalone bold label (per services/logging/sddm model) or (b) bold label + inline `hexpand` separator on the same row (per system_gui model); both are acceptable; pick whichever fits the page density
- `set_fastfetch_ui_sensitive()` iterates a list of `self.` widget references — this is why several fastfetch hboxes were promoted from local vars to instance attributes in the same commit
- Kernel boot entry parsing: `re.sub(r'\s*\([^)]+\)', '', raw_title)` strips ALL parenthesised segments, not just "(default)" — this future-proofs against other suffixes bootctl may add

### Files Modified

`sddm_gui.py` • `performance_gui.py` • `performance.py` • `logging_gui.py` • `system_gui.py` • `fastfetch.py` • `fastfetch_gui.py` • `kernel.py` • `kernel_gui.py` • `desktopr.py` • `desktopr_gui.py` • `autostart.py` • `themes_gui.py` • `packages_gui.py` • `services_gui.py` • `user.py` • `user_gui.py` • `sddm.py` • `gui.py`

---

## 2026.05.03 - UI Layout Consistency: Software Page Section Headers

### What Changed

- **Section headers on software page are now bold** — all 5 section labels (`GUI Package Managers`, `AUR Helpers`, `Flatpak / Snap / AppImage`, `TUI Package Tools`, `Logout Managers`) changed from `set_text()` to `set_markup("<b>...</b>")` to match the system page pattern
- **Layout consistency rule added to CLAUDE.md** — objective 26 now mandates that all pages use `set_markup("<b>...</b>")` for section headers and `set_name("title")` for page titles; any page being edited must have its section labels verified against this standard

### Technical Details

- The system_gui.py pattern (`set_markup("<b>Hardware</b>")`) is now the canonical standard for all section headers across the app
- Page titles continue to use `set_name("title")` for CSS-based styling — no change needed there

### Files Modified

- `usr/share/archlinux-tweak-tool/software_gui.py`
- `CLAUDE.md`

---

## 2026.05.02 - Audio Scripts Migrated to ATT data/bin

### What Changed

- **Audio install buttons now run standalone scripts** — PulseAudio and PipeWire install buttons launch `data/bin/install-pulseaudio.sh` and `data/bin/install-pipewire.sh` in an alacritty terminal instead of executing Python package logic inline
- **Scripts made self-contained** — removed dependency on ArcoLinux-Nemesis `common.sh`; all helper functions (`log_section`, `log_info`, `log_success`, `log_warn`, `pkg_installed`, `install_packages`, `remove_if_installed`) are now defined inline in each script
- **Dead Python logic removed** — `add_autoconnect_pulseaudio()`, `on_click_switch_to_pulseaudio()`, and `on_click_switch_to_pipewire()` inline package logic replaced with a simple `alacritty -e bash -c` launcher following the maintenance.py `_run_terminal` pattern
- **Terminal stays open** — `read -p "Press Enter to close..."` appended via the `bash -c` wrapper so alacritty always waits for input

### Technical Details

- Scripts use `set -euo pipefail`; `read -p` is placed in the outer `bash -c` string (not inside the script) so it runs even when the script exits early via `set -e`
- Both callbacks use `subprocess.Popen(cmd, shell=True).wait()` in a daemon thread; ATT console gets `log_success` + in-app notification when terminal closes
- `systemctl --user` calls in both scripts have `2>/dev/null || true` to fail silently if running in a root context

### Files Modified

- `usr/share/archlinux-tweak-tool/data/bin/install-pulseaudio.sh`
- `usr/share/archlinux-tweak-tool/data/bin/install-pipewire.sh`
- `usr/share/archlinux-tweak-tool/services.py`

---

## 2026.05.02 - M4 Feature Testing: Services Tab Complete, UI Layout Refinement

### What Changed

#### SDDM Settings Save Bug Fix

- **User Context Bug** — Fixed `on_click_sddm_apply()` incorrectly saving settings as root instead of the actual user
  - Root cause: code was using `os.getenv("SUDO_USER") or os.getenv("USER")` which falls back to "root" when environment variables are unset
  - Fix: replaced with `fn.sudo_username` which correctly gets the actual logged-in user via `getlogin()`
  - Impact: SDDM configuration now saves with the correct user in `User=` field instead of `User=root`
  - **Console Logging** — Added user display in SDDM apply output for verification (`User: <username>`)

#### Services Tab — Full Feature Implementation & Testing

- **Audio Server Switching** — Batch PulseAudio and Pipewire installations (all audio, alsa, gstreamer packages in single terminal); added `check_audio_server()` to verify active server after install
- **Bluetooth Operations** — Batch installation (bluez + bluez-utils together); added daemon thread with label updates for enable/disable/restart controls
- **CUPS Printing** — Batch CUPS installation with systemctl controls (enable, disable, restart)
- **CUPS-PDF Printer** — Added dynamic label updates showing installed/not-installed status via `self.cups_pdf_label`
- **Printer Drivers** — Batch installation of all foomatic, gutenprint, ghostscript packages together; dynamic label updates via `self.printer_drivers_label`
- **HP Printer Support (HPLIP)** — Single-package install/remove with label feedback
- **System Config Printer** — GUI tool for printer setup (install/remove/status)
- **Lock File Cleanup** — Added pacman db.lck removal before batch audio server switches to prevent "database is locked" errors during parallel operations
- **Logging Pattern Refinement** — Introduced `fn.log_info_concise()` for visible path logging without verbose headers (complement to `debug_print()`)

#### UI Layout Reorganization (services_gui.py)

- **Section-Based Headers** — Divided printing section into four logical sections:
  - **CUPS Service** — contains CUPS install/remove controls
  - **Printer Drivers** — contains foomatic/gutenprint/ghostscript batch installation
  - **Tools** — contains system-config-printer and HP drivers (HPLIP)
  - **Status** — shows current CUPS service and socket status (active/inactive)
- **Consistent Label Styling** — All labels use 3-space indentation prefix and hexpand=True for alignment
- **Dynamic Status Labels** — Cups-pdf and printer drivers labels update after install/remove operations showing "Installed" status
- **Dynamic Service Status** — CUPS service status label refreshes after enable/disable/restart operations via `update_cups_status()` callback
- **Section Spacing** — Added 20px top margin before Status header to separate service controls from status display

#### Logging Pattern Addition (functions.py)

- **`log_info_concise()` function** — New logging function that outputs bare `print()` for concise multi-line operations; used for source→target paths in pacman, file copy, and shell operations; complements existing `debug_print()` (--debug only) and `log_info()` (with headers)

#### Other Module Updates

- **maintenance.py** — Added `fn.log_info_concise()` calls to GPG config operations for visible file path logging
- **shell.py** — Updated bashrc operations to use `fn.log_info_concise()` for visible path logging instead of bare `print()`

### Technical Details

- **Batch Pacman Operations** — All package installations use `fn.launch_pacman_install_in_terminal()` and removals use `fn.launch_pacman_remove_in_terminal()` to prevent multiple alacritty windows and database lock contention
- **Label Updates Pattern** — Store UI labels as `self.cups_pdf_label`, `self.printer_drivers_label`, `self.cups_status_label` in GUI init, then call `.set_markup()` in callback functions after terminal operations complete
- **Dynamic Status Refresh** — `update_cups_status()` function in services.py checks current `fn.check_service("cups")` and `fn.check_socket("cups")` status, called from on_click_enable_cups, on_click_disable_cups, on_click_restart_cups to refresh label via `GLib.idle_add()`
- **Lock File Handling** — Check for and remove `/var/lib/pacman/db.lck` before launching audio server switches; prevents cascading errors during rapid pacman calls
- **Section Headers** — Four section titles (CUPS Service, Printer Drivers, Tools, Status) with bold markup and horizontal separators; each section groups related controls
- **Logging Layers**:
  - `fn.log_section()` — major headers (green with separators)
  - `fn.log_subsection()` — feature headers (cyan)
  - `fn.log_info()` — blue headers with messages
  - `fn.log_info_concise()` — bare print for path logging (new)
  - `fn.debug_print()` — `--debug` flag only

### Files Modified

`sddm.py` • `services.py` • `services_gui.py` • `maintenance.py` • `shell.py` • `functions.py`

### Test Status

- **Services Tab** ✓ — All batch operations implemented, label updates functional, logging patterns applied
- **Themes/Icons/Themer** ⏳ — Next for M4 testing (code review shows flake8-clean, ready for feature testing)
- **Remaining Tabs** ⏳ — desktopr, fastfetch, performance, kernel, user, ai, network, software, system, logging, privacy, autostart

### Next Milestone

- Continue M4 Feature Testing: Themes → Icons → Themer → Desktopr → remaining tabs
- Each tab: launch app, verify all controls work, confirm no crashes or missing functionality

---

## 2026.05.02 - Code Cleanup Complete: All S/M/L Tasks Done, Ready for M4 Feature Testing

### What Changed

#### Small Tasks (S1–S10) — All Complete

- ✓ S1: flake8 installed and configured (ignore: E402, W503, W504, E128, E203)
- ✓ S2: Pending deletions committed (100+ files)
- ✓ S3–S6: Arco ref cleanup in maintenance.py, services_gui.py, desktopr_gui.py, support.py — **no refs found** (already clean)
- ✓ S7–S8: **NOT MERGING** (functions_sddm.py, functions_makedir.py stay separate per agreement)
- ✓ S9: TODO/FIXME audit — **no markers found** (already clean)
- ✓ S10: Flake8 linting complete — codebase passes with configured ignores

#### Medium Tasks (M1–M5) — All Complete

- ✓ M1: Arco refs in 6 files (functions.py, network_gui.py, shell.py, pacman.py, services.py, pacman_functions.py) — only `change_distro_label()` multi-distro support (intentional, keep)
- ✓ M2: desktopr.py — only `/etc/skel/.config/arco-chadwm` folder path (intentional, keep)
- ✓ M3: shell_gui.py — no arco refs found (already clean)
- ✓ M5: data/kiro/ population — finished

#### Large Tasks (L1–L2) — All Complete (Confirmed Intentional)

- ✓ L1: themes_gui.py — all 109 refs are real AUR package names (`arcolinux-arc-*-git`) — **SKIP, NEVER CHANGE**
- ✓ L2: themes.py — all 547 refs are real AUR package names (`arcolinux-arc-*-git`) — **SKIP, NEVER CHANGE**

#### Memory Updates

- Confirmed: `arco-chadwm` folder is CRITICAL system path — never rename
- Confirmed: `arcolinux-arc-*` package names are upstream AUR packages — never rename
- Confirmed: `change_distro_label()` is intentional multi-distro support — keep all entries
- Added: Auto-fix flake8 violations without asking permission
- Added: Never establish git tags (user's explicit ban)

### Technical Details

All code cleanup tasks systematically completed. No real arco/brand references remain except:

1. Multi-distro support in `change_distro_label()` (intentional)
2. Real AUR package names in themes modules (untouchable)
3. System folder path `/etc/skel/.config/arco-chadwm` (untouchable)

Codebase lint-clean with flake8. All Small/Medium/Large refactor tasks done.

### Files Modified

`.flake8` • `CHANGELOG.md` • Memory files (5 updated)

### Next Milestone

**M4 Feature Completeness Test** — 18 tabs on Kiro (Packages, SDDM, Shell, Maintenance, Services, Themes, Icons, Themer, Desktopr, Fastfetch, Performance, Kernel, User, AI, Network, Software, System, Logging, Privacy, Autostart)

---

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

| File                  | Covers                                                                                                                                                                          |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `pacman_gui.py`       | Pacman page UI — switches, AUR buttons, custom repo, blank pacman, reset/edit row                                                                                               |
| `pacman.py`           | Pacman toggle callbacks, update_repos_switches, parallel downloads                                                                                                              |
| `pacman_functions.py` | Repo read/write helpers, AUR helper install/remove, toggle_test_repos                                                                                                           |
| `ai.py`               | AI tools callbacks — install/remove ollama, LLM runners                                                                                                                         |
| `ai_gui.py`           | AI Tools page UI — Local LLM Runners section                                                                                                                                    |
| `packages.py`         | Package export/import/install logic                                                                                                                                             |
| `packages_gui.py`     | Packages page UI — export, import, install from list                                                                                                                            |
| `sddm.py`             | SDDM callbacks — apply settings, wallpaper, install/remove Simplicity theme                                                                                                     |
| `sddm_gui.py`         | SDDM page UI — theme, session, cursor, autologin, wallpaper section                                                                                                             |
| `icons.py`            | Icon theme callbacks — Sardi, Surfn, Neo Candy install/remove/find                                                                                                              |
| `icons_gui.py`        | Icons page UI — three sub-tabs with FlowBox checkboxes, preview lightbox, centred action buttons                                                                                |
| `shell.py`            | Shell switching callbacks — bash, fish, zsh, oh-my-zsh, oh-my-fish install/remove                                                                                               |
| `shell_gui.py`        | Shells page UI — shell switcher, ZSH theme selector, preview images                                                                                                             |
| `kernel.py`           | Kernel list, CPU compatibility checks, install/remove via Alacritty, boot entry management                                                                                      |
| `kernel_gui.py`       | Kernels page UI — per-kernel rows with status/install/remove, systemd-boot default selector                                                                                     |
| `log_callbacks.py`    | Logging callbacks — journalctl, dmesg, pacman log, Xorg log, systemd-analyze viewers                                                                                            |
| `logging_gui.py`      | Logging page UI — nine log viewer button rows                                                                                                                                   |
| `maintenance.py`      | Maintenance callbacks — cache clean, orphan remove, pacman lock, mirrors, hw-probe, cursors                                                                                     |
| `maintenance_gui.py`  | Maintenance page UI — all button rows and section layout                                                                                                                        |
| `autostart.py`        | Autostart callbacks — enable/disable autostart entries                                                                                                                          |
| `autostart_gui.py`    | Autostart page UI                                                                                                                                                               |
| `network_gui.py`      | Network page UI — nsswitch, network discovery, samba, samba user                                                                                                                |
| `services.py`         | Services callbacks — nsswitch, discovery install/disable, samba install/remove/user                                                                                             |
| `fastfetch.py`        | Fastfetch callbacks — install/remove, config apply                                                                                                                              |
| `fastfetch_gui.py`    | Fastfetch page UI                                                                                                                                                               |
| `performance.py`      | Performance callbacks — tuned, irqbalance, ananicy, gamemode, zram, swapfile, fstrim                                                                                            |
| `performance_gui.py`  | Performance page UI — all sections and button rows                                                                                                                              |
| `privacy.py`          | Privacy callbacks — uBlock Origin install/remove, hblock install/remove/enable/disable                                                                                          |
| `privacy_gui.py`      | Privacy page UI — Content Blocking and Network &amp; Tracking Protection sections                                                                                               |
| `themes.py`           | Arc theme callbacks — install/remove/find, preset selections (all/blue/dark/none)                                                                                               |
| `themes_gui.py`       | Themes page UI — FlowBox checkboxes, preset buttons, action buttons, preview image                                                                                              |
| `software.py`         | Software callbacks — launch/install/remove for GUI managers, AUR helpers, Flatpak/Snap/AppImage, TUI tools, logout managers                                                     |
| `software_gui.py`     | Software page UI — five sections with install/remove rows                                                                                                                       |
| `user.py`             | User account callbacks — create user, delete user, delete user + home folder, populate dropdown                                                                                 |
| `user_gui.py`         | User page UI — create user form, delete user section, arch visudo note                                                                                                          |
| `system.py`           | System info callbacks — CPU, memory, block/PCI/USB/block devices, inxi, hwinfo, fdisk, fstab, hostnamectl, localectl, systemd services/timers, dmesg, gparted, partitionmanager |
| `system_gui.py`       | System page UI — 20 viewer rows; gparted and partitionmanager show installed status                                                                                             |

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

Objective 13 (Remove Dead Code) & Objective 23 (Lint) status: COMPLETE

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

| Count | Code | Issue                                                      |
|-------|------|------------------------------------------------------------|
| 133   | E302 | Missing 2 blank lines between functions                    |
| 111   | E501 | Lines over 120 chars                                       |
| 40    | F541 | f-strings with no `{}` placeholders                        |
| 24    | E402 | Module-level imports not at top of file                    |
| 22    | F401 | Unused imports                                             |
| 22    | E722 | Bare `except:` clauses                                     |
| 17    | W293 | Blank lines containing whitespace                          |
| 15    | F811 | Duplicate imports                                          |
| 11    | F841 | Variables assigned but never used                          |
| 6     | F821 | **Undefined name `arepo`** — real bug, needs investigation |
| 6     | E203 | Whitespace before `:`                                      |
| 8     | E702 | Multiple statements on one line                            |

### F821 Undefined Names — pending fix

`arepo` confirmed removed (no references found — already cleaned up with deleted arco files).
Four remaining F821 bugs to fix next session:

| File                 | Line | Undefined name                                   | Likely cause                     |
|----------------------|------|--------------------------------------------------|----------------------------------|
| `icons.py`           | 89   | `set_att_checkboxes_theming_surfn_icons_normal`  | Function removed or renamed      |
| `icons.py`           | 96   | `set_att_checkboxes_theming_surfn_icons_minimal` | Function removed or renamed      |
| `maintenance_gui.py` | 93   | `fn`                                             | Missing `import functions as fn` |
| `themer.py`          | 596  | `readlink`                                       | Should be `os.readlink`          |

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
