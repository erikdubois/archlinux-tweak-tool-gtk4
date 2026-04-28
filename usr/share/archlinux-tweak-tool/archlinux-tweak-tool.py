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
support = None
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
        print(
            "---------------------------------------------------------------------------"
        )
        print("If you have errors, report it on the github")
        print("https://github.com/erikdubois/archlinux-tweak-tool-gyk4")
        print(
            "---------------------------------------------------------------------------"
        )
        print("Following distros are supported:")
        print(" - Arch Linux    - https://archlinux.org/")
        print(" - ArchBang      - https://archbang.org/")
        print(" - Archcraft     - https://archcraft.io/")
        print(" - Archman       - https://archman.org/")
        print(" - Artix         - https://artixlinux.org/")
        print(" - Axyl          - https://axyl-os.github.io/")
        print(" - BerserkerOS   - https://berserkarch.xyz/")
        print(" - BigLinux      - https://www.biglinux.com.br/")
        print(" - BlendOS       - https://blendos.co/")
        print(" - Bluestar      - https://sourceforge.net/projects/bluestarlinux/")
        print(" - CachyOS       - https://cachyos.org/")
        print(" - Calam-arch    - https://sourceforge.net/projects/blue-arch-installer/")
        print(" - Crystal Linux - https://getcryst.al/")
        print(" - EndeavourOS   - https://endeavouros.com/")
        print(" - Garuda        - https://garudalinux.org/")
        print(" - Liya          - https://sourceforge.net/projects/liya-2024/")
        print(" - LinuxHub Prime - https://linuxhub.link/")
        print(" - Mabox         - https://maboxlinux.org/")
        print(" - Manjaro       - https://manjaro.org/")
        print(" - Nyarch        - https://nyarchlinux.moe/")
        print(" - ParchLinux    - https://parchlinux.ir/")
        print(" - PrismLinux    - https://www.prismlinux.org/")
        print(" - RebornOS      - https://rebornos.org/")
        print(" - StormOS       - https://sourceforge.net/projects/hackman-linux/")
        print(
            "---------------------------------------------------------------------------"
        )
        print("Other Arch Linux based distros will be visited later")
        print("Adding repositories should be done with great care - they can conflict")
        print(
            "---------------------------------------------------------------------------"
        )
        print("We make backups of files related to the ATT.")
        print("You can recognize them by the extension .bak or .back")
        print("If we have a reset button, the backup file will be used")
        print("If you have errors, because of the login managers")
        print("You can try running one of these scripts:")
        print("Run fix-sddm-conf")
        print("You can receive ATT support on https://github.com/erikdubois/archlinux-tweak-tool-gtk4")
        print(
            "---------------------------------------------------------------------------"
        )
        print("[INFO] : pkgver = pkgversion")
        print("[INFO] : pkgrel = pkgrelease")
        print(
            "---------------------------------------------------------------------------"
        )
        print("[INFO] : Distro = " + fn.distr)
        print(
            "---------------------------------------------------------------------------"
        )

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
            print("[INFO] : Theme = " + base_theme + dark_str)
        else:
            print("[INFO] : Theme = not set")
        print(
            "---------------------------------------------------------------------------"
        )

        print("[INFO] : User = " + fn.sudo_username)
        fn.findgroup()
        print(
            "---------------------------------------------------------------------------"
        )
        if DEBUG:
            print("[DEBUG] Debug mode enabled")
        super().__init__(application=app, title="Arch Linux Tweak Tool")
        self.connect("close-request", self.on_close)
        self.set_default_size(1100, 920)

        self.opened = True
        self.firstrun = True
        # self.desktop = ""
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
        global zsh_theme, user, themer, support, settings, services, sddm
        global pacman_functions, fastfetch, maintenance, gui, icons, themes, att
        global desktopr, autostart, PackagesPromptGui, call, fastfetch_gui, pmf
        global functions_makedir, functions_backup, functions_startup, functions_sddm

        startup_start = time.time()
        fn.debug_print("Startup sequence initiated")

        # Lazy imports to reduce time-to-first-window.
        from subprocess import call as _call

        import zsh_theme as _zsh_theme
        import user as _user
        import themer as _themer
        import support as _support
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
        import functions_sddm as _functions_sddm
        from packages_prompt_gui import PackagesPromptGui as _PackagesPromptGui

        zsh_theme = _zsh_theme
        user = _user
        themer = _themer
        support = _support
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
        functions_sddm = _functions_sddm
        PackagesPromptGui = _PackagesPromptGui
        call = _call
        pmf = pacman_functions

        imports_time = time.time()
        fn.debug_print(f"Imports completed in {imports_time - startup_start:.3f}s")

        # Ensure application directories exist first
        functions_makedir.ensure_app_dirs()

        # Ensure root config directories exist
        functions_makedir.ensure_root_config_dirs()

        # Backup GTK config from user home to root
        functions_backup.backup_gtk_config()

        # Create .bak backups of system and user configuration files
        functions_backup.backup_system_configs()
        functions_backup.backup_user_configs()

        # Fix directory permissions (must be last)
        functions_startup.fix_permissions()

        init_time = time.time()
        fn.debug_print(f"Initialization (dirs, backups, permissions) completed in {init_time - imports_time:.3f}s")

        # Build and display GUI
        gui.gui(self, Gtk, Gdk, GdkPixbuf, base_dir, os, Pango, GLib)

        # Window is now responsive to user interaction
        gui_complete_time = time.time()
        fn.debug_print(f"[RESPONSIVE] Window becomes interactive after {gui_complete_time - init_time:.3f}s")

        try:
            self.present()
        except Exception:
            pass

        gui_time = time.time()
        fn.debug_print(f"GUI creation and display completed in {gui_time - init_time:.3f}s")

        # Set initializing flag to suppress logging during switch initialization
        # Individual pages will handle switch initialization via lazy loading
        self.initializing = True

        if not fn.path.isfile("/tmp/att.lock"):
            with open("/tmp/att.lock", "w", encoding="utf-8") as f:
                f.write("")

        if not fn.path.isfile("/tmp/att.lock"):
            with open("/tmp/att.lock", "w", encoding="utf8") as f:
                f.write("")

        # Cleanup splash screen
        if getattr(self, "_splash", None) is not None:
            try:
                self._splash.destroy()
            except Exception:
                pass
            self._splash = None

        total_time = time.time()
        print(f"[INFO] Total startup time: {total_time - startup_start:.3f}s")
        fn.debug_print(f"Total startup time: {total_time - startup_start:.3f}s")

        # Returning False removes the idle callback.
        return False

    # All feature callbacks have been extracted to separate modules
    # AI TOOLS → ai.py | AUTOSTART → autostart.py | DESKTOPR → desktopr.py
    # FASTFETCH → fastfetch.py | ICONS → icons.py | KERNEL → kernel.py
    # LOGGING → log_callbacks.py | MAINTENANCE → maintenance.py | PACKAGES → packages.py
    # PRIVACY → privacy.py | SDDM → sddm.py | SERVICES → services.py
    # SHELLS → shell.py | SYSTEM → system.py | THEMER → themer.py
    # THEMES → themes.py | USER → user.py | ZSH THEMES → zsh_theme.py
    # Startup initialization → functions_startup.py, functions_makedir.py, functions_backup.py, functions_sddm.py
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
    print("\nATT is Closing.")
    fn.unlink("/tmp/att.lock")
    if _app_ref is not None:
        _app_ref.quit()


class ATTApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.arcolinux.archlinux-tweak-tool")
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
                "The lock file has been found. This indicates there is already an instance of <b>ArchLinux Tweak Tool</b> running.\n"
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
                print("Make sure there is just one instance of ArchLinux Tweak Tool running")
                print("Then you can restart the application")

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
