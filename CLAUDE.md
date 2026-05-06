# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ArchLinux Tweak Tool (ATT) is a GTK4-based Python application for managing Arch-based Linux systems. It provides a graphical interface for system customization, package management, theming, services, and maintenance tasks without requiring command-line expertise.

- **Language**: Python 3.8+
- **GUI Framework**: GTK4 (4.6+)
- **Entry Point**: `usr/share/archlinux-tweak-tool/archlinux-tweak-tool.py`
- **Desktop Launcher**: `usr/share/applications/archlinux-tweak-tool.desktop`

## Requirements

**Runtime:**
- Python 3.8 or later
- GTK4 libraries (version 4.6+)
- GObject Introspection (gi)
- Standard library modules: os, sys, subprocess, threading, time, shutil, json

**System Tools:**
- bash (shell execution)
- sudo (elevated operations)
- pacman (package management)
- git (version control)
- flake8 (linting, development only)

**For Optional Features:**
- alacritty (terminal for package operations)
- fastfetch (system information display)
- zsh, fish, bash (shell support)
- systemctl (service management)

## Developer Objectives

These are the core principles guiding all development on this project:

1. **Fast Loading Application** - Minimize startup time through lazy-loading of heavy modules
2. **In-App Updating** - Dynamically update dropdown menus and other UI elements without full reloads
3. **Minimal Core** - Keep the main `archlinux-tweak-tool.py` file small and focused on entry point logic
4. **Modular Functions** - Separate general utilities in `functions.py` from task-specific functions
5. **Clear Structure** - Maintain strict feature-based organization (feature.py + feature_gui.py pattern)
6. **Dual Logging** - Provide both in-app notifications and console output for all operations
7. **Safe Package Operations** - Use popup terminal (Alacritty) for installations/removals with "press enter to close" workflow; never combine `alacritty --hold` with `read -p` — use one or the other; ATT preference is `read -p` at the end of the script without `--hold`; never use `subprocess.call()` to launch alacritty from a GUI callback — always use `Popen` in a daemon thread (via `_run_terminal` or equivalent) so ATT stays responsive while the terminal is open
8. **Reliability** - Never crash; handle all errors gracefully with user feedback
9. **Non-Invasive** - Respect user system state; avoid unwanted modifications
10. **User Communication** - Clearly communicate drastic changes through labels and confirmation dialogs before execution
11. **Multi-Distro Scope** - ATT targets all Arch-based systems (Kiro, Artix, Manjaro, etc.); remove Garuda and EndeavourOS *repo and package* references since ATT no longer ships those; keep `fn.distr` detection guards that conditionally show/hide UI to avoid conflicts on specific systems
12. **Data Folder Consolidation** - Transition to Kiro-only data folder; update all paths before removing other distro-specific directories
13. **Remove Dead Code** - Eliminate unused functions, imports, and legacy code left-overs; keep codebase clean and maintainable
14. **Transparency** - Always show the user what is happening to their system; in `--debug` mode show source, target, result for every file operation so nothing happens silently
15. **Teach GTK4 & Python Best Practices** - When implementing or reviewing code, explain the GTK4 and Python patterns being used so the developer builds deeper understanding; link to relevant docs when non-obvious
16. **Consistent Variable Naming** - Use the same naming conventions for variables across all modules: `snake_case` for variables/functions, `PascalCase` for classes; never mix styles within equivalent constructs
17. **No Duplicate Functions** - Before writing any helper or utility function, check `functions.py` and existing modules for an equivalent; reuse and consolidate rather than duplicating logic across pages
18. **Follow GTK4 Best Practices** - Apply current GTK4 idioms: use `Gtk.Builder` for complex layouts, prefer `GObject` signals over direct calls, avoid deprecated GTK3 APIs, and follow GNOME HIG for UX consistency
19. **Teach Effective Claude Usage** - When a task is unclear or too broad, ask the developer to scope it; suggest when a plan-mode session, a sub-agent, or a focused prompt would yield better results; flag when a request risks wasted tokens
20. **Model Selection Guidance** - Recommend switching to Opus when the task requires deep multi-file reasoning, architecture decisions, or security review; stay on Sonnet for routine edits, bug fixes, and single-file changes; use Haiku for fast lookups only
21. **Use Plan Mode for Non-Trivial Work** - Invoke plan mode before any change that touches more than two files, introduces a new pattern, or has irreversible side-effects; present the plan and get confirmation before executing
22. **Project-Driven Development** - Maintain a milestone/deliverable mindset: group related changes into logical milestones, identify what constitutes a shippable/packageable state between milestones, and flag when in-progress work is blocking a release
23. **Lint, Spacing & Comments** - All Python code must pass `flake8` (PEP 8): 4-space indentation, max line length 120, one blank line between methods, two blank lines between top-level definitions; remove inline comments that only restate the code; keep only comments that explain WHY (a constraint, a workaround, a non-obvious invariant)
24. **Maintain CHANGELOG.md Automatically** - After every session that changes code or project structure, update `CHANGELOG.md` without being asked; group entries by date (`YYYY.MM.DD`), use the existing structured layout (What Changed / Technical Details / Files Modified), one entry per day consolidating all changes made that day
25. **Never Change Code Without Explicit Confirmation** - Before any Edit, Write, or file deletion, state exactly what you intend to change and why, then wait for the user to approve. Never add constants, remove functions, or restructure files based on your own judgment alone — always ask first.
26. **UI Layout Consistency** - All pages must use the same layout patterns: section headers use `set_markup("<b>Section Name</b>")` (never `set_text()`); page titles use `set_name("title")` styled via CSS. When adding or editing any page, verify its section labels match this standard and fix any inconsistencies in the same change.
27. **Descriptive Variable Names — No Numbered Boxes** - Never use numbered widget names like `hbox1`, `hbox2`, `vbox3`. When touching any file that has them, rename all occurrences to descriptive names that reflect the content (e.g. `hbox_current_boot`, `hbox_pacman_log`). Rename the container, the label, and every `append()` reference in the same edit — never rename partially.
28. **Mandatory Console Output in Every Touched File** - Every file we touch must contain at least one `fn.log_*` call (`log_section`, `log_subsection`, `log_info`, `log_success`, `log_warn`, or `log_error`) so operations are always visible in the console. When touching a file that has none, add appropriate `log_*` calls to any callbacks or functions that perform user-visible actions before finishing the edit.
29. **ATT Script Standard** - Every bash script in ATT must follow the ATT Script Standard: start with `set -euo pipefail`; define `RESET`/`CYAN`/`GREEN`/`RED`/`YELLOW` via `tput`; define `separator`, `header`, `success`, `info`, `warn`, `error` helper functions; wrap every logical step in a `header` call; use `success`/`info`/`warn`/`error` for all output — never bare `echo`. Reference examples: [usr/bin/fix-sddm-conf](usr/bin/fix-sddm-conf) and [usr/share/archlinux-tweak-tool/data/bin/fix-pacman-databases-and-keys](usr/share/archlinux-tweak-tool/data/bin/fix-pacman-databases-and-keys). When touching any script that does not follow this standard, bring it into compliance in the same edit. **Exception: [usr/bin/archlinux-tweak-tool](usr/bin/archlinux-tweak-tool) is permanently exempt — never apply ATT Script Standard to this file under any circumstances.**

## Architecture

### Module Organization

The codebase follows a **feature-based module pattern** with a clear separation between logic and UI:

```text
usr/share/archlinux-tweak-tool/
├── archlinux-tweak-tool.py       # Main entry point, GTK application setup
├── functions.py                   # Central utility module (logging, subprocess, helpers)
├── gui.py                         # Main GUI container that imports all *_gui modules
├── <feature>.py                   # Business logic: icons.py, themes.py, desktopr.py, etc.
├── <feature>_gui.py              # Corresponding GUI: icons_gui.py, themes_gui.py, etc.
├── <feature>_callbacks.py         # Optional: isolated callback handlers (log_callbacks.py)
├── data/                          # Distro-specific configuration files and templates
│   ├── arch/                      # Arch Linux configs
│   ├── arco/                      # ArcoLinux configs
│   ├── kiro/                      # Kiro configs
│   └── ...                        # Other distro-specific directories
└── images/                        # Application assets
```

### Key Modules

| Module | Purpose |
| ------ | ------- |
| **functions.py** | Central utilities: logging (log_error, log_success, log_section), subprocess operations, file I/O, GTK helpers |
| **gui.py** | Main GUI container; imports and instantiates all *_gui modules |
| **icons.py / icons_gui.py** | Icon theme management |
| **themes.py / themes_gui.py** | GTK theme management |
| **desktopr.py / desktopr_gui.py** | Desktop/wallpaper configuration |
| **sddm.py / sddm_gui.py** | SDDM login manager configuration |
| **maintenance.py / maintenance_gui.py** | System cleanup, orphan packages, mirrors |
| **performance.py / performance_gui.py** | System optimization settings |
| **services.py / services_gui.py** | systemd service management |
| **packages.py / packages_gui.py** | Package import/export/installation |
| **shell.py / shell_gui.py** | Shell configuration and switching |
| **user.py / user_gui.py** | User account creation/management |
| **fastfetch.py / fastfetch_gui.py** | System information display configuration |
| **support.py** | Distro detection and support utilities |
| **settings.py** | Application settings |

### Startup Flow

1. `archlinux-tweak-tool.py` creates the main `Gtk.Application`
2. Early imports: functions, support, utilities, desktopr_gui (splash screen)
3. GUI window created with fast display
4. **Heavy modules lazy-loaded** in `_finish_startup_init()` to keep startup time low:
   - zsh_theme, user, themer, settings, services, sddm, pacman_functions, fastfetch, maintenance, icons, themes, desktopr, autostart, packages, and all GUI modules
5. Splash screen hidden after initialization complete

## Development Patterns

### Logging & Output

All user-facing output uses **functions.py logging functions** (never `print()`):

```python
import functions as fn

fn.debug_print(message)              # Debug-only output (with --debug flag)
fn.log_section("Major Header")       # Green section header with separators
fn.log_subsection("Minor Header")    # Cyan subsection header
fn.log_info("Informational")         # Blue info message
fn.log_success("Success message")    # Green success with separators
fn.log_warn("Warning message")       # Yellow warning with separators
fn.log_error("Error message", lineno=X, cmd="command")  # Red error with details
```

### GTK4 Callbacks

All GTK button/widget callbacks **must include a `_widget` parameter** as the second argument (after `self`):

```python
def on_button_click(self, _widget):  # Note: _widget parameter
    fn.log_success("Button clicked")
```

This is required even if the widget parameter is unused. Recent GTK4 API changes require this signature.

### Markup & Special Characters

In GTK `set_markup()` calls, **ampersands must be escaped as `&amp;`** or the label silently renders nothing:

```python
# Correct
label.set_markup("Set <b>&amp;</b> configure")

# Wrong - will render as empty
label.set_markup("Set <b>&</b> configure")
```

### Async Operations

For long-running operations that could freeze the UI, use `GLib.idle_add()` to defer execution:

```python
from gi.repository import GLib

GLib.idle_add(expensive_function, priority=GLib.PRIORITY_LOW)
```

Recent fixes: thumbnail loading, file operations that previously blocked the UI.

### Terminal Actions — wait_and_refresh Pattern

When a button launches an alacritty terminal (install/remove package) and a label or button must update afterward, **always use `wait_and_refresh` in a daemon thread**. Never use a fixed timeout (`GLib.timeout_add`) — the terminal takes longer than any hardcoded delay.

The subprocess function must `return` the `Popen` object so the thread can wait on it:

```python
# In pacman_functions.py — always return the process
def install_something(self):
    fn.log_subsection("Installing something...")
    fn.show_in_app_notification(self, "Opening terminal...")
    return fn.subprocess.Popen(
        ["alacritty", "--hold", "-e", "bash", "-c", "sudo pacman -S something"],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )

# In the GUI — wait for terminal close, then refresh
def wait_and_refresh(process):
    if process is None:
        fn.GLib.idle_add(refresh_labels)
        return
    fn.debug_print("Waiting for terminal to close...")
    process.wait()
    fn.debug_print("Terminal closed — refreshing labels")
    fn.GLib.idle_add(refresh_labels)

btn.connect(
    "clicked",
    lambda w: fn.threading.Thread(
        target=wait_and_refresh,
        args=(install_something(self),),
        daemon=True,
    ).start(),
)
```

### Dialog Patterns

- **File Dialogs**: Use `.connect()` + `.present()` pattern instead of `.run()`
  - Set `transient_for=self.window` for proper modality
  - Avoid deprecated GTK3 patterns like `GTK_RESPONSE_OK`, use `Gtk.ResponseType.OK`
- **Message Dialogs**: Connect to response signal; track explicit user selections rather than relying on return values

### Subprocess Management

Call system commands via `fn.subprocess_call()` or `fn.subprocess_run()` with proper error handling:

```python
result = fn.subprocess_run(["pacman", "-Sy"], check=True)
fn.subprocess_call("pacman -S package", shell=True)  # For shell syntax
```

Always log results and errors using the logging functions above.

### Package/System Operations

- **Pacman calls** must be wrapped with appropriate exception handling
- Use `fn.install_package(self, "package_name")` for interactive installation
- Network operations that could fail: retry logic and user feedback
- **Know the orphan cascade bug** (memory: Orphan Removal Bug): `pacman -Rns $(pacman -Qdtq)` can cascade-remove unrelated packages after uninstalling a dependency. Always verify operation scope first.

### File Operations

- Create backup files with `.bak` extension before modifying system config
- Use `shutil.copy()` for backups, not manual subprocess calls
- Always handle file not found gracefully
- Use absolute paths; avoid assumptions about working directory

## Common Tasks

### Running the Application

```bash
# Direct execution (requires sudo for system operations)
sudo python3 usr/share/archlinux-tweak-tool/archlinux-tweak-tool.py

# Via desktop launcher (handles pkexec automatically)
archlinux-tweak-tool

# With debug output
sudo python3 usr/share/archlinux-tweak-tool/archlinux-tweak-tool.py --debug
```

### Adding a New Feature

1. Create `<feature>.py` with business logic
2. Create `<feature>_gui.py` with GTK interface that imports from `<feature>.py`
3. Add callbacks in `<feature>_gui.py` or isolated `<feature>_callbacks.py` if complex
4. Import the `<feature>_gui` module in `gui.py` and call its GUI function
5. Follow the logging and callback patterns above
6. Test widget layout, async operations, and error handling

### Updating Distro Configs

Configuration files live in `usr/share/archlinux-tweak-tool/data/<distro>/`:

- Store package lists, shell configs, wallpapers, and distro-specific defaults
- Use `up.sh` script to pull/push updates and regenerate nemesis_packages.txt

### Debugging

Use the `--debug` flag to enable `fn.debug_print()` output:

```bash
sudo python3 usr/share/archlinux-tweak-tool/archlinux-tweak-tool.py --debug
```

Debug output includes D-Bus warnings, initialization steps, and custom debug messages.

## Known Issues & Workarounds

- **GTK FileChooser**: Use `.connect("response")` + `.present()` instead of `.run()` (blocking deprecated)
- **FlowBox clearing**: Use `get_first_child()` + `remove()` in a loop, not deprecated `get_model()`
- **Ampersand in markup**: Always escape as `&amp;` in `set_markup()` calls
- **Double initialization**: Set initializing flag **before** first `set_active()` calls to suppress spurious logging

## Recent Work

- **Wallpaper: XFCE detection + xfconf-query D-Bus fix (2026-05-05)** — `_get_user_env()` reads session env from `/proc/<pid>/environ`; `_set_xfce()` runs xfconf-query as real user via `sudo -u` + D-Bus prefix; `--create` flag replaces two-step set; still unconfirmed working (S11)
- **Shell tab: active shell indicator (2026-05-05)** — stack switcher tab for the active shell now shows "(active)"; derived from `fn.get_shell()` at GUI build time
- **Omarchy added (2026-05-05)** — startup banner updated; `DISTRO_TESTING.md` entry added (3.7.0-2); detection was already in `functions.py`
- **SDDM theme dropdown refresh (2026-05-04)** — `pop_theme_box` called inside `refresh()` after install/remove of edu-simplicity; dropdown now updates without restart
- **Kernel tab: chaotic-AUR dynamic refresh (2026-05-04)** — kernel rows rebuilt on tab map signal when chaotic status changes; no restart needed
- **Kernel tab: boot entry enrichment (2026-05-04)** — dropdown shows `title — kernel_pkg`; orphan entries filtered; `lbl_current` uses enriched string
- **M4 Feature Test complete (2026-05-03)** — all 20 tabs verified working on Kiro
- **fastfetch_gui.py cleanup (2026-05-03)** — all numbered widget names replaced with descriptive identifiers; dead `self.hbox26` and empty spacer `hbox22` removed
- **Lolcat install fix (2026-05-03)** — `on_fast_lolcat_toggled` now installs `lolcat` package via terminal if missing; previously only wrote shell config with no install
- Widget renaming pass (objective 27) — all numbered hbox/vbox names replaced with descriptive identifiers across 10+ GUI files
- Section header markup consistency (objective 26) — all pages now use `set_markup("<b>...</b>")` for section headers
- Fastfetch remove button implemented + `set_fastfetch_ui_sensitive()` for install-state control
- Kernel: boot entry title parsing fixed; non-systemd-boot fallback message added
- Desktopr: `refresh_installed_desktops()` added; called after install/remove
- Autostart: layout fix — add-entry controls moved inside mainbox
- Audio scripts migrated to `data/bin/` standalone scripts
- SDDM user context bug fixed (`fn.sudo_username` instead of `os.getenv`)

Check git log for full implementation details.

## Project Plan — v1.0 Release by 2026-05-29

**Constraint:** 3–5 hours/day · 30 days · ~90–150 hours total  
**Goal:** Shippable, Kiro-only ATT package with all tabs functional and codebase clean

### Current State Snapshot (2026-05-03)

| Area | Status |
| ---- | ------ |
| Module structure | ✓ Done — all feature.py + feature_gui.py pairs exist |
| GTK4 API compliance | ✓ Done — callbacks, dialogs, async fixed |
| Logging standardization | ✓ Done — print() replaced throughout |
| Non-Kiro data deletion | ✓ Done — committed all deletions |
| Code cleanup (S/M/L tasks) | ✓ Done — all Small, Medium, Large cleanup tasks complete |
| Kiro code references | ✓ Done — only intentional: multi-distro guards, real AUR packages, system paths |
| Kiro data folder | ✓ Done — populated per audit |
| Duplicate/dead code | ✓ Done — removed, consolidated, no duplicates |
| Flake8 linting | ✓ Done — codebase passes all checks |
| **M4 Feature Test** | **✓ Done — all 20 tabs verified working on Kiro (2026-05-03)** |

---

### Milestones

#### M1 — Clean Foundation (Days 1–5 · ~15h)

**Deliverable:** App launches without errors; only kiro data in tree; no uncommitted deletions

- [ ] Commit all staged deletions (any/, arch/, arco/ data folders)
- [ ] Verify app still runs after deletions; fix any broken imports
- [ ] Delete `functions_backup.py` (confirmed dead code)
- [ ] Audit what `data/kiro/` needs vs what `data/arco/` had; create a gap list
- [ ] Commit: "chore: clean slate — remove non-Kiro data, dead files"

**Packaging checkpoint:** Tagging `pre-m1` so there is always a known-good rollback point.

---

#### M2 — Kiro Code Migration (Days 6–14 · ~30h)

**Deliverable:** Zero arco/arch/garuda/endeavouros references in Python source

- [ ] Systematic grep-and-replace pass on all 723 references, file by file
- [ ] Update every data path to `data/kiro/` equivalents
- [ ] Remove distro-detection branches that only applied to arco/garuda
- [ ] Populate `data/kiro/` with Kiro-specific equivalents for each gap found in M1
- [ ] Run the app after each file to catch breakage early
- [ ] Commit per module: "feat(shell): migrate shell module to Kiro paths"

**Packaging checkpoint:** App runs on Kiro with no dead code paths referencing removed distros.

---

#### M3 — Code Quality (Days 15–20 · ~20h)

**Deliverable:** DRY, consistently named codebase with no duplicate helpers

- [ ] Audit `functions.py` against all feature modules — consolidate duplicated helpers
- [ ] Enforce `snake_case` variables/functions throughout; rename inconsistencies
- [ ] Remove any remaining unused imports and dead functions (per objective 13)
- [ ] Verify all callbacks follow `def on_x(self, _widget):` pattern (per objective GTK4)
- [ ] Confirm all `set_markup()` calls escape `&` as `&amp;`
- [ ] Commit: "refactor: consolidate helpers, enforce naming conventions"

**Packaging checkpoint:** `pylint` / `flake8` passes cleanly on all modules.

---

#### M4 — Feature Completeness (Days 21–26 · ~25h)

**Deliverable:** Every tab tested and working end-to-end on a Kiro system

Test each module in order of risk (most likely to be broken first):

- [ ] `packages` / `packages_gui` — package import/export with Kiro package lists
- [ ] `sddm` / `sddm_gui` — SDDM config with kiro sddm data
- [ ] `shell` / `shell_gui` — shell switching with kiro configs
- [ ] `maintenance` / `maintenance_gui` — mirrors, orphan removal (mind the cascade bug)
- [ ] `services` / `services_gui` — systemd service toggle
- [ ] `themes`, `icons`, `themer` — theming stack
- [ ] `desktopr`, `fastfetch`, `performance`, `kernel`, `user`, `ai` — remaining tabs
- [ ] Fix each broken feature before moving to the next
- [ ] Commit per fixed feature: "fix(sddm): update wallpaper paths for Kiro"

**Packaging checkpoint:** Manual test pass — all tabs open, primary actions work without crash.

---

### Risk Register

| Risk | Likelihood | Mitigation |
| ---- | ---------- | ---------- |
| Kiro data files need creation from scratch (not just renamed arco files) | High | Tackle in M1 gap audit; allocate extra M2 time if large |
| 723 code references take longer than 30h to migrate safely | Medium | Use plan mode + grep per-file; batch by module not by search term |
| Feature tab broken after data migration, hard to diagnose | Medium | Test after each module commit, not at end of M2 |
| Orphan removal cascade bug triggered during testing | Low | Never test `pacman -Rns $(pacman -Qdtq)` without reviewing output first |

---

### Session Conventions

- Start each session by stating which milestone and task you are on
- End each session with a one-line status: what was done and what is next
- Use **plan mode** before any task that touches more than 2 files or has irreversible effects
- Commit at the end of every session — never leave the repo in a broken state overnight
- If a task is taking 2× longer than estimated, flag it and re-scope rather than rushing

---

## Workflow

### Priority Tasks — Do These Before Any Real Work

These are one-time setup tasks. Until they are done, every session wastes time on avoidable problems.

- [ ] **Install flake8** — `sudo pacman -S python-flake8`; needed for all lint work (objective 23)
- [ ] **Commit pending deletions** — `git add -u && git commit -m "chore: remove non-Kiro data files"` — 100+ files deleted on disk but not in git; repo is in a broken-in-between state until this is done
- [ ] **Verify app still launches** — run `sudo python3 usr/share/archlinux-tweak-tool/archlinux-tweak-tool.py` and record any import or file-not-found errors; fix before proceeding
- [ ] **Audit data/kiro/ gaps** — compare `data/kiro/` against what `data/arco/` had; write the gap list as a comment or note; this list drives all of M2 data work
- [ ] **Establish a git tag baseline** — `git tag pre-m1` after the deletions commit so there is always a known-good rollback point

---

### Session Start Checklist

Every session, before writing a single line of code:

1. State the milestone and task: "Working on M2 — clearing arco refs in `shell_gui.py`"
2. `git status` — confirm clean working tree from last session
3. `git log --oneline -5` — remind yourself where you left off
4. If touching more than 2 files → enter plan mode first

### Session End Checklist

Before closing:

1. Run the app and confirm it still launches without errors
2. `git add` specific files (never `git add .` — avoid accidentally staging `.env` or large binaries)
3. Commit with a clear message: `feat(shell): migrate shell_gui to Kiro paths`
4. One-line note: what was done, what is next

---

### Task Size Guide

Use this to pick the right task for the time you have available.

| Time available | Pick |
| -------------- | ---- |
| 30 min | One Small task (S1–S10) |
| 1–2 hrs | One Medium task or two Small tasks |
| 3–4 hrs | One Large task with plan mode up front |
| 5 hrs | One Large task + one Medium task |

**Never start a Large task with less than 3 hours available** — half-finished migrations leave the repo in a broken state.

---

### Task List

#### Small — under 1 hour each

- [x] S1 — Install `flake8`: `sudo pacman -S python-flake8`
- [x] S2 — Commit all pending deletions (`git add -u`) — done, working tree clean
- [x] S3 — Clear arco refs in `maintenance.py` — 0 refs confirmed
- [x] S4 — Clear arco refs in `services_gui.py` — 0 refs confirmed
- [x] S5 — Clear arco refs in `desktopr_gui.py` — 0 refs confirmed
- [x] S6 — Clear arco refs in `support.py` — file deleted
- [x] S7 — Merge `functions_sddm.py` into `functions.py` — decided to keep separate (stay separate by design)
- [x] S8 — Merge `functions_makedir.py` into `functions.py` — decided to keep separate (stay separate by design)
- [x] S9 — Review all TODO/FIXME markers — none found, already cleared
- [x] S10 — Run flake8 on one small module and fix all warnings — done project-wide
- [ ] S11 — Fix XFCE wallpaper: xfconf-query runs as real user via sudo -u + D-Bus env but still not confirmed working; D-Bus session may not be reachable from pkexec context

#### Medium — 1–4 hours each

- [x] M1 — Clear arco refs in `functions.py`, `network_gui.py`, `shell.py`, `pacman.py`, `services.py`, `pacman_functions.py` — 0 refs confirmed in all
- [x] M2 — Clear arco refs in `desktopr.py` — only ref is `/etc/skel/.config/arco-chadwm` (real folder name on disk, protected, keep)
- [x] M3 — Clear arco refs in `shell_gui.py` — 0 refs confirmed
- [x] M4 — Merge `functions_backup.py` (3 fns) + `functions_startup.py` (4 fns) into `functions.py`; update all importers
- [x] M5 — Audit `data/kiro/` gaps — moot; data migrated to flat `data/` structure, no distro subfolders
- [x] M6 — Populate `data/kiro/bin/` — moot; flat `data/bin/` already in place
- [x] M7 — Full flake8 pass on `functions.py` — passes clean
- [x] M8 — Audit `functions.py` for duplicates — 2 found: `is_chaotic_aur_enabled()` (kernel.py + pacman_functions.py vs check_chaotic_aur_active in functions.py) and `pop_gtk_cursor_names()` (maintenance.py + sddm.py)

#### Large — 4+ hours each

- [x] L1 — Clear arco refs in `themes_gui.py` — all 109 refs are `arcolinux-arc-*` real AUR package names, protected, keep
- [x] L2 — Clear arco refs in `themes.py` — all 547 refs are `arcolinux-arc-*` real AUR package names, protected, keep
- [x] L3 — Consolidate duplicate helpers found in M8 — done: chaotic-AUR/nemesis checks unified, pop_gtk_cursor_names icon-scan extracted to fn.list_cursor_themes()
- [x] L4 — Feature test pass: every tab on Kiro — done 2026-05-03, all 20 tabs verified working
