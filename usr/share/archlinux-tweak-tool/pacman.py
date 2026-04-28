# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn


def on_nemesis_toggle(self, widget, active):
    if hasattr(self, 'initializing') and self.initializing:
        return
    from pacman_functions import repo_exist, append_repo, toggle_test_repos
    import desktopr_gui
    if not repo_exist("[nemesis_repo]"):
        append_repo(self, fn.nemesis_repo)
        fn.debug_print("Repo added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "nemesis")
    fn.update_repos(self)
    desktopr_gui.update_button_state(self, fn)
    fn.GLib.timeout_add(100, self.refresh_aur_buttons)


def on_chaotic_toggle(self, widget, active):
    if hasattr(self, 'initializing') and self.initializing:
        return
    from pacman_functions import repo_exist, append_repo, toggle_test_repos
    import desktopr_gui
    if not repo_exist("[chaotic-aur]"):
        append_repo(self, fn.chaotic_aur_repo)
        fn.debug_print("Repo added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Chaotic-AUR repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "chaotics")
    fn.update_repos(self)
    desktopr_gui.update_button_state(self, fn)
    fn.GLib.timeout_add(100, self.refresh_aur_buttons)


def on_pacman_toggle1(self, widget, active):
    if hasattr(self, 'initializing') and self.initializing:
        return
    from pacman_functions import repo_exist, append_repo, toggle_test_repos
    if not repo_exist("[core-testing]"):
        append_repo(self, fn.arch_testing_repo)
        fn.debug_print("Repo added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "testing")


def on_pacman_toggle2(self, widget, active):
    if hasattr(self, 'initializing') and self.initializing:
        return
    from pacman_functions import repo_exist, append_repo, toggle_test_repos
    if not repo_exist("[core]"):
        append_repo(self, fn.arch_core_repo)
        fn.debug_print("Repo added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "core")


def on_pacman_toggle3(self, widget, active):
    if hasattr(self, 'initializing') and self.initializing:
        return
    from pacman_functions import repo_exist, append_repo, toggle_test_repos
    if not repo_exist("[extra]"):
        append_repo(self, fn.arch_extra_repo)
        fn.debug_print("Repo added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "extra")


def on_pacman_toggle4(self, widget, active):
    if hasattr(self, 'initializing') and self.initializing:
        return
    from pacman_functions import repo_exist, append_repo, toggle_test_repos
    if not repo_exist("[extra-testing]"):
        append_repo(self, fn.arch_community_testing_repo)
        fn.debug_print("Repo added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "extra-testing")


def on_pacman_toggle5(self, widget, active):
    if hasattr(self, 'initializing') and self.initializing:
        return
    from pacman_functions import repo_exist, append_repo, toggle_test_repos
    if not repo_exist("[extra-testing]"):
        append_repo(self, fn.arch_extra_testing_repo)
        fn.debug_print("Repo added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "community")


def on_pacman_toggle6(self, widget, active):
    if hasattr(self, 'initializing') and self.initializing:
        return
    from pacman_functions import repo_exist, append_repo, toggle_test_repos
    if not repo_exist("[multilib-testing]"):
        append_repo(self, fn.arch_multilib_testing_repo)
        fn.debug_print("Repo added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "multilib-testing")


def on_pacman_toggle7(self, widget, active):
    if hasattr(self, 'initializing') and self.initializing:
        return
    from pacman_functions import repo_exist, append_repo, toggle_test_repos
    if not repo_exist("[multilib]"):
        append_repo(self, fn.arch_multilib_repo)
        fn.debug_print("Repo added to /etc/pacman.conf")
        fn.show_in_app_notification(self, "Repo has been added to /etc/pacman.conf")
    else:
        if self.opened is False:
            toggle_test_repos(self, widget.get_active(), "multilib")


def custom_repo_clicked(self, widget):
    fn.log_subsection("Adding custom repo...")
    from pacman_functions import append_repo
    custom_repo_text = self.textview_custom_repo.get_buffer()
    startiter, enditer = custom_repo_text.get_bounds()
    repo_content = custom_repo_text.get_text(startiter, enditer, True)

    if len(repo_content.strip()) < 5:
        fn.log_warn("No custom repo defined")
        fn.show_in_app_notification(self, "No custom repo defined")
        return

    fn.debug_print(f"Custom repo content: {repo_content}")
    append_repo(self, repo_content)
    try:
        fn.update_repos(self)
        fn.log_success("Custom repo added")
    except Exception as error:
        fn.log_error(f"Error: {error}")
        fn.log_warn("Check /etc/pacman.conf for correctness")


def reset_pacman_blank(self, widget):
    fn.log_subsection("Resetting pacman.conf to blank state...")
    fn.shutil.copy(fn.pacman, fn.pacman + ".bak")
    if fn.distr == "arch":
        fn.shutil.copy(fn.blank_pacman_arch, fn.pacman)
    fn.log_success("Blank pacman.conf created")
    fn.log_info("Add repositories in desired order, ATT will reboot automatically")
    fn.restart_program()


def reset_pacman_local(self, widget):
    fn.log_subsection("Resetting pacman.conf from backup...")
    if fn.path.isfile(fn.pacman + ".bak"):
        fn.shutil.copy(fn.pacman + ".bak", fn.pacman)
        fn.log_success("pacman.conf reset from .bak")
        fn.show_in_app_notification(
            self, "Default Settings Applied - check in a terminal"
        )
    fn.GLib.timeout_add(500, self.update_repos_switches)


def reset_pacman_online(self, widget):
    fn.log_subsection("Resetting pacman.conf to online defaults...")
    if fn.distr == "arch":
        fn.shutil.copy(fn.pacman_arch, fn.pacman)
    if fn.distr == "arcolinux":
        fn.shutil.copy(fn.pacman_arco, fn.pacman)
    if fn.distr == "endeavouros":
        fn.shutil.copy(fn.pacman_eos, fn.pacman)
    if fn.distr == "garuda":
        fn.shutil.copy(fn.blank_pacman_garuda, fn.pacman)
    fn.log_success("Online version of pacman.conf saved")
    fn.show_in_app_notification(
        self, "Default Settings Applied - check in a terminal"
    )
    fn.GLib.timeout_add(500, self.update_repos_switches)


def edit_pacman_conf_clicked(self, widget):
    fn.show_in_app_notification(self, "Opening pacman.conf in terminal")
    fn.subprocess.Popen(
        ["alacritty", "-e", "sudo", "nano", fn.pacman],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )


def update_repos_switches(self):
    from pacman_functions import check_repo
    self.nemesis_switch.set_active(check_repo("[nemesis_repo]"))


def check_parallel_downloads(lists, value):
    """find number of parallel downloads"""
    if fn.path.isfile(fn.pacman):
        try:
            pos = fn.get_position(lists, value)
            val = lists[pos].strip()
            return val
        except Exception as error:
            print(error)


def set_parallel_downloads(self, widget):
    """set number of parallel downloads in pacman.conf"""
    fn.log_subsection("Setting parallel downloads...")
    if fn.path.isfile(fn.pacman):
        try:
            with open(fn.pacman, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            par_downloads = fn.get_combo_text(self.parallel_downloads)
            pos_par_down = fn.get_position(lines, "ParallelDownloads")
            lines[pos_par_down] = "ParallelDownloads = " + par_downloads + "\n"

            with open(fn.pacman, "w", encoding="utf-8") as f:
                f.writelines(lines)
                f.close()
            fn.debug_print(f"Config saved: {lines[pos_par_down].strip()}")
            fn.log_success("Parallel downloads setting saved")
            fn.show_in_app_notification(self, "Settings Saved Successfully")

            # GLib.idle_add(fn.messagebox,self, "Success!!", "Settings applied successfully")
        except Exception as error:
            fn.log_error(f"Error: {error}")
            fn.messagebox(
                self,
                "Failed!!",
                'There seems to have been a problem in "set_parallel_downloads"',
            )


def pop_parallel_downloads(self):
    """populate parallel downloads for pacman"""
    if fn.path.isfile(fn.pacman):
        try:
            with open(fn.pacman, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
        except Exception as error:
            print(error)
            fn.messagebox(
                self,
                "Failed!!",
                'There seems to have been a problem in "pop_parallel_downloads"',
            )
    try:
        parallel_downloads = check_parallel_downloads(lines, "ParallelDownloads").split(
            "="
        )[1]
        active_number = int(parallel_downloads) - 1
        return active_number
    except IndexError:
        active_number = ""


def on_click_apply_parallel_downloads(self, widget):
    set_parallel_downloads(self, widget)
