# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn


def _check_install_repos(self):
    nemesis_ok = fn.check_nemesis_repo_active()
    chaotic_ok = fn.check_chaotic_aur_active()
    if not nemesis_ok and not chaotic_ok:
        msg = "Neither nemesis_repo nor chaotic-aur is enabled — add them in the Pacman tab before installing"
        fn.log_info(msg)
        fn.show_in_app_notification(self, msg)
        return False
    if not nemesis_ok:
        msg = "nemesis_repo is not enabled — enable it in the Pacman tab for full icon theme support"
        fn.log_info(msg)
        fn.show_in_app_notification(self, msg)
    if not chaotic_ok:
        msg = "chaotic-aur is not enabled — enable it in the Pacman tab for full icon theme support"
        fn.log_info(msg)
        fn.show_in_app_notification(self, msg)
    return True


def on_click_att_sardi_icon_theming_all_selection(self, _widget):
    fn.log_subsection("All Sardi icons selected")
    fn.show_in_app_notification(self, "We have selected all sardi icons")
    set_att_checkboxes_theming_sardi_icons_all(self)


def on_click_att_sardi_icon_theming_mint_selection(self, _widget):
    fn.log_subsection("Mint selection applied - Sardi icons")
    fn.show_in_app_notification(
        self, "We have selected the mint selection - sardi icons"
    )
    set_att_checkboxes_theming_sardi_mint_icons(self)


def on_click_att_sardi_icon_theming_mixing_selection(self, _widget):
    fn.log_subsection("Mixing selection applied - Sardi icons")
    fn.show_in_app_notification(
        self, "We have selected the mixing selection - sardi icons"
    )
    set_att_checkboxes_theming_sardi_mixing_icons(self)


def on_click_att_sardi_icon_theming_variations_selection(self, _widget):
    fn.log_subsection("Variations selection applied - Sardi icons")
    fn.show_in_app_notification(
        self, "We have selected the variation selection - sardi icons"
    )
    set_att_checkboxes_theming_sardi_icons_variations(self)


def on_click_att_sardi_icon_theming_none_selection(self, _widget):
    fn.log_subsection("No Sardi icons selected")
    fn.show_in_app_notification(self, "We have selected no sardiicons")
    set_att_checkboxes_theming_sardi_icons_none(self)


def on_click_att_fam_sardi_icon_theming_sardi_selection(self, _widget):
    fn.log_subsection("Sardi family selected")
    fn.show_in_app_notification(self, "We have selected the Sardi family themes")
    set_att_fam_checkboxes_theming_sardi_icons(self)


def on_click_att_fam_sardi_icon_theming_sardi_flexible_selection(self, _widget):
    fn.log_subsection("Sardi flexible family selected")
    fn.show_in_app_notification(
        self, "We have selected the Sardi flexible family themes"
    )
    set_att_fam_checkboxes_theming_sardi_flexible(self)


def on_click_att_fam_sardi_icon_theming_sardi_mono_selection(self, _widget):
    fn.log_subsection("Sardi mono family selected")
    fn.show_in_app_notification(
        self, "We have selected the Sardi mono family themes"
    )
    set_att_fam_checkboxes_theming_sardi_mono(self)


def on_click_att_fam_sardi_icon_theming_sardi_flat_selection(self, _widget):
    fn.log_subsection("Sardi flat family selected")
    fn.show_in_app_notification(
        self, "We have selected the Sardi flat family themes"
    )
    set_att_fam_checkboxes_theming_sardi_flat(self)


def on_click_att_fam_sardi_icon_theming_sardi_ghost_selection(self, _widget):
    fn.log_subsection("Sardi ghost family selected")
    fn.show_in_app_notification(
        self, "We have selected the Sardi ghost family themes"
    )
    set_att_fam_checkboxes_theming_sardi_ghost(self)


def on_click_att_fam_sardi_icon_theming_sardi_orb_selection(self, _widget):
    fn.log_subsection("Sardi orb family selected")
    fn.show_in_app_notification(
        self, "We have selected the Sardi orb family themes"
    )
    set_att_fam_checkboxes_theming_sardi_orb(self)


def on_click_att_surfn_theming_all_selection(self, _widget):
    fn.log_subsection("All Surfn icons selected")
    fn.show_in_app_notification(self, "We have selected all surfn icons")
    set_att_checkboxes_theming_surfn_icons_all(self)


def on_click_att_surfn_theming_none_selection(self, _widget):
    fn.log_subsection("No Surfn icons selected")
    fn.show_in_app_notification(self, "We have selected no surfn icons")
    set_att_checkboxes_theming_surfn_icons_none(self)


def on_install_extras_clicked(self, _widget):
    fn.log_subsection("Installing selected Neo Candy icon packages...")
    install_att_extras(self)


def on_remove_extras_clicked(self, _widget):
    fn.log_subsection("Removing selected Neo Candy icon packages...")
    remove_att_extras(self)


def on_find_extras_clicked(self, _widget):
    fn.log_subsection("Showing installed projects...")
    fn.show_in_app_notification(self, "We show the installed icon themes")
    find_att_extras(self)


def on_click_extras_theming_all_selection(self, _widget):
    fn.log_subsection("All projects selected")
    fn.show_in_app_notification(self, "We have selected all icon themes")
    set_att_checkboxes_extras_all(self)


def on_click_extras_theming_none_selection(self, _widget):
    fn.log_subsection("No projects selected")
    fn.show_in_app_notification(self, "We have selected none of the icon themes")
    set_att_checkboxes_extras_none(self)


def on_install_att_sardi_icon_themes_clicked(self, _widget):
    fn.log_subsection("Installing selected Sardi icon themes...")
    install_sardi_icons(self)


def on_remove_att_sardi_icon_themes_clicked(self, _widget):
    fn.log_subsection("Removing selected Sardi icon themes...")
    remove_sardi_icons(self)


def on_find_att_sardi_icon_themes_clicked(self, _widget):
    fn.log_subsection("Showing installed Sardi icon themes...")
    fn.show_in_app_notification(self, "We show the installed icon themes")
    find_sardi_icons(self)


def on_install_att_surfn_icon_themes_clicked(self, _widget):
    fn.log_subsection("Installing selected Surfn icon themes...")
    install_surfn_icons(self)


def on_remove_att_surfn_icon_themes_clicked(self, _widget):
    fn.log_subsection("Removing selected Surfn icon themes...")
    remove_surfn_icons(self)


def on_find_att_surfn_icon_themes_clicked(self, _widget):
    fn.log_subsection("Showing all installed Surfn icon themes...")
    fn.show_in_app_notification(self, "We show the installed icon themes")
    find_surfn_icons(self)


# choices
def set_att_checkboxes_theming_sardi_icons_all(self):
    self.sardi_icons_att.set_active(True)
    self.sardi_colora_variations_icons_git.set_active(True)
    self.sardi_flat_colora_variations_icons_git.set_active(True)
    self.sardi_flat_mint_y_icons_git.set_active(True)
    self.sardi_flat_mixing_icons_git.set_active(True)
    self.sardi_flexible_colora_variations_icons_git.set_active(True)
    self.sardi_flexible_luv_colora_variations_icons_git.set_active(True)
    self.sardi_flexible_mint_y_icons_git.set_active(True)
    self.sardi_flexible_mixing_icons_git.set_active(True)
    self.sardi_flexible_variations_icons_git.set_active(True)
    self.sardi_ghost_flexible_colora_variations_icons_git.set_active(True)
    self.sardi_ghost_flexible_mint_y_icons_git.set_active(True)
    self.sardi_ghost_flexible_mixing_icons_git.set_active(True)
    self.sardi_ghost_flexible_variations_icons_git.set_active(True)
    self.sardi_mint_y_icons_git.set_active(True)
    self.sardi_mixing_icons_git.set_active(True)
    self.sardi_mono_colora_variations_icons_git.set_active(True)
    self.sardi_mono_mint_y_icons_git.set_active(True)
    self.sardi_mono_mixing_icons_git.set_active(True)
    self.sardi_mono_numix_colora_variations_icons_git.set_active(True)
    self.sardi_mono_papirus_colora_variations_icons_git.set_active(True)
    self.sardi_orb_colora_mint_y_icons_git.set_active(True)
    self.sardi_orb_colora_mixing_icons_git.set_active(True)
    self.sardi_orb_colora_variations_icons_git.set_active(True)


def set_att_checkboxes_theming_sardi_mint_icons(self):

    self.sardi_icons_att.set_active(True)
    self.sardi_colora_variations_icons_git.set_active(False)
    self.sardi_flat_colora_variations_icons_git.set_active(False)
    self.sardi_flat_mint_y_icons_git.set_active(True)
    self.sardi_flat_mixing_icons_git.set_active(False)
    self.sardi_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_luv_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_mint_y_icons_git.set_active(True)
    self.sardi_flexible_mixing_icons_git.set_active(False)
    self.sardi_flexible_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_mint_y_icons_git.set_active(True)
    self.sardi_ghost_flexible_mixing_icons_git.set_active(False)
    self.sardi_ghost_flexible_variations_icons_git.set_active(False)
    self.sardi_mint_y_icons_git.set_active(True)
    self.sardi_mixing_icons_git.set_active(False)
    self.sardi_mono_colora_variations_icons_git.set_active(False)
    self.sardi_mono_mint_y_icons_git.set_active(True)
    self.sardi_mono_mixing_icons_git.set_active(False)
    self.sardi_mono_numix_colora_variations_icons_git.set_active(False)
    self.sardi_mono_papirus_colora_variations_icons_git.set_active(False)
    self.sardi_orb_colora_mint_y_icons_git.set_active(True)
    self.sardi_orb_colora_mixing_icons_git.set_active(False)
    self.sardi_orb_colora_variations_icons_git.set_active(False)


def set_att_checkboxes_theming_sardi_mixing_icons(self):

    self.sardi_icons_att.set_active(True)
    self.sardi_colora_variations_icons_git.set_active(False)
    self.sardi_flat_colora_variations_icons_git.set_active(False)
    self.sardi_flat_mint_y_icons_git.set_active(False)
    self.sardi_flat_mixing_icons_git.set_active(True)
    self.sardi_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_luv_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_mint_y_icons_git.set_active(False)
    self.sardi_flexible_mixing_icons_git.set_active(True)
    self.sardi_flexible_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_mint_y_icons_git.set_active(False)
    self.sardi_ghost_flexible_mixing_icons_git.set_active(True)
    self.sardi_ghost_flexible_variations_icons_git.set_active(False)
    self.sardi_mint_y_icons_git.set_active(False)
    self.sardi_mixing_icons_git.set_active(True)
    self.sardi_mono_colora_variations_icons_git.set_active(False)
    self.sardi_mono_mint_y_icons_git.set_active(False)
    self.sardi_mono_mixing_icons_git.set_active(True)
    self.sardi_mono_numix_colora_variations_icons_git.set_active(False)
    self.sardi_mono_papirus_colora_variations_icons_git.set_active(False)
    self.sardi_orb_colora_mint_y_icons_git.set_active(False)
    self.sardi_orb_colora_mixing_icons_git.set_active(True)
    self.sardi_orb_colora_variations_icons_git.set_active(False)


def set_att_checkboxes_theming_sardi_icons_variations(self):

    self.sardi_icons_att.set_active(True)
    self.sardi_colora_variations_icons_git.set_active(True)
    self.sardi_flat_colora_variations_icons_git.set_active(True)
    self.sardi_flat_mint_y_icons_git.set_active(False)
    self.sardi_flat_mixing_icons_git.set_active(False)
    self.sardi_flexible_colora_variations_icons_git.set_active(True)
    self.sardi_flexible_luv_colora_variations_icons_git.set_active(True)
    self.sardi_flexible_mint_y_icons_git.set_active(False)
    self.sardi_flexible_mixing_icons_git.set_active(False)
    self.sardi_flexible_variations_icons_git.set_active(True)
    self.sardi_ghost_flexible_colora_variations_icons_git.set_active(True)
    self.sardi_ghost_flexible_mint_y_icons_git.set_active(False)
    self.sardi_ghost_flexible_mixing_icons_git.set_active(False)
    self.sardi_ghost_flexible_variations_icons_git.set_active(True)
    self.sardi_mint_y_icons_git.set_active(False)
    self.sardi_mixing_icons_git.set_active(False)
    self.sardi_mono_colora_variations_icons_git.set_active(True)
    self.sardi_mono_mint_y_icons_git.set_active(False)
    self.sardi_mono_mixing_icons_git.set_active(False)
    self.sardi_mono_numix_colora_variations_icons_git.set_active(True)
    self.sardi_mono_papirus_colora_variations_icons_git.set_active(True)
    self.sardi_orb_colora_mint_y_icons_git.set_active(False)
    self.sardi_orb_colora_mixing_icons_git.set_active(False)
    self.sardi_orb_colora_variations_icons_git.set_active(True)


def set_att_checkboxes_theming_sardi_icons_none(self):

    self.sardi_icons_att.set_active(False)
    self.sardi_colora_variations_icons_git.set_active(False)
    self.sardi_flat_colora_variations_icons_git.set_active(False)
    self.sardi_flat_mint_y_icons_git.set_active(False)
    self.sardi_flat_mixing_icons_git.set_active(False)
    self.sardi_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_luv_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_mint_y_icons_git.set_active(False)
    self.sardi_flexible_mixing_icons_git.set_active(False)
    self.sardi_flexible_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_mint_y_icons_git.set_active(False)
    self.sardi_ghost_flexible_mixing_icons_git.set_active(False)
    self.sardi_ghost_flexible_variations_icons_git.set_active(False)
    self.sardi_mint_y_icons_git.set_active(False)
    self.sardi_mixing_icons_git.set_active(False)
    self.sardi_mono_colora_variations_icons_git.set_active(False)
    self.sardi_mono_mint_y_icons_git.set_active(False)
    self.sardi_mono_mixing_icons_git.set_active(False)
    self.sardi_mono_numix_colora_variations_icons_git.set_active(False)
    self.sardi_mono_papirus_colora_variations_icons_git.set_active(False)
    self.sardi_orb_colora_mint_y_icons_git.set_active(False)
    self.sardi_orb_colora_mixing_icons_git.set_active(False)
    self.sardi_orb_colora_variations_icons_git.set_active(False)


# Families


def set_att_fam_checkboxes_theming_sardi_icons(self):
    self.sardi_icons_att.set_active(True)
    self.sardi_colora_variations_icons_git.set_active(True)
    self.sardi_flat_colora_variations_icons_git.set_active(False)
    self.sardi_flat_mint_y_icons_git.set_active(False)
    self.sardi_flat_mixing_icons_git.set_active(False)
    self.sardi_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_luv_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_mint_y_icons_git.set_active(False)
    self.sardi_flexible_mixing_icons_git.set_active(False)
    self.sardi_flexible_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_mint_y_icons_git.set_active(False)
    self.sardi_ghost_flexible_mixing_icons_git.set_active(False)
    self.sardi_ghost_flexible_variations_icons_git.set_active(False)
    self.sardi_mint_y_icons_git.set_active(False)
    self.sardi_mixing_icons_git.set_active(True)
    self.sardi_mono_colora_variations_icons_git.set_active(False)
    self.sardi_mono_mint_y_icons_git.set_active(False)
    self.sardi_mono_mixing_icons_git.set_active(False)
    self.sardi_mono_numix_colora_variations_icons_git.set_active(False)
    self.sardi_mono_papirus_colora_variations_icons_git.set_active(False)
    self.sardi_orb_colora_mint_y_icons_git.set_active(False)
    self.sardi_orb_colora_mixing_icons_git.set_active(False)
    self.sardi_orb_colora_variations_icons_git.set_active(False)


def set_att_fam_checkboxes_theming_sardi_flexible(self):

    self.sardi_icons_att.set_active(False)
    self.sardi_colora_variations_icons_git.set_active(False)
    self.sardi_flat_colora_variations_icons_git.set_active(False)
    self.sardi_flat_mint_y_icons_git.set_active(False)
    self.sardi_flat_mixing_icons_git.set_active(False)
    self.sardi_flexible_colora_variations_icons_git.set_active(True)
    self.sardi_flexible_luv_colora_variations_icons_git.set_active(True)
    self.sardi_flexible_mint_y_icons_git.set_active(True)
    self.sardi_flexible_mixing_icons_git.set_active(True)
    self.sardi_flexible_variations_icons_git.set_active(True)
    self.sardi_ghost_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_mint_y_icons_git.set_active(False)
    self.sardi_ghost_flexible_mixing_icons_git.set_active(False)
    self.sardi_ghost_flexible_variations_icons_git.set_active(False)
    self.sardi_mint_y_icons_git.set_active(False)
    self.sardi_mixing_icons_git.set_active(False)
    self.sardi_mono_colora_variations_icons_git.set_active(False)
    self.sardi_mono_mint_y_icons_git.set_active(False)
    self.sardi_mono_mixing_icons_git.set_active(False)
    self.sardi_mono_numix_colora_variations_icons_git.set_active(False)
    self.sardi_mono_papirus_colora_variations_icons_git.set_active(False)
    self.sardi_orb_colora_mint_y_icons_git.set_active(False)
    self.sardi_orb_colora_mixing_icons_git.set_active(False)
    self.sardi_orb_colora_variations_icons_git.set_active(False)


def set_att_fam_checkboxes_theming_sardi_mono(self):

    self.sardi_icons_att.set_active(False)
    self.sardi_colora_variations_icons_git.set_active(False)
    self.sardi_flat_colora_variations_icons_git.set_active(False)
    self.sardi_flat_mint_y_icons_git.set_active(False)
    self.sardi_flat_mixing_icons_git.set_active(False)
    self.sardi_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_luv_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_mint_y_icons_git.set_active(False)
    self.sardi_flexible_mixing_icons_git.set_active(False)
    self.sardi_flexible_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_mint_y_icons_git.set_active(False)
    self.sardi_ghost_flexible_mixing_icons_git.set_active(False)
    self.sardi_ghost_flexible_variations_icons_git.set_active(False)
    self.sardi_mint_y_icons_git.set_active(False)
    self.sardi_mixing_icons_git.set_active(False)
    self.sardi_mono_colora_variations_icons_git.set_active(True)
    self.sardi_mono_mint_y_icons_git.set_active(True)
    self.sardi_mono_mixing_icons_git.set_active(True)
    self.sardi_mono_numix_colora_variations_icons_git.set_active(True)
    self.sardi_mono_papirus_colora_variations_icons_git.set_active(True)
    self.sardi_orb_colora_mint_y_icons_git.set_active(False)
    self.sardi_orb_colora_mixing_icons_git.set_active(False)
    self.sardi_orb_colora_variations_icons_git.set_active(False)


def set_att_fam_checkboxes_theming_sardi_flat(self):

    self.sardi_icons_att.set_active(False)
    self.sardi_colora_variations_icons_git.set_active(False)
    self.sardi_flat_colora_variations_icons_git.set_active(True)
    self.sardi_flat_mint_y_icons_git.set_active(True)
    self.sardi_flat_mixing_icons_git.set_active(True)
    self.sardi_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_luv_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_mint_y_icons_git.set_active(False)
    self.sardi_flexible_mixing_icons_git.set_active(False)
    self.sardi_flexible_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_mint_y_icons_git.set_active(False)
    self.sardi_ghost_flexible_mixing_icons_git.set_active(False)
    self.sardi_ghost_flexible_variations_icons_git.set_active(False)
    self.sardi_mint_y_icons_git.set_active(False)
    self.sardi_mixing_icons_git.set_active(False)
    self.sardi_mono_colora_variations_icons_git.set_active(False)
    self.sardi_mono_mint_y_icons_git.set_active(False)
    self.sardi_mono_mixing_icons_git.set_active(False)
    self.sardi_mono_numix_colora_variations_icons_git.set_active(False)
    self.sardi_mono_papirus_colora_variations_icons_git.set_active(False)
    self.sardi_orb_colora_mint_y_icons_git.set_active(False)
    self.sardi_orb_colora_mixing_icons_git.set_active(False)
    self.sardi_orb_colora_variations_icons_git.set_active(False)


def set_att_fam_checkboxes_theming_sardi_ghost(self):

    self.sardi_icons_att.set_active(False)
    self.sardi_colora_variations_icons_git.set_active(False)
    self.sardi_flat_colora_variations_icons_git.set_active(False)
    self.sardi_flat_mint_y_icons_git.set_active(False)
    self.sardi_flat_mixing_icons_git.set_active(False)
    self.sardi_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_luv_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_mint_y_icons_git.set_active(False)
    self.sardi_flexible_mixing_icons_git.set_active(False)
    self.sardi_flexible_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_colora_variations_icons_git.set_active(True)
    self.sardi_ghost_flexible_mint_y_icons_git.set_active(True)
    self.sardi_ghost_flexible_mixing_icons_git.set_active(True)
    self.sardi_ghost_flexible_variations_icons_git.set_active(True)
    self.sardi_mint_y_icons_git.set_active(False)
    self.sardi_mixing_icons_git.set_active(False)
    self.sardi_mono_colora_variations_icons_git.set_active(False)
    self.sardi_mono_mint_y_icons_git.set_active(False)
    self.sardi_mono_mixing_icons_git.set_active(False)
    self.sardi_mono_numix_colora_variations_icons_git.set_active(False)
    self.sardi_mono_papirus_colora_variations_icons_git.set_active(False)
    self.sardi_orb_colora_mint_y_icons_git.set_active(False)
    self.sardi_orb_colora_mixing_icons_git.set_active(False)
    self.sardi_orb_colora_variations_icons_git.set_active(False)


def set_att_fam_checkboxes_theming_sardi_orb(self):

    self.sardi_icons_att.set_active(False)
    self.sardi_colora_variations_icons_git.set_active(False)
    self.sardi_flat_colora_variations_icons_git.set_active(False)
    self.sardi_flat_mint_y_icons_git.set_active(False)
    self.sardi_flat_mixing_icons_git.set_active(False)
    self.sardi_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_luv_colora_variations_icons_git.set_active(False)
    self.sardi_flexible_mint_y_icons_git.set_active(False)
    self.sardi_flexible_mixing_icons_git.set_active(False)
    self.sardi_flexible_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_colora_variations_icons_git.set_active(False)
    self.sardi_ghost_flexible_mint_y_icons_git.set_active(False)
    self.sardi_ghost_flexible_mixing_icons_git.set_active(False)
    self.sardi_ghost_flexible_variations_icons_git.set_active(False)
    self.sardi_mint_y_icons_git.set_active(False)
    self.sardi_mixing_icons_git.set_active(False)
    self.sardi_mono_colora_variations_icons_git.set_active(False)
    self.sardi_mono_mint_y_icons_git.set_active(False)
    self.sardi_mono_mixing_icons_git.set_active(False)
    self.sardi_mono_numix_colora_variations_icons_git.set_active(False)
    self.sardi_mono_papirus_colora_variations_icons_git.set_active(False)
    self.sardi_orb_colora_mint_y_icons_git.set_active(True)
    self.sardi_orb_colora_mixing_icons_git.set_active(True)
    self.sardi_orb_colora_variations_icons_git.set_active(True)


def _collect_sardi_packages(self):
    pairs = [
        (self.sardi_icons_att, "sardi-icons"),
        (self.sardi_colora_variations_icons_git, "sardi-colora-variations-icons-git"),
        (self.sardi_flat_colora_variations_icons_git, "sardi-flat-colora-variations-icons-git"),
        (self.sardi_flat_mint_y_icons_git, "sardi-flat-mint-y-icons-git"),
        (self.sardi_flat_mixing_icons_git, "sardi-flat-mixing-icons-git"),
        (self.sardi_flexible_colora_variations_icons_git, "sardi-flexible-colora-variations-icons-git"),
        (self.sardi_flexible_luv_colora_variations_icons_git, "sardi-flexible-luv-colora-variations-icons-git"),
        (self.sardi_flexible_mint_y_icons_git, "sardi-flexible-mint-y-icons-git"),
        (self.sardi_flexible_mixing_icons_git, "sardi-flexible-mixing-icons-git"),
        (self.sardi_flexible_variations_icons_git, "sardi-flexible-variations-icons-git"),
        (self.sardi_ghost_flexible_colora_variations_icons_git, "sardi-ghost-flexible-colora-variations-icons-git"),
        (self.sardi_ghost_flexible_mint_y_icons_git, "sardi-ghost-flexible-mint-y-icons-git"),
        (self.sardi_ghost_flexible_mixing_icons_git, "sardi-ghost-flexible-mixing-icons-git"),
        (self.sardi_ghost_flexible_variations_icons_git, "sardi-ghost-flexible-variations-icons-git"),
        (self.sardi_mint_y_icons_git, "sardi-mint-y-icons-git"),
        (self.sardi_mixing_icons_git, "sardi-mixing-icons-git"),
        (self.sardi_mono_colora_variations_icons_git, "sardi-mono-colora-variations-icons-git"),
        (self.sardi_mono_mint_y_icons_git, "sardi-mono-mint-y-icons-git"),
        (self.sardi_mono_mixing_icons_git, "sardi-mono-mixing-icons-git"),
        (self.sardi_mono_numix_colora_variations_icons_git, "sardi-mono-numix-colora-variations-icons-git"),
        (self.sardi_mono_papirus_colora_variations_icons_git, "sardi-mono-papirus-colora-variations-icons-git"),
        (self.sardi_orb_colora_mint_y_icons_git, "sardi-orb-colora-mint-y-icons-git"),
        (self.sardi_orb_colora_mixing_icons_git, "sardi-orb-colora-mixing-icons-git"),
        (self.sardi_orb_colora_variations_icons_git, "sardi-orb-colora-variations-icons-git"),
    ]
    return [pkg for cb, pkg in pairs if cb.get_active()]


def install_sardi_icons(self):
    if not _check_install_repos(self):
        return
    packages = _collect_sardi_packages(self)
    if not packages:
        fn.log_info("No Sardi icons selected for installation")
        fn.show_in_app_notification(self, "No Sardi icons selected for installation")
        return
    fn.log_subsection(f"Installing {len(packages)} Sardi icon packages...")
    fn.log_info(f"  {', '.join(packages)}")
    process = fn.launch_pacman_install_in_terminal(" ".join(packages))
    fn.show_in_app_notification(self, f"Installing {len(packages)} Sardi icon packages...")
    fn.wait_and_notify(process, self, "Sardi icons installation complete")


def remove_sardi_icons(self):
    packages = _collect_sardi_packages(self)
    if not packages:
        fn.log_info("No Sardi icons selected for removal")
        fn.show_in_app_notification(self, "No Sardi icons selected for removal")
        return
    fn.log_subsection(f"Removing {len(packages)} Sardi icon packages...")
    fn.log_info(f"  {', '.join(packages)}")
    process = fn.launch_pacman_remove_in_terminal(" ".join(packages))
    fn.show_in_app_notification(self, f"Removing {len(packages)} Sardi icon packages...")
    fn.wait_and_notify(process, self, "Sardi icons removal complete")


def find_sardi_icons(self):
    set_att_checkboxes_theming_sardi_icons_none(self)

    # find which ones are installed
    if fn.check_package_installed("sardi-icons"):
        self.sardi_icons_att.set_active(True)
    if fn.check_package_installed("sardi-colora-variations-icons-git"):
        self.sardi_colora_variations_icons_git.set_active(True)
    if fn.check_package_installed("sardi-flat-colora-variations-icons-git"):
        self.sardi_flat_colora_variations_icons_git.set_active(True)
    if fn.check_package_installed("sardi-flat-mint-y-icons-git"):
        self.sardi_flat_mint_y_icons_git.set_active(True)
    if fn.check_package_installed("sardi-flat-mixing-icons-git"):
        self.sardi_flat_mixing_icons_git.set_active(True)
    if fn.check_package_installed("sardi-flexible-colora-variations-icons-git"):
        self.sardi_flexible_colora_variations_icons_git.set_active(True)
    if fn.check_package_installed("sardi-flexible-luv-colora-variations-icons-git"):
        self.sardi_flexible_luv_colora_variations_icons_git.set_active(True)
    if fn.check_package_installed("sardi-flexible-mint-y-icons-git"):
        self.sardi_flexible_mint_y_icons_git.set_active(True)
    if fn.check_package_installed("sardi-flexible-mixing-icons-git"):
        self.sardi_flexible_mixing_icons_git.set_active(True)
    if fn.check_package_installed("sardi-flexible-variations-icons-git"):
        self.sardi_flexible_variations_icons_git.set_active(True)
    if fn.check_package_installed("sardi-ghost-flexible-colora-variations-icons-git"):
        self.sardi_ghost_flexible_colora_variations_icons_git.set_active(True)
    if fn.check_package_installed("sardi-ghost-flexible-mint-y-icons-git"):
        self.sardi_ghost_flexible_mint_y_icons_git.set_active(True)
    if fn.check_package_installed("sardi-ghost-flexible-mixing-icons-git"):
        self.sardi_ghost_flexible_mixing_icons_git.set_active(True)
    if fn.check_package_installed("sardi-ghost-flexible-variations-icons-git"):
        self.sardi_ghost_flexible_variations_icons_git.set_active(True)
    if fn.check_package_installed("sardi-mint-y-icons-git"):
        self.sardi_mint_y_icons_git.set_active(True)
    if fn.check_package_installed("sardi-mixing-icons-git"):
        self.sardi_mixing_icons_git.set_active(True)
    if fn.check_package_installed("sardi-mono-colora-variations-icons-git"):
        self.sardi_mono_colora_variations_icons_git.set_active(True)
    if fn.check_package_installed("sardi-mono-mint-y-icons-git"):
        self.sardi_mono_mint_y_icons_git.set_active(True)
    if fn.check_package_installed("sardi-mono-mixing-icons-git"):
        self.sardi_mono_mixing_icons_git.set_active(True)
    if fn.check_package_installed("sardi-mono-numix-colora-variations-icons-git"):
        self.sardi_mono_numix_colora_variations_icons_git.set_active(True)
    if fn.check_package_installed("sardi-mono-papirus-colora-variations-icons-git"):
        self.sardi_mono_papirus_colora_variations_icons_git.set_active(True)
    if fn.check_package_installed("sardi-orb-colora-mint-y-icons-git"):
        self.sardi_orb_colora_mint_y_icons_git.set_active(True)
    if fn.check_package_installed("sardi-orb-colora-mixing-icons-git"):
        self.sardi_orb_colora_mixing_icons_git.set_active(True)
    if fn.check_package_installed("sardi-orb-colora-variations-icons-git"):
        self.sardi_orb_colora_variations_icons_git.set_active(True)

    installed = _collect_sardi_packages(self)
    if installed:
        fn.log_subsection(f"Found {len(installed)} Sardi icon packages installed")
        fn.log_info(f"  {', '.join(installed)}")
        fn.show_in_app_notification(self, f"{len(installed)} Sardi icon packages installed")
    else:
        fn.log_info("No Sardi icon packages installed")
        fn.show_in_app_notification(self, "No Sardi icon packages installed")


def set_att_checkboxes_theming_surfn_icons_all(self):
    self.surfn_icons_git_att.set_active(True)
    self.surfn_arc_breeze_icons_git.set_active(True)
    self.surfn_mint_y_icons_git.set_active(True)
    self.surfn_plasma_dark.set_active(True)
    self.surfn_plasma_light.set_active(True)
    self.surfn_plasma_flow.set_active(True)


def set_att_checkboxes_theming_surfn_icons_none(self):

    self.surfn_icons_git_att.set_active(False)
    self.surfn_arc_breeze_icons_git.set_active(False)
    self.surfn_mint_y_icons_git.set_active(False)
    self.surfn_plasma_dark.set_active(False)
    self.surfn_plasma_light.set_active(False)
    self.surfn_plasma_flow.set_active(False)


def _collect_surfn_packages(self):
    pairs = [
        (self.surfn_icons_git_att, "surfn-icons-git"),
        (self.surfn_arc_breeze_icons_git, "surfn-arc-breeze-icons-git"),
        (self.surfn_mint_y_icons_git, "surfn-mint-y-icons-git"),
        (self.surfn_plasma_dark, "surfn-plasma-dark-icons-git"),
        (self.surfn_plasma_light, "surfn-plasma-light-icons-git"),
        (self.surfn_plasma_flow, "surfn-plasma-flow-git"),
    ]
    return [pkg for cb, pkg in pairs if cb.get_active()]


def install_surfn_icons(self):
    if not _check_install_repos(self):
        return
    packages = _collect_surfn_packages(self)
    if not packages:
        fn.log_info("No Surfn icons selected for installation")
        fn.show_in_app_notification(self, "No Surfn icons selected for installation")
        return
    fn.log_subsection(f"Installing {len(packages)} Surfn icon packages...")
    fn.log_info(f"  {', '.join(packages)}")
    process = fn.launch_pacman_install_in_terminal(" ".join(packages))
    fn.show_in_app_notification(self, f"Installing {len(packages)} Surfn icon packages...")
    fn.wait_and_notify(process, self, "Surfn icons installation complete")


def remove_surfn_icons(self):
    packages = _collect_surfn_packages(self)
    if not packages:
        fn.log_info("No Surfn icons selected for removal")
        fn.show_in_app_notification(self, "No Surfn icons selected for removal")
        return
    fn.log_subsection(f"Removing {len(packages)} Surfn icon packages...")
    fn.log_info(f"  {', '.join(packages)}")
    process = fn.launch_pacman_remove_in_terminal(" ".join(packages))
    fn.show_in_app_notification(self, f"Removing {len(packages)} Surfn icon packages...")
    fn.wait_and_notify(process, self, "Surfn icons removal complete")


def find_surfn_icons(self):
    set_att_checkboxes_theming_surfn_icons_none(self)

    if fn.check_package_installed("surfn-arc-breeze-icons-git"):
        self.surfn_arc_breeze_icons_git.set_active(True)
    if fn.check_package_installed("surfn-mint-y-icons-git"):
        self.surfn_mint_y_icons_git.set_active(True)
    if fn.check_package_installed("surfn-plasma-light-icons-git"):
        self.surfn_plasma_light.set_active(True)
    if fn.check_package_installed("surfn-plasma-flow-git"):
        self.surfn_plasma_flow.set_active(True)
    if fn.check_package_installed("surfn-plasma-dark-icons-git"):
        self.surfn_plasma_dark.set_active(True)
    if fn.check_package_installed("surfn-icons-git"):
        self.surfn_icons_git_att.set_active(True)

    installed = _collect_surfn_packages(self)
    if installed:
        fn.log_subsection(f"Found {len(installed)} Surfn icon packages installed")
        fn.log_info(f"  {', '.join(installed)}")
        fn.show_in_app_notification(self, f"{len(installed)} Surfn icon packages installed")
    else:
        fn.log_info("No Surfn icon packages installed")
        fn.show_in_app_notification(self, "No Surfn icon packages installed")


def set_att_checkboxes_extras_all(self):
    self.att_candy_beauty.set_active(True)
    self.edu_candy_beauty_arc.set_active(True)
    self.edu_candy_beauty_arc_mint_grey.set_active(True)
    self.edu_candy_beauty_arc_mint_red.set_active(True)
    self.edu_candy_beauty_tela.set_active(True)
    self.edu_papirus_dark_tela.set_active(True)
    self.edu_papirus_dark_tela_grey.set_active(True)
    self.edu_vimix_dark_tela.set_active(True)
    self.edu_neo_candy_qogir.set_active(True)


def set_att_checkboxes_extras_none(self):
    self.att_candy_beauty.set_active(False)
    self.edu_candy_beauty_arc.set_active(False)
    self.edu_candy_beauty_arc_mint_grey.set_active(False)
    self.edu_candy_beauty_arc_mint_red.set_active(False)
    self.edu_candy_beauty_tela.set_active(False)
    self.edu_papirus_dark_tela.set_active(False)
    self.edu_papirus_dark_tela_grey.set_active(False)
    self.edu_vimix_dark_tela.set_active(False)
    self.edu_neo_candy_qogir.set_active(False)


def _collect_extras_packages(self):
    pairs = [
        (self.att_candy_beauty, "neo-candy-icons-git"),
        (self.edu_candy_beauty_arc, "edu-neo-candy-arc-git"),
        (self.edu_candy_beauty_arc_mint_grey, "edu-neo-candy-arc-mint-grey-git"),
        (self.edu_candy_beauty_arc_mint_red, "edu-neo-candy-arc-mint-red-git"),
        (self.edu_candy_beauty_tela, "edu-neo-candy-tela-git"),
        (self.edu_papirus_dark_tela, "edu-papirus-dark-tela-git"),
        (self.edu_papirus_dark_tela_grey, "edu-papirus-dark-tela-grey-git"),
        (self.edu_vimix_dark_tela, "edu-vimix-dark-tela-git"),
        (self.edu_neo_candy_qogir, "edu-neo-candy-qogir-git"),
    ]
    return [pkg for cb, pkg in pairs if cb.get_active()]


def install_att_extras(self):
    if not _check_install_repos(self):
        return
    packages = _collect_extras_packages(self)
    if not packages:
        fn.log_info("No Neo Candy icons selected for installation")
        fn.show_in_app_notification(self, "No Neo Candy icons selected for installation")
        return
    fn.log_subsection(f"Installing {len(packages)} Neo Candy icon packages...")
    fn.log_info(f"  {', '.join(packages)}")
    process = fn.launch_pacman_install_in_terminal(" ".join(packages))
    fn.show_in_app_notification(self, f"Installing {len(packages)} Neo Candy icon packages...")
    fn.wait_and_notify(process, self, "Neo Candy icons installation complete")


def remove_att_extras(self):
    packages = _collect_extras_packages(self)
    if not packages:
        fn.log_info("No Neo Candy icons selected for removal")
        fn.show_in_app_notification(self, "No Neo Candy icons selected for removal")
        return
    fn.log_subsection(f"Removing {len(packages)} Neo Candy icon packages...")
    fn.log_info(f"  {', '.join(packages)}")
    process = fn.launch_pacman_remove_in_terminal(" ".join(packages))
    fn.show_in_app_notification(self, f"Removing {len(packages)} Neo Candy icon packages...")
    fn.wait_and_notify(process, self, "Neo Candy icons removal complete")


def find_att_extras(self):
    set_att_checkboxes_extras_none(self)

    if fn.check_package_installed("neo-candy-icons-git"):
        self.att_candy_beauty.set_active(True)
    if fn.check_package_installed("edu-neo-candy-arc-git"):
        self.edu_candy_beauty_arc.set_active(True)
    if fn.check_package_installed("edu-neo-candy-arc-mint-grey-git"):
        self.edu_candy_beauty_arc_mint_grey.set_active(True)
    if fn.check_package_installed("edu-neo-candy-arc-mint-red-git"):
        self.edu_candy_beauty_arc_mint_red.set_active(True)
    if fn.check_package_installed("edu-neo-candy-tela-git"):
        self.edu_candy_beauty_tela.set_active(True)
    if fn.check_package_installed("edu-papirus-dark-tela-git"):
        self.edu_papirus_dark_tela.set_active(True)
    if fn.check_package_installed("edu-papirus-dark-tela-grey-git"):
        self.edu_papirus_dark_tela_grey.set_active(True)
    if fn.check_package_installed("edu-vimix-dark-tela-git"):
        self.edu_vimix_dark_tela.set_active(True)
    if fn.check_package_installed("edu-neo-candy-qogir-git"):
        self.edu_neo_candy_qogir.set_active(True)

    installed = _collect_extras_packages(self)
    if installed:
        fn.log_subsection(f"Found {len(installed)} Neo Candy icon packages installed")
        fn.log_info(f"  {', '.join(installed)}")
        fn.show_in_app_notification(self, f"{len(installed)} Neo Candy icon packages installed")
    else:
        fn.log_info("No Neo Candy icon packages installed")
        fn.show_in_app_notification(self, "No Neo Candy icon packages installed")
