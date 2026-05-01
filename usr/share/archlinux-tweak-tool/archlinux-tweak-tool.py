#!/usr/bin/env python3

# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0103,C0115,C0116,C0411,C0413,E1101,E0213,I1101,R0902,R0904,R0912,R0913,R0914,R0915,R0916,R1705,W0613,W0621,W0622,W0702,W0703
# pylint:disable=C0301,C0302 #line too long

import splash
import os
import subprocess
import signal
import datetime
import time
import functions as fn
import desktopr_gui
import utilities
import gi

# Heavy modules are imported lazily in `_finish_startup_init()` so the window can
# appear quickly. These names are populated at runtime.
zsh_theme = None
user = None
themer = None
settings = None
services = None
sddm = None
pacman_functions = None
fastfetch = None
maintenance = None
gui = None
icons = None
themes = None
desktopr = None
autostart = None
PackagesPromptGui = None
call = None
fastfetch_gui = None

gi.require_version("Gtk", "4.0")
from gi.repository import Gdk, GdkPixbuf, Gtk, Pango, GLib, Gio

# suppress harmless D-Bus session bus warning when running via pkexec


def _log_writer(_level, fields, _n_fields, _user_data):
    try:
        for field in fields:
            if field.key == "MESSAGE" and "Unable to acquire session bus" in (
                field.value if isinstance(field.value, str)
                else field.value.decode("utf-8", errors="replace")
            ):
                return GLib.LogWriterOutput.HANDLED
    except Exception:
        pass
    return GLib.LogWriterOutput.UNHANDLED


GLib.log_set_writer_func(_log_writer, None)
from os import readlink


base_dir = fn.path.dirname(fn.path.realpath(__file__))
pmf = None
DEBUG = False


class Main(Gtk.ApplicationWindow):
    def __init__(self, app):
        print("-" * 75)
        print("Arch Linux Tweak Tool - Error reporting: https://github.com/erikdubois/archlinux-tweak-tool-gtk4")
        print("-" * 75)
        print("Supported distributions: Arch, ArchBang, Archcraft, Archman, Artix, Axyl,")
        print("BerserkerOS, BigLinux, BlendOS, Bluestar, CachyOS, Calam-arch, Crystal Linux,")
        print("EndeavourOS, Garuda, Liya, LinuxHub Prime, Mabox, Manjaro, Nyarch, ParchLinux,")
        print("PrismLinux, RebornOS, StormOS (other Arch-based distros supported)")
        print("-" * 75)
        print("Backups: Files modified by ATT are backed up (.bak extension)")
        print("Support: https://github.com/erikdubois/archlinux-tweak-tool-gtk4")
        print("-" * 75)

        _gtk_theme = os.environ.get("GTK_THEME", "").strip("\"'") or None
        if not _gtk_theme:
            try:
                with open("/etc/environment", "r", encoding="utf-8") as _f:
                    for _line in _f:
                        _line = _line.strip()
                        if _line.startswith("GTK_THEME="):
                            _gtk_theme = _line.split("=", 1)[1].strip().strip("\"'")
                            break
            except Exception:
                pass
        if _gtk_theme:
            is_dark = _gtk_theme.lower().endswith("-dark")
            base_theme = _gtk_theme[:-5] if is_dark else _gtk_theme
            dark_str = " (dark mode)" if is_dark else ""
            print(f"[System] Distro={fn.distr} | Theme={base_theme}{dark_str} | User={fn.sudo_username}", flush=True)
            print("-" * 75)
        else:
            print(f"[System] Distro={fn.distr} | Theme=not set | User={fn.sudo_username}", flush=True)
            print("-" * 75)
        fn.findgroup()
        if DEBUG:
            fn.debug_print("[DEBUG] Debug mode enabled")
        super().__init__(application=app, title="Arch Linux Tweak Tool")
        self.connect("close-request", self.on_close)
        self.set_default_size(1100, 920)

        self.opened = True
        self.firstrun = True
        self.timeout_id = None

        self.desktop_status = Gtk.Label()
        self.image_DE = Gtk.Picture()

        self.label7 = Gtk.Label(xalign=0)
        self.label7.set_visible(False)
        self.progress = Gtk.ProgressBar()
        self.progress.set_pulse_step(0.2)
        self.progress.set_visible(False)
        self.login_wallpaper_path = ""
        self.fb = Gtk.FlowBox()
        self.flowbox_wall = Gtk.FlowBox()

        # Force splash screen to stay visible until init is done.
        # The main window will only be presented at the end of `_finish_startup_init()`.
        self._splash = splash.SplashScreen(transient_for=self)

        GLib.idle_add(self._finish_startup_init)
        return

    def _finish_startup_init(self):
        """Deferred startup initialization.

        Runs after the window has had a chance to present itself.
        """
        global zsh_theme, user, themer, settings, services, sddm
        global pacman_functions, fastfetch, maintenance, gui, icons, themes, att
        global desktopr, autostart, PackagesPromptGui, call, fastfetch_gui, pmf
        global functions_makedir, functions_backup, functions_startup

        startup_start = time.time()
        fn.debug_print("Startup sequence initiated")

        # Lazy imports to reduce time-to-first-window.
        from subprocess import call as _call

        import zsh_theme as _zsh_theme
        import user as _user
        import themer as _themer
        import settings as _settings
        import services as _services
        import sddm as _sddm
        import pacman_functions as _pacman_functions
        import fastfetch as _fastfetch
        import maintenance as _maintenance
        import gui as _gui
        import icons as _icons
        import themes as _themes
        import desktopr as _desktopr
        import autostart as _autostart
        import fastfetch_gui as _fastfetch_gui
        import functions_makedir as _functions_makedir
        import functions_backup as _functions_backup
        import functions_startup as _functions_startup
        from packages_prompt_gui import PackagesPromptGui as _PackagesPromptGui

        zsh_theme = _zsh_theme
        user = _user
        themer = _themer
        settings = _settings
        services = _services
        sddm = _sddm
        pacman_functions = _pacman_functions
        fastfetch = _fastfetch
        maintenance = _maintenance
        gui = _gui
        icons = _icons
        themes = _themes
        desktopr = _desktopr
        autostart = _autostart
        fastfetch_gui = _fastfetch_gui
        functions_makedir = _functions_makedir
        functions_backup = _functions_backup
        functions_startup = _functions_startup
        PackagesPromptGui = _PackagesPromptGui
        call = _call
        pmf = pacman_functions

        imports_time = time.time()
        fn.debug_print(f"Imports completed in {imports_time - startup_start:.3f}s")

        # Ensure directories exist before building GUI
        functions_makedir.ensure_app_dirs()
        functions_makedir.ensure_root_config_dirs()

        makedirs_time = time.time()
        fn.debug_print(f"Makedirs completed in {makedirs_time - imports_time:.3f}s")

        # Build and display GUI
        gui.gui(self, Gtk, Gdk, GdkPixbuf, base_dir, os, Pango, GLib)

        self.initializing = True

        if not fn.path.isfile("/tmp/att.lock"):
            with open("/tmp/att.lock", "w", encoding="utf-8") as f:
                f.write("")

        try:
            self.present()
        except Exception:
            pass

        # Destroy splash immediately after window is presented
        if getattr(self, "_splash", None) is not None:
            try:
                self._splash.destroy()
            except Exception:
                pass
            self._splash = None

        gui_time = time.time()
        fn.debug_print(f"[RESPONSIVE] Window visible after {gui_time - startup_start:.3f}s")

        # Defer backups and permissions to after window is visible
        GLib.idle_add(self._finish_background_init, startup_start, priority=GLib.PRIORITY_LOW)

        return False

    def _finish_background_init(self, startup_start):
        """Run backups and permission fixes after the window is already visible."""
        functions_backup.backup_gtk_config()
        functions_backup.backup_system_configs()
        functions_backup.backup_user_configs()
        functions_startup.fix_permissions()

        total_time = time.time()
        fn.debug_print(f"[INFO] Total startup time (incl. background init): {total_time - startup_start:.3f}s")
        self.initializing = False

        return False

    # All feature callbacks have been extracted to separate modules
    # AI TOOLS → ai.py | AUTOSTART → autostart.py | DESKTOPR → desktopr.py
    # FASTFETCH → fastfetch.py | ICONS → icons.py | KERNEL → kernel.py
    # LOGGING → log_callbacks.py | MAINTENANCE → maintenance.py | PACKAGES → packages.py
    # PRIVACY → privacy.py | SDDM → sddm.py | SERVICES → services.py
    # SHELLS → shell.py | SYSTEM → system.py | THEMER → themer.py
    # THEMES → themes.py | USER → user.py | ZSH THEMES → zsh_theme.py
    # Startup initialization → functions_startup.py, functions_makedir.py, functions_backup.py
    # Image utilities → functions.py

    # Bottom buttons

    def on_refresh_att_clicked(self, desktop):
        fn.restart_program()

    def on_close(self, window):
        try:
            fn.unlink("/tmp/att.lock")
        except FileNotFoundError:
            pass
        self.get_application().quit()
        return False


# Application entry point


_app_ref = None


def signal_handler(sig, frame):
    fn.debug_print("\nATT is Closing.")
    fn.unlink("/tmp/att.lock")
    if _app_ref is not None:
        _app_ref.quit()


class ATTApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.kiro.archlinux-tweak-tool")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        # These lines offer protection and grace when a kernel has obfuscated
        # or removed basic OS functionality.
        os_function_support = True
        try:
            fn.getlogin()
        except Exception:
            os_function_support = False

        if not fn.path.isfile("/tmp/att.lock") and os_function_support:
            with open("/tmp/att.pid", "w", encoding="utf-8") as f:
                f.write(str(fn.getpid()))

            # apply GTK_THEME from /etc/environment when not in environment (e.g. pkexec)
            gtk_theme = os.environ.get("GTK_THEME", "").strip("\"'") or None
            if not gtk_theme:
                try:
                    with open("/etc/environment", "r", encoding="utf-8") as _f:
                        for _line in _f:
                            _line = _line.strip()
                            if _line.startswith("GTK_THEME="):
                                gtk_theme = _line.split("=", 1)[1].strip().strip("\"'")
                                break
                except Exception:
                    pass
            if gtk_theme:
                prefer_dark = gtk_theme.lower().endswith("-dark")
                theme_name = gtk_theme[:-5] if prefer_dark else gtk_theme
                Gtk.Settings.get_default().set_property("gtk-theme-name", theme_name)
                Gtk.Settings.get_default().set_property(
                    "gtk-application-prefer-dark-theme", prefer_dark
                )

            style_provider = Gtk.CssProvider()
            style_provider.load_from_path(base_dir + "/icons.css")
            display = Gdk.Display.get_default()
            if display is not None:
                Gtk.StyleContext.add_provider_for_display(
                    display,
                    style_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
                )
            Main(app)
        else:
            self._show_lock_or_unsupported_dialog(app, os_function_support)

    def _show_lock_or_unsupported_dialog(self, app, os_function_support):
        if os_function_support:
            md = Gtk.MessageDialog(
                transient_for=None,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Lock File Found",
            )
            md.props.secondary_text = (
                "The lock file has been found. This indicates there is already an instance of"
                " <b>ArchLinux Tweak Tool</b> running.\n"
                "Click yes to remove the lock file\n"
                "and try running ATT again"
            )
            md.props.secondary_use_markup = True
        else:
            md = Gtk.MessageDialog(
                transient_for=None,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.CLOSE,
                text="Kernel Not Supported",
            )
            md.props.secondary_text = (
                "Your current kernel does not support basic os function calls. <b>ArchLinux Tweak Tool</b> "
                "requires these to work."
            )
            md.props.secondary_use_markup = True

        result_holder = [None]
        loop = GLib.MainLoop()

        def on_lock_response(d, response_id):
            result_holder[0] = response_id
            loop.quit()
            d.destroy()

        md.connect("response", on_lock_response)
        md.present()
        loop.run()

        if result_holder[0] in (Gtk.ResponseType.OK, Gtk.ResponseType.YES):
            pid = ""
            try:
                with open("/tmp/att.pid", "r", encoding="utf-8") as f:
                    pid = f.read().strip()

                if fn.check_if_process_is_running(int(pid)):
                    md2 = Gtk.MessageDialog(
                        transient_for=None,
                        message_type=Gtk.MessageType.INFO,
                        buttons=Gtk.ButtonsType.CLOSE,
                        text="You first need to close the existing application",
                    )
                    md2.props.secondary_text = "You first need to close the existing application"

                    md2.props.secondary_use_markup = True
                    loop2 = GLib.MainLoop()

                    def on_close_response(d, response_id):
                        loop2.quit()
                        d.destroy()

                    md2.connect("response", on_close_response)
                    md2.present()
                    loop2.run()
                else:
                    fn.unlink("/tmp/att.lock")
            except Exception:
                fn.debug_print("Make sure there is just one instance of ArchLinux Tweak Tool running")
                fn.debug_print("Then you can restart the application")

        app.quit()


if __name__ == "__main__":
    import sys

    if "--debug" in sys.argv:
        DEBUG = True
        sys.argv.remove("--debug")
        fn.set_debug(True)

    signal.signal(signal.SIGINT, signal_handler)
    app = ATTApplication()
    _app_ref = app
    sys.exit(app.run(sys.argv))
