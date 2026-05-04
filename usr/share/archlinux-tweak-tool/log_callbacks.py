# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn

# ====================================================================
# LOGGING CALLBACKS
# ====================================================================


def on_click_log_current_boot(self, _widget):
    if not fn.check_package_installed("fzf"):
        fn.log_info("fzf is not installed — please install it first")
        fn.show_in_app_notification(self, "fzf is required — install it first")
        return
    try:
        fn.log_subsection("Launching current boot log viewer...")
        fn.subprocess.Popen(
            "alacritty -e bash -c 'SYSTEMD_COLORS=1 journalctl -b 0 | fzf --ansi'",
            shell=True,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_log_prev_boot(self, _widget):
    if not fn.check_package_installed("fzf"):
        fn.log_info("fzf is not installed — please install it first")
        fn.show_in_app_notification(self, "fzf is required — install it first")
        return
    try:
        fn.log_subsection("Launching previous boot log viewer...")
        fn.subprocess.Popen(
            "alacritty -e bash -c 'SYSTEMD_COLORS=1 journalctl -b -1 | fzf --ansi'",
            shell=True,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_log_errors(self, _widget):
    if not fn.check_package_installed("fzf"):
        fn.log_info("fzf is not installed — please install it first")
        fn.show_in_app_notification(self, "fzf is required — install it first")
        return
    try:
        fn.log_subsection("Launching system errors log viewer...")
        fn.subprocess.Popen(
            "alacritty -e bash -c 'SYSTEMD_COLORS=1 journalctl -b -p err | fzf --ansi'",
            shell=True,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_log_recent(self, _widget):
    if not fn.check_package_installed("fzf"):
        fn.log_info("fzf is not installed — please install it first")
        fn.show_in_app_notification(self, "fzf is required — install it first")
        return
    try:
        fn.log_subsection("Launching recent logs viewer...")
        fn.subprocess.Popen(
            'alacritty -e bash -c \'SYSTEMD_COLORS=1 journalctl --since "20 minutes ago" | fzf --ansi\'',
            shell=True,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_log_xorg(self, _widget):
    for pkg in ("fzf", "bat"):
        if not fn.check_package_installed(pkg):
            fn.log_info(f"{pkg} is not installed — please install it first")
            fn.show_in_app_notification(self, f"{pkg} is required — install it first")
            return
    try:
        fn.log_subsection("Launching Xorg log viewer...")
        fn.subprocess.Popen(
            "alacritty -e bash -c 'bat --color=always /var/log/Xorg.0.log | fzf --ansi'",
            shell=True,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_log_pacman(self, _widget):
    for pkg in ("fzf", "bat"):
        if not fn.check_package_installed(pkg):
            fn.log_info(f"{pkg} is not installed — please install it first")
            fn.show_in_app_notification(self, f"{pkg} is required — install it first")
            return
    try:
        fn.log_subsection("Launching pacman log viewer...")
        fn.subprocess.Popen(
            "alacritty -e bash -c 'bat --color=always /var/log/pacman.log | fzf --ansi'",
            shell=True,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_log_xsession(self, _widget):
    for pkg in ("fzf", "bat"):
        if not fn.check_package_installed(pkg):
            fn.log_info(f"{pkg} is not installed — please install it first")
            fn.show_in_app_notification(self, f"{pkg} is required — install it first")
            return
    try:
        fn.log_subsection("Launching X session log viewer...")
        cmd = (
            "alacritty -e bash -c '"
            "found=; "
            "for f in ~/.xsession-errors ~/.local/share/xorg/Xorg.0.log /var/log/Xorg.0.log; do "
            "  [ -s \"$f\" ] && { found=$f; break; }; "
            "done; "
            "if [ -n \"$found\" ]; then bat --color=always \"$found\" | fzf --ansi; "
            "else echo \"No X session error file found\"; read; fi'"
        )
        fn.subprocess.Popen(cmd, shell=True)
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_log_blame(self, _widget):
    if not fn.check_package_installed("fzf"):
        fn.log_info("fzf is not installed — please install it first")
        fn.show_in_app_notification(self, "fzf is required — install it first")
        return
    try:
        fn.log_subsection("Launching boot blame analyzer...")
        fn.subprocess.Popen(
            "alacritty -e bash -c 'systemd-analyze blame | fzf --ansi'",
            shell=True,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")


def on_click_log_dmesg(self, _widget):
    if not fn.check_package_installed("fzf"):
        fn.log_info("fzf is not installed — please install it first")
        fn.show_in_app_notification(self, "fzf is required — install it first")
        return
    try:
        fn.log_subsection("Launching kernel messages viewer...")
        fn.subprocess.Popen(
            "alacritty -e bash -c 'sudo dmesg --color=always | fzf --ansi'",
            shell=True,
        )
    except Exception as error:
        fn.log_error(f"Error: {error}")
