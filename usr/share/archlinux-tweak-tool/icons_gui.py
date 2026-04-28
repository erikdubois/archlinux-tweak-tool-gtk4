# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0103,

import functools
import desktopr_gui
import icons


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
    # can_shrink=True: Picture accepts allocation smaller than the pixbuf's natural
    # size, so SCALE_DOWN fires when the size_request is updated on resize.
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


def gui(self, Gtk, GdkPixbuf, vboxstack25, att, fn, base_dir):
    """create a gui"""
    from gi.repository import Gdk
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl1 = Gtk.Label(xalign=0)
    lbl1.set_text("Icons")
    lbl1.set_name("title")
    hbox3.append(lbl1)

    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox4.append(hseparator)

    # ==========================================================
    #                     DESIGN
    # ==========================================================

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

    vboxstack2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack2.set_hexpand(True)
    vboxstack2.set_vexpand(True)
    vboxstack3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack3.set_hexpand(True)
    vboxstack3.set_vexpand(True)
    vboxstack4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack4.set_hexpand(True)
    vboxstack4.set_vexpand(True)

    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
    stack.set_transition_duration(350)
    stack.set_hhomogeneous(False)
    stack.set_vhomogeneous(False)

    stack_switcher = Gtk.StackSwitcher()
    stack_switcher.set_orientation(Gtk.Orientation.HORIZONTAL)
    stack_switcher.set_stack(stack)

    # ==================================================================
    #                       ICONS TAB - SARDI
    # ==================================================================

    hbox20 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox20_label = Gtk.Label(xalign=0)
    hbox20_label.set_markup(
        'Select the packages you want to install or remove, then click the appropriate button.\n\
Ensure that the <b>Nemesis repository is enabled</b> — see the "Pacman" tab for details.'
    )
    hbox20_label.set_margin_start(10)
    hbox20_label.set_margin_end(10)
    hbox20.append(hbox20_label)

    hbox21 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    self.sardi_icons_att = Gtk.CheckButton(label="sardi-icons")
    self.sardi_colora_variations_icons_git = Gtk.CheckButton(
        label="sardi-colora-variations-icons"
    )
    self.sardi_flat_colora_variations_icons_git = Gtk.CheckButton(
        label="sardi-flat-colora-variations-icons"
    )
    self.sardi_flat_mint_y_icons_git = Gtk.CheckButton(
        label="sardi-flat-mint-y-icons"
    )
    self.sardi_flat_mixing_icons_git = Gtk.CheckButton(
        label="sardi-flat-mixing-icons"
    )
    self.sardi_flexible_colora_variations_icons_git = Gtk.CheckButton(
        label="sardi-flexible-colora-variations-icons"
    )
    self.sardi_flexible_luv_colora_variations_icons_git = Gtk.CheckButton(
        label="sardi-flexible-luv-colora-variations-icons"
    )
    self.sardi_flexible_mint_y_icons_git = Gtk.CheckButton(
        label="sardi-flexible-mint-y-icons"
    )
    self.sardi_flexible_mixing_icons_git = Gtk.CheckButton(
        label="sardi-flexible-mixing-icons"
    )
    self.sardi_flexible_variations_icons_git = Gtk.CheckButton(
        label="sardi-flexible-variations-icons"
    )
    self.sardi_ghost_flexible_colora_variations_icons_git = Gtk.CheckButton(
        label="sardi-ghost-flexible-colora-variations-icons"
    )
    self.sardi_ghost_flexible_mint_y_icons_git = Gtk.CheckButton(
        label="sardi-ghost-flexible-mint-y-icons"
    )
    self.sardi_ghost_flexible_mixing_icons_git = Gtk.CheckButton(
        label="sardi-ghost-flexible-mixing-icons"
    )
    self.sardi_ghost_flexible_variations_icons_git = Gtk.CheckButton(
        label="sardi-ghost-flexible-variations-icons"
    )
    self.sardi_mint_y_icons_git = Gtk.CheckButton(label="sardi-mint-y-icons")
    self.sardi_mixing_icons_git = Gtk.CheckButton(label="sardi-mixing-icons")
    self.sardi_mono_colora_variations_icons_git = Gtk.CheckButton(
        label="sardi-mono-colora-variations-icons"
    )
    self.sardi_mono_mint_y_icons_git = Gtk.CheckButton(
        label="sardi-mono-mint-y-icons"
    )
    self.sardi_mono_mixing_icons_git = Gtk.CheckButton(
        label="sardi-mono-mixing-icons"
    )
    self.sardi_mono_numix_colora_variations_icons_git = Gtk.CheckButton(
        label="sardi-mono-numix-colora-variations-icons"
    )
    self.sardi_mono_papirus_colora_variations_icons_git = Gtk.CheckButton(
        label="sardi-mono-papirus-colora-variations-icons"
    )
    self.sardi_orb_colora_mint_y_icons_git = Gtk.CheckButton(
        label="sardi-orb-colora-mint-y-icons"
    )
    self.sardi_orb_colora_mixing_icons_git = Gtk.CheckButton(
        label="sardi-orb-colora-mixing-icons"
    )
    self.sardi_orb_colora_variations_icons_git = Gtk.CheckButton(
        label="sardi-orb-colora-variations-icons"
    )

    flowbox_sardi = Gtk.FlowBox()
    flowbox_sardi.set_valign(Gtk.Align.START)
    flowbox_sardi.set_max_children_per_line(10)
    flowbox_sardi.set_selection_mode(Gtk.SelectionMode.NONE)

    flowbox_sardi.append(self.sardi_icons_att)
    flowbox_sardi.append(self.sardi_colora_variations_icons_git)
    flowbox_sardi.append(self.sardi_flat_colora_variations_icons_git)
    flowbox_sardi.append(self.sardi_flat_mint_y_icons_git)
    flowbox_sardi.append(self.sardi_flat_mixing_icons_git)
    flowbox_sardi.append(self.sardi_flexible_colora_variations_icons_git)
    flowbox_sardi.append(self.sardi_flexible_luv_colora_variations_icons_git)
    flowbox_sardi.append(self.sardi_flexible_mint_y_icons_git)
    flowbox_sardi.append(self.sardi_flexible_mixing_icons_git)
    flowbox_sardi.append(self.sardi_flexible_variations_icons_git)
    flowbox_sardi.append(self.sardi_ghost_flexible_colora_variations_icons_git)
    flowbox_sardi.append(self.sardi_ghost_flexible_mint_y_icons_git)
    flowbox_sardi.append(self.sardi_ghost_flexible_mixing_icons_git)
    flowbox_sardi.append(self.sardi_ghost_flexible_variations_icons_git)
    flowbox_sardi.append(self.sardi_mint_y_icons_git)
    flowbox_sardi.append(self.sardi_mixing_icons_git)
    flowbox_sardi.append(self.sardi_mono_colora_variations_icons_git)
    flowbox_sardi.append(self.sardi_mono_mint_y_icons_git)
    flowbox_sardi.append(self.sardi_mono_mixing_icons_git)
    flowbox_sardi.append(self.sardi_mono_numix_colora_variations_icons_git)
    flowbox_sardi.append(self.sardi_mono_papirus_colora_variations_icons_git)
    flowbox_sardi.append(self.sardi_orb_colora_mint_y_icons_git)
    flowbox_sardi.append(self.sardi_orb_colora_mixing_icons_git)
    flowbox_sardi.append(self.sardi_orb_colora_variations_icons_git)

    flowbox_sardi.set_hexpand(True)
    flowbox_sardi.set_vexpand(True)
    flowbox_sardi.set_margin_start(10)
    flowbox_sardi.set_margin_end(10)
    hbox21.append(flowbox_sardi)

    hbox23 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label23 = Gtk.Label()
    label23.set_text("Choose what to select with a button")
    btn_all_sardi = Gtk.Button(label="All")
    btn_all_sardi.connect("clicked", functools.partial(icons.on_click_att_sardi_icon_theming_all_selection, self))
    btn_mint_sardi = Gtk.Button(label="Mint")
    btn_mint_sardi.connect(
        "clicked", functools.partial(icons.on_click_att_sardi_icon_theming_mint_selection, self)
    )
    btn_mixing_sardi = Gtk.Button(label="Mixing")
    btn_mixing_sardi.connect(
        "clicked", functools.partial(icons.on_click_att_sardi_icon_theming_mixing_selection, self)
    )
    btn_variation_sardi = Gtk.Button(label="Variations")
    btn_variation_sardi.connect(
        "clicked", functools.partial(icons.on_click_att_sardi_icon_theming_variations_selection, self)
    )
    btn_none_sardi = Gtk.Button(label="None")
    btn_none_sardi.connect(
        "clicked", functools.partial(icons.on_click_att_sardi_icon_theming_none_selection, self)
    )
    label23.set_margin_start(10)
    label23.set_margin_end(10)
    hbox23.append(label23)
    btn_all_sardi.set_margin_start(10)
    btn_all_sardi.set_margin_end(10)
    hbox23.append(btn_all_sardi)
    btn_variation_sardi.set_margin_start(10)
    btn_variation_sardi.set_margin_end(10)
    hbox23.append(btn_variation_sardi)
    btn_mixing_sardi.set_margin_start(10)
    btn_mixing_sardi.set_margin_end(10)
    hbox23.append(btn_mixing_sardi)
    btn_mint_sardi.set_margin_start(10)
    btn_mint_sardi.set_margin_end(10)
    hbox23.append(btn_mint_sardi)
    btn_none_sardi.set_margin_start(10)
    btn_none_sardi.set_margin_end(10)
    hbox23.append(btn_none_sardi)

    # families
    hbox22 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label22 = Gtk.Label()
    label22.set_text("Choose the family with a button")
    btn_sardi_fam = Gtk.Button(label="Sardi")
    btn_sardi_fam.connect(
        "clicked", functools.partial(icons.on_click_att_fam_sardi_icon_theming_sardi_selection, self)
    )
    btn_sardi_flexible_fam = Gtk.Button(label="Sardi Flexible")
    btn_sardi_flexible_fam.connect(
        "clicked", functools.partial(icons.on_click_att_fam_sardi_icon_theming_sardi_flexible_selection, self)
    )
    btn_sardi_mono_fam = Gtk.Button(label="Sardi Mono")
    btn_sardi_mono_fam.connect(
        "clicked", functools.partial(icons.on_click_att_fam_sardi_icon_theming_sardi_mono_selection, self)
    )
    btn_sardi_flat_fam = Gtk.Button(label="Sardi Flat")
    btn_sardi_flat_fam.connect(
        "clicked", functools.partial(icons.on_click_att_fam_sardi_icon_theming_sardi_flat_selection, self)
    )
    btn_sardi_ghost_fam = Gtk.Button(label="Sardi Ghost")
    btn_sardi_ghost_fam.connect(
        "clicked", functools.partial(icons.on_click_att_fam_sardi_icon_theming_sardi_ghost_selection, self)
    )
    btn_sardi_orb_fam = Gtk.Button(label="Sardi Orb")
    btn_sardi_orb_fam.connect(
        "clicked", functools.partial(icons.on_click_att_fam_sardi_icon_theming_sardi_orb_selection, self)
    )
    label22.set_margin_start(10)
    label22.set_margin_end(10)
    hbox22.append(label22)
    btn_sardi_fam.set_margin_start(10)
    btn_sardi_fam.set_margin_end(10)
    hbox22.append(btn_sardi_fam)
    btn_sardi_flexible_fam.set_margin_start(10)
    btn_sardi_flexible_fam.set_margin_end(10)
    hbox22.append(btn_sardi_flexible_fam)
    btn_sardi_mono_fam.set_margin_start(10)
    btn_sardi_mono_fam.set_margin_end(10)
    hbox22.append(btn_sardi_mono_fam)
    btn_sardi_flat_fam.set_margin_start(10)
    btn_sardi_flat_fam.set_margin_end(10)
    hbox22.append(btn_sardi_flat_fam)
    btn_sardi_ghost_fam.set_margin_start(10)
    btn_sardi_ghost_fam.set_margin_end(10)
    hbox22.append(btn_sardi_ghost_fam)
    btn_sardi_orb_fam.set_margin_start(10)
    btn_sardi_orb_fam.set_margin_end(10)
    hbox22.append(btn_sardi_orb_fam)

    hbox29 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_install_sardi = Gtk.Button(label="Install the selected icon themes")
    button_install_sardi.connect(
        "clicked", functools.partial(icons.on_install_att_sardi_icon_themes_clicked, self)
    )
    button_find_sardi_icons = Gtk.Button(label="Show the installed icon themes")
    button_find_sardi_icons.connect(
        "clicked", functools.partial(icons.on_find_att_sardi_icon_themes_clicked, self)
    )
    button_remove_sardi_icons = Gtk.Button(label="Uninstall the selected icon themes")
    button_remove_sardi_icons.connect(
        "clicked", functools.partial(icons.on_remove_att_sardi_icon_themes_clicked, self)
    )
    button_remove_sardi_icons.set_margin_start(10)
    button_remove_sardi_icons.set_margin_end(10)
    button_remove_sardi_icons.set_hexpand(True)
    hbox29.append(button_remove_sardi_icons)
    button_find_sardi_icons.set_margin_start(10)
    button_find_sardi_icons.set_margin_end(10)
    hbox29.append(button_find_sardi_icons)
    button_install_sardi.set_margin_start(10)
    button_install_sardi.set_margin_end(10)
    hbox29.append(button_install_sardi)  # pack_end

    # ==================================================================
    #                       ICONS TAB - SURFN
    # ==================================================================

    hbox30 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox30_label = Gtk.Label(xalign=0)
    hbox30_label.set_markup(
        'Select the packages you want to install or remove, then click the appropriate button.\n\
Ensure that the <b>Nemesis repository is enabled</b> — see the "Pacman" tab for details.'
    )
    hbox30_label.set_margin_start(10)
    hbox30_label.set_margin_end(10)
    hbox30.append(hbox30_label)

    hbox31 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    self.surfn_icons_git_att = Gtk.CheckButton(label="surfn-icons")
    self.surfn_arc_breeze_icons_git = Gtk.CheckButton(
        label="surfn-arc-breeze-icons"
    )
    self.surfn_mint_y_icons_git = Gtk.CheckButton(label="surfn-mint-y-icons")
    self.surfn_plasma_dark = Gtk.CheckButton(label="surfn-plasma-dark")
    self.surfn_plasma_light = Gtk.CheckButton(label="surfn-plasma-light")
    self.surfn_plasma_flow = Gtk.CheckButton(label="surfn-plasma-flow")

    flowbox_surfn = Gtk.FlowBox()
    flowbox_surfn.set_valign(Gtk.Align.START)
    flowbox_surfn.set_max_children_per_line(10)
    flowbox_surfn.set_selection_mode(Gtk.SelectionMode.NONE)

    flowbox_surfn.append(self.surfn_icons_git_att)
    flowbox_surfn.append(self.surfn_arc_breeze_icons_git)
    flowbox_surfn.append(self.surfn_mint_y_icons_git)
    flowbox_surfn.append(self.surfn_plasma_dark)
    flowbox_surfn.append(self.surfn_plasma_light)
    flowbox_surfn.append(self.surfn_plasma_flow)

    flowbox_surfn.set_hexpand(True)
    flowbox_surfn.set_vexpand(True)
    flowbox_surfn.set_margin_start(10)
    flowbox_surfn.set_margin_end(10)
    hbox31.append(flowbox_surfn)

    hbox32 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label32 = Gtk.Label()
    label32.set_text("Choose what to select with a button")
    btn_all_surfn = Gtk.Button(label="All")
    btn_all_surfn.connect("clicked", functools.partial(icons.on_click_att_surfn_theming_all_selection, self))
    # btn_normal_selection = Gtk.Button(label="Normal")
    # btn_normal_selection.connect(
    #     "clicked", self.on_click_att_surfn_theming_normal_selection
    # )
    # btn_small_selection = Gtk.Button(label="Minimal")
    # btn_small_selection.connect(
    #     "clicked", self.on_click_att_surfn_theming_minimal_selection
    # )
    btn_none_surfn = Gtk.Button(label="None")
    btn_none_surfn.connect("clicked", functools.partial(icons.on_click_att_surfn_theming_none_selection, self))
    label32.set_margin_start(10)
    label32.set_margin_end(10)
    label32.set_hexpand(True)
    hbox32.append(label32)
    btn_none_surfn.set_margin_start(10)
    btn_none_surfn.set_margin_end(10)
    hbox32.append(btn_none_surfn)  # pack_end
    # hbox32.pack_end(btn_small_selection, False, False, 10)
    # hbox32.pack_end(btn_normal_selection, False, False, 10)
    btn_all_surfn.set_margin_start(10)
    btn_all_surfn.set_margin_end(10)
    hbox32.append(btn_all_surfn)  # pack_end

    hbox39 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_install_surfn_icons = Gtk.Button(label="Install the selected icon themes")
    button_install_surfn_icons.connect(
        "clicked", functools.partial(icons.on_install_att_surfn_icon_themes_clicked, self)
    )
    button_find_surfn_icons = Gtk.Button(label="Show the installed icon themes")
    button_find_surfn_icons.connect(
        "clicked", functools.partial(icons.on_find_att_surfn_icon_themes_clicked, self)
    )
    button_remove_surfn_icons = Gtk.Button(label="Uninstall the selected icon themes")
    button_remove_surfn_icons.connect(
        "clicked", functools.partial(icons.on_remove_att_surfn_icon_themes_clicked, self)
    )
    button_remove_surfn_icons.set_margin_start(10)
    button_remove_surfn_icons.set_margin_end(10)
    button_remove_surfn_icons.set_hexpand(True)
    hbox39.append(button_remove_surfn_icons)
    button_find_surfn_icons.set_margin_start(10)
    button_find_surfn_icons.set_margin_end(10)
    hbox39.append(button_find_surfn_icons)
    button_install_surfn_icons.set_margin_start(10)
    button_install_surfn_icons.set_margin_end(10)
    hbox39.append(button_install_surfn_icons)  # pack_end

    # ==================================================================
    #                       EXTRAS TAB
    # ==================================================================

    hbox40 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox40_label = Gtk.Label(xalign=0)
    hbox40_label.set_markup(
        'Select the packages you want to install or remove, then click the appropriate button.\n\
Ensure that the <b>Nemesis repository is enabled</b> — see the "Pacman" tab for details.'
    )
    hbox40_label.set_margin_start(10)
    hbox40_label.set_margin_end(10)
    hbox40.append(hbox40_label)

    hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    self.att_candy_beauty = Gtk.CheckButton(label="Neo Candy Icons")
    self.edu_candy_beauty_arc = Gtk.CheckButton(label="Edu Neo Candy Arc")
    self.edu_candy_beauty_arc_mint_grey = Gtk.CheckButton(
        label="Edu Neo Candy Arc Mint Grey"
    )
    self.edu_candy_beauty_arc_mint_red = Gtk.CheckButton(
        label="Edu Neo Candy Arc Mint Red"
    )
    self.edu_candy_beauty_tela = Gtk.CheckButton(label="Edu Neo Candy Tela")
    self.edu_papirus_dark_tela = Gtk.CheckButton(label="Edu Papirus Dark Tela")
    self.edu_papirus_dark_tela_grey = Gtk.CheckButton(
        label="Edu Papirus Dark Tela Grey "
    )
    self.edu_vimix_dark_tela = Gtk.CheckButton(label="Edu Vimix Dark Tela")

    flowbox_extra = Gtk.FlowBox()
    flowbox_extra.set_valign(Gtk.Align.START)
    flowbox_extra.set_max_children_per_line(10)
    flowbox_extra.set_selection_mode(Gtk.SelectionMode.NONE)

    flowbox_extra.append(self.att_candy_beauty)
    flowbox_extra.append(self.edu_candy_beauty_arc)
    flowbox_extra.append(self.edu_candy_beauty_arc_mint_grey)
    flowbox_extra.append(self.edu_candy_beauty_arc_mint_red)
    flowbox_extra.append(self.edu_candy_beauty_tela)
    flowbox_extra.append(self.edu_papirus_dark_tela)
    flowbox_extra.append(self.edu_papirus_dark_tela_grey)
    flowbox_extra.append(self.edu_vimix_dark_tela)

    flowbox_extra.set_hexpand(True)
    flowbox_extra.set_vexpand(True)
    flowbox_extra.set_margin_start(10)
    flowbox_extra.set_margin_end(10)
    hbox41.append(flowbox_extra)

    hbox42 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label42 = Gtk.Label()
    label42.set_text("Choose what to select with a button")
    btn_all_extra = Gtk.Button(label="All")
    btn_all_extra.connect("clicked", functools.partial(icons.on_click_extras_theming_all_selection, self))
    btn_none_extra = Gtk.Button(label="None")
    btn_none_extra.connect("clicked", functools.partial(icons.on_click_extras_theming_none_selection, self))
    label42.set_margin_start(10)
    label42.set_margin_end(10)
    label42.set_hexpand(True)
    hbox42.append(label42)
    btn_all_extra.set_margin_start(10)
    btn_all_extra.set_margin_end(10)
    hbox42.append(btn_all_extra)  # pack_end
    btn_none_extra.set_margin_start(10)
    btn_none_extra.set_margin_end(10)
    hbox42.append(btn_none_extra)  # pack_end

    hbox49 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_install_icons = Gtk.Button(label="Install the selected packages")
    button_install_icons.connect("clicked", functools.partial(icons.on_install_extras_clicked, self))
    button_find_icons = Gtk.Button(label="Show  the installed packages")
    button_find_icons.connect("clicked", functools.partial(icons.on_find_extras_clicked, self))
    button_remove_icons = Gtk.Button(label="Uninstall the selected packages")
    button_remove_icons.connect("clicked", functools.partial(icons.on_remove_extras_clicked, self))
    button_remove_icons.set_margin_start(10)
    button_remove_icons.set_margin_end(10)
    button_remove_icons.set_hexpand(True)
    hbox49.append(button_remove_icons)
    button_find_icons.set_margin_start(10)
    button_find_icons.set_margin_end(10)
    hbox49.append(button_find_icons)
    button_install_icons.set_margin_start(10)
    button_install_icons.set_margin_end(10)
    hbox49.append(button_install_icons)  # pack_end

    # ====================================================================
    #                       STACK
    # ====================================================================

    _att_pics = []  # collects (pic, scale) for the resize handler below

    # icons
    hbox20.set_margin_start(10)
    hbox20.set_margin_end(10)
    vboxstack2.append(hbox20)
    hbox21.set_margin_start(10)
    hbox21.set_margin_end(10)
    vboxstack2.append(hbox21)
    vboxstack2.append(_att_preview_picture(Gtk, GdkPixbuf, Gdk, base_dir, "sardi.jpg", out_pics=_att_pics))
    hbox23.set_margin_start(10)
    hbox23.set_margin_end(10)
    vboxstack2.append(hbox23)
    hbox22.set_margin_start(10)
    hbox22.set_margin_end(10)
    vboxstack2.append(hbox22)
    vboxstack2.append(hbox29)

    # cursors
    hbox30.set_margin_start(10)
    hbox30.set_margin_end(10)
    vboxstack3.append(hbox30)
    hbox31.set_margin_start(10)
    hbox31.set_margin_end(10)
    vboxstack3.append(hbox31)
    vboxstack3.append(_att_preview_picture(Gtk, GdkPixbuf, Gdk, base_dir, "surfn.jpg", scale=0.8, out_pics=_att_pics))
    hbox32.set_margin_start(10)
    hbox32.set_margin_end(10)
    vboxstack3.append(hbox32)
    vboxstack3.append(hbox39)

    # fonts
    hbox40.set_margin_start(10)
    hbox40.set_margin_end(10)
    vboxstack4.append(hbox40)
    hbox41.set_margin_start(10)
    hbox41.set_margin_end(10)
    vboxstack4.append(hbox41)
    vboxstack4.append(
        _att_preview_picture(Gtk, GdkPixbuf, Gdk, base_dir, "neocandy.jpg", scale=0.8, out_pics=_att_pics)
    )
    hbox42.set_margin_start(10)
    hbox42.set_margin_end(10)
    vboxstack4.append(hbox42)
    vboxstack4.append(hbox49)

    # ==================================================================
    #                       PACK TO STACK
    # ==================================================================

    stack.add_titled(vboxstack4, "stack4", "Neo Candy")
    stack.add_titled(vboxstack2, "stack2", "Sardi")
    stack.add_titled(vboxstack3, "stack3", "Surfn")

    vbox.append(stack_switcher)
    stack.set_hexpand(True)
    stack.set_vexpand(True)
    vbox.append(stack)

    vboxstack25.append(hbox3)
    vboxstack25.append(hbox4)
    vbox.set_hexpand(True)
    vbox.set_vexpand(True)
    vboxstack25.append(vbox)

    # Responsive images: recompute size_request whenever the window is resized.
    # notify::default-width fires as the user drags to resize in GTK4.
    def _on_att_resize(win, _pspec):
        new_size = max(100, min(desktopr_gui.IMAGE_PREVIEW_MIN,
                                int(win.get_width() * 0.2)))
        for pic, scale in _att_pics:
            s = max(50, int(new_size * scale))
            pic.set_size_request(s, s)

    self.connect("notify::default-width", _on_att_resize)
