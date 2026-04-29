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
    """Lazy load and check repository status when page is visible"""
    try:
        import time
        start = time.time()
        # Check all repos
        arch_testing = pacman_functions.check_repo("[core-testing]")
        arch_core = pacman_functions.check_repo("[core]")
        arch_extra = pacman_functions.check_repo("[extra]")
        arch_community = pacman_functions.check_repo("[extra-testing]")
        arch_multilib_testing = pacman_functions.check_repo("[multilib-testing]")
        arch_multilib = pacman_functions.check_repo("[multilib]")
        nemesis_repo = pacman_functions.check_repo("[nemesis_repo]")
        chaotic_repo = pacman_functions.check_repo("[chaotic-aur]")

        # Update switches without triggering callbacks
        self.checkbutton2.set_active(arch_testing)
        self.checkbutton6.set_active(arch_core)
        self.checkbutton7.set_active(arch_extra)
        self.checkbutton5.set_active(arch_community)
        self.checkbutton3.set_active(arch_multilib_testing)
        self.checkbutton8.set_active(arch_multilib)
        self.nemesis_switch.set_active(nemesis_repo)
        self.chaotic_switch.set_active(chaotic_repo)
        elapsed = time.time() - start
        fn.debug_print(f"[LAZY] Pacman repositories checked in {elapsed:.3f}s")
    except Exception:
        pass


def gui(self, Gtk, vboxstack1, fn):
    """create a gui"""
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl1 = Gtk.Label(xalign=0)
    lbl1.set_text("Pacman Config Editor")
    lbl1.set_name("title")
    hbox3.append(lbl1)

    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox4.append(hseparator)

    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    # message = Gtk.Label(xalign=0)
    # message.set_text("Refresh the pacman databases when you toggle the switch on/off")
    button_update_repos = Gtk.Button(label="Update pacman databases")
    button_update_repos.connect("clicked", functools.partial(maintenance.on_update_pacman_databases_clicked, self))
    # hbox5.pack_start(message, True, True, 0)
    hbox5.append(button_update_repos)  # pack_end

    parallel_downloads_label = Gtk.Label(xalign=1)
    parallel_downloads_label.set_markup(f"ParallelDownloads: {get_parallel_downloads(fn)}")
    parallel_downloads_label.set_margin_start(10)
    parallel_downloads_label.set_margin_end(10)
    self.parallel_downloads_label = parallel_downloads_label
    # ========================================================
    #               FOOTER
    # ========================================================

    self.custom_repo = Gtk.Button(label="Apply custom repo")
    self.custom_repo.connect("clicked", functools.partial(pacman.custom_repo_clicked, self))
    reset_pacman_local = Gtk.Button(label="Reset pacman local")
    reset_pacman_local.connect("clicked", functools.partial(pacman.reset_pacman_local, self))
    reset_pacman_online = Gtk.Button(label="Reset pacman ATT")
    reset_pacman_online.connect("clicked", functools.partial(pacman.reset_pacman_online, self))
    blank_pacman = Gtk.Button(label="Blank pacman (auto reboot) and select")
    blank_pacman.connect("clicked", functools.partial(pacman.reset_pacman_blank, self))
    edit_pacman_conf = Gtk.Button(label="Edit pacman.conf in terminal")
    edit_pacman_conf.connect("clicked", functools.partial(pacman.edit_pacman_conf_clicked, self))
    label_backup = Gtk.Label(xalign=0)
    label_backup.set_text("You can find the backup at /etc/pacman.conf.bak")

    # ==========================================================
    #                   GLOBALS
    # ==========================================================

    hboxstack1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack7 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack8 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack9 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack10 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack11 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack12 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack13 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack14 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack15 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack16 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack17 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack18 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack19 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack23 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    hboxstack24 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

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
    self.checkbutton5.connect("notify::active", functools.partial(pacman.on_pacman_toggle5, self))
    label12 = Gtk.Label(xalign=0)
    label12.set_markup("#Enable Arch Linux extra-testing repo")

    self.checkbutton7 = Gtk.Switch()
    self.checkbutton7.connect("notify::active", functools.partial(pacman.on_pacman_toggle3, self))
    label14 = Gtk.Label(xalign=0)
    label14.set_markup("Enable Arch Linux extra repo")

    self.checkbutton4 = Gtk.Switch()
    self.checkbutton4.connect("notify::active", functools.partial(pacman.on_pacman_toggle4, self))
    label10 = Gtk.Label(xalign=0)
    label10.set_markup("# Enable Arch Linux core testing repo")

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
    #               CUSTOM REPOS
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

    vboxstack2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    hboxstack1.set_margin_start(10)
    hboxstack1.set_margin_end(10)
    vboxstack2.append(hboxstack1)

    # ========================================================
    #               TESTING REPOS PACKING
    # ========================================================

    label12.set_margin_start(10)
    label12.set_margin_end(10)
    label12.set_hexpand(True)
    hboxstack14.append(label12)
    self.checkbutton5.set_margin_start(10)
    self.checkbutton5.set_margin_end(10)
    hboxstack14.append(self.checkbutton5)  # pack_end
    label3.set_margin_start(10)
    label3.set_margin_end(10)
    label3.set_hexpand(True)
    hboxstack5.append(label3)
    self.checkbutton2.set_margin_start(10)
    self.checkbutton2.set_margin_end(10)
    hboxstack5.append(self.checkbutton2)  # pack_end
    label13.set_margin_start(10)
    label13.set_margin_end(10)
    label13.set_hexpand(True)
    hboxstack15.append(label13)
    self.checkbutton6.set_margin_start(10)
    self.checkbutton6.set_margin_end(10)
    hboxstack15.append(self.checkbutton6)  # pack_end
    label14.set_margin_start(10)
    label14.set_margin_end(10)
    label14.set_hexpand(True)
    hboxstack16.append(label14)
    self.checkbutton7.set_margin_start(10)
    self.checkbutton7.set_margin_end(10)
    hboxstack16.append(self.checkbutton7)  # pack_end
    label10.set_margin_start(10)
    label10.set_margin_end(10)
    label10.set_hexpand(True)
    hboxstack12.append(label10)
    self.checkbutton4.set_margin_start(10)
    self.checkbutton4.set_margin_end(10)
    hboxstack12.append(self.checkbutton4)  # pack_end
    label4.set_margin_start(10)
    label4.set_margin_end(10)
    label4.set_hexpand(True)
    hboxstack6.append(label4)
    self.checkbutton3.set_margin_start(10)
    self.checkbutton3.set_margin_end(10)
    hboxstack6.append(self.checkbutton3)  # pack_end
    label15.set_margin_start(10)
    label15.set_margin_end(10)
    label15.set_hexpand(True)
    hboxstack17.append(label15)
    self.checkbutton8.set_margin_start(10)
    self.checkbutton8.set_margin_end(10)
    hboxstack17.append(self.checkbutton8)  # pack_end

    # ========================================================
    #               OTHER REPOS PACKING
    # ========================================================

    label11.set_margin_start(10)
    label11.set_margin_end(10)
    label11.set_hexpand(True)
    hboxstack13.append(label11)
    self.nemesis_switch.set_margin_start(10)
    self.nemesis_switch.set_margin_end(10)
    hboxstack13.append(self.nemesis_switch)  # pack_end

    hboxstack_chaotic = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_chaotic.set_margin_start(10)
    label_chaotic.set_margin_end(10)
    label_chaotic.set_hexpand(True)
    hboxstack_chaotic.append(label_chaotic)
    self.chaotic_switch.set_margin_start(10)
    self.chaotic_switch.set_margin_end(10)
    hboxstack_chaotic.append(self.chaotic_switch)  # pack_end

    vboxstack4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack4.append(hboxstack13)
    vboxstack4.append(hboxstack_chaotic)
    hboxstack11.set_margin_bottom(20)
    vboxstack4.append(hboxstack11)

    # ========================================================
    #               CUSTOM REPOS PACKING
    # ========================================================

    label2.set_margin_start(10)
    label2.set_margin_end(10)
    hboxstack2.append(label2)
    scrolled_window.set_hexpand(True)
    scrolled_window.set_vexpand(True)
    scrolled_window.set_margin_start(10)
    scrolled_window.set_margin_end(10)
    hboxstack3.append(scrolled_window)

    # ========================================================
    #               BUTTONS PACKING
    # ========================================================

    hboxstack4.append(reset_pacman_online)  # pack_end
    hboxstack4.append(reset_pacman_local)  # pack_end
    hboxstack4.append(edit_pacman_conf)  # pack_end
    # hboxstack4.pack_start(label_backup, False, False, 0)

    # ========================================================
    #               TESTING REPOS PACKING TO FRAME
    # ========================================================

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox.append(hboxstack5)
    vbox.append(hboxstack15)
    vbox.append(hboxstack14)
    vbox.append(hboxstack16)
    # vbox.pack_start(hboxstack12, False, False, 0)
    vbox.append(hboxstack6)
    hboxstack17.set_margin_bottom(10)
    vbox.append(hboxstack17)
    frame.set_child(vbox)

    # ========================================================
    #               OTHER REPOS PACKING TO FRAME
    # ========================================================

    vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox2.append(hboxstack10)
    vbox2.append(vboxstack4)
    frame2.set_child(vbox2)

    # ========================================================
    #               OTHER REPOS PACKING TO FRAME
    # ========================================================

    vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox3.append(hboxstack18)
    vbox3.append(hboxstack7)
    vbox3.append(hboxstack8)
    vbox3.append(hboxstack9)

    # ========================================================
    #               PACK TO WINDOW
    # ========================================================

    # =================ARCO REPO========================

    spacer = Gtk.Label()
    spacer.set_hexpand(True)
    hbox5.append(spacer)

    hbox5.append(parallel_downloads_label)

    aur_status = Gtk.Label(xalign=1)
    aur_status.set_margin_start(10)
    aur_status.set_margin_end(10)
    hbox5.append(aur_status)

    nemesis_status = Gtk.Label(xalign=1)
    nemesis_status.set_margin_start(10)
    nemesis_status.set_margin_end(10)
    hbox5.append(nemesis_status)

    vboxstack1.append(hbox3)
    vboxstack1.append(hbox4)
    vboxstack1.append(hbox5)
    #vboxstack1.pack_start(frame3, False, False, 5)

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
        aur_status.set_text("Chaotic-AUR: " + ("enabled" if chaotic_now else "disabled"))

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

    # =================TESTING REPO========================

    vboxstack1.append(frame)

    # =================OTHER REPO========================

    vboxstack1.append(frame2)

    # =================CUSTOM REPO========================

    vboxstack1.append(hboxstack2)
    hboxstack3.set_hexpand(True)
    hboxstack3.set_vexpand(True)
    vboxstack1.append(hboxstack3)

    hboxstack_custom_repo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    self.custom_repo.set_margin_start(10)
    self.custom_repo.set_margin_end(10)
    hboxstack_custom_repo.append(self.custom_repo)  # pack_end
    vboxstack1.append(hboxstack_custom_repo)

    hboxstack_blank_pacman = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    blank_pacman.set_margin_start(10)
    blank_pacman.set_margin_end(10)
    hboxstack_blank_pacman.append(blank_pacman)
    vboxstack1.append(hboxstack_blank_pacman)

    # =================FOOTER========================

    hboxstack4.set_margin_start(10)
    vboxstack1.append(hboxstack4)  # pack_end

    # Lazy load repository states when page becomes visible
    from gi.repository import GLib
    GLib.idle_add(init_repos_lazy_load, self, priority=GLib.PRIORITY_LOW)
