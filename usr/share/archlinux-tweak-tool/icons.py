# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import json
import os

import functions as fn

_SARDI_COUNT = 24
_NEOCANDY_COUNT = 9

_SURFN_FAMILIES_JSON = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "surfn_families.json")
# Base package every Surfn variant depends on; never bulk-removed while variants remain.
_SURFN_BASE_PKG = "surfn-icons-git"


def _load_surfn_families():
    """Load the generated Surfn family table ({family: [{token, package}, …]})."""
    try:
        with open(_SURFN_FAMILIES_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as error:
        fn.log_error(f"Could not load Surfn family table: {error}")
        return {}


SURFN_FAMILIES = _load_surfn_families()


def _all_surfn_tokens():
    return [entry["token"] for items in SURFN_FAMILIES.values() for entry in items]


# Which families live under each Surfn sub-tab. Surfn-Tela is an intentional placeholder
# (no families yet) — to be filled in later.
SURFN_TABS = {
    "Surfn": ["Plasma", "Numix", "Papirus", "Arc / Breeze", "Other"],
    "Surfn-Mint": ["Mint-X", "Mint-Y"],
    "Surfn-Tela": [],
}


def _tab_tokens(family_labels):
    return [entry["token"] for fam in family_labels for entry in SURFN_FAMILIES.get(fam, [])]


def _surfn_pkg(token):
    for items in SURFN_FAMILIES.values():
        for entry in items:
            if entry["token"] == token:
                return entry["package"]
    return token + "-icons-git"


def get_available_icon_counts():
    """Return (sardi, surfn, neocandy) installable package counts."""
    return _SARDI_COUNT, len(_all_surfn_tokens()), _NEOCANDY_COUNT


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
    fn.show_in_app_notification(self, "We have selected the mint selection - sardi icons")
    set_att_checkboxes_theming_sardi_mint_icons(self)


def on_click_att_sardi_icon_theming_mixing_selection(self, _widget):
    fn.log_subsection("Mixing selection applied - Sardi icons")
    fn.show_in_app_notification(self, "We have selected the mixing selection - sardi icons")
    set_att_checkboxes_theming_sardi_mixing_icons(self)


def on_click_att_sardi_icon_theming_variations_selection(self, _widget):
    fn.log_subsection("Variations selection applied - Sardi icons")
    fn.show_in_app_notification(self, "We have selected the variation selection - sardi icons")
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
    fn.show_in_app_notification(self, "We have selected the Sardi flexible family themes")
    set_att_fam_checkboxes_theming_sardi_flexible(self)


def on_click_att_fam_sardi_icon_theming_sardi_mono_selection(self, _widget):
    fn.log_subsection("Sardi mono family selected")
    fn.show_in_app_notification(self, "We have selected the Sardi mono family themes")
    set_att_fam_checkboxes_theming_sardi_mono(self)


def on_click_att_fam_sardi_icon_theming_sardi_flat_selection(self, _widget):
    fn.log_subsection("Sardi flat family selected")
    fn.show_in_app_notification(self, "We have selected the Sardi flat family themes")
    set_att_fam_checkboxes_theming_sardi_flat(self)


def on_click_att_fam_sardi_icon_theming_sardi_ghost_selection(self, _widget):
    fn.log_subsection("Sardi ghost family selected")
    fn.show_in_app_notification(self, "We have selected the Sardi ghost family themes")
    set_att_fam_checkboxes_theming_sardi_ghost(self)


def on_click_att_fam_sardi_icon_theming_sardi_orb_selection(self, _widget):
    fn.log_subsection("Sardi orb family selected")
    fn.show_in_app_notification(self, "We have selected the Sardi orb family themes")
    set_att_fam_checkboxes_theming_sardi_orb(self)


def on_click_att_surfn_theming_all_selection(self, tokens, _widget):
    fn.log_subsection("All Surfn icons selected")
    fn.show_in_app_notification(self, "We have selected all surfn icons")
    set_att_checkboxes_theming_surfn_icons_all(self, tokens)


def on_click_att_surfn_theming_none_selection(self, tokens, _widget):
    fn.log_subsection("No Surfn icons selected")
    fn.show_in_app_notification(self, "We have selected no surfn icons")
    set_att_checkboxes_theming_surfn_icons_none(self, tokens)


def on_click_att_surfn_family_selection(self, family_label, scope_tokens, _widget):
    """Tick one Surfn family (the filter buttons) and clear the rest within the tab."""
    fn.log_subsection(f"Select {family_label} Surfn icons")
    fn.show_in_app_notification(self, f"We have selected the {family_label} Surfn icons")
    select_surfn_family(self, family_label, scope_tokens)


def on_install_neocandy_clicked(self, _widget):
    fn.log_subsection("Installing selected Neo Candy icon packages...")
    install_att_neocandy(self)


def on_remove_neocandy_clicked(self, _widget):
    fn.log_subsection("Removing selected Neo Candy icon packages...")
    remove_att_neocandy(self)


def on_find_neocandy_clicked(self, _widget):
    fn.log_subsection("Showing installed projects...")
    fn.show_in_app_notification(self, "We show the installed icon themes")
    find_att_neocandy(self)


def on_click_neocandy_theming_all_selection(self, _widget):
    fn.log_subsection("All projects selected")
    fn.show_in_app_notification(self, "We have selected all icon themes")
    set_att_checkboxes_neocandy_all(self)


def on_click_neocandy_theming_none_selection(self, _widget):
    fn.log_subsection("No projects selected")
    fn.show_in_app_notification(self, "We have selected none of the icon themes")
    set_att_checkboxes_neocandy_none(self)


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


def on_install_att_surfn_icon_themes_clicked(self, tokens, _widget):
    fn.log_subsection("Installing selected Surfn icon themes...")
    install_surfn_icons(self, tokens)


def on_remove_att_surfn_icon_themes_clicked(self, tokens, _widget):
    fn.log_subsection("Removing selected Surfn icon themes...")
    remove_surfn_icons(self, tokens)


def on_find_att_surfn_icon_themes_clicked(self, tokens, _widget):
    fn.log_subsection("Showing all installed Surfn icon themes...")
    fn.show_in_app_notification(self, "We show the installed icon themes")
    find_surfn_icons(self, tokens)


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


def set_att_checkboxes_theming_surfn_icons_all(self, tokens=None):
    for token in tokens if tokens is not None else _all_surfn_tokens():
        self.surfn_checkboxes[token].set_active(True)


def set_att_checkboxes_theming_surfn_icons_none(self, tokens=None):
    for token in tokens if tokens is not None else _all_surfn_tokens():
        self.surfn_checkboxes[token].set_active(False)


def select_surfn_family(self, family_label, scope_tokens=None):
    """Tick the checkboxes for one Surfn family and clear the rest within scope."""
    scope = scope_tokens if scope_tokens is not None else _all_surfn_tokens()
    family_tokens = {entry["token"] for entry in SURFN_FAMILIES.get(family_label, [])}
    for token in scope:
        self.surfn_checkboxes[token].set_active(token in family_tokens)


def _collect_surfn_packages(self, tokens=None):
    scope = tokens if tokens is not None else _all_surfn_tokens()
    return [_surfn_pkg(token) for token in scope if self.surfn_checkboxes[token].get_active()]


def install_surfn_icons(self, tokens=None):
    if not _check_install_repos(self):
        return
    packages = _collect_surfn_packages(self, tokens)
    if not packages:
        fn.log_info("No Surfn icons selected for installation")
        fn.show_in_app_notification(self, "No Surfn icons selected for installation")
        return
    fn.log_subsection(f"Installing {len(packages)} Surfn icon packages...")
    fn.log_info(f"  {', '.join(packages)}")
    process = fn.launch_pacman_install_in_terminal(" ".join(packages))
    fn.show_in_app_notification(self, f"Installing {len(packages)} Surfn icon packages...")
    fn.wait_and_notify(process, self, "Surfn icons installation complete")


def remove_surfn_icons(self, tokens=None):
    packages = _collect_surfn_packages(self, tokens)
    if not packages:
        fn.log_info("No Surfn icons selected for removal")
        fn.show_in_app_notification(self, "No Surfn icons selected for removal")
        return
    # Every variant depends on the base; removing it while variants remain would
    # cascade them all out, so keep the base unless it is the only thing selected.
    if _SURFN_BASE_PKG in packages and len(packages) > 1:
        packages.remove(_SURFN_BASE_PKG)
        fn.log_warn(f"Keeping {_SURFN_BASE_PKG} — other Surfn variants depend on it")
        fn.show_in_app_notification(self, f"Kept {_SURFN_BASE_PKG} (variants depend on it)")
    fn.log_subsection(f"Removing {len(packages)} Surfn icon packages...")
    fn.log_info(f"  {', '.join(packages)}")
    process = fn.launch_pacman_remove_in_terminal(" ".join(packages))
    fn.show_in_app_notification(self, f"Removing {len(packages)} Surfn icon packages...")
    fn.wait_and_notify(process, self, "Surfn icons removal complete")


def find_surfn_icons(self, tokens=None):
    scope = tokens if tokens is not None else _all_surfn_tokens()
    set_att_checkboxes_theming_surfn_icons_none(self, scope)
    installed_map = fn.check_packages_installed([_surfn_pkg(t) for t in scope])
    for token in scope:
        if installed_map.get(_surfn_pkg(token)):
            self.surfn_checkboxes[token].set_active(True)

    installed = _collect_surfn_packages(self, scope)
    if installed:
        fn.log_subsection(f"Found {len(installed)} Surfn icon packages installed")
        fn.log_info(f"  {', '.join(installed)}")
        fn.show_in_app_notification(self, f"{len(installed)} Surfn icon packages installed")
    else:
        fn.log_info("No Surfn icon packages installed")
        fn.show_in_app_notification(self, "No Surfn icon packages installed")


def set_att_checkboxes_neocandy_all(self):
    self.att_candy_beauty.set_active(True)
    self.edu_candy_beauty_arc.set_active(True)
    self.edu_candy_beauty_arc_mint_grey.set_active(True)
    self.edu_candy_beauty_arc_mint_red.set_active(True)
    self.edu_candy_beauty_tela.set_active(True)
    self.edu_papirus_dark_tela.set_active(True)
    self.edu_papirus_dark_tela_grey.set_active(True)
    self.edu_vimix_dark_tela.set_active(True)
    self.edu_neo_candy_qogir.set_active(True)


def set_att_checkboxes_neocandy_none(self):
    self.att_candy_beauty.set_active(False)
    self.edu_candy_beauty_arc.set_active(False)
    self.edu_candy_beauty_arc_mint_grey.set_active(False)
    self.edu_candy_beauty_arc_mint_red.set_active(False)
    self.edu_candy_beauty_tela.set_active(False)
    self.edu_papirus_dark_tela.set_active(False)
    self.edu_papirus_dark_tela_grey.set_active(False)
    self.edu_vimix_dark_tela.set_active(False)
    self.edu_neo_candy_qogir.set_active(False)


def _collect_neocandy_packages(self):
    pairs = [
        (self.att_candy_beauty, "neo-candy-icons-git"),
        (self.edu_candy_beauty_arc, "kiro-neo-candy-arc"),
        (self.edu_candy_beauty_arc_mint_grey, "kiro-neo-candy-arc-mint-grey"),
        (self.edu_candy_beauty_arc_mint_red, "kiro-neo-candy-arc-mint-red"),
        (self.edu_candy_beauty_tela, "kiro-neo-candy-tela"),
        (self.edu_papirus_dark_tela, "kiro-papirus-dark-tela"),
        (self.edu_papirus_dark_tela_grey, "kiro-papirus-dark-tela-grey"),
        (self.edu_vimix_dark_tela, "kiro-vimix-dark-tela"),
        (self.edu_neo_candy_qogir, "kiro-neo-candy-qogir"),
    ]
    return [pkg for cb, pkg in pairs if cb.get_active()]


def install_att_neocandy(self):
    if not _check_install_repos(self):
        return
    packages = _collect_neocandy_packages(self)
    if not packages:
        fn.log_info("No Neo Candy icons selected for installation")
        fn.show_in_app_notification(self, "No Neo Candy icons selected for installation")
        return
    fn.log_subsection(f"Installing {len(packages)} Neo Candy icon packages...")
    fn.log_info(f"  {', '.join(packages)}")
    process = fn.launch_pacman_install_in_terminal(" ".join(packages))
    fn.show_in_app_notification(self, f"Installing {len(packages)} Neo Candy icon packages...")
    fn.wait_and_notify(process, self, "Neo Candy icons installation complete")


def remove_att_neocandy(self):
    packages = _collect_neocandy_packages(self)
    if not packages:
        fn.log_info("No Neo Candy icons selected for removal")
        fn.show_in_app_notification(self, "No Neo Candy icons selected for removal")
        return
    fn.log_subsection(f"Removing {len(packages)} Neo Candy icon packages...")
    fn.log_info(f"  {', '.join(packages)}")
    process = fn.launch_pacman_remove_in_terminal(" ".join(packages))
    fn.show_in_app_notification(self, f"Removing {len(packages)} Neo Candy icon packages...")
    fn.wait_and_notify(process, self, "Neo Candy icons removal complete")


def find_att_neocandy(self):
    set_att_checkboxes_neocandy_none(self)

    if fn.check_package_installed("neo-candy-icons-git"):
        self.att_candy_beauty.set_active(True)
    if fn.check_package_installed("kiro-neo-candy-arc"):
        self.edu_candy_beauty_arc.set_active(True)
    if fn.check_package_installed("kiro-neo-candy-arc-mint-grey"):
        self.edu_candy_beauty_arc_mint_grey.set_active(True)
    if fn.check_package_installed("kiro-neo-candy-arc-mint-red"):
        self.edu_candy_beauty_arc_mint_red.set_active(True)
    if fn.check_package_installed("kiro-neo-candy-tela"):
        self.edu_candy_beauty_tela.set_active(True)
    if fn.check_package_installed("kiro-papirus-dark-tela"):
        self.edu_papirus_dark_tela.set_active(True)
    if fn.check_package_installed("kiro-papirus-dark-tela-grey"):
        self.edu_papirus_dark_tela_grey.set_active(True)
    if fn.check_package_installed("kiro-vimix-dark-tela"):
        self.edu_vimix_dark_tela.set_active(True)
    if fn.check_package_installed("kiro-neo-candy-qogir"):
        self.edu_neo_candy_qogir.set_active(True)

    installed = _collect_neocandy_packages(self)
    if installed:
        fn.log_subsection(f"Found {len(installed)} Neo Candy icon packages installed")
        fn.log_info(f"  {', '.join(installed)}")
        fn.show_in_app_notification(self, f"{len(installed)} Neo Candy icon packages installed")
    else:
        fn.log_info("No Neo Candy icon packages installed")
        fn.show_in_app_notification(self, "No Neo Candy icon packages installed")
