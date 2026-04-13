# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================


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
        if fn.get_shell() == "bash":
            hbox5_lbl.set_markup("Bash (active)")
        else:
            hbox5_lbl.set_markup("Bash (not active)")
        hbox5_lbl.set_name("title")
        hbox5.append(hbox5_lbl)

        hbox6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox6.append(hseparator)

        hbox7 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox7_lbl = Gtk.Label()
        if fn.check_package_installed("bash"):
            hbox7_lbl.set_markup("Bash is already <b>installed</b>")
        else:
            hbox7_lbl.set_markup("Bash is not installed")
        if fn.check_package_installed("bash-completion"):
            hbox7_lbl.set_markup(
                "Bash and bash-completion are already <b>installed</b>"
            )
        else:
            hbox7_lbl.set_markup(
                "Bash is already installed and  bash-completion is not installed"
            )
        install_bash_completion = Gtk.Button(label="Install bash-completion")
        install_bash_completion.connect(
            "clicked", self.on_install_bash_completion_clicked
        )
        remove_bash_completion = Gtk.Button(label="Remove bash-completion")
        remove_bash_completion.connect(
            "clicked", self.on_remove_bash_completion_clicked
        )
        hbox7_lbl.set_margin_start(10)
        hbox7_lbl.set_margin_end(10)
        hbox7_lbl.set_hexpand(True)
        hbox7.append(hbox7_lbl)
        install_bash_completion.set_margin_start(10)
        install_bash_completion.set_margin_end(10)
        hbox7.append(install_bash_completion)  # pack_end
        remove_bash_completion.set_margin_start(10)
        remove_bash_completion.set_margin_end(10)
        hbox7.append(remove_bash_completion)  # pack_end

        hbox8 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox8_lbl = Gtk.Label()
        hbox8_lbl.set_markup("Overwrite your ~/.bashrc with the ATT bashrc")
        self.arcolinux_bash = Gtk.Button(label="Install the ATT bashrc configuration")
        self.arcolinux_bash.connect("clicked", self.on_arcolinux_bash_clicked)
        self.bash_reset = Gtk.Button(label="Reset back to the original ~/.bashrc")
        self.bash_reset.connect("clicked", self.on_bash_reset_clicked)
        hbox8_lbl.set_margin_start(10)
        hbox8_lbl.set_margin_end(10)
        hbox8_lbl.set_hexpand(True)
        hbox8.append(hbox8_lbl)
        self.arcolinux_bash.set_margin_start(10)
        self.arcolinux_bash.set_margin_end(10)
        hbox8.append(self.arcolinux_bash)  # pack_end
        self.bash_reset.set_margin_start(10)
        self.bash_reset.set_margin_end(10)
        hbox8.append(self.bash_reset)  # pack_end

        hbox9 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox9_lbl = Gtk.Label()
        hbox9_lbl.set_markup("\n<b>If you just switched shell, log-out first</b>")
        # hbox9_lbl.set_margin_top(30)
        hbox9_lbl.set_margin_start(10)
        hbox9_lbl.set_margin_end(10)
        hbox9.append(hbox9_lbl)

        # ==========================================================
        #                     BUTTONS
        # ==========================================================

        hbox10 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        tobash = Gtk.Button(label="Apply bash")
        tobash.connect("clicked", self.tobash_apply)
        tofish = Gtk.Button(label="Apply fish")
        tofish.connect("clicked", self.tofish_apply)
        tozsh = Gtk.Button(label="Apply zsh")
        tozsh.connect("clicked", self.tozsh_apply)
        # bashreset = Gtk.Button(label="Reset bash")
        # bashreset.connect("clicked", self.on_bash_reset_clicked)

        hbox10.append(tobash)
        if not fn.distr == "archcraft":
            hbox10.append(tofish)
        hbox10.append(tozsh)
        # hbox10.pack_end(bashreset, False, False, 0)

        # ==========================================================
        #                     VBOXSTACK
        # ==========================================================

        vboxstack1.append(hbox5)  # Combobox
        vboxstack1.append(hbox6)  # Combobox
        vboxstack1.append(hbox7)  # fish
        vboxstack1.append(hbox8)  # oh-my-fish
        vboxstack1.append(hbox9)  # image
        vboxstack1.append(hbox10)  # pack_end  # Buttons

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
        hbox19_lbl.set_markup("Zsh (inactive)")
        if fn.get_shell() == "zsh":
            hbox19_lbl.set_markup("ZSH THEMES (Zsh active)")
        else:
            hbox19_lbl.set_markup("ZSH THEMES (Zsh not active)")
        hbox19_lbl.set_name("title")
        hbox19.append(hbox19_lbl)

        hbox20 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox20.append(hseparator)

        # ==========================================================

        hbox26 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox26_lbl = Gtk.Label()
        if fn.check_package_installed("zsh"):
            hbox26_lbl.set_markup("Zsh is already <b>installed</b>")
        else:
            hbox26_lbl.set_markup("Zsh is not installed")
        if fn.check_package_installed("zsh-completions"):
            hbox26_lbl.set_markup("Zsh and Zsh-completion are already <b>installed</b>")

        self.install_zsh_completions = Gtk.Button(label="Install zsh-completion")
        self.install_zsh_completions.connect(
            "clicked", self.on_install_zsh_completions_clicked
        )
        self.remove_zsh_completions = Gtk.Button(label="Remove zsh-completion")
        self.remove_zsh_completions.connect(
            "clicked", self.on_remove_zsh_completions_clicked
        )
        hbox26_lbl.set_margin_start(10)
        hbox26_lbl.set_margin_end(10)
        hbox26_lbl.set_hexpand(False)
        hbox26.append(hbox26_lbl)
        self.install_zsh_completions.set_margin_start(10)
        self.install_zsh_completions.set_margin_end(10)
        hbox26.append(self.install_zsh_completions)  # pack_end
        self.remove_zsh_completions.set_margin_start(10)
        self.remove_zsh_completions.set_margin_end(10)
        hbox26.append(self.remove_zsh_completions)  # pack_end

        hbox27 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox27_lbl = Gtk.Label()
        if fn.check_package_installed("zsh-syntax-highlighting"):
            hbox27_lbl.set_markup("Zsh-syntax-highlighting is already <b>installed</b>")
        else:
            hbox27_lbl.set_markup("Zsh-syntax-highlighting is not installed")
        self.install_zsh_syntax_highlighting = Gtk.Button(label="Install Zsh-syntax-highlighting")
        self.install_zsh_syntax_highlighting.connect(
            "clicked", self.on_install_zsh_syntax_highlighting_clicked
        )
        self.remove_zsh_syntax_highlighting = Gtk.Button(label="Remove Zsh-syntax-highlighting")
        self.remove_zsh_syntax_highlighting.connect(
            "clicked", self.on_remove_zsh_syntax_highlighting_clicked
        )
        hbox27_lbl.set_margin_start(10)
        hbox27_lbl.set_margin_end(10)
        hbox27_lbl.set_hexpand(False)
        hbox27.append(hbox27_lbl)
        self.install_zsh_syntax_highlighting.set_margin_start(10)
        self.install_zsh_syntax_highlighting.set_margin_end(10)
        hbox27.append(self.install_zsh_syntax_highlighting)  # pack_end
        self.remove_zsh_syntax_highlighting.set_margin_start(10)
        self.remove_zsh_syntax_highlighting.set_margin_end(10)
        hbox27.append(self.remove_zsh_syntax_highlighting)  # pack_end

        hbox28 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox28_lbl = Gtk.Label()
        if fn.check_package_installed("oh-my-zsh-git"):
            hbox28_lbl.set_markup("Oh-my-zsh-git is already <b>installed</b>")
        else:
            hbox28_lbl.set_markup("Oh-my-zsh-git is not installed")
        self.install_zsh_omz = Gtk.Button(label="Install Oh-my-zsh")
        self.install_zsh_omz.connect("clicked", self.install_oh_my_zsh)
        self.remove_zsh_omz = Gtk.Button(label="Remove Oh-my-zsh")
        self.remove_zsh_omz.connect("clicked", self.remove_oh_my_zsh)
        hbox28_lbl.set_margin_start(10)
        hbox28_lbl.set_margin_end(10)
        hbox28_lbl.set_hexpand(False)
        hbox28.append(hbox28_lbl)
        self.install_zsh_omz.set_margin_start(10)
        self.install_zsh_omz.set_margin_end(10)
        hbox28.append(self.install_zsh_omz)  # pack_end
        self.remove_zsh_omz.set_margin_start(10)
        self.remove_zsh_omz.set_margin_end(10)
        hbox28.append(self.remove_zsh_omz)  # pack_end

        hbox25 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox25_lbl = Gtk.Label()
        hbox25_lbl.set_markup("Overwrite your ~/.zshrc with the ATT zshrc")
        self.arcolinux_zsh = Gtk.Button(label="Install the ATT zshrc configuration")
        self.arcolinux_zsh.connect("clicked", self.on_arcolinux_zshrc_clicked)
        self.zsh_reset = Gtk.Button(label="Reset back to the original ~/.zshrc")
        self.zsh_reset.connect("clicked", self.on_zshrc_reset_clicked)
        hbox25_lbl.set_margin_start(10)
        hbox25_lbl.set_margin_end(10)
        hbox25_lbl.set_hexpand(False)
        hbox25.append(hbox25_lbl)
        self.arcolinux_zsh.set_margin_start(10)
        self.arcolinux_zsh.set_margin_end(10)
        hbox25.append(self.arcolinux_zsh)  # pack_end
        self.zsh_reset.set_margin_start(10)
        self.zsh_reset.set_margin_end(10)
        hbox25.append(self.zsh_reset)  # pack_end

        hbox21 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox21_lbl = Gtk.Label()
        hbox21_lbl.set_markup("Zsh themes")
        self.zsh_themes = Gtk.DropDown.new_from_strings([])
        self.zsh_themes.set_size_request(300, 20)
        zsh_theme.get_themes(self.zsh_themes)
        hbox21_lbl.set_margin_start(10)
        hbox21_lbl.set_margin_end(10)
        hbox21_lbl.set_hexpand(False)
        hbox21.append(hbox21_lbl)
        self.zsh_themes.set_margin_start(10)
        self.zsh_themes.set_margin_end(10)
        hbox21.append(self.zsh_themes)  # pack_end

        hbox29 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.termset = Gtk.Button(label="Apply Zsh theme")
        self.termset.connect("clicked", self.on_zsh_apply_theme)
        if not fn.check_package_installed("zsh"):
            self.termset.set_sensitive(False)
        self.termset.set_margin_start(10)
        self.termset.set_margin_end(10)
        hbox29.append(self.termset)  # pack_end

        # image dimensions - this will (in time) allow the image changing function
        # to be re-usable by other parts of the app
        image_width = 500
        image_height = 380
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
        image.set_hexpand(True)
        image.set_vexpand(True)

        self.zsh_themes.connect(
            "notify::selected",
            lambda w, _p, img, tt, ab, iw, ih: self.update_image(w, img, tt, ab, iw, ih),
            image,
            "zsh",
            base_dir,
            image_width,
            image_height,
        )

        hbox23 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox23_lbl = Gtk.Label()
        hbox23_lbl.set_markup(
            "Restart your terminal to apply the new Zsh theme\n\n<b>\
If you just switched shell, log-out first</b>\n"
        )
        hbox23_lbl.set_margin_top(30)
        hbox23_lbl.set_margin_start(10)
        hbox23_lbl.set_margin_end(10)
        hbox23.append(hbox23_lbl)

        hbox24 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        tozsh = Gtk.Button(label="Apply zsh")
        tobash = Gtk.Button(label="Apply bash")
        tofish = Gtk.Button(label="Apply fish")
        termreset = Gtk.Button(label="Reset or create ~/.zshrc")

        tozsh.connect("clicked", self.tozsh_apply)
        tobash.connect("clicked", self.tobash_apply)
        tofish.connect("clicked", self.tofish_apply)
        termreset.connect("clicked", self.on_zsh_reset)

        hbox24.append(tozsh)
        hbox24.append(tobash)
        if not fn.distr == "archcraft":
            hbox24.append(tofish)
        hbox24.append(termreset)  # pack_end

        vboxstack2.append(hbox19)
        vboxstack2.append(hbox20)
        vboxstack2.append(hbox26)
        vboxstack2.append(hbox27)
        vboxstack2.append(hbox28)
        vboxstack2.append(hbox25)
        vboxstack2.append(hbox21)
        vboxstack2.append(hbox29)
        vboxstack2.append(image)
        vboxstack2.append(hbox23)
        vboxstack2.append(hbox24)  # pack_end

        if not fn.check_package_installed("oh-my-zsh-git") or not fn.path.isfile(
            fn.zsh_config
        ):
            self.termset.set_sensitive(False)
            termreset.set_sensitive(False)
        if not fn.path.isfile(fn.zsh_config):
            termreset.set_sensitive(True)

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
        install_only_zsh.connect("clicked", self.on_clicked_install_only_zsh)

        vboxstack2.append(hbox32)
        vboxstack2.append(hbox41)
        vboxstack2.append(message)
        vboxstack2.append(install_only_zsh)

    # ==================================================================
    #                       FISH
    # ==================================================================

    if fn.check_package_installed("fish"):
        hbox30 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox30_lbl = Gtk.Label(xalign=0)
        if fn.get_shell() == "fish":
            hbox30_lbl.set_markup("Fish (active)")
        else:
            hbox30_lbl.set_markup("Fish (not active)")
        hbox30_lbl.set_name("title")
        hbox30.append(hbox30_lbl)

        hbox31 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox31.append(hseparator)

        hbox32 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox32_lbl = Gtk.Label()
        if fn.check_package_installed("fish"):
            hbox32_lbl.set_markup("Fish is already <b>installed</b>")
        else:
            hbox32_lbl.set_markup("Fish is not installed")
        install_fish = Gtk.Button(label="Install Fish")
        install_fish.connect("clicked", self.on_install_only_fish_clicked)
        remove_fish = Gtk.Button(label="Remove Fish")
        remove_fish.connect("clicked", self.on_remove_only_fish_clicked)
        hbox32_lbl.set_margin_start(10)
        hbox32_lbl.set_margin_end(10)
        hbox32_lbl.set_hexpand(False)
        hbox32.append(hbox32_lbl)
        install_fish.set_margin_start(10)
        install_fish.set_margin_end(10)
        hbox32.append(install_fish)  # pack_end
        remove_fish.set_margin_start(10)
        remove_fish.set_margin_end(10)
        hbox32.append(remove_fish)  # pack_end

        hbox33 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox33_lbl = Gtk.Label()
        if fn.check_package_installed("edu-shells-git"):
            hbox33_lbl.set_markup(
                "ATT bash, zsh and fish incl. oh-my-fish, themes and plugins is already <b>installed</b>"
            )
        else:
            hbox33_lbl.set_markup(
                "ATT fish incl. oh-my-fish, themes and plugins is not installed"
            )
        self.arcolinux_fish = Gtk.Button(label="Install the ATT Fish package")
        self.arcolinux_fish.connect("clicked", self.on_arcolinux_fish_package_clicked)
        hbox33_lbl.set_margin_start(10)
        hbox33_lbl.set_margin_end(10)
        hbox33_lbl.set_hexpand(False)
        hbox33.append(hbox33_lbl)
        self.arcolinux_fish.set_margin_start(10)
        self.arcolinux_fish.set_margin_end(10)
        hbox33.append(self.arcolinux_fish)  # pack_end

        hbox38 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox38_lbl = Gtk.Label()
        hbox38_lbl.set_markup("Overwrite your config.fish with the ATT config")
        self.arcolinux_fish = Gtk.Button(label="Install just the ATT config.fish")
        self.arcolinux_fish.connect("clicked", self.on_arcolinux_only_fish_clicked)
        self.fish_reset = Gtk.Button(label="Reset back to the original ~/.config/config.fish")
        self.fish_reset.connect("clicked", self.on_fish_reset_clicked)
        hbox38_lbl.set_margin_start(10)
        hbox38_lbl.set_margin_end(10)
        hbox38_lbl.set_hexpand(True)
        hbox38.append(hbox38_lbl)
        self.arcolinux_fish.set_margin_start(10)
        self.arcolinux_fish.set_margin_end(10)
        hbox38.append(self.arcolinux_fish)  # pack_end
        self.fish_reset.set_margin_start(10)
        self.fish_reset.set_margin_end(10)
        hbox38.append(self.fish_reset)  # pack_end

        hbox34 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox34_lbl = Gtk.Label()
        hbox34_lbl.set_markup(
            "Restart your terminal to apply the new Fish theme\n\
\nYou will find scripts in your ~/.config/fish \
folder to install oh-my-fish, theme and plugins\n\
if you installed the ATT Fish configuration\n\n<b>If you just switched shell, log-out first</b>\n"
        )
        hbox34_lbl.set_margin_top(20)
        hbox34_lbl.set_margin_start(10)
        hbox34_lbl.set_margin_end(10)
        hbox34.append(hbox34_lbl)

        # ==========================================================
        #                     BUTTONS
        # ==========================================================

        hbox35 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        tofish = Gtk.Button(label="Apply fish")
        tofish.connect("clicked", self.tofish_apply)
        tobash = Gtk.Button(label="Apply bash")
        tobash.connect("clicked", self.tobash_apply)
        tozsh = Gtk.Button(label="Apply zsh")
        tozsh.connect("clicked", self.tozsh_apply)
        termreset = Gtk.Button(label="Reset fish")
        termreset.connect("clicked", self.on_fish_reset_clicked)
        remove_fish_all = Gtk.Button(label="Remove all Fish related packages")
        remove_fish_all.connect("clicked", self.on_remove_fish_all)

        if not fn.distr == "archcraft":
            hbox35.append(tofish)
        hbox35.append(tobash)
        hbox35.append(tozsh)
        hbox35.append(termreset)  # pack_end
        hbox35.append(remove_fish_all)  # pack_end

        # ==========================================================
        #                     VBOXSTACK
        # ==========================================================

        vboxstack3.append(hbox30)  # Combobox
        vboxstack3.append(hbox31)  # Combobox
        vboxstack3.append(hbox32)  # fish
        vboxstack3.append(hbox38)  # oh-my-fish
        vboxstack3.append(hbox33)  # oh-my-fish
        vboxstack3.append(hbox34)  # image
        vboxstack3.append(hbox35)  # pack_end  # Buttons

    else:
        # no fish installed
        hbox36 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox36_lbl = Gtk.Label(xalign=0)
        hbox36_lbl.set_markup("Fish is not installed")
        hbox36_lbl.set_name("title")
        hbox36.append(hbox36_lbl)

        hbox37 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox37.append(hseparator)

        message = Gtk.Label()
        message.set_markup(
            "<b>Fish does not seem to be installed\n\
Restart Att to see the information</b>"
        )

        install_only_fish = Gtk.Button(label="Install Fish - auto reboot")
        install_only_fish.connect("clicked", self.on_install_only_fish_clicked_reboot)

        vboxstack3.append(hbox36)
        vboxstack3.append(hbox37)
        vboxstack3.append(message)
        vboxstack3.append(install_only_fish)

    # ==================================================================
    #                       EXTRA
    # ==================================================================

    hbox51 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox51_lbl = Gtk.Label()
    hbox51_lbl.set_markup(
        "The shell configurations of the ATT contain\
 aliases that require certain applications\n\
\nHere you can select the missing applications and install them\n\
Activate the ArcoLinux repos to install all of them\n\n\
Applications that were NOT installed will be <b>unselected</b> again\n\
Activate the necessary repos"
    )
    self.select_all = Gtk.CheckButton(label="Select them all")
    self.select_all.connect("notify::active", self.on_select_all_toggle)
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
    self.yay = Gtk.CheckButton(label="yay")
    self.paru = Gtk.CheckButton(label="paru")
    self.bat = Gtk.CheckButton(label="bat")
    self.downgrade = Gtk.CheckButton(label="downgrade")
    self.hw_probe = Gtk.CheckButton(label="hw-probe")
    self.rate_mirrors = Gtk.CheckButton(label="rate-mirrors")
    self.most = Gtk.CheckButton(label="most")

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

    extra_shell_applications = Gtk.Button(label="Install these applications")
    extra_shell_applications.connect(
        "clicked", self.on_extra_shell_applications_clicked
    )

    vboxstack4.append(hbox51)
    # vboxstack4.pack_start(hbox52, False, False, 0)
    vboxstack4.append(flowbox)
    extra_shell_applications.set_hexpand(False)
    vboxstack4.append(extra_shell_applications)
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
