# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools
import pacman_functions
import pacman
import maintenance
import functions as fn


def get_parallel_downloads(fn):
    """Get ParallelDownloads value from pacman.conf"""
    try:
        with open(fn.pacman, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("ParallelDownloads"):
                    value = line.split("=")[1].strip()
                    return value
    except Exception:
        pass
    return "Not set"


def init_repos_lazy_load(self):
    """Check repository status and populate switches when the pacman page is opened."""
    try:
        import time
        start = time.time()
        arch_testing = pacman_functions.check_repo("[core-testing]")
        arch_core = pacman_functions.check_repo("[core]")
        arch_extra = pacman_functions.check_repo("[extra]")
        arch_extra_testing = pacman_functions.check_repo("[extra-testing]")
        arch_multilib_testing = pacman_functions.check_repo("[multilib-testing]")
        arch_multilib = pacman_functions.check_repo("[multilib]")
        nemesis_repo = pacman_functions.check_repo("[nemesis_repo]")
        chaotic_repo = pacman_functions.check_repo("[chaotic-aur]")

        self.initializing = True
        self.checkbutton2.set_active(arch_testing)
        self.checkbutton6.set_active(arch_core)
        self.checkbutton7.set_active(arch_extra)
        self.checkbutton5.set_active(arch_extra_testing)
        self.checkbutton3.set_active(arch_multilib_testing)
        self.checkbutton8.set_active(arch_multilib)
        self.nemesis_switch.set_active(nemesis_repo)
        self.chaotic_switch.set_active(chaotic_repo)
        self.initializing = False
        elapsed = time.time() - start
        fn.debug_print(f"[LAZY] Pacman repositories checked in {elapsed:.3f}s")
    except Exception:
        self.initializing = False


def gui(self, Gtk, vboxstack1, fn):
    """create a gui"""
    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl1 = Gtk.Label(xalign=0)
    lbl1.set_text("Pacman Config Editor")
    lbl1.set_name("title")
    hbox_title.append(lbl1)

    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox_sep.append(hseparator)

    hbox_toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_update_repos = Gtk.Button(label="Update pacman databases")
    button_update_repos.connect("clicked", functools.partial(maintenance.on_update_pacman_databases_clicked, self))
    hbox_toolbar.append(button_update_repos)

    parallel_downloads_label = Gtk.Label(xalign=1)
    parallel_downloads_label.set_markup(f"ParallelDownloads: {get_parallel_downloads(fn)}")
    parallel_downloads_label.set_margin_start(10)
    parallel_downloads_label.set_margin_end(10)
    self.parallel_downloads_label = parallel_downloads_label

    self.custom_repo = Gtk.Button(label="Apply custom repo")
    self.custom_repo.connect("clicked", functools.partial(pacman.custom_repo_clicked, self))
    reset_pacman_local = Gtk.Button(label="Reset your pacman local")
    reset_pacman_local.connect("clicked", functools.partial(pacman.reset_pacman_local, self))
    reset_pacman_online = Gtk.Button(label="Reset pacman ATT")
    reset_pacman_online.connect("clicked", functools.partial(pacman.reset_pacman_online, self))
    blank_pacman = Gtk.Button(label="Blank pacman (auto reboot) and select")
    blank_pacman.connect("clicked", functools.partial(pacman.reset_pacman_blank, self))
    edit_pacman_conf = Gtk.Button(label="Edit pacman.conf in terminal")
    edit_pacman_conf.connect("clicked", functools.partial(pacman.edit_pacman_conf_clicked, self))

    # ========================================================
    #               ARCHLINUX REPOS
    # ========================================================

    frame = Gtk.Frame(label="")
    framelbl = frame.get_label_widget()
    framelbl.set_markup("<b>Arch Linux repos</b>")

    self.checkbutton2 = Gtk.Switch()
    self.checkbutton2.connect("notify::active", functools.partial(pacman.on_pacman_toggle1, self))
    label3 = Gtk.Label(xalign=0)
    label3.set_markup("# Enable Arch Linux core testing repo")

    self.checkbutton6 = Gtk.Switch()
    self.checkbutton6.connect("notify::active", functools.partial(pacman.on_pacman_toggle2, self))
    label13 = Gtk.Label(xalign=0)
    label13.set_markup("Enable Arch Linux core repo")

    self.checkbutton5 = Gtk.Switch()
    self.checkbutton5.connect("notify::active", functools.partial(pacman.on_pacman_toggle4, self))
    label12 = Gtk.Label(xalign=0)
    label12.set_markup("# Enable Arch Linux extra-testing repo")

    self.checkbutton7 = Gtk.Switch()
    self.checkbutton7.connect("notify::active", functools.partial(pacman.on_pacman_toggle3, self))
    label14 = Gtk.Label(xalign=0)
    label14.set_markup("Enable Arch Linux extra repo")

    self.checkbutton3 = Gtk.Switch()
    self.checkbutton3.connect("notify::active", functools.partial(pacman.on_pacman_toggle6, self))
    label4 = Gtk.Label(xalign=0)
    label4.set_markup("# Enable Arch Linux multilib testing repo")

    self.checkbutton8 = Gtk.Switch()
    self.checkbutton8.connect("notify::active", functools.partial(pacman.on_pacman_toggle7, self))
    label15 = Gtk.Label(xalign=0)
    label15.set_markup("Enable Arch Linux multilib repo")

    # ========================================================
    #               OTHER REPOS
    # ========================================================

    frame2 = Gtk.Frame(label="")
    frame2lbl = frame2.get_label_widget()
    frame2lbl.set_markup("<b>Other repos</b>")

    self.nemesis_switch = Gtk.Switch()
    self.nemesis_switch.connect("notify::active", functools.partial(pacman.on_nemesis_toggle, self))
    label11 = Gtk.Label(xalign=0)
    label11.set_markup("Enable Nemesis repo")

    self.chaotic_switch = Gtk.Switch()
    self.chaotic_switch.connect("notify::active", functools.partial(pacman.on_chaotic_toggle, self))
    label_chaotic = Gtk.Label(xalign=0)
    label_chaotic.set_markup("Enable Chaotic-AUR repo")

    # ========================================================
    #               CUSTOM REPO
    # ========================================================

    label2 = Gtk.Label(xalign=0)
    label2.set_markup("<b>Add custom repo to pacman.conf</b>")

    self.textview_custom_repo = Gtk.TextView()
    self.textview_custom_repo.set_wrap_mode(Gtk.WrapMode.WORD)
    self.textview_custom_repo.set_editable(True)
    self.textview_custom_repo.set_cursor_visible(True)

    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    scrolled_window.set_child(self.textview_custom_repo)

    # ========================================================
    #               ARCH LINUX REPOS PACKING
    # ========================================================

    hbox_core_testing = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    label3.set_margin_start(10)
    label3.set_margin_end(10)
    label3.set_hexpand(True)
    hbox_core_testing.append(label3)
    self.checkbutton2.set_margin_start(10)
    self.checkbutton2.set_margin_end(10)
    hbox_core_testing.append(self.checkbutton2)

    hbox_core = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    label13.set_margin_start(10)
    label13.set_margin_end(10)
    label13.set_hexpand(True)
    hbox_core.append(label13)
    self.checkbutton6.set_margin_start(10)
    self.checkbutton6.set_margin_end(10)
    hbox_core.append(self.checkbutton6)

    hbox_extra_testing = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    label12.set_margin_start(10)
    label12.set_margin_end(10)
    label12.set_hexpand(True)
    hbox_extra_testing.append(label12)
    self.checkbutton5.set_margin_start(10)
    self.checkbutton5.set_margin_end(10)
    hbox_extra_testing.append(self.checkbutton5)

    hbox_extra = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    label14.set_margin_start(10)
    label14.set_margin_end(10)
    label14.set_hexpand(True)
    hbox_extra.append(label14)
    self.checkbutton7.set_margin_start(10)
    self.checkbutton7.set_margin_end(10)
    hbox_extra.append(self.checkbutton7)

    hbox_multilib_testing = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    label4.set_margin_start(10)
    label4.set_margin_end(10)
    label4.set_hexpand(True)
    hbox_multilib_testing.append(label4)
    self.checkbutton3.set_margin_start(10)
    self.checkbutton3.set_margin_end(10)
    hbox_multilib_testing.append(self.checkbutton3)

    hbox_multilib = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    label15.set_margin_start(10)
    label15.set_margin_end(10)
    label15.set_hexpand(True)
    hbox_multilib.append(label15)
    self.checkbutton8.set_margin_start(10)
    self.checkbutton8.set_margin_end(10)
    hbox_multilib.set_margin_bottom(10)
    hbox_multilib.append(self.checkbutton8)

    vbox_arch_repos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox_arch_repos.append(hbox_core_testing)
    vbox_arch_repos.append(hbox_core)
    vbox_arch_repos.append(hbox_extra_testing)
    vbox_arch_repos.append(hbox_extra)
    vbox_arch_repos.append(hbox_multilib_testing)
    vbox_arch_repos.append(hbox_multilib)
    frame.set_child(vbox_arch_repos)

    # ========================================================
    #               OTHER REPOS PACKING
    # ========================================================

    hbox_nemesis = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    label11.set_margin_start(10)
    label11.set_margin_end(10)
    label11.set_hexpand(True)
    hbox_nemesis.append(label11)
    self.nemesis_switch.set_margin_start(10)
    self.nemesis_switch.set_margin_end(10)
    hbox_nemesis.append(self.nemesis_switch)

    hbox_chaotic = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_chaotic.set_margin_start(10)
    label_chaotic.set_margin_end(10)
    label_chaotic.set_hexpand(True)
    hbox_chaotic.append(label_chaotic)
    self.chaotic_switch.set_margin_start(10)
    self.chaotic_switch.set_margin_end(10)
    hbox_chaotic.append(self.chaotic_switch)

    vbox_other_repos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox_other_repos.set_margin_bottom(20)
    vbox_other_repos.append(hbox_nemesis)
    vbox_other_repos.append(hbox_chaotic)
    frame2.set_child(vbox_other_repos)

    # ========================================================
    #               CUSTOM REPO PACKING
    # ========================================================

    hbox_custom_label = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    label2.set_margin_start(10)
    label2.set_margin_end(10)
    hbox_custom_label.append(label2)

    hbox_custom_scroll = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hbox_custom_scroll.set_hexpand(True)
    hbox_custom_scroll.set_vexpand(True)
    scrolled_window.set_hexpand(True)
    scrolled_window.set_vexpand(True)
    scrolled_window.set_margin_start(10)
    scrolled_window.set_margin_end(10)
    hbox_custom_scroll.append(scrolled_window)

    # ========================================================
    #               FOOTER BUTTONS PACKING
    # ========================================================

    hbox_footer_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hbox_footer_buttons.set_margin_start(10)
    hbox_footer_buttons.append(reset_pacman_online)
    hbox_footer_buttons.append(reset_pacman_local)
    hbox_footer_buttons.append(edit_pacman_conf)

    # ========================================================
    #               TOOLBAR STATUS LABELS
    # ========================================================

    spacer = Gtk.Label()
    spacer.set_hexpand(True)
    hbox_toolbar.append(spacer)
    hbox_toolbar.append(parallel_downloads_label)

    aur_status = Gtk.Label(xalign=1)
    aur_status.set_margin_start(10)
    aur_status.set_margin_end(10)
    hbox_toolbar.append(aur_status)

    nemesis_status = Gtk.Label(xalign=1)
    nemesis_status.set_margin_start(10)
    nemesis_status.set_margin_end(10)
    hbox_toolbar.append(nemesis_status)

    vboxstack1.append(hbox_title)
    vboxstack1.append(hbox_sep)
    vboxstack1.append(hbox_toolbar)

    # =================AUR HELPER========================

    hbox_aur_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator_aur = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator_aur.set_hexpand(True)
    hbox_aur_sep.append(hseparator_aur)

    hbox_aur_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    aur_title = Gtk.Label(xalign=0)
    aur_title.set_markup("<b>AUR Helper</b>")
    aur_title.set_margin_start(10)
    aur_title.set_margin_end(10)
    hbox_aur_title.append(aur_title)

    hbox_aur_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    btn_aur_yay = Gtk.Button()
    btn_aur_paru = Gtk.Button()
    yay_handler_id = [None]
    paru_handler_id = [None]

    def refresh_aur_buttons():
        if yay_handler_id[0]:
            btn_aur_yay.disconnect(yay_handler_id[0])
            yay_handler_id[0] = None
        if paru_handler_id[0]:
            btn_aur_paru.disconnect(paru_handler_id[0])
            paru_handler_id[0] = None

        chaotic_now = pacman_functions.is_chaotic_aur_enabled()
        aur_status.set_text("Chaotic-Aur repo: " + ("enabled" if chaotic_now else "disabled"))

        nemesis_now = pacman_functions.check_repo("[nemesis_repo]")
        nemesis_status.set_text("Nemesis repo: " + ("enabled" if nemesis_now else "disabled"))

        def wait_and_refresh(process, success_msg):
            if process is None:
                fn.GLib.idle_add(refresh_aur_buttons)
                return
            fn.debug_print("Waiting for terminal to close...")
            process.wait()
            fn.debug_print("Terminal closed — refreshing AUR button labels")
            fn.log_success(success_msg)
            fn.GLib.idle_add(lambda: fn.show_in_app_notification(self, success_msg))
            fn.GLib.idle_add(refresh_aur_buttons)

        if fn.path.exists("/usr/bin/yay"):
            btn_aur_yay.set_label("Remove yay-git")
            yay_handler_id[0] = btn_aur_yay.connect(
                "clicked",
                lambda w: fn.threading.Thread(
                    target=wait_and_refresh,
                    args=(pacman_functions.remove_aur_helper(self, "yay"), "yay-git removed"),
                    daemon=True,
                ).start(),
            )
        else:
            btn_aur_yay.set_label("Install yay-git")
            if chaotic_now:
                yay_handler_id[0] = btn_aur_yay.connect(
                    "clicked",
                    lambda w: fn.threading.Thread(
                        target=wait_and_refresh,
                        args=(pacman_functions.install_yay_pacman(self), "yay-git installed"),
                        daemon=True,
                    ).start(),
                )
            else:
                yay_handler_id[0] = btn_aur_yay.connect(
                    "clicked",
                    lambda w: fn.threading.Thread(
                        target=wait_and_refresh,
                        args=(pacman_functions.install_yay_git(self), "yay-git installed"),
                        daemon=True,
                    ).start(),
                )

        if fn.path.exists("/usr/bin/paru"):
            btn_aur_paru.set_label("Remove paru-git")
            paru_handler_id[0] = btn_aur_paru.connect(
                "clicked",
                lambda w: fn.threading.Thread(
                    target=wait_and_refresh,
                    args=(pacman_functions.remove_aur_helper(self, "paru"), "paru-git removed"),
                    daemon=True,
                ).start(),
            )
        else:
            btn_aur_paru.set_label("Install paru-git")
            if chaotic_now:
                paru_handler_id[0] = btn_aur_paru.connect(
                    "clicked",
                    lambda w: fn.threading.Thread(
                        target=wait_and_refresh,
                        args=(pacman_functions.install_paru_pacman(self), "paru-git installed"),
                        daemon=True,
                    ).start(),
                )
            else:
                paru_handler_id[0] = btn_aur_paru.connect(
                    "clicked",
                    lambda w: fn.threading.Thread(
                        target=wait_and_refresh,
                        args=(pacman_functions.install_paru_git(self), "paru-git installed"),
                        daemon=True,
                    ).start(),
                )
        return False

    refresh_aur_buttons()
    self.refresh_aur_buttons = refresh_aur_buttons

    hbox_aur_buttons.set_hexpand(True)
    btn_aur_yay.set_hexpand(True)
    btn_aur_paru.set_hexpand(True)
    hbox_aur_buttons.append(btn_aur_yay)
    hbox_aur_buttons.append(btn_aur_paru)

    vboxstack1.append(hbox_aur_sep)
    vboxstack1.append(hbox_aur_title)
    vboxstack1.append(hbox_aur_buttons)

    # =================ARCH REPOS FRAME========================

    vboxstack1.append(frame)

    # =================OTHER REPOS FRAME========================

    vboxstack1.append(frame2)

    # =================CUSTOM REPO========================

    vboxstack1.append(hbox_custom_label)
    vboxstack1.append(hbox_custom_scroll)

    hbox_apply_custom_repo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    self.custom_repo.set_margin_start(10)
    self.custom_repo.set_margin_end(10)
    hbox_apply_custom_repo.append(self.custom_repo)
    vboxstack1.append(hbox_apply_custom_repo)

    hbox_blank_pacman = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    blank_pacman.set_margin_start(10)
    blank_pacman.set_margin_end(10)
    hbox_blank_pacman.append(blank_pacman)
    vboxstack1.append(hbox_blank_pacman)

    # =================FOOTER========================

    vboxstack1.append(hbox_footer_buttons)

    vboxstack1.connect("map", lambda _w: init_repos_lazy_load(self))
