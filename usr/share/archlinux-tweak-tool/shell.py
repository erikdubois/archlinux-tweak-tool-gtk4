# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
import zsh_theme
from gi.repository import GLib


def tobash_apply(self, _widget):
    fn.log_subsection("Apply Bash")
    fn.debug_print(f"  Current shell : {fn.get_shell()}")
    fn.debug_print("  Target shell  : bash")
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


def on_install_att_bashrc_clicked(self, _widget):
    fn.log_subsection("Apply ATT Bash Configuration")
    fn.debug_print(f"  Source : {fn.bashrc_kiro}")
    fn.debug_print(f"  Target : {fn.bash_config}")
    fn.debug_print(f"  Exists : {fn.path.isfile(fn.bashrc_kiro)}")
    try:
        if fn.path.isfile(fn.bashrc_kiro):
            fn.log_info_concise(f"  From: {fn.bashrc_kiro}")
            fn.log_info_concise(f"  To:   {fn.bash_config}")
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
            fn.log_info_concise(f"  From: {backup}")
            fn.log_info_concise(f"  To:   {fn.bash_config}")
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


def on_install_att_fish_config_clicked(self, _widget):
    fn.log_subsection("Apply ATT Fish Configuration")
    fn.debug_print(f"  Source : {fn.fish_config_kiro}")
    fn.debug_print(f"  Target : {fn.fish_config}")
    fn.debug_print(f"  Exists : {fn.path.isfile(fn.fish_config_kiro)}")
    try:
        if fn.path.isfile(fn.fish_config_kiro):
            fn.os.makedirs(fn.os.path.dirname(fn.fish_config), exist_ok=True)
            if fn.path.isfile(fn.fish_config):
                fn.log_info_concise(f"  From: {fn.fish_config}")
                fn.log_info_concise(f"  To:   {fn.fish_config}.bak")
                fn.shutil.copy(fn.fish_config, fn.fish_config + ".bak")
            fn.log_info_concise(f"  From: {fn.fish_config_kiro}")
            fn.log_info_concise(f"  To:   {fn.fish_config}")
            fn.shutil.copy(fn.fish_config_kiro, fn.fish_config)
            fn.debug_print("  Result : copied successfully")
            fn.permissions(fn.os.path.dirname(fn.fish_config))
            fn.debug_print(f"  Perms  : permissions set on {fn.os.path.dirname(fn.fish_config)}")
            fn.log_success("ATT fish configuration applied - open a new terminal to activate")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "ATT config.fish applied - open new terminal")
        else:
            fn.debug_print("  Result : source file not found - nothing copied")
            fn.log_warn("ATT config.fish source not found")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "ATT config.fish source not found")
    except Exception as error:
        fn.debug_print(f"  Result : FAILED - {error}")
        fn.log_error(f"Failed to apply ATT fish configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to apply fish configuration: {error}")


def on_fish_reset_clicked(self, _widget):
    fn.log_subsection("Restore Original Fish Configuration")
    backup = fn.fish_config + ".bak"
    fn.debug_print(f"  Source : {backup}")
    fn.debug_print(f"  Target : {fn.fish_config}")
    fn.debug_print(f"  Exists : {fn.path.isfile(backup)}")
    try:
        if fn.path.isfile(backup):
            fn.log_info_concise(f"  From: {backup}")
            fn.log_info_concise(f"  To:   {fn.fish_config}")
            fn.shutil.copy(backup, fn.fish_config)
            fn.debug_print("  Result : copied successfully")
            fn.permissions(fn.fish_config)
            fn.debug_print(f"  Perms  : permissions set on {fn.fish_config}")
        else:
            fn.debug_print("  Result : no backup found - nothing restored")
        fn.log_success("Original fish configuration restored - please logout")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "Your personal config.fish is applied again - logout")
    except Exception as error:
        fn.debug_print(f"  Result : FAILED - {error}")
        fn.log_error(f"Failed to restore fish configuration: {error}")
        fn.messagebox(self, "Error", f"Failed to restore fish configuration: {error}")


def on_install_only_fish_clicked(self, _widget):
    fn.log_subsection("Install Fish")
    fn.debug_print("  Package  : fish")
    fn.debug_print(f"  Installed: {fn.check_package_installed('fish')}")
    if fn.check_package_installed("fish"):
        fn.log_info("Fish is already installed")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "Fish is already installed")
        return
    fn.install_package(self, "fish")


def on_install_only_fish_clicked_reboot(self, _widget):
    fn.log_subsection("Install Fish")
    fn.debug_print("  Package  : fish")
    fn.debug_print(f"  Installed: {fn.check_package_installed('fish')}")
    fn.debug_print("  Reboot   : ATT will restart after install")
    if fn.check_package_installed("fish"):
        fn.log_info("Fish is already installed")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "Fish is already installed")
        return
    fn.install_package(self, "fish")
    fn.restart_program()


def on_remove_fish_all(self, _widget):
    fn.log_subsection("Remove All Fish Packages")
    fn.debug_print("  Package  : fish")
    fn.debug_print(f"  Installed: {fn.check_package_installed('fish')}")
    if not fn.check_package_installed("fish"):
        fn.log_info("fish is not installed")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "Fish is not installed")
        return
    process = fn.launch_pacman_remove_in_terminal("fish")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "Removing fish - terminal opened")

    def wait_remove():
        try:
            process.wait()
            fn.log_success("Fish removed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "Fish removed")
        except Exception as error:
            fn.log_error(f"Failed to remove fish: {error}")

    fn.threading.Thread(target=wait_remove, daemon=True).start()


def on_remove_only_fish_clicked(self, _widget):
    fn.log_subsection("Remove Fish")
    fn.debug_print("  Package  : fish")
    fn.debug_print(f"  Installed: {fn.check_package_installed('fish')}")
    if not fn.check_package_installed("fish"):
        fn.log_info("fish is not installed")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "Fish is not installed")
        return
    process = fn.launch_pacman_remove_in_terminal("fish")
    fn.GLib.idle_add(fn.show_in_app_notification, self, "Removing fish - terminal opened")

    def wait_remove():
        try:
            process.wait()
            fn.log_success("Fish removed")
            fn.GLib.idle_add(fn.show_in_app_notification, self, "Fish removed")
        except Exception as error:
            fn.log_error(f"Failed to remove fish: {error}")

    fn.threading.Thread(target=wait_remove, daemon=True).start()


def tofish_apply(self, _widget):
    fn.log_subsection("Apply Fish")
    fn.debug_print(f"  Current shell : {fn.get_shell()}")
    fn.debug_print("  Target shell  : fish")
    fn.change_shell(self, "fish")


def tooltip_callback(self, _widget, x, y, keyboard_mode, tooltip, text):
    tooltip.set_text(text)
    return True


def on_install_att_zshrc_clicked(self, _widget):
    fn.log_subsection("Apply ATT Zsh Configuration")
    fn.debug_print(f"  Source : {fn.zshrc_kiro}")
    fn.debug_print(f"  Target : {fn.zsh_config}")
    fn.debug_print(f"  Exists : {fn.path.isfile(fn.zshrc_kiro)}")
    try:
        if fn.path.isfile(fn.zshrc_kiro):
            fn.log_info_concise(f"  From: {fn.zshrc_kiro}")
            fn.log_info_concise(f"  To:   {fn.zsh_config}")
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
            fn.log_info_concise(f"  From: {backup}")
            fn.log_info_concise(f"  To:   {fn.zsh_config}")
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
    fn.log_subsection("Apply Zsh Theme")
    theme = fn.get_combo_text(self.zsh_themes)
    fn.debug_print(f"  Theme  : {theme}")
    fn.debug_print(f"  Target : {fn.zsh_config}")
    zsh_theme.set_config(self, theme)
    fn.log_success(f"Zsh theme set to {theme} - open a new terminal to activate")
    fn.GLib.idle_add(fn.show_in_app_notification, self, f"Zsh theme set to {theme}")


def tozsh_apply(self, _widget):
    fn.log_subsection("Apply Zsh")
    fn.debug_print(f"  Current shell : {fn.get_shell()}")
    fn.debug_print("  Target shell  : zsh")
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
    pairs = [
        ("expac", self.expac),
        ("ripgrep", self.ripgrep),
        ("yay-git", self.yay),
        ("paru-git", self.paru),
        ("bat", self.bat),
        ("downgrade", self.downgrade),
        ("hw-probe", self.hw_probe),
        ("rate-mirrors", self.rate_mirrors),
        ("most", self.most),
        ("fzf", self.fzf),
    ]
    selected = [pkg for pkg, cb in pairs if cb.get_active()]
    if not selected:
        fn.log_info("No packages selected")
        fn.show_in_app_notification(self, "No packages selected")
        return

    fn.log_info(f"Installing: {' '.join(selected)}")
    fn.show_in_app_notification(self, "Opening terminal...")

    def wait_and_refresh(process):
        if process is not None:
            process.wait()
        for pkg, cb in pairs:
            installed = fn.check_package_installed(pkg)
            fn.GLib.idle_add(cb.set_active, installed)
            fn.log_item(f"  {pkg:<20} {'OK' if installed else 'NOT INSTALLED'}")
        fn.GLib.idle_add(fn.log_success, "Extra shell applications done")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "Extra shell applications installed")

    process = fn.launch_pacman_install_in_terminal(" ".join(selected))
    fn.threading.Thread(target=wait_and_refresh, args=(process,), daemon=True).start()


def on_extra_shell_applications_remove_clicked(self, _widget):
    fn.log_subsection("Remove Extra Shell Applications")
    pairs = [
        ("expac", self.expac),
        ("ripgrep", self.ripgrep),
        ("yay-git", self.yay),
        ("paru-git", self.paru),
        ("bat", self.bat),
        ("downgrade", self.downgrade),
        ("hw-probe", self.hw_probe),
        ("rate-mirrors", self.rate_mirrors),
        ("most", self.most),
        ("fzf", self.fzf),
    ]
    selected = [pkg for pkg, cb in pairs if cb.get_active()]
    if not selected:
        fn.log_info("No packages selected")
        fn.show_in_app_notification(self, "No packages selected")
        return

    fn.log_info(f"Removing: {' '.join(selected)}")
    fn.show_in_app_notification(self, "Opening terminal...")

    def wait_and_refresh(process):
        if process is not None:
            process.wait()
        for pkg, cb in pairs:
            installed = fn.check_package_installed(pkg)
            fn.GLib.idle_add(cb.set_active, installed)
            fn.log_item(f"  {pkg:<20} {'OK' if installed else 'NOT INSTALLED'}")
        fn.GLib.idle_add(self.select_all.set_active, False)
        fn.GLib.idle_add(fn.log_success, "Extra shell applications removal done")
        fn.GLib.idle_add(fn.show_in_app_notification, self, "Extra shell applications removed")

    pkgs = " ".join(selected)
    script = f"sudo pacman -Rdd --noconfirm {pkgs}; echo ''; read -p 'Press Enter to close'"
    process = fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script])
    fn.threading.Thread(target=wait_and_refresh, args=(process,), daemon=True).start()


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
        self.fzf.set_active(True)


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
