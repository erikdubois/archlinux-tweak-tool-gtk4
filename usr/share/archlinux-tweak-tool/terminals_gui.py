# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
import functions as fn


def gui(self, Gtk, vboxStack7, termite):
    """create a gui"""
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl1 = Gtk.Label(xalign=0)
    lbl1.set_text("Terminals")
    lbl1.set_name("title")
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox4.append(hseparator)
    hbox3.append(lbl1)

    # label25 = Gtk.Label()
    # label25.set_text("Termite themes :\n     Use the button to install - Select the theme here")
    # hbox25 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    # hbox25.pack_start(label25, False, False, 10)

    hbox01 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label01 = Gtk.Label()
    label01.set_markup("<b>URXVT</b>")
    label01.set_margin_start(10)
    label01.set_margin_end(10)
    hbox01.append(label01)

    label23 = Gtk.Label()
    label23.set_text("Urxvt themes - Change the settings of ~/.Xresources manually")
    hbox23 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label23.set_margin_start(10)
    label23.set_margin_end(10)
    hbox23.append(label23)

    hbox02 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    hbox02.set_margin_top(30)
    label02 = Gtk.Label()
    label02.set_markup("<b>ALACRITTY</b>")
    label02.set_margin_start(10)
    label02.set_margin_end(10)
    hbox02.append(label02)

    hbox06 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label06 = Gtk.Label()
    label06.set_markup(
        "Choose your Alcritty theme - type 'alacritty-themes' in the terminal"
    )
    label06.set_margin_start(10)
    label06.set_margin_end(10)
    hbox06.append(label06)

    hbox07 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label07 = Gtk.Label()
    if fn.check_package_installed("alacritty") == True:
        label07.set_markup("Alacritty already <b>installed</b>")
    else:
        label07.set_markup("Install Alacritty")
    btn_install_alacritty = Gtk.Button(label="Install Alacritty")
    btn_install_alacritty.connect("clicked", self.on_clicked_install_alacritty)
    label07.set_margin_start(10)
    label07.set_margin_end(10)
    label07.set_hexpand(True)
    hbox07.append(label07)
    btn_install_alacritty.set_margin_start(10)
    btn_install_alacritty.set_margin_end(10)
    hbox07.append(btn_install_alacritty)  # pack_end

    hbox03 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label03 = Gtk.Label()
    if fn.check_package_installed("alacritty-themes") == True:
        label03.set_markup("Alacritty-themes is already <b>installed</b>")
    else:
        label03.set_markup("Install Alacritty-themes")
    btn_install_alacritty_themes = Gtk.Button(label="Install Alacritty themes")
    btn_install_alacritty_themes.connect(
        "clicked", self.on_clicked_install_alacritty_themes
    )
    btn_remove_alacritty_themes = Gtk.Button(label="Remove Alacritty themes")
    btn_remove_alacritty_themes.connect(
        "clicked", self.on_clicked_remove_alacritty_themes
    )
    label03.set_margin_start(10)
    label03.set_margin_end(10)
    label03.set_hexpand(True)
    hbox03.append(label03)
    btn_install_alacritty_themes.set_margin_start(10)
    btn_install_alacritty_themes.set_margin_end(10)
    hbox03.append(btn_install_alacritty_themes)  # pack_end
    btn_remove_alacritty_themes.set_margin_start(10)
    btn_remove_alacritty_themes.set_margin_end(10)
    hbox03.append(btn_remove_alacritty_themes)  # pack_end

    hbox26 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    btn_set_att_alacritty_theme = Gtk.Button(label="Set ATT Alacritty-theme")
    btn_set_att_alacritty_theme.connect(
        "clicked", self.on_clicked_set_arcolinux_alacritty_theme_config
    )
    btn_reset_alacritty = Gtk.Button(label="Reset Alacritty theme")
    btn_reset_alacritty.connect("clicked", self.on_clicked_reset_alacritty)
    btn_reset_alacritty.set_margin_start(10)
    btn_reset_alacritty.set_margin_end(10)
    hbox26.append(btn_reset_alacritty)  # pack_end
    btn_set_att_alacritty_theme.set_margin_start(10)
    btn_set_att_alacritty_theme.set_margin_end(10)
    hbox26.append(btn_set_att_alacritty_theme)  # pack_end

    hbox04 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    hbox04.set_margin_top(0)
    label04 = Gtk.Label()
    label04.set_markup("<b>XFCE4-TERMINAL</b>")
    label04.set_margin_start(10)
    label04.set_margin_end(10)
    hbox04.append(label04)

    hbox27 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label27 = Gtk.Label()
    label27.set_markup(
        "Choose your Xfce4-terminal theme in the preferences,\
colors, presets of Xfce4-terminal"
    )
    label27.set_margin_start(10)
    label27.set_margin_end(10)
    hbox27.append(label27)

    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label28 = Gtk.Label()
    if fn.check_package_installed("xfce4-terminal"):
        label28.set_markup("Xfce4-terminal already <b>installed</b>")
    else:
        label28.set_markup("Install Xfce4-terminal")
    btn_install_xfce4_terminal = Gtk.Button(label="Install Xfce4-terminal")
    btn_install_xfce4_terminal.connect(
        "clicked", self.on_clicked_install_xfce4_terminal
    )
    btn_remove_xfce4_terminal = Gtk.Button(label="Remove Xfce4-terminal")
    btn_remove_xfce4_terminal.connect("clicked", self.on_clicked_remove_xfce4_terminal)
    label28.set_margin_start(10)
    label28.set_margin_end(10)
    label28.set_hexpand(True)
    hbox2.append(label28)
    btn_install_xfce4_terminal.set_margin_start(10)
    btn_install_xfce4_terminal.set_margin_end(10)
    hbox2.append(btn_install_xfce4_terminal)  # pack_end
    btn_remove_xfce4_terminal.set_margin_start(10)
    btn_remove_xfce4_terminal.set_margin_end(10)
    hbox2.append(btn_remove_xfce4_terminal)  # pack_end

    hbox28 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label08 = Gtk.Label()
    if fn.check_package_installed("xfce4-terminal-base16-colors-git"):
        label08.set_markup("Xfce4-terminal themes <b>installed</b>")
    else:
        label08.set_markup("Install all Xfce4-terminal themes")
    btn_install_xfce4_terminal_themes = Gtk.Button(
        label="Install Xfce4-terminal themes"
    )
    btn_install_xfce4_terminal_themes.connect(
        "clicked", self.on_clicked_install_xfce4_themes
    )
    btn_remove_xfce4_terminal_themes = Gtk.Button(label="Remove Xfce4-terminal themes")
    btn_remove_xfce4_terminal_themes.connect(
        "clicked", self.on_clicked_remove_xfce4_themes
    )
    label08.set_margin_start(10)
    label08.set_margin_end(10)
    label08.set_hexpand(True)
    hbox28.append(label08)
    btn_install_xfce4_terminal_themes.set_margin_start(10)
    btn_install_xfce4_terminal_themes.set_margin_end(10)
    hbox28.append(btn_install_xfce4_terminal_themes)  # pack_end
    btn_remove_xfce4_terminal_themes.set_margin_start(10)
    btn_remove_xfce4_terminal_themes.set_margin_end(10)
    hbox28.append(btn_remove_xfce4_terminal_themes)  # pack_end

    hbox29 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    btn_choose_xfce4_theme = Gtk.Button(label="Reset xfce4-terminal theme")
    btn_choose_xfce4_theme.connect("clicked", self.on_clicked_reset_xfce4_terminal)
    btn_choose_xfce4_theme.set_margin_start(10)
    btn_choose_xfce4_theme.set_margin_end(10)
    hbox29.append(btn_choose_xfce4_theme)  # pack_end

    hbox05 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    hbox05.set_margin_top(30)
    label05 = Gtk.Label()
    label05.set_markup("<b>TERMITE</b>")
    label05.set_margin_start(10)
    label05.set_margin_end(10)
    hbox05.append(label05)

    hbox24 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label24 = Gtk.Label()
    if fn.check_package_installed("termite"):
        label24.set_markup("Termite is already <b>installed</b>")
    else:
        label24.set_markup("Install Termite")
    btn_install_termite = Gtk.Button(label="Install Termite")
    btn_install_termite.connect("clicked", self.on_clicked_install_termite)
    btn_remove_termite = Gtk.Button(label="Remove Termite")
    btn_remove_termite.connect("clicked", self.on_clicked_remove_termite)
    label24.set_margin_start(10)
    label24.set_margin_end(10)
    label24.set_hexpand(True)
    hbox24.append(label24)
    btn_install_termite.set_margin_start(10)
    btn_install_termite.set_margin_end(10)
    hbox24.append(btn_install_termite)  # pack_end
    btn_remove_termite.set_margin_start(10)
    btn_remove_termite.set_margin_end(10)
    hbox24.append(btn_remove_termite)  # pack_end

    hbox21 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label21 = Gtk.Label()
    if fn.check_package_installed("arcolinux-termite-themes-git"):
        label21.set_markup("Termite themes are already <b>installed</b>")
    else:
        label21.set_markup("Install Termite themes")
    btn_install_termite_themes = Gtk.Button(label="Install Termite themes")
    btn_install_termite_themes.connect(
        "clicked", self.on_clicked_install_termite_themes
    )
    btn_remove_termite_themes = Gtk.Button(label="Remove Termite themes")
    btn_remove_termite_themes.connect("clicked", self.on_clicked_remove_termite_themes)
    label21.set_margin_start(10)
    label21.set_margin_end(10)
    label21.set_hexpand(True)
    hbox21.append(label21)
    btn_install_termite_themes.set_margin_start(10)
    btn_install_termite_themes.set_margin_end(10)
    hbox21.append(btn_install_termite_themes)  # pack_end
    btn_remove_termite_themes.set_margin_start(10)
    btn_remove_termite_themes.set_margin_end(10)
    hbox21.append(btn_remove_termite_themes)  # pack_end

    hbox22 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label22 = Gtk.Label()
    label22.set_markup("Remove the themes manually from ~/.config/termite")
    label22.set_margin_start(10)
    label22.set_margin_end(10)
    hbox22.append(label22)

    hbox19 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label19 = Gtk.Label()
    label19.set_markup("Choose your <b>Termite</b> theme")
    self.term_themes = Gtk.DropDown.new_from_strings([])
    termite.get_themes(self.term_themes)
    label19.set_margin_start(10)
    label19.set_margin_end(10)
    hbox19.append(label19)
    self.term_themes.set_hexpand(True)
    self.term_themes.set_vexpand(True)
    self.term_themes.set_margin_start(10)
    self.term_themes.set_margin_end(10)
    hbox19.append(self.term_themes)

    hbox20 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    termreset = Gtk.Button(label="Reset Termite")
    termreset.connect("clicked", self.on_term_reset)
    termset = Gtk.Button(label="Apply Termite theme")
    termset.connect("clicked", self.on_term_apply)
    hbox20.append(termreset)  # pack_end
    hbox20.append(termset)  # pack_end

    vboxStack7.append(hbox3)  # lbl1
    vboxStack7.append(hbox4)  # seperator
    #vboxStack7.pack_start(hbox01, False, False, 0)
    #vboxStack7.pack_start(hbox23, False, False, 0)
    #vboxStack7.pack_start(hbox02, False, False, 0)
    #vboxStack7.pack_start(hbox06, False, False, 0)
    vboxStack7.append(hbox07)
    #vboxStack7.pack_start(hbox03, False, False, 0)
    #vboxStack7.pack_start(hbox26, False, False, 0)
    vboxStack7.append(hbox04)
    vboxStack7.append(hbox27)
    vboxStack7.append(hbox2)
    #vboxStack7.pack_start(hbox28, False, False, 0)
    #vboxStack7.pack_start(hbox29, False, False, 0)
    #vboxStack7.pack_start(hbox05, False, False, 0)
    #vboxStack7.pack_start(hbox24, False, False, 0)
    #vboxStack7.pack_start(hbox21, False, False, 0)
    #vboxStack7.pack_start(hbox22, False, False, 0)
    #vboxStack7.pack_start(hbox19, False, False, 0)
    #vboxStack7.pack_start(hbox20, False, False, 0)
