# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0103,

import functools
import desktopr_gui
import themes
import functions_startup


def _att_preview_picture(Gtk, GdkPixbuf, Gdk, base_dir, filename, scale=1.0, out_pics=None):
    """Preview image wrapped in a Frame.

    out_pics: if provided, (pic, scale) is appended so the caller can update
    set_size_request dynamically via a size-allocate handler.
    """
    img_load = int(desktopr_gui.IMAGE_PREVIEW_LOAD * scale)
    img_min = int(desktopr_gui.IMAGE_PREVIEW_MIN * scale)
    pic = Gtk.Picture()
    try:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            base_dir + "/images/" + filename,
            img_load,
            img_load,
        )
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        pic.set_paintable(texture)
    except Exception:
        pass
    pic.set_can_shrink(True)
    pic.set_content_fit(Gtk.ContentFit.SCALE_DOWN)
    pic.set_size_request(img_min, img_min)
    pic.set_hexpand(True)
    pic.set_vexpand(False)
    pic.set_halign(Gtk.Align.CENTER)
    pic.set_valign(Gtk.Align.CENTER)
    frame = Gtk.Frame(label="Preview")
    frame.set_child(pic)
    frame.set_hexpand(True)
    frame.set_vexpand(True)
    frame.set_margin_start(10)
    frame.set_margin_end(10)
    frame.set_margin_top(10)
    frame.set_margin_bottom(10)
    if out_pics is not None:
        out_pics.append((pic, scale))
    return frame


def gui(self, Gtk, GdkPixbuf, vboxstack_themes, themes_module, fn, base_dir):
    """create themes gui"""
    from gi.repository import Gdk

    # Setup icon/cursor theme defaults on-demand
    functions_startup.setup_icon_theme()

    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_title = Gtk.Label(xalign=0)
    lbl_title.set_text("Themes")
    lbl_title.set_name("title")
    hbox_title.append(lbl_title)

    hbox_separator = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox_separator.append(hseparator)

    hbox_info = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_info_label = Gtk.Label(xalign=0)
    hbox_info_label.set_markup(
        'Select the packages you want to install or remove, then click the appropriate button.\n\
Ensure that the <b>Nemesis repository is enabled</b> — see the "Pacman" tab for details.\n\
Check if /etc/environment sets your GTK_THEME, and if so, change it there'
    )

    hbox_info_label.set_margin_start(10)
    hbox_info_label.set_margin_end(10)
    hbox_info.append(hbox_info_label)

    hbox_checkboxes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    self.arcolinux_arc_aqua = Gtk.CheckButton(label="arcolinux-arc-aqua")
    self.arcolinux_arc_archlinux_blue = Gtk.CheckButton(
        label="arcolinux-arc-archlinux-blue"
    )
    self.arcolinux_arc_arcolinux_blue = Gtk.CheckButton(
        label="arcolinux-arc-arcolinux-blue"
    )
    self.arcolinux_arc_azul = Gtk.CheckButton(label="arcolinux-arc-azul")
    self.arcolinux_arc_azure = Gtk.CheckButton(label="arcolinux-arc-azure")
    self.arcolinux_arc_azure_dodger_blue = Gtk.CheckButton(
        label="arcolinux-arc-azure-dodger-blue"
    )
    self.arcolinux_arc_blood = Gtk.CheckButton(label="arcolinux-arc-blood")
    self.arcolinux_arc_blue_sky = Gtk.CheckButton(label="arcolinux-arc-blue-sky")
    self.arcolinux_arc_botticelli = Gtk.CheckButton(label="arcolinux-arc-botticelli")
    self.arcolinux_arc_bright_lilac = Gtk.CheckButton(
        label="arcolinux-arc-bright-lilac"
    )
    self.arcolinux_arc_carnation = Gtk.CheckButton(label="arcolinux-arc-carnation")
    self.arcolinux_arc_carolina_blue = Gtk.CheckButton(
        label="arcolinux-arc-carolina-blue"
    )
    self.arcolinux_arc_casablanca = Gtk.CheckButton(label="arcolinux-arc-casablanca")
    self.arcolinux_arc_crimson = Gtk.CheckButton(label="arcolinux-arc-crimson")
    self.arcolinux_arc_dawn = Gtk.CheckButton(label="arcolinux-arc-dawn")
    self.arcolinux_arc_dodger_blue = Gtk.CheckButton(label="arcolinux-arc-dodger-blue")
    self.arcolinux_arc_dracul = Gtk.CheckButton(label="arcolinux-arc-dracul")
    self.arcolinux_arc_emerald = Gtk.CheckButton(label="arcolinux-arc-emerald")
    self.arcolinux_arc_evopop = Gtk.CheckButton(label="arcolinux-arc-evopop")
    self.arcolinux_arc_fern = Gtk.CheckButton(label="arcolinux-arc-fern")
    self.arcolinux_arc_fire = Gtk.CheckButton(label="arcolinux-arc-fire")
    self.arcolinux_arc_froly = Gtk.CheckButton(label="arcolinux-arc-froly")
    self.arcolinux_arc_havelock = Gtk.CheckButton(label="arcolinux-arc-havelock")
    self.arcolinux_arc_hibiscus = Gtk.CheckButton(label="arcolinux-arc-hibiscus")
    self.arcolinux_arc_light_blue_grey = Gtk.CheckButton(
        label="arcolinux-arc-light-blue-grey"
    )
    self.arcolinux_arc_light_blue_surfn = Gtk.CheckButton(
        label="arcolinux-arc-light-blue-surfn"
    )
    self.arcolinux_arc_light_salmon = Gtk.CheckButton(
        label="arcolinux-arc-light-salmon"
    )
    self.arcolinux_arc_mandy = Gtk.CheckButton(label="arcolinux-arc-mandy")
    self.arcolinux_arc_mantis = Gtk.CheckButton(label="arcolinux-arc-mantis")
    self.arcolinux_arc_medium_blue = Gtk.CheckButton(label="arcolinux-arc-medium-blue")
    self.arcolinux_arc_niagara = Gtk.CheckButton(label="arcolinux-arc-niagara")
    self.arcolinux_arc_nice_blue = Gtk.CheckButton(label="arcolinux-arc-nice-blue")
    self.arcolinux_arc_numix = Gtk.CheckButton(label="arcolinux-arc-numix")
    self.arcolinux_arc_orchid = Gtk.CheckButton(label="arcolinux-arc-orchid")
    self.arcolinux_arc_pale_grey = Gtk.CheckButton(label="arcolinux-arc-pale-grey")
    self.arcolinux_arc_paper = Gtk.CheckButton(label="arcolinux-arc-paper")
    self.arcolinux_arc_pink = Gtk.CheckButton(label="arcolinux-arc-pink")
    self.arcolinux_arc_polo = Gtk.CheckButton(label="arcolinux-arc-polo")
    self.arcolinux_arc_punch = Gtk.CheckButton(label="arcolinux-arc-punch")
    self.arcolinux_arc_red_orange = Gtk.CheckButton(label="arcolinux-arc-red-orange")
    self.arcolinux_arc_rusty_orange = Gtk.CheckButton(
        label="arcolinux-arc-rusty-orange"
    )
    self.arcolinux_arc_sky_blue = Gtk.CheckButton(label="arcolinux-arc-sky-blue")
    self.arcolinux_arc_slate_grey = Gtk.CheckButton(label="arcolinux-arc-slate-grey")
    self.arcolinux_arc_smoke = Gtk.CheckButton(label="arcolinux-arc-smoke")
    self.arcolinux_arc_soft_blue = Gtk.CheckButton(label="arcolinux-arc-soft-blue")
    self.arcolinux_arc_tacao = Gtk.CheckButton(label="arcolinux-arc-tacao")
    self.arcolinux_arc_tangerine = Gtk.CheckButton(label="arcolinux-arc-tangerine")
    self.arcolinux_arc_tory = Gtk.CheckButton(label="arcolinux-arc-tory")
    self.arcolinux_arc_vampire = Gtk.CheckButton(label="arcolinux-arc-vampire")
    self.arcolinux_arc_warm_pink = Gtk.CheckButton(label="arcolinux-arc-warm-pink")

    flowbox_themes = Gtk.FlowBox()
    flowbox_themes.set_valign(Gtk.Align.START)
    flowbox_themes.set_max_children_per_line(10)
    flowbox_themes.set_selection_mode(Gtk.SelectionMode.NONE)

    flowbox_themes.append(self.arcolinux_arc_aqua)
    flowbox_themes.append(self.arcolinux_arc_archlinux_blue)
    flowbox_themes.append(self.arcolinux_arc_arcolinux_blue)
    flowbox_themes.append(self.arcolinux_arc_azul)
    flowbox_themes.append(self.arcolinux_arc_azure)
    flowbox_themes.append(self.arcolinux_arc_azure_dodger_blue)
    flowbox_themes.append(self.arcolinux_arc_blood)
    flowbox_themes.append(self.arcolinux_arc_blue_sky)
    flowbox_themes.append(self.arcolinux_arc_botticelli)
    flowbox_themes.append(self.arcolinux_arc_bright_lilac)
    flowbox_themes.append(self.arcolinux_arc_carnation)
    flowbox_themes.append(self.arcolinux_arc_carolina_blue)
    flowbox_themes.append(self.arcolinux_arc_casablanca)
    flowbox_themes.append(self.arcolinux_arc_crimson)
    flowbox_themes.append(self.arcolinux_arc_dawn)
    flowbox_themes.append(self.arcolinux_arc_dodger_blue)
    flowbox_themes.append(self.arcolinux_arc_dracul)
    flowbox_themes.append(self.arcolinux_arc_emerald)
    flowbox_themes.append(self.arcolinux_arc_evopop)
    flowbox_themes.append(self.arcolinux_arc_fern)
    flowbox_themes.append(self.arcolinux_arc_fire)
    flowbox_themes.append(self.arcolinux_arc_froly)
    flowbox_themes.append(self.arcolinux_arc_havelock)
    flowbox_themes.append(self.arcolinux_arc_hibiscus)
    flowbox_themes.append(self.arcolinux_arc_light_blue_grey)
    flowbox_themes.append(self.arcolinux_arc_light_blue_surfn)
    flowbox_themes.append(self.arcolinux_arc_light_salmon)
    flowbox_themes.append(self.arcolinux_arc_mandy)
    flowbox_themes.append(self.arcolinux_arc_mantis)
    flowbox_themes.append(self.arcolinux_arc_medium_blue)
    flowbox_themes.append(self.arcolinux_arc_niagara)
    flowbox_themes.append(self.arcolinux_arc_nice_blue)
    flowbox_themes.append(self.arcolinux_arc_numix)
    flowbox_themes.append(self.arcolinux_arc_orchid)
    flowbox_themes.append(self.arcolinux_arc_pale_grey)
    flowbox_themes.append(self.arcolinux_arc_paper)
    flowbox_themes.append(self.arcolinux_arc_pink)
    flowbox_themes.append(self.arcolinux_arc_polo)
    flowbox_themes.append(self.arcolinux_arc_punch)
    flowbox_themes.append(self.arcolinux_arc_red_orange)
    flowbox_themes.append(self.arcolinux_arc_rusty_orange)
    flowbox_themes.append(self.arcolinux_arc_sky_blue)
    flowbox_themes.append(self.arcolinux_arc_slate_grey)
    flowbox_themes.append(self.arcolinux_arc_smoke)
    flowbox_themes.append(self.arcolinux_arc_soft_blue)
    flowbox_themes.append(self.arcolinux_arc_tacao)
    flowbox_themes.append(self.arcolinux_arc_tangerine)
    flowbox_themes.append(self.arcolinux_arc_tory)
    flowbox_themes.append(self.arcolinux_arc_vampire)
    flowbox_themes.append(self.arcolinux_arc_warm_pink)

    flowbox_themes.set_hexpand(True)
    flowbox_themes.set_vexpand(True)
    flowbox_themes.set_margin_start(10)
    flowbox_themes.set_margin_end(10)
    hbox_checkboxes.append(flowbox_themes)

    hbox_presets = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    hbox_presets.set_hexpand(True)
    label18 = Gtk.Label()
    label18.set_text("Choose what to select with a button")
    btn_all_selection_themes = Gtk.Button(label="All")
    btn_all_selection_themes.connect("clicked", functools.partial(themes.on_click_att_theming_all_selection, self))
    btn_blue_selection_themes = Gtk.Button(label="Blue")
    btn_blue_selection_themes.connect(
        "clicked", functools.partial(themes.on_click_att_theming_blue_selection, self)
    )
    btn_dark_selection_themes = Gtk.Button(label="Dark")
    btn_dark_selection_themes.connect(
        "clicked", functools.partial(themes.on_click_att_theming_dark_selection, self)
    )
    btn_none_selection_themes = Gtk.Button(label="None")
    btn_none_selection_themes.connect(
        "clicked", functools.partial(themes.on_click_att_theming_none_selection, self)
    )
    label18.set_margin_start(10)
    label18.set_margin_end(10)
    label18.set_hexpand(True)
    label18.set_xalign(0)
    hbox_presets.append(label18)
    btn_all_selection_themes.set_margin_start(10)
    btn_all_selection_themes.set_margin_end(10)
    hbox_presets.append(btn_all_selection_themes)
    btn_dark_selection_themes.set_margin_start(10)
    btn_dark_selection_themes.set_margin_end(10)
    hbox_presets.append(btn_dark_selection_themes)
    btn_blue_selection_themes.set_margin_start(10)
    btn_blue_selection_themes.set_margin_end(10)
    hbox_presets.append(btn_blue_selection_themes)
    btn_none_selection_themes.set_margin_start(10)
    btn_none_selection_themes.set_margin_end(10)
    hbox_presets.append(btn_none_selection_themes)

    hbox_actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_install_themes = Gtk.Button(label="Install the selected themes")
    button_install_themes.connect("clicked", functools.partial(themes.on_install_att_themes_clicked, self))
    button_remove_themes = Gtk.Button(label="Uninstall the selected themes")
    button_remove_themes.connect("clicked", functools.partial(themes.on_remove_att_themes_clicked, self))
    button_find_themes = Gtk.Button(label="Show the installed themes")
    button_find_themes.connect("clicked", functools.partial(themes.on_find_att_themes_clicked, self))

    button_remove_themes.set_margin_start(10)
    button_remove_themes.set_margin_end(10)
    button_remove_themes.set_hexpand(True)
    hbox_actions.append(button_remove_themes)
    button_find_themes.set_margin_start(10)
    button_find_themes.set_margin_end(10)
    hbox_actions.append(button_find_themes)
    button_install_themes.set_margin_start(10)
    button_install_themes.set_margin_end(10)
    hbox_actions.append(button_install_themes)

    _themes_pics = []

    vboxstack_themes.append(hbox_title)
    vboxstack_themes.append(hbox_separator)

    hbox_info.set_margin_start(10)
    hbox_info.set_margin_end(10)
    vboxstack_themes.append(hbox_info)
    hbox_checkboxes.set_margin_start(10)
    hbox_checkboxes.set_margin_end(10)
    vboxstack_themes.append(hbox_checkboxes)
    vboxstack_themes.append(
        _att_preview_picture(Gtk, GdkPixbuf, Gdk, base_dir, "arcthemes.jpg", scale=1, out_pics=_themes_pics)
    )
    hbox_presets.set_margin_start(10)
    hbox_presets.set_margin_end(10)
    vboxstack_themes.append(hbox_presets)
    vboxstack_themes.append(hbox_actions)

    return _themes_pics
