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
        themes_to_install.append("edu-arc-dawn-git")
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
        themes_to_remove.append("edu-arc-dawn-git")
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
    if fn.check_package_installed("edu-arc-dawn-git"):
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

# ====================================================================
# THEMES CALLBACKS
# ====================================================================


def on_install_att_themes_clicked(self, _widget):
    fn.log_subsection("Install Arc Themes")
    fn.debug_print("Installing selected Arc themes")
    install_themes(self)


def on_remove_att_themes_clicked(self, _widget):
    fn.log_subsection("Remove Arc Themes")
    fn.debug_print("Removing selected Arc themes")
    remove_themes(self)


def on_find_att_themes_clicked(self, _widget):
    fn.log_subsection("Scan for Installed Themes")
    fn.debug_print("Checking which Arc themes are installed")
    find_themes(self)
    fn.log_success("Theme scan complete")


def on_click_att_theming_all_selection(self, _widget):
    fn.log_subsection("Select All Themes")
    fn.debug_print("Enabling all Arc themes for installation")
    set_att_checkboxes_theming_all(self)
    fn.log_success("All themes selected")


def on_click_att_theming_blue_selection(self, _widget):
    fn.log_subsection("Select Blue Themes")
    fn.debug_print("Enabling blue-themed Arc themes")
    set_att_checkboxes_theming_blue(self)
    fn.log_success("Blue themes selected")


def on_click_att_theming_dark_selection(self, _widget):
    fn.log_subsection("Select Dark Themes")
    fn.debug_print("Enabling dark-themed Arc themes")
    set_att_checkboxes_theming_dark(self)
    fn.log_success("Dark themes selected")


def on_click_att_theming_none_selection(self, _widget):
    fn.log_subsection("Clear Theme Selection")
    fn.debug_print("Deselecting all Arc themes")
    set_att_checkboxes_theming_none(self)
    fn.log_success("All themes deselected")
