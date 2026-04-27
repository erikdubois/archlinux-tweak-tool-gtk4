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
import functions as fn
import desktopr_gui
import utilities
import gi

# Heavy modules are imported lazily in `_finish_startup_init()` so the window can
# appear quickly. These names are populated at runtime.
zsh_theme = None
user = None
themer = None
design = None
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
        global zsh_theme, user, themer, design, support, settings, services, sddm
        global pacman_functions, fastfetch, maintenance, gui, icons, themes, att
        global desktopr, autostart, PackagesPromptGui, call, fastfetch_gui, pmf

        # Lazy imports to reduce time-to-first-window.
        from subprocess import call as _call

        import zsh_theme as _zsh_theme
        import user as _user
        import themer as _themer
        import design as _design
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
        from packages_prompt_gui import PackagesPromptGui as _PackagesPromptGui

        zsh_theme = _zsh_theme
        user = _user
        themer = _themer
        design = _design
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
        PackagesPromptGui = _PackagesPromptGui
        call = _call
        pmf = pacman_functions

        # =====================================================
        #     ATT THEME DARK OR LIGHT - FOLLOW USER SELECTION
        # ====================================================

        # ensuring we have a directory
        if not fn.path.isdir("/root/.config/"):
            try:
                fn.makedirs("/root/.config", 0o766)
            except Exception as error:
                print(error)

        if not fn.path.isdir("/root/.config/gtk-3.0"):
            try:
                fn.makedirs("/root/.config/gtk-3.0", 0o766)
            except Exception as error:
                print(error)

        if not fn.path.isdir("/root/.config/gtk-4.0"):
            try:
                fn.makedirs("/root/.config/gtk-4.0", 0o766)
            except Exception as error:
                print(error)

        if not fn.path.isdir("/root/.config/xsettingsd"):
            try:
                fn.makedirs("/root/.config/xsettingsd", 0o766)
            except Exception as error:
                print(error)

        if fn.path.isdir(fn.home + "/.config/gtk-3.0"):
            try:
                if not os.path.islink("/root/.config/gtk-3.0"):
                    fn.shutil.rmtree("/root/.config/gtk-3.0")
                    fn.shutil.copytree(
                        fn.home + "/.config/gtk-3.0", "/root/.config/gtk-3.0"
                    )
            except Exception as error:
                print(error)

        if fn.path.isdir(fn.home + "/.config/gtk-4.0/"):
            try:
                if not os.path.islink("/root/.config/gtk-4.0"):
                    fn.shutil.rmtree("/root/.config/gtk-4.0/")
                    fn.shutil.copytree(
                        fn.home + "/.config/gtk-4.0/", "/root/.config/gtk-4.0/"
                    )
            except Exception as error:
                print(error)

        if fn.path.isdir("/root/.config/xsettingsd/xsettingsd.conf"):
            try:
                if not os.path.islink("/root/.config/xsettingsd/"):
                    fn.shutil.rmtree("/root/.config/xsettingsd/")
                    if fn.path.isdir(fn.home + "/.config/xsettingsd/"):
                        fn.shutil.copytree(
                            fn.home + "/.config/xsettingsd/",
                            "/root/.config/xsettingsd/",
                        )
            except Exception as error:
                print(error)

        # =====================================================
        #     ENSURING WE HAVE THE DIRECTORIES WE NEED
        # =====================================================

        # make directory if it doesn't exist
        if not fn.path.isdir(fn.log_dir):
            try:
                fn.mkdir(fn.log_dir)
            except Exception as error:
                print(error)

        # make directory if it doesn't exist
        if not fn.path.isdir(fn.att_log_dir):
            try:
                fn.mkdir(fn.att_log_dir)
            except Exception as error:
                print(error)

        # ensuring we have a neofetch directory
        if not fn.path.exists(fn.home + "/.config/neofetch"):
            try:
                fn.makedirs(fn.home + "/.config/neofetch", 0o766)
                fn.permissions(fn.home + "/.config/neofetch")
            except Exception as error:
                print(error)

        # ensuring we have a fastfetch directory
        if not fn.path.exists(fn.home + "/.config/fastfetch"):
            try:
                fn.makedirs(fn.home + "/.config/fastfetch", 0o766)
                fn.permissions(fn.home + "/.config/fastfetch")
            except Exception as error:
                print(error)

        # ensuring we have .autostart
        if not fn.path.exists(fn.home + "/.config/autostart"):
            try:
                fn.makedirs(fn.home + "/.config/autostart", 0o766)
                fn.permissions(fn.home + "/.config/autostart")
            except Exception as error:
                print(error)

        # ensuring we have a directory for backups
        if not fn.path.isdir(fn.home + "/.config/archlinux-tweak-tool"):
            try:
                fn.makedirs(fn.home + "/.config/archlinux-tweak-tool", 0o766)
                fn.permissions(fn.home + "/.config/archlinux-tweak-tool")
            except Exception as error:
                print(error)

        # if there is a file called default remove it
        if fn.path.isfile("/usr/share/icons/default"):
            try:
                fn.unlink("/usr/share/icons/default")
            except Exception as error:
                print(error)

        # ensuring we have an index.theme
        if not fn.path.isdir("/usr/share/icons/default"):
            try:
                fn.makedirs("/usr/share/icons/default", 0o755)
            except Exception as error:
                print(error)

        if not fn.path.isfile("/usr/share/icons/default/index.theme"):
            if fn.path.isfile("/usr/share/icons/default/index.theme.bak"):
                try:
                    fn.shutil.copy(
                        "/usr/share/icons/default/index.theme.bak",
                        "/usr/share/icons/default/index.theme",
                    )
                except Exception as error:
                    print(error)
            else:
                try:
                    fn.shutil.copy(
                        "/usr/share/archlinux-tweak-tool/data/arco/cursor/index.theme",
                        "/usr/share/icons/default/index.theme",
                    )
                except Exception as error:
                    print(error)

        # =====================================================
        #                   MAKING BACKUPS
        # =====================================================

        if fn.path.isfile(fn.sddm_default_d1):
            if not fn.path.isfile(fn.sddm_default_d1_bak):
                try:
                    fn.shutil.copy(fn.sddm_default_d1, fn.sddm_default_d1_bak)
                except Exception as error:
                    print(error)

        if fn.path.isfile(fn.sddm_default_d2):
            if not fn.path.isfile(fn.sddm_default_d2_bak):
                try:
                    fn.shutil.copy(fn.sddm_default_d2, fn.sddm_default_d2_bak)
                except Exception as error:
                    pass

        # ensuring we have a backup of index.theme
        if fn.path.exists("/usr/share/icons/default/index.theme"):
            if not fn.path.isfile("/usr/share/icons/default/index.theme" + ".bak"):
                try:
                    fn.shutil.copy(
                        "/usr/share/icons/default/index.theme",
                        "/usr/share/icons/default/index.theme" + ".bak",
                    )
                except Exception as error:
                    print(error)

        # ensuring we have a backup of samba.conf
        if fn.path.exists("/etc/samba/smb.conf"):
            if not fn.path.isfile("/etc/samba/smb.conf" + ".bak"):
                try:
                    fn.shutil.copy(
                        "/etc/samba/smb.conf", "/etc/samba/smb.conf" + ".bak"
                    )
                except Exception as error:
                    print(error)

        # ensuring we have a backup of the nsswitch.conf
        if fn.path.exists("/etc/nsswitch.conf"):
            if not fn.path.isfile("/etc/nsswitch.conf" + ".bak"):
                try:
                    fn.shutil.copy("/etc/nsswitch.conf", "/etc/nsswitch.conf" + ".bak")
                except Exception as error:
                    print(error)

        # ensuring we have a backup of the config.fish
        if not fn.path.isfile(
            fn.home + "/.config/fish/config.fish" + ".bak"
        ) and fn.path.isfile(fn.home + "/.config/fish/config.fish"):
            try:
                fn.shutil.copy(
                    fn.home + "/.config/fish/config.fish",
                    fn.home + "/.config/fish/config.fish" + ".bak",
                )
                fn.permissions(fn.home + "/.config/fish/config.fish.bak")
            except Exception as error:
                print(error)

        # ensuring we have a backup of the archlinux mirrorlist
        if fn.path.isfile(fn.mirrorlist):
            if not fn.path.isfile(fn.mirrorlist + ".bak"):
                try:
                    fn.shutil.copy(fn.mirrorlist, fn.mirrorlist + ".bak")
                except Exception as error:
                    print(error)

        # ensuring we have a backup of current /etc/hosts
        if fn.path.isfile("/etc/hosts"):
            try:
                if not fn.path.isfile("/etc/hosts" + ".bak"):
                    fn.shutil.copy("/etc/hosts", "/etc/hosts" + ".bak")
            except Exception as error:
                print(error)

        # ensuring we have a backup of current neofetch
        if fn.path.isfile(fn.neofetch_config):
            try:
                if not fn.path.isfile(fn.neofetch_config + ".bak"):
                    fn.shutil.copy(fn.neofetch_config, fn.neofetch_config + ".bak")
                    fn.permissions(fn.neofetch_config + ".bak")
            except Exception as error:
                print(error)

        # ensuring we have a backup of current fastfetch
        if fn.path.isfile(fn.fastfetch_config):
            try:
                if not fn.path.isfile(fn.fastfetch_config + ".bak"):
                    fn.shutil.copy(fn.fastfetch_config, fn.fastfetch_config + ".bak")
                    fn.permissions(fn.fastfetch_config + ".bak")
            except Exception as error:
                print(error)

        # make backup of ~/.bashrc
        if fn.path.isfile(fn.bash_config):
            try:
                if not fn.path.isfile(fn.bash_config + ".bak"):
                    fn.shutil.copy(fn.bash_config, fn.bash_config + ".bak")
                    fn.permissions(fn.home + "/.bashrc.bak")
            except Exception as error:
                print(error)

        # make backup of ~/.zshrc
        if fn.path.isfile(fn.zsh_config):
            try:
                if not fn.path.isfile(fn.zsh_config + ".bak"):
                    fn.shutil.copy(fn.zsh_config, fn.zsh_config + ".bak")
                    fn.permissions(fn.home + "/.zshrc.bak")
            except Exception as error:
                print(error)

        # put usable .zshrc file there if nothing
        if not fn.path.isfile(fn.zsh_config):
            try:
                fn.shutil.copy(fn.zshrc_arco, fn.home)
                fn.permissions(fn.home + "/.zshrc")
            except Exception as error:
                print(error)

        # make backup of /etc/pacman.conf
        if fn.path.isfile(fn.pacman):
            if not fn.path.isfile(fn.pacman + ".bak"):
                try:
                    fn.shutil.copy(fn.pacman, fn.pacman + ".bak")
                except Exception as error:
                    print(error)

        # make backup of .config/xfce4/terminal/terminalrc
        if fn.file_check(fn.xfce4_terminal_config):
            try:
                if not fn.path.isfile(fn.xfce4_terminal_config + ".bak"):
                    fn.shutil.copy(
                        fn.xfce4_terminal_config, fn.xfce4_terminal_config + ".bak"
                    )
                    fn.permissions(fn.xfce4_terminal_config + ".bak")
            except Exception as error:
                print(error)

        # make backup of .config/alacritty/alacritty.yml
        if fn.file_check(fn.alacritty_config):
            try:
                if not fn.path.isfile(fn.alacritty_config + ".bak"):
                    fn.shutil.copy(fn.alacritty_config, fn.alacritty_config + ".bak")
                    fn.permissions(fn.alacritty_config + ".bak")
            except Exception as error:
                print(error)

        # =====================================================
        #               CATCHING ERRORS
        # =====================================================

        # make directory if it doesn't exist'
        if fn.path.exists("/usr/bin/sddm"):
            fn.create_sddm_k_dir()

            # if there is an sddm.conf but is empty = 0
            if fn.path.isfile(fn.sddm_default_d1):
                try:
                    if fn.path.getsize(fn.sddm_default_d1) == 0:
                        fn.shutil.copy(fn.sddm_default_d1_kiro, fn.sddm_default_d1)
                        fn.shutil.copy(fn.sddm_default_d2_kiro, fn.sddm_default_d2)
                except Exception as error:
                    print(error)

            # if there is NO sddm.conf at all - both are not there
            if not fn.path.exists(fn.sddm_default_d1) and not fn.path.exists(
                fn.sddm_default_d2
            ):
                try:
                    fn.shutil.copy(fn.sddm_default_d1_kiro, fn.sddm_default_d1)
                    fn.shutil.copy(fn.sddm_default_d2_kiro, fn.sddm_default_d2)

                    message = """
    The default SDDM files in your installation were either missing or corrupted.
    ATT has created and/or updated the necessary SDDM files.
    Backups have been created where possible.

    Affected files:
        - /etc/sddm.conf
        - /etc/sddm.conf.d/kde_settings.conf
        - /usr/lib/sddm/sddm.conf.d/default.conf

    You may need to adjust the settings again if necessary."""

                    print(message.strip())
                    fn.restart_program()
                except OSError as e:
                    # This will ONLY execute if the sddm files and the underlying sddm files do not exist
                    if e.errno == 2:
                        command = "/usr/local/bin/fix-sddm-config"
                        fn.subprocess.call(
                            command,
                            shell=True,
                            stdout=fn.subprocess.PIPE,
                            stderr=fn.subprocess.STDOUT,
                        )
                        print(
                            "The SDDM files in your installation either did not exist, or were corrupted."
                        )
                        print(
                            "These files have now been RESTORED. Please re-run the Tweak Tool if it did not load for you."
                        )
                        fn.restart_program()

            # adding lines to sddm
            if fn.path.isfile(fn.sddm_default_d2):
                session_exists = sddm.check_sddmk_session("Session=")
                if session_exists is False:
                    sddm.insert_session("#Session=")

            # adding lines to sddm
            if fn.path.isfile(fn.sddm_default_d2):
                user_exists = sddm.check_sddmk_user("User=")
                if user_exists is False:
                    sddm.insert_user("#User=")

        if fn.path.exists("/usr/bin/sddm"):
            # if any of the variables are missing we copy/paste
            if sddm.check_sddmk_complete():
                pass
            else:
                fn.create_sddm_k_dir()
                fn.shutil.copy(fn.sddm_default_d1_kiro, fn.sddm_default_d1)
                fn.shutil.copy(fn.sddm_default_d2_kiro, fn.sddm_default_d2)
                print(
                    "We changed your sddm configuration files so that ATT could start"
                )
                print(
                    "Backups are at /etc/bak.kde_settings.conf and /etc/bak.sddm.conf"
                )
                GLib.idle_add(
                    fn.show_in_app_notification,
                    self,
                    "We had to change your sddm configuration files",
                )

        # ensuring we have a neofetch config to start with
        if not fn.path.isfile(fn.neofetch_config):
            try:
                fn.shutil.copy(fn.neofetch_arco, fn.neofetch_config)
                fn.permissions(fn.neofetch_config)
            except Exception as error:
                print(error)

        # ensuring we have a fastfetch config to start with
        if not fn.path.isfile(fn.fastfetch_config):
            try:
                fn.shutil.copy(fn.fastfetch_arco, fn.fastfetch_config)
                fn.permissions(fn.fastfetch_config)
            except Exception as error:
                print(error)

        # ensuring permissions
        a1 = fn.stat(fn.home + "/.config/autostart")
        a2 = fn.stat(fn.home + "/.config/archlinux-tweak-tool")
        autostart_uid = a1.st_uid
        att_uid = a2.st_uid

        # fixing root permissions if the folder exists
        # can be removed later - 02/11/2021 startdate
        if fn.path.exists(fn.home + "/.config-att"):
            fn.permissions(fn.home + "/.config-att")

        if autostart_uid == 0:
            fn.permissions(fn.home + "/.config/autostart")
            print("Fixing autostart permissions...")

        if att_uid == 0:
            fn.permissions(fn.home + "/.config/archlinux-tweak-tool")
            print("Fixing archlinux-tweak-tool permissions...")

        if not fn.path.isfile(fn.config):
            key = {"theme": ""}
            settings.make_file("TERMITE", key)
            fn.permissions(fn.config)

        # =====================================================
        #      LAUNCHING GUI AND SETTING ALL THE OBJECTS
        # =====================================================

        gui.gui(self, Gtk, Gdk, GdkPixbuf, base_dir, os, Pango, GLib)
        # Now that the UI is built, show the main window.
        try:
            self.present()
        except Exception:
            pass

        # =====================================================
        #               READING AND SETTING
        # =====================================================

        # ========================ARCH REPO=============================

        arch_testing = pmf.check_repo("[core-testing]")
        arch_core = pmf.check_repo("[core]")
        arch_extra = pmf.check_repo("[extra]")
        arch_community = pmf.check_repo("[extra-testing]")
        arch_multilib_testing = pmf.check_repo("[multilib-testing]")
        arch_multilib = pmf.check_repo("[multilib]")

        # ========================OTHER REPO=============================

        chaotics_repo = pmf.check_repo("[chaotic-aur]")
        nemesis_repo = pmf.check_repo("[nemesis_repo]")

        # ========================ARCH LINUX REPO SET TOGGLE==================

        self.checkbutton2.set_active(arch_testing)
        self.checkbutton6.set_active(arch_core)
        self.checkbutton7.set_active(arch_extra)
        self.checkbutton5.set_active(arch_community)
        self.checkbutton3.set_active(arch_multilib_testing)
        self.checkbutton8.set_active(arch_multilib)

        # ========================OTHER REPO SET TOGGLE==================

        self.chaotics_switch.set_active(chaotics_repo)
        self.opened = False
        self.nemesis_switch.set_active(nemesis_repo)
        self.opened = False

        # ====================DESKTOP INSTALL REINSTALL===================

        if not fn.check_edu_repos_active():
            self.button_install.set_sensitive(False)
            self.button_reinstall.set_sensitive(False)


        # =====================================================
        #                        SDDM
        # =====================================================

        if fn.path.exists("/usr/bin/sddm"):
            try:
                # if not "plasma" in self.desktop.lower():
                if sddm.check_sddm(
                    sddm.get_sddm_lines(fn.sddm_default_d2), "CursorTheme="
                ) and sddm.check_sddm(sddm.get_sddm_lines(fn.sddm_default_d2), "User="):
                    if fn.path.isfile(fn.sddm_default_d2):
                        if "#" in sddm.check_sddm(
                            sddm.get_sddm_lines(fn.sddm_default_d2), "User="
                        ):
                            self.autologin_sddm.set_active(False)
                            self.sessions_sddm.set_sensitive(False)
                        else:
                            self.autologin_sddm.set_active(True)
                            self.sessions_sddm.set_sensitive(True)
            except:
                pass

        if not fn.path.isfile("/tmp/att.lock"):
            with open("/tmp/att.lock", "w", encoding="utf-8") as f:
                f.write("")

        if not fn.path.isfile("/tmp/att.lock"):
            with open("/tmp/att.lock", "w", encoding="utf8") as f:
                f.write("")

        # =====================================================
        #     IF ALL THIS IS DONE - DESTROY SPLASH SCREEN
        # =====================================================

        if getattr(self, "_splash", None) is not None:
            try:
                self._splash.destroy()
            except Exception:
                pass
            self._splash = None

        # Returning False removes the idle callback.
        return False

    # =====================================================
    # =====================================================
    # =====================================================
    # =====================================================
    #     END OF DEF __INIT__(SELF)
    # =====================================================
    # =====================================================
    # =====================================================
    # =====================================================

    # =====================================================
    #     CREATE AUTOSTART_GUI
    # =====================================================

    def create_autostart_columns(self, treeView):
        rendererText = Gtk.CellRendererText()
        renderer_checkbox = Gtk.CellRendererToggle()
        column_checkbox = Gtk.TreeViewColumn("", renderer_checkbox, active=0)
        renderer_checkbox.connect("toggled", self.renderer_checkbox, self.startups)
        renderer_checkbox.set_activatable(True)
        column_checkbox.set_sort_column_id(0)

        column = Gtk.TreeViewColumn("Name", rendererText, text=1)
        column.set_sort_column_id(1)

        column2 = Gtk.TreeViewColumn("Comment", rendererText, text=2)
        column2.set_sort_column_id(2)

        treeView.append_column(column_checkbox)
        treeView.append_column(column)
        treeView.append_column(column2)

    def create_columns(self, treeView):
        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", rendererText, text=0)
        column.set_sort_column_id(0)
        treeView.append_column(column)

    def renderer_checkbox(self, renderer, path, model):
        if path is not None:
            it = model.get_iter(path)
            model[it][0] = not model[it][0]

    def on_activated(self, treeview, path, column):
        failed = False
        treestore, selected_treepaths = treeview.get_selection().get_selected_rows()
        selected_treepath = selected_treepaths[0]
        selected_row = treestore[selected_treepath]
        bool = selected_row[0]
        text = selected_row[1]

        if bool:
            bools = False
        else:
            bools = True

        with open(
            fn.home + "/.config/autostart/" + text + ".desktop", "r", encoding="utf-8"
        ) as f:
            lines = f.readlines()
            f.close()
        try:
            pos = fn.get_position(lines, "Hidden=")
        except:
            failed = True
            with open(
                fn.home + "/.config/autostart/" + text + ".desktop",
                "a",
                encoding="utf-8",
            ) as f:
                f.write("Hidden=" + str(bools))
                f.close()
        if not failed:
            val = lines[pos].split("=")[1].strip()
            lines[pos] = lines[pos].replace(val, str(bools).lower())
            with open(
                fn.home + "/.config/autostart/" + text + ".desktop",
                "w",
                encoding="utf-8",
            ) as f:
                f.writelines(lines)
                f.close()

    # ====================================================================
    #                       AUTOSTART
    # ====================================================================

    def on_comment_changed(self, widget):
        if len(self.txtbox1.get_text()) >= 3 and len(self.txtbox2.get_text()) >= 3:
            self.abutton.set_sensitive(True)

    # autostart toggle on and off
    def on_auto_toggle(self, widget, data, lbl):
        failed = False
        try:
            with open(fn.autostart + lbl + ".desktop", "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            try:
                pos = fn.get_position(lines, "Hidden=")
            except:
                failed = True
                with open(fn.autostart + lbl + ".desktop", "a", encoding="utf-8") as f:
                    f.write("Hidden=" + str(not widget.get_active()).lower())
                    f.close()
        except:
            pass
        if not failed:
            try:
                val = lines[pos].split("=")[1].strip()
                lines[pos] = lines[pos].replace(
                    val, str(not widget.get_active()).lower()
                )
                with open(fn.autostart + lbl + ".desktop", "w", encoding="utf-8") as f:
                    f.writelines(lines)
                    f.close()
            except:
                # non .desktop files
                pass

    # remove file from ~/.config/autostart
    def on_auto_remove_clicked(self, gesture_or_widget, listbox, lbl):
        try:
            fn.unlink(fn.autostart + lbl + ".desktop")
            print("Removed item from ~/.config/autostart/")
            self.vvbox.remove(listbox)
        except Exception as error:
            print(error)
            print("We were unable to remove it")
            print("Evaluate if it can/should be removed")
            print("Then remove it manually")
            print("We only remove .desktop files")

    def clear_autostart(self):
        child = self.vvbox.get_first_child()
        while child is not None:
            next_child = child.get_next_sibling()
            self.vvbox.remove(child)
            child = next_child

    def load_autostart(self, files):
        self.clear_autostart()

        for x in files:
            self.add_row(x)

    def add_row(self, x):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        lbl = Gtk.Label(xalign=0)
        lbl.set_text(x)

        swtch = Gtk.Switch()
        swtch.connect("notify::active", self.on_auto_toggle, lbl.get_text())
        swtch.set_active(autostart.get_startups(lbl.get_text()))

        listbox = Gtk.ListBox()

        pbfb = GdkPixbuf.Pixbuf.new_from_file_at_size(
            fn.path.join(base_dir, "images/remove.png"), 28, 28
        )
        texture = Gdk.Texture.new_for_pixbuf(pbfb)
        fbimage = Gtk.Image.new_from_paintable(texture)
        fbimage.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        fbimage.set_tooltip_text("Remove")

        _listbox = listbox
        _text = lbl.get_text()
        fb_gesture = Gtk.GestureClick.new()
        fb_gesture.connect(
            "pressed",
            lambda g, n, x, y, lb=_listbox, t=_text: self.on_auto_remove_clicked(g, lb, t),
        )
        fbimage.add_controller(fb_gesture)

        lbl.set_hexpand(True)
        hbox.append(lbl)
        swtch.set_margin_top(10)
        swtch.set_margin_bottom(10)
        vbox2.append(swtch)
        hbox.append(vbox2)
        hbox.append(fbimage)

        vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        hbox.set_margin_top(5)
        hbox.set_margin_bottom(5)
        vbox1.append(hbox)

        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        listboxrow = Gtk.ListBoxRow()
        listboxrow.set_child(vbox1)
        listbox.append(listboxrow)

        self.vvbox.append(listbox)

    def on_remove_auto(self, widget):
        selection = self.treeView4.get_selection()
        model, paths = selection.get_selected_rows()

        # Get the TreeIter instance for each path
        for path in paths:
            iter = model.get_iter(path)
            # Remove the ListStore row referenced by iter
            value = model.get_value(iter, 1)
            model.remove(iter)
            fn.unlink(fn.home + "/.config/autostart/" + value + ".desktop")
            print("Item has been removed from autostart")
            fn.show_in_app_notification(self, "Item has been removed from autostart")

    def on_add_autostart(self, widget):
        if len(self.txtbox1.get_text()) > 1 and len(self.txtbox2.get_text()) > 1:
            autostart.add_autostart(
                self,
                self.txtbox1.get_text(),
                self.txtbox2.get_text(),
                self.txtbox3.get_text(),
            )
        print("Item has been added to autostart")
        fn.show_in_app_notification(self, "Item has been added to autostart")

    def on_exec_browse(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file",
            transient_for=self,
            action=Gtk.FileChooserAction.OPEN,
        )

        dialog.set_select_multiple(False)
        dialog.set_current_folder(Gio.File.new_for_path(fn.home))
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_Open", Gtk.ResponseType.OK)
        dialog.connect("response", self.open_response_auto)

        dialog.present()

    def open_response_auto(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            files = dialog.get_files()
            if files:
                foldername = files[0].get_path()
                print(foldername)
                self.txtbox2.set_text(foldername)
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    #                MAIN FUNCTIONS
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================


    # ====================================================================
    #                       ATT
    # ====================================================================

    # themes

    def on_install_att_themes_clicked(self, widget):
        print("We have installed all the selected themes")
        fn.show_in_app_notification(self, "We have installed all the selected themes")
        themes.install_themes(self)


    def on_remove_att_themes_clicked(self, widget):
        print("We have removed all the selected themes")
        fn.show_in_app_notification(self, "We have removed all the selected themes")
        themes.remove_themes(self)


    def on_find_att_themes_clicked(self, widget):
        print("[INFO] We show the installed themes")
        fn.show_in_app_notification(self, "We show the installed themes")
        themes.find_themes(self)


    # ====================================================================
    # Sardi

    def on_install_att_sardi_icon_themes_clicked(self, widget):
        print("[INFO] Installing selected Sardi icon themes")
        icons.install_sardi_icons(self)

    def on_remove_att_sardi_icon_themes_clicked(self, widget):
        print("[INFO] Removing selected Sardi icon themes")
        icons.remove_sardi_icons(self)

    def on_find_att_sardi_icon_themes_clicked(self, widget):
        print("[INFO] We show the installed sardi icon themes")
        fn.show_in_app_notification(self, "We show the installed sardi icon themes")
        icons.find_sardi_icons(self)

    # ====================================================================
    # surfn

    def on_install_att_surfn_icon_themes_clicked(self, widget):
        print("[INFO] Installing selected Surfn icon themes")
        icons.install_surfn_icons(self)

    def on_remove_att_surfn_icon_themes_clicked(self, widget):
        print("[INFO] Removing selected Surfn icon themes")
        icons.remove_surfn_icons(self)

    def on_find_att_surfn_icon_themes_clicked(self, widget):
        print("[INFO] We show all the installed Surfn icon themes")
        fn.show_in_app_notification(self, "We show all the installed Surfn icon themes")
        icons.find_surfn_icons(self)

    # ====================================================================
    # selection of theming

    def on_click_att_theming_all_selection(self, widget):
        print("[INFO] We have selected all themes")
        fn.show_in_app_notification(self, "We have selected all themes")
        themes.set_att_checkboxes_theming_all(self)

    def on_click_att_theming_blue_selection(self, widget):
        print("[INFO] We have selected the normal selection - blue themes")
        fn.show_in_app_notification(
            self, "We have selected the normal selection - blue themes"
        )
        themes.set_att_checkboxes_theming_blue(self)

    def on_click_att_theming_dark_selection(self, widget):
        print("[INFO] We have selected the minimal selection - dark themes")
        fn.show_in_app_notification(
            self, "We have selected the minimal selection - dark themes"
        )
        themes.set_att_checkboxes_theming_dark(self)

    def on_click_att_theming_none_selection(self, widget):
        print("[INFO] We have selected no themes")
        fn.show_in_app_notification(self, "We have selected no themes")
        themes.set_att_checkboxes_theming_none(self)

    # selection of icon theming
    def on_click_att_sardi_icon_theming_all_selection(self, widget):
        print("[INFO] We have selected all sardi icons")
        fn.show_in_app_notification(self, "We have selected all sardi icons")
        icons.set_att_checkboxes_theming_sardi_icons_all(self)

    def on_click_att_sardi_icon_theming_mint_selection(self, widget):
        print("[INFO] We have selected the mint selection - sardi icons")
        fn.show_in_app_notification(
            self, "We have selected the mint selection - sardi icons"
        )
        icons.set_att_checkboxes_theming_sardi_mint_icons(self)

    def on_click_att_sardi_icon_theming_mixing_selection(self, widget):
        print("[INFO] We have selected the mixing selection - sardi icons")
        fn.show_in_app_notification(
            self, "We have selected the mixing selection - sardi icons"
        )
        icons.set_att_checkboxes_theming_sardi_mixing_icons(self)

    def on_click_att_sardi_icon_theming_variations_selection(self, widget):
        print("[INFO] We have selected the variation selection - sardi icons")
        fn.show_in_app_notification(
            self, "We have selected the variation selection - sardi icons"
        )
        icons.set_att_checkboxes_theming_sardi_icons_variations(self)

    def on_click_att_sardi_icon_theming_none_selection(self, widget):
        print("[INFO] We have selected no sardi icons")
        fn.show_in_app_notification(self, "We have selected no sardiicons")
        icons.set_att_checkboxes_theming_sardi_icons_none(self)

    # different families of SARDI

    def on_click_att_fam_sardi_icon_theming_sardi_selection(self, widget):
        print("[INFO] We have selected the Sardi family")
        fn.show_in_app_notification(self, "We have selected the Sardi family themes")
        icons.set_att_fam_checkboxes_theming_sardi_icons(self)

    def on_click_att_fam_sardi_icon_theming_sardi_flexible_selection(self, widget):
        print("[INFO] We have selected the Sardi flexible family")
        fn.show_in_app_notification(
            self, "We have selected the Sardi flexible family themes"
        )
        icons.set_att_fam_checkboxes_theming_sardi_flexible(self)

    def on_click_att_fam_sardi_icon_theming_sardi_mono_selection(self, widget):
        print("[INFO] We have selected the Sardi mono family")
        fn.show_in_app_notification(
            self, "We have selected the Sardi mono family themes"
        )
        icons.set_att_fam_checkboxes_theming_sardi_mono(self)

    def on_click_att_fam_sardi_icon_theming_sardi_flat_selection(self, widget):
        print("[INFO] We have selected the Sardi flat family")
        fn.show_in_app_notification(
            self, "We have selected the Sardi flat family themes"
        )
        icons.set_att_fam_checkboxes_theming_sardi_flat(self)

    def on_click_att_fam_sardi_icon_theming_sardi_ghost_selection(self, widget):
        print("[INFO] We have selected the Sardi ghost family")
        fn.show_in_app_notification(
            self, "We have selected the Sardi ghost family themes"
        )
        icons.set_att_fam_checkboxes_theming_sardi_ghost(self)

    def on_click_att_fam_sardi_icon_theming_sardi_orb_selection(self, widget):
        print("[INFO] We have selected the Sardi orb family")
        fn.show_in_app_notification(
            self, "We have selected the Sardi orb family themes"
        )
        icons.set_att_fam_checkboxes_theming_sardi_orb(self)

    # selection of Surfn icons theming
    def on_click_att_surfn_theming_all_selection(self, widget):
        print("[INFO] We have selected all cursors")
        fn.show_in_app_notification(self, "We have selected all cursors")
        icons.set_att_checkboxes_theming_surfn_icons_all(self)

    def on_click_att_surfn_theming_normal_selection(self, widget):
        print("[INFO] We have selected the normal selection - cursors")
        fn.show_in_app_notification(
            self, "We have selected the normal selection - cursors"
        )
        icons.set_att_checkboxes_theming_surfn_icons_normal(self)

    def on_click_att_surfn_theming_minimal_selection(self, widget):
        print("[INFO] We have selected the minimal selection - cursors")
        fn.show_in_app_notification(
            self, "We have selected the minimal selection - cursors"
        )
        icons.set_att_checkboxes_theming_surfn_icons_minimal(self)

    def on_click_att_surfn_theming_none_selection(self, widget):
        print("[INFO] We have selected no cursors")
        fn.show_in_app_notification(self, "We have selected no cursors")
        icons.set_att_checkboxes_theming_surfn_icons_none(self)

    def on_install_extras_clicked(self, widget):
        print("[INFO] Installing selected Neo Candy icon packages")
        icons.install_att_extras(self)


    # extras
    def on_remove_extras_clicked(self, widget):
        print("[INFO] Removing selected Neo Candy icon packages")
        icons.remove_att_extras(self)


    def on_find_extras_clicked(self, widget):
        print("[INFO] We show the installed projects")
        fn.show_in_app_notification(self, "We show the installed projects")
        icons.find_att_extras(self)


    # selection of extras theming
    def on_click_extras_theming_all_selection(self, widget):
        print("[INFO] We have selected all projects")
        fn.show_in_app_notification(self, "We have selected all projects")
        icons.set_att_checkboxes_extras_all(self)

    def on_click_extras_theming_none_selection(self, widget):
        print("[INFO] We have selected none of the projects")
        fn.show_in_app_notification(self, "We have selected none of the projects")
        icons.set_att_checkboxes_extras_none(self)

    # ====================================================================
    #                       BASH
    # ====================================================================

    def tobash_apply(self, widget):
        fn.change_shell(self, "bash")

    def on_install_bash_completion_clicked(self, widget):
        fn.install_package(self, "bash")
        fn.install_package(self, "bash-completion")

    def on_remove_bash_completion_clicked(self, widget):
        fn.remove_package(self, "bash-completion")

    def on_arcolinux_bash_clicked(self, widget):
        try:
            if fn.path.isfile(fn.bashrc_arco):
                fn.shutil.copy(fn.bashrc_arco, fn.bash_config)
                fn.permissions(fn.home + "/.bashrc")
            fn.source_shell(self)
        except Exception as error:
            print(error)

        print("ATT ~/.bashrc is applied")
        GLib.idle_add(fn.show_in_app_notification, self, "ATT ~/.bashrc is applied")

    def on_bash_reset_clicked(self, widget):
        try:
            if fn.path.isfile(fn.bash_config + ".bak"):
                fn.shutil.copy(fn.bash_config + ".bak", fn.bash_config)
                fn.permissions(fn.home + "/.bashrc")
        except Exception as error:
            print(error)

        print("Your personal ~/.bashrc is applied again - logout")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Your personal ~/.bashrc is applied again - logout",
        )

    #    #====================================================================
    #    #                       DESIGN
    #    #====================================================================

    # design
    def on_install_themes_clicked(self, widget):
        design.install_themes(self)
        print("We have installed all the selected themes")
        fn.show_in_app_notification(self, "We have installed all the selected themes")
        # populate cursor themes - some themes include a cursor
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)


    def on_remove_themes_clicked(self, widget):
        design.remove_themes(self)
        print("We have removed all the selected themes")
        fn.show_in_app_notification(self, "We have removed all the selected themes")
        # populate cursor themes - some themes include a cursor
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)


    def on_find_themes_clicked(self, widget):
        design.find_themes(self)
        print("We show all the installed themes")
        fn.show_in_app_notification(self, "We show all the installed themes")
        # populate cursor themes - some themes include a cursor
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)


    # icons
    def on_install_icon_themes_clicked(self, widget):
        design.install_icon_themes(self)
        print("We have installed all the selected icon themes")
        fn.show_in_app_notification(
            self, "We have installed all the selected icon themes"
        )
        # populate cursor themes
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_remove_icon_themes_clicked(self, widget):
        design.remove_icon_themes(self)
        print("We have removed all the selected icon themes")
        fn.show_in_app_notification(
            self, "We have removed all the selected icon themes"
        )
        # populate cursor themes
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_find_icon_themes_clicked(self, widget):
        design.find_icon_themes(self)
        print("We show all the installed icon themes")
        fn.show_in_app_notification(self, "We show all the installed icon themes")
        # populate cursor themes
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    # cursors
    def on_install_cursor_themes_clicked(self, widget):
        design.install_cursor_themes(self)
        print("We have installed all the selected cursor themes")
        fn.show_in_app_notification(
            self, "We have installed all the selected cursor themes"
        )
        # populate cursor themes
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_remove_cursor_themes_clicked(self, widget):
        design.remove_cursor_themes(self)
        print("We have removed all the selected cursor themes")
        fn.show_in_app_notification(
            self, "We have removed all the selected cursor themes"
        )
        # populate cursor themes
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_find_cursor_themes_clicked(self, widget):
        design.find_cursor_themes(self)
        print("We show all the installed cursor themes")
        fn.show_in_app_notification(self, "We show all the installed cursor themes")
        # populate cursor themes
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    # fonts
    def on_install_fonts_clicked(self, widget):
        design.install_fonts(self)
        print("We have installed all the selected fonts")
        fn.show_in_app_notification(self, "We have installed all the selected fonts")

    def on_remove_fonts_clicked(self, widget):
        design.remove_fonts(self)
        print("We have removed all the selected fonts")
        fn.show_in_app_notification(self, "We have removed all the selected fonts")

    def on_find_fonts_clicked(self, widget):
        design.find_fonts(self)
        print("We show all the installed fonts")
        fn.show_in_app_notification(self, "We show all the installed fonts")

    ############################################################################

    # selection of theming
    def on_click_theming_all_selection(self, widget):
        print("We have selected all themes")
        fn.show_in_app_notification(self, "We have selected all themes")
        design.set_checkboxes_theming_all(self)

    def on_click_theming_normal_selection(self, widget):
        print("We have selected the normal selection - themes")
        fn.show_in_app_notification(
            self, "We have selected the normal selection - themes"
        )
        design.set_checkboxes_theming_normal(self)

    def on_click_theming_minimal_selection(self, widget):
        print("We have selected the minimal selection - themes")
        fn.show_in_app_notification(
            self, "We have selected the minimal selection - themes"
        )
        design.set_checkboxes_theming_minimal(self)

    def on_click_theming_none_selection(self, widget):
        print("We have selected no themes")
        fn.show_in_app_notification(self, "We have selected no themes")
        design.set_checkboxes_theming_none(self)

    # selection of icon theming
    def on_click_icon_theming_all_selection(self, widget):
        print("We have selected all icons")
        fn.show_in_app_notification(self, "We have selected all icons")
        design.set_checkboxes_theming_icons_all(self)

    def on_click_icon_theming_normal_selection(self, widget):
        print("We have selected the normal selection - icons")
        fn.show_in_app_notification(
            self, "We have selected the normal selection - icons"
        )
        design.set_checkboxes_theming_icons_normal(self)

    def on_click_icon_theming_minimal_selection(self, widget):
        print("We have selected the minimal selection - icons")
        fn.show_in_app_notification(
            self, "We have selected the minimal selection - icons"
        )
        design.set_checkboxes_theming_icons_minimal(self)

    def on_click_icon_theming_none_selection(self, widget):
        print("We have selected no icons")
        fn.show_in_app_notification(self, "We have selected no icons")
        design.set_checkboxes_theming_icons_none(self)

    # selection of cursor theming
    def on_click_cursor_theming_all_selection(self, widget):
        print("We have selected all cursors")
        fn.show_in_app_notification(self, "We have selected all cursors")
        design.set_checkboxes_theming_cursors_all(self)

    def on_click_cursor_theming_normal_selection(self, widget):
        print("We have selected the normal selection - cursors")
        fn.show_in_app_notification(
            self, "We have selected the normal selection - cursors"
        )
        design.set_checkboxes_theming_cursors_normal(self)

    def on_click_cursor_theming_minimal_selection(self, widget):
        print("We have selected the minimal selection - cursors")
        fn.show_in_app_notification(
            self, "We have selected the minimal selection - cursors"
        )
        design.set_checkboxes_theming_cursors_minimal(self)

    def on_click_cursor_theming_none_selection(self, widget):
        print("We have selected no cursors")
        fn.show_in_app_notification(self, "We have selected no cursors")
        design.set_checkboxes_theming_cursors_none(self)

    # selection of font theming
    def on_click_font_theming_all_selection(self, widget):
        print("We have selected all fonts")
        fn.show_in_app_notification(self, "We have selected all fonts")
        design.set_checkboxes_fonts_all(self)

    def on_click_font_theming_normal_selection(self, widget):
        print("We have selected the normal selection - fonts")
        fn.show_in_app_notification(
            self, "We have selected the normal selection - fonts"
        )
        design.set_checkboxes_fonts_normal(self)

    def on_click_font_theming_minimal_selection(self, widget):
        print("We have selected the minimal selection - fonts")
        fn.show_in_app_notification(
            self, "We have selected the minimal selection - fonts"
        )
        design.set_checkboxes_fonts_minimal(self)

    def on_click_font_theming_none_selection(self, widget):
        print("We have selected no fonts")
        fn.show_in_app_notification(self, "We have selected no fonts")
        design.set_checkboxes_fonts_none(self)

    #    #====================================================================
    #    #                       DESKTOPR
    #    #====================================================================

    def on_d_combo_changed(self, widget, pspec=None):
        from gi.repository import Gdk

        try:
            pixbuf3 = GdkPixbuf.Pixbuf.new_from_file_at_size(
                base_dir + "/desktop_data/" + fn.get_combo_text(self.d_combo) + ".jpg",
                desktopr_gui.IMAGE_PREVIEW_LOAD,
                desktopr_gui.IMAGE_PREVIEW_LOAD,
            )
            texture = Gdk.Texture.new_for_pixbuf(pixbuf3)
            self.image_DE.set_paintable(texture)
        except:
            self.image_DE.set_paintable(None)
        if desktopr.check_desktop(fn.get_combo_text(self.d_combo)):
            self.desktop_status.set_markup('<span size="x-large"><b>This desktop is installed</b></span>')
        else:
            self.desktop_status.set_markup('<span size="x-large"><b>This desktop is NOT installed</b></span>')

    def on_install_clicked(self, widget, state):
        fn.create_log(self)
        print("installing " + fn.get_combo_text(self.d_combo))
        desktopr.check_lock(self, fn.get_combo_text(self.d_combo), state)

    def on_default_clicked(self, widget):
        fn.create_log(self)
        if desktopr.check_desktop(fn.get_combo_text(self.d_combo)) is True:
            secs = settings.read_section()
            if "DESKTOP" in secs:
                settings.write_settings(
                    "DESKTOP", "default", fn.get_combo_text(self.d_combo)
                )
            else:
                settings.new_settings(
                    "DESKTOP", {"default": fn.get_combo_text(self.d_combo)}
                )
        else:
            fn.show_in_app_notification(self, "That desktop is not installed")
            print("Desktop is not installed")

    #    #====================================================================
    #    #                       FISH
    #    #====================================================================

    def on_install_only_fish_clicked_reboot(self, widget):
        fn.install_package(self, "fish")
        fn.restart_program()

    def on_install_only_fish_clicked(self, widget):
        fn.install_package(self, "fish")
        print("Only Fish has been installed")
        print("Fish is installed without a configuration")
        fn.show_in_app_notification(
            self, "Only the Fish package is installed without a configuration"
        )

    def on_remove_only_fish_clicked(self, widget):
        fn.remove_package(self, "fish")

    def on_arcolinux_fish_package_clicked(self, widget):
        fn.install_arco_package(self, "edu-shells-git")
        if fn.check_package_installed("edu-shells-git") is True:
            # backup whatever is there
            if fn.path_check(fn.home + "/.config/fish"):
                now = datetime.datetime.now()

                if not fn.path.exists(fn.home + "/.config/fish-att"):
                    fn.makedirs(fn.home + "/.config/fish-att")
                    fn.permissions(fn.home + "/.config/fish-att")

                if fn.path.exists(fn.home + "/.config-att"):
                    fn.permissions(fn.home + "/.config-att")

                fn.copy_func(
                    fn.home + "/.config/fish",
                    fn.home
                    + "/.config/fish-att/fish-att-"
                    + now.strftime("%Y-%m-%d-%H-%M-%S"),
                    isdir=True,
                )
                fn.permissions(
                    fn.home
                    + "/.config/fish-att/fish-att-"
                    + now.strftime("%Y-%m-%d-%H-%M-%S")
                )

            fn.copy_func("/etc/skel/.config/fish", fn.home + "/.config/", True)
            fn.permissions(fn.home + "/.config/fish")

            # if there is no file .config/fish
            if not fn.path.isfile(fn.home + "/.config/fish/config.fish"):
                fn.shutil.copy(
                    "/etc/skel/.config/fish/config.fish",
                    fn.home + "/.config/fish/config.fish",
                )
                fn.permissions(fn.home + "/.config/fish/config.fish")

            fn.source_shell(self)
            print(
                "ATT Fish config is installed and your old fish folder (if any) is in ~/.config/fish-att"
            )
            fn.show_in_app_notification(self, "ATT fish config is installed")

    def on_arcolinux_only_fish_clicked(self, widget):
        if not fn.path.isdir(fn.home + "/.config/fish/"):
            try:
                fn.mkdir(fn.home + "/.config/fish/")
                fn.permissions(fn.home + "/.config/fish/")
            except Exception as error:
                print(error)

        if fn.path.isfile(fn.fish_arco):
            fn.shutil.copy(fn.fish_arco, fn.home + "/.config/fish/config.fish")
            fn.permissions(fn.home + "/.config/fish/config.fish")

        if not fn.path.isfile(fn.home + "/.config/fish/config.fish.bak"):
            fn.shutil.copy(fn.fish_arco, fn.home + "/.config/fish/config.fish.bak")
            fn.permissions(fn.home + "/.config/fish/config.fish.bak")

        fn.source_shell(self)
        print("Fish config has been saved")
        fn.show_in_app_notification(self, "Fish config has been saved")

    def on_fish_reset_clicked(self, widget):
        if fn.path.isfile(fn.home + "/.config/fish/config.fish.bak"):
            fn.shutil.copy(
                fn.home + "/.config/fish/config.fish.bak",
                fn.home + "/.config/fish/config.fish",
            )
            fn.permissions(fn.home + "/.config/fish/config.fish")

        if not fn.path.isfile(fn.home + "/.config/fish/config.fish.bak"):
            fn.shutil.copy(fn.fish_arco, fn.home + "/.config/fish/config.fish")
            fn.permissions(fn.home + "/.config/fish/config.fish")

        print("Fish config reset")
        fn.show_in_app_notification(self, "Fish config reset")

    def on_remove_fish_all(self, widget):
        fn.remove_package_s(self,"edu-shells-git")
        fn.remove_package_s(self,"fish")
        print("Bash, Zsh and Fish is removed from /etc/skel - remove the folder in ~/.config/fish manually")
        fn.show_in_app_notification(
            self, "Bash, Zsh and Fish is removed from /etc/skel - remove the folder in ~/.config/fish manually"
        )

    def tofish_apply(self, widget):
        fn.change_shell(self, "fish")

    # ====================================================================
    #                       FIXES
    # ====================================================================

    def on_click_install_arch_keyring(self, widget):
        print("[INFO] Starting local archlinux-keyring installation")
        GLib.idle_add(fn.show_in_app_notification, self, "Starting archlinux-keyring installation...")
        try:
            pathway = base_dir + "/data/arch/packages/keyring/"
            print(f"[INFO] Package pathway: {pathway}")
            print("[INFO] Searching for archlinux-keyring package...")
            files = fn.listdir(pathway)
            if not files:
                raise Exception("No package files found in pathway")
            package_file = pathway + str(files).strip("[]'")
            print(f"[INFO] Found package: {package_file}")
            print(f"[INFO] Package size check...")
            if fn.os.path.exists(package_file):
                size = fn.os.path.getsize(package_file)
                print(f"[INFO] Package file size: {size} bytes")
            else:
                raise Exception(f"Package file not found: {package_file}")
            print("[INFO] Starting package installation...")
            GLib.idle_add(fn.show_in_app_notification, self, "Installing archlinux-keyring...")
            fn.install_local_package(self, package_file)
        except Exception as error:
            print(f"[ERROR] Local installation failed: {error}")
            GLib.idle_add(fn.show_in_app_notification, self, f"Installation failed: {error}")

    def on_click_install_arch_keyring_online(self, widget):
        print("[INFO] Starting online archlinux-keyring installation")
        pathway = "/tmp/att-installation/"
        print(f"[INFO] Creating temporary directory: {pathway}")
        fn.mkdir(pathway)
        command = (
            "wget https://archlinux.org/packages/core/any/archlinux-keyring/download --content-disposition -P"
            + pathway
        )
        try:
            print("[INFO] Downloading archlinux-keyring package...")
            GLib.idle_add(fn.show_in_app_notification, self, "Downloading archlinux-keyring package...")
            fn.subprocess.call(
                command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("[INFO] Download completed successfully")
            GLib.idle_add(fn.show_in_app_notification, self, "Download completed, installing package...")
            print("[INFO] Locating downloaded package file...")
            files = fn.listdir(pathway)
            if not files:
                raise Exception("No files found after download")
            package_file = pathway + str(files).strip("[]'")
            print(f"[INFO] Found package: {package_file}")
            if not fn.os.path.exists(package_file):
                raise Exception(f"Package file not found: {package_file}")
            print("[INFO] Starting package installation...")
            fn.install_local_package(self, package_file)
        except Exception as error:
            print(f"[ERROR] Installation failed: {error}")
            GLib.idle_add(fn.show_in_app_notification, self, f"Installation failed: {error}")
        finally:
            print("[INFO] Cleaning up temporary files...")
            try:
                fn.shutil.rmtree(pathway)
                print("[INFO] Cleanup completed")
            except Exception as error:
                print(f"[WARNING] Cleanup failed: {error}")

    def on_click_fix_pacman_keys(self, widget):
        fn.install_package(self, "alacritty")
        try:
            fn.subprocess.call(
                "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/any/fix-pacman-databases-and-keys; read -p \"Press Enter to close...\"'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Pacman has been reset (gpg, libraries,keys)")
            GLib.idle_add(fn.show_in_app_notification, self, "Pacman keys fixed")
        except Exception as error:
            print(error)

    def on_click_probe(self, widget):
        print("[INFO] Starting hardware probe")
        print("[INFO] Installing hw-probe package...")
        fn.install_package(self, "hw-probe")
        print("[INFO] Installing alacritty terminal...")
        fn.install_package(self, "alacritty")
        try:
            print("[INFO] Launching hardware probe...")
            GLib.idle_add(fn.show_in_app_notification, self, "Running hardware probe...")
            fn.subprocess.call(
                "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/arco/bin/arcolinux-probe; read -p \"Press Enter to close...\"'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("[INFO] Probe link has been created")
            GLib.idle_add(
                fn.show_in_app_notification, self, "Probe link has been created"
            )
        except Exception as error:
            print(f"[ERROR] Hardware probe failed: {error}")
            GLib.idle_add(
                fn.show_in_app_notification, self, f"Probe failed: {error}"
            )

    def on_click_fix_mainstream(self, widget):
        fn.install_package(self, "alacritty")
        try:
            command = "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/any/set-mainstream-servers; read -p \"Press Enter to close...\"'"
            fn.subprocess.call(
                command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Mainstream servers have been set")
            GLib.idle_add(
                fn.show_in_app_notification, self, "Mainstream servers have been saved"
            )
        except Exception as error:
            print(error)

    def on_click_reset_mirrorlist(self, widget):
        try:
            if fn.path.isfile(fn.mirrorlist + ".bak"):
                fn.shutil.copy(fn.mirrorlist + ".bak", fn.mirrorlist)
        except Exception as error:
            print(error)
        print("Your original mirrorlist is back")
        GLib.idle_add(
            fn.show_in_app_notification, self, "Your original mirrorlist is back"
        )
        fn.install_package(self, "alacritty")
        try:
            fn.subprocess.call(
                f"alacritty -e bash -c 'cat {fn.mirrorlist}; echo \"\"; read -p \"Press Enter to close...\"'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_get_arch_mirrors(self, widget):
        fn.install_package(self, "alacritty")
        try:
            fn.install_package(self, "reflector")
            fn.subprocess.call(
                "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/any/archlinux-get-mirrors-reflector; read -p \"Press Enter to close...\"'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Fastest Arch Linux servers have been set using reflector")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Fastest Arch Linux servers saved - reflector",
            )
        except:
            print("Install alacritty")

    def on_click_get_arch_mirrors2(self, widget):
        fn.install_package(self, "alacritty")
        try:
            fn.subprocess.call(
                "alacritty -e bash -c '/usr/share/archlinux-tweak-tool/data/any/archlinux-get-mirrors-rate-mirrors; read -p \"Press Enter to close...\"'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Fastest Arch Linux servers have been set using rate-mirrors")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Fastest Arch Linux servers saved - rate-mirrors",
            )
        except Exception as error:
            print(error)

    def on_click_fix_sddm_conf(self, widget):
        fn.install_package(self, "alacritty")
        try:
            command = "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/arco/bin/arcolinux-fix-sddm-config"
            fn.subprocess.call(
                command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("We use the default setup from plasma")
            print("Two files:")
            print(" - /etc/sddm.conf")
            print(" - /etc/sddm.d.conf/kde_settings.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Saved the original SDDM configuration",
            )
        except:
            print("Install alacritty")

    def on_click_fix_pacman_conf(self, widget):
        try:
            command = "alacritty --hold -e /usr/local/bin/arcolinux-fix-pacman-conf"
            fn.subprocess.call(
                command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Saved the original /etc/pacman.conf")
            GLib.idle_add(
                fn.show_in_app_notification, self, "Saved the original /etc/pacman.conf"
            )
        except Exception as error:
            print(error)

    def on_click_fix_pacman_gpg_conf(self, widget):
        print("[INFO] Starting gpg.conf backup and reset")
        if not fn.path.isfile(fn.gpg_conf + ".bak"):
            print(f"[INFO] Creating backup of current gpg.conf to {fn.gpg_conf}.bak")
            fn.shutil.copy(fn.gpg_conf, fn.gpg_conf + ".bak")
        print(f"[INFO] Restoring original gpg.conf from {fn.gpg_conf_original}")
        print("[INFO] Content of original gpg.conf:")
        print("=" * 70)
        try:
            with open(fn.gpg_conf_original, 'r') as f:
                content = f.read()
                print(content)
        except Exception as e:
            print(f"[ERROR] Could not read gpg.conf: {e}")
        print("=" * 70)
        fn.shutil.copy(fn.gpg_conf_original, fn.gpg_conf)
        print("[INFO] The new /etc/pacman.d/gnupg/gpg.conf has been saved")
        print("[INFO] Backup is in /etc/pacman.d/gnupg/gpg.conf.bak")
        print("[INFO] We only add servers to the config")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "The new /etc/pacman.d/gnupg/gpg.conf has been saved",
        )

    def on_click_fix_pacman_gpg_conf_local(self, widget):
        print("[INFO] Starting local gpg.conf backup and reset")
        if not fn.path.isdir(fn.home + "/.gnupg"):
            try:
                print(f"[INFO] Creating directory: {fn.home}/.gnupg")
                fn.makedirs(fn.home + "/.gnupg", 0o766)
                fn.permissions(fn.home + "/.gnupg")
                print("[INFO] Directory created and permissions set")
            except Exception as error:
                print(f"[ERROR] Failed to create directory: {error}")

        if not fn.path.isfile(fn.gpg_conf_local + ".bak"):
            try:
                print(f"[INFO] Creating backup of current gpg.conf to {fn.gpg_conf_local}.bak")
                fn.shutil.copy(fn.gpg_conf_local, fn.gpg_conf_local + ".bak")
                fn.permissions(fn.gpg_conf_local + ".bak")
                print("[INFO] Backup created successfully")
            except Exception as error:
                print(f"[ERROR] Failed to create backup: {error}")

        print(f"[INFO] Restoring original gpg.conf from {fn.gpg_conf_local_original}")
        print("[INFO] Content of original local gpg.conf:")
        print("=" * 70)
        try:
            with open(fn.gpg_conf_local_original, 'r') as f:
                content = f.read()
                print(content)
        except Exception as e:
            print(f"[ERROR] Could not read local gpg.conf: {e}")
        print("=" * 70)
        fn.shutil.copy(fn.gpg_conf_local_original, fn.gpg_conf_local)
        fn.permissions(fn.gpg_conf_local)
        print("[INFO] The new ~/.gnupg/gpg.conf has been saved")
        print("[INFO] Backup is in ~/.gnupg/gpg.conf.bak")
        print("[INFO] We only add servers to the config")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "The new ~/.gnupg/gpg.conf has been saved",
        )

    def on_click_install_arch_mirrors(self, widget):
        fn.install_package(self, "reflector")
        self.btn_run_reflector.set_sensitive(True)

    def on_click_install_arch_mirrors2(self, widget):
        fn.install_package(self, "rate-mirrors")
        self.btn_run_rate_mirrors.set_sensitive(True)

    def on_click_apply_global_cursor(self, widget):
        print("[INFO] Starting global cursor application")
        try:
            cursor = fn.get_combo_text(self.cursor_themes)
            print(f"[INFO] Selected cursor theme: {cursor}")
            print("[INFO] Applying global cursor theme...")
            maintenance.set_global_cursor(self, cursor)
            print(f"[INFO] Cursor '{cursor}' is saved in /usr/share/icons/default")
            print("[INFO] Global cursor theme applied successfully")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Cursor is saved globally",
            )
        except Exception as error:
            print(f"[ERROR] Failed to apply global cursor: {error}")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                f"Failed to apply cursor: {error}",
            )

    def on_click_update_system(self, widget):
        try:
            print("[INFO] Starting system update")
            print("[INFO] Installing alacritty terminal...")
            fn.install_package(self, "alacritty")
            print("[INFO] Launching system update...")
            GLib.idle_add(fn.show_in_app_notification, self, "Starting system update...")
            fn.subprocess.call(
                "alacritty -e bash -c 'sudo pacman -Syu; echo \"\"; echo \"=== Update complete ===\"; read -p \"Press Enter to close...\"'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("[INFO] System update completed")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "System update completed",
            )
        except Exception as error:
            print(f"[ERROR] Update system failed: {error}")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                f"Update failed: {error}",
            )

    def on_click_clean_cache(self, widget):
        try:
            print("[INFO] Starting pacman cache cleanup")
            print("[INFO] Installing alacritty terminal...")
            fn.install_package(self, "alacritty")
            print("[INFO] Launching pacman cache cleanup...")
            GLib.idle_add(fn.show_in_app_notification, self, "Starting cache cleanup...")
            fn.subprocess.call(
                "alacritty -e bash -c 'sudo pacman -Sc; echo \"\"; echo \"=== Clean complete ===\"; read -p \"Press Enter to close...\"'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("[INFO] Pacman cache cleanup completed")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Pacman cache cleaned",
            )
        except Exception as error:
            print(f"[ERROR] Clean cache failed: {error}")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                f"Cleanup failed: {error}",
            )

    def on_click_remove_pacman_lock(self, widget):
        try:
            print("[INFO] Starting pacman lock removal")
            print("[INFO] Installing alacritty terminal...")
            fn.install_package(self, "alacritty")
            print("[INFO] Checking pacman lock file: /var/lib/pacman/db.lck")
            print("[INFO] Launching pacman lock removal...")
            GLib.idle_add(fn.show_in_app_notification, self, "Removing pacman lock...")
            fn.subprocess.call(
                "alacritty -e bash -c 'sudo rm -f /var/lib/pacman/db.lck; echo \"\"; echo \"=== Lock removed ===\"; read -p \"Press Enter to close...\"'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("[INFO] Pacman lock removal completed")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Pacman lock removed",
            )
        except Exception as error:
            print(f"[ERROR] Remove pacman lock failed: {error}")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                f"Lock removal failed: {error}",
            )

    # ====================================================================
    #                   INVESTIGATE YOUR LOGS
    # ====================================================================

    def on_click_log_current_boot(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                "alacritty -e bash -c 'SYSTEMD_COLORS=1 journalctl -b 0 | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_log_prev_boot(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                "alacritty -e bash -c 'SYSTEMD_COLORS=1 journalctl -b -1 | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_log_errors(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                "alacritty -e bash -c 'SYSTEMD_COLORS=1 journalctl -b -p err | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_log_recent(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                'alacritty -e bash -c \'SYSTEMD_COLORS=1 journalctl --since "20 minutes ago" | fzf --ansi\'',
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_log_xorg(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.install_package(self, "bat")
            fn.subprocess.call(
                "alacritty -e bash -c 'bat --color=always /var/log/Xorg.0.log | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_log_pacman(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.install_package(self, "bat")
            fn.subprocess.call(
                "alacritty -e bash -c 'bat --color=always /var/log/pacman.log | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_log_xsession(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.install_package(self, "bat")
            cmd = (
                "alacritty -e bash -c '"
                "found=; "
                "for f in ~/.xsession-errors ~/.local/share/xorg/Xorg.0.log /var/log/Xorg.0.log; do "
                "  [ -s \"$f\" ] && { found=$f; break; }; "
                "done; "
                "if [ -n \"$found\" ]; then bat --color=always \"$found\" | fzf --ansi; "
                "else echo \"No X session error file found\"; read; fi'"
            )
            fn.subprocess.call(
                cmd,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_log_blame(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                "alacritty -e bash -c 'systemd-analyze blame | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_log_dmesg(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                "alacritty -e bash -c 'sudo dmesg --color=always | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    # ====================================================================
    #                       SYSTEM INSPECTION
    # ====================================================================

    def on_click_system_cpu(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.install_package(self, "bat")
            fn.subprocess.call(
                "alacritty -e bash -c 'lscpu | bat --color=always -l conf | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_memory_disk(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e bash -c 'echo \"=== MEMORY ===\"; free -h; echo; echo \"=== DISK USAGE ===\"; df -h'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_lsblk(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                "alacritty -e bash -c 'lsblk -f -o+SIZE | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_lspci(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                "alacritty -e bash -c 'lspci -vnn | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_lsusb(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                "alacritty -e bash -c 'lsusb | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_lsmod(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.install_package(self, "bat")
            fn.subprocess.call(
                "alacritty -e bash -c 'lsmod | bat --color=always -l conf | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_inxi(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.install_package(self, "inxi")
            fn.subprocess.call(
                "alacritty -e bash -c 'inxi -Fxx -c 2 --za | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_hwinfo(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.install_package(self, "hwinfo")
            fn.install_package(self, "bat")
            fn.subprocess.call(
                "alacritty -e bash -c 'hwinfo --short | bat --color=always -l conf | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_fdisk(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.install_package(self, "bat")
            fn.subprocess.call(
                "alacritty -e bash -c 'sudo fdisk -l | bat --color=always -l conf | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_fstab(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.install_package(self, "bat")
            fn.subprocess.call(
                "alacritty -e bash -c 'bat --color=always /etc/fstab | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_hostnamectl(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e bash -c 'hostnamectl'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_localectl(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e bash -c 'localectl'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_services(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                "alacritty -e bash -c 'SYSTEMD_COLORS=1 systemctl list-units --type=service | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_services_enabled(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                "alacritty -e bash -c 'SYSTEMD_COLORS=1 systemctl list-unit-files --type=service --state=enabled | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_services_failed(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                "alacritty -e bash -c 'SYSTEMD_COLORS=1 systemctl list-units --failed | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_timers_enabled(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            import pwd
            uid = pwd.getpwnam(fn.sudo_username).pw_uid
            fn.subprocess.call(
                "alacritty -e bash -c '{ echo \"=== System Timers ===\"; "
                "SYSTEMD_COLORS=1 systemctl list-unit-files --type=timer --state=enabled; "
                "echo; "
                "echo \"=== User Timers ===\"; "
                "sudo -u " + fn.sudo_username +
                " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
                " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus"
                " SYSTEMD_COLORS=1"
                " systemctl --user list-unit-files --type=timer --state=enabled; "
                "} | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_dmesg(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "fzf")
            fn.subprocess.call(
                "alacritty -e bash -c 'sudo dmesg --color=always | fzf --ansi'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

    def on_click_system_gparted(self, widget):
        try:
            if fn.path.exists("/usr/bin/gparted"):
                print("\n[INFO] Launching gparted")
                fn.subprocess.call(
                    "sudo gparted &",
                    shell=True,
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
                GLib.idle_add(fn.show_in_app_notification, self, "GParted launched")
            else:
                print("\n[INFO] gparted not installed, starting installation")
                process = fn.launch_pacman_install_in_terminal("gparted")
                GLib.idle_add(fn.show_in_app_notification, self, "gparted installation started")

                def wait_install():
                    try:
                        import time
                        print("[INFO] Waiting for gparted installation to complete...")
                        process.wait()
                        print("[INFO] Installation process completed")
                        time.sleep(1)
                        if fn.path.exists("/usr/bin/gparted"):
                            print("[INFO] Binary exists at /usr/bin/gparted, installation successful")
                            GLib.idle_add(fn.show_in_app_notification, self, "gparted installed")
                            time.sleep(1)
                            print("[INFO] Launching gparted")
                            fn.subprocess.Popen(
                                "sudo gparted &",
                                shell=True,
                                stdout=fn.subprocess.PIPE,
                                stderr=fn.subprocess.STDOUT,
                            )
                            GLib.idle_add(fn.show_in_app_notification, self, "GParted launched")
                        else:
                            print("[INFO] Binary NOT found at /usr/bin/gparted, checking for errors...")
                    except Exception as e:
                        print(f"Error: {e}")

                fn.threading.Thread(target=wait_install, daemon=True).start()
        except Exception as error:
            print(error)

    # ====================================================================
    #                       SOFTWARE
    # ====================================================================

    def on_click_software_pamac(self, widget):
        try:
            if fn.path.exists("/usr/bin/pamac-manager"):
                print("\n[INFO] Launching pamac-manager")
                fn.subprocess.Popen(
                    "sudo -E -u " + fn.sudo_username + " pamac-manager &",
                    shell=True,
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
                GLib.idle_add(fn.show_in_app_notification, self, "Pamac launched")
            else:
                print("\n[INFO] pamac-aur not installed, starting installation")
                process = fn.launch_pacman_install_in_terminal("pamac-aur")
                GLib.idle_add(fn.show_in_app_notification, self, "pamac-aur installation started")

                def wait_install():
                    try:
                        import time
                        print("[INFO] Waiting for pamac-aur installation to complete...")
                        process.wait()
                        print("[INFO] Installation process completed")
                        time.sleep(1)
                        if fn.path.exists("/usr/bin/pamac-manager"):
                            print("[INFO] Binary exists at /usr/bin/pamac-manager, installation successful")
                            GLib.idle_add(self.lbl_software_pamac.set_markup, "Pamac - GUI package manager <b>installed</b>")
                            GLib.idle_add(fn.show_in_app_notification, self, "pamac-aur installed")
                            time.sleep(1)
                            print("[INFO] Launching pamac-manager")
                            fn.subprocess.Popen(
                                "sudo -E -u " + fn.sudo_username + " pamac-manager &",
                                shell=True,
                                stdout=fn.subprocess.PIPE,
                                stderr=fn.subprocess.STDOUT,
                            )
                            GLib.idle_add(fn.show_in_app_notification, self, "Pamac launched")
                        else:
                            print("[INFO] Binary NOT found at /usr/bin/pamac-manager, checking for errors...")
                            fn.check_missing_repo_error(self, "", "pamac-aur")
                    except Exception as e:
                        print(f"Error: {e}")

                fn.threading.Thread(target=wait_install, daemon=True).start()
        except Exception as error:
            print(error)


    def on_click_software_octopi(self, widget):
        try:
            if fn.path.exists("/usr/bin/octopi"):
                print("\n[INFO] Launching octopi")
                fn.subprocess.Popen(
                    "sudo -E -u " + fn.sudo_username + " octopi &",
                    shell=True,
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
                GLib.idle_add(fn.show_in_app_notification, self, "Octopi launched")
            else:
                print("\n[INFO] octopi not installed, starting installation")
                process = fn.launch_pacman_install_in_terminal("octopi")
                GLib.idle_add(fn.show_in_app_notification, self, "octopi installation started")

                def wait_install():
                    try:
                        import time
                        print("[INFO] Waiting for octopi installation to complete...")
                        process.wait()
                        print("[INFO] Installation process completed")
                        time.sleep(1)
                        if fn.path.exists("/usr/bin/octopi"):
                            print("[INFO] Binary exists at /usr/bin/octopi, installation successful")
                            GLib.idle_add(self.lbl_software_octopi.set_markup, "Octopi - GUI package manager <b>installed</b>")
                            GLib.idle_add(fn.show_in_app_notification, self, "octopi installed")
                            time.sleep(1)
                            print("[INFO] Launching octopi")
                            fn.subprocess.Popen(
                                "sudo -E -u " + fn.sudo_username + " octopi &",
                                shell=True,
                                stdout=fn.subprocess.PIPE,
                                stderr=fn.subprocess.STDOUT,
                            )
                            GLib.idle_add(fn.show_in_app_notification, self, "Octopi launched")
                        else:
                            print("[INFO] Binary NOT found at /usr/bin/octopi, checking for errors...")
                            fn.check_missing_repo_error(self, "", "octopi")
                    except Exception as e:
                        print(f"Error: {e}")

                fn.threading.Thread(target=wait_install, daemon=True).start()
        except Exception as error:
            print(error)

    def on_click_software_gnome(self, widget):
        try:
            if fn.path.exists("/usr/bin/gnome-software"):
                print("\n[INFO] Launching gnome-software")
                import pwd
                uid = pwd.getpwnam(fn.sudo_username).pw_uid
                fn.subprocess.Popen(
                    "sudo -E -u " + fn.sudo_username +
                    " HOME=/home/" + fn.sudo_username +
                    " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
                    " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus" +
                    " gnome-software &",
                    shell=True,
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
                GLib.idle_add(fn.show_in_app_notification, self, "GNOME Software launched")
            else:
                print("\n[INFO] gnome-software not installed, starting installation")
                process = fn.launch_pacman_install_in_terminal("gnome-software")
                GLib.idle_add(fn.show_in_app_notification, self, "gnome-software installation started")

                def wait_install():
                    try:
                        import time
                        import pwd
                        print("[INFO] Waiting for gnome-software installation to complete...")
                        process.wait()
                        print("[INFO] Installation process completed")
                        time.sleep(1)
                        if fn.path.exists("/usr/bin/gnome-software"):
                            print("[INFO] Binary exists at /usr/bin/gnome-software, installation successful")
                            GLib.idle_add(self.lbl_software_gnome.set_markup, "GNOME Software - GUI package manager <b>installed</b>")
                            GLib.idle_add(fn.show_in_app_notification, self, "gnome-software installed")
                            time.sleep(1)
                            print("[INFO] Launching gnome-software")
                            uid = pwd.getpwnam(fn.sudo_username).pw_uid
                            fn.subprocess.Popen(
                                "sudo -E -u " + fn.sudo_username +
                                " HOME=/home/" + fn.sudo_username +
                                " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
                                " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus" +
                                " gnome-software &",
                                shell=True,
                                stdout=fn.subprocess.PIPE,
                                stderr=fn.subprocess.STDOUT,
                            )
                            GLib.idle_add(fn.show_in_app_notification, self, "gnome-software launched")
                        else:
                            print("[INFO] Binary NOT found at /usr/bin/gnome-software, checking for errors...")
                            fn.check_missing_repo_error(self, "", "gnome-software")
                    except Exception as e:
                        print(f"Error: {e}")

                fn.threading.Thread(target=wait_install, daemon=True).start()
        except Exception as error:
            print(error)

    def on_click_software_discover(self, widget):
        try:
            if not fn.path.exists("/usr/bin/plasma-discover"):
                print("\n[INFO] plasma-discover not installed, starting installation")
                process = fn.launch_pacman_install_in_terminal("discover packagekit-qt6")
                GLib.idle_add(fn.show_in_app_notification, self, "discover installation started")

                def wait_install():
                    try:
                        import time
                        import pwd
                        print("[INFO] Waiting for discover installation to complete...")
                        process.wait()
                        print("[INFO] Installation process completed")
                        time.sleep(1)
                        if fn.path.exists("/usr/bin/plasma-discover"):
                            print("[INFO] Binary exists at /usr/bin/plasma-discover, installation successful")
                            GLib.idle_add(self.lbl_software_discover.set_markup, "KDE Discover - KDE software center (pulls KDE deps) <b>installed</b>")
                            GLib.idle_add(fn.show_in_app_notification, self, "plasma-discover installed")
                            print("[INFO] Launching plasma-discover")
                            uid = pwd.getpwnam(fn.sudo_username).pw_uid
                            fn.subprocess.Popen(
                                "DISPLAY=:0 sudo -E -u " + fn.sudo_username +
                                " HOME=/home/" + fn.sudo_username +
                                " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
                                " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus" +
                                " plasma-discover",
                                shell=True,
                                stdout=fn.subprocess.DEVNULL,
                                stderr=fn.subprocess.DEVNULL,
                            )
                        else:
                            print("[INFO] Binary NOT found at /usr/bin/plasma-discover, checking for errors...")
                    except Exception as e:
                        print(f"Error: {e}")

                fn.threading.Thread(target=wait_install, daemon=True).start()
            else:
                print("\n[INFO] Launching plasma-discover")
                import pwd
                uid = pwd.getpwnam(fn.sudo_username).pw_uid
                fn.subprocess.Popen(
                    "DISPLAY=:0 sudo -E -u " + fn.sudo_username +
                    " HOME=/home/" + fn.sudo_username +
                    " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
                    " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus" +
                    " plasma-discover",
                    shell=True,
                    stdout=fn.subprocess.DEVNULL,
                    stderr=fn.subprocess.DEVNULL,
                )
                GLib.idle_add(fn.show_in_app_notification, self, "KDE Discover launched")
        except Exception as error:
            print(error)

    def on_click_software_bauh(self, widget):
        try:
            if fn.path.exists("/usr/bin/bauh"):
                print("\n[INFO] Launching bauh")
                fn.subprocess.Popen(
                    "sudo -E -u " + fn.sudo_username + " bauh &",
                    shell=True,
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
                GLib.idle_add(fn.show_in_app_notification, self, "Bauh launched")
            else:
                print("\n[INFO] bauh not installed, starting installation")
                process = fn.launch_pacman_install_in_terminal("bauh")
                GLib.idle_add(fn.show_in_app_notification, self, "bauh installation started")
                fn.wait_install_and_update(process, "/usr/bin/bauh", self.lbl_software_bauh, "Bauh - Multi-format package manager <b>installed</b>", self, "bauh installation complete", "bauh")
        except Exception as error:
            print(error)

    def on_click_software_yay(self, widget):
        try:
            if fn.path.exists("/usr/bin/yay"):
                print("\n[INFO] yay-git already installed")
                GLib.idle_add(fn.show_in_app_notification, self, "yay-git already installed")
                return
            process = fn.launch_pacman_install_in_terminal("yay-git")
            GLib.idle_add(fn.show_in_app_notification, self, "yay-git installation started")
            fn.wait_install_and_update(process, "/usr/bin/yay", self.lbl_software_yay, "Yay-git - AUR helper (Go-based) <b>installed</b>", self, "yay-git installed", "yay-git")
        except Exception as error:
            print(error)

    def on_click_software_paru(self, widget):
        try:
            if fn.path.exists("/usr/bin/paru"):
                print("\n[INFO] paru-git already installed")
                GLib.idle_add(fn.show_in_app_notification, self, "paru-git already installed")
                return
            process = fn.launch_pacman_install_in_terminal("paru-git")
            GLib.idle_add(fn.show_in_app_notification, self, "paru-git installation started")
            fn.wait_install_and_update(process, "/usr/bin/paru", self.lbl_software_paru, "Paru-git - AUR helper (Rust-based) <b>installed</b>", self, "paru-git installed", "paru-git")
        except Exception as error:
            print(error)

    def on_click_software_trizen(self, widget):
        try:
            if fn.path.exists("/usr/bin/trizen"):
                print("\n[INFO] trizen already installed")
                GLib.idle_add(fn.show_in_app_notification, self, "trizen already installed")
                return
            print("\n[INFO] trizen not installed, starting installation")
            process = fn.launch_pacman_install_in_terminal("trizen")
            GLib.idle_add(fn.show_in_app_notification, self, "trizen installation started")
            fn.wait_install_and_update(process, "/usr/bin/trizen", self.lbl_software_trizen, "Trizen - AUR helper (Perl-based) <b>installed</b>", self, "trizen installed", "trizen")
        except Exception as error:
            print(error)

    def on_click_software_pikaur(self, widget):
        try:
            if fn.path.exists("/usr/bin/pikaur"):
                print("\n[INFO] pikaur-git already installed")
                GLib.idle_add(fn.show_in_app_notification, self, "pikaur-git already installed")
                return
            print("\n[INFO] pikaur-git not installed, starting installation")
            process = fn.launch_pacman_install_in_terminal("pikaur-git")
            GLib.idle_add(fn.show_in_app_notification, self, "pikaur-git installation started")
            fn.wait_install_and_update(process, "/usr/bin/pikaur", self.lbl_software_pikaur, "Pikaur-git - AUR helper (Python-based) <b>installed</b>", self, "pikaur-git installed")
        except Exception as error:
            print(error)

    def on_click_software_yay_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("yay-git")
            GLib.idle_add(fn.show_in_app_notification, self, "yay-git removal started")
            fn.wait_remove_and_update(process, "/usr/bin/yay", self.lbl_software_yay, "Yay-git - AUR helper (Go-based)", self, "yay-git removal complete")
        except Exception as error:
            print(error)

    def on_click_software_paru_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("paru-git")
            GLib.idle_add(fn.show_in_app_notification, self, "paru-git removal started")
            fn.wait_remove_and_update(process, "/usr/bin/paru", self.lbl_software_paru, "Paru-git - AUR helper (Rust-based)", self, "paru-git removal complete")
        except Exception as error:
            print(error)

    def on_click_software_trizen_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("trizen")
            GLib.idle_add(fn.show_in_app_notification, self, "trizen removal started")
            fn.wait_remove_and_update(process, "/usr/bin/trizen", self.lbl_software_trizen, "Trizen - AUR helper (Perl-based)", self, "trizen removal complete")
        except Exception as error:
            print(error)

    def on_click_software_pikaur_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("pikaur-git")
            GLib.idle_add(fn.show_in_app_notification, self, "pikaur-git removal started")
            fn.wait_remove_and_update(process, "/usr/bin/pikaur", self.lbl_software_pikaur, "Pikaur-git - AUR helper (Python-based)", self, "pikaur-git removal complete")
        except Exception as error:
            print(error)

    def on_click_software_pacui_open(self, widget):
        try:
            if not fn.path.exists("/usr/bin/pacui"):
                print("\n[INFO] pacui not installed, starting installation")
                script = "pacman -S --noconfirm pacui; echo ''; echo '=== Installation complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
                process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
                GLib.idle_add(fn.show_in_app_notification, self, "pacui installation started")

                def wait_install():
                    try:
                        import time
                        print("[INFO] Waiting for pacui installation to complete...")
                        process.wait()
                        print("[INFO] Installation process completed")
                        time.sleep(1)
                        if fn.path.exists("/usr/bin/pacui"):
                            print("[INFO] Binary exists at /usr/bin/pacui, installation successful")
                            GLib.idle_add(self.lbl_software_pacui.set_markup, "Pacui - TUI pacman wrapper <b>installed</b>")
                            GLib.idle_add(fn.show_in_app_notification, self, "pacui installed")
                            time.sleep(1)
                            print("[INFO] Launching pacui")
                            fn.subprocess.Popen(
                                ["alacritty", "-e", "sudo", "-u", fn.sudo_username, "pacui"],
                                stdout=fn.subprocess.PIPE,
                                stderr=fn.subprocess.STDOUT,
                            )
                            GLib.idle_add(fn.show_in_app_notification, self, "pacui launched")
                        else:
                            print("[INFO] Binary NOT found at /usr/bin/pacui, checking for errors...")
                    except Exception as e:
                        print(f"Error: {e}")

                fn.threading.Thread(target=wait_install, daemon=True).start()
            else:
                print("\n[INFO] Launching pacui")
                fn.subprocess.Popen(
                    ["alacritty", "-e", "sudo", "-u", fn.sudo_username, "pacui"],
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
                GLib.idle_add(fn.show_in_app_notification, self, "pacui launched")
        except Exception as error:
            print(error)

    def on_click_software_pacui_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("pacui")
            GLib.idle_add(fn.show_in_app_notification, self, "pacui removal started")
            fn.wait_remove_and_update(process, "/usr/bin/pacui", self.lbl_software_pacui, "Pacui - TUI pacman wrapper", self, "pacui removal complete")
        except Exception as error:
            print(error)

    def on_click_software_flatpak(self, widget):
        try:
            if not fn.path.exists("/usr/bin/flatpak"):
                print("\n[INFO] flatpak not installed, starting installation")
                script = "pacman -S --noconfirm flatpak; echo ''; echo '=== Installation complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
                process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
                GLib.idle_add(fn.show_in_app_notification, self, "flatpak installation started")

                def wait_install():
                    try:
                        import time
                        print("[INFO] Waiting for flatpak installation to complete...")
                        process.wait()
                        print("[INFO] Installation process completed")
                        time.sleep(1)
                        if fn.path.exists("/usr/bin/flatpak"):
                            print("[INFO] Binary exists at /usr/bin/flatpak, installation successful")
                            GLib.idle_add(self.lbl_software_flatpak.set_markup, "Flatpak - Manage Flatpak apps <b>installed</b>")
                            GLib.idle_add(fn.show_in_app_notification, self, "flatpak installed")
                            time.sleep(1)
                            print("[INFO] Launching flatpak")
                            script = (
                                "echo '=== Installed Flatpak apps ===' && "
                                "sudo -u " + fn.sudo_username + " flatpak list && "
                                "echo '' && "
                                "echo 'To install an app: flatpak install flathub <app-id>'"
                            )
                            fn.subprocess.Popen(
                                ["alacritty", "--hold", "-e", "bash", "-c", script],
                                stdout=fn.subprocess.PIPE,
                                stderr=fn.subprocess.STDOUT,
                            )
                            GLib.idle_add(fn.show_in_app_notification, self, "flatpak launched")
                        else:
                            print("[INFO] Binary NOT found at /usr/bin/flatpak, checking for errors...")
                    except Exception as e:
                        print(f"Error: {e}")

                fn.threading.Thread(target=wait_install, daemon=True).start()
            else:
                print("\n[INFO] Launching flatpak")
                script = (
                    "echo '=== Installed Flatpak apps ===' && "
                    "sudo -u " + fn.sudo_username + " flatpak list && "
                    "echo '' && "
                    "echo 'To install an app: flatpak install flathub <app-id>'"
                )
                fn.subprocess.Popen(
                    ["alacritty", "--hold", "-e", "bash", "-c", script],
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
                GLib.idle_add(fn.show_in_app_notification, self, "flatpak launched")
        except Exception as error:
            print(error)

    def on_click_software_flatpak_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("flatpak")
            GLib.idle_add(fn.show_in_app_notification, self, "flatpak removal started")
            fn.wait_remove_and_update(process, "/usr/bin/flatpak", self.lbl_software_flatpak, "Flatpak - Manage Flatpak apps", self, "flatpak removal complete")
        except Exception as error:
            print(error)

    def on_click_software_snapd(self, widget):
        try:
            if not fn.path.exists("/usr/bin/snap"):
                aur_helper = fn.get_aur_helper()
                if aur_helper is None:
                    GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found - install yay, paru, trizen or pikaur first")
                    return
                print("\n[INFO] snapd not installed, starting installation")
                process = fn.launch_aur_install_in_terminal(aur_helper, "snapd")
                GLib.idle_add(fn.show_in_app_notification, self, "snapd installation started")

                def wait_install():
                    try:
                        import time
                        print("[INFO] Waiting for snapd installation to complete...")
                        process.wait()
                        print("[INFO] Installation process completed")
                        time.sleep(1)
                        if fn.path.exists("/usr/bin/snap"):
                            print("[INFO] Binary exists at /usr/bin/snap, installation successful")
                            GLib.idle_add(self.lbl_software_snapd.set_markup, "Snapd - Manage Snap apps <b>installed</b>")
                            GLib.idle_add(fn.show_in_app_notification, self, "snapd installed")
                        else:
                            print("[INFO] Binary NOT found at /usr/bin/snap, checking for errors...")
                    except Exception as e:
                        print(f"Error: {e}")

                fn.threading.Thread(target=wait_install, daemon=True).start()
            else:
                print("\n[INFO] Launching snapd")
                script = (
                    "echo '=== Installed Snap apps ===' && "
                    "sudo -u " + fn.sudo_username + " snap list && "
                    "echo '' && "
                    "echo 'To install an app: snap install <app-name>'"
                )
                fn.subprocess.Popen(
                    ["alacritty", "--hold", "-e", "bash", "-c", script],
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
                GLib.idle_add(fn.show_in_app_notification, self, "snapd launched")
        except Exception as error:
            print(error)

    def on_click_software_snapd_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("snapd")
            GLib.idle_add(fn.show_in_app_notification, self, "snapd removal started")
            fn.wait_remove_and_update(process, "/usr/bin/snap", self.lbl_software_snapd, "Snapd - Manage Snap apps", self, "snapd removal complete")
        except Exception as error:
            print(error)

    def on_click_software_appimagelauncher(self, widget):
        try:
            if not fn.path.exists("/usr/bin/app-manager"):
                aur_helper = fn.get_aur_helper()
                if aur_helper is None:
                    GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found - install yay, paru, trizen or pikaur first")
                    return
                print("\n[INFO] appmanager not installed, starting installation")
                process = fn.launch_aur_install_in_terminal(aur_helper, "appmanager")
                GLib.idle_add(fn.show_in_app_notification, self, "appmanager installation started")

                def wait_install():
                    try:
                        import time
                        import pwd
                        print("[INFO] Waiting for appmanager installation to complete...")
                        process.wait()
                        print("[INFO] Installation process completed")
                        time.sleep(1)
                        if fn.path.exists("/usr/bin/app-manager"):
                            print("[INFO] Binary exists at /usr/bin/app-manager, installation successful")
                            GLib.idle_add(self.lbl_software_appimagelauncher.set_markup, "App-manager - Manage AppImages <b>installed</b>")
                            GLib.idle_add(fn.show_in_app_notification, self, "appmanager installed")
                            time.sleep(1)
                            print("[INFO] Launching app-manager")
                            uid = pwd.getpwnam(fn.sudo_username).pw_uid
                            fn.subprocess.Popen(
                                "sudo -E -u " + fn.sudo_username +
                                " HOME=/home/" + fn.sudo_username +
                                " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
                                " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus" +
                                " app-manager &",
                                shell=True,
                                stdout=fn.subprocess.PIPE,
                                stderr=fn.subprocess.STDOUT,
                            )
                            GLib.idle_add(fn.show_in_app_notification, self, "app-manager launched")
                        else:
                            print("[INFO] Binary NOT found at /usr/bin/app-manager, checking for errors...")
                    except Exception as e:
                        print(f"Error: {e}")

                fn.threading.Thread(target=wait_install, daemon=True).start()
                return
            print("\n[INFO] Launching app-manager")
            import pwd
            uid = pwd.getpwnam(fn.sudo_username).pw_uid
            fn.subprocess.call(
                "sudo -E -u " + fn.sudo_username +
                " HOME=/home/" + fn.sudo_username +
                " XDG_RUNTIME_DIR=/run/user/" + str(uid) +
                " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(uid) + "/bus" +
                " app-manager &",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            GLib.idle_add(fn.show_in_app_notification, self, "App-manager launched")
        except Exception as error:
            print(error)

    def on_click_software_appimagelauncher_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("appmanager")
            GLib.idle_add(fn.show_in_app_notification, self, "appmanager removal started")
            fn.wait_remove_and_update(process, "/usr/bin/app-manager", self.lbl_software_appimagelauncher, "App-manager - Manage AppImages", self, "appmanager removal complete")
        except Exception as error:
            print(error)

    def on_click_software_pacseek(self, widget):
        try:
            if not fn.path.exists("/usr/bin/pacseek"):
                print("\n[INFO] pacseek not installed, starting installation")
                script = "pacman -S --noconfirm pacseek; echo ''; echo '=== Installation complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
                process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
                GLib.idle_add(fn.show_in_app_notification, self, "pacseek installation started")

                def wait_install():
                    try:
                        import time
                        print("[INFO] Waiting for pacseek installation to complete...")
                        process.wait()
                        print("[INFO] Installation process completed")
                        time.sleep(1)
                        if fn.path.exists("/usr/bin/pacseek"):
                            print("[INFO] Binary exists at /usr/bin/pacseek, installation successful")
                            GLib.idle_add(self.lbl_software_pacseek.set_markup, "Pacseek - TUI package searcher <b>installed</b>")
                            GLib.idle_add(fn.show_in_app_notification, self, "pacseek installed")
                            time.sleep(1)
                            print("[INFO] Launching pacseek")
                            fn.subprocess.Popen(
                                ["alacritty", "-e", "sudo", "-u", fn.sudo_username, "pacseek"],
                                stdout=fn.subprocess.PIPE,
                                stderr=fn.subprocess.STDOUT,
                            )
                            GLib.idle_add(fn.show_in_app_notification, self, "pacseek launched")
                        else:
                            print("[INFO] Binary NOT found at /usr/bin/pacseek, checking for errors...")
                    except Exception as e:
                        print(f"Error: {e}")

                fn.threading.Thread(target=wait_install, daemon=True).start()
            else:
                print("\n[INFO] Launching pacseek")
                fn.subprocess.Popen(
                    ["alacritty", "-e", "sudo", "-u", fn.sudo_username, "pacseek"],
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
                GLib.idle_add(fn.show_in_app_notification, self, "pacseek launched")
        except Exception as error:
            print(error)

    def on_click_software_pacseek_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("pacseek")
            GLib.idle_add(fn.show_in_app_notification, self, "pacseek removal started")
            fn.wait_remove_and_update(process, "/usr/bin/pacseek", self.lbl_software_pacseek, "Pacseek - TUI package searcher", self, "pacseek removal complete")
        except Exception as error:
            print(error)

    def on_click_software_pamac_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("pamac-aur")
            GLib.idle_add(fn.show_in_app_notification, self, "pamac-aur removal started")

            fn.wait_remove_and_update(process, "/usr/bin/pamac-manager", self.lbl_software_pamac, "Pamac - GUI package manager", self, "pamac-aur removal complete")
        except Exception as error:
            print(error)

    def on_click_software_octopi_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("octopi")
            GLib.idle_add(fn.show_in_app_notification, self, "octopi removal started")

            fn.wait_remove_and_update(process, "/usr/bin/octopi", self.lbl_software_octopi, "Octopi - GUI package manager", self, "octopi removal complete")
        except Exception as error:
            print(error)

    def on_click_software_gnome_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("gnome-software")
            GLib.idle_add(fn.show_in_app_notification, self, "gnome-software removal started")

            fn.wait_remove_and_update(process, "/usr/bin/gnome-software", self.lbl_software_gnome, "GNOME Software - GUI package manager", self, "gnome-software removal complete")
        except Exception as error:
            print(error)

    def on_click_software_discover_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("discover")
            GLib.idle_add(fn.show_in_app_notification, self, "plasma-discover removal started")

            fn.wait_remove_and_update(process, "/usr/bin/plasma-discover", self.lbl_software_discover, "KDE Discover - GUI package manager", self, "plasma-discover removal complete")
        except Exception as error:
            print(error)

    def on_click_software_bauh_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("bauh")
            GLib.idle_add(fn.show_in_app_notification, self, "bauh removal started")

            fn.wait_remove_and_update(process, "/usr/bin/bauh", self.lbl_software_bauh, "Bauh - GUI package manager", self, "bauh removal complete")
        except Exception as error:
            print(error)

    def on_click_software_archlinux_logout(self, widget):
        try:
            if fn.path.exists("/usr/bin/archlinux-logout-gtk4"):
                print("\n[INFO] Launching archlinux-logout-gtk4")
                fn.subprocess.Popen(
                    "archlinux-logout-gtk4 &",
                    shell=True,
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
                GLib.idle_add(fn.show_in_app_notification, self, "ArchLinux Logout launched")
            else:
                print("\n[INFO] archlinux-logout-gtk4-git not installed, starting installation")
                process = fn.launch_pacman_install_in_terminal("archlinux-logout-gtk4-git")
                GLib.idle_add(fn.show_in_app_notification, self, "archlinux-logout-gtk4-git installation started")

                def wait_install():
                    try:
                        import time
                        print("[INFO] Waiting for archlinux-logout-gtk4-git installation to complete...")
                        process.wait()
                        print("[INFO] Installation process completed")
                        time.sleep(1)
                        if fn.path.exists("/usr/bin/archlinux-logout-gtk4"):
                            print("[INFO] Binary exists at /usr/bin/archlinux-logout-gtk4, installation successful")
                            GLib.idle_add(self.lbl_software_archlinux_logout.set_markup, "ArchLinux Logout - Session logout tool <b>installed</b>")
                            GLib.idle_add(fn.show_in_app_notification, self, "archlinux-logout-gtk4-git installed")
                            time.sleep(1)
                            print("[INFO] Launching archlinux-logout-gtk4")
                            fn.subprocess.Popen(
                                "archlinux-logout-gtk4 &",
                                shell=True,
                                stdout=fn.subprocess.PIPE,
                                stderr=fn.subprocess.STDOUT,
                            )
                            GLib.idle_add(fn.show_in_app_notification, self, "ArchLinux Logout launched")
                        else:
                            print("[INFO] Binary NOT found at /usr/bin/archlinux-logout-gtk4, checking for errors...")
                            fn.check_missing_repo_error(self, "", "archlinux-logout-gtk4-git")
                    except Exception as e:
                        print(f"Error: {e}")

                fn.threading.Thread(target=wait_install, daemon=True).start()
        except Exception as error:
            print(error)

    def on_click_software_archlinux_logout_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("archlinux-logout-gtk4-git")
            GLib.idle_add(fn.show_in_app_notification, self, "archlinux-logout-gtk4-git removal started")

            fn.wait_remove_and_update(process, "/usr/bin/archlinux-logout-gtk4", self.lbl_software_archlinux_logout, "ArchLinux Logout - Session logout tool", self, "archlinux-logout-gtk4-git removal complete")
        except Exception as error:
            print(error)

    def on_click_software_powermenu(self, widget):
        try:
            if fn.path.exists("/usr/local/bin/edu-powermenu"):
                print("\n[INFO] Launching edu-powermenu")
                fn.subprocess.Popen(
                    "edu-powermenu &",
                    shell=True,
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
                GLib.idle_add(fn.show_in_app_notification, self, "powermenu launched")
            else:
                print("\n[INFO] edu-powermenu-git not installed, starting installation")
                process = fn.launch_pacman_install_in_terminal("edu-powermenu-git")
                GLib.idle_add(fn.show_in_app_notification, self, "edu-powermenu-git installation started")

                def wait_install():
                    try:
                        import time
                        print("[INFO] Waiting for edu-powermenu-git installation to complete...")
                        process.wait()
                        print("[INFO] Installation process completed")
                        time.sleep(1)
                        if fn.path.exists("/usr/local/bin/edu-powermenu"):
                            print("[INFO] Binary exists at /usr/local/bin/edu-powermenu, installation successful")
                            GLib.idle_add(self.lbl_software_powermenu.set_markup, "powermenu - Power menu for i3/sway <b>installed</b>")
                            GLib.idle_add(fn.show_in_app_notification, self, "edu-powermenu-git installed")
                            time.sleep(1)
                            print("[INFO] Launching edu-powermenu")
                            fn.subprocess.Popen(
                                "edu-powermenu &",
                                shell=True,
                                stdout=fn.subprocess.PIPE,
                                stderr=fn.subprocess.STDOUT,
                            )
                            GLib.idle_add(fn.show_in_app_notification, self, "powermenu launched")
                        else:
                            print("[INFO] Binary NOT found at /usr/local/bin/edu-powermenu, checking for errors...")
                            fn.check_missing_repo_error(self, "", "edu-powermenu-git")
                    except Exception as e:
                        print(f"Error: {e}")

                fn.threading.Thread(target=wait_install, daemon=True).start()
        except Exception as error:
            print(error)

    def on_click_software_powermenu_remove(self, widget):
        try:
            process = fn.launch_pacman_remove_in_terminal("edu-powermenu-git")
            GLib.idle_add(fn.show_in_app_notification, self, "edu-powermenu-git removal started")

            fn.wait_remove_and_update(process, "/usr/local/bin/edu-powermenu", self.lbl_software_powermenu, "powermenu - Power menu for i3/sway", self, "edu-powermenu-git removal complete")
        except Exception as error:
            print(error)

    # ====================================================================
    #                       AI TOOLS
    # ====================================================================

    def on_click_ai_ollama(self, widget):
        try:
            if fn.path.exists("/usr/bin/ollama"):
                process = fn.launch_pacman_remove_in_terminal("ollama")
                def wait_removal():
                    process.wait()
                    GLib.idle_add(self.lbl_ai_ollama.set_markup, "Ollama - Local LLM runner")
                    GLib.idle_add(self.btn_ai_ollama.set_label, "Install")
                    GLib.idle_add(fn.show_in_app_notification, self, "ollama removal complete")
                fn.threading.Thread(target=wait_removal, daemon=True).start()
                GLib.idle_add(fn.show_in_app_notification, self, "ollama removal started")
            else:
                has_nvidia = fn.path.exists("/dev/nvidia0")
                pkgs = "ollama ollama-cuda" if has_nvidia else "ollama"
                process = fn.launch_pacman_install_in_terminal(pkgs)
                def wait_install():
                    try:
                        stdout_data, stderr_data = process.communicate()
                        stdout_str = stdout_data.decode() if stdout_data else ""
                        stderr_str = stderr_data.decode() if stderr_data else ""
                        error_output = stderr_str + stdout_str
                        if fn.path.exists("/usr/bin/ollama"):
                            GLib.idle_add(self.lbl_ai_ollama.set_markup, "Ollama - Local LLM runner <b>installed</b>")
                            GLib.idle_add(self.btn_ai_ollama.set_label, "Remove")
                            GLib.idle_add(fn.show_in_app_notification, self, "ollama installation complete")
                        else:
                            fn.check_missing_repo_error(self, error_output, "ollama")
                    except Exception as e:
                        print(f"Error in ollama wait_install: {e}")
                fn.threading.Thread(target=wait_install, daemon=True).start()
                GLib.idle_add(fn.show_in_app_notification, self, "ollama installation started")
        except Exception as error:
            print(error)

    def on_click_ai_webui(self, widget):
        try:
            if fn.path.exists("/usr/bin/open-webui"):
                process = fn.launch_pacman_remove_in_terminal("open-webui")
                def wait_removal():
                    process.wait()
                    GLib.idle_add(self.lbl_ai_webui.set_markup, "Open WebUI - Browser UI for Ollama")
                    GLib.idle_add(self.btn_ai_webui.set_label, "Install")
                    GLib.idle_add(fn.show_in_app_notification, self, "open-webui removal complete")
                fn.threading.Thread(target=wait_removal, daemon=True).start()
                GLib.idle_add(fn.show_in_app_notification, self, "open-webui removal started")
            else:
                aur_helper = fn.get_aur_helper()
                if aur_helper is None:
                    GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found. Install yay or paru first.")
                    return
                process = fn.launch_aur_install_in_terminal(aur_helper, "open-webui")
                def wait_install():
                    try:
                        stdout_data, stderr_data = process.communicate()
                        stdout_str = stdout_data.decode() if stdout_data else ""
                        stderr_str = stderr_data.decode() if stderr_data else ""
                        error_output = stderr_str + stdout_str
                        if fn.path.exists("/usr/bin/open-webui"):
                            GLib.idle_add(self.lbl_ai_webui.set_markup, "Open WebUI - Browser UI for Ollama <b>installed</b>")
                            GLib.idle_add(self.btn_ai_webui.set_label, "Remove")
                            GLib.idle_add(fn.show_in_app_notification, self, "open-webui installation complete")
                        else:
                            fn.check_missing_repo_error(self, error_output, "open-webui")
                    except Exception as e:
                        print(f"Error in open-webui wait_install: {e}")
                fn.threading.Thread(target=wait_install, daemon=True).start()
                GLib.idle_add(fn.show_in_app_notification, self, "open-webui installation started")
        except Exception as error:
            print(error)

    def on_click_ai_claude(self, widget):
        try:
            if fn.path.exists("/usr/bin/claude"):
                process = fn.launch_pacman_remove_in_terminal("claude-code")
                def wait_removal():
                    process.wait()
                    GLib.idle_add(self.lbl_ai_claude.set_markup, "Claude Code - Anthropic CLI")
                    GLib.idle_add(self.btn_ai_claude.set_label, "Install")
                    GLib.idle_add(fn.show_in_app_notification, self, "claude-code removal complete")
                fn.threading.Thread(target=wait_removal, daemon=True).start()
                GLib.idle_add(fn.show_in_app_notification, self, "claude-code removal started")
            else:
                aur_helper = fn.get_aur_helper()
                if aur_helper is None:
                    GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found. Install yay or paru first.")
                    return
                process = fn.launch_aur_install_in_terminal(aur_helper, "claude-code")
                def wait_install():
                    process.wait()
                    if fn.path.exists("/usr/bin/claude"):
                        GLib.idle_add(self.lbl_ai_claude.set_markup, "Claude Code - Anthropic CLI <b>installed</b>")
                        GLib.idle_add(self.btn_ai_claude.set_label, "Remove")
                        GLib.idle_add(fn.show_in_app_notification, self, "claude-code installation complete")
                fn.threading.Thread(target=wait_install, daemon=True).start()
                GLib.idle_add(fn.show_in_app_notification, self, "claude-code installation started")
        except Exception as error:
            print(error)

    def on_click_ai_aider(self, widget):
        try:
            aider_path = f"/home/{fn.sudo_username}/.local/bin/aider"
            if fn.path.exists("/usr/bin/aider") or fn.path.exists(aider_path):
                aur_helper = fn.get_aur_helper()
                script = f"rm -f {aider_path}; "
                if aur_helper:
                    script += f"sudo -u {fn.sudo_username} {aur_helper} -Rs --noconfirm aider-install; "
                script += "echo ''; echo '=== Removal complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
                process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
                def wait_removal():
                    process.wait()
                    GLib.idle_add(self.lbl_ai_aider.set_markup, "Aider - AI pair programming")
                    GLib.idle_add(self.btn_ai_aider.set_label, "Install")
                    GLib.idle_add(fn.show_in_app_notification, self, "aider removal complete")
                fn.threading.Thread(target=wait_removal, daemon=True).start()
                GLib.idle_add(fn.show_in_app_notification, self, "aider removal started")
            else:
                aur_helper = fn.get_aur_helper()
                if aur_helper is None:
                    GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found. Install yay or paru first.")
                    return
                process = fn.launch_aur_install_in_terminal(aur_helper, "aider-install")
                def wait_install():
                    try:
                        import time
                        process.wait()
                        time.sleep(1)
                        fn.subprocess.call(f"sudo -u {fn.sudo_username} aider-install", shell=True, stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT)
                        if fn.path.exists("/usr/bin/aider") or fn.path.exists(aider_path):
                            GLib.idle_add(self.lbl_ai_aider.set_markup, "Aider - AI pair programming <b>installed</b>")
                            GLib.idle_add(self.btn_ai_aider.set_label, "Remove")
                            GLib.idle_add(fn.show_in_app_notification, self, "aider installation complete")
                        else:
                            print(f"Aider binary not found. Checked: /usr/bin/aider and {aider_path}")
                    except Exception as e:
                        print(f"Error in wait_install: {e}")
                fn.threading.Thread(target=wait_install, daemon=True).start()
                GLib.idle_add(fn.show_in_app_notification, self, "aider installation started")
        except Exception as error:
            print(error)

    def on_click_ai_codex(self, widget):
        try:
            codex_paths = ["/usr/bin/codex", "/usr/local/bin/codex", f"/home/{fn.sudo_username}/.local/bin/codex", f"/home/{fn.sudo_username}/.npm-global/bin/codex"]
            codex_installed = any(fn.path.exists(p) for p in codex_paths)

            if codex_installed:
                process = fn.launch_npm_remove_in_terminal("@openai/codex")
                if process:
                    def wait_removal():
                        try:
                            import time
                            process.wait()
                            time.sleep(1)
                            GLib.idle_add(self.lbl_ai_codex.set_markup, "OpenAI Codex CLI")
                            GLib.idle_add(self.btn_ai_codex.set_label, "Install")
                            GLib.idle_add(fn.show_in_app_notification, self, "Codex removal complete")
                        except Exception as e:
                            print(f"Error in codex wait_removal: {e}")
                    fn.threading.Thread(target=wait_removal, daemon=True).start()
                    GLib.idle_add(fn.show_in_app_notification, self, "Codex removal started")
                else:
                    GLib.idle_add(fn.show_in_app_notification, self, "Codex removal failed")
            else:
                process = fn.launch_npm_install_in_terminal("@openai/codex")
                if process:
                    def wait_install():
                        try:
                            import time
                            process.wait()
                            time.sleep(1)
                            if any(fn.path.exists(p) for p in codex_paths):
                                GLib.idle_add(self.lbl_ai_codex.set_markup, "OpenAI Codex CLI <b>installed</b>")
                                GLib.idle_add(self.btn_ai_codex.set_label, "Remove")
                                GLib.idle_add(fn.show_in_app_notification, self, "Codex installation complete")
                            else:
                                print(f"Codex binary not found. Checked: {codex_paths}")
                        except Exception as e:
                            print(f"Error in codex wait_install: {e}")
                    fn.threading.Thread(target=wait_install, daemon=True).start()
                    GLib.idle_add(fn.show_in_app_notification, self, "Codex installation started")
                else:
                    GLib.idle_add(fn.show_in_app_notification, self, "Codex installation failed")
        except Exception as error:
            print(error)

    def on_click_ai_gemini(self, widget):
        try:
            gemini_paths = ["/usr/bin/gemini", "/usr/local/bin/gemini", f"/home/{fn.sudo_username}/.local/bin/gemini", f"/home/{fn.sudo_username}/.npm-global/bin/gemini"]
            gemini_installed = any(fn.path.exists(p) for p in gemini_paths)

            if gemini_installed:
                process = fn.launch_npm_remove_in_terminal("@google/gemini-cli")
                if process:
                    def wait_removal():
                        try:
                            import time
                            process.wait()
                            time.sleep(1)
                            GLib.idle_add(self.lbl_ai_gemini.set_markup, "Google Gemini CLI")
                            GLib.idle_add(self.btn_ai_gemini.set_label, "Install")
                            GLib.idle_add(fn.show_in_app_notification, self, "Gemini removal complete")
                        except Exception as e:
                            print(f"Error in gemini wait_removal: {e}")
                    fn.threading.Thread(target=wait_removal, daemon=True).start()
                    GLib.idle_add(fn.show_in_app_notification, self, "Gemini removal started")
                else:
                    GLib.idle_add(fn.show_in_app_notification, self, "Gemini removal failed")
            else:
                process = fn.launch_npm_install_in_terminal("@google/gemini-cli")
                if process:
                    def wait_install():
                        try:
                            import time
                            process.wait()
                            time.sleep(1)
                            if any(fn.path.exists(p) for p in gemini_paths):
                                GLib.idle_add(self.lbl_ai_gemini.set_markup, "Google Gemini CLI <b>installed</b>")
                                GLib.idle_add(self.btn_ai_gemini.set_label, "Remove")
                                GLib.idle_add(fn.show_in_app_notification, self, "Gemini installation complete")
                            else:
                                print(f"Gemini binary not found. Checked: {gemini_paths}")
                        except Exception as e:
                            print(f"Error in gemini wait_install: {e}")
                    fn.threading.Thread(target=wait_install, daemon=True).start()
                    GLib.idle_add(fn.show_in_app_notification, self, "Gemini installation started")
                else:
                    GLib.idle_add(fn.show_in_app_notification, self, "Gemini installation failed")
        except Exception as error:
            print(error)

    def open_url_in_browser(self, url):
        if not fn.ensure_firefox_installed():
            print(f"[ERROR] Cannot open {url}: Firefox installation failed")
            return
        try:
            fn.subprocess.Popen(f"sudo -u {fn.sudo_username} DISPLAY=:0 firefox -new-tab '{url}'", shell=True, stdout=fn.subprocess.DEVNULL, stderr=fn.subprocess.DEVNULL)
        except Exception as error:
            print(error)

    def on_click_ai_ollama_link(self, widget):
        self.open_url_in_browser("https://ollama.com/")

    def on_click_ai_webui_link(self, widget):
        self.open_url_in_browser("https://openwebui.com/")

    def on_click_ai_claude_link(self, widget):
        self.open_url_in_browser("https://code.claude.com/docs/en/cli-reference")

    def on_click_ai_aider_link(self, widget):
        self.open_url_in_browser("https://aider.chat/")

    def on_click_ai_gemini_link(self, widget):
        self.open_url_in_browser("https://geminicli.com/")

    def on_click_ai_codex_link(self, widget):
        self.open_url_in_browser("https://developers.openai.com/codex/cli")

    def on_click_ai_chatgpt(self, widget):
        self.open_url_in_browser("https://chatgpt.com")

    def on_click_ai_chatgpt_link(self, widget):
        self.open_url_in_browser("https://academy.openai.com/")

    def on_click_ai_claude_web_link(self, widget):
        self.open_url_in_browser("https://claude.com/resources/tutorials?open_in_browser=1")

    def on_click_ai_gemini_web_link(self, widget):
        self.open_url_in_browser("https://gemini.google.com/")

    def on_click_ai_perplexity_link(self, widget):
        self.open_url_in_browser("https://www.perplexity.ai/hub/getting-started")

    def on_click_ai_claude_web(self, widget):
        self.open_url_in_browser("https://claude.ai")

    def on_click_ai_gemini_web(self, widget):
        self.open_url_in_browser("https://gemini.google.com")

    def on_click_ai_perplexity(self, widget):
        self.open_url_in_browser("https://perplexity.ai")

    def on_click_ai_dalle_link(self, widget):
        self.open_url_in_browser("https://openai.com/index/dall-e-3/")

    def on_click_ai_dalle(self, widget):
        self.open_url_in_browser("https://openai.com/dall-e-3")

    def on_click_ai_midjourney_link(self, widget):
        self.open_url_in_browser("https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide")

    def on_click_ai_midjourney(self, widget):
        self.open_url_in_browser("https://www.midjourney.com")

    def on_click_ai_leonardo_link(self, widget):
        self.open_url_in_browser("https://leonardo.ai/learn/")

    def on_click_ai_leonardo(self, widget):
        self.open_url_in_browser("https://leonardo.ai")

    def on_click_ai_firefly_link(self, widget):
        self.open_url_in_browser("https://www.adobe.com/learn/firefly")

    def on_click_ai_firefly(self, widget):
        self.open_url_in_browser("https://www.adobe.com/products/firefly")



    # ====================================================================
    #                            PRIVACY
    # ====================================================================

    def set_hblock(self, widget, state):
        if fn.check_edu_repos_active() is True:
            if self.firstrun is not True:
                t = fn.threading.Thread(
                    target=fn.set_hblock, args=(self, widget, widget.get_active())
                )
                t.start()
                print("Hblock is now active/inactive")
                GLib.idle_add(
                    fn.show_in_app_notification, self, "Hblock is active/inactive"
                )
            else:
                self.firstrun = False
        else:
            print("-----------------------------------------------------------------------")
            print("For full ATT functionality, activate chaotic-aur and/or nemesis_repo ")
            print("You can enable the repositories in the pacman menu")
            print("-----------------------------------------------------------------------")
            self.hbswich.set_active(False)
            GLib.idle_add(
                fn.show_in_app_notification, self, "First activate the chaotic-aur and/or the nemesis repo in pacman "
            )

    def set_ublock_firefox(self, widget, state):
        t = fn.threading.Thread(
            target=fn.set_firefox_ublock, args=(self, widget, widget.get_active())
        )
        t.start()

    # ====================================================================
    #                        FASTFETCH CONFIG
    # ====================================================================

    def on_install_fast(self, widget):
        fn.install_package(self, "fastfetch-git")

    # ====================================================================
    #                        FASTFETCH CONFIG
    # ====================================================================

    def on_apply_fast(self, widget):
        small_ascii = "auto"
        backend = "off"
        fastfetch.apply_config(self, backend, small_ascii)

    def on_reset_fast_att(self, widget):
        if fn.path.isfile(fn.fastfetch_arco):
            fn.shutil.copy(fn.fastfetch_arco, fn.fastfetch_config)
            fn.permissions(fn.fastfetch_config)
            print("Fastfetch default ATT settings applied")
            fn.show_in_app_notification(self, "Default settings applied")
            fastfetch.get_checkboxes(self)

    def on_reset_fast(self, widget):
        if fn.path.isfile(fn.fastfetch_config + ".bak"):
            fn.shutil.copy(fn.fastfetch_config + ".bak", fn.fastfetch_config)

            fastfetch.get_checkboxes(self)
            print("fastfetch default settings applied")
            fn.show_in_app_notification(self, "Default settings applied")

    # When using this function to toggle a lolcat: utility = name of tool, e.g. fastfetch

    def lolcat_toggle(self, widget, active, utility):
        lolcat_state = widget.get_active()
        util_state = utilities.get_util_state(self, utility)

        if lolcat_state:
            utilities.install_util(self, "lolcat")
            if not util_state or utility == "fastfetch":
                util_state = True
                utilities.set_util_state(self, utility, True, True)
        elif not lolcat_state and utility == "fastfetch":
            utilities.set_util_state(self, utility, True, False)

    def on_fast_util_toggled(self, switch, gparam):
        util_state = switch.get_active()
        lolcat_state = self.fast_lolcat.get_active()

        if util_state and not fn.path.exists("/usr/bin/fastfetch"):
            print("\n[INFO] fastfetch installation started")
            fn.install_package(self, "fastfetch-git")
            return

        fastfetch.toggle_fastfetch(util_state)

        if not util_state:
            self.fast_lolcat.set_active(False)
            lolcat_state = False

        fastfetch.write_configs(util_state, lolcat_state)
        self.fast_lolcat.set_sensitive(util_state)

    def on_fast_lolcat_toggled(self, switch, gparam):
        lolcat_state = switch.get_active()
        util_state = self.fast_util.get_active()

        if util_state:
            fastfetch.toggle_lolcat(lolcat_state)
            fastfetch.write_configs(util_state, lolcat_state)

    def util_toggle(self, widget, active, utility):
        util_state = widget.get_active()
        lolcat_state = utilities.get_lolcat_state(self, utility)

        if util_state:
            utilities.install_util(self, utility)
            if utility == "fastfetch":
                utilities.set_util_state(self, utility, True, lolcat_state)
        else:
            if lolcat_state:
                lolcat_state = False
            utilities.set_util_state(self, utility, False, False)

    def on_click_fastfetch_all_selection(self, widget):
        print("You have selected all Fastfetch switches")
        fastfetch.set_checkboxes_all(self)

    def on_click_fastfetch_normal_selection(self, widget):
        print("You have selected the normal selection")
        fastfetch.set_checkboxes_normal(self)

    def on_click_fastfetch_small_selection(self, widget):
        print("You have selected the small selection")
        fastfetch.set_checkboxes_small(self)

    def on_click_fastfetch_none_selection(self, widget):
        print("You have not selected any Fastfetch switch")
        fastfetch.set_checkboxes_none(self)

    def on_mirror_seed_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"
        ):
            pmf.append_mirror(self, fn.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_seed")

    def on_mirror_gitlab_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://gitlab.com/arcolinux/$repo/-/raw/main/$arch"
        ):
            pmf.append_mirror(self, fn.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_gitlab")

    def on_mirror_belnet_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"
        ):
            pmf.append_mirror(self, fn.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_belnet")

    def on_mirror_funami_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://mirror.funami.tech/arcolinux/$repo/$arch"
        ):
            pmf.append_mirror(self, fn.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_funami")

    def on_mirror_jingk_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://mirror.jingk.ai/arcolinux/$repo/$arch"
        ):
            pmf.append_mirror(self, fn.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_jingk")

    def on_mirror_accum_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://mirror.accum.se/mirror/arcolinux.info/$repo/$arch"
        ):
            pmf.append_mirror(self, fn.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_accum")

    def on_mirror_aarnet_repo_toggle(self, widget, active):
        if not pmf.mirror_exist(
            "Server = https://mirror.aarnet.edu.au/pub/arcolinux/$repo/$arch"
        ):
            pmf.append_mirror(self, fn.aarnetmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_aarnet")

    # =====================================================
    #               PACMAN CONF
    # =====================================================

    def on_update_pacman_databases_clicked(self, Widget):
        fn.show_in_app_notification(self, "Opening terminal to update pacman databases")
        fn.subprocess.Popen(
            ["alacritty", "-e", "bash", "-c", "sudo pacman -Sy; read -p 'Press Enter to exit...'"],
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.PIPE,
        )

    def on_arcolinux_clicked(self, widget):
        fn.install_arcolinux(self)
        print("ArcoLinux repo added + activated")
        fn.show_in_app_notification(
            self, "ArcoLinux repo added + activated"
        )
        self.on_pacman_arepo_toggle(self.arepo_button, True)
        self.on_pacman_a3p_toggle(self.a3prepo_button, True)
        fn.update_repos(self)
        fn.restart_program()

    def on_pacman_atestrepo_toggle(self, widget, active):
        if not pmf.repo_exist("[arcolinux_repo_testing]"):
            pmf.append_repo(self, fn.atestrepo)
            print("Repo has been added to /etc/pacman.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Repo has been added to /etc/pacman.conf",
            )
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "arco_testing")

    def on_pacman_arepo_toggle(self, widget, active):
        if not pmf.repo_exist("[arcolinux_repo]"):
            pmf.append_repo(self, fn.arepo)
            print("Repo has been added to /etc/pacman.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Repo has been added to /etc/pacman.conf",
            )
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "arco_base")
                if fn.check_arco_repos_active() is True:
                    self.button_install.set_sensitive(True)
                    self.button_reinstall.set_sensitive(True)
                    #self.install_arco_vimix.set_sensitive(True)
                else:
                    self.button_install.set_sensitive(False)
                    self.button_reinstall.set_sensitive(False)
                    #self.install_arco_vimix.set_sensitive(False)

    def on_pacman_a3p_toggle(self, widget, active):
        if not pmf.repo_exist("[arcolinux_repo_3party]"):
            pmf.append_repo(self, fn.a3drepo)
            print("Repo has been added to /etc/pacman.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Repo has been added to /etc/pacman.conf",
            )
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "arco_a3p")
                if fn.check_arco_repos_active() is True:
                    self.button_install.set_sensitive(True)
                    self.button_reinstall.set_sensitive(True)
                else:
                    self.button_install.set_sensitive(False)
                    self.button_reinstall.set_sensitive(False)

    def on_pacman_axl_toggle(self, widget, active):
        if not pmf.repo_exist("[arcolinux_repo_xlarge]"):
            pmf.append_repo(self, fn.axlrepo)
            print("Repo has been added to /etc/pacman.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Repo has been added to /etc/pacman.conf",
            )
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "arco_axl")

    def on_reborn_clicked(self, widget):
        fn.install_reborn(self)
        print("Reborn keyring and mirrors added")
        print("Restart Att and select the repos")
        GLib.idle_add(
            fn.show_in_app_notification, self, "Reborn keyring and mirrors added"
        )
        fn.update_repos(self)

    def on_reborn_toggle(self, widget, active):
        if not pmf.repo_exist("[Reborn-OS]"):
            pmf.append_repo(self, fn.reborn_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "reborn")

    def on_garuda_clicked(self, widget):
        fn.install_chaotics(self)
        print("Chaotics keyring and mirrors added")
        print("Restart Att and select the repos")
        GLib.idle_add(
            fn.show_in_app_notification, self, "Chaotics keyring and mirrors added"
        )
        fn.update_repos(self)

    def on_garuda_toggle(self, widget, active):
        if not pmf.repo_exist("[garuda]"):
            pmf.append_repo(self, fn.garuda_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "garuda")

    def on_chaotics_clicked(self, widget):
        fn.install_chaotics(self)
        print("Chaotics keyring and mirrors added")
        print("Restart Att and select the repos")
        GLib.idle_add(
            fn.show_in_app_notification, self, "Chaotics keyring and mirrors added"
        )
        fn.update_repos(self)

    def on_chaotics_toggle(self, widget, active):
        if not pmf.repo_exist("[chaotic-aur]"):
            pmf.append_repo(self, fn.chaotics_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "chaotics")
        fn.GLib.timeout_add(100, self.refresh_aur_buttons)

    def on_endeavouros_clicked(self, widget):
        fn.install_endeavouros(self)
        print("EndeavourOS keyring and mirrors added")
        print("Restart Att and select the repo")
        fn.show_in_app_notification(self, "Restart Att and select the repo")
        fn.update_repos(self)

    def on_endeavouros_toggle(self, widget, active):
        if not pmf.repo_exist("[endeavouros]"):
            pmf.append_repo(self, fn.endeavouros_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "endeavouros")

    def on_nemesis_toggle(self, widget, active):
        if not pmf.repo_exist("[nemesis_repo]"):
            pmf.append_repo(self, fn.nemesis_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "nemesis")
        fn.update_repos(self)
        desktopr_gui.update_button_state(self, fn)
        fn.GLib.timeout_add(100, self.refresh_aur_buttons)

    def on_pacman_toggle1(self, widget, active):
        if not pmf.repo_exist("[core-testing]"):
            pmf.append_repo(self, fn.arch_testing_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "testing")

    def on_pacman_toggle2(self, widget, active):
        if not pmf.repo_exist("[core]"):
            pmf.append_repo(self, fn.arch_core_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "core")

    def on_pacman_toggle3(self, widget, active):
        if not pmf.repo_exist("[extra]"):
            pmf.append_repo(self, fn.arch_extra_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "extra")

    def on_pacman_toggle4(self, widget, active):
        if not pmf.repo_exist("[extra-testing]"):
            pmf.append_repo(self, fn.arch_community_testing_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "extra-testing")

    def on_pacman_toggle5(self, widget, active):
        if not pmf.repo_exist("[extra-testing]"):
            pmf.append_repo(self, fn.arch_extra_testing_repo)
            print("Repo has been added to /etc/pacman.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Repo has been added to /etc/pacman.conf",
            )
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "community")

    def on_pacman_toggle6(self, widget, active):
        if not pmf.repo_exist("[multilib-testing]"):
            pmf.append_repo(self, fn.arch_multilib_testing_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "multilib-testing")

    def on_pacman_toggle7(self, widget, active):
        if not pmf.repo_exist("[multilib]"):
            pmf.append_repo(self, fn.arch_multilib_repo)
            print("Repo has been added to /etc/pacman.conf")
            fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(), "multilib")

    def custom_repo_clicked(self, widget):
        custom_repo_text = self.textview_custom_repo.get_buffer()
        startiter, enditer = custom_repo_text.get_bounds()
        repo_content = custom_repo_text.get_text(startiter, enditer, True)

        if len(repo_content.strip()) < 5:
            print("[INFO] No custom repo defined")
            fn.show_in_app_notification(self, "No custom repo defined")
            return

        print(repo_content)
        pmf.append_repo(self, repo_content)
        try:
            fn.update_repos(self)
        except Exception as error:
            print(error)
            print("Is the code correct? - check /etc/pacman.conf")

    def blank_pacman(source, target):
        fn.shutil.copy(fn.pacman, fn.pacman + ".bak")
        if fn.distr == "arch":
            fn.shutil.copy(fn.blank_pacman_arch, fn.pacman)
        if fn.distr == "arcolinux":
            fn.shutil.copy(fn.blank_pacman_arco, fn.pacman)
        if fn.distr == "endeavouros":
            fn.shutil.copy(fn.blank_pacman_eos, fn.pacman)
        if fn.distr == "garuda":
            fn.shutil.copy(fn.blank_pacman_garuda, fn.pacman)
        print("We have now a blank pacman /etc/pacman.conf depending on the distro")
        print("ATT will reboot automatically")
        print(
            "Now add the repositories in the order you would like them to appear in the /etc/pacman.conf"
        )
        fn.restart_program()

    def reset_pacman_local(self, widget):
        if fn.path.isfile(fn.pacman + ".bak"):
            fn.shutil.copy(fn.pacman + ".bak", fn.pacman)
            print("We have used /etc/pacman.conf.bak to reset /etc/pacman.conf")
            fn.show_in_app_notification(
                self, "Default Settings Applied - check in a terminal"
            )
        fn.GLib.timeout_add(500, self.update_repos_switches)

    def reset_pacman_online(self, widget):
        if fn.distr == "arch":
            fn.shutil.copy(fn.pacman_arch, fn.pacman)
        if fn.distr == "arcolinux":
            fn.shutil.copy(fn.pacman_arco, fn.pacman)
        if fn.distr == "endeavouros":
            fn.shutil.copy(fn.pacman_eos, fn.pacman)
        if fn.distr == "garuda":
            fn.shutil.copy(fn.pacman_garuda, fn.pacman)
        print("The online version of /etc/pacman.conf is saved")
        fn.show_in_app_notification(
            self, "Default Settings Applied - check in a terminal"
        )
        fn.GLib.timeout_add(500, self.update_repos_switches)

    def edit_pacman_conf_clicked(self, widget):
        fn.show_in_app_notification(self, "Opening pacman.conf in terminal")
        fn.subprocess.Popen(
            ["alacritty", "-e", "sudo", "nano", fn.pacman],
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.PIPE,
        )

    def update_repos_switches(self):
        """Update all repo switches based on current pacman.conf state."""
        self.chaotics_switch.set_active(pmf.check_repo("[chaotic-aur]"))
        self.nemesis_switch.set_active(pmf.check_repo("[nemesis_repo]"))
        self.arepo_button.set_active(pmf.check_repo("[arcolinux]"))
        self.a3prepo_button.set_active(pmf.check_repo("[arcolinux-3rdparty]"))
        self.axlrepo_button.set_active(pmf.check_repo("[archuserrepo]"))
        if hasattr(self, 'refresh_aur_buttons'):
            self.refresh_aur_buttons()
        if hasattr(self, 'parallel_downloads_label'):
            import pacman_gui
            value = pacman_gui.get_parallel_downloads(fn)
            self.parallel_downloads_label.set_markup(f"ParallelDownloads: {value}")
        return False

    # =====================================================
    #               PATREON LINK
    # =====================================================

    def tooltip_callback(self, widget, x, y, keyboard_mode, tooltip, text):
        tooltip.set_text(text)
        return True

    # ====================================================================
    #                       SDDM
    # ====================================================================

    def on_click_sddm_apply(self, widget):
        fn.create_sddm_k_dir()
        if (
            self.sessions_sddm.get_selected_item() is not None
            and self.theme_sddm.get_selected_item() is not None
            and self.autologin_sddm.get_active() is True
            and self.sddm_cursor_themes.get_selected_item() is not None
        ) or (
            self.autologin_sddm.get_active() is False
            and self.theme_sddm.get_selected_item() is not None
            and self.sddm_cursor_themes.get_selected_item() is not None
        ):
            print("=" * 50)
            print("Applying Sddm settings")
            print(" - Auto login    :", self.autologin_sddm.get_active())
            print(" - Session       :", fn.get_combo_text(self.sessions_sddm))
            print(" - Theme         :", fn.get_combo_text(self.theme_sddm))
            print(" - Cursor theme  :", fn.get_combo_text(self.sddm_cursor_themes))
            print(" - Config file   :", fn.sddm_default_d2)

            if fn.path.isfile(fn.sddm_default_d2):
                t1 = fn.threading.Thread(
                    target=sddm.set_sddm_value,
                    args=(
                        self,
                        sddm.get_sddm_lines(fn.sddm_default_d2),
                        fn.sudo_username,
                        fn.get_combo_text(self.sessions_sddm),
                        self.autologin_sddm.get_active(),
                        fn.get_combo_text(self.theme_sddm),
                        fn.get_combo_text(self.sddm_cursor_themes),
                    ),
                )
                t1.daemon = True
                t1.start()

            if fn.check_content("[Autologin]", fn.sddm_default_d1):
                print(" - Autologin file:", fn.sddm_default_d1)
                t2 = fn.threading.Thread(
                    target=sddm.set_user_autologin_value,
                    args=(
                        self,
                        sddm.get_sddm_lines(fn.sddm_default_d1),
                        fn.sudo_username,
                        fn.get_combo_text(self.sessions_sddm),
                        self.autologin_sddm.get_active(),
                    ),
                )
                t2.daemon = True
                t2.start()

            print("Sddm settings saved successfully")
            print("=" * 50)
            fn.show_in_app_notification(self, "Sddm settings saved successfully")

        else:
            print("You need to select desktop, theme and cursor first")
            fn.show_in_app_notification(
                self, "You need to select desktop and/or theme first"
            )

    def on_click_sddm_reset(self, widget):
        if fn.path.isfile(fn.sddm_default_d2):
            if "#" in sddm.check_sddm(sddm.get_sddm_lines(fn.sddm_default_d2), "User="):
                self.autologin_sddm.set_active(False)
            else:
                self.autologin_sddm.set_active(True)
            print("Your sddm.conf backup is now applied")
            fn.show_in_app_notification(self, "Your sddm.conf backup is now applied")
        else:
            print("We did not find a backup file for sddm.conf")
            fn.show_in_app_notification(
                self, "We did not find a backup file for sddm.conf"
            )

    def on_click_sddm_reset_original_att(self, widget):
        fn.create_sddm_k_dir()
        try:
            fn.shutil.copy(fn.sddm_default_d1_kiro, fn.sddm_default_d1)
            fn.shutil.copy(fn.sddm_default_d2_kiro, fn.sddm_default_d2)
        except Exception as error:
            print(error)

        print("The ATT sddm configuration is now applied")
        print(
            "Both files have been changed /etc/sddm.conf and /etc/sddm.conf.d/kde_settings.conf"
        )
        print("Now change the configuration like you want it to be and save")
        fn.show_in_app_notification(
            self, "The ATT sddm.conf and sddm.d.conf is now applied"
        )
        fn.restart_program()

    def on_click_sddm_reset_original(self, widget):
        fn.create_sddm_k_dir()
        try:
            if fn.path.isfile(fn.sddm_default_d1_bak):
                fn.shutil.copy(fn.sddm_default_d1_bak, fn.sddm_default_d1)
            if fn.path.isfile(fn.sddm_default_d2_bak):
                fn.shutil.copy(fn.sddm_default_d2_bak, fn.sddm_default_d2)
        except Exception as error:
            print(error)

        print("Your orignal sddm configuration is now applied")
        print(
            "Both files have been changed /etc/sddm.conf and /etc/sddm.conf.d/kde_settings.conf"
        )
        fn.show_in_app_notification(
            self, "Your original sddm.conf and sddm.d.conf is now applied"
        )
        fn.restart_program()

    def on_click_no_sddm_reset_original(self, widget):
        fn.create_sddm_k_dir()
        if fn.path.isfile(fn.sddm_default_d1_kiro):
            fn.shutil.copyfile(fn.sddm_default_d1_kiro, fn.sddm_default_d1)
            fn.shutil.copyfile(fn.sddm_default_d2_kiro, fn.sddm_default_d2)
        print("The Kiro sddm configuration is now applied")
        fn.show_in_app_notification(
            self, "The Kiro sddm configuration is now applied"
        )

    def on_autologin_sddm_activated(self, widget, gparam):
        if widget.get_active():
            command = "groupadd autologin"
            try:
                fn.subprocess.call(
                    command.split(" "),
                    shell=False,
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
            except Exception as error:
                print(error)
            self.sessions_sddm.set_sensitive(True)
        else:
            self.sessions_sddm.set_sensitive(False)

    def on_click_install_sddm_themes(self, widget):
        fn.install_arco_package(self, "edu-sddm-simplicity-git")
        sddm.pop_theme_box(self, self.theme_sddm)

    def on_browse_sddm_folder(self, widget):
        dialog = Gtk.FileDialog()
        dialog.set_title("Choose a folder with wallpapers")
        current = self.sddm_folder_entry.get_text().strip()
        start = current if fn.path.isdir(current) else fn.home
        dialog.set_initial_folder(Gio.File.new_for_path(start))
        dialog.select_folder(self, None, self.on_sddm_folder_response_cb)

    def on_sddm_folder_response_cb(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                folder_path = folder.get_path()
                self.sddm_folder_entry.set_text(folder_path)
                self._populate_sddm_thumbs(folder_path)
        except Exception:
            pass

    def on_load_sddm_folder(self, _widget):
        folder_path = self.sddm_folder_entry.get_text().strip()
        if fn.path.isdir(folder_path):
            self._populate_sddm_thumbs(folder_path)
        else:
            fn.show_in_app_notification(self, "Folder not found")

    def on_stop_sddm_loading(self, _widget):
        self._sddm_load_gen = getattr(self, "_sddm_load_gen", 0) + 1

    def _populate_sddm_thumbs(self, folder_path):
        self._sddm_load_gen = getattr(self, "_sddm_load_gen", 0) + 1
        current_gen = self._sddm_load_gen

        child = self.sddm_thumb_flow.get_first_child()
        while child is not None:
            next_child = child.get_next_sibling()
            self.sddm_thumb_flow.remove(child)
            child = next_child

        exts = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
        try:
            entries = sorted(fn.os.listdir(folder_path))
        except Exception:
            return

        image_paths = [
            fn.path.join(folder_path, name)
            for name in entries
            if name.lower().endswith(exts)
        ]

        idx = [0]

        def load_next():
            if self._sddm_load_gen != current_gen:
                return False
            if idx[0] >= len(image_paths):
                return False
            path = image_paths[idx[0]]
            idx[0] += 1
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, 160, 100, True)
                texture = Gdk.Texture.new_for_pixbuf(pixbuf)
                pic = Gtk.Picture.new_for_paintable(texture)
                pic.set_can_shrink(False)
                pic.set_size_request(160, 100)

                lbl = Gtk.Label()
                lbl.set_text(fn.path.basename(path))
                lbl.set_max_width_chars(18)
                lbl.set_ellipsize(Pango.EllipsizeMode.MIDDLE)

                box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
                box.set_margin_top(4)
                box.set_margin_bottom(4)
                box.set_margin_start(4)
                box.set_margin_end(4)
                box.append(pic)
                box.append(lbl)

                btn = Gtk.Button()
                btn.set_child(box)
                btn.connect("clicked", self.on_sddm_thumb_clicked, path)
                self.sddm_thumb_flow.append(btn)
            except Exception:
                pass
            return True

        GLib.idle_add(load_next)

    def on_sddm_thumb_clicked(self, widget, path):
        self.login_wallpaper_path = path
        self.sddm_wallpaper_lbl.set_text(path)
        self.sddm_wallpaper_preview.set_filename(path)
        self.sddm_wallpaper_preview.get_parent().set_visible(True)

    def on_set_sddm_wallpaper(self, widget):
        simplicity_images = "/usr/share/sddm/themes/edu-simplicity/images"
        simplicity_conf = "/usr/share/sddm/themes/edu-simplicity/theme.conf"
        dest = simplicity_images + "/background.jpg"
        dest_bak = simplicity_images + "/background.jpg.bak"

        if not self.login_wallpaper_path or not fn.path.isfile(self.login_wallpaper_path):
            fn.show_in_app_notification(self, "First choose a wallpaper image")
            return

        if not fn.path.isdir(simplicity_images):
            fn.show_in_app_notification(
                self, "Simplicity theme not found - install it first"
            )
            return

        try:
            if fn.path.isfile(dest) and not fn.path.isfile(dest_bak):
                fn.shutil.copy(dest, dest_bak)
                print(" - Backup created:", dest_bak)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.login_wallpaper_path)
            pixbuf.savev(dest, "jpeg", [], [])
            with open(simplicity_conf, "w", encoding="utf-8") as f:
                f.write("[General]\nbackground=images/background.jpg\n")
            print("=" * 50)
            print("Applying Sddm wallpaper")
            print(" - Source        :", self.login_wallpaper_path)
            print(" - Destination   :", dest)
            print(" - Config file   :", simplicity_conf)
            print("Sddm wallpaper applied successfully")
            print("=" * 50)
            fn.show_in_app_notification(self, "Simplicity wallpaper applied")
        except Exception as error:
            print(error)
            fn.show_in_app_notification(self, "Failed to apply wallpaper")

    def on_restore_sddm_wallpaper(self, widget):
        simplicity_images = "/usr/share/sddm/themes/edu-simplicity/images"
        simplicity_conf = "/usr/share/sddm/themes/edu-simplicity/theme.conf"
        dest = simplicity_images + "/background.jpg"
        dest_bak = simplicity_images + "/background.jpg.bak"

        if not fn.path.isdir(simplicity_images):
            fn.show_in_app_notification(
                self, "Simplicity theme not found - install it first"
            )
            return

        if not fn.path.isfile(dest_bak):
            fn.show_in_app_notification(self, "No backup found - apply a wallpaper first")
            return

        try:
            fn.shutil.copy(dest_bak, dest)
            with open(simplicity_conf, "w", encoding="utf-8") as f:
                f.write("[General]\nbackground=images/background.jpg\n")
            self.sddm_wallpaper_lbl.set_text("Default wallpaper restored")
            self.sddm_wallpaper_preview.set_filename(dest)
            self.sddm_wallpaper_preview.get_parent().set_visible(True)
            self.login_wallpaper_path = ""
            print("Sddm simplicity wallpaper restored to default")
            fn.show_in_app_notification(self, "Default wallpaper restored")
        except Exception as error:
            print(error)
            fn.show_in_app_notification(self, "Failed to restore wallpaper")

    def on_click_install_bibata_cursor(self, widget):
        fn.install_arco_package(self, "bibata-cursor-theme")
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_click_remove_bibata_cursor(self, widget):
        fn.remove_package(self, "bibata-cursor-theme")
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_click_install_bibatar_cursor(self, widget):
        fn.install_arco_package(self, "bibata-extra-cursor-theme")
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_click_remove_bibatar_cursor(self, widget):
        fn.remove_package(self, "bibata-extra-cursor-theme")
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    # if no sddm - press 1
    def on_click_att_sddm_clicked(self, desktop):
        fn.install_package(self, "sddm")
        fn.install_arco_package(self, "arcolinux-sddm-simplicity-git")
        print("Do not forget to enable sddm")
        fn.show_in_app_notification(self, "Sddm has been installed but not enabled")
        fn.create_sddm_k_dir()
        fn.shutil.copyfile(fn.sddm_default_d1_kiro, fn.sddm_default_d1)
        fn.shutil.copyfile(fn.sddm_default_d2_kiro, fn.sddm_default_d2)
        print("The Kiro sddm configuration is now applied")
        fn.show_in_app_notification(self, "The Kiro sddm configuration is now applied")
        fn.restart_program()

    def on_click_sddm_enable(self, desktop):
        fn.install_package(self, "sddm-git")
        fn.enable_login_manager(self, "sddm")

    def on_launch_adt_clicked(self, desktop):
        # check if package is installed and update label
        if self.adt_installed is True:
            fn.remove_package(self, "arcolinux-desktop-trasher-git")
            if fn.check_package_installed("arcolinux-desktop-trasher-git") is False:
                self.button_adt.set_label("Install the ArcoLinux Desktop Trasher")
                self.adt_installed = False

        else:
            fn.install_package(self, "arcolinux-desktop-trasher-git")
            if fn.check_package_installed("arcolinux-desktop-trasher-git") is True:
                self.button_adt.set_label("Remove the ArcoLinux Desktop Trasher")
                self.adt_installed = True

    def on_click_apply_parallel_downloads(self, widget):
        maintenance.set_parallel_downloads(self, widget)

    # ====================================================================
    #                       SERVICES - NSSWITCH
    # ====================================================================

    def update_network_status(self):
        if hasattr(self, 'network_status_label'):
            status1 = fn.check_service("smb")
            status1_text = "<b>active</b>" if status1 else "inactive"
            status2 = fn.check_service("nmb")
            status2_text = "<b>active</b>" if status2 else "inactive"
            status3 = fn.check_service("avahi-daemon")
            status3_text = "<b>active</b>" if status3 else "inactive"
            self.network_status_label.set_markup(
                "Samba: " + status1_text + "   Nmb: " + status2_text + "   Avahi: " + status3_text
            )

    def on_install_discovery_clicked(self, widget):
        fn.install_discovery(self)
        self.update_network_status()
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Network discovery is installed - a good nsswitch_config is needed",
        )
        print("[INFO] Network discovery is installed")

    def on_remove_discovery_clicked(self, widget):
        fn.remove_discovery(self)
        self.update_network_status()
        GLib.idle_add(fn.show_in_app_notification, self, "Network discovery is removed")
        print("[INFO] Network discovery is removed")

    def on_click_reset_nsswitch(self, widget):
        if fn.path.isfile(fn.nsswitch_config + ".bak"):
            fn.shutil.copy(fn.nsswitch_config + ".bak", fn.nsswitch_config)

        print("/etc/nsswitch.config reset")
        fn.show_in_app_notification(self, "Nsswitch config reset")

    def on_click_edit_nsswitch(self, widget):
        try:
            fn.subprocess.Popen(["nano", fn.nsswitch_config])
            print("Opened /etc/nsswitch.conf in nano")
            fn.show_in_app_notification(self, "nsswitch.conf opened in terminal")
        except Exception as e:
            print(f"Error opening nsswitch.conf: {e}")
            fn.show_in_app_notification(self, "Error opening nsswitch.conf for editing")

    def on_click_apply_nsswitch(self, widget):
        services.choose_nsswitch(self)

    # ====================================================================
    #                       SERVICES - SAMBA
    # ====================================================================

    def on_click_create_samba_user(self, widget):
        services.create_samba_user(self)

    def on_click_restart_smb(self, widget):
        services.restart_smb(self)
        self.update_network_status()

    def on_click_save_samba_share(self, widget):
        fn.save_samba_config(self)

    def on_click_install_arco_thunar_plugin(self, widget):
        fn.install_arco_thunar_plugin(self, widget)

    def on_click_apply_samba(self, widget):
        services.choose_smb_conf(self)
        print("Applying selected samba configuration")
        fn.show_in_app_notification(self, "Applying selected samba configuration")

    def on_click_reset_samba(self, widget):
        if fn.path.isfile(fn.samba_config + ".bak"):
            fn.shutil.copy(fn.samba_config + ".bak", fn.samba_config)
            print("We have reset your /etc/samba/smb.conf")
            fn.show_in_app_notification(self, "Original smb.conf is applied")
        if not fn.path.isfile(fn.samba_config + ".bak"):
            print("We have no original /etc/samba/smb.conf.bak file - we can not reset")
            print("Instead choose one from the dropdown")
            fn.show_in_app_notification(self, "No backup configuration present")

    def on_click_edit_samba_nano(self, widget):
        fn.subprocess.Popen(
            ["alacritty", "-e", "nano", fn.samba_config],
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.PIPE,
        )
        print(f"Opening {fn.samba_config} in nano")
        fn.show_in_app_notification(self, "Opening samba.conf in terminal with nano")

    def on_click_install_samba(self, widget):
        print("\n" + "=" * 70)
        print("INSTALLING SAMBA")
        print("=" * 70)
        fn.install_samba(self)
        print("✓ Samba package installed")
        print("\nApplying 'Easy' configuration...")
        services.choose_smb_conf(self)
        print("✓ Easy configuration applied with automatic 'Shared' folder setup")
        print("=" * 70 + "\n")
        self.update_network_status()
        fn.show_in_app_notification(
            self, "✓ Samba installed with Easy configuration. Restart smb to apply."
        )

    def on_click_uninstall_samba(self, widget):
        print("\n" + "=" * 70)
        print("UNINSTALLING SAMBA")
        print("=" * 70)
        fn.uninstall_samba(self)
        print("✓ Samba package uninstalled")
        print("=" * 70 + "\n")
        self.update_network_status()
        fn.show_in_app_notification(self, "✓ Samba has been uninstalled")

    # ====================================================================
    #                       SERVICES - AUDIO
    # ====================================================================

    def on_click_switch_to_pulseaudio(self, widget):
        print("Installing pulseaudio")

        if fn.check_package_installed("pipewire-pulse"):
            fn.remove_package_dd(self, "pipewire-pulse")
            fn.remove_package_dd(self, "wireplumber")

        try:
            fn.install_package(self, "pulseaudio")  # conflicts with pipewire-pulse
            fn.install_package(
                self, "pulseaudio-bluetooth"
            )  # conflicts with pipewire-pulse
            fn.install_package(self, "pulseaudio-alsa")

            fn.install_package(self, "pavucontrol")

            fn.install_package(self, "alsa-utils")
            fn.install_package(self, "alsa-plugins")
            fn.install_package(self, "alsa-lib")
            fn.install_package(self, "alsa-firmware")
            fn.install_package(self, "gstreamer")
            fn.install_package(self, "gst-plugins-good")
            fn.install_package(self, "gst-plugins-bad")
            fn.install_package(self, "gst-plugins-base")
            fn.install_package(self, "gst-plugins-ugly")

            # add line for autoconnect
            services.add_autoconnect_pulseaudio(self)

        except Exception as error:
            print(error)

    def on_click_switch_to_pipewire(self, widget):
        print("Installing pipewire")
        blueberry_installed = False

        try:
            if fn.check_package_installed("pulseaudio"):
                fn.remove_package_dd(self, "pulseaudio")
                fn.remove_package_dd(self, "pulseaudio-bluetooth")

            fn.install_package(self, "pipewire")
            fn.install_package(
                self, "pipewire-pulse"
            )  # contains wireplumber - conflicts with pulseaudio and pulseaudio-bluetooth
            fn.install_package(self, "pipewire-alsa")
            # fn.install_package(self, "pipewire-jack")
            # fn.install_package(self, "pipewire-zeroconf")

            fn.install_package(self, "pavucontrol")

            fn.install_package(self, "alsa-utils")
            fn.install_package(self, "alsa-plugins")
            fn.install_package(self, "alsa-lib")
            fn.install_package(self, "alsa-firmware")
            fn.install_package(self, "gstreamer")
            fn.install_package(self, "gst-plugins-good")
            fn.install_package(self, "gst-plugins-bad")
            fn.install_package(self, "gst-plugins-base")
            fn.install_package(self, "gst-plugins-ugly")

            if blueberry_installed:
                fn.install_package(self, "blueberry")

            if fn.check_package_installed("pipewire-media-session"):
                fn.remove_package_dd(self, "pipewire-media-session")
                fn.install_package(self, "pipewire-pulse")
                fn.install_package(self, "wireplumber")

        except Exception as error:
            print(error)

    # ====================================================================
    #                       SERVICES - BLUETOOTH
    # ====================================================================
    # applications
    def on_click_install_bluetooth(self, widget):
        print("Installing bluetooth")
        fn.install_package(self, "bluez")
        fn.install_package(self, "bluez-utils")
        if fn.check_package_installed("bluez"):
            self.enable_bt.set_sensitive(True)
            self.disable_bt.set_sensitive(True)
            self.restart_bt.set_sensitive(True)

    def on_click_remove_bluetooth(self, widget):
        print("Removing bluez")
        fn.remove_package_dd(self, "bluez")
        fn.remove_package_dd(self, "bluez-utils")
        if not fn.check_package_installed("bluez"):
            self.enable_bt.set_sensitive(False)
            self.disable_bt.set_sensitive(False)
            self.restart_bt.set_sensitive(False)

    def on_click_install_blueberry(self, widget):
        print("Installing blueberry")
        fn.install_package(self, "blueberry")

    def on_click_remove_blueberry(self, widget):
        print("Removing blueberry")
        fn.remove_package(self, "blueberry")

    def on_click_install_blueman(self, widget):
        print("Installing blueman")
        fn.install_package(self, "blueman")

    def on_click_remove_blueman(self, widget):
        print("Removing blueman")
        fn.remove_package(self, "blueman")

    def on_click_install_bluedevil(self, widget):
        print("Installing bluedevil")
        fn.install_package(self, "bluedevil")

    def on_click_remove_bluedevil(self, widget):
        print("Removing bluedevil")
        fn.remove_package_s(self, "bluedevil")

    # service
    def on_click_enable_bluetooth(self, widget):
        print("Enabling bluetooth service/socket")
        fn.enable_service("bluetooth")
        fn.show_in_app_notification(self, "Bluetooth has been enabled")

    def on_click_disable_bluetooth(self, widget):
        print("Enabling bluetooth service/socket")
        fn.disable_service("bluetooth")
        fn.show_in_app_notification(self, "Bluetooth has been disabled")

    def on_click_restart_bluetooth(self, widget):
        print("Restart bluetooth")
        fn.restart_service("bluetooth")
        fn.show_in_app_notification(self, "Bluetooth has been restarted")

    # ====================================================================
    #                       SERVICES - CUPS
    # ====================================================================

    def on_click_install_cups(self, widget):
        print("Installing cups")
        fn.install_package(self, "cups")

    def on_click_remove_cups(self, widget):
        print("Removing cups")
        fn.remove_package(self, "cups")

    def on_click_install_cups_pdf(self, widget):
        print("Installing cups-pdf")
        fn.install_package(self, "cups-pdf")

    def on_click_remove_cups_pdf(self, widget):
        print("Removing cups-pdf")
        fn.remove_package(self, "cups-pdf")

    def on_click_enable_cups(self, widget):
        print("Enabling cups service/socket")
        fn.enable_service("cups")

    def on_click_disable_cups(self, widget):
        print("Enabling cups service/socket")
        fn.disable_service("cups")

    def on_click_restart_cups(self, widget):
        print("Restart cups")
        fn.restart_service("cups")

    def on_click_install_printer_drivers(self, widget):
        print("Following printer drivers have been installed")
        fn.install_package(self, "foomatic-db-engine")
        fn.install_package(self, "foomatic-db")
        fn.install_package(self, "foomatic-db-ppds")
        fn.install_package(self, "foomatic-db-nonfree")
        fn.install_package(self, "foomatic-db-nonfree-ppds")
        fn.install_package(self, "gutenprint")
        fn.install_package(self, "foomatic-db-gutenprint-ppds")
        fn.install_package(self, "ghostscript")
        fn.install_package(self, "gsfonts")

    def on_click_remove_printer_drivers(self, widget):
        print("Following printer drivers have been removed")
        fn.remove_package(self, "foomatic-db-engine")
        fn.remove_package(self, "foomatic-db")
        fn.remove_package(self, "foomatic-db-ppds")
        fn.remove_package(self, "foomatic-db-nonfree")
        fn.remove_package(self, "foomatic-db-nonfree-ppds")
        fn.remove_package(self, "gutenprint")
        fn.remove_package(self, "foomatic-db-gutenprint-ppds")
        fn.remove_package(self, "ghostscript")
        fn.remove_package(self, "gsfonts")

    def on_click_install_hplip(self, widget):
        print("Installing Hplip")
        fn.install_package(self, "hplip")

    def on_click_remove_hplip(self, widget):
        print("Removing Hplip")
        fn.remove_package(self, "hplip")

    def on_click_install_system_config_printer(self, widget):
        print("Installing system_config_printer")
        fn.install_package(self, "system-config-printer")

    def on_click_remove_system_config_printer(self, widget):
        print("Removing system_config_printer")
        fn.remove_package(self, "system_config_printer")

    # ====================================================================
    #                       SHELLS EXTRA
    # ====================================================================

    def on_extra_shell_applications_clicked(self, widget):
        if self.expac.get_active():
            fn.install_package(self, "expac")
        if self.ripgrep.get_active():
            fn.install_package(self, "ripgrep")
        if self.yay.get_active():
            fn.install_arco_package(self, "yay-git")
        if self.paru.get_active():
            fn.install_arco_package(self, "paru-git")
        if self.bat.get_active():
            fn.install_package(self, "bat")
        if self.downgrade.get_active():
            fn.install_arco_package(self, "downgrade")
        if self.hw_probe.get_active():
            fn.install_arco_package(self, "hw-probe")
        if self.rate_mirrors.get_active():
            fn.install_arco_package(self, "rate-mirrors")
        if self.most.get_active():
            fn.install_package(self, "most")
        print("Software has been installed depending on the repos")
        fn.show_in_app_notification(
            self, "Software has been installed depending on the repos"
        )
        if fn.check_package_installed("expac") is False:
            self.expac.set_active(False)
        if fn.check_package_installed("ripgrep") is False:
            self.ripgrep.set_active(False)
        if fn.check_package_installed("yay-git") is False:
            self.yay.set_active(False)
        if fn.check_package_installed("paru-git") is False:
            self.paru.set_active(False)
        if fn.check_package_installed("bat") is False:
            self.bat.set_active(False)
        if fn.check_package_installed("downgrade") is False:
            self.downgrade.set_active(False)
        if fn.check_package_installed("hw-probe") is False:
            self.hw_probe.set_active(False)
        if fn.check_package_installed("rate-mirrors") is False:
            self.rate_mirrors.set_active(False)
        if fn.check_package_installed("most") is False:
            self.most.set_active(False)

    def on_select_all_toggle(self, widget, active):
        if self.select_all.get_active():
            self.expac.set_active(True)
            self.ripgrep.set_active(True)
            self.yay.set_active(True)
            self.paru.set_active(True)
            self.bat.set_active(True)
            self.downgrade.set_active(True)
            self.hw_probe.set_active(True)
            self.rate_mirrors.set_active(True)
            self.most.set_active(True)

    # =====================================================
    #               THEMER FUNCTIONS
    # =====================================================

    def on_polybar_toggle(self, widget, active):
        if widget.get_active():
            themer.toggle_polybar(self, themer.get_list(fn.i3wm_config), True)
        else:
            themer.toggle_polybar(self, themer.get_list(fn.i3wm_config), False)
            if fn.check_if_process_is_running("polybar"):
                try:
                    fn.subprocess.run(
                        ["killall", "-q", "polybar"], check=True, shell=False
                    )
                except Exception as error:
                    print(error)

    def awesome_apply_clicked(self, widget):
        if not fn.path.isfile(fn.awesome_config + ".bak"):
            fn.shutil.copy(fn.awesome_config, fn.awesome_config + ".bak")

        tree_iter = self.awesome_combo.get_active_iter()
        if tree_iter is not None:
            model = self.awesome_combo.get_model()
            row_id, name = model[tree_iter][:2]
        nid = str(row_id + 1)
        themer.set_awesome_theme(themer.get_list(fn.awesome_config), nid)
        print("Theme applied successfully")
        fn.show_in_app_notification(self, "Theme set successfully")

    def awesome_reset_clicked(self, widget):
        if fn.path.isfile(fn.awesome_config + ".bak"):
            fn.shutil.copy(fn.awesome_config + ".bak", fn.awesome_config)
            fn.show_in_app_notification(self, "Config reset successfully")

            awesome_list = themer.get_list(fn.awesome_config)
            awesome_lines = themer.get_awesome_themes(awesome_list)

            self.store.clear()
            # TODO: enumerate
            for x in range(len(awesome_lines)):
                self.store.append([x, awesome_lines[x]])
            val = int(
                themer.get_value(awesome_list, "local chosen_theme =")
                .replace("themes[", "")
                .replace("]", "")
            )
            self.awesome_combo.set_active(val - 1)

    def i3wm_apply_clicked(self, widget):
        if fn.path.isfile(fn.i3wm_config):
            fn.shutil.copy(fn.i3wm_config, fn.i3wm_config + ".bak")

        themer.set_i3_themes(
            themer.get_list(fn.i3wm_config), fn.get_combo_text(self.i3_combo)
        )
        if not themer.check_polybar(themer.get_list(fn.i3wm_config)):
            themer.set_i3_themes_bar(
                themer.get_list(fn.i3wm_config), fn.get_combo_text(self.i3_combo)
            )
        print("Theme applied successfully")
        fn.show_in_app_notification(self, "Theme applied successfully")

    def i3wm_reset_clicked(self, widget):
        if fn.path.isfile(fn.i3wm_config + ".bak"):
            fn.shutil.copy(fn.i3wm_config + ".bak", fn.i3wm_config)
            fn.show_in_app_notification(self, "Config reset successfully")

            i3_list = themer.get_list(fn.i3wm_config)

            themer.get_i3_themes(self.i3_combo, i3_list)

    def qtile_apply_clicked(self, widget):
        if fn.path.isfile(fn.qtile_config):
            fn.shutil.copy(fn.qtile_config, fn.qtile_config + ".bak")

        themer.set_qtile_themes(
            themer.get_list(fn.qtile_config), fn.get_combo_text(self.qtile_combo)
        )
        print("Theme applied successfully")
        fn.show_in_app_notification(self, "Theme applied successfully")

    def qtile_reset_clicked(self, widget):
        if fn.path.isfile(fn.qtile_config + ".bak"):
            fn.shutil.copy(fn.qtile_config + ".bak", fn.qtile_config)
            fn.show_in_app_notification(self, "Config reset successfully")

            qtile_list = themer.get_list(fn.qtile_config)

            themer.get_qtile_themes(self.qtile_combo, qtile_list)

    def leftwm_apply_clicked(self, widget):
        themer.set_leftwm_themes(fn.get_combo_text(self.leftwm_combo))
        print("Theme " + fn.get_combo_text(self.leftwm_combo) + " applied successfully")
        fn.show_in_app_notification(
            self,
            "Theme " + fn.get_combo_text(self.leftwm_combo) + " applied successfully",
        )
        self.status_leftwm.set_markup("<b>Theme is installed and applied</b>")

    def leftwm_reset_clicked(self, widget):
        themer.reset_leftwm_themes(fn.get_combo_text(self.leftwm_combo))
        print("Reverting back to candy as fall-back")
        print("Theme " + fn.get_combo_text(self.leftwm_combo) + " reset successfully")
        fn.show_in_app_notification(
            self, "Theme " + fn.get_combo_text(self.leftwm_combo) + " reset successfully"
        )
        self.status_leftwm.set_markup("<b>Theme is installed and applied</b>")

    def leftwm_remove_clicked(self, widget):
        themer.remove_leftwm_themes(fn.get_combo_text(self.leftwm_combo))
        print("Reverting back to candy as fall-back")
        print("Theme " + fn.get_combo_text(self.leftwm_combo) + " removed successfully")
        fn.show_in_app_notification(
            self,
            "Theme " + fn.get_combo_text(self.leftwm_combo) + " removed successfully",
        )

    def on_leftwm_combo_changed(self, widget, pspec=None):
        link_theme = fn.path.basename(readlink(fn.leftwm_config_theme_current))
        theme = fn.get_combo_text(self.leftwm_combo)
        if fn.path_check(fn.leftwm_config_theme + theme):
            self.status_leftwm.set_markup("<b>Theme is installed</b>")
        else:
            self.status_leftwm.set_markup("<b>Theme is NOT installed</b>")

        if fn.path_check(fn.leftwm_config_theme + theme) and link_theme == theme:
            self.status_leftwm.set_markup("<b>Theme is installed and applied</b>")

    # ====================================================================
    #                       TERMINALS
    # ====================================================================

    def on_clicked_install_alacritty(self, widget):
        fn.install_package(self, "alacritty")

    def on_clicked_install_alacritty_themes(self, widget):
        if fn.check_edu_repos_active() is True:
            fn.install_package(self, "alacritty")
            fn.install_package(self, "ttf-hack")
            fn.install_arco_package(self, "alacritty-themes")
            fn.install_arco_package(self, "base16-alacritty-git")
            print("Alacritty themes installed")
            fn.show_in_app_notification(self, "Alacritty themes installed")

            # if there is no file copy/paste from /etc/skel else alacritty-themes crash
            if not fn.path.isfile(fn.alacritty_config):
                if not fn.path.isdir(fn.alacritty_config_dir):
                    try:
                        fn.mkdir(fn.alacritty_config_dir)
                        fn.permissions(fn.alacritty_config_dir)
                    except Exception as error:
                        print(error)

                fn.shutil.copy(fn.alacritty_arco, fn.alacritty_config)
                fn.permissions(fn.home + "/.config/alacritty")
                print("Alacritty config saved")
        else:
            print("First activate the nemesis repo")
            fn.show_in_app_notification(self, "First activate the nemesis repo")

    def on_clicked_remove_alacritty_themes(self, widget):
        fn.remove_package(self, "alacritty")
        fn.remove_package(self, "ttf-hack")
        fn.remove_package(self, "alacritty-themes")
        fn.remove_package(self, "base16-alacritty-git")
        print("Alacritty themes removed")
        fn.show_in_app_notification(self, "Alacritty themes removed")

    def on_clicked_install_xfce4_terminal(self, widget):
        fn.install_package(self, "xfce4-terminal")

    def on_clicked_remove_xfce4_terminal(self, widget):
        fn.remove_package(self, "xfce4-terminal")

    def on_clicked_install_xfce4_themes(self, widget):
        if fn.check_edu_repos_active() is True:
            fn.install_arco_package(self, "xfce4-terminal-base16-colors-git")
            fn.install_arco_package(self, "tempus-themes-xfce4-terminal-git")
            fn.install_arco_package(self, "prot16-xfce4-terminal")
            print("Xfce4 themes installed")
            fn.show_in_app_notification(self, "Xfce4 themes installed")
        else:
            print("First activate the nemesis repo")
            fn.show_in_app_notification(self, "First activate the nemesis repo")

    def on_clicked_remove_xfce4_themes(self, widget):
        fn.remove_package(self, "xfce4-terminal-base16-colors-git")
        fn.remove_package(self, "tempus-themes-xfce4-terminal-git")
        fn.remove_package(self, "prot16-xfce4-terminal")
        print("Xfce4 themes removed")
        fn.show_in_app_notification(self, "Xfce4 themes removed")

    def on_clicked_reset_xfce4_terminal(self, widget):
        if fn.path.isfile(fn.xfce4_terminal_config + ".bak"):
            fn.shutil.copy(fn.xfce4_terminal_config + ".bak", fn.xfce4_terminal_config)
            fn.permissions(fn.home + "/.config/xfce4/terminal")
            print("xfce4-terminal reset")
            fn.show_in_app_notification(self, "Xfce4-terminal reset")

    def on_clicked_reset_alacritty(self, widget):
        if fn.path.isfile(fn.alacritty_config + ".bak"):
            fn.shutil.copy(fn.alacritty_config + ".bak", fn.alacritty_config)
            fn.permissions(fn.home + "/.config/alacritty")
            print("Alacritty reset")
            fn.show_in_app_notification(self, "Alacritty reset")

    def on_clicked_set_arcolinux_alacritty_theme_config(self, widget):
        if fn.path.isfile(fn.alacritty_config):
            fn.shutil.copy(fn.alacritty_arco, fn.alacritty_config)
            fn.permissions(fn.home + "/.config/alacritty")
            print("Applied the ATT Alacritty theme/config")
            fn.show_in_app_notification(self, "Applied the ATT Alacritty theme/config")

    # ====================================================================
    #                      TERMITE
    # ====================================================================

    def on_clicked_install_termite(self, widget):
        fn.install_arco_package(self, "termite")
        terminals.get_themes(self.term_themes)

    def on_clicked_remove_termite(self, widget):
        fn.remove_package(self, "termite")
        terminals.get_themes(self.term_themes)

    def on_clicked_install_termite_themes(self, widget):
        if fn.check_edu_repos_active() is True:
            fn.install_arco_package(self, "termite")
            fn.install_arco_package(self, "arcolinux-termite-themes-git")
            fn.copy_func("/etc/skel/.config/termite", fn.home + "/.config/", True)
            fn.permissions(fn.home + "/.config/termite")
            terminals.get_themes(self.term_themes)
            print("Termite  themes installed")
            fn.show_in_app_notification(self, "Termite themes installed")
        else:
            print("First activate the nemesis repo")
            fn.show_in_app_notification(self, "First activate the nemesis repo")

    def on_clicked_remove_termite_themes(self, widget):
        fn.remove_package(self, "arcolinux-termite-themes-git")
        terminals.get_themes(self.term_themes)
        print("Termite  themes removed")
        GLib.idle_add(fn.show_in_app_notification, self, "Termite themes removed")

    def on_term_apply(self, widget):
        if self.term_themes.get_selected_item() is not None:
            widget.set_sensitive(False)
            terminals.set_config(self, fn.get_combo_text(self.term_themes))
            widget.set_sensitive(True)

    def on_term_reset(self, widget):
        if fn.path.isfile(fn.termite_config + ".bak"):
            fn.shutil.copy(fn.termite_config + ".bak", fn.termite_config)
            fn.show_in_app_notification(self, "Default Settings Applied")
            if fn.path.isfile(fn.config):
                settings.write_settings("TERMITE", "theme", "")
                terminals.get_themes(self.term_themes)

    # ====================================================================
    #                       USER
    # ====================================================================

    def on_click_user_apply(self, widget):
        user.create_user(self)
        user.pop_cbt_users(self, self.cbt_users)

    def on_click_delete_user(self, widget):
        user.on_click_delete_user(self)
        user.pop_cbt_users(self, self.cbt_users)

    def on_click_delete_all_user(self, widget):
        user.on_click_delete_all_user(self)
        user.pop_cbt_users(self, self.cbt_users)

    # ====================================================================
    #                      ZSH THEMES
    # ====================================================================

    def on_clicked_install_only_zsh(self, widget):
        fn.install_package(self, "zsh")
        fn.restart_program()

    def on_install_zsh_completions_clicked(self, widget):
        fn.install_package(self, "zsh-completions")

    def on_remove_zsh_completions_clicked(self, widget):
        fn.remove_package(self, "zsh-completions")

    def on_install_zsh_syntax_highlighting_clicked(self, widget):
        fn.install_package(self, "zsh-syntax-highlighting")

    def on_remove_zsh_syntax_highlighting_clicked(self, widget):
        fn.remove_package(self, "zsh-syntax-highlighting")

    def on_arcolinux_zshrc_clicked(self, widget):
        try:
            if fn.path.isfile(fn.zshrc_arco):
                fn.shutil.copy(fn.zshrc_arco, fn.zsh_config)
                fn.permissions(fn.home + "/.zshrc")
            fn.source_shell(self)
        except Exception as error:
            print(error)

        print("ATT ~/.zshrc is applied")
        GLib.idle_add(fn.show_in_app_notification, self, "ATT ~/.zshrc is applied")

    def on_zshrc_reset_clicked(self, widget):
        try:
            if fn.path.isfile(fn.zsh_config + ".bak"):
                fn.shutil.copy(fn.zsh_config + ".bak", fn.zsh_config)
                fn.permissions(fn.home + "/.zshrc")
        except Exception as error:
            print(error)

        print("Your personal ~/.zshrc is applied again - logout")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Your personal ~/.zshrc is applied again - logout",
        )

    def on_zsh_apply_theme(self, widget):
        # create a .zshrc if it doesn't exist'
        if not fn.path.isfile(fn.zsh_config):
            fn.shutil.copy(fn.zshrc_arco, fn.zsh_config)
            fn.permissions(fn.home + "/.zshrc")

        if self.zsh_themes.get_selected_item() is not None:
            # widget.set_sensitive(False)
            zsh_theme.set_config(self, fn.get_combo_text(self.zsh_themes))
            widget.set_sensitive(True)
            print("Applying zsh theme")

    def on_zsh_reset(self, widget):
        if fn.path.isfile(fn.zsh_config + ".bak"):
            fn.shutil.copy(fn.zsh_config + ".bak", fn.zsh_config)
            fn.permissions(fn.home + "/.zshrc")
            fn.permissions(fn.home + "/.zshrc.bak")
            fn.show_in_app_notification(self, "Default settings applied")
            print("Backup has been applied")
        else:
            fn.shutil.copy(
                "/usr/share/archlinux-tweak-tool/data/arco/.zshrc", fn.home + "/.zshrc"
            )
            fn.permissions(fn.home + "/.zshrc")
            fn.show_in_app_notification(self, "Valid ~/.zshrc applied")
            print("Valid ~/.zshrc applied")

    def tozsh_apply(self, widget):
        fn.change_shell(self, "zsh")

    def install_oh_my_zsh(self, widget):
        fn.install_arco_package(self, "oh-my-zsh-git")
        self.termset.set_sensitive(True)
        self.zsh_themes.set_sensitive(True)
        zsh_theme.get_themes(self.zsh_themes)

    def update_image(
        self, widget, image, theme_type, att_base, image_width, image_height
    ):
        from gi.repository import Gdk

        sample_path = ""
        preview_path = ""
        random_option = False
        if theme_type == "zsh":
            sample_path = att_base + "/images/zsh-sample.jpg"
            preview_path = (
                att_base + "/images/zsh_previews/" + fn.get_combo_text(widget) + ".jpg"
            )
            if fn.get_combo_text(widget) == "random":
                random_option = True
        elif theme_type == "qtile":
            sample_path = att_base + "/images/qtile-sample.jpg"
            preview_path = (
                att_base + "/themer_data/qtile/" + fn.get_combo_text(widget) + ".jpg"
            )
        elif theme_type == "leftwm":
            sample_path = att_base + "/images/leftwm-sample.jpg"
            preview_path = (
                att_base + "/themer_data/leftwm/" + fn.get_combo_text(widget) + ".jpg"
            )
        elif theme_type == "i3":
            sample_path = att_base + "/images/i3-sample.jpg"
            preview_path = (
                att_base + "/themer_data/i3/" + fn.get_combo_text(widget) + ".jpg"
            )
        elif theme_type == "awesome":
            # Awesome section doesn't use a DropDown, but a ComboBox - which has different properties.
            tree_iter = self.awesome_combo.get_active_iter()
            if tree_iter is not None:
                model = self.awesome_combo.get_model()
                row_id, name = model[tree_iter][:2]

            sample_path = att_base + "/images/awesome-sample.jpg"
            preview_path = att_base + "/themer_data/awesomewm/" + name + ".jpg"
        elif theme_type == "neofetch":
            sample_path = att_base + fn.get_combo_text(widget)
            preview_path = att_base + fn.get_combo_text(widget)
        else:
            # If we are doing our job correctly, this should never be shown to users. If it does, we have done something wrong as devs.
            print(
                "Function update_image passed an incorrect value for theme_type. Value passed was: "
                + theme_type
            )
            print(
                "Remember that the order for using this function is: self, widget, image, theme_type, att_base_path, image_width, image_height."
            )
        # source_pixbuf = image.get_pixbuf()
        if fn.path.isfile(preview_path) and not random_option:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                preview_path, image_width, image_height
            )
        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                sample_path, image_width, image_height
            )
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        image.set_paintable(texture)

    def remove_oh_my_zsh(self, widget):
        fn.remove_package(self, "oh-my-zsh-git")
        zsh_theme.get_themes(self.zsh_themes)
        self.termset.set_sensitive(False)
        self.zsh_themes.set_sensitive(False)

    # ====================================================================
    #                            PACKAGES
    # ====================================================================#

    def on_click_export_packages(
        self,
        widget,
        packages_obj,
        rb_export_all,
        rb_export_explicit,
        gui_parts,
    ):
        try:
            if not os.path.exists(packages_obj.export_dir):
                fn.makedirs(packages_obj.export_dir)
                fn.permissions(packages_obj.export_dir)
            if fn.check_pacman_lockfile() is True:
                fn.logger.warning(
                    "Export aborted, failed to lock database, pacman lockfile exists at %s"
                )

                fn.messagebox(
                    self,
                    "Export of packages failed",
                    "Failed to lock database, pacman lockfile exists at %s\nIs another pacman process running ?"
                    % fn.pacman_lockfile,
                )

            else:
                vbox_stack = gui_parts[0]
                grid_package_status = gui_parts[1]
                grid_package_count = gui_parts[2]
                vbox_pacmanlog = gui_parts[3]
                textbuffer = gui_parts[4]
                textview = gui_parts[5]
                label_package_status = gui_parts[6]
                label_package_count = gui_parts[7]

                if vbox_pacmanlog.is_visible() is False:
                    vbox_stack.append(grid_package_status)
                    vbox_stack.append(grid_package_count)
                    vbox_stack.append(vbox_pacmanlog)

                    grid_package_status.set_visible(False)
                    grid_package_count.set_visible(False)
                else:
                    grid_package_status.set_visible(False)
                    grid_package_count.set_visible(False)

                rb_export_selected = None
                if rb_export_all.get_active():
                    rb_export_selected = "export_all"
                if rb_export_explicit.get_active():
                    rb_export_selected = "export_explicit"
                export_ok = packages_obj.export_packages(rb_export_selected, gui_parts)
                if export_ok is False:
                    fn.messagebox(
                        self,
                        "Export failed",
                        "Failed to export list of packages",
                    )
                else:
                    fn.messagebox(
                        self,
                        "Export completed",
                        "Exported to file %s" % packages_obj.default_export_path,
                    )

        except Exception as e:
            fn.logger.error("Exception in on_click_export_packages(): %s" % e)

    def on_message_dialog_yes_response(self, widget):
        fn.logger.info("Ok to proceed to install")
        widget.destroy()

    def on_message_dialog_no_response(self, widget):
        fn.logger.info("Packages install skipped by user")
        widget.destroy()

    def on_click_install_packages(self, widget, packages_obj, gui_parts):
        import gi
        gi.require_version("Gio", "2.0")
        from gi.repository import Gio

        packages_dir = packages_obj.export_dir

        # Create file chooser dialog
        file_chooser = Gtk.FileChooserDialog(
            title="Select Packages File to Install",
            parent=self,
            action=Gtk.FileChooserAction.OPEN,
            modal=True,
        )
        file_chooser.add_button("_Open", -5)
        file_chooser.add_button("_Cancel", -6)

        # Set initial folder using Gio.File
        initial_folder = Gio.File.new_for_path(packages_dir)
        file_chooser.set_current_folder(initial_folder)

        # Add filter for .txt files
        file_filter = Gtk.FileFilter()
        file_filter.set_name("Package Files (*.txt)")
        file_filter.add_pattern("*.txt")
        file_chooser.add_filter(file_filter)

        # Handle response
        handled = [False]  # Use list to allow modification in nested function

        def on_response(dialog, response_id, user_data=None):
            if handled[0]:
                return
            handled[0] = True

            print(f"Response ID: {response_id}")
            if response_id == -5 or response_id == -4:
                selected_file = dialog.get_file()
                if selected_file:
                    file_path = selected_file.get_path()
                    print(f"Selected packages file: {file_path}")
                    fn.show_in_app_notification(
                        self, f"Opening terminal to install from: {fn.path.basename(file_path)}"
                    )
                    # Open terminal with installation command
                    fn.subprocess.Popen(
                        ["alacritty", "-e", "bash", "-c", f"pacman -S --needed $(cat {file_path} | grep -v '^#' | tr '\\n' ' '); read -p 'Press Enter to exit...'"],
                        stdout=fn.subprocess.PIPE,
                        stderr=fn.subprocess.PIPE,
                    )
            else:
                print("Package selection cancelled")
                fn.show_in_app_notification(self, "Package selection cancelled")
            dialog.close()

        file_chooser.connect("response", on_response)
        file_chooser.present()

    # ====================================================================
    #                            BOTTOM BUTTONS
    # ====================================================================

    def on_refresh_att_clicked(self, desktop):
        fn.restart_program()

    def on_close(self, window):
        try:
            fn.unlink("/tmp/att.lock")
        except FileNotFoundError:
            pass
        self.get_application().quit()
        return False


    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    #                END OF MAIN FUNCTIONS
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================
    # ================================================================================


# ====================================================================
#                       MAIN
# ====================================================================


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
    signal.signal(signal.SIGINT, signal_handler)
    app = ATTApplication()
    _app_ref = app
    sys.exit(app.run(sys.argv))
