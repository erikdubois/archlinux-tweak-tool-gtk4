# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0301,R1705

import functions as fn


def get_list(fle):
    """get list"""
    with open(fle, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()
    return lines


def get_value(lists, types):
    """get value"""
    try:
        pos = fn.get_position(lists, types)
        color = lists[pos].split("=")[-1].strip()

        return color
    except Exception as error:
        fn.log_error(str(error))


def move_file(self, state):
    """move file"""
    if state:
        if fn.os.path.isfile(fn.home + "/.config/i3/config-polybar"):
            fn.subprocess.run(
                [
                    "mv",
                    fn.home + "/.config/i3/config",
                    fn.home + "/.config/i3/config-bar",
                ],
                check=True,
            )
            fn.subprocess.run(
                [
                    "mv",
                    fn.home + "/.config/i3/config-polybar",
                    fn.home + "/.config/i3/config",
                ],
                check=True,
            )
        else:
            fn.messagebox(
                self,
                "OOPS!",
                "you dont seem to have <b>config-polybar</b>\
                file in your <i>~/.config/i3</i> directory. So we can not enable this feature.",
            )
            self.poly.set_active(False)
    else:
        fn.subprocess.run(
            [
                "mv",
                fn.home + "/.config/i3/config",
                fn.home + "/.config/i3/config-polybar",
            ],
            check=True,
        )
        fn.subprocess.run(
            ["mv", fn.home + "/.config/i3/config-bar", fn.home + "/.config/i3/config"],
            check=True,
        )


def toggle_polybar(self, lines, state):
    """Toggle polybar"""
    if state:
        if not check_polybar(lines):
            move_file(self, True)
    else:
        if check_polybar(lines):
            move_file(self, False)


def check_polybar(lines):
    """check polybar"""
    try:
        pos = fn.get_position(lines, "~/.config/polybar/launch.sh")
        if "#" in lines[pos]:
            return False
        else:
            return True
    except Exception as error:
        fn.log_error(str(error))
        return False


# =================================================================
# =                  I3WM
# =================================================================


def get_i3_themes(combo, lines):
    """get i3 themes"""
    _m = combo.get_model()
    _m.splice(0, _m.get_n_items(), [])
    try:
        menu = [x for x in fn.os.listdir(fn.home + "/.config/i3") if ".theme" in x]

        current_theme = fn.get_position(lines, "Theme name :")
        theme_name = (
            lines[current_theme].split(":")[1].strip().lower().replace(" ", "-")
        )  # noqa
        active = 0
        sorted_menu = sorted(menu)
        # TODO: enumerate
        for i in range(len(sorted_menu)):
            if theme_name in sorted_menu[i]:
                active = i
            combo.get_model().append(sorted_menu[i].replace(".theme", ""))
        combo.set_selected(active)
    except Exception as error:
        fn.log_error(str(error))


def set_i3_themes(lines, theme):
    """set i3 themes"""
    try:
        pos1 = fn.get_position(lines, "##START THEMING WM")
        pos2 = fn.get_position(lines, "##STOP THEMING WM")
        name = theme.lower().replace(" ", "-")
        with open(
            fn.home + "/.config/i3/" + name + ".theme", "r", encoding="utf-8"
        ) as f:
            theme_lines = f.readlines()
            f.close()
        pos3 = fn.get_position(theme_lines, "##START THEMING WM")
        pos4 = fn.get_position(theme_lines, "##STOP THEMING WM")
        lines[pos1 : pos2 + 1] = theme_lines[pos3 : pos4 + 1]
        with open(fn.i3wm_config, "w", encoding="utf-8") as f:
            f.writelines(lines)
            f.close()
    except Exception as error:
        fn.log_error(str(error))


def set_i3_themes_bar(lines, theme):
    """set i3 themes bar"""
    try:
        pos1 = fn.get_position(lines, "##START THEMING BAR")
        pos2 = fn.get_position(lines, "##STOP THEMING BAR")
        name = theme.lower().replace(" ", "-")
        with open(
            fn.home + "/.config/i3/" + name + ".theme", "r", encoding="utf-8"
        ) as f:
            theme_lines = f.readlines()
            f.close()

        pos3 = fn.get_position(theme_lines, "##START THEMING BAR")
        pos4 = fn.get_position(theme_lines, "##STOP THEMING BAR")

        lines[pos1 : pos2 + 1] = theme_lines[pos3 : pos4 + 1]

        with open(fn.i3wm_config, "w", encoding="utf-8") as f:
            f.writelines(lines)
            f.close()
    except Exception as error:
        fn.log_error(str(error))


# =================================================================
# =                  AWESOME
# =================================================================


def get_awesome_themes(lines):
    """get awesome themes"""
    theme_pos = fn.get_position(lines, "local themes = {")
    end_theme_pos = fn.get_position(lines, "local chosen_theme")

    coms = [x for x in lines[theme_pos:end_theme_pos] if '",' in x]
    theme_list = []
    for x in coms:
        theme_list.append(x.split('"')[1].strip())
    return_list = sorted(theme_list)
    return return_list


def set_awesome_theme(lines, val):
    """set awesome themes"""
    theme_pos = fn.get_position(lines, "local chosen_theme")
    lst = lines[theme_pos].split("=")[1].replace("themes[", "").replace("]", "").strip()
    lines[theme_pos] = lines[theme_pos].replace(
        "themes[" + lst + "]", "themes[" + val + "]"
    )
    with open(fn.awesome_config, "w", encoding="utf-8") as f:
        f.writelines(lines)
        f.close()


# =================================================================
# =                  QTILE
# =================================================================


def get_qtile_themes(combo, lines):
    """get qtile themes"""
    _m = combo.get_model()
    _m.splice(0, _m.get_n_items(), [])
    if fn.check_package_installed("edu-qtile-git"):
        try:
            menu = [
                x
                for x in fn.os.listdir(fn.home + "/.config/qtile/themes/")
                if ".theme" in x
            ]

            current_theme = fn.get_position(lines, "Theme name :")
            theme_name = (
                lines[current_theme].split(":")[1].strip().lower().replace(" ", "-")
            )  # noqa
            active = 0
            sorted_menu = sorted(menu)
            # TODO: enumerate
            for i in range(len(sorted_menu)):
                if theme_name in sorted_menu[i]:
                    active = i
                combo.get_model().append(sorted_menu[i].replace(".theme", ""))
            combo.set_selected(active)
        except Exception as error:
            fn.log_error(str(error))


def set_qtile_themes(lines, theme):
    """set qtile themes"""
    if fn.check_package_installed("edu-qtile-git"):
        try:
            pos1 = fn.get_position(lines, "# COLORS FOR THE BAR")
            pos2 = fn.get_position(lines, "colors = init_colors()")
            name = theme.lower().replace(" ", "-")
            with open(
                fn.home + "/.config/qtile/themes/" + name + ".theme",
                "r",
                encoding="utf-8",
            ) as f:
                theme_lines = f.readlines()
                f.close()
            pos3 = fn.get_position(theme_lines, "# COLORS FOR THE BAR")
            pos4 = fn.get_position(theme_lines, "colors = init_colors()")

            lines[pos1 : pos2 + 1] = theme_lines[pos3 : pos4 + 1]

            with open(fn.qtile_config, "w", encoding="utf-8") as f:
                f.writelines(lines)
                f.close()
        except Exception as error:
            fn.log_error(str(error))


# =================================================================
# =                  LEFTWM
# =================================================================


def get_leftwm_themes(combo, lines):
    """get leftwm themes"""
    _m = combo.get_model()
    _m.splice(0, _m.get_n_items(), [])
    if fn.check_package_installed("edu-leftwm-git"):
        try:
            menu = [
                x
                for x in fn.os.listdir(fn.home + "/.config/leftwm/themes/")
                if ".theme" in x
            ]

            current_theme = fn.get_position(lines, "Theme name :")
            theme_name = (
                lines[current_theme].split(":")[1].strip().lower().replace(" ", "-")
            )  # noqa
            active = 0
            sorted_menu = sorted(menu)
            # TODO: enumerate
            for i in range(len(sorted_menu)):
                if theme_name in sorted_menu[i]:
                    active = i
                combo.get_model().append(sorted_menu[i].replace(".theme", ""))
            combo.set_selected(active)
        except Exception as error:
            fn.log_error(str(error))


def set_leftwm_themes(theme):
    """set leftwm themes"""
    fn.subprocess.run(
        ["bash", "-c", "su - " + fn.sudo_username + ' -c "leftwm-theme update' + '"'],
        check=True,
        stdout=fn.subprocess.PIPE,
    )
    # install
    fn.subprocess.run(
        [
            "bash",
            "-c",
            "su - " + fn.sudo_username + ' -c "leftwm-theme install ' + theme + '"',
        ],
        check=True,
        stdout=fn.subprocess.PIPE,
    )
    # apply
    fn.subprocess.run(
        [
            "bash",
            "-c",
            "su - " + fn.sudo_username + ' -c "leftwm-theme apply ' + theme + '"',
        ],
        check=True,
        stdout=fn.subprocess.PIPE,
    )


def remove_leftwm_themes(theme):
    """remove leftwm themes"""
    fn.subprocess.run(
        ["bash", "-c", "su - " + fn.sudo_username + ' -c "leftwm-theme apply candy"'],
        check=True,
        stdout=fn.subprocess.PIPE,
    )
    # remove
    if not theme == "candy":
        fn.subprocess.run(
            [
                "bash",
                "-c",
                "su - "
                + fn.sudo_username
                + ' -c "leftwm-theme uninstall '
                + theme
                + ' --noconfirm"',
            ],
            check=True,
            stdout=fn.subprocess.PIPE,
        )


def reset_leftwm_themes(theme):
    """reset leftwm theme to candy"""
    fn.subprocess.run(
        ["bash", "-c", "su - " + fn.sudo_username + ' -c "leftwm-theme apply candy"'],
        check=True,
        stdout=fn.subprocess.PIPE,
    )

    # remove
    if not theme == "candy":
        fn.subprocess.run(
            [
                "bash",
                "-c",
                "su - "
                + fn.sudo_username
                + ' -c "leftwm-theme uninstall '
                + theme
                + ' --noconfirm"',
            ],
            check=True,
            stdout=fn.subprocess.PIPE,
        )

    # update
    fn.subprocess.run(
        ["bash", "-c", "su - " + fn.sudo_username + ' -c "leftwm-theme update' + '"'],
        check=True,
        stdout=fn.subprocess.PIPE,
    )

    # install
    fn.subprocess.run(
        [
            "bash",
            "-c",
            "su - " + fn.sudo_username + ' -c "leftwm-theme install ' + theme + '"',
        ],
        check=True,
        stdout=fn.subprocess.PIPE,
    )
    # apply
    fn.subprocess.run(
        [
            "bash",
            "-c",
            "su - " + fn.sudo_username + ' -c "leftwm-theme apply ' + theme + '"',
        ],
        check=True,
        stdout=fn.subprocess.PIPE,
    )

# ====================================================================
# THEMER CALLBACKS
# ====================================================================


def on_polybar_toggle(self, widget, active):
    fn.log_subsection("Toggle Polybar")
    try:
        if widget.get_active():
            fn.debug_print("Enabling polybar")
            toggle_polybar(self, get_list(fn.i3wm_config), True)
            fn.log_success("Polybar enabled")
        else:
            fn.debug_print("Disabling polybar")
            toggle_polybar(self, get_list(fn.i3wm_config), False)
            if fn.check_if_process_is_running("polybar"):
                fn.debug_print("Stopping polybar process")
                fn.subprocess.run(
                    ["killall", "-q", "polybar"], check=True, shell=False
                )
            fn.log_success("Polybar disabled")
    except Exception as error:
        fn.log_error(f"Failed to toggle polybar: {error}")
        fn.messagebox(self, "Error", f"Failed to toggle polybar: {error}")


def awesome_apply_clicked(self, widget):
    fn.log_subsection("Apply Awesome Theme")
    try:
        if not fn.path.isfile(fn.awesome_config + ".bak"):
            fn.debug_print(f"Creating backup: {fn.awesome_config}.bak")
            fn.shutil.copy(fn.awesome_config, fn.awesome_config + ".bak")

        tree_iter = self.awesome_combo.get_active_iter()
        if tree_iter is not None:
            model = self.awesome_combo.get_model()
            row_id, name = model[tree_iter][:2]
        nid = str(row_id + 1)
        fn.debug_print(f"Applying awesome theme: {nid}")
        set_awesome_theme(get_list(fn.awesome_config), nid)
        fn.log_success("Awesome theme applied successfully")
        fn.show_in_app_notification(self, "Theme set successfully")
    except Exception as error:
        fn.log_error(f"Failed to apply awesome theme: {error}")
        fn.messagebox(self, "Error", f"Failed to apply theme: {error}")


def awesome_reset_clicked(self, widget):
    fn.log_subsection("Reset Awesome Theme")
    try:
        if fn.path.isfile(fn.awesome_config + ".bak"):
            fn.debug_print("Restoring awesome config from backup")
            fn.shutil.copy(fn.awesome_config + ".bak", fn.awesome_config)
            fn.log_success("Awesome configuration reset")
            fn.show_in_app_notification(self, "Config reset successfully")

            awesome_list = get_list(fn.awesome_config)
            awesome_lines = get_awesome_themes(awesome_list)

            self.store.clear()
            for x in range(len(awesome_lines)):
                self.store.append([x, awesome_lines[x]])
            val = int(
                get_value(awesome_list, "local chosen_theme =")
                .replace("themes[", "")
                .replace("]", "")
            )
            self.awesome_combo.set_active(val - 1)
        else:
            fn.log_warn("Backup configuration not found")
    except Exception as error:
        fn.log_error(f"Failed to reset awesome theme: {error}")
        fn.messagebox(self, "Error", f"Failed to reset theme: {error}")


def i3wm_apply_clicked(self, widget):
    fn.log_subsection("Apply I3WM Theme")
    try:
        if fn.path.isfile(fn.i3wm_config):
            fn.debug_print(f"Creating backup: {fn.i3wm_config}.bak")
            fn.shutil.copy(fn.i3wm_config, fn.i3wm_config + ".bak")

        fn.debug_print(f"Applying i3wm theme: {fn.get_combo_text(self.i3_combo)}")
        set_i3_themes(
            get_list(fn.i3wm_config), fn.get_combo_text(self.i3_combo)
        )
        if not check_polybar(get_list(fn.i3wm_config)):
            fn.debug_print("Updating polybar configuration")
            set_i3_themes_bar(
                get_list(fn.i3wm_config), fn.get_combo_text(self.i3_combo)
            )
        fn.log_success("I3WM theme applied successfully")
        fn.show_in_app_notification(self, "Theme applied successfully")
    except Exception as error:
        fn.log_error(f"Failed to apply i3wm theme: {error}")
        fn.messagebox(self, "Error", f"Failed to apply theme: {error}")


def i3wm_reset_clicked(self, widget):
    fn.log_subsection("Reset I3WM Theme")
    try:
        if fn.path.isfile(fn.i3wm_config + ".bak"):
            fn.debug_print("Restoring i3wm config from backup")
            fn.shutil.copy(fn.i3wm_config + ".bak", fn.i3wm_config)
            fn.log_success("I3WM configuration reset")
            fn.show_in_app_notification(self, "Config reset successfully")

            i3_list = get_list(fn.i3wm_config)

            get_i3_themes(self.i3_combo, i3_list)
        else:
            fn.log_warn("Backup configuration not found")
    except Exception as error:
        fn.log_error(f"Failed to reset i3wm theme: {error}")
        fn.messagebox(self, "Error", f"Failed to reset theme: {error}")


def qtile_apply_clicked(self, widget):
    fn.log_subsection("Apply Qtile Theme")
    try:
        if fn.path.isfile(fn.qtile_config):
            fn.debug_print(f"Creating backup: {fn.qtile_config}.bak")
            fn.shutil.copy(fn.qtile_config, fn.qtile_config + ".bak")

        fn.debug_print(f"Applying qtile theme: {fn.get_combo_text(self.qtile_combo)}")
        set_qtile_themes(
            get_list(fn.qtile_config), fn.get_combo_text(self.qtile_combo)
        )
        fn.log_success("Qtile theme applied successfully")
        fn.show_in_app_notification(self, "Theme applied successfully")
    except Exception as error:
        fn.log_error(f"Failed to apply qtile theme: {error}")
        fn.messagebox(self, "Error", f"Failed to apply theme: {error}")


def qtile_reset_clicked(self, widget):
    fn.log_subsection("Reset Qtile Theme")
    try:
        if fn.path.isfile(fn.qtile_config + ".bak"):
            fn.debug_print("Restoring qtile config from backup")
            fn.shutil.copy(fn.qtile_config + ".bak", fn.qtile_config)
            fn.log_success("Qtile configuration reset")
            fn.show_in_app_notification(self, "Config reset successfully")

            qtile_list = get_list(fn.qtile_config)

            get_qtile_themes(self.qtile_combo, qtile_list)
        else:
            fn.log_warn("Backup configuration not found")
    except Exception as error:
        fn.log_error(f"Failed to reset qtile theme: {error}")
        fn.messagebox(self, "Error", f"Failed to reset theme: {error}")


def leftwm_apply_clicked(self, widget):
    fn.log_subsection("Apply Leftwm Theme")
    try:
        theme_name = fn.get_combo_text(self.leftwm_combo)
        fn.debug_print(f"Applying leftwm theme: {theme_name}")
        set_leftwm_themes(theme_name)
        fn.log_success(f"Leftwm theme {theme_name} applied successfully")
        fn.show_in_app_notification(
            self,
            "Theme " + theme_name + " applied successfully",
        )
        self.status_leftwm.set_markup("<b>Theme is installed and applied</b>")
    except Exception as error:
        fn.log_error(f"Failed to apply leftwm theme: {error}")
        fn.messagebox(self, "Error", f"Failed to apply theme: {error}")


def leftwm_reset_clicked(self, widget):
    fn.log_subsection("Reset Leftwm Theme")
    try:
        theme_name = fn.get_combo_text(self.leftwm_combo)
        fn.debug_print("Reverting to candy as fallback")
        reset_leftwm_themes(theme_name)
        fn.debug_print(f"Resetting theme: {theme_name}")
        fn.log_success(f"Leftwm theme {theme_name} reset successfully")
        fn.show_in_app_notification(
            self, "Theme " + theme_name + " reset successfully"
        )
        self.status_leftwm.set_markup("<b>Theme is installed and applied</b>")
    except Exception as error:
        fn.log_error(f"Failed to reset leftwm theme: {error}")
        fn.messagebox(self, "Error", f"Failed to reset theme: {error}")


def leftwm_remove_clicked(self, widget):
    fn.log_subsection("Remove Leftwm Theme")
    try:
        theme_name = fn.get_combo_text(self.leftwm_combo)
        fn.debug_print("Reverting to candy as fallback")
        remove_leftwm_themes(theme_name)
        fn.debug_print(f"Removing theme: {theme_name}")
        fn.log_success(f"Leftwm theme {theme_name} removed successfully")
        fn.show_in_app_notification(
            self,
            "Theme " + theme_name + " removed successfully",
        )
    except Exception as error:
        fn.log_error(f"Failed to remove leftwm theme: {error}")
        fn.messagebox(self, "Error", f"Failed to remove theme: {error}")


def on_leftwm_combo_changed(self, widget, pspec=None):
    link_theme = fn.path.basename(fn.os.readlink(fn.leftwm_config_theme_current))
    theme = fn.get_combo_text(self.leftwm_combo)
    if fn.path_check(fn.leftwm_config_theme + theme):
        self.status_leftwm.set_markup("<b>Theme is installed</b>")
    else:
        self.status_leftwm.set_markup("<b>Theme is NOT installed</b>")

    if fn.path_check(fn.leftwm_config_theme + theme) and link_theme == theme:
        self.status_leftwm.set_markup("<b>Theme is installed and applied</b>")
