# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn


def _refresh_ublock_label(self):
    installed = fn.check_package_installed("firefox-ublock-origin")
    self.lbl_ublock.set_markup(
        "uBlock Origin for Firefox" + (" <b>installed</b>" if installed else "")
    )


def _refresh_hblock_label(self):
    installed = fn.check_package_installed("edu-hblock-git")
    self.lbl_hblock.set_markup(
        "hblock — ad/tracker blocking via /etc/hosts" + (" <b>installed</b>" if installed else "")
    )
    self.btn_enable_hblock.set_sensitive(installed)
    self.btn_disable_hblock.set_sensitive(installed)


def on_click_install_ublock(self, _widget):
    if fn.check_package_installed("firefox-ublock-origin"):
        fn.log_info("uBlock Origin is already installed")
        fn.show_in_app_notification(self, "uBlock Origin is already installed")
        return
    fn.log_subsection("Install uBlock Origin")
    script = "sudo pacman -S firefox-ublock-origin --needed; read -p 'Press enter to close'"
    process = fn.subprocess.Popen(
        ["alacritty", "-e", "bash", "-c", script],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )

    def wait_and_refresh():
        process.wait()
        fn.GLib.idle_add(_refresh_ublock_label, self)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_click_remove_ublock(self, _widget):
    if not fn.check_package_installed("firefox-ublock-origin"):
        fn.log_info("uBlock Origin is not installed")
        fn.show_in_app_notification(self, "uBlock Origin is not installed")
        return
    fn.log_subsection("Remove uBlock Origin")
    script = "sudo pacman -Rs firefox-ublock-origin; read -p 'Press enter to close'"
    process = fn.subprocess.Popen(
        ["alacritty", "-e", "bash", "-c", script],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )

    def wait_and_refresh():
        process.wait()
        fn.GLib.idle_add(_refresh_ublock_label, self)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_click_install_hblock(self, _widget):
    if fn.check_package_installed("edu-hblock-git"):
        fn.log_info("hblock is already installed")
        fn.show_in_app_notification(self, "hblock is already installed")
        return
    fn.log_subsection("Install hblock")
    script = "sudo pacman -S edu-hblock-git --needed; read -p 'Press enter to close'"
    process = fn.subprocess.Popen(
        ["alacritty", "-e", "bash", "-c", script],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )

    def wait_and_refresh():
        process.wait()
        fn.GLib.idle_add(_refresh_hblock_label, self)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_click_remove_hblock(self, _widget):
    if not fn.check_package_installed("edu-hblock-git"):
        fn.log_info("hblock is not installed")
        fn.show_in_app_notification(self, "hblock is not installed")
        return
    fn.log_subsection("Remove hblock")
    script = "sudo pacman -Rs edu-hblock-git; read -p 'Press enter to close'"
    process = fn.subprocess.Popen(
        ["alacritty", "-e", "bash", "-c", script],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )

    def wait_and_refresh():
        process.wait()
        fn.GLib.idle_add(_refresh_hblock_label, self)

    fn.threading.Thread(target=wait_and_refresh, daemon=True).start()


def on_click_enable_hblock(self, _widget):
    if not fn.check_package_installed("edu-hblock-git"):
        fn.log_info("hblock is not installed")
        fn.show_in_app_notification(self, "hblock is not installed — install it first")
        return
    fn.log_subsection("Enable hblock")

    def run_enable():
        stop_pulse = fn.threading.Event()

        def _pulse():
            while not stop_pulse.is_set():
                fn.GLib.idle_add(self.progress.pulse)
                fn.time.sleep(0.1)

        fn.GLib.idle_add(self.btn_enable_hblock.set_sensitive, False)
        fn.GLib.idle_add(self.btn_disable_hblock.set_sensitive, False)
        fn.GLib.idle_add(self.label7.set_text, "Enabling hblock...")
        fn.GLib.idle_add(self.label7.set_visible, True)
        fn.GLib.idle_add(self.progress.set_visible, True)
        fn.threading.Thread(target=_pulse, daemon=True).start()
        fn.subprocess.run(
            ["/usr/bin/hblock"],
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.PIPE,
        )
        stop_pulse.set()
        fn.log_success("hblock enabled")
        fn.GLib.idle_add(self.progress.set_visible, False)
        fn.GLib.idle_add(self.label7.set_text, "hblock enabled")
        fn.GLib.idle_add(self.label7.set_visible, False)
        fn.GLib.idle_add(fn.show_in_app_notification, self, "hblock enabled")
        fn.GLib.idle_add(
            self.lbl_hblock_status.set_markup,
            "Enable or disable hblock — check /etc/hosts <b>enabled</b>",
        )
        fn.GLib.idle_add(self.btn_enable_hblock.set_sensitive, True)
        fn.GLib.idle_add(self.btn_disable_hblock.set_sensitive, True)

    fn.threading.Thread(target=run_enable, daemon=True).start()


def on_click_disable_hblock(self, _widget):
    if not fn.check_package_installed("edu-hblock-git"):
        fn.log_info("hblock is not installed")
        fn.show_in_app_notification(self, "hblock is not installed")
        return
    fn.log_subsection("Disable hblock")

    def run_disable():
        stop_pulse = fn.threading.Event()

        def _pulse():
            while not stop_pulse.is_set():
                fn.GLib.idle_add(self.progress.pulse)
                fn.time.sleep(0.1)

        fn.GLib.idle_add(self.btn_enable_hblock.set_sensitive, False)
        fn.GLib.idle_add(self.btn_disable_hblock.set_sensitive, False)
        fn.GLib.idle_add(self.label7.set_text, "Disabling hblock...")
        fn.GLib.idle_add(self.label7.set_visible, True)
        fn.GLib.idle_add(self.progress.set_visible, True)
        fn.threading.Thread(target=_pulse, daemon=True).start()
        fn.subprocess.run(
            ["sh", "-c", "HBLOCK_SOURCES='' /usr/bin/hblock"],
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.PIPE,
        )
        stop_pulse.set()
        fn.log_success("hblock disabled")
        fn.GLib.idle_add(self.progress.set_visible, False)
        fn.GLib.idle_add(self.label7.set_text, "hblock disabled")
        fn.GLib.idle_add(self.label7.set_visible, False)
        fn.GLib.idle_add(fn.show_in_app_notification, self, "hblock disabled")
        fn.GLib.idle_add(
            self.lbl_hblock_status.set_markup,
            "Enable or disable hblock — check /etc/hosts disabled",
        )
        fn.GLib.idle_add(self.btn_enable_hblock.set_sensitive, True)
        fn.GLib.idle_add(self.btn_disable_hblock.set_sensitive, True)

    fn.threading.Thread(target=run_disable, daemon=True).start()
