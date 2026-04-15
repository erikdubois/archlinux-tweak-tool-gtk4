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
lxdm = None
login = None
lightdm = None
maintenance = None
gui = None
att = None
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
        print("Run fix-lightdm-conf")
        print("Run fix-lxdm-conf")
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

        _gtk_theme = os.environ.get("GTK_THEME")
        if not _gtk_theme:
            try:
                with open("/etc/environment", "r", encoding="utf-8") as _f:
                    for _line in _f:
                        _line = _line.strip()
                        if _line.startswith("GTK_THEME="):
                            _gtk_theme = _line.split("=", 1)[1].strip()
                            break
            except Exception:
                pass
        print("[INFO] : Theme = " + (_gtk_theme if _gtk_theme else "not set"))
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

        self.grub_image_path = ""
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
        global pacman_functions, fastfetch, lxdm, login, lightdm, maintenance, gui, att
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
        import lxdm as _lxdm
        import login as _login
        import lightdm as _lightdm
        import maintenance as _maintenance
        import gui as _gui
        import att as _att
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
        lxdm = _lxdm
        login = _login
        lightdm = _lightdm
        maintenance = _maintenance
        gui = _gui
        att = _att
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

        # ensuring we have a backup of /etc/lightdm/lightdm.conf
        if fn.path.isfile(fn.lightdm_conf):
            if not fn.path.isfile(fn.lightdm_conf_bak):
                try:
                    fn.shutil.copy(fn.lightdm_conf, fn.lightdm_conf_bak)
                except Exception as error:
                    print(error)

        # ensuring we have a backup of /etc/lightdm/lightdm-gtk-greeter.conf
        if fn.path.isfile(fn.lightdm_greeter):
            if not fn.path.isfile(fn.lightdm_greeter_bak):
                try:
                    fn.shutil.copy(fn.lightdm_greeter, fn.lightdm_greeter_bak)
                except Exception as error:
                    print(error)

        # ensuring we have a backup of /etc/lightdm/slick-greeter.conf
        if fn.path.isfile(fn.lightdm_slick_greeter):
            if not fn.path.isfile(fn.lightdm_slick_greeter_bak):
                try:
                    fn.shutil.copy(
                        fn.lightdm_slick_greeter, fn.lightdm_slick_greeter_bak
                    )
                except Exception as error:
                    print(error)

        # ensuring we have a backup of /etc/lxdm/lxdm.conf
        if fn.path.isfile(fn.lxdm_conf):
            if not fn.path.isfile(fn.lxdm_conf_bak):
                try:
                    fn.shutil.copy(fn.lxdm_conf, fn.lxdm_conf_bak)
                except Exception as error:
                    print(error)

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

        # ensuring we have a backup or the arcolinux mirrorlist
        if fn.path.isfile(fn.arcolinux_mirrorlist):
            if not fn.path.isfile(fn.arcolinux_mirrorlist + ".bak"):
                try:
                    fn.shutil.copy(
                        fn.arcolinux_mirrorlist, fn.arcolinux_mirrorlist + ".bak"
                    )
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

        # make backup of /etc/default/grub
        # renaming bak to back for BigLinux
        if fn.path.isfile(fn.grub_default_grub):
            if not fn.path.isfile(fn.grub_default_grub + ".back"):
                try:
                    fn.shutil.copy(fn.grub_default_grub, fn.grub_default_grub + ".back")
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
                        fn.shutil.copy(fn.sddm_default_d1_arco, fn.sddm_default_d1)
                        fn.shutil.copy(fn.sddm_default_d2_arco, fn.sddm_default_d2)
                except Exception as error:
                    print(error)

            # if there is NO sddm.conf at all - both are not there
            if not fn.path.exists(fn.sddm_default_d1) and not fn.path.exists(
                fn.sddm_default_d2
            ):
                try:
                    fn.shutil.copy(fn.sddm_default_d1_arco, fn.sddm_default_d1)
                    fn.shutil.copy(fn.sddm_default_d2_arco, fn.sddm_default_d2)

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
                fn.shutil.copy(fn.sddm_default_d1_arco, fn.sddm_default_d1)
                fn.shutil.copy(fn.sddm_default_d2_arco, fn.sddm_default_d2)
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

        gui.gui(self, Gtk, Gdk, GdkPixbuf, base_dir, os, Pango)
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
        #                     LIGHTDM
        # =====================================================

        if fn.path.exists("/usr/bin/lightdm"):
            if fn.path.isfile(fn.lightdm_conf):
                try:
                    if "#" in lightdm.check_lightdm(
                        fn.get_lines(fn.lightdm_conf), "autologin-user="
                    ):
                        self.autologin_lightdm.set_active(False)
                        self.sessions_lightdm.set_sensitive(False)
                    else:
                        self.autologin_lightdm.set_active(True)
                        self.sessions_lightdm.set_sensitive(True)
                except Exception as error:
                    print(error)

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

        # =====================================================
        #                        LXDM
        # =====================================================

        if fn.path.exists("/usr/bin/lxdm"):
            try:
                pos = fn.get_position(fn.get_lines(fn.lxdm_conf), "bottom_pane=")
                lines = fn.get_lines(fn.lxdm_conf)
                state = lines[pos].split("=")[1].strip()
                if fn.path.isfile(fn.lxdm_conf):
                    if state == "1":
                        self.panel_lxdm.set_active(True)
                    else:
                        self.panel_lxdm.set_active(False)
            except Exception as error:
                pass

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
        att.install_themes(self)
        # populate lightdm page
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_theme_names_lightdm(self, self.gtk_theme_names_lightdm)
        # populate lxdm page
        if fn.check_package_installed("lxdm"):
            lxdm.pop_gtk_theme_names_lxdm(self.lxdm_gtk_theme)

    def on_remove_att_themes_clicked(self, widget):
        print("We have removed all the selected themes")
        fn.show_in_app_notification(self, "We have removed all the selected themes")
        att.remove_themes(self)
        # populate lightdm page
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_theme_names_lightdm(self, self.gtk_theme_names_lightdm)
        # populate lxdm page
        if fn.check_package_installed("lxdm"):
            lxdm.pop_gtk_theme_names_lxdm(self.lxdm_gtk_theme)

    def on_find_att_themes_clicked(self, widget):
        print("ATT : We show the installed themes")
        fn.show_in_app_notification(self, "We show the installed themes")
        att.find_themes(self)
        # populate lightdm page
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_theme_names_lightdm(self, self.gtk_theme_names_lightdm)
        # populate lxdm page
        if fn.check_package_installed("lxdm"):
            lxdm.pop_gtk_theme_names_lxdm(self.lxdm_gtk_theme)

    # ====================================================================
    # Sardi

    def on_install_att_sardi_icon_themes_clicked(self, widget):
        print("ATT : We have installed all the selected sardi icon themes")
        fn.show_in_app_notification(
            self, "We have installed all the selected sardi icon themes"
        )
        att.install_sardi_icons(self)
        # populate icon names on lightdm
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)

    def on_remove_att_sardi_icon_themes_clicked(self, widget):
        print("ATT : We have removed all the selected sardi icon themes")
        fn.show_in_app_notification(
            self, "We have removed all the selected sardi icon themes"
        )
        att.remove_sardi_icons(self)
        # populate icon names lightdm
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)

    def on_find_att_sardi_icon_themes_clicked(self, widget):
        print("ATT : We show the installed sardi icon themes")
        fn.show_in_app_notification(self, "We show the installed sardi icon themes")
        att.find_sardi_icons(self)
        # populate icon names on lightdm
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)

    # ====================================================================
    # surfn

    def on_install_att_surfn_icon_themes_clicked(self, widget):
        print("ATT : We have installed all the selected Surfn cursor themes")
        fn.show_in_app_notification(
            self, "We have installed all the selected Surfn cursor themes"
        )
        att.install_surfn_icons(self)
        # populate icon names on lightdm
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)

    def on_remove_att_surfn_icon_themes_clicked(self, widget):
        print("ATT : We have removed all the selected Surfn cursor themes")
        fn.show_in_app_notification(
            self, "We have removed all the selected Surfn cursor themes"
        )
        att.remove_surfn_icons(self)
        # populate icon names on lightdm
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)

    def on_find_att_surfn_icon_themes_clicked(self, widget):
        print("ATT : We show all the installed Surfn icon themes")
        fn.show_in_app_notification(self, "We show all the installed Surfn icon themes")
        att.find_surfn_icons(self)
        # populate icon names on lightdm
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)

    # ====================================================================
    # selection of theming

    def on_click_att_theming_all_selection(self, widget):
        print("ATT : We have selected all themes")
        fn.show_in_app_notification(self, "We have selected all themes")
        att.set_att_checkboxes_theming_all(self)

    def on_click_att_theming_blue_selection(self, widget):
        print("ATT : We have selected the normal selection - blue themes")
        fn.show_in_app_notification(
            self, "We have selected the normal selection - blue themes"
        )
        att.set_att_checkboxes_theming_blue(self)

    def on_click_att_theming_dark_selection(self, widget):
        print("ATT : We have selected the minimal selection - dark themes")
        fn.show_in_app_notification(
            self, "We have selected the minimal selection - dark themes"
        )
        att.set_att_checkboxes_theming_dark(self)

    def on_click_att_theming_none_selection(self, widget):
        print("ATT : We have selected no themes")
        fn.show_in_app_notification(self, "We have selected no themes")
        att.set_att_checkboxes_theming_none(self)

    # selection of icon theming
    def on_click_att_sardi_icon_theming_all_selection(self, widget):
        print("ATT : We have selected all sardi icons")
        fn.show_in_app_notification(self, "We have selected all sardi icons")
        att.set_att_checkboxes_theming_sardi_icons_all(self)

    def on_click_att_sardi_icon_theming_mint_selection(self, widget):
        print("ATT : We have selected the mint selection - sardi icons")
        fn.show_in_app_notification(
            self, "We have selected the mint selection - sardi icons"
        )
        att.set_att_checkboxes_theming_sardi_mint_icons(self)

    def on_click_att_sardi_icon_theming_mixing_selection(self, widget):
        print("ATT : We have selected the mixing selection - sardi icons")
        fn.show_in_app_notification(
            self, "We have selected the mixing selection - sardi icons"
        )
        att.set_att_checkboxes_theming_sardi_mixing_icons(self)

    def on_click_att_sardi_icon_theming_variations_selection(self, widget):
        print("ATT : We have selected the variation selection - sardi icons")
        fn.show_in_app_notification(
            self, "We have selected the variation selection - sardi icons"
        )
        att.set_att_checkboxes_theming_sardi_icons_variations(self)

    def on_click_att_sardi_icon_theming_none_selection(self, widget):
        print("ATT : We have selected no sardi icons")
        fn.show_in_app_notification(self, "We have selected no sardiicons")
        att.set_att_checkboxes_theming_sardi_icons_none(self)

    # different families of SARDI

    def on_click_att_fam_sardi_icon_theming_sardi_selection(self, widget):
        print("ATT : We have selected the Sardi family")
        fn.show_in_app_notification(self, "We have selected the Sardi family themes")
        att.set_att_fam_checkboxes_theming_sardi_icons(self)

    def on_click_att_fam_sardi_icon_theming_sardi_flexible_selection(self, widget):
        print("ATT : We have selected the Sardi flexible family")
        fn.show_in_app_notification(
            self, "We have selected the Sardi flexible family themes"
        )
        att.set_att_fam_checkboxes_theming_sardi_flexible(self)

    def on_click_att_fam_sardi_icon_theming_sardi_mono_selection(self, widget):
        print("ATT : We have selected the Sardi mono family")
        fn.show_in_app_notification(
            self, "We have selected the Sardi mono family themes"
        )
        att.set_att_fam_checkboxes_theming_sardi_mono(self)

    def on_click_att_fam_sardi_icon_theming_sardi_flat_selection(self, widget):
        print("ATT : We have selected the Sardi flat family")
        fn.show_in_app_notification(
            self, "We have selected the Sardi flat family themes"
        )
        att.set_att_fam_checkboxes_theming_sardi_flat(self)

    def on_click_att_fam_sardi_icon_theming_sardi_ghost_selection(self, widget):
        print("ATT : We have selected the Sardi ghost family")
        fn.show_in_app_notification(
            self, "We have selected the Sardi ghost family themes"
        )
        att.set_att_fam_checkboxes_theming_sardi_ghost(self)

    def on_click_att_fam_sardi_icon_theming_sardi_orb_selection(self, widget):
        print("ATT : We have selected the Sardi orb family")
        fn.show_in_app_notification(
            self, "We have selected the Sardi orb family themes"
        )
        att.set_att_fam_checkboxes_theming_sardi_orb(self)

    # selection of Surfn icons theming
    def on_click_att_surfn_theming_all_selection(self, widget):
        print("ATT : We have selected all cursors")
        fn.show_in_app_notification(self, "We have selected all cursors")
        att.set_att_checkboxes_theming_surfn_icons_all(self)

    def on_click_att_surfn_theming_normal_selection(self, widget):
        print("ATT : We have selected the normal selection - cursors")
        fn.show_in_app_notification(
            self, "We have selected the normal selection - cursors"
        )
        att.set_att_checkboxes_theming_surfn_icons_normal(self)

    def on_click_att_surfn_theming_minimal_selection(self, widget):
        print("ATT : We have selected the minimal selection - cursors")
        fn.show_in_app_notification(
            self, "We have selected the minimal selection - cursors"
        )
        att.set_att_checkboxes_theming_surfn_icons_minimal(self)

    def on_click_att_surfn_theming_none_selection(self, widget):
        print("ATT : We have selected no cursors")
        fn.show_in_app_notification(self, "We have selected no cursors")
        att.set_att_checkboxes_theming_surfn_icons_none(self)

    def on_install_extras_clicked(self, widget):
        print("ATT : We install the selected projects")
        fn.show_in_app_notification(self, "We install the selected projects")
        att.install_att_extras(self)
        # populate lightdm page
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_theme_names_lightdm(self, self.gtk_theme_names_lightdm)
            lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)
        # populate lxdm page
        if fn.check_package_installed("lxdm"):
            lxdm.pop_gtk_theme_names_lxdm(self.lxdm_gtk_theme)

    # extras
    def on_remove_extras_clicked(self, widget):
        print("ATT : We remove the selected projects")
        fn.show_in_app_notification(self, "We remove the selected projects")
        att.remove_att_extras(self)
        # populate lightdm page
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_theme_names_lightdm(self, self.gtk_theme_names_lightdm)
            lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)
        # populate lxdm page
        if fn.check_package_installed("lxdm"):
            lxdm.pop_gtk_theme_names_lxdm(self.lxdm_gtk_theme)

    def on_find_extras_clicked(self, widget):
        print("ATT : We show the installed projects")
        fn.show_in_app_notification(self, "We show the installed projects")
        att.find_att_extras(self)
        # populate lightdm page
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_theme_names_lightdm(self, self.gtk_theme_names_lightdm)
            lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)
        # populate lxdm page
        if fn.check_package_installed("lxdm"):
            lxdm.pop_gtk_theme_names_lxdm(self.lxdm_gtk_theme)

    # selection of extras theming
    def on_click_extras_theming_all_selection(self, widget):
        print("ATT : We have selected all projects")
        fn.show_in_app_notification(self, "We have selected all projects")
        att.set_att_checkboxes_extras_all(self)

    def on_click_extras_theming_none_selection(self, widget):
        print("ATT : We have selected none of the projects")
        fn.show_in_app_notification(self, "We have selected none of the projects")
        att.set_att_checkboxes_extras_none(self)

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
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)
        # populate lightdm page
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_theme_names_lightdm(self, self.gtk_theme_names_lightdm)
        # populate lxdm page
        if fn.check_package_installed("lxdm"):
            lxdm.pop_gtk_theme_names_lxdm(self.lxdm_gtk_theme)

    def on_remove_themes_clicked(self, widget):
        design.remove_themes(self)
        print("We have removed all the selected themes")
        fn.show_in_app_notification(self, "We have removed all the selected themes")
        # populate cursor themes - some themes include a cursor
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)
        # populate lightdm page
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_theme_names_lightdm(self, self.gtk_theme_names_lightdm)
        # populate lxdm page
        if fn.check_package_installed("lxdm"):
            lxdm.pop_gtk_theme_names_lxdm(self.lxdm_gtk_theme)

    def on_find_themes_clicked(self, widget):
        design.find_themes(self)
        print("We show all the installed themes")
        fn.show_in_app_notification(self, "We show all the installed themes")
        # populate cursor themes - some themes include a cursor
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)
        # populate lightdm page
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_theme_names_lightdm(self, self.gtk_theme_names_lightdm)
        # populate lxdm page
        if fn.check_package_installed("lxdm"):
            lxdm.pop_gtk_theme_names_lxdm(self.lxdm_gtk_theme)

    # icons
    def on_install_icon_themes_clicked(self, widget):
        design.install_icon_themes(self)
        print("We have installed all the selected icon themes")
        fn.show_in_app_notification(
            self, "We have installed all the selected icon themes"
        )
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)
            # populate cursor themes
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_remove_icon_themes_clicked(self, widget):
        design.remove_icon_themes(self)
        print("We have removed all the selected icon themes")
        fn.show_in_app_notification(
            self, "We have removed all the selected icon themes"
        )
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)
        # populate cursor themes
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_find_icon_themes_clicked(self, widget):
        design.find_icon_themes(self)
        print("We show all the installed icon themes")
        fn.show_in_app_notification(self, "We show all the installed icon themes")
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_icon_names_lightdm(self, self.gtk_icon_names_lightdm)
        # populate cursor themes
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
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
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
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
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_find_cursor_themes_clicked(self, widget):
        design.find_cursor_themes(self)
        print("We show all the installed cursor themes")
        fn.show_in_app_notification(self, "We show all the installed cursor themes")
        # populate cursor themes
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
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
        pathway = base_dir + "/data/arch/packages/"
        file = fn.listdir(pathway)
        fn.install_local_package(self, pathway + str(file).strip("[]'"))

    def on_click_install_arch_keyring_online(self, widget):
        pathway = "/tmp/att-installation/"
        fn.mkdir(pathway)
        command = (
            "wget https://archlinux.org/packages/core/any/archlinux-keyring/download --content-disposition -P"
            + pathway
        )
        try:
            fn.subprocess.call(
                command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Downloading the package")
            GLib.idle_add(fn.show_in_app_notification, self, "Downloading the package")
        except Exception as error:
            print(error)

        file = fn.listdir(pathway)
        fn.install_local_package(self, pathway + str(file).strip("[]'"))
        try:
            fn.shutil.rmtree(pathway)
        except Exception as error:
            print(error)

    def on_click_fix_pacman_keys(self, widget):
        fn.install_package(self, "alacritty")
        try:
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/any/fix-pacman-databases-and-keys",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Pacman has been reset (gpg, libraries,keys)")
            GLib.idle_add(fn.show_in_app_notification, self, "Pacman keys fixed")
        except Exception as error:
            print(error)

    def on_click_probe(self, widget):
        fn.install_package(self, "hw-probe")
        fn.install_package(self, "alacritty")
        try:
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/arco/bin/arcolinux-probe",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Probe link has been created")
            GLib.idle_add(
                fn.show_in_app_notification, self, "Probe link has been created"
            )
        except Exception as error:
            print(error)

    def on_click_fix_mainstream(self, widget):
        fn.install_package(self, "alacritty")
        try:
            command = "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/any/set-mainstream-servers"
            fn.subprocess.call(
                command.split(" "),
                shell=False,
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

    def on_click_get_arch_mirrors(self, widget):
        fn.install_package(self, "alacritty")
        try:
            fn.install_package(self, "reflector")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/any/archlinux-get-mirrors-reflector",
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
                "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/any/archlinux-get-mirrors-rate-mirrors",
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
        if not fn.path.isfile(fn.gpg_conf + ".bak"):
            fn.shutil.copy(fn.gpg_conf, fn.gpg_conf + ".bak")
        fn.shutil.copy(fn.gpg_conf_original, fn.gpg_conf)
        print("The new /etc/pacman.d/gnupg/gpg.conf has been saved")
        print("We only add servers to the config")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "The new /etc/pacman.d/gnupg/gpg.conf has been saved",
        )

    def on_click_fix_pacman_gpg_conf_local(self, widget):
        if not fn.path.isdir(fn.home + "/.gnupg"):
            try:
                fn.makedirs(fn.home + "/.gnupg", 0o766)
                fn.permissions(fn.home + "/.gnupg")
            except Exception as error:
                print(error)

        if not fn.path.isfile(fn.gpg_conf_local + ".bak"):
            try:
                fn.shutil.copy(fn.gpg_conf_local, fn.gpg_conf_local + ".bak")
                fn.permissions(fn.gpg_conf_local + ".bak")
            except Exception as error:
                print(error)

        fn.shutil.copy(fn.gpg_conf_local_original, fn.gpg_conf_local)
        fn.permissions(fn.gpg_conf_local)
        print("The new ~/.gnupg/gpg.conf has been saved")
        print("We only add servers to the config")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "The new ~/.gnupg/gpg.conf has been saved",
        )

    def on_click_install_arch_mirrors(self, widget):
        fn.install_package(self, "reflector")
        self.btn_run_reflector.set_sensitive(True)

    def on_click_install_arch_mirrors2(self, widget):
        fn.install_arco_package(self, "rate-mirrors")
        self.btn_run_rate_mirrors.set_sensitive(True)

    def on_click_apply_global_cursor(self, widget):
        cursor = fn.get_combo_text(self.cursor_themes)
        maintenance.set_global_cursor(self, cursor)
        print("Cursor is saved in /usr/share/icons/default")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Cursor saved in /usr/share/icons/default",
        )

    def on_click_remove_all_variety_packages(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/arco/bin/arcolinux-remove-variety",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Removing variety and any related packages")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Removing variety and any related packages",
            )
        except:
            print("Install alacritty")

    def on_click_remove_all_conky_packages(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/arco/bin/arcolinux-remove-conky",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Removing conky and any related packages")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Removing conky and any related packages",
            )
        except:
            print("Install alacritty")

    def on_click_remove_all_kernels_but_linux(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/arco/bin/arcolinux-remove-all-kernels-but-linux",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Removing kernel(s) and any related packages")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Removing kernel(s) and any related packages",
            )
        except:
            print("Install alacritty")

    def on_click_remove_all_kernels_but_linux_cachyos(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/arco/bin/arcolinux-remove-all-kernels-but-linux-cachyos",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Removing kernel(s) and any related packages")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Removing kernel(s) and any related packages",
            )
        except:
            print("Install alacritty")

    def on_click_remove_all_kernels_but_linux_lts(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/arco/bin/arcolinux-remove-all-kernels-but-linux-lts",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Removing kernel(s) and any related packages")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Removing kernel(s) and any related packages",
            )
        except:
            print("Install alacritty")

    def on_click_remove_all_kernels_but_linux_zen(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/arco/bin/arcolinux-remove-all-kernels-but-linux-zen",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Removing kernel(s) and any related packages")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Removing kernel(s) and any related packages",
            )
        except:
            print("Install alacritty")

    def on_click_change_debug(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e /usr/share/archlinux-tweak-tool/data/arco/bin/remove-debug",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Changing debug into !debug in /etc/makepkg.conf")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Changing debug into !debug in /etc/makepkg.conf",
            )
        except:
            print("Install alacritty")

    def on_click_update_system(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e bash -c 'sudo pacman -Syu; echo \"you can close this window now\"'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Updating system")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "System update completed",
            )
        except:
            print("Update system failed")

    def on_click_clean_cache(self, widget):
        try:
            fn.install_package(self, "alacritty")
            fn.subprocess.call(
                "alacritty --hold -e bash -c 'sudo pacman -Sc; echo \"you can close this window now\"'",
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Cleaning pacman cache")
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Pacman cache cleaned",
            )
        except:
            print("Clean cache failed")

    # ====================================================================
    #                       GRUB
    # ====================================================================

    def on_grub_item_clicked(self, widget, data):
        for x in data:
            self.grub_image_path = x.get_name()

    def on_set_grub_wallpaper(self, widget):
        if not fn.path.isfile(fn.grub_theme_conf):
            self.on_click_install_arco_vimix_clicked(self)

        if self.grub_image_path == "":
            fn.show_in_app_notification(self, "First choose a wallpaper image")
        else:
            fn.set_grub_wallpaper(self, self.grub_image_path)

    def on_reset_grub_wallpaper(self, widget):
        if fn.path.isfile(fn.grub_theme_conf + ".bak"):
            fn.shutil.copy(fn.grub_theme_conf + ".bak", fn.grub_theme_conf)
        self.pop_themes_grub(self.grub_theme_combo, fn.get_grub_wallpapers(), True)

        if not fn.path.isfile(fn.grub_theme_conf):
            self.on_click_install_arco_vimix_clicked(self)

        print("Default Vimix grub wallpaper applied")
        fn.show_in_app_notification(self, "Default Vimix grub wallpaper applied")

    def on_reset_grub(self, widget):
        if fn.path.isfile(fn.grub_default_grub + ".back"):
            fn.shutil.copy(fn.grub_default_grub + ".back", fn.grub_default_grub)
        self.pop_themes_grub(self.grub_theme_combo, fn.get_grub_wallpapers(), True)
        fn.make_grub(self)

    def pop_themes_grub(self, combo, lists, start):
        if fn.path.isfile(fn.grub_theme_conf):
            _m = combo.get_model(); _m.splice(0, _m.get_n_items(), [])
            with open(fn.grub_theme_conf, "r", encoding="utf-8") as f:
                listss = f.readlines()
                f.close()

            val = fn.get_position(listss, "desktop-image: ")
            # bg_image = listss[val].split(" ")[1].replace('"', "").strip()

            child = self.fb.get_first_child()
            while child is not None:
                next_child = child.get_next_sibling()
                self.fb.remove(child)
                child = next_child

            for x in lists:
                pb = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    "/boot/grub/themes/Vimix/" + x, 128, 128
                )
                pimage = Gtk.Image()
                pimage.set_name("/boot/grub/themes/Vimix/" + x)
                pimage.set_from_pixbuf(pb)
                self.fb.append(pimage)

    def on_grub_theme_change(self, widget, pspec=None):
        try:
            pixbuf3 = GdkPixbuf.Pixbuf.new_from_file_at_size(
                "/boot/grub/themes/Vimix/" + fn.get_combo_text(widget),
                645,
                645,
            )
            print(fn.get_combo_text(widget))
            self.image_grub.set_from_pixbuf(pixbuf3)
        except Exception as error:
            print(error)

    def on_import_wallpaper(self, widget):
        text = self.tbimage.get_text()
        if len(text) > 1:
            print(fn.path.basename(text))
            fn.shutil.copy(text, "/boot/grub/themes/Vimix/" + fn.path.basename(text))
            self.pop_themes_grub(self.grub_theme_combo, fn.get_grub_wallpapers(), False)
        else:
            print("First search for a wallpaper")
            fn.show_in_app_notification(self, "First select an image")

    def on_remove_wallpaper(self, widget):
        widget.set_sensitive(False)
        if fn.path.isfile(self.grub_image_path):
            excludes = [
                "archlinux03.jpg",
                "archlinux04.jpg",
                "archlinux06.jpg",
                "archlinux07.jpg",
                "arcolinux01.jpg",
                "arcolinux02.jpg",
                "arcolinux03.jpg",
                "arcolinux04.jpg",
                "arcolinux05.jpg",
                "arcolinux06.jpg",
                "arcolinux07.jpg",
                "arcolinux08.jpg",
                "background-slaze.jpg",
                "background-stylish.jpg",
                "background-tela.jpg",
                "background-vimix.jpg",
                "archlinux01.png",
                "archlinux02.png",
                "archlinux05.png",
                "arcolinux09.png",
                "arcolinux10.png",
                "arcolinux11.png",
                "arcolinux.png",
                "background.png",
            ]

            if not fn.path.basename(self.grub_image_path) in excludes:
                fn.unlink(self.grub_image_path)
                self.pop_themes_grub(
                    self.grub_theme_combo, fn.get_grub_wallpapers(), True
                )
                fn.show_in_app_notification(self, "Wallpaper removed successfully")
            else:
                fn.show_in_app_notification(self, "You can not remove that wallpaper")
        else:
            print("First select a wallpaper to remove")
            fn.show_in_app_notification(self, "First select a wallpaper to remove")
        widget.set_sensitive(True)

    def on_choose_wallpaper(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file",
            transient_for=self,
            action=Gtk.FileChooserAction.OPEN,
        )
        filter = Gtk.FileFilter()
        filter.set_name("IMAGE Files")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpg")
        filter.add_mime_type("image/jpeg")
        dialog.set_filter(filter)
        dialog.set_current_folder(Gio.File.new_for_path(fn.home))
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_Open", Gtk.ResponseType.OK)
        dialog.connect("response", self.open_response_cb)

        dialog.present()

    def open_response_cb(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            f = dialog.get_file()
            if f:
                self.tbimage.set_text(f.get_path())
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def on_click_install_arco_vimix_clicked(self, desktop):
        if fn.check_package_installed("grub2-theme-vimix-git"):
            fn.remove_package(self, "grub2-theme-vimix-git")
        fn.install_arco_package(self, "arcolinux-grub-theme-vimix-git")
        if fn.check_package_installed("arcolinux-grub-theme-vimix-git"):
            fn.set_default_grub_theme(self)
            fn.make_grub(self)
            GLib.idle_add(
                fn.show_in_app_notification, self, "Setting saved successfully"
            )
        fn.restart_program()

    def on_reset_grub_vimix(self, desktop):
        fn.install_arco_package(self, "arcolinux-grub-theme-vimix-git")
        fn.set_default_grub_theme(self)
        fn.make_grub(self)
        GLib.idle_add(fn.show_in_app_notification, self, "Vimix has been installed")

    def on_click_install_orignal_grub_rebornos(self, widget):
        if fn.check_package_installed("arcolinux-grub-theme-vimix-git"):
            fn.remove_package(self, "arcolinux-grub-theme-vimix-git")
        fn.install_package(self, "grub2-theme-vimix-git")
        self.on_reset_grub(self)
        fn.restart_program()

    def on_clicked_grub_timeout(self, widget):
        seconds = int(self.scale.get_value())
        fn.set_grub_timeout(self, seconds)
        fn.make_grub(self)

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
            print("First activate the nemesis repo")
            self.hbswich.set_active(False)
            GLib.idle_add(
                fn.show_in_app_notification, self, "First activate the nemesis repo"
            )

    def set_ublock_firefox(self, widget, state):
        t = fn.threading.Thread(
            target=fn.set_firefox_ublock, args=(self, widget, widget.get_active())
        )
        t.start()

    # ====================================================================
    #                       LIGHTDM
    # ====================================================================

    def on_click_lightdm_apply(self, widget):
        # for autologin, user and session
        if (
            (
                self.sessions_lightdm.get_selected_item() is not None
                and self.autologin_lightdm.get_active() is True
            )
            or self.autologin_lightdm.get_active() is False
            and self.gtk_theme_names_lightdm.get_selected_item() is not None
            and self.gtk_icon_names_lightdm.get_selected_item() is not None
            and self.cursor_themes_lightdm.get_selected_item() is not None
        ):
            t1 = fn.threading.Thread(
                target=lightdm.set_lightdm_value,
                args=(
                    self,
                    fn.get_lines(fn.lightdm_conf),
                    fn.sudo_username,
                    fn.get_combo_text(self.sessions_lightdm),
                    self.autologin_lightdm.get_active(),
                ),
            )
            t1.daemon = True
            t1.start()
            print("Lightdm autologin and session settings saved successfully")
        else:
            print("Make sure all variables are filled in")
            fn.show_in_app_notification(self, "Fill in all fields")

        # for theme,icon and cursor - lightdm greeter
        if (
            (self.gtk_theme_names_lightdm.get_selected_item() is not None)
            and self.gtk_icon_names_lightdm.get_selected_item() is not None
            and self.cursor_themes_lightdm.get_selected_item() is not None
        ):
            t1 = fn.threading.Thread(
                target=lightdm.set_lightdm_icon_theme_cursor,
                args=(
                    self,
                    fn.get_lines(fn.lightdm_greeter),
                    fn.get_combo_text(self.gtk_theme_names_lightdm),
                    fn.get_combo_text(self.gtk_icon_names_lightdm),
                    fn.get_combo_text(self.cursor_themes_lightdm),
                ),
            )
            t1.daemon = True
            t1.start()
            print("Lightdm icon and theme settings saved successfully")
        else:
            print("Make sure all variables are filled in")
            fn.show_in_app_notification(self, "Fill in all fields")

        # for theme,icon and cursor - slick greeter
        if (
            (self.gtk_theme_names_lightdm.get_selected_item() is not None)
            and self.gtk_icon_names_lightdm.get_selected_item() is not None
            and self.cursor_themes_lightdm.get_selected_item() is not None
        ):
            t1 = fn.threading.Thread(
                target=lightdm.set_lightdm_icon_theme_cursor_slick,
                args=(
                    self,
                    fn.get_lines(fn.lightdm_slick_greeter),
                    fn.get_combo_text(self.gtk_theme_names_lightdm),
                    fn.get_combo_text(self.gtk_icon_names_lightdm),
                ),
            )
            t1.daemon = True
            t1.start()
            print("Lightdm icon and theme settings saved successfully")
        else:
            print("Make sure all variables are filled in")
            fn.show_in_app_notification(self, "Fill in all fields")

    def on_click_install_arco_lightdmgreeter(self, widget):
        if fn.path.isfile(fn.lightdm_greeter_arco_att):
            fn.shutil.copy(fn.lightdm_greeter_arco_att, fn.lightdm_greeter)

        print("Lightdm gtk-greeter-settings applied")
        fn.show_in_app_notification(self, "Lightdm gtk-greeter-settings applied")

    def on_click_reset_lightdm_lightdm_greeter(self, widget):
        if fn.path.isfile(fn.lightdm_conf_bak):
            fn.shutil.copy(fn.lightdm_conf_bak, fn.lightdm_conf)
        if fn.path.isfile(fn.lightdm_greeter_bak):
            fn.shutil.copy(fn.lightdm_greeter_bak, fn.lightdm_greeter)

        if "#" in lightdm.check_lightdm(
            fn.get_lines(fn.lightdm_conf), "autologin-user="
        ):
            self.autologin_lightdm.set_active(False)
        else:
            self.autologin_lightdm.set_active(True)

        print("Lightdm and lightdm gtk-greeter-settings applied")
        fn.show_in_app_notification(self, "Lightdm settings applied")
        fn.restart_program()

    def on_autologin_lightdm_activated(self, widget, gparam):
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

            self.sessions_lightdm.set_sensitive(True)
        else:
            self.sessions_lightdm.set_sensitive(False)

    # no lightdm present
    def on_click_att_lightdm_clicked(self, desktop):
        fn.install_package(self, "lightdm")
        fn.install_package(self, "lightdm-gtk-greeter")
        fn.install_package(self, "lightdm-gtk-greeter-settings")
        print("--------------------------------------------")
        print("Do not forget to enable Lightdm")
        print("--------------------------------------------")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Lightdm has been installed but not enabled",
        )
        try:
            fn.shutil.copy(fn.lightdm_conf_arco, fn.lightdm_conf)
            fn.shutil.copy(fn.lightdm_greeter_arco, fn.lightdm_greeter)
            fn.shutil.copy(fn.ligthdm_slick_greeter_arco, fn.lightdm_slick_greeter)
        except Exception as error:
            print(error)
        fn.restart_program()

    def on_click_lightdm_enable(self, desktop):
        fn.install_package(self, "lightdm")
        fn.install_package(self, "lightdm-gtk-greeter")
        fn.enable_login_manager(self, "lightdm")

    def on_click_install_slick_greeter(self, desktop):
        fn.install_package(self, "lightdm-slick-greeter")
        fn.enable_slick_greeter(self)
        login.find_slick_greeter_label(self.lbl_slickgreeter)

    def on_click_remove_slick_greeter(self, desktop):
        fn.remove_package(self, "lightdm-slick-greeter")
        fn.disable_slick_greeter(self)
        login.find_slick_greeter_label(self.lbl_slickgreeter)

    def on_click_lightdm_reset_original_att(self, widget):
        try:
            fn.shutil.copy(fn.lightdm_conf_arco, fn.lightdm_conf)
            fn.shutil.copy(fn.lightdm_greeter_arco, fn.lightdm_greeter)
            fn.shutil.copy(fn.ligthdm_slick_greeter_arco, fn.lightdm_slick_greeter)
        except Exception as error:
            print(error)

        print(
            "All files have been changed /etc/lightdm.conf, /etc/lightdm-gtk-greeter.conf"
        )
        print("and /etc/lightdm/slick-greeter.conf")
        print("Now change the configuration like you want it to be and save")
        fn.show_in_app_notification(
            self, "The ATT lightdm configuration is now applied"
        )
        fn.restart_program()

    # ====================================================================
    #                        LXDM
    # ====================================================================

    def on_click_install_lxdm(self, desktop):
        fn.install_package(self, "lxdm")
        print("--------------------------------------------")
        print("Do not forget to enable Lxdm")
        print("--------------------------------------------")
        fn.restart_program()

    # no lxdm present
    def on_click_att_lxdm_clicked(self, desktop):
        fn.install_package(self, "lxdm")
        try:
            fn.shutil.copy(fn.lxdm_conf_arco, fn.lxdm_conf)
        except Exception as error:
            print(error)
        try:
            fn.shutil.copy(fn.lxdm_conf_arco, fn.lxdm_conf)
        except Exception as error:
            print(error)
        print("--------------------------------------------")
        print("Do not forget to enable Lxdm")
        print("--------------------------------------------")
        fn.restart_program()

    def on_click_lxdm_enable(self, desktop):
        fn.install_package(self, "lxdm")
        fn.enable_login_manager(self, "lxdm")

    def on_autologin_lxdm_activated(self, widget, gparam):
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

    def on_click_lxdm_reset_original_att(self, widget):
        try:
            fn.shutil.copy(fn.lxdm_conf_arco, fn.lxdm_conf)
        except Exception as error:
            print(error)

        print("ATT Lxdm configuration file has been saved /etc/lxdm/lxdm.conf")
        print("Now change the configuration like you want it to be and save")
        fn.show_in_app_notification(self, "The ATT Lxdm configuration is now applied")
        fn.restart_program()

    def on_click_lxdm_reset(self, widget):
        if fn.path.isfile(fn.lxdm_conf_bak):
            fn.shutil.copy(fn.lxdm_conf_bak, fn.lxdm_conf)
        print("Lxdm default settings applied")
        fn.show_in_app_notification(self, "Lxdm default settings applied")
        fn.restart_program()

    def on_click_install_att_lxdm_minimalo(self, widget):
        fn.install_arco_package(self, "arcolinux-lxdm-theme-minimalo-git")
        lxdm.pop_lxdm_theme_greeter(self.lxdm_theme_greeter)

    def on_click_remove_att_lxdm_minimalo(self, widget):
        fn.remove_package(self, "arcolinux-lxdm-theme-minimalo-git")
        lxdm.pop_lxdm_theme_greeter(self.lxdm_theme_greeter)

    def on_click_install_lxdm_themes(self, widget):
        fn.install_arco_package(self, "lxdm-themes")
        lxdm.pop_lxdm_theme_greeter(self.lxdm_theme_greeter)

    def on_click_remove_lxdm_themes(self, widget):
        fn.remove_package(self, "lxdm-themes")
        lxdm.pop_lxdm_theme_greeter(self.lxdm_theme_greeter)

    def on_click_lxdm_apply(self, widget):
        if (
            self.lxdm_gtk_theme.get_selected_item() is not None
            and self.lxdm_theme_greeter.get_selected_item() is not None
        ):
            t1 = fn.threading.Thread(
                target=lxdm.set_lxdm_value,
                args=(
                    self,
                    fn.get_lines(fn.lxdm_conf),
                    fn.sudo_username,
                    fn.get_combo_text(self.lxdm_gtk_theme),
                    fn.get_combo_text(self.lxdm_theme_greeter),
                    self.autologin_lxdm.get_active(),
                    self.panel_lxdm.get_active(),
                ),
            )
            t1.daemon = True
            t1.start()
            print("Lxdm autologin and other session settings saved successfully")
        else:
            print("Select all elements - none can be empty")
            fn.show_in_app_notification(self, "You need to select all elements first")

    # ====================================================================
    #                        FASTFETCH CONFIG
    # ====================================================================

    def on_install_fast(self, widget):
        fn.install_package(self, "fastfetch")

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
            utilities.install_util("lolcat")
            if not util_state or utility == "fastfetch":
                util_state = True
                utilities.set_util_state(self, utility, True, True)
        elif not lolcat_state and utility == "fastfetch":
            utilities.set_util_state(self, utility, True, False)

        utilities.write_configs(utility, util_state, lolcat_state)

    def on_fast_util_toggled(self, switch, gparam):
        util_state = switch.get_active()
        lolcat_state = self.fast_lolcat.get_active()

        fastfetch.toggle_fastfetch(util_state)

        if not util_state:
            self.fast_lolcat.set_active(False)
            lolcat_state = False

        utilities.write_configs("fastfetch", util_state, lolcat_state)
        self.fast_lolcat.set_sensitive(util_state)

    def on_fast_lolcat_toggled(self, switch, gparam):
        lolcat_state = switch.get_active()
        util_state = self.fast_util.get_active()

        if util_state:
            fastfetch.toggle_lolcat(lolcat_state)
            utilities.write_configs("fastfetch", util_state, lolcat_state)

    def util_toggle(self, widget, active, utility):
        util_state = widget.get_active()
        lolcat_state = utilities.get_lolcat_state(self, utility)

        if util_state:
            utilities.install_util(utility)
            if utility == "fastfetch":
                utilities.set_util_state(self, utility, True, lolcat_state)
        else:
            if lolcat_state:
                lolcat_state = False
            utilities.set_util_state(self, utility, False, False)
            if utility == "fastfetch":
                utilities.set_util_state(self, utility, False, False)

            utilities.write_configs(utility, util_state, lolcat_state)

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
        fn.update_repos(self)
        print("sudo pacman -Sy")
        print("All the selected pacman databases are up-to-date")
        fn.show_in_app_notification(
            self, "All the selected pacman databases are up-to-date"
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
        #utilities.set_util_state_arco_switch(self)

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

        if not len(custom_repo_text.get_text(startiter, enditer, True)) < 5:
            print(custom_repo_text.get_text(startiter, enditer, True))
            pmf.append_repo(self, custom_repo_text.get_text(startiter, enditer, True))
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

    # =====================================================
    #               PATREON LINK
    # =====================================================

    def on_social_clicked(self, widget, event):
        sup = support.Support(self)
        sup.connect("response", lambda d, r: d.destroy())
        sup.present()

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
            fn.shutil.copy(fn.sddm_default_d1_arco, fn.sddm_default_d1)
            fn.shutil.copy(fn.sddm_default_d2_arco, fn.sddm_default_d2)
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
            self, "The original sddm.conf and sddm.d.conf is now applied"
        )
        fn.restart_program()

    def on_click_no_sddm_reset_original(self, widget):
        fn.create_sddm_k_dir()
        if fn.path.isfile(fn.sddm_default_d1_arco):
            fn.shutil.copyfile(fn.sddm_default_d1_arco, fn.sddm_default_d1)
            fn.shutil.copyfile(fn.sddm_default_d2_arco, fn.sddm_default_d2)
        print("The ArcoLinux sddm configuration is now applied")
        fn.show_in_app_notification(
            self, "The ArcoLinux sddm configuration is now applied"
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
        fn.install_arco_package(self, "arcolinux-meta-sddm-themes")
        sddm.pop_theme_box(self, self.theme_sddm)

    def on_click_remove_sddm_themes(self, widget):
        fn.remove_package_s(self, "arcolinux-meta-sddm-themes")
        if self.keep_default_theme.get_active() is True:
            fn.install_arco_package(self, "arcolinux-sddm-simplicity-git")
        fn.remove_package_remnants("arcolinux-meta-sddm-themes")
        sddm.pop_theme_box(self, self.theme_sddm)

    def on_click_install_bibata_cursor(self, widget):
        fn.install_arco_package(self, "bibata-cursor-theme-bin")
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_click_remove_bibata_cursor(self, widget):
        fn.remove_package(self, "bibata-cursor-theme-bin")
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_click_install_bibatar_cursor(self, widget):
        fn.install_arco_package(self, "bibata-extra-cursor-theme")
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    def on_click_remove_bibatar_cursor(self, widget):
        fn.remove_package(self, "bibata-extra-cursor-theme")
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    # if no sddm - press 1
    def on_click_att_sddm_clicked(self, desktop):
        fn.install_package(self, "sddm")
        fn.install_arco_package(self, "arcolinux-sddm-simplicity-git")
        print("Do not forget to enable sddm")
        fn.show_in_app_notification(self, "Sddm has been installed but not enabled")
        fn.create_sddm_k_dir()
        fn.shutil.copyfile(fn.sddm_default_d1_arco, fn.sddm_default_d1)
        fn.shutil.copyfile(fn.sddm_default_d2_arco, fn.sddm_default_d2)
        print("The ATT sddm configuration is now applied")
        fn.show_in_app_notification(self, "The ATT sddm configuration is now applied")
        fn.restart_program()

    def on_click_sddm_enable(self, desktop):
        fn.install_package(self, "sddm")
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

    def on_install_discovery_clicked(self, widget):
        fn.install_discovery(self)
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Network discovery is installed - a good nsswitch_config is needed",
        )
        print("Network discovery is installed")

    def on_remove_discovery_clicked(self, widget):
        fn.remove_discovery(self)
        GLib.idle_add(fn.show_in_app_notification, self, "Network discovery is removed")
        print("Network discovery is removed")

    def on_click_reset_nsswitch(self, widget):
        if fn.path.isfile(fn.nsswitch_config + ".bak"):
            fn.shutil.copy(fn.nsswitch_config + ".bak", fn.nsswitch_config)

        print("/etc/nsswitch.config reset")
        fn.show_in_app_notification(self, "Nsswitch config reset")

    def on_click_apply_nsswitch(self, widget):
        services.choose_nsswitch(self)

    # ====================================================================
    #                       SERVICES - SAMBA
    # ====================================================================

    def on_click_create_samba_user(self, widget):
        services.create_samba_user(self)

    def on_click_restart_smb(self, widget):
        services.restart_smb(self)

    def on_click_save_samba_share(self, widget):
        fn.save_samba_config(self)

    def on_click_install_arco_thunar_plugin(self, widget):
        fn.install_arco_thunar_plugin(self, widget)

    def on_click_install_arco_caja_plugin(self, widget):
        fn.install_arco_caja_plugin(self, widget)

    def on_click_install_arco_nemo_plugin(self, widget):
        fn.install_arco_nemo_plugin(self, widget)

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

    def on_click_install_samba(self, widget):
        fn.install_samba(self)
        print("Samba has been successfully installed")
        fn.show_in_app_notification(self, "Samba has been successfully installed")

    def on_click_uninstall_samba(self, widget):
        fn.uninstall_samba(self)
        print("Samba has been successfully uninstalled")
        fn.show_in_app_notification(self, "Samba has been successfully uninstalled")

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

                    grid_package_status.hide()
                    grid_package_count.hide()
                else:
                    grid_package_status.hide()
                    grid_package_count.hide()

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
        try:
            if fn.check_pacman_lockfile() is True:
                fn.logger.warning(
                    "Install aborted, failed to lock database, pacman lockfile exists at %s"
                    % fn.pacman_lockfile
                )

                fn.messagebox(
                    self,
                    "Install aborted",
                    "Failed to lock database, pacman lockfile exists at %s\nIs another pacman process running ?"
                    % fn.pacman_lockfile,
                )
            else:
                packages = packages_obj.get_packages_file_content()

                if packages is not None:
                    packages_prompt_dialog = PackagesPromptGui(packages)
                    packages_prompt_dialog.set_transient_for(self)

                    result_holder = [None]
                    loop = GLib.MainLoop()

                    def on_pkgs_response(dialog, response_id):
                        result_holder[0] = response_id
                        loop.quit()
                        dialog.destroy()

                    packages_prompt_dialog.connect("response", on_pkgs_response)
                    packages_prompt_dialog.present()
                    loop.run()

                    if result_holder[0] == Gtk.ResponseType.OK:
                        widget.set_sensitive(False)
                        fn.logger.info("Preparing installation")
                        vbox_stack = gui_parts[0]
                        grid_package_status = gui_parts[1]
                        grid_package_count = gui_parts[2]
                        vbox_pacmanlog = gui_parts[3]
                        # textbuffer = gui_parts[4]
                        # textview = gui_parts[5]
                        label_package_status = gui_parts[6]
                        label_package_count = gui_parts[7]

                        if vbox_pacmanlog.is_visible() is False:
                            vbox_stack.append(grid_package_status)
                            vbox_stack.append(grid_package_count)
                            vbox_stack.append(vbox_pacmanlog)
                        else:
                            grid_package_status.show()
                            grid_package_count.show()

                        packages_obj.install_packages(packages, widget, gui_parts)
                else:
                    fn.logger.error(
                        "Package list file %s not found"
                        % packages_obj.default_export_path
                    )
                    fn.messagebox(
                        self,
                        "Error package list file not found",
                        "Cannot find %s" % packages_obj.default_export_path,
                    )

        except Exception as e:
            fn.logger.error("Exception in on_click_install_packages(): %s" % e)
            widget.set_sensitive(True)

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

    def on_reload_att_clicked(self, widget):
        # login
        if fn.check_package_installed("sddm") and hasattr(self, "sessions_sddm"):
            sddm.pop_box(self, self.sessions_sddm)
        if fn.check_package_installed("lightdm") and hasattr(self, "sessions_lightdm"):
            lightdm.pop_box_sessions_lightdm(self, self.sessions_lightdm)
        # terminal
        if fn.check_package_installed("termite") and hasattr(self, "term_themes"):
            terminals.get_themes(self.term_themes)
        # themes
        if fn.check_package_installed("arcolinux-leftwm-git") and hasattr(self, "term_themes"):
            terminals.get_themes(self.term_themes)
        # populate all cursors dropdowns
        if fn.check_package_installed("sddm") and hasattr(self, "sddm_cursor_themes"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm") and hasattr(self, "cursor_themes_lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)
        # populate cursor themes - some themes include a cursor
        if fn.check_package_installed("sddm") and hasattr(self, "sddm_cursor_themes"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        if fn.check_package_installed("lightdm") and hasattr(self, "cursor_themes_lightdm"):
            lightdm.pop_gtk_cursor_names(self, self.cursor_themes_lightdm)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)
        # populate lightdm page
        if fn.check_package_installed("lightdm") and hasattr(self, "gtk_theme_names_lightdm"):
            lightdm.pop_gtk_theme_names_lightdm(self, self.gtk_theme_names_lightdm)
        # populate lxdm page
        if fn.check_package_installed("lxdm") and hasattr(self, "lxdm_gtk_theme"):
            lxdm.pop_gtk_theme_names_lxdm(self.lxdm_gtk_theme)
        print("Reloaded")

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
            gtk_theme = os.environ.get("GTK_THEME")
            if not gtk_theme:
                try:
                    with open("/etc/environment", "r", encoding="utf-8") as _f:
                        for _line in _f:
                            _line = _line.strip()
                            if _line.startswith("GTK_THEME="):
                                gtk_theme = _line.split("=", 1)[1].strip()
                                break
                except Exception:
                    pass
            if gtk_theme:
                Gtk.Settings.get_default().set_property("gtk-theme-name", gtk_theme)

            style_provider = Gtk.CssProvider()
            style_provider.load_from_path(base_dir + "/att.css")
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
