# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
from gi.repository import GLib


def tobash_apply(self, widget):
    fn.change_shell(self, "bash")


def on_install_bash_completion_clicked(self, widget):
    fn.log_subsection("Installing bash and bash-completion...")
    process = fn.launch_pacman_install_in_terminal("bash bash-completion")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "Installation started")

    def wait_install():
        try:
            process.wait()
            fn.log_success("Installation completed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "bash and bash-completion installed")
        except Exception as e:
            fn.log_error(f"Error: {e}")

    fn.threading.Thread(target=wait_install, daemon=True).start()


def on_remove_bash_completion_clicked(self, widget):
    fn.remove_package(self, "bash-completion")


def on_arcolinux_bash_clicked(self, widget):
    fn.log_subsection("Apply ATT Bash Configuration")
    try:
        if fn.path.isfile(fn.bashrc_arco):
            fn.debug_print(f"Copying ATT bashrc from {fn.bashrc_arco}")
            fn.shutil.copy(fn.bashrc_arco, fn.bash_config)
            fn.debug_print(f"Setting permissions on {fn.home}/.bashrc")
            fn.permissions(fn.home + "/.bashrc")
        fn.debug_print("Sourcing shell configuration")
        fn.source_shell(self)
        fn.log_success("ATT bash configuration applied")
        GLib.idle_add(fn.show_in_app_notification, self, "ATT ~/.bashrc is applied")
    except Exception as error:
        fn.log_error(f"Failed to apply ATT bash configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to apply bash configuration: {error}")


def on_bash_reset_clicked(self, widget):
    fn.log_subsection("Restore Original Bash Configuration")
    try:
        if fn.path.isfile(fn.bash_config + ".bak"):
            fn.debug_print(f"Restoring bashrc from backup")
            fn.shutil.copy(fn.bash_config + ".bak", fn.bash_config)
            fn.debug_print(f"Setting permissions on {fn.home}/.bashrc")
            fn.permissions(fn.home + "/.bashrc")
        fn.log_success("Original bash configuration restored - please logout")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Your personal ~/.bashrc is applied again - logout",
        )
    except Exception as error:
        fn.log_error(f"Failed to restore bash configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to restore bash configuration: {error}")


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
    fn.log_subsection("Apply ATT Zsh Configuration")
    try:
        if fn.path.isfile(fn.zshrc_arco):
            fn.debug_print(f"Copying ATT zshrc from {fn.zshrc_arco}")
            fn.shutil.copy(fn.zshrc_arco, fn.zsh_config)
            fn.debug_print(f"Setting permissions on {fn.home}/.zshrc")
            fn.permissions(fn.home + "/.zshrc")
        fn.debug_print("Sourcing shell configuration")
        fn.source_shell(self)
        fn.log_success("ATT zsh configuration applied")
        GLib.idle_add(fn.show_in_app_notification, self, "ATT ~/.zshrc is applied")
    except Exception as error:
        fn.log_error(f"Failed to apply ATT zsh configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to apply zsh configuration: {error}")


def on_zshrc_reset_clicked(self, widget):
    fn.log_subsection("Restore Original Zsh Configuration")
    try:
        if fn.path.isfile(fn.zsh_config + ".bak"):
            fn.debug_print(f"Restoring zshrc from backup")
            fn.shutil.copy(fn.zsh_config + ".bak", fn.zsh_config)
            fn.debug_print(f"Setting permissions on {fn.home}/.zshrc")
            fn.permissions(fn.home + "/.zshrc")
        fn.log_success("Original zsh configuration restored - please logout")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Your personal ~/.zshrc is applied again - logout",
        )
    except Exception as error:
        fn.log_error(f"Failed to restore zsh configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to restore zsh configuration: {error}")


def on_zsh_apply_theme(self, widget):
    fn.log_subsection("Apply ATT Zsh Theme")
    try:
        # zsh_theme.set_att_checkboxes_zsh_all(self)
        fn.debug_print("Applying ATT zsh theme")
        fn.log_success("ATT zsh theme applied")
        fn.show_in_app_notification(self, "ATT zsh theme is applied")
    except Exception as error:
        fn.log_error(f"Failed to apply zsh theme: {error}")
        fn.messagebox(self, "Error", f"Failed to apply zsh theme: {error}")


def on_zsh_reset(self, widget):
    fn.log_subsection("Reset Zsh Theme")
    try:
        fn.debug_print("Resetting zsh theme")
        # zsh_theme.set_att_checkboxes_zsh_none(self)
        fn.log_success("Zsh theme reset")
        fn.show_in_app_notification(self, "zsh theme is reset")
    except Exception as error:
        fn.log_error(f"Failed to reset zsh theme: {error}")
        fn.messagebox(self, "Error", f"Failed to reset zsh theme: {error}")


def tozsh_apply(self, widget):
    fn.change_shell(self, "zsh")


def install_oh_my_zsh(self, widget):
    fn.log_subsection("Install Oh My Zsh")
    import subprocess
    try:
        fn.debug_print("Downloading Oh My Zsh from GitHub")
        fn.show_in_app_notification(self, "Installing Oh My Zsh")
        result = subprocess.run(
            ["bash", "-c", "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"],
            check=False
        )
        if result.returncode == 0:
            fn.log_success("Oh My Zsh installed successfully")
            fn.show_in_app_notification(self, "Oh My Zsh installed successfully")
        else:
            fn.log_error("Failed to install Oh My Zsh - check network connection")
            fn.show_in_app_notification(self, "Failed to install Oh My Zsh")
    except Exception as error:
        fn.log_error(f"Failed to install Oh My Zsh: {error}")
        fn.show_in_app_notification(self, f"Error: {error}")


def remove_oh_my_zsh(self, widget):
    fn.remove_package(self, "oh-my-zsh-git")
    # zsh_theme.get_themes(self.zsh_themes)
    self.termset.set_sensitive(False)
    self.zsh_themes.set_sensitive(False)


def on_extra_shell_applications_clicked(self, widget):
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

        fn.log_success(f"Software installed (availability depends on enabled repositories)")
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
# ADDITIONAL ZSH CALLBACKS
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


def on_arcolinux_zshrc_clicked_dup(self, widget):
    fn.log_subsection("Apply ATT Zsh Configuration")
    try:
        if fn.path.isfile(fn.zshrc_arco):
            fn.debug_print(f"Copying ATT zshrc from {fn.zshrc_arco}")
            fn.shutil.copy(fn.zshrc_arco, fn.zsh_config)
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


def on_zshrc_reset_clicked_dup(self, widget):
    fn.log_subsection("Restore Original Zsh Configuration")
    try:
        if fn.path.isfile(fn.zsh_config + ".bak"):
            fn.debug_print(f"Restoring zshrc from backup")
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


def on_zsh_reset_full(self, widget):
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
                "/usr/share/archlinux-tweak-tool/data/arco/.zshrc", fn.home + "/.zshrc"
            )
            fn.permissions(fn.home + "/.zshrc")
            fn.log_success("Default zshrc applied")
            fn.show_in_app_notification(self, "Valid ~/.zshrc applied")
    except Exception as error:
        fn.log_error(f"Failed to reset zsh configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to reset zsh configuration: {error}")


def remove_oh_my_zsh(self, widget):
    fn.remove_package(self, "oh-my-zsh-git")
    from zsh_theme import get_themes
    get_themes(self.zsh_themes)
    self.termset.set_sensitive(False)
    self.zsh_themes.set_sensitive(False)
