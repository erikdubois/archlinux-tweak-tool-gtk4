# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools
import shell


def gui(self, Gtk, vboxstack23, zsh_theme, base_dir, GdkPixbuf, fn):
    """create a gui"""
    from gi.repository import Gdk

    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox1_lbl = Gtk.Label(xalign=0)
    hbox1_lbl.set_markup("Shells")
    hbox1_lbl.set_name("title")
    hbox1_lbl.set_margin_start(10)
    hbox1_lbl.set_margin_end(10)
    hbox1.append(hbox1_lbl)

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox0.append(hseparator)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    vboxstack1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
    stack.set_transition_duration(350)
    stack.set_hhomogeneous(False)
    stack.set_vhomogeneous(False)

    stack_switcher = Gtk.StackSwitcher()
    stack_switcher.set_orientation(Gtk.Orientation.HORIZONTAL)
    stack_switcher.set_stack(stack)

    if fn.check_package_installed("bash"):
        # ======================================================================
        #                              BASH
        # ======================================================================

        hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox5_lbl = Gtk.Label(xalign=0)
        hbox5_lbl.set_markup("Bash")
        hbox5_lbl.set_name("title")
        hbox5.append(hbox5_lbl)

        hbox_bash_top_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox_bash_top_sep.append(hseparator)

        # ── Installation ──────────────────────────────────────────────

        hbox_installation_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_installation_title_lbl = Gtk.Label(xalign=0)
        hbox_installation_title_lbl.set_markup("<b>Installation</b>")
        hbox_installation_title_lbl.set_margin_start(10)
        hbox_installation_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_installation_sep.set_hexpand(True)
        hbox_installation_sep.set_valign(Gtk.Align.CENTER)
        hbox_installation_title.append(hbox_installation_title_lbl)
        hbox_installation_title.append(hbox_installation_sep)

        hbox_bash_completion_lbl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.bash_completion_lbl = Gtk.Label(xalign=0)
        if fn.check_package_installed("bash"):
            self.bash_completion_lbl.set_markup("Bash is already <b>installed</b>")
        else:
            self.bash_completion_lbl.set_markup("Bash is not installed")
        if fn.check_package_installed("bash-completion"):
            self.bash_completion_lbl.set_markup(
                "Bash and bash-completion are already <b>installed</b>"
            )
        else:
            self.bash_completion_lbl.set_markup(
                "Bash is already installed and bash-completion is not installed"
            )
        self.bash_completion_lbl.set_margin_start(10)
        self.bash_completion_lbl.set_margin_end(10)
        hbox_bash_completion_lbl.append(self.bash_completion_lbl)

        hbox_bash_completion_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        install_bash_completion = Gtk.Button(label="Install bash-completion")
        install_bash_completion.connect(
            "clicked", functools.partial(shell.on_install_bash_completion_clicked, self)
        )
        remove_bash_completion = Gtk.Button(label="Remove bash-completion")
        remove_bash_completion.connect(
            "clicked", functools.partial(shell.on_remove_bash_completion_clicked, self)
        )
        hbox_bash_completion_btns.set_margin_start(10)
        hbox_bash_completion_btns.append(install_bash_completion)
        hbox_bash_completion_btns.append(remove_bash_completion)

        # ── ATT config ────────────────────────────────────────────────

        hbox_att_config_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_att_config_title_lbl = Gtk.Label(xalign=0)
        hbox_att_config_title_lbl.set_markup("<b>ATT config</b>")
        hbox_att_config_title_lbl.set_margin_start(10)
        hbox_att_config_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_att_config_sep.set_hexpand(True)
        hbox_att_config_sep.set_valign(Gtk.Align.CENTER)
        hbox_att_config_title.append(hbox_att_config_title_lbl)
        hbox_att_config_title.append(hbox_att_config_sep)

        hbox_bash_config_lbl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox_bash_config_lbl_txt = Gtk.Label(xalign=0)
        hbox_bash_config_lbl_txt.set_markup("Overwrite your ~/.bashrc with the ATT bashrc")
        hbox_bash_config_lbl_txt.set_margin_start(10)
        hbox_bash_config_lbl_txt.set_margin_end(10)
        hbox_bash_config_lbl.append(hbox_bash_config_lbl_txt)

        hbox_bash_config_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.install_bash_config = Gtk.Button(label="Install the ATT bashrc configuration")
        self.install_bash_config.connect("clicked", functools.partial(shell.on_install_att_bashrc_clicked, self))
        self.bash_reset = Gtk.Button(label="Reset back to your original ~/.bashrc")
        self.bash_reset.connect("clicked", functools.partial(shell.on_bash_reset_clicked, self))
        hbox_bash_config_btns.set_margin_start(10)
        hbox_bash_config_btns.append(self.install_bash_config)
        hbox_bash_config_btns.append(self.bash_reset)

        # ── Change shell ──────────────────────────────────────────────

        hbox_change_shell_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_change_shell_title_lbl = Gtk.Label(xalign=0)
        hbox_change_shell_title_lbl.set_markup("<b>Change shell</b>")
        hbox_change_shell_title_lbl.set_margin_start(10)
        hbox_change_shell_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_change_shell_sep.set_hexpand(True)
        hbox_change_shell_sep.set_valign(Gtk.Align.CENTER)
        hbox_change_shell_title.append(hbox_change_shell_title_lbl)
        hbox_change_shell_title.append(hbox_change_shell_sep)

        hbox_logout_warning = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_logout_warning_lbl = Gtk.Label()
        hbox_logout_warning_lbl.set_markup("<b>If you just switched shell, log-out first</b>")
        hbox_logout_warning_lbl.set_margin_start(10)
        hbox_logout_warning_lbl.set_margin_end(10)
        hbox_logout_warning.append(hbox_logout_warning_lbl)

        hbox_shell_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        tobash = Gtk.Button(label="Apply bash")
        tobash.connect("clicked", functools.partial(shell.tobash_apply, self))
        hbox_shell_buttons.set_margin_start(10)
        hbox_shell_buttons.append(tobash)

        # ==========================================================
        #                     VBOXSTACK
        # ==========================================================

        vboxstack1.append(hbox5)
        vboxstack1.append(hbox_bash_top_sep)
        vboxstack1.append(hbox_installation_title)
        vboxstack1.append(hbox_bash_completion_lbl)
        vboxstack1.append(hbox_bash_completion_btns)
        vboxstack1.append(hbox_att_config_title)
        vboxstack1.append(hbox_bash_config_lbl)
        vboxstack1.append(hbox_bash_config_btns)
        vboxstack1.append(hbox_change_shell_title)
        vboxstack1.append(hbox_logout_warning)
        vboxstack1.append(hbox_shell_buttons)

    else:
        # no bash installed
        hbox36 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox36_lbl = Gtk.Label(xalign=0)
        hbox36_lbl.set_markup("Bash is not installed")
        hbox36_lbl.set_name("title")
        hbox36.append(hbox36_lbl)

        hbox37 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox37.append(hseparator)

        message = Gtk.Label()
        message.set_markup("<b>Bash does not seem to be installed</b>")

        vboxstack1.append(hbox36)
        vboxstack1.append(hbox37)
        vboxstack1.append(message)

    # ==================================================================
    #                       ZSH
    # ==================================================================

    if fn.check_package_installed("zsh"):
        hbox19 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox19_lbl = Gtk.Label(xalign=0)
        hbox19_lbl.set_markup("Zsh")
        hbox19_lbl.set_name("title")
        hbox19.append(hbox19_lbl)

        hbox_zsh_top_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox_zsh_top_sep.append(hseparator)

        # ── Installation ──────────────────────────────────────────────

        hbox_zsh_installation_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_zsh_installation_title_lbl = Gtk.Label(xalign=0)
        hbox_zsh_installation_title_lbl.set_markup("<b>Installation</b>")
        hbox_zsh_installation_title_lbl.set_margin_start(10)
        hbox_zsh_installation_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_zsh_installation_sep.set_hexpand(True)
        hbox_zsh_installation_sep.set_valign(Gtk.Align.CENTER)
        hbox_zsh_installation_title.append(hbox_zsh_installation_title_lbl)
        hbox_zsh_installation_title.append(hbox_zsh_installation_sep)

        hbox_zsh_status_lbl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        zsh_status_lbl = Gtk.Label(xalign=0)
        zsh_status_lbl.set_markup("Zsh is <b>installed</b>")
        zsh_status_lbl.set_margin_start(10)
        zsh_status_lbl.set_margin_end(10)
        self.zsh_completions_lbl = Gtk.Label(xalign=0)
        if fn.check_package_installed("zsh-completions"):
            self.zsh_completions_lbl.set_markup("Zsh-completion is already <b>installed</b>")
        else:
            self.zsh_completions_lbl.set_markup("Zsh-completion is <b>not</b> installed")
        self.zsh_completions_lbl.set_margin_start(10)
        self.zsh_completions_lbl.set_margin_end(10)
        hbox_zsh_status_lbl.append(zsh_status_lbl)
        hbox_zsh_status_lbl.append(self.zsh_completions_lbl)

        hbox_zsh_completions_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.install_zsh_completions = Gtk.Button(label="Install zsh-completion")
        self.install_zsh_completions.connect(
            "clicked", functools.partial(shell.on_install_zsh_completions_clicked, self)
        )
        self.remove_zsh_completions = Gtk.Button(label="Remove zsh-completion")
        self.remove_zsh_completions.connect(
            "clicked", functools.partial(shell.on_remove_zsh_completions_clicked, self)
        )
        hbox_zsh_completions_btns.set_margin_start(10)
        hbox_zsh_completions_btns.append(self.install_zsh_completions)
        hbox_zsh_completions_btns.append(self.remove_zsh_completions)

        hbox_zsh_syntax_lbl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.zsh_syntax_lbl = Gtk.Label(xalign=0)
        if fn.check_package_installed("zsh-syntax-highlighting"):
            self.zsh_syntax_lbl.set_markup("Zsh-syntax-highlighting is already <b>installed</b>")
        else:
            self.zsh_syntax_lbl.set_markup("Zsh-syntax-highlighting is not installed")
        self.zsh_syntax_lbl.set_margin_start(10)
        self.zsh_syntax_lbl.set_margin_end(10)
        hbox_zsh_syntax_lbl.append(self.zsh_syntax_lbl)

        hbox_zsh_syntax_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.install_zsh_syntax_highlighting = Gtk.Button(label="Install Zsh-syntax-highlighting")
        self.install_zsh_syntax_highlighting.connect(
            "clicked", functools.partial(shell.on_install_zsh_syntax_highlighting_clicked, self)
        )
        self.remove_zsh_syntax_highlighting = Gtk.Button(label="Remove Zsh-syntax-highlighting")
        self.remove_zsh_syntax_highlighting.connect(
            "clicked", functools.partial(shell.on_remove_zsh_syntax_highlighting_clicked, self)
        )
        hbox_zsh_syntax_btns.set_margin_start(10)
        hbox_zsh_syntax_btns.append(self.install_zsh_syntax_highlighting)
        hbox_zsh_syntax_btns.append(self.remove_zsh_syntax_highlighting)

        # ── Oh-my-zsh ─────────────────────────────────────────────────

        hbox_zsh_omz_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_zsh_omz_title_lbl = Gtk.Label(xalign=0)
        hbox_zsh_omz_title_lbl.set_markup("<b>Oh-my-zsh</b>")
        hbox_zsh_omz_title_lbl.set_margin_start(10)
        hbox_zsh_omz_title_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_zsh_omz_title_sep.set_hexpand(True)
        hbox_zsh_omz_title_sep.set_valign(Gtk.Align.CENTER)
        hbox_zsh_omz_title.append(hbox_zsh_omz_title_lbl)
        hbox_zsh_omz_title.append(hbox_zsh_omz_title_sep)

        hbox_zsh_omz_lbl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.zsh_omz_lbl = Gtk.Label(xalign=0)
        if fn.check_package_installed("oh-my-zsh-git"):
            self.zsh_omz_lbl.set_markup("Oh-my-zsh-git is already <b>installed</b>")
        else:
            self.zsh_omz_lbl.set_markup("Oh-my-zsh-git is not installed")
        self.zsh_omz_lbl.set_margin_start(10)
        self.zsh_omz_lbl.set_margin_end(10)
        hbox_zsh_omz_lbl.append(self.zsh_omz_lbl)

        hbox_zsh_omz_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.install_zsh_omz = Gtk.Button(label="Install Oh-my-zsh")
        self.install_zsh_omz.connect("clicked", functools.partial(shell.install_oh_my_zsh, self))
        self.remove_zsh_omz = Gtk.Button(label="Remove Oh-my-zsh")
        self.remove_zsh_omz.connect("clicked", functools.partial(shell.remove_oh_my_zsh, self))
        hbox_zsh_omz_btns.set_margin_start(10)
        hbox_zsh_omz_btns.append(self.install_zsh_omz)
        hbox_zsh_omz_btns.append(self.remove_zsh_omz)

        # ── ATT config ────────────────────────────────────────────────

        hbox_zsh_att_config_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_zsh_att_config_title_lbl = Gtk.Label(xalign=0)
        hbox_zsh_att_config_title_lbl.set_markup("<b>ATT config</b>")
        hbox_zsh_att_config_title_lbl.set_margin_start(10)
        hbox_zsh_att_config_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_zsh_att_config_sep.set_hexpand(True)
        hbox_zsh_att_config_sep.set_valign(Gtk.Align.CENTER)
        hbox_zsh_att_config_title.append(hbox_zsh_att_config_title_lbl)
        hbox_zsh_att_config_title.append(hbox_zsh_att_config_sep)

        hbox_zsh_config_lbl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox_zsh_config_lbl_txt = Gtk.Label(xalign=0)
        hbox_zsh_config_lbl_txt.set_markup("Overwrite your ~/.zshrc with the ATT zshrc")
        hbox_zsh_config_lbl_txt.set_margin_start(10)
        hbox_zsh_config_lbl_txt.set_margin_end(10)
        hbox_zsh_config_lbl.append(hbox_zsh_config_lbl_txt)

        hbox_zsh_config_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.install_zsh_config = Gtk.Button(label="Install the ATT zshrc configuration")
        self.install_zsh_config.connect("clicked", functools.partial(shell.on_install_att_zshrc_clicked, self))
        self.zsh_reset = Gtk.Button(label="Reset back to the original ~/.zshrc")
        self.zsh_reset.connect("clicked", functools.partial(shell.on_zshrc_reset_clicked, self))
        hbox_zsh_config_btns.set_margin_start(10)
        hbox_zsh_config_btns.append(self.install_zsh_config)
        hbox_zsh_config_btns.append(self.zsh_reset)

        # ── Themes ────────────────────────────────────────────────────

        hbox_zsh_themes_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_zsh_themes_title_lbl = Gtk.Label(xalign=0)
        hbox_zsh_themes_title_lbl.set_markup("<b>Themes</b>")
        hbox_zsh_themes_title_lbl.set_margin_start(10)
        hbox_zsh_themes_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_zsh_themes_sep.set_hexpand(True)
        hbox_zsh_themes_sep.set_valign(Gtk.Align.CENTER)
        hbox_zsh_themes_title.append(hbox_zsh_themes_title_lbl)
        hbox_zsh_themes_title.append(hbox_zsh_themes_sep)

        hbox_zsh_themes_dropdown = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_zsh_themes_dropdown_lbl = Gtk.Label(xalign=0)
        hbox_zsh_themes_dropdown_lbl.set_markup("Zsh themes")
        hbox_zsh_themes_dropdown_lbl.set_margin_start(10)
        hbox_zsh_themes_dropdown_lbl.set_margin_end(10)
        self.zsh_themes = Gtk.DropDown.new_from_strings([])
        self.zsh_themes.set_size_request(300, 20)
        zsh_theme.get_themes(self.zsh_themes)
        self.zsh_themes.set_margin_start(10)
        self.zsh_themes.set_margin_end(10)
        hbox_zsh_themes_dropdown.append(hbox_zsh_themes_dropdown_lbl)
        hbox_zsh_themes_dropdown.append(self.zsh_themes)

        hbox_zsh_apply_theme_btn = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.termset = Gtk.Button(label="Apply Zsh theme")
        self.termset.connect("clicked", functools.partial(shell.on_zsh_apply_theme, self))
        omz_installed = fn.check_package_installed("oh-my-zsh-git")
        self.termset.set_sensitive(omz_installed)
        self.zsh_themes.set_sensitive(omz_installed)
        self.termset.set_margin_start(10)
        self.termset.set_margin_end(10)
        hbox_zsh_apply_theme_btn.append(self.termset)

        image_width = 800
        image_height = 500
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            base_dir + "/images/zsh-sample.jpg", image_width, image_height
        )
        if self.zsh_themes.get_selected_item() is None:
            pass
        elif fn.path.isfile(
            base_dir
            + "/images/zsh_previews/"
            + fn.get_combo_text(self.zsh_themes)
            + ".jpg"
        ):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                base_dir
                + "/images/zsh_previews/"
                + fn.get_combo_text(self.zsh_themes)
                + ".jpg",
                image_width,
                image_height,
            )
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        image = Gtk.Picture.new_for_paintable(texture)
        image.set_content_fit(Gtk.ContentFit.CONTAIN)
        image.set_margin_top(0)
        image.set_hexpand(False)
        image.set_vexpand(False)

        self.zsh_themes.connect(
            "notify::selected",
            lambda w, _p, img, tt, ab, iw, ih: fn.update_image(self, w, img, tt, ab, iw, ih),
            image,
            "zsh",
            base_dir,
            image_width,
            image_height,
        )

        # ── Change shell ──────────────────────────────────────────────

        hbox_zsh_change_shell_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_zsh_change_shell_title_lbl = Gtk.Label(xalign=0)
        hbox_zsh_change_shell_title_lbl.set_markup("<b>Change shell</b>")
        hbox_zsh_change_shell_title_lbl.set_margin_start(10)
        hbox_zsh_change_shell_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_zsh_change_shell_sep.set_hexpand(True)
        hbox_zsh_change_shell_sep.set_valign(Gtk.Align.CENTER)
        hbox_zsh_change_shell_title.append(hbox_zsh_change_shell_title_lbl)
        hbox_zsh_change_shell_title.append(hbox_zsh_change_shell_sep)

        hbox_zsh_logout_warning = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_zsh_logout_warning_lbl = Gtk.Label(xalign=0)
        hbox_zsh_logout_warning_lbl.set_markup(
            "Restart your terminal to apply the new Zsh theme\n"
            "<b>If you just switched shell, log-out first</b>"
        )
        hbox_zsh_logout_warning_lbl.set_margin_start(10)
        hbox_zsh_logout_warning_lbl.set_margin_end(10)
        hbox_zsh_logout_warning.append(hbox_zsh_logout_warning_lbl)

        hbox_zsh_shell_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        tozsh = Gtk.Button(label="Apply zsh")
        tozsh.connect("clicked", functools.partial(shell.tozsh_apply, self))
        hbox_zsh_shell_buttons.set_margin_start(10)
        hbox_zsh_shell_buttons.append(tozsh)

        vboxstack2.append(hbox19)
        vboxstack2.append(hbox_zsh_top_sep)
        vboxstack2.append(hbox_zsh_installation_title)
        vboxstack2.append(hbox_zsh_status_lbl)
        vboxstack2.append(hbox_zsh_completions_btns)
        vboxstack2.append(hbox_zsh_syntax_lbl)
        vboxstack2.append(hbox_zsh_syntax_btns)
        vboxstack2.append(hbox_zsh_att_config_title)
        vboxstack2.append(hbox_zsh_config_lbl)
        vboxstack2.append(hbox_zsh_config_btns)
        vboxstack2.append(hbox_zsh_omz_title)
        vboxstack2.append(hbox_zsh_omz_lbl)
        vboxstack2.append(hbox_zsh_omz_btns)
        vboxstack2.append(hbox_zsh_themes_title)
        vboxstack2.append(hbox_zsh_themes_dropdown)
        vboxstack2.append(hbox_zsh_apply_theme_btn)
        vboxstack2.append(image)
        vboxstack2.append(hbox_zsh_change_shell_title)
        vboxstack2.append(hbox_zsh_logout_warning)
        vboxstack2.append(hbox_zsh_shell_buttons)

    else:
        # no zsh installed
        hbox32 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox32_lbl = Gtk.Label(xalign=0)
        hbox32_lbl.set_markup("Zsh is not installed")
        hbox32_lbl.set_name("title")
        hbox32.append(hbox32_lbl)

        hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox41.append(hseparator)

        message = Gtk.Label()
        message.set_markup("<b>Zsh does not seem to be installed</b>")

        install_only_zsh = Gtk.Button(
            label="Install only Zsh and restart ATT to configure"
        )
        install_only_zsh.connect("clicked", functools.partial(shell.on_clicked_install_only_zsh, self))

        vboxstack2.append(hbox32)
        vboxstack2.append(hbox41)
        vboxstack2.append(message)
        vboxstack2.append(install_only_zsh)

    # ==================================================================
    #                       FISH
    # ==================================================================

    if fn.check_package_installed("fish"):
        # ── Title ─────────────────────────────────────────────────────

        hbox_fish_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_fish_title_lbl = Gtk.Label(xalign=0)
        hbox_fish_title_lbl.set_markup("Fish")
        hbox_fish_title_lbl.set_name("title")
        hbox_fish_title.append(hbox_fish_title_lbl)

        hbox_fish_top_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox_fish_top_sep.append(hseparator)

        # ── Installation ──────────────────────────────────────────────

        hbox_fish_installation_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_fish_installation_title_lbl = Gtk.Label(xalign=0)
        hbox_fish_installation_title_lbl.set_markup("<b>Installation</b>")
        hbox_fish_installation_title_lbl.set_margin_start(10)
        hbox_fish_installation_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_fish_installation_sep.set_hexpand(True)
        hbox_fish_installation_sep.set_valign(Gtk.Align.CENTER)
        hbox_fish_installation_title.append(hbox_fish_installation_title_lbl)
        hbox_fish_installation_title.append(hbox_fish_installation_sep)

        hbox_fish_status_lbl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        fish_status_lbl = Gtk.Label(xalign=0)
        fish_status_lbl.set_markup("Fish is <b>installed</b>")
        fish_status_lbl.set_margin_start(10)
        fish_status_lbl.set_margin_end(10)
        hbox_fish_status_lbl.append(fish_status_lbl)

        hbox_fish_install_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.install_fish = Gtk.Button(label="Install Fish")
        self.install_fish.connect("clicked", functools.partial(shell.on_install_only_fish_clicked, self))
        self.remove_fish = Gtk.Button(label="Remove Fish")
        self.remove_fish.connect("clicked", functools.partial(shell.on_remove_only_fish_clicked, self))
        hbox_fish_install_btns.set_margin_start(10)
        hbox_fish_install_btns.append(self.install_fish)
        hbox_fish_install_btns.append(self.remove_fish)

        # ── ATT config ────────────────────────────────────────────────

        hbox_fish_att_config_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_fish_att_config_title_lbl = Gtk.Label(xalign=0)
        hbox_fish_att_config_title_lbl.set_markup("<b>ATT config</b>")
        hbox_fish_att_config_title_lbl.set_margin_start(10)
        hbox_fish_att_config_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_fish_att_config_sep.set_hexpand(True)
        hbox_fish_att_config_sep.set_valign(Gtk.Align.CENTER)
        hbox_fish_att_config_title.append(hbox_fish_att_config_title_lbl)
        hbox_fish_att_config_title.append(hbox_fish_att_config_sep)

        hbox_fish_config_lbl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox_fish_config_lbl_txt = Gtk.Label(xalign=0)
        hbox_fish_config_lbl_txt.set_markup("Overwrite your ~/.config/fish/config.fish with the ATT config")
        hbox_fish_config_lbl_txt.set_margin_start(10)
        hbox_fish_config_lbl_txt.set_margin_end(10)
        hbox_fish_config_lbl.append(hbox_fish_config_lbl_txt)

        hbox_fish_config_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.install_fish_config = Gtk.Button(label="Install the ATT config.fish")
        self.install_fish_config.connect("clicked", functools.partial(shell.on_install_att_fish_config_clicked, self))
        self.fish_reset = Gtk.Button(label="Reset back to the original ~/.config/fish/config.fish")
        self.fish_reset.connect("clicked", functools.partial(shell.on_fish_reset_clicked, self))
        hbox_fish_config_btns.set_margin_start(10)
        hbox_fish_config_btns.append(self.install_fish_config)
        hbox_fish_config_btns.append(self.fish_reset)

        # ── Change shell ──────────────────────────────────────────────

        hbox_fish_change_shell_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_fish_change_shell_title_lbl = Gtk.Label(xalign=0)
        hbox_fish_change_shell_title_lbl.set_markup("<b>Change shell</b>")
        hbox_fish_change_shell_title_lbl.set_margin_start(10)
        hbox_fish_change_shell_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_fish_change_shell_sep.set_hexpand(True)
        hbox_fish_change_shell_sep.set_valign(Gtk.Align.CENTER)
        hbox_fish_change_shell_title.append(hbox_fish_change_shell_title_lbl)
        hbox_fish_change_shell_title.append(hbox_fish_change_shell_sep)

        hbox_fish_logout_warning = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_fish_logout_warning_lbl = Gtk.Label(xalign=0)
        hbox_fish_logout_warning_lbl.set_markup(
            "Restart your terminal to apply the new Fish config\n"
            "<b>If you just switched shell, log-out first</b>"
        )
        hbox_fish_logout_warning_lbl.set_margin_start(10)
        hbox_fish_logout_warning_lbl.set_margin_end(10)
        hbox_fish_logout_warning.append(hbox_fish_logout_warning_lbl)

        hbox_fish_shell_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        tofish = Gtk.Button(label="Apply fish")
        tofish.connect("clicked", functools.partial(shell.tofish_apply, self))
        hbox_fish_shell_btns.set_margin_start(10)
        if not fn.distr == "archcraft":
            hbox_fish_shell_btns.append(tofish)

        vboxstack3.append(hbox_fish_title)
        vboxstack3.append(hbox_fish_top_sep)
        vboxstack3.append(hbox_fish_installation_title)
        vboxstack3.append(hbox_fish_status_lbl)
        vboxstack3.append(hbox_fish_install_btns)
        vboxstack3.append(hbox_fish_att_config_title)
        vboxstack3.append(hbox_fish_config_lbl)
        vboxstack3.append(hbox_fish_config_btns)
        vboxstack3.append(hbox_fish_change_shell_title)
        vboxstack3.append(hbox_fish_logout_warning)
        vboxstack3.append(hbox_fish_shell_btns)

    else:
        # no fish installed
        hbox_fish_no_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_fish_no_title_lbl = Gtk.Label(xalign=0)
        hbox_fish_no_title_lbl.set_markup("Fish is not installed")
        hbox_fish_no_title_lbl.set_name("title")
        hbox_fish_no_title.append(hbox_fish_no_title_lbl)

        hbox_fish_no_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox_fish_no_sep.append(hseparator)

        fish_not_installed_msg = Gtk.Label()
        fish_not_installed_msg.set_markup(
            "<b>Fish does not seem to be installed\nRestart ATT to see the information</b>"
        )

        hbox_fish_no_btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        install_only_fish = Gtk.Button(label="Install Fish and restart ATT to configure")
        install_only_fish.connect("clicked", functools.partial(shell.on_install_only_fish_clicked_reboot, self))
        hbox_fish_no_btns.set_margin_start(10)
        hbox_fish_no_btns.append(install_only_fish)

        vboxstack3.append(hbox_fish_no_title)
        vboxstack3.append(hbox_fish_no_sep)
        vboxstack3.append(fish_not_installed_msg)
        vboxstack3.append(hbox_fish_no_btns)

    # ==================================================================
    #                       EXTRA
    # ==================================================================

    hbox51 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox51_lbl = Gtk.Label()
    hbox51_lbl.set_markup(
        "The shell configurations of the ATT contain\
 aliases that require certain applications\n\
\nHere you can select the missing applications and install them\n\
Activate the nemesis repo (when needed) to install all of them\n\n\
Applications that were NOT installed will be <b>unselected</b> again\n\
Activate the necessary repos"
    )
    self.select_all = Gtk.CheckButton(label="Select them all")
    self.select_all.connect("notify::active", functools.partial(shell.on_select_all_toggle, self))
    hbox51_lbl.set_margin_top(20)
    hbox51_lbl.set_margin_start(10)
    hbox51_lbl.set_margin_end(10)
    hbox51_lbl.set_hexpand(False)
    hbox51.append(hbox51_lbl)
    self.select_all.set_margin_start(10)
    self.select_all.set_margin_end(10)
    hbox51.append(self.select_all)  # pack_end

    # hbox52 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    # self.select_all = Gtk.CheckButton(label="Select them all")
    # #hbox52.set_margin_top(20)
    # hbox52.pack_start(self.select_all, False, False, 10)

    self.expac = Gtk.CheckButton(label="expac")
    self.ripgrep = Gtk.CheckButton(label="ripgrep")
    self.yay = Gtk.CheckButton(label="yay-git")
    self.paru = Gtk.CheckButton(label="paru-git")
    self.bat = Gtk.CheckButton(label="bat")
    self.downgrade = Gtk.CheckButton(label="downgrade")
    self.hw_probe = Gtk.CheckButton(label="hw-probe")
    self.rate_mirrors = Gtk.CheckButton(label="rate-mirrors")
    self.most = Gtk.CheckButton(label="most")
    self.fzf = Gtk.CheckButton(label="fzf")

    flowbox = Gtk.FlowBox()
    flowbox.set_valign(Gtk.Align.START)
    flowbox.set_max_children_per_line(2)
    flowbox.set_selection_mode(Gtk.SelectionMode.NONE)

    flowbox.append(self.expac)
    flowbox.append(self.ripgrep)
    flowbox.append(self.yay)
    flowbox.append(self.paru)
    flowbox.append(self.bat)
    flowbox.append(self.downgrade)
    flowbox.append(self.hw_probe)
    flowbox.append(self.rate_mirrors)
    flowbox.append(self.most)
    flowbox.append(self.fzf)

    extra_shell_applications = Gtk.Button(label="Install packages")
    extra_shell_applications.connect(
        "clicked", functools.partial(shell.on_extra_shell_applications_clicked, self)
    )

    vboxstack4.append(hbox51)
    # vboxstack4.pack_start(hbox52, False, False, 0)
    vboxstack4.append(flowbox)
    remove_shell_applications = Gtk.Button(label="Remove packages")
    remove_shell_applications.connect(
        "clicked", functools.partial(shell.on_extra_shell_applications_remove_clicked, self)
    )

    hbox_extra_btn = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_extra_btn.set_margin_start(10)
    hbox_extra_btn.append(extra_shell_applications)
    hbox_extra_btn.append(remove_shell_applications)
    vboxstack4.append(hbox_extra_btn)
    # vboxstack4.pack_start(install_only_fish, False, False, 0)

    # ==================================================================
    #                       PACK TO STACK
    # ==================================================================

    stack.add_titled(vboxstack1, "stack1", "BASH")
    stack.add_titled(vboxstack2, "stack2", "ZSH")
    if not fn.distr == "archcraft":
        stack.add_titled(vboxstack3, "stack3", "FISH")
    stack.add_titled(vboxstack4, "stack4", "EXTRA")

    vbox.append(stack_switcher)
    stack.set_hexpand(True)
    stack.set_vexpand(True)
    vbox.append(stack)

    vboxstack23.append(hbox1)
    vboxstack23.append(hbox0)
    vbox.set_hexpand(True)
    vbox.set_vexpand(True)
    vboxstack23.append(vbox)
