# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
from gi.repository import GLib


def tobash_apply(self, _widget):
    fn.change_shell(self, "bash")


def _refresh_bash_completion_label(self):
    if fn.check_package_installed("bash-completion"):
        fn.GLib.idle_add(self.bash_completion_lbl.set_markup,
                         "Bash and bash-completion are already <b>installed</b>")
    else:
        fn.GLib.idle_add(self.bash_completion_lbl.set_markup,
                         "Bash is already installed and bash-completion is not installed")


def on_install_bash_completion_clicked(self, _widget):
    fn.log_subsection("Installing bash and bash-completion...")
    process = fn.launch_pacman_install_in_terminal("bash bash-completion")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "Installation started")

    def wait_install():
        try:
            process.wait()
            fn.log_success("Installation completed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "bash and bash-completion installed")
            _refresh_bash_completion_label(self)
        except Exception as e:
            fn.log_error(f"Error: {e}")

    fn.threading.Thread(target=wait_install, daemon=True).start()


def on_remove_bash_completion_clicked(self, _widget):
    fn.log_subsection("Removing bash-completion...")
    process = fn.launch_pacman_remove_in_terminal("bash-completion")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "Removal started")

    def wait_remove():
        try:
            process.wait()
            fn.log_success("bash-completion removed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "bash-completion removed")
            _refresh_bash_completion_label(self)
        except Exception as e:
            fn.log_error(f"Error: {e}")

    fn.threading.Thread(target=wait_remove, daemon=True).start()


def on_arcolinux_bash_clicked(self, _widget):
    fn.log_subsection("Apply ATT Bash Configuration")
    fn.debug_print(f"  Source : {fn.bashrc_kiro}")
    fn.debug_print(f"  Target : {fn.bash_config}")
    fn.debug_print(f"  Exists : {fn.path.isfile(fn.bashrc_kiro)}")
    try:
        if fn.path.isfile(fn.bashrc_kiro):
            fn.shutil.copy(fn.bashrc_kiro, fn.bash_config)
            fn.debug_print("  Result : copied successfully")
            fn.permissions(fn.home + "/.bashrc")
            fn.debug_print(f"  Perms  : permissions set on {fn.bash_config}")
            fn.log_success("ATT bash configuration applied - open a new terminal to activate")
            GLib.idle_add(fn.show_in_app_notification, self, "ATT ~/.bashrc applied - open new terminal")
        else:
            fn.debug_print("  Result : source file not found - nothing copied")
            fn.log_warn("ATT bashrc not found - add .bashrc to data/")
    except Exception as error:
        fn.debug_print(f"  Result : FAILED - {error}")
        fn.log_error(f"Failed to apply ATT bash configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to apply bash configuration: {error}")


def on_bash_reset_clicked(self, _widget):
    fn.log_subsection("Restore Original Bash Configuration")
    backup = fn.bash_config + ".bak"
    fn.debug_print(f"  Source : {backup}")
    fn.debug_print(f"  Target : {fn.bash_config}")
    fn.debug_print(f"  Exists : {fn.path.isfile(backup)}")
    try:
        if fn.path.isfile(backup):
            fn.shutil.copy(backup, fn.bash_config)
            fn.debug_print("  Result : copied successfully")
            fn.permissions(fn.home + "/.bashrc")
            fn.debug_print(f"  Perms  : permissions set on {fn.bash_config}")
        else:
            fn.debug_print("  Result : no backup found - nothing restored")
        fn.log_success("Original bash configuration restored - please logout")
        GLib.idle_add(fn.show_in_app_notification, self, "Your personal ~/.bashrc is applied again - logout")
    except Exception as error:
        fn.debug_print(f"  Result : FAILED - {error}")
        fn.log_error(f"Failed to restore bash configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to restore bash configuration: {error}")


def on_arcolinux_fish_package_clicked(self, _widget):
    """Install fish shell from ArcoLinux package"""
    fn.install_package(self, "fish")
    fn.show_in_app_notification(self, "Fish shell installed")


def on_arcolinux_only_fish_clicked(self, _widget):
    """Set fish as default shell"""
    import subprocess
    subprocess.run(['chsh', '-s', '/usr/bin/fish'], check=False)
    fn.show_in_app_notification(self, "Fish set as default shell")


def on_fish_reset_clicked(self, _widget):
    """Reset fish configuration"""
    fish_config_dir = fn.os.path.expanduser("~/.config/fish")
    if fn.path.exists(fish_config_dir):
        fn.shutil.rmtree(fish_config_dir)
    fn.show_in_app_notification(self, "Fish configuration reset")


def on_install_only_fish_clicked(self, _widget):
    """Install fish shell only"""
    fn.install_package(self, "fish")


def on_install_only_fish_clicked_reboot(self, _widget):
    """Install fish shell and reboot"""
    fn.install_package(self, "fish")
    fn.restart_program()


def on_remove_fish_all(self, _widget):
    """Remove fish shell completely"""
    if not fn.check_package_installed("fish"):
        fn.log_info("fish is not installed")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "fish is not installed")
        return
    fn.log_subsection("Removing fish...")
    process = fn.launch_pacman_remove_in_terminal("fish")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "Removal started")

    def wait_remove():
        try:
            process.wait()
            fn.log_success("fish removed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "fish removed")
        except Exception as e:
            fn.log_error(f"Error: {e}")

    fn.threading.Thread(target=wait_remove, daemon=True).start()


def on_remove_only_fish_clicked(self, _widget):
    """Remove fish shell"""
    if not fn.check_package_installed("fish"):
        fn.log_info("fish is not installed")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "fish is not installed")
        return
    fn.log_subsection("Removing fish...")
    process = fn.launch_pacman_remove_in_terminal("fish")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "Removal started")

    def wait_remove():
        try:
            process.wait()
            fn.log_success("fish removed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "fish removed")
        except Exception as e:
            fn.log_error(f"Error: {e}")

    fn.threading.Thread(target=wait_remove, daemon=True).start()


def tofish_apply(self, _widget):
    fn.change_shell(self, "fish")


def tooltip_callback(self, _widget, x, y, keyboard_mode, tooltip, text):
    tooltip.set_text(text)
    return True


def on_arcolinux_zshrc_clicked(self, _widget):
    fn.log_subsection("Apply ATT Zsh Configuration")
    fn.debug_print(f"  Source : {fn.zshrc_kiro}")
    fn.debug_print(f"  Target : {fn.zsh_config}")
    fn.debug_print(f"  Exists : {fn.path.isfile(fn.zshrc_kiro)}")
    try:
        if fn.path.isfile(fn.zshrc_kiro):
            fn.shutil.copy(fn.zshrc_kiro, fn.zsh_config)
            fn.debug_print("  Result : copied successfully")
            fn.permissions(fn.home + "/.zshrc")
            fn.debug_print(f"  Perms  : permissions set on {fn.zsh_config}")
            fn.log_success("ATT zsh configuration applied - open a new terminal to activate")
            GLib.idle_add(fn.show_in_app_notification, self, "ATT ~/.zshrc applied - open new terminal")
        else:
            fn.debug_print("  Result : source file not found - nothing copied")
    except Exception as error:
        fn.debug_print(f"  Result : FAILED - {error}")
        fn.log_error(f"Failed to apply ATT zsh configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to apply zsh configuration: {error}")


def on_zshrc_reset_clicked(self, _widget):
    fn.log_subsection("Restore Original Zsh Configuration")
    backup = fn.zsh_config + ".bak"
    fn.debug_print(f"  Source : {backup}")
    fn.debug_print(f"  Target : {fn.zsh_config}")
    fn.debug_print(f"  Exists : {fn.path.isfile(backup)}")
    try:
        if fn.path.isfile(backup):
            fn.shutil.copy(backup, fn.zsh_config)
            fn.debug_print("  Result : copied successfully")
            fn.permissions(fn.home + "/.zshrc")
            fn.debug_print(f"  Perms  : permissions set on {fn.zsh_config}")
        else:
            fn.debug_print("  Result : no backup found - nothing restored")
        fn.log_success("Original zsh configuration restored - please logout")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Your personal ~/.zshrc is applied again - logout",
        )
    except Exception as error:
        fn.debug_print(f"  Result : FAILED - {error}")
        fn.log_error(f"Failed to restore zsh configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to restore zsh configuration: {error}")


def on_zsh_apply_theme(self, _widget):
    fn.log_subsection("Apply ATT Zsh Theme")
    try:
        # zsh_theme.set_att_checkboxes_zsh_all(self)
        fn.debug_print("Applying ATT zsh theme")
        fn.log_success("ATT zsh theme applied")
        fn.show_in_app_notification(self, "ATT zsh theme is applied")
    except Exception as error:
        fn.log_error(f"Failed to apply zsh theme: {error}")
        fn.messagebox(self, "Error", f"Failed to apply zsh theme: {error}")


def on_zsh_reset(self, _widget):
    fn.log_subsection("Reset Zsh Theme")
    try:
        fn.debug_print("Resetting zsh theme")
        # zsh_theme.set_att_checkboxes_zsh_none(self)
        fn.log_success("Zsh theme reset")
        fn.show_in_app_notification(self, "zsh theme is reset")
    except Exception as error:
        fn.log_error(f"Failed to reset zsh theme: {error}")
        fn.messagebox(self, "Error", f"Failed to reset zsh theme: {error}")


def tozsh_apply(self, _widget):
    fn.change_shell(self, "zsh")


def install_oh_my_zsh(self, _widget):
    if fn.check_package_installed("oh-my-zsh-git"):
        fn.debug_print("oh-my-zsh-git already installed")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "oh-my-zsh-git already installed")
        return
    aur_helper = fn.get_aur_helper()
    if aur_helper is None:
        fn.log_error("No AUR helper found (yay/paru). Install one first.")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "No AUR helper found — install yay or paru first")
        return
    fn.log_subsection("Installing oh-my-zsh-git...")
    fn.debug_print(f"AUR helper: {aur_helper}")
    process = fn.launch_aur_install_in_terminal(aur_helper, "oh-my-zsh-git")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "oh-my-zsh-git installation started")

    def wait_install():
        try:
            process.wait()
            fn.log_success("oh-my-zsh-git installed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "oh-my-zsh-git installed")
            fn.GLib.idle_add(_refresh_zsh_omz_lbl, self)
            fn.GLib.idle_add(_refresh_termset_sensitive, self)
        except Exception as e:
            fn.log_error(f"Error: {e}")

    fn.threading.Thread(target=wait_install, daemon=True).start()


def on_extra_shell_applications_clicked(self, _widget):
    fn.log_subsection("Install Extra Shell Applications")
    try:
        selected = []
        if self.expac.get_active():
            fn.debug_print("Installing expac")
            fn.install_package(self, "expac")
            selected.append("expac")
        if self.ripgrep.get_active():
            fn.debug_print("Installing ripgrep")
            fn.install_package(self, "ripgrep")
            selected.append("ripgrep")
        if self.yay.get_active():
            fn.debug_print("Installing yay-git")
            fn.install_package(self, "yay-git")
            selected.append("yay-git")
        if self.paru.get_active():
            fn.debug_print("Installing paru-git")
            fn.install_package(self, "paru-git")
            selected.append("paru-git")
        if self.bat.get_active():
            fn.debug_print("Installing bat")
            fn.install_package(self, "bat")
            selected.append("bat")
        if self.downgrade.get_active():
            fn.debug_print("Installing downgrade")
            fn.install_package(self, "downgrade")
            selected.append("downgrade")
        if self.hw_probe.get_active():
            fn.debug_print("Installing hw-probe")
            fn.install_package(self, "hw-probe")
            selected.append("hw-probe")
        if self.rate_mirrors.get_active():
            fn.debug_print("Installing rate-mirrors")
            fn.install_package(self, "rate-mirrors")
            selected.append("rate-mirrors")
        if self.most.get_active():
            fn.debug_print("Installing most")
            fn.install_package(self, "most")
            selected.append("most")

        fn.log_success("Software installed (availability depends on enabled repositories)")
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
    except Exception as error:
        fn.log_error(f"Failed to install shell applications: {error}")
        fn.messagebox(self, "Error", f"Failed to install applications: {error}")


def on_select_all_toggle(self, _widget, active):
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
# ADDITIONAL ZSH CALLBACKS
# ====================================================================


def on_clicked_install_only_zsh(self, _widget):
    fn.install_package(self, "zsh")
    fn.restart_program()


def _refresh_zsh_completions_lbl(self):
    if fn.check_package_installed("zsh-completions"):
        self.zsh_completions_lbl.set_markup("Zsh-completion is already <b>installed</b>")
    else:
        self.zsh_completions_lbl.set_markup("Zsh-completion is <b>not</b> installed")


def _refresh_zsh_syntax_lbl(self):
    if fn.check_package_installed("zsh-syntax-highlighting"):
        self.zsh_syntax_lbl.set_markup("Zsh-syntax-highlighting is already <b>installed</b>")
    else:
        self.zsh_syntax_lbl.set_markup("Zsh-syntax-highlighting is not installed")


def _refresh_zsh_omz_lbl(self):
    if fn.check_package_installed("oh-my-zsh-git"):
        self.zsh_omz_lbl.set_markup("Oh-my-zsh-git is already <b>installed</b>")
    else:
        self.zsh_omz_lbl.set_markup("Oh-my-zsh-git is not installed")


def _refresh_termset_sensitive(self):
    installed = fn.check_package_installed("oh-my-zsh-git")
    self.termset.set_sensitive(installed)
    self.zsh_themes.set_sensitive(installed)


def on_install_zsh_completions_clicked(self, _widget):
    if fn.check_package_installed("zsh-completions"):
        fn.debug_print("zsh-completions already installed")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "zsh-completions already installed")
        return
    fn.log_subsection("Installing zsh-completions...")
    process = fn.launch_pacman_install_in_terminal("zsh-completions")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "zsh-completions installation started")

    def wait_install():
        try:
            process.wait()
            fn.log_success("zsh-completions installed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "zsh-completions installed")
            fn.GLib.idle_add(_refresh_zsh_completions_lbl, self)
        except Exception as e:
            fn.log_error(f"Error: {e}")

    fn.threading.Thread(target=wait_install, daemon=True).start()


def on_remove_zsh_completions_clicked(self, _widget):
    if not fn.check_package_installed("zsh-completions"):
        fn.log_info("zsh-completions is not installed")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "zsh-completions is not installed")
        return
    fn.log_subsection("Removing zsh-completions...")
    process = fn.launch_pacman_remove_in_terminal("zsh-completions")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "Removal started")

    def wait_remove():
        try:
            process.wait()
            fn.log_success("zsh-completions removed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "zsh-completions removed")
            fn.GLib.idle_add(_refresh_zsh_completions_lbl, self)
        except Exception as e:
            fn.log_error(f"Error: {e}")

    fn.threading.Thread(target=wait_remove, daemon=True).start()


def on_install_zsh_syntax_highlighting_clicked(self, _widget):
    if fn.check_package_installed("zsh-syntax-highlighting"):
        fn.debug_print("zsh-syntax-highlighting already installed")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "zsh-syntax-highlighting already installed")
        return
    fn.log_subsection("Installing zsh-syntax-highlighting...")
    process = fn.launch_pacman_install_in_terminal("zsh-syntax-highlighting")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "zsh-syntax-highlighting installation started")

    def wait_install():
        try:
            process.wait()
            fn.log_success("zsh-syntax-highlighting installed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "zsh-syntax-highlighting installed")
            fn.GLib.idle_add(_refresh_zsh_syntax_lbl, self)
        except Exception as e:
            fn.log_error(f"Error: {e}")

    fn.threading.Thread(target=wait_install, daemon=True).start()


def on_remove_zsh_syntax_highlighting_clicked(self, _widget):
    if not fn.check_package_installed("zsh-syntax-highlighting"):
        fn.log_info("zsh-syntax-highlighting is not installed")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "zsh-syntax-highlighting is not installed")
        return
    fn.log_subsection("Removing zsh-syntax-highlighting...")
    process = fn.launch_pacman_remove_in_terminal("zsh-syntax-highlighting")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "Removal started")

    def wait_remove():
        try:
            process.wait()
            fn.log_success("zsh-syntax-highlighting removed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "zsh-syntax-highlighting removed")
            fn.GLib.idle_add(_refresh_zsh_syntax_lbl, self)
        except Exception as e:
            fn.log_error(f"Error: {e}")

    fn.threading.Thread(target=wait_remove, daemon=True).start()


def on_arcolinux_zshrc_clicked_dup(self, _widget):
    fn.log_subsection("Apply ATT Zsh Configuration")
    try:
        if fn.path.isfile(fn.zshrc_kiro):
            fn.debug_print(f"Copying ATT zshrc from {fn.zshrc_kiro}")
            fn.shutil.copy(fn.zshrc_kiro, fn.zsh_config)
            fn.debug_print(f"Setting permissions on {fn.home}/.zshrc")
            fn.permissions(fn.home + "/.zshrc")
        fn.debug_print("Sourcing shell configuration")
        fn.source_shell(self)
        fn.log_success("ATT zsh configuration applied")
        from gi.repository import GLib
        GLib.idle_add(fn.show_in_app_notification, self, "ATT ~/.zshrc is applied")
    except Exception as error:
        fn.log_error(f"Failed to apply ATT zsh configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to apply zsh configuration: {error}")


def on_zshrc_reset_clicked_dup(self, _widget):
    fn.log_subsection("Restore Original Zsh Configuration")
    try:
        if fn.path.isfile(fn.zsh_config + ".bak"):
            fn.debug_print("Restoring zshrc from backup")
            fn.shutil.copy(fn.zsh_config + ".bak", fn.zsh_config)
            fn.debug_print(f"Setting permissions on {fn.home}/.zshrc")
            fn.permissions(fn.home + "/.zshrc")
        fn.log_success("Original zsh configuration restored - please logout")
        from gi.repository import GLib
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Your personal ~/.zshrc is applied again - logout",
        )
    except Exception as error:
        fn.log_error(f"Failed to restore zsh configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to restore zsh configuration: {error}")


def on_zsh_reset_full(self, _widget):
    fn.log_subsection("Reset Zsh Configuration")
    try:
        if fn.path.isfile(fn.zsh_config + ".bak"):
            fn.debug_print("Restoring zshrc from backup")
            fn.shutil.copy(fn.zsh_config + ".bak", fn.zsh_config)
            fn.permissions(fn.home + "/.zshrc")
            fn.permissions(fn.home + "/.zshrc.bak")
            fn.log_success("Backup configuration applied")
            fn.show_in_app_notification(self, "Default settings applied")
        else:
            fn.debug_print("Applying default ATT zshrc")
            fn.shutil.copy(
                "/usr/share/archlinux-tweak-tool/data/.zshrc", fn.home + "/.zshrc"
            )
            fn.permissions(fn.home + "/.zshrc")
            fn.log_success("Default zshrc applied")
            fn.show_in_app_notification(self, "Valid ~/.zshrc applied")
    except Exception as error:
        fn.log_error(f"Failed to reset zsh configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to reset zsh configuration: {error}")


def remove_oh_my_zsh(self, _widget):
    if not fn.check_package_installed("oh-my-zsh-git"):
        fn.log_info("oh-my-zsh-git is not installed")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "oh-my-zsh-git is not installed")
        return
    fn.log_subsection("Removing oh-my-zsh-git...")
    process = fn.launch_pacman_remove_in_terminal("oh-my-zsh-git")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "Removal started")

    def wait_remove():
        try:
            process.wait()
            fn.log_success("oh-my-zsh-git removed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "oh-my-zsh-git removed")
            fn.GLib.idle_add(_refresh_zsh_omz_lbl, self)
            fn.GLib.idle_add(_refresh_termset_sensitive, self)
            from zsh_theme import get_themes
            fn.GLib.idle_add(get_themes, self.zsh_themes)
            fn.GLib.idle_add(self.zsh_themes.set_sensitive, False)
        except Exception as e:
            fn.log_error(f"Error: {e}")

    fn.threading.Thread(target=wait_remove, daemon=True).start()
