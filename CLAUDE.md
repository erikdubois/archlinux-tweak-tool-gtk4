# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ArchLinux Tweak Tool (ATT) is a GTK4-based Python application for managing Arch-based Linux systems. It provides a graphical interface for system customization, package management, theming, services, and maintenance tasks without requiring command-line expertise.

- **Language**: Python 3.x
- **GUI Framework**: GTK4
- **Entry Point**: `usr/share/archlinux-tweak-tool/archlinux-tweak-tool.py`
- **Desktop Launcher**: `usr/share/applications/archlinux-tweak-tool.desktop`

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

Recent commits focused on:

- GTK4 API compliance (callback signatures, dialog patterns)
- Logging standardization (replaced print() throughout)
- Async UI responsiveness (thumbnails, file operations with idle_add)
- SDDM wallpaper function restoration

Check git log for implementation details on GTK4 patterns and workarounds.

## Project Plan — v1.0 Release by 2026-05-29

**Constraint:** 3–5 hours/day · 30 days · ~90–150 hours total  
**Goal:** Shippable, Kiro-only ATT package with all tabs functional and codebase clean

### Current State Snapshot (2026-04-29)

| Area | Status |
| ---- | ------ |
| Module structure | Done — all feature.py + feature_gui.py pairs exist |
| GTK4 API compliance | Done — callbacks, dialogs, async fixed |
| Logging standardization | Done — print() replaced throughout |
| Non-Kiro data deletion | Staged but not committed (~100 files) |
| Kiro code references | **Incomplete — 723 arco/arch/garuda refs remain in .py files** |
| Kiro data folder | **Sparse — only 3 scripts vs 40+ in arco** |
| Duplicate/dead code | **Exists — functions_backup.py, possible duplicate helpers** |
| PKGBUILD / packaging | Not started |

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

#### M5 — Package & Release (Days 27–30 · ~10h)

**Deliverable:** AUR-ready PKGBUILD, v1.0 git tag, release notes

- [ ] Write or update `PKGBUILD` with correct dependencies and install paths
- [ ] Test clean install from PKGBUILD in a fresh environment (VM or clean chroot)
- [ ] Write brief `CHANGELOG.md` or release notes
- [ ] Tag `v1.0.0` on main branch
- [ ] Push to AUR if applicable

**Final deliverable:** `archlinux-tweak-tool` installable from AUR or package file on Kiro.

---

### Risk Register

| Risk | Likelihood | Mitigation |
| ---- | ---------- | ---------- |
| Kiro data files need creation from scratch (not just renamed arco files) | High | Tackle in M1 gap audit; allocate extra M2 time if large |
| 723 code references take longer than 30h to migrate safely | Medium | Use plan mode + grep per-file; batch by module not by search term |
| Feature tab broken after data migration, hard to diagnose | Medium | Test after each module commit, not at end of M2 |
| Orphan removal cascade bug triggered during testing | Low | Never test `pacman -Rns $(pacman -Qdtq)` without reviewing output first |
| Packaging dependencies incomplete | Low | Document all imports at start of M5; cross-check with running system |

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

- [ ] S1 — Install `flake8`: `sudo pacman -S python-flake8`
- [ ] S2 — Commit all pending deletions (`git add -u`)
- [ ] S3 — Clear arco refs in `maintenance.py` (1 ref)
- [ ] S4 — Clear arco refs in `services_gui.py` (1 ref)
- [ ] S5 — Clear arco refs in `desktopr_gui.py` (1 ref)
- [ ] S6 — Clear arco refs in `support.py` (2 refs)
- [ ] S7 — Merge `functions_sddm.py` (1 function) into `functions.py`
- [ ] S8 — Merge `functions_makedir.py` (2 functions) into `functions.py`
- [ ] S9 — Review all TODO/FIXME markers — decide keep or delete (~40 across codebase)
- [ ] S10 — Run flake8 on one small module and fix all warnings

#### Medium — 1–4 hours each

- [ ] M1 — Clear arco refs in `functions.py` (7), `network_gui.py` (6), `shell.py` (5), `pacman.py` (5), `services.py` (4), `pacman_functions.py` (4) — do in one session
- [ ] M2 — Clear arco refs in `desktopr.py` (16 refs, 673 lines)
- [ ] M3 — Clear arco refs in `shell_gui.py` (20 refs, 670 lines)
- [ ] M4 — Merge `functions_backup.py` (3 fns) + `functions_startup.py` (4 fns) into `functions.py`; update all importers
- [ ] M5 — Audit `data/kiro/` gaps vs arco — produce the gap list (research only, no code changes)
- [ ] M6 — Populate `data/kiro/bin/` with missing Kiro-equivalent scripts
- [ ] M7 — Full flake8 pass on `functions.py` (2418 lines, 111 functions)
- [ ] M8 — Audit `functions.py` for duplicate helpers already in feature modules (read-only pass)

#### Large — 4+ hours each

- [ ] L1 — Clear arco refs in `themes_gui.py` (109 refs)
- [ ] L2 — Clear arco refs in `themes.py` (547 refs, 657 lines) — biggest single task; use plan mode
- [ ] L3 — Consolidate duplicate helpers found in M8 — touches every module that uses them
- [ ] L4 — Feature test pass: every tab on Kiro (packages, sddm, shell, maintenance, services, themes, icons, desktopr, fastfetch, performance, kernel, user, ai)
- [ ] L5 — Write PKGBUILD and test clean install in chroot
