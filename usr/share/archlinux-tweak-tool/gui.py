# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

# ============Functions============
import functions as fn
import functions_startup
import settings

import desktopr
import maintenance
import fastfetch
import performance
import sddm
import icons
import themes
import themer
import user
import zsh_theme

# =============GUI=================
import icons_gui
import themes_gui
import autostart
import desktopr_gui
import maintenance_gui
import fastfetch_gui
import kernel_gui
import pacman_gui
import performance_gui
import sddm_gui
import privacy_gui
import services_gui
import shell_gui
import themer_gui
import user_gui
import ai_gui
import logging_gui
import network_gui
import system_gui
import software_gui
import packages_gui
import wallpaper
import wallpaper_gui
import plymouth_gui


def gui(self, Gtk, Gdk, GdkPixbuf, base_dir, os, Pango, GLib):
    """creation of the gui"""

    # =======================================================
    #                       App Notifications
    # =======================================================

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    self.notification_revealer = Gtk.Revealer()
    self.notification_revealer.set_reveal_child(False)

    self.notification_label = Gtk.Label()
    self.notification_label.set_hexpand(True)

    notification_bg = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    notification_bg.set_size_request(-1, 30)
    notification_bg.add_css_class("att-notification-bar")
    notification_bg.append(self.notification_label)

    css_notif = Gtk.CssProvider()
    css_notif.load_from_data(b".att-notification-bar { background-color: #1a1a1a; }")
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        css_notif,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )

    self.notification_revealer.set_child(notification_bg)

    self.notification_revealer.set_hexpand(True)
    self.notification_revealer.set_vexpand(False)
    hbox0.append(self.notification_revealer)

    # ==========================================================
    #                       CONTAINER
    # ==========================================================

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

    hbox.set_hexpand(True)
    hbox.set_vexpand(True)
    vbox.append(hbox0)
    vbox.append(hbox)
    self.set_child(vbox)

    # ==========================================================
    #                    INITIALIZE STACK
    # ==========================================================
    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
    stack.set_transition_duration(350)

    vboxstack1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack8 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack10 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack12 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack13 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack14 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack18 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack19 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack23 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack25 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack26 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack27 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack28 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack_sddm = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack_ai = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack_logging = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack_network = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack_system = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack_software = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack_themes = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack_wallpaper = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack_plymouth = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    # ==========================================================
    #                 ICONS
    # ==========================================================

    icons_gui.gui(self, Gtk, GdkPixbuf, vboxstack25, icons, fn, base_dir)

    # ==========================================================
    #                THEMES
    # ==========================================================

    themes_gui.gui(self, Gtk, GdkPixbuf, vboxstack_themes, themes, fn, base_dir)

    # ==========================================================
    #                AUTOSTART
    # ==========================================================

    autostart.gui(self, Gtk, vboxstack13, fn)

    # ==========================================================
    #                DESKTOP
    # ==========================================================

    desktopr_gui.gui(self, Gtk, GdkPixbuf, vboxstack12, desktopr, fn, base_dir)

    # # ==========================================================
    # #               FASTFETCH
    # # ==========================================================

    functions_startup.setup_fastfetch_config()
    if fn.file_check(fn.fastfetch_config):
        fastfetch_gui.gui(self, Gtk, GdkPixbuf, vboxstack8, fastfetch, fn, base_dir)
    else:
        hbox31 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl1 = Gtk.Label(xalign=0)
        lbl1.set_text("fastfetch Editor")
        lbl1.set_name("title")
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(False)
        hbox41.append(hseparator)
        hbox31.append(lbl1)
        vboxstack8.append(hbox31)
        vboxstack8.append(hbox41)
        fastfetch_message = Gtk.Label()
        fastfetch_message.set_hexpand(True)
        fastfetch_message.set_markup(
            "fastfetch configuration file not found.\n"
            "Install <b>fastfetch</b> and enable it to use this tab."
        )
        vboxstack8.append(fastfetch_message)

    # # ==========================================================
    # #               MAINTENANCE
    # # ==========================================================

    maintenance_gui.gui(self, Gtk, Gdk, GdkPixbuf, vboxstack19, fn, maintenance)

    # ==========================================================
    #                 PACMAN
    # ==========================================================

    if fn.file_check(fn.pacman):
        pacman_gui.gui(self, Gtk, vboxstack1, fn)

    # ==========================================================
    #                 PRIVACY - HBLOCK
    # ==========================================================

    privacy_gui.gui(self, Gtk, vboxstack3, fn)

    # ==========================================================
    #                      SERVICES
    # ==========================================================

    services_gui.gui(self, Gtk, vboxstack14, fn)

    # ==========================================================
    #                        SHELLS
    # ==========================================================

    shell_gui.gui(self, Gtk, vboxstack23, zsh_theme, base_dir, GdkPixbuf, fn)

    # ==========================================================
    #                 THEMES
    # ==========================================================

    themer_gui.gui(self, Gtk, GdkPixbuf, vboxstack10, themer, fn, base_dir)
    self.on_desktop_changed = lambda: themer_gui.refresh_themer_dropdowns(self, fn, themer)

    # # ==========================================================
    # #                USER
    # # ==========================================================

    user_gui.gui(self, Gtk, vboxstack18, user, fn)

    # =====================================================
    #                       PACKAGES - EXPORT/INSTALL
    # =====================================================

    packages_gui.gui(self, Gtk, vboxstack26, fn)

    # =====================================================
    #                       PERFORMANCE
    # =====================================================

    if fn.distr != "artix":
        performance_gui.gui(self, Gtk, vboxstack27, performance, fn)

    sddm_gui.gui(self, Gtk, Pango, vboxstack_sddm, sddm, fn)

    kernel_gui.gui(self, Gtk, vboxstack28, fn)

    ai_gui.gui(self, Gtk, vboxstack_ai, fn)

    logging_gui.gui(self, Gtk, vboxstack_logging, fn)

    network_gui.gui(self, Gtk, vboxstack_network, fn)

    system_gui.gui(self, Gtk, vboxstack_system, fn)

    software_gui.gui(self, Gtk, vboxstack_software, fn)

    wallpaper_gui.gui(self, Gtk, Pango, vboxstack_wallpaper, wallpaper, fn, base_dir)

    if fn.check_content("omarchy", "/etc/plymouth/plymouthd.conf"):
        plymouth_gui.gui(self, Gtk, vboxstack_plymouth, fn)

    # ==========================================================
    #                   ADD TO WINDOW
    # ==========================================================
    stack.add_titled(vboxstack_ai, "stack_ai", "AI Tools")  # AI tools

    stack.add_titled(vboxstack13, "stack13", "Autostart")  # Autostart

    stack.add_titled(vboxstack12, "stack12", "Desktop")  # Desktop installer

    stack.add_titled(vboxstack8, "stack4", "Fastfetch")  # fastfetch config

    stack.add_titled(vboxstack25, "stack25", "Icons")  # Icons and themes

    stack.add_titled(vboxstack28, "stack28", "Kernels")  # kernel manager

    stack.add_titled(vboxstack_logging, "stack_logging", "Logging")  # log investigator

    stack.add_titled(vboxstack19, "stack19", "Maintenance")  # Maintenance

    stack.add_titled(vboxstack_network, "stack_network", "Network")  # network + samba

    stack.add_titled(vboxstack26, "packages", "Packages")  # Packages

    stack.add_titled(vboxstack1, "stack6", "Pacman")  # Pacman config

    if fn.check_content("omarchy", "/etc/plymouth/plymouthd.conf"):
        stack.add_titled(vboxstack_plymouth, "stack_plymouth", "Plymouth")  # Plymouth boot theme

    stack.add_titled(vboxstack3, "stack2", "Privacy")  # Privacy

    if fn.distr != "artix":
        stack.add_titled(vboxstack27, "stack27", "Performance")  # performance

    stack.add_titled(vboxstack_sddm, "stack_sddm", "Sddm")  # sddm

    if fn.distr != "artix":
        stack.add_titled(vboxstack14, "stack14", "Services")  # services

    stack.add_titled(vboxstack23, "stack23", "Shells")  # shell

    stack.add_titled(vboxstack_software, "stack_software", "Software")  # software installers

    stack.add_titled(vboxstack_system, "stack_system", "System")  # system inspector

    stack.add_titled(vboxstack10, "stack11", "Themer")  # Themer

    stack.add_titled(vboxstack_themes, "stack_themes", "Themes")  # arc themes

    stack.add_titled(vboxstack18, "stack18", "User")  # user

    stack.add_titled(vboxstack_wallpaper, "stack_wallpaper", "Wallpaper")  # wallpaper

    stack_switcher = Gtk.StackSidebar()
    stack_switcher.set_name("sidebar")
    stack_switcher.set_stack(stack)

    # =====================================================
    #                       LOGO
    # =====================================================

    ivbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    # =====================================================
    #               RESTART/QUIT BUTTON
    # =====================================================

    def on_quit(widget):
        fn.unlink("/tmp/att.lock")
        self.get_application().quit()
        fn.debug_print("Thanks for using ArchLinux Tweak Tool")
        fn.debug_print("Report issues to make it even better")
        fn.debug_print("=" * 75)

    lbl_distro = Gtk.Label(xalign=0)
    lbl_distro.set_markup("Working on\n" + fn.change_distro_label(fn.distr))
    btn_restart_att = Gtk.Button(label="Restart ATT")
    btn_restart_att.set_size_request(100, 30)
    btn_restart_att.set_visible(False)
    btn_restart_att.connect("clicked", self.on_refresh_att_clicked)
    btn_quit_att = Gtk.Button(label="Quit ATT")
    btn_quit_att.set_size_request(100, 30)
    btn_quit_att.connect("clicked", on_quit)

    # =====================================================
    #                      PACKS
    # =====================================================

    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

    btn_dark_theme = Gtk.Button()
    btn_dark_theme.set_size_request(100, 30)

    # read saved preference and set initial state (default: on)
    dark_state = [True]
    try:
        secs = settings.read_section()
        if "APPEARANCE" in secs:
            dark_state[0] = settings.read_settings("APPEARANCE", "dark_theme") == "True"
    except Exception:
        pass

    if dark_state[0]:
        btn_dark_theme.set_label("Dark theme on")
    else:
        btn_dark_theme.set_label("Dark theme")

    def on_dark_theme_clicked(widget):
        dark_state[0] = not dark_state[0]
        if dark_state[0]:
            btn_dark_theme.set_label("Dark theme on")
        else:
            btn_dark_theme.set_label("Dark theme")
        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", dark_state[0])
        try:
            secs = settings.read_section()
            if "APPEARANCE" in secs:
                settings.write_settings("APPEARANCE", "dark_theme", str(dark_state[0]))
            else:
                settings.new_settings("APPEARANCE", {"dark_theme": str(dark_state[0])})
        except Exception:
            pass

    btn_dark_theme.connect("clicked", on_dark_theme_clicked)

    hbox6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

    hbox2.append(lbl_distro)
    lbl_distro.set_visible(True)
    hbox6.append(btn_dark_theme)
    hbox3.append(btn_restart_att)
    hbox4.append(btn_quit_att)

    stack_switcher.set_size_request(70, -1)
    stack_switcher.set_hexpand(False)
    stack_switcher.set_vexpand(True)
    ivbox.append(stack_switcher)

    ivbox.append(hbox2)
    ivbox.append(hbox5)
    ivbox.append(hbox3)
    ivbox.append(hbox4)

    stack.set_hexpand(True)
    stack.set_vexpand(True)
    vbox1.append(stack)

    # make the content scrollable
    scrolledWindow = Gtk.ScrolledWindow()
    scrolledWindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    scrolledWindow.set_child(vbox1)

    hbox.append(ivbox)
    scrolledWindow.set_hexpand(True)
    scrolledWindow.set_vexpand(True)
    hbox.append(scrolledWindow)

    stack.set_hhomogeneous(False)
    stack.set_vhomogeneous(False)
