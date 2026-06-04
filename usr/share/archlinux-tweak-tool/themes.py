# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn


def install_themes(self):
    """Install selected arc themes with detailed logging."""
    themes_to_install = []

    if self.arcolinux_arc_aqua.get_active():
        themes_to_install.append("arcolinux-arc-aqua-git")
    if self.arcolinux_arc_archlinux_blue.get_active():
        themes_to_install.append("arcolinux-arc-archlinux-blue-git")
    if self.arcolinux_arc_arcolinux_blue.get_active():
        themes_to_install.append("arcolinux-arc-arcolinux-blue-git")
    if self.arcolinux_arc_azul.get_active():
        themes_to_install.append("arcolinux-arc-azul-git")
    if self.arcolinux_arc_azure.get_active():
        themes_to_install.append("arcolinux-arc-azure-git")
    if self.arcolinux_arc_azure_dodger_blue.get_active():
        themes_to_install.append("arcolinux-arc-azure-dodger-blue-git")
    if self.arcolinux_arc_blood.get_active():
        themes_to_install.append("arcolinux-arc-blood-git")
    if self.arcolinux_arc_blue_sky.get_active():
        themes_to_install.append("arcolinux-arc-blue-sky-git")
    if self.arcolinux_arc_botticelli.get_active():
        themes_to_install.append("arcolinux-arc-botticelli-git")
    if self.arcolinux_arc_bright_lilac.get_active():
        themes_to_install.append("arcolinux-arc-bright-lilac-git")
    if self.arcolinux_arc_carnation.get_active():
        themes_to_install.append("arcolinux-arc-carnation-git")
    if self.arcolinux_arc_carolina_blue.get_active():
        themes_to_install.append("arcolinux-arc-carolina-blue-git")
    if self.arcolinux_arc_casablanca.get_active():
        themes_to_install.append("arcolinux-arc-casablanca-git")
    if self.arcolinux_arc_crimson.get_active():
        themes_to_install.append("arcolinux-arc-crimson-git")
    if self.arcolinux_arc_dawn.get_active():
        themes_to_install.append("kiro-arc-dawn")
    if self.arcolinux_arc_dodger_blue.get_active():
        themes_to_install.append("arcolinux-arc-dodger-blue-git")
    if self.arcolinux_arc_dracul.get_active():
        themes_to_install.append("arcolinux-arc-dracul-git")
    if self.arcolinux_arc_emerald.get_active():
        themes_to_install.append("arcolinux-arc-emerald-git")
    if self.arcolinux_arc_evopop.get_active():
        themes_to_install.append("arcolinux-arc-evopop-git")
    if self.arcolinux_arc_fern.get_active():
        themes_to_install.append("arcolinux-arc-fern-git")
    if self.arcolinux_arc_fire.get_active():
        themes_to_install.append("arcolinux-arc-fire-git")
    if self.arcolinux_arc_froly.get_active():
        themes_to_install.append("arcolinux-arc-froly-git")
    if self.arcolinux_arc_havelock.get_active():
        themes_to_install.append("arcolinux-arc-havelock-git")
    if self.arcolinux_arc_hibiscus.get_active():
        themes_to_install.append("arcolinux-arc-hibiscus-git")
    if self.arcolinux_arc_light_blue_grey.get_active():
        themes_to_install.append("arcolinux-arc-light-blue-grey-git")
    if self.arcolinux_arc_light_blue_surfn.get_active():
        themes_to_install.append("arcolinux-arc-light-blue-surfn-git")
    if self.arcolinux_arc_light_salmon.get_active():
        themes_to_install.append("arcolinux-arc-light-salmon-git")
    if self.arcolinux_arc_mandy.get_active():
        themes_to_install.append("arcolinux-arc-mandy-git")
    if self.arcolinux_arc_mantis.get_active():
        themes_to_install.append("arcolinux-arc-mantis-git")
    if self.arcolinux_arc_medium_blue.get_active():
        themes_to_install.append("arcolinux-arc-medium-blue-git")
    if self.arcolinux_arc_niagara.get_active():
        themes_to_install.append("arcolinux-arc-niagara-git")
    if self.arcolinux_arc_nice_blue.get_active():
        themes_to_install.append("arcolinux-arc-nice-blue-git")
    if self.arcolinux_arc_numix.get_active():
        themes_to_install.append("arcolinux-arc-numix-git")
    if self.arcolinux_arc_orchid.get_active():
        themes_to_install.append("arcolinux-arc-orchid-git")
    if self.arcolinux_arc_pale_grey.get_active():
        themes_to_install.append("arcolinux-arc-pale-grey-git")
    if self.arcolinux_arc_paper.get_active():
        themes_to_install.append("arcolinux-arc-paper-git")
    if self.arcolinux_arc_pink.get_active():
        themes_to_install.append("arcolinux-arc-pink-git")
    if self.arcolinux_arc_polo.get_active():
        themes_to_install.append("arcolinux-arc-polo-git")
    if self.arcolinux_arc_punch.get_active():
        themes_to_install.append("arcolinux-arc-punch-git")
    if self.arcolinux_arc_red_orange.get_active():
        themes_to_install.append("arcolinux-arc-red-orange-git")
    if self.arcolinux_arc_rusty_orange.get_active():
        themes_to_install.append("arcolinux-arc-rusty-orange-git")
    if self.arcolinux_arc_sky_blue.get_active():
        themes_to_install.append("arcolinux-arc-sky-blue-git")
    if self.arcolinux_arc_slate_grey.get_active():
        themes_to_install.append("arcolinux-arc-slate-grey-git")
    if self.arcolinux_arc_smoke.get_active():
        themes_to_install.append("arcolinux-arc-smoke-git")
    if self.arcolinux_arc_soft_blue.get_active():
        themes_to_install.append("arcolinux-arc-soft-blue-git")
    if self.arcolinux_arc_tacao.get_active():
        themes_to_install.append("arcolinux-arc-tacao-git")
    if self.arcolinux_arc_tangerine.get_active():
        themes_to_install.append("arcolinux-arc-tangerine-git")
    if self.arcolinux_arc_tory.get_active():
        themes_to_install.append("arcolinux-arc-tory-git")
    if self.arcolinux_arc_vampire.get_active():
        themes_to_install.append("arcolinux-arc-vampire-git")
    if self.arcolinux_arc_warm_pink.get_active():
        themes_to_install.append("arcolinux-arc-warm-pink-git")

    if not themes_to_install:
        fn.log_warn("No themes selected for installation")
        fn.show_in_app_notification(self, "No themes selected for installation")
        return

    packages_str = " ".join(themes_to_install)
    fn.log_info(f"Installing {len(themes_to_install)} Arc theme(s): {', '.join(themes_to_install)}")
    process = fn.launch_pacman_install_in_terminal(packages_str)
    fn.show_in_app_notification(self, f"Installing {len(themes_to_install)} themes...")
    fn.wait_and_notify(process, self, "Arc themes installation complete")


def remove_themes(self):
    """Remove selected arc themes with detailed logging."""
    themes_to_remove = []

    if self.arcolinux_arc_aqua.get_active():
        themes_to_remove.append("arcolinux-arc-aqua-git")
    if self.arcolinux_arc_archlinux_blue.get_active():
        themes_to_remove.append("arcolinux-arc-archlinux-blue-git")
    if self.arcolinux_arc_arcolinux_blue.get_active():
        themes_to_remove.append("arcolinux-arc-arcolinux-blue-git")
    if self.arcolinux_arc_azul.get_active():
        themes_to_remove.append("arcolinux-arc-azul-git")
    if self.arcolinux_arc_azure.get_active():
        themes_to_remove.append("arcolinux-arc-azure-git")
    if self.arcolinux_arc_azure_dodger_blue.get_active():
        themes_to_remove.append("arcolinux-arc-azure-dodger-blue-git")
    if self.arcolinux_arc_blood.get_active():
        themes_to_remove.append("arcolinux-arc-blood-git")
    if self.arcolinux_arc_blue_sky.get_active():
        themes_to_remove.append("arcolinux-arc-blue-sky-git")
    if self.arcolinux_arc_botticelli.get_active():
        themes_to_remove.append("arcolinux-arc-botticelli-git")
    if self.arcolinux_arc_bright_lilac.get_active():
        themes_to_remove.append("arcolinux-arc-bright-lilac-git")
    if self.arcolinux_arc_carnation.get_active():
        themes_to_remove.append("arcolinux-arc-carnation-git")
    if self.arcolinux_arc_carolina_blue.get_active():
        themes_to_remove.append("arcolinux-arc-carolina-blue-git")
    if self.arcolinux_arc_casablanca.get_active():
        themes_to_remove.append("arcolinux-arc-casablanca-git")
    if self.arcolinux_arc_crimson.get_active():
        themes_to_remove.append("arcolinux-arc-crimson-git")
    if self.arcolinux_arc_dawn.get_active():
        themes_to_remove.append("kiro-arc-dawn")
    if self.arcolinux_arc_dodger_blue.get_active():
        themes_to_remove.append("arcolinux-arc-dodger-blue-git")
    if self.arcolinux_arc_dracul.get_active():
        themes_to_remove.append("arcolinux-arc-dracul-git")
    if self.arcolinux_arc_emerald.get_active():
        themes_to_remove.append("arcolinux-arc-emerald-git")
    if self.arcolinux_arc_evopop.get_active():
        themes_to_remove.append("arcolinux-arc-evopop-git")
    if self.arcolinux_arc_fern.get_active():
        themes_to_remove.append("arcolinux-arc-fern-git")
    if self.arcolinux_arc_fire.get_active():
        themes_to_remove.append("arcolinux-arc-fire-git")
    if self.arcolinux_arc_froly.get_active():
        themes_to_remove.append("arcolinux-arc-froly-git")
    if self.arcolinux_arc_havelock.get_active():
        themes_to_remove.append("arcolinux-arc-havelock-git")
    if self.arcolinux_arc_hibiscus.get_active():
        themes_to_remove.append("arcolinux-arc-hibiscus-git")
    if self.arcolinux_arc_light_blue_grey.get_active():
        themes_to_remove.append("arcolinux-arc-light-blue-grey-git")
    if self.arcolinux_arc_light_blue_surfn.get_active():
        themes_to_remove.append("arcolinux-arc-light-blue-surfn-git")
    if self.arcolinux_arc_light_salmon.get_active():
        themes_to_remove.append("arcolinux-arc-light-salmon-git")
    if self.arcolinux_arc_mandy.get_active():
        themes_to_remove.append("arcolinux-arc-mandy-git")
    if self.arcolinux_arc_mantis.get_active():
        themes_to_remove.append("arcolinux-arc-mantis-git")
    if self.arcolinux_arc_medium_blue.get_active():
        themes_to_remove.append("arcolinux-arc-medium-blue-git")
    if self.arcolinux_arc_niagara.get_active():
        themes_to_remove.append("arcolinux-arc-niagara-git")
    if self.arcolinux_arc_nice_blue.get_active():
        themes_to_remove.append("arcolinux-arc-nice-blue-git")
    if self.arcolinux_arc_numix.get_active():
        themes_to_remove.append("arcolinux-arc-numix-git")
    if self.arcolinux_arc_orchid.get_active():
        themes_to_remove.append("arcolinux-arc-orchid-git")
    if self.arcolinux_arc_pale_grey.get_active():
        themes_to_remove.append("arcolinux-arc-pale-grey-git")
    if self.arcolinux_arc_paper.get_active():
        themes_to_remove.append("arcolinux-arc-paper-git")
    if self.arcolinux_arc_pink.get_active():
        themes_to_remove.append("arcolinux-arc-pink-git")
    if self.arcolinux_arc_polo.get_active():
        themes_to_remove.append("arcolinux-arc-polo-git")
    if self.arcolinux_arc_punch.get_active():
        themes_to_remove.append("arcolinux-arc-punch-git")
    if self.arcolinux_arc_red_orange.get_active():
        themes_to_remove.append("arcolinux-arc-red-orange-git")
    if self.arcolinux_arc_rusty_orange.get_active():
        themes_to_remove.append("arcolinux-arc-rusty-orange-git")
    if self.arcolinux_arc_sky_blue.get_active():
        themes_to_remove.append("arcolinux-arc-sky-blue-git")
    if self.arcolinux_arc_slate_grey.get_active():
        themes_to_remove.append("arcolinux-arc-slate-grey-git")
    if self.arcolinux_arc_smoke.get_active():
        themes_to_remove.append("arcolinux-arc-smoke-git")
    if self.arcolinux_arc_soft_blue.get_active():
        themes_to_remove.append("arcolinux-arc-soft-blue-git")
    if self.arcolinux_arc_tacao.get_active():
        themes_to_remove.append("arcolinux-arc-tacao-git")
    if self.arcolinux_arc_tangerine.get_active():
        themes_to_remove.append("arcolinux-arc-tangerine-git")
    if self.arcolinux_arc_tory.get_active():
        themes_to_remove.append("arcolinux-arc-tory-git")
    if self.arcolinux_arc_vampire.get_active():
        themes_to_remove.append("arcolinux-arc-vampire-git")
    if self.arcolinux_arc_warm_pink.get_active():
        themes_to_remove.append("arcolinux-arc-warm-pink-git")

    if not themes_to_remove:
        fn.log_warn("No themes selected for removal")
        fn.show_in_app_notification(self, "No themes selected for removal")
        return

    packages_str = " ".join(themes_to_remove)
    fn.log_info(f"Removing {len(themes_to_remove)} Arc theme(s): {', '.join(themes_to_remove)}")
    process = fn.launch_pacman_remove_in_terminal(packages_str)
    fn.show_in_app_notification(self, f"Removing {len(themes_to_remove)} themes...")
    fn.wait_and_notify(process, self, "Arc themes removal complete")


def find_themes(self):
    """Check which arc themes are installed and tick their checkboxes."""
    self.arcolinux_arc_aqua.set_active(False)
    self.arcolinux_arc_archlinux_blue.set_active(False)
    self.arcolinux_arc_arcolinux_blue.set_active(False)
    self.arcolinux_arc_azul.set_active(False)
    self.arcolinux_arc_azure.set_active(False)
    self.arcolinux_arc_azure_dodger_blue.set_active(False)
    self.arcolinux_arc_blood.set_active(False)
    self.arcolinux_arc_blue_sky.set_active(False)
    self.arcolinux_arc_botticelli.set_active(False)
    self.arcolinux_arc_bright_lilac.set_active(False)
    self.arcolinux_arc_carnation.set_active(False)
    self.arcolinux_arc_carolina_blue.set_active(False)
    self.arcolinux_arc_casablanca.set_active(False)
    self.arcolinux_arc_crimson.set_active(False)
    self.arcolinux_arc_dawn.set_active(False)
    self.arcolinux_arc_dodger_blue.set_active(False)
    self.arcolinux_arc_dracul.set_active(False)
    self.arcolinux_arc_emerald.set_active(False)
    self.arcolinux_arc_evopop.set_active(False)
    self.arcolinux_arc_fern.set_active(False)
    self.arcolinux_arc_fire.set_active(False)
    self.arcolinux_arc_froly.set_active(False)
    self.arcolinux_arc_havelock.set_active(False)
    self.arcolinux_arc_hibiscus.set_active(False)
    self.arcolinux_arc_light_blue_grey.set_active(False)
    self.arcolinux_arc_light_blue_surfn.set_active(False)
    self.arcolinux_arc_light_salmon.set_active(False)
    self.arcolinux_arc_mandy.set_active(False)
    self.arcolinux_arc_mantis.set_active(False)
    self.arcolinux_arc_medium_blue.set_active(False)
    self.arcolinux_arc_niagara.set_active(False)
    self.arcolinux_arc_nice_blue.set_active(False)
    self.arcolinux_arc_numix.set_active(False)
    self.arcolinux_arc_orchid.set_active(False)
    self.arcolinux_arc_pale_grey.set_active(False)
    self.arcolinux_arc_paper.set_active(False)
    self.arcolinux_arc_pink.set_active(False)
    self.arcolinux_arc_polo.set_active(False)
    self.arcolinux_arc_punch.set_active(False)
    self.arcolinux_arc_red_orange.set_active(False)
    self.arcolinux_arc_rusty_orange.set_active(False)
    self.arcolinux_arc_sky_blue.set_active(False)
    self.arcolinux_arc_slate_grey.set_active(False)
    self.arcolinux_arc_smoke.set_active(False)
    self.arcolinux_arc_soft_blue.set_active(False)
    self.arcolinux_arc_tacao.set_active(False)
    self.arcolinux_arc_tangerine.set_active(False)
    self.arcolinux_arc_tory.set_active(False)
    self.arcolinux_arc_vampire.set_active(False)
    self.arcolinux_arc_warm_pink.set_active(False)

    if fn.check_package_installed("arcolinux-arc-aqua-git"):
        self.arcolinux_arc_aqua.set_active(True)
    if fn.check_package_installed("arcolinux-arc-archlinux-blue-git"):
        self.arcolinux_arc_archlinux_blue.set_active(True)
    if fn.check_package_installed("arcolinux-arc-arcolinux-blue-git"):
        self.arcolinux_arc_arcolinux_blue.set_active(True)
    if fn.check_package_installed("arcolinux-arc-azul-git"):
        self.arcolinux_arc_azul.set_active(True)
    if fn.check_package_installed("arcolinux-arc-azure-git"):
        self.arcolinux_arc_azure.set_active(True)
    if fn.check_package_installed("arcolinux-arc-azure-dodger-blue-git"):
        self.arcolinux_arc_azure_dodger_blue.set_active(True)
    if fn.check_package_installed("arcolinux-arc-blood-git"):
        self.arcolinux_arc_blood.set_active(True)
    if fn.check_package_installed("arcolinux-arc-blue-sky-git"):
        self.arcolinux_arc_blue_sky.set_active(True)
    if fn.check_package_installed("arcolinux-arc-botticelli-git"):
        self.arcolinux_arc_botticelli.set_active(True)
    if fn.check_package_installed("arcolinux-arc-bright-lilac-git"):
        self.arcolinux_arc_bright_lilac.set_active(True)
    if fn.check_package_installed("arcolinux-arc-carnation-git"):
        self.arcolinux_arc_carnation.set_active(True)
    if fn.check_package_installed("arcolinux-arc-carolina-blue-git"):
        self.arcolinux_arc_carolina_blue.set_active(True)
    if fn.check_package_installed("arcolinux-arc-casablanca-git"):
        self.arcolinux_arc_casablanca.set_active(True)
    if fn.check_package_installed("arcolinux-arc-crimson-git"):
        self.arcolinux_arc_crimson.set_active(True)
    if fn.check_package_installed("kiro-arc-dawn"):
        self.arcolinux_arc_dawn.set_active(True)
    if fn.check_package_installed("arcolinux-arc-dodger-blue-git"):
        self.arcolinux_arc_dodger_blue.set_active(True)
    if fn.check_package_installed("arcolinux-arc-dracul-git"):
        self.arcolinux_arc_dracul.set_active(True)
    if fn.check_package_installed("arcolinux-arc-emerald-git"):
        self.arcolinux_arc_emerald.set_active(True)
    if fn.check_package_installed("arcolinux-arc-evopop-git"):
        self.arcolinux_arc_evopop.set_active(True)
    if fn.check_package_installed("arcolinux-arc-fern-git"):
        self.arcolinux_arc_fern.set_active(True)
    if fn.check_package_installed("arcolinux-arc-fire-git"):
        self.arcolinux_arc_fire.set_active(True)
    if fn.check_package_installed("arcolinux-arc-froly-git"):
        self.arcolinux_arc_froly.set_active(True)
    if fn.check_package_installed("arcolinux-arc-havelock-git"):
        self.arcolinux_arc_havelock.set_active(True)
    if fn.check_package_installed("arcolinux-arc-hibiscus-git"):
        self.arcolinux_arc_hibiscus.set_active(True)
    if fn.check_package_installed("arcolinux-arc-light-blue-grey-git"):
        self.arcolinux_arc_light_blue_grey.set_active(True)
    if fn.check_package_installed("arcolinux-arc-light-blue-surfn-git"):
        self.arcolinux_arc_light_blue_surfn.set_active(True)
    if fn.check_package_installed("arcolinux-arc-light-salmon-git"):
        self.arcolinux_arc_light_salmon.set_active(True)
    if fn.check_package_installed("arcolinux-arc-mandy-git"):
        self.arcolinux_arc_mandy.set_active(True)
    if fn.check_package_installed("arcolinux-arc-mantis-git"):
        self.arcolinux_arc_mantis.set_active(True)
    if fn.check_package_installed("arcolinux-arc-medium-blue-git"):
        self.arcolinux_arc_medium_blue.set_active(True)
    if fn.check_package_installed("arcolinux-arc-niagara-git"):
        self.arcolinux_arc_niagara.set_active(True)
    if fn.check_package_installed("arcolinux-arc-nice-blue-git"):
        self.arcolinux_arc_nice_blue.set_active(True)
    if fn.check_package_installed("arcolinux-arc-numix-git"):
        self.arcolinux_arc_numix.set_active(True)
    if fn.check_package_installed("arcolinux-arc-orchid-git"):
        self.arcolinux_arc_orchid.set_active(True)
    if fn.check_package_installed("arcolinux-arc-pale-grey-git"):
        self.arcolinux_arc_pale_grey.set_active(True)
    if fn.check_package_installed("arcolinux-arc-paper-git"):
        self.arcolinux_arc_paper.set_active(True)
    if fn.check_package_installed("arcolinux-arc-pink-git"):
        self.arcolinux_arc_pink.set_active(True)
    if fn.check_package_installed("arcolinux-arc-polo-git"):
        self.arcolinux_arc_polo.set_active(True)
    if fn.check_package_installed("arcolinux-arc-punch-git"):
        self.arcolinux_arc_punch.set_active(True)
    if fn.check_package_installed("arcolinux-arc-red-orange-git"):
        self.arcolinux_arc_red_orange.set_active(True)
    if fn.check_package_installed("arcolinux-arc-rusty-orange-git"):
        self.arcolinux_arc_rusty_orange.set_active(True)
    if fn.check_package_installed("arcolinux-arc-sky-blue-git"):
        self.arcolinux_arc_sky_blue.set_active(True)
    if fn.check_package_installed("arcolinux-arc-slate-grey-git"):
        self.arcolinux_arc_slate_grey.set_active(True)
    if fn.check_package_installed("arcolinux-arc-smoke-git"):
        self.arcolinux_arc_smoke.set_active(True)
    if fn.check_package_installed("arcolinux-arc-soft-blue-git"):
        self.arcolinux_arc_soft_blue.set_active(True)
    if fn.check_package_installed("arcolinux-arc-tacao-git"):
        self.arcolinux_arc_tacao.set_active(True)
    if fn.check_package_installed("arcolinux-arc-tangerine-git"):
        self.arcolinux_arc_tangerine.set_active(True)
    if fn.check_package_installed("arcolinux-arc-tory-git"):
        self.arcolinux_arc_tory.set_active(True)
    if fn.check_package_installed("arcolinux-arc-vampire-git"):
        self.arcolinux_arc_vampire.set_active(True)
    if fn.check_package_installed("arcolinux-arc-warm-pink-git"):
        self.arcolinux_arc_warm_pink.set_active(True)


def set_att_checkboxes_theming_all(self):
    """Select all arc theme checkboxes."""
    self.arcolinux_arc_aqua.set_active(True)
    self.arcolinux_arc_archlinux_blue.set_active(True)
    self.arcolinux_arc_arcolinux_blue.set_active(True)
    self.arcolinux_arc_azul.set_active(True)
    self.arcolinux_arc_azure.set_active(True)
    self.arcolinux_arc_azure_dodger_blue.set_active(True)
    self.arcolinux_arc_blood.set_active(True)
    self.arcolinux_arc_blue_sky.set_active(True)
    self.arcolinux_arc_botticelli.set_active(True)
    self.arcolinux_arc_bright_lilac.set_active(True)
    self.arcolinux_arc_carnation.set_active(True)
    self.arcolinux_arc_carolina_blue.set_active(True)
    self.arcolinux_arc_casablanca.set_active(True)
    self.arcolinux_arc_crimson.set_active(True)
    self.arcolinux_arc_dawn.set_active(True)
    self.arcolinux_arc_dodger_blue.set_active(True)
    self.arcolinux_arc_dracul.set_active(True)
    self.arcolinux_arc_emerald.set_active(True)
    self.arcolinux_arc_evopop.set_active(True)
    self.arcolinux_arc_fern.set_active(True)
    self.arcolinux_arc_fire.set_active(True)
    self.arcolinux_arc_froly.set_active(True)
    self.arcolinux_arc_havelock.set_active(True)
    self.arcolinux_arc_hibiscus.set_active(True)
    self.arcolinux_arc_light_blue_grey.set_active(True)
    self.arcolinux_arc_light_blue_surfn.set_active(True)
    self.arcolinux_arc_light_salmon.set_active(True)
    self.arcolinux_arc_mandy.set_active(True)
    self.arcolinux_arc_mantis.set_active(True)
    self.arcolinux_arc_medium_blue.set_active(True)
    self.arcolinux_arc_niagara.set_active(True)
    self.arcolinux_arc_nice_blue.set_active(True)
    self.arcolinux_arc_numix.set_active(True)
    self.arcolinux_arc_orchid.set_active(True)
    self.arcolinux_arc_pale_grey.set_active(True)
    self.arcolinux_arc_paper.set_active(True)
    self.arcolinux_arc_pink.set_active(True)
    self.arcolinux_arc_polo.set_active(True)
    self.arcolinux_arc_punch.set_active(True)
    self.arcolinux_arc_red_orange.set_active(True)
    self.arcolinux_arc_rusty_orange.set_active(True)
    self.arcolinux_arc_sky_blue.set_active(True)
    self.arcolinux_arc_slate_grey.set_active(True)
    self.arcolinux_arc_smoke.set_active(True)
    self.arcolinux_arc_soft_blue.set_active(True)
    self.arcolinux_arc_tacao.set_active(True)
    self.arcolinux_arc_tangerine.set_active(True)
    self.arcolinux_arc_tory.set_active(True)
    self.arcolinux_arc_vampire.set_active(True)
    self.arcolinux_arc_warm_pink.set_active(True)


def set_att_checkboxes_theming_blue(self):
    """Select only the blue-family arc theme checkboxes."""
    self.arcolinux_arc_aqua.set_active(True)
    self.arcolinux_arc_archlinux_blue.set_active(True)
    self.arcolinux_arc_arcolinux_blue.set_active(True)
    self.arcolinux_arc_azul.set_active(True)
    self.arcolinux_arc_azure.set_active(True)
    self.arcolinux_arc_azure_dodger_blue.set_active(True)
    self.arcolinux_arc_blood.set_active(False)
    self.arcolinux_arc_blue_sky.set_active(True)
    self.arcolinux_arc_botticelli.set_active(True)
    self.arcolinux_arc_bright_lilac.set_active(False)
    self.arcolinux_arc_carnation.set_active(False)
    self.arcolinux_arc_carolina_blue.set_active(True)
    self.arcolinux_arc_casablanca.set_active(False)
    self.arcolinux_arc_crimson.set_active(False)
    self.arcolinux_arc_dawn.set_active(False)
    self.arcolinux_arc_dodger_blue.set_active(False)
    self.arcolinux_arc_dracul.set_active(False)
    self.arcolinux_arc_emerald.set_active(False)
    self.arcolinux_arc_evopop.set_active(False)
    self.arcolinux_arc_fern.set_active(False)
    self.arcolinux_arc_fire.set_active(False)
    self.arcolinux_arc_froly.set_active(False)
    self.arcolinux_arc_havelock.set_active(True)
    self.arcolinux_arc_hibiscus.set_active(False)
    self.arcolinux_arc_light_blue_grey.set_active(False)
    self.arcolinux_arc_light_blue_surfn.set_active(False)
    self.arcolinux_arc_light_salmon.set_active(False)
    self.arcolinux_arc_mandy.set_active(False)
    self.arcolinux_arc_mantis.set_active(False)
    self.arcolinux_arc_medium_blue.set_active(True)
    self.arcolinux_arc_niagara.set_active(False)
    self.arcolinux_arc_nice_blue.set_active(True)
    self.arcolinux_arc_numix.set_active(False)
    self.arcolinux_arc_orchid.set_active(False)
    self.arcolinux_arc_pale_grey.set_active(False)
    self.arcolinux_arc_paper.set_active(False)
    self.arcolinux_arc_pink.set_active(False)
    self.arcolinux_arc_polo.set_active(True)
    self.arcolinux_arc_punch.set_active(False)
    self.arcolinux_arc_red_orange.set_active(False)
    self.arcolinux_arc_rusty_orange.set_active(False)
    self.arcolinux_arc_sky_blue.set_active(True)
    self.arcolinux_arc_slate_grey.set_active(False)
    self.arcolinux_arc_smoke.set_active(False)
    self.arcolinux_arc_soft_blue.set_active(True)
    self.arcolinux_arc_tacao.set_active(False)
    self.arcolinux_arc_tangerine.set_active(False)
    self.arcolinux_arc_tory.set_active(True)
    self.arcolinux_arc_vampire.set_active(False)
    self.arcolinux_arc_warm_pink.set_active(False)


def set_att_checkboxes_theming_dark(self):
    """Select only the dark arc theme checkboxes."""
    self.arcolinux_arc_aqua.set_active(False)
    self.arcolinux_arc_archlinux_blue.set_active(False)
    self.arcolinux_arc_arcolinux_blue.set_active(False)
    self.arcolinux_arc_azul.set_active(False)
    self.arcolinux_arc_azure.set_active(False)
    self.arcolinux_arc_azure_dodger_blue.set_active(False)
    self.arcolinux_arc_blood.set_active(False)
    self.arcolinux_arc_blue_sky.set_active(False)
    self.arcolinux_arc_botticelli.set_active(False)
    self.arcolinux_arc_bright_lilac.set_active(False)
    self.arcolinux_arc_carnation.set_active(False)
    self.arcolinux_arc_carolina_blue.set_active(False)
    self.arcolinux_arc_casablanca.set_active(False)
    self.arcolinux_arc_crimson.set_active(False)
    self.arcolinux_arc_dawn.set_active(True)
    self.arcolinux_arc_dodger_blue.set_active(True)
    self.arcolinux_arc_dracul.set_active(True)
    self.arcolinux_arc_emerald.set_active(False)
    self.arcolinux_arc_evopop.set_active(False)
    self.arcolinux_arc_fern.set_active(False)
    self.arcolinux_arc_fire.set_active(False)
    self.arcolinux_arc_froly.set_active(False)
    self.arcolinux_arc_havelock.set_active(False)
    self.arcolinux_arc_hibiscus.set_active(False)
    self.arcolinux_arc_light_blue_grey.set_active(False)
    self.arcolinux_arc_light_blue_surfn.set_active(False)
    self.arcolinux_arc_light_salmon.set_active(False)
    self.arcolinux_arc_mandy.set_active(False)
    self.arcolinux_arc_mantis.set_active(False)
    self.arcolinux_arc_medium_blue.set_active(False)
    self.arcolinux_arc_niagara.set_active(False)
    self.arcolinux_arc_nice_blue.set_active(False)
    self.arcolinux_arc_numix.set_active(False)
    self.arcolinux_arc_orchid.set_active(False)
    self.arcolinux_arc_pale_grey.set_active(True)
    self.arcolinux_arc_paper.set_active(False)
    self.arcolinux_arc_pink.set_active(False)
    self.arcolinux_arc_polo.set_active(False)
    self.arcolinux_arc_punch.set_active(False)
    self.arcolinux_arc_red_orange.set_active(False)
    self.arcolinux_arc_rusty_orange.set_active(False)
    self.arcolinux_arc_sky_blue.set_active(False)
    self.arcolinux_arc_slate_grey.set_active(True)
    self.arcolinux_arc_smoke.set_active(True)
    self.arcolinux_arc_soft_blue.set_active(False)
    self.arcolinux_arc_tacao.set_active(False)
    self.arcolinux_arc_tangerine.set_active(False)
    self.arcolinux_arc_tory.set_active(False)
    self.arcolinux_arc_vampire.set_active(True)
    self.arcolinux_arc_warm_pink.set_active(False)


def set_att_checkboxes_theming_none(self):
    """Deselect all arc theme checkboxes."""
    self.arcolinux_arc_aqua.set_active(False)
    self.arcolinux_arc_archlinux_blue.set_active(False)
    self.arcolinux_arc_arcolinux_blue.set_active(False)
    self.arcolinux_arc_azul.set_active(False)
    self.arcolinux_arc_azure.set_active(False)
    self.arcolinux_arc_azure_dodger_blue.set_active(False)
    self.arcolinux_arc_blood.set_active(False)
    self.arcolinux_arc_blue_sky.set_active(False)
    self.arcolinux_arc_botticelli.set_active(False)
    self.arcolinux_arc_bright_lilac.set_active(False)
    self.arcolinux_arc_carnation.set_active(False)
    self.arcolinux_arc_carolina_blue.set_active(False)
    self.arcolinux_arc_casablanca.set_active(False)
    self.arcolinux_arc_crimson.set_active(False)
    self.arcolinux_arc_dawn.set_active(False)
    self.arcolinux_arc_dodger_blue.set_active(False)
    self.arcolinux_arc_dracul.set_active(False)
    self.arcolinux_arc_emerald.set_active(False)
    self.arcolinux_arc_evopop.set_active(False)
    self.arcolinux_arc_fern.set_active(False)
    self.arcolinux_arc_fire.set_active(False)
    self.arcolinux_arc_froly.set_active(False)
    self.arcolinux_arc_havelock.set_active(False)
    self.arcolinux_arc_hibiscus.set_active(False)
    self.arcolinux_arc_light_blue_grey.set_active(False)
    self.arcolinux_arc_light_blue_surfn.set_active(False)
    self.arcolinux_arc_light_salmon.set_active(False)
    self.arcolinux_arc_mandy.set_active(False)
    self.arcolinux_arc_mantis.set_active(False)
    self.arcolinux_arc_medium_blue.set_active(False)
    self.arcolinux_arc_niagara.set_active(False)
    self.arcolinux_arc_nice_blue.set_active(False)
    self.arcolinux_arc_numix.set_active(False)
    self.arcolinux_arc_orchid.set_active(False)
    self.arcolinux_arc_pale_grey.set_active(False)
    self.arcolinux_arc_paper.set_active(False)
    self.arcolinux_arc_pink.set_active(False)
    self.arcolinux_arc_polo.set_active(False)
    self.arcolinux_arc_punch.set_active(False)
    self.arcolinux_arc_red_orange.set_active(False)
    self.arcolinux_arc_rusty_orange.set_active(False)
    self.arcolinux_arc_sky_blue.set_active(False)
    self.arcolinux_arc_slate_grey.set_active(False)
    self.arcolinux_arc_smoke.set_active(False)
    self.arcolinux_arc_soft_blue.set_active(False)
    self.arcolinux_arc_tacao.set_active(False)
    self.arcolinux_arc_tangerine.set_active(False)
    self.arcolinux_arc_tory.set_active(False)
    self.arcolinux_arc_vampire.set_active(False)
    self.arcolinux_arc_warm_pink.set_active(False)


# ── Themes callbacks ─────────────────────────────────────────────────


def on_install_att_themes_clicked(self, _widget):
    """Install the checked arc theme packages."""
    fn.log_subsection("Install Arc Themes")
    fn.debug_print("Installing selected Arc themes")
    install_themes(self)


def on_remove_att_themes_clicked(self, _widget):
    """Remove the checked arc theme packages."""
    fn.log_subsection("Remove Arc Themes")
    fn.debug_print("Removing selected Arc themes")
    remove_themes(self)


def on_find_att_themes_clicked(self, _widget):
    """Scan installed packages and tick matching arc theme checkboxes."""
    fn.log_subsection("Scan for Installed Themes")
    fn.debug_print("Checking which Arc themes are installed")
    find_themes(self)
    fn.log_success("Theme scan complete")


def on_click_att_theming_all_selection(self, _widget):
    """Select all arc theme checkboxes via preset."""
    fn.log_subsection("Select All Themes")
    fn.debug_print("Enabling all Arc themes for installation")
    set_att_checkboxes_theming_all(self)
    fn.log_success("All themes selected")


def on_click_att_theming_blue_selection(self, _widget):
    """Select the blue-family arc theme checkboxes via preset."""
    fn.log_subsection("Select Blue Themes")
    fn.debug_print("Enabling blue-themed Arc themes")
    set_att_checkboxes_theming_blue(self)
    fn.log_success("Blue themes selected")


def on_click_att_theming_dark_selection(self, _widget):
    """Select the dark arc theme checkboxes via preset."""
    fn.log_subsection("Select Dark Themes")
    fn.debug_print("Enabling dark-themed Arc themes")
    set_att_checkboxes_theming_dark(self)
    fn.log_success("Dark themes selected")


def on_click_att_theming_none_selection(self, _widget):
    """Deselect all arc theme checkboxes via preset."""
    fn.log_subsection("Clear Theme Selection")
    fn.debug_print("Deselecting all Arc themes")
    set_att_checkboxes_theming_none(self)
    fn.log_success("All themes deselected")


# ── System-wide dark theme toggle (/etc/environment) ───────────────

ENV_FILE = "/etc/environment"
_ARC_DAWN_GTK_LINE = 'GTK_THEME="Arc-Dawn-Dark"'


def _is_arc_dawn_active(stripped):
    return stripped == _ARC_DAWN_GTK_LINE


def _is_arc_dawn_commented(stripped):
    return stripped.startswith("#") and stripped.lstrip("#").strip() == _ARC_DAWN_GTK_LINE


def arc_dawn_gtk_state():
    """Return 'active', 'commented' or 'absent' for the Arc-Dawn-Dark GTK_THEME line in /etc/environment."""
    try:
        with open(ENV_FILE, encoding="utf-8") as env_file:
            for line in env_file:
                stripped = line.strip()
                if _is_arc_dawn_active(stripped):
                    return "active"
                if _is_arc_dawn_commented(stripped):
                    return "commented"
    except OSError as error:
        fn.log_warn(f"Could not read {ENV_FILE}: {error}")
    return "absent"


def _log_gtk_theme_outcome(new_state):
    """Explain in the terminal what the toggle changed and how to make it take effect."""
    if new_state == "commented":
        fn.log_success(f'Commented out GTK_THEME="Arc-Dawn-Dark" in {ENV_FILE}')
        fn.log_info("The system-wide dark GTK theme override is now OFF.")
        fn.log_info("Switch to the light Arc theme (or any other), then LOG OUT and LOG BACK IN to apply it.")
        fn.log_info("Heads-up: your icons may no longer match — pick an icon set that suits the new theme.")
    else:
        fn.log_success(f'Re-enabled GTK_THEME="Arc-Dawn-Dark" in {ENV_FILE}')
        fn.log_info("The system-wide dark GTK theme is back ON (Kiro's default look).")
        fn.log_info("LOG OUT and LOG BACK IN for the dark theme to apply across the whole desktop.")


# Plasma reads its own Qt theme; these /etc/environment keys override it and trigger
# the yellow "could not apply theme" popup — line 1 and 2 of a stock Kiro environment.
_PLASMA_QT_KEYS = ("QT_QPA_PLATFORMTHEME", "QT_STYLE_OVERRIDE")


def _env_key(stripped):
    body = stripped.lstrip("#").strip()
    if "=" not in body:
        return None
    return body.split("=", 1)[0].strip()


def _is_qt_override_active(stripped):
    return not stripped.startswith("#") and _env_key(stripped) in _PLASMA_QT_KEYS


def _is_qt_override_commented(stripped):
    return stripped.startswith("#") and _env_key(stripped) in _PLASMA_QT_KEYS


def _log_plasma_qt_outcome(new_state):
    """Explain the Plasma Qt-override toggle in the terminal."""
    if new_state == "commented":
        fn.log_success(f"Commented the Qt overrides (QT_QPA_PLATFORMTHEME, QT_STYLE_OVERRIDE) in {ENV_FILE}")
        fn.log_info("Plasma now controls its own Qt theme — the yellow 'could not apply theme' popup should stop.")
        fn.log_info("LOG OUT and LOG BACK IN for Plasma to take over the theming.")
    else:
        fn.log_success(f"Restored the Qt overrides (qt5ct / Kvantum) in {ENV_FILE}")
        fn.log_info("qt5ct and Kvantum drive the Qt theme again (the non-Plasma default).")
        fn.log_info("LOG OUT and LOG BACK IN for the change to take effect.")


def _toggle_env(self, is_active, is_commented, subsection):
    """Comment every active matching line, or else uncomment every commented one; return {state, changes}."""
    fn.log_subsection(subsection)
    try:
        with open(ENV_FILE, encoding="utf-8") as env_file:
            lines = env_file.readlines()
    except OSError as error:
        fn.log_error(f"Could not read {ENV_FILE}: {error}")
        fn.show_in_app_notification(self, f"Could not read {ENV_FILE}")
        return {"state": "absent", "changes": []}

    active = [i for i, line in enumerate(lines) if is_active(line.strip())]
    commented = [i for i, line in enumerate(lines) if is_commented(line.strip())]
    if not active and not commented:
        fn.log_warn(f"No matching line found in {ENV_FILE} — nothing to toggle")
        fn.show_in_app_notification(self, f"No matching line in {ENV_FILE}")
        return {"state": "absent", "changes": []}

    changes = []
    if active:
        new_state = "commented"
        for index in active:
            from_line = lines[index].strip()
            lines[index] = "#" + lines[index].lstrip()
            changes.append((from_line, lines[index].strip()))
    else:
        new_state = "active"
        for index in commented:
            from_line = lines[index].strip()
            lines[index] = lines[index].lstrip().lstrip("#").lstrip(" \t")
            changes.append((from_line, lines[index].strip()))

    try:
        fn.shutil.copy(ENV_FILE, ENV_FILE + ".bak")
        with open(ENV_FILE, "w", encoding="utf-8") as env_file:
            env_file.writelines(lines)
    except OSError as error:
        fn.log_error(f"Could not write {ENV_FILE}: {error}")
        fn.show_in_app_notification(self, f"Could not write {ENV_FILE}")
        return {"state": "absent", "changes": []}

    for from_line, to_line in changes:
        fn.log_info(f"Changed:  {from_line}  ->  {to_line}")
    return {"state": new_state, "changes": changes}


def toggle_arc_dawn_gtk_theme(self):
    """Comment/uncomment GTK_THEME="Arc-Dawn-Dark" in /etc/environment; return {state, changes}."""
    result = _toggle_env(self, _is_arc_dawn_active, _is_arc_dawn_commented, "Toggle the system-wide dark GTK theme")
    if result["state"] in ("active", "commented"):
        _log_gtk_theme_outcome(result["state"])
    return result


def toggle_plasma_qt_overrides(self):
    """Comment/uncomment the Plasma-conflicting Qt override lines in /etc/environment; return {state, changes}."""
    result = _toggle_env(self, _is_qt_override_active, _is_qt_override_commented, "Toggle the Plasma Qt overrides")
    if result["state"] in ("active", "commented"):
        _log_plasma_qt_outcome(result["state"])
    return result


# Static brand-orange labels — same on every state, on every distro.
GTK_TOGGLE_LABEL = "Enable or Disable the system-wide dark theme (/etc/environment)"
PLASMA_QT_TOGGLE_LABEL = "Enable or Disable the Plasma Qt theme overrides (/etc/environment)"


def style_toggle_button(button, text):
    """Give an /etc/environment toggle button its standing brand-orange label."""
    label = button.get_child()
    if not isinstance(label, fn.Gtk.Label):
        label = fn.Gtk.Label()
        button.set_child(label)
    label.set_markup(f'<span foreground="#FFA500">{text}</span>')


def _show_change_dialog(self, changes):
    """Pop up the before→after line(s) we changed in /etc/environment."""
    dialog = fn.Gtk.MessageDialog(
        transient_for=self,
        message_type=fn.Gtk.MessageType.INFO,
        buttons=fn.Gtk.ButtonsType.OK,
        text="Updated /etc/environment",
    )
    dialog.props.secondary_text = "\n".join(f"{from_line}  →  {to_line}" for from_line, to_line in changes)
    dialog.connect("response", lambda d, _r: d.destroy())
    dialog.show()


def open_env_in_terminal(self):
    """Open /etc/environment in a terminal editor so the user can edit it directly (non-Kiro systems)."""
    fn.log_subsection("Open /etc/environment in a terminal editor")
    if not fn.shutil.which("alacritty"):
        fn.log_warn("alacritty not found — cannot open a terminal editor")
        fn.show_in_app_notification(self, "alacritty not found — open /etc/environment manually")
        return
    script = (
        'echo "Editing /etc/environment — save and close when done, then log out and back in."; '
        "${EDITOR:-nano} /etc/environment"
    )
    fn.threading.Thread(
        target=lambda: fn.subprocess.Popen(["alacritty", "-e", "bash", "-c", script]).wait(),
        daemon=True,
    ).start()
    fn.log_info("Opened /etc/environment in a terminal editor")
    fn.show_in_app_notification(self, "Editing /etc/environment in a terminal — log out and back in after saving")


def on_click_edit_environment(self, _widget):
    """Open /etc/environment in a terminal editor (non-Kiro Themes-page reminder button)."""
    open_env_in_terminal(self)


def on_click_toggle_gtk_theme(self, _widget):
    """On Kiro: toggle the dark GTK_THEME line and pop up the change. Elsewhere: open the file to edit."""
    if fn.get_distro_label() != "Kiro":
        open_env_in_terminal(self)
        return
    result = toggle_arc_dawn_gtk_theme(self)
    if result["state"] not in ("commented", "active"):
        return
    _show_change_dialog(self, result["changes"])
    if result["state"] == "commented":
        fn.show_in_app_notification(self, "Dark theme OFF — switch theme, then log out and back in to apply")
    else:
        fn.show_in_app_notification(self, "Dark theme restored — log out and back in to apply it everywhere")


def on_click_toggle_plasma_qt(self, _widget):
    """On Kiro: comment/uncomment the Plasma-conflicting Qt overrides and pop up the change. Elsewhere: open the file."""
    if fn.get_distro_label() != "Kiro":
        open_env_in_terminal(self)
        return
    result = toggle_plasma_qt_overrides(self)
    if result["state"] not in ("commented", "active"):
        return
    _show_change_dialog(self, result["changes"])
    if result["state"] == "commented":
        fn.show_in_app_notification(self, "Qt overrides OFF — Plasma controls its theme; log out and back in")
    else:
        fn.show_in_app_notification(self, "Qt overrides restored (qt5ct/Kvantum) — log out and back in")
