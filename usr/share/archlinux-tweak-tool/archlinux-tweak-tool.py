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
    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       AI TOOLS
    # ====================================================================
    # ====================================================================
    # ====================================================================
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
        try:
            fn.subprocess.Popen(f"sudo -u {fn.sudo_username} DISPLAY=:0 xdg-open '{url}'", shell=True, stdout=fn.subprocess.DEVNULL, stderr=fn.subprocess.DEVNULL)
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
    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       AUTOSTART
    # ====================================================================
    # ====================================================================
    # ====================================================================
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
    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       DESIGN
    # ====================================================================
    # ====================================================================
    # ====================================================================
    # ====================================================================

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
        print("We show the installed icon themes")
        fn.show_in_app_notification(self, "We show the installed icon themes")
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
        print("We show the installed cursor themes")
        fn.show_in_app_notification(self, "We show the installed cursor themes")
        # populate cursor themes
        if fn.check_package_installed("sddm"):
            sddm.pop_gtk_cursor_names(self, self.sddm_cursor_themes)
        maintenance.pop_gtk_cursor_names(self.cursor_themes)

    # fonts
    def on_install_fonts_clicked(self, widget):
        design.install_fonts(self)

    def on_remove_fonts_clicked(self, widget):
        design.remove_fonts(self)

    def on_find_fonts_clicked(self, widget):
        design.find_fonts(self)

    def on_click_theming_all_selection(self, widget):
        design.set_checkboxes_all(self)

    def on_click_theming_normal_selection(self, widget):
        design.set_checkboxes_normal(self)

    def on_click_theming_minimal_selection(self, widget):
        design.set_checkboxes_minimal(self)

    def on_click_theming_none_selection(self, widget):
        design.set_checkboxes_none(self)

    def on_click_icon_theming_all_selection(self, widget):
        design.set_checkboxes_all_icon(self)

    def on_click_icon_theming_normal_selection(self, widget):
        design.set_checkboxes_normal_icon(self)

    def on_click_icon_theming_minimal_selection(self, widget):
        design.set_checkboxes_minimal_icon(self)

    def on_click_icon_theming_none_selection(self, widget):
        design.set_checkboxes_none_icon(self)

    def on_click_cursor_theming_all_selection(self, widget):
        design.set_checkboxes_all_cursors(self)

    def on_click_cursor_theming_normal_selection(self, widget):
        design.set_checkboxes_normal_cursors(self)

    def on_click_cursor_theming_minimal_selection(self, widget):
        design.set_checkboxes_minimal_cursors(self)

    def on_click_cursor_theming_none_selection(self, widget):
        design.set_checkboxes_none_cursors(self)

    def on_click_font_theming_all_selection(self, widget):
        design.set_checkboxes_all_fonts(self)

    def on_click_font_theming_normal_selection(self, widget):
        design.set_checkboxes_normal_fonts(self)

    def on_click_font_theming_minimal_selection(self, widget):
        design.set_checkboxes_minimal_fonts(self)

    def on_click_font_theming_none_selection(self, widget):
        design.set_checkboxes_none_fonts(self)

    # ====================================================================
    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       DESKTOPR
    # ====================================================================
    # ====================================================================
    # ====================================================================
    # ====================================================================

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

    # ====================================================================
    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       FASTFETCH
    # ====================================================================
    # ====================================================================
    # ====================================================================
    # ====================================================================

    def on_install_fast(self, widget):
        fn.install_package(self, "fastfetch-git")

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

    # ====================================================================
    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       ICONS
    # ====================================================================
    # ====================================================================
    # ====================================================================
    # ====================================================================

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
    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       KERNEL
    # ====================================================================
    # ====================================================================
    # ====================================================================
    # ====================================================================
    
    # Programming logic is in kernel.py

    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       LOGGING
    # ====================================================================
    # ====================================================================
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
    # ====================================================================
    # ====================================================================
    #                       MAINTENANCE
    # ====================================================================
    # All MAINTENANCE callbacks have been extracted to maintenance.py
    # See: maintenance.py for implementation

    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       PACKAGES
    # ====================================================================
    # All PACKAGES callbacks have been extracted to packages.py
    # See: packages.py for implementation
    # ====================================================================

    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       PRIVACY
    # ====================================================================
    # ====================================================================
    # ====================================================================

    def set_hblock(self, widget, state):
        import subprocess
        if state:
            result = subprocess.run(['sudo', 'systemctl', 'start', 'hblock'], capture_output=True)
            if result.returncode == 0:
                fn.show_in_app_notification(self, "hblock enabled")
            else:
                fn.show_in_app_notification(self, "Failed to enable hblock")
        else:
            subprocess.run(['sudo', 'systemctl', 'stop', 'hblock'], capture_output=True)
            fn.show_in_app_notification(self, "hblock disabled")

    def set_ublock_firefox(self, widget, state):
        """Toggle uBlock Origin in Firefox"""
        import subprocess
        firefox_extensions_dir = fn.os.path.expanduser("~/.mozilla/firefox")

        if state:
            fn.show_in_app_notification(self, "Installing uBlock Origin in Firefox")
            # uBlock Origin installation logic
        else:
            fn.show_in_app_notification(self, "Disabling uBlock Origin in Firefox")


    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       SDDM
    # ====================================================================
    # ====================================================================
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
        if not sddm.ensure_sddm_config(self):
            return

        try:
            fn.shutil.copy(fn.sddm_default_d1_kiro, fn.sddm_default_d1)
            fn.shutil.copy(fn.sddm_default_d2_kiro, fn.sddm_default_d2)
        except Exception as error:
            print(error)
            fn.messagebox(self, "Error", f"Failed to apply SDDM configuration: {error}")
            return

        print("The ATT sddm configuration is now applied")
        print(
            "Both files have been changed /etc/sddm.conf and /etc/sddm.conf.d/kde_settings.conf"
        )
        fn.show_in_app_notification(
            self, "The ATT sddm.conf and sddm.d.conf is now applied"
        )
        fn.restart_program()

    def on_click_sddm_reset_original(self, widget):
        if not fn.path.isfile(fn.sddm_default_d1_bak) or not fn.path.isfile(fn.sddm_default_d2_bak):
            fn.messagebox(
                self,
                "Backup Not Found",
                "No backup of your original SDDM configuration was found.\n\n"
                "Backups are created automatically when SDDM configuration is first modified.\n\n"
                "You can apply the default ATT SDDM configuration instead."
            )
            return

        fn.create_sddm_k_dir()
        try:
            if fn.path.isfile(fn.sddm_default_d1_bak):
                fn.shutil.copy(fn.sddm_default_d1_bak, fn.sddm_default_d1)
            if fn.path.isfile(fn.sddm_default_d2_bak):
                fn.shutil.copy(fn.sddm_default_d2_bak, fn.sddm_default_d2)
        except Exception as error:
            print(error)
            fn.messagebox(self, "Error", f"Failed to restore SDDM configuration: {error}")
            return

        print("Your original sddm configuration is now applied")
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
    # ====================================================================
    # ====================================================================
    #                       SERVICES - AUDIO
    # ====================================================================
    # ====================================================================
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
    # ====================================================================
    # ====================================================================
    #                       SERVICES - BLUETOOTH
    # ====================================================================
    # ====================================================================
    # ====================================================================

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
    # ====================================================================
    # ====================================================================
    #                       SERVICES - CUPS
    # ====================================================================
    # ====================================================================
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
    # ====================================================================
    # ====================================================================
    #                       SERVICES - NSSWITCH
    # ====================================================================
    # ====================================================================
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
    # ====================================================================
    # ====================================================================
    #                       SERVICES - SAMBA
    # ====================================================================
    # ====================================================================
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
    # ====================================================================
    # ====================================================================
    #                       SHELLS
    # ====================================================================
    # ====================================================================
    # ====================================================================

    # BASH

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

    # FISH

    def on_arcolinux_fish_package_clicked(self, widget):
        """Install fish shell from ArcoLinux package"""
        fn.install_package(self, "fish")
        fn.show_in_app_notification(self, "Fish shell installed")

    def on_arcolinux_only_fish_clicked(self, widget):
        """Set fish as default shell"""
        import subprocess
        subprocess.run(['chsh', '-s', '/usr/bin/fish'], check=False)
        fn.show_in_app_notification(self, "Fish set as default shell")

    def on_fish_reset_clicked(self, widget):
        """Reset fish configuration"""
        fish_config_dir = fn.os.path.expanduser("~/.config/fish")
        if fn.path.exists(fish_config_dir):
            fn.shutil.rmtree(fish_config_dir)
        fn.show_in_app_notification(self, "Fish configuration reset")

    def on_install_only_fish_clicked(self, widget):
        """Install fish shell only"""
        fn.install_package(self, "fish")

    def on_install_only_fish_clicked_reboot(self, widget):
        """Install fish shell and reboot"""
        fn.install_package(self, "fish")
        fn.restart_program()

    def on_remove_fish_all(self, widget):
        """Remove fish shell completely"""
        fn.uninstall_package(self, "fish")
        fn.show_in_app_notification(self, "Fish shell removed")

    def on_remove_only_fish_clicked(self, widget):
        """Remove fish shell"""
        fn.uninstall_package(self, "fish")

    def tofish_apply(self, widget):
        """Apply fish shell configuration"""
        fn.show_in_app_notification(self, "Fish configuration applied")

    def tooltip_callback(self, widget, x, y, keyboard_mode, tooltip, text):
        tooltip.set_text(text)
        return True

    # ZSH

    def on_clicked_install_only_zsh(self, widget):
        fn.install_package(self, "zsh")

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
        zsh_theme.set_att_checkboxes_zsh_all(self)
        print("[INFO] ATT zsh theme is applied")
        fn.show_in_app_notification(self, "ATT zsh theme is applied")

    def on_zsh_reset(self, widget):
        print("[INFO] zsh theme is reset")
        fn.show_in_app_notification(self, "zsh theme is reset")
        zsh_theme.set_att_checkboxes_zsh_none(self)

    def tozsh_apply(self, widget):
        fn.change_shell(self, "zsh")

    def install_oh_my_zsh(self, widget):
        import subprocess
        print("[INFO] Installing Oh My Zsh")
        fn.show_in_app_notification(self, "Installing Oh My Zsh")
        try:
            result = subprocess.run(
                ["bash", "-c", "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"],
                check=False
            )
            if result.returncode == 0:
                print("[INFO] Oh My Zsh installed successfully")
                fn.show_in_app_notification(self, "Oh My Zsh installed successfully")
            else:
                print("[ERROR] Failed to install Oh My Zsh")
                fn.show_in_app_notification(self, "Failed to install Oh My Zsh")
        except Exception as error:
            print(f"[ERROR] {error}")
            fn.show_in_app_notification(self, f"Error: {error}")

    def remove_oh_my_zsh(self, widget):
        fn.remove_package(self, "oh-my-zsh-git")
        zsh_theme.get_themes(self.zsh_themes)
        self.termset.set_sensitive(False)
        self.zsh_themes.set_sensitive(False)

    # SHELL EXTRA

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


    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       SYSTEM
    # ====================================================================
    # ====================================================================
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
    # ====================================================================
    # ====================================================================
    #                       TERMINALS
    # ====================================================================
    # ====================================================================
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
    # ====================================================================
    # ====================================================================
    #                       THEMER FUNCTIONS
    # ====================================================================
    # ====================================================================
    # ====================================================================

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
    # ====================================================================
    # ====================================================================
    #                       THEMES
    # ====================================================================
    # ====================================================================
    # ====================================================================

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


    # ====================================================================
    # ====================================================================
    # ====================================================================
    #                       USER
    # ====================================================================
    # ====================================================================
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
