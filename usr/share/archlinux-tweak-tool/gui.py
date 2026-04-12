# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

# ============Functions============
import functions as fn

import desktopr
import fixes
import lightdm
import login
import lxdm
import fastfetch
import sddm
#import design
import att
#import terminals

# import template
import themer
import user
import zsh_theme
import packages

# =============GUI=================
import att_gui
import autostart_gui
import desktopr_gui
import fixes_gui
#import grub_gui
#import login_gui
#import arcolinuxmirrors_gui
import fastfetch_gui
import pacman_gui
import privacy_gui
#import terminals_gui
#import utilities_gui
import services_gui
import shell_gui
import themer_gui
#import design_gui
import user_gui
import packages_gui

# import Template_GUI
# import Polybar_GUI


def gui(self, Gtk, Gdk, GdkPixbuf, base_dir, os, Pango):
    """creation of the gui"""

    # =======================================================
    #                       App Notifications
    # =======================================================

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    self.notification_revealer = Gtk.Revealer()
    self.notification_revealer.set_reveal_child(False)

    self.notification_label = Gtk.Label()

    pb_panel = GdkPixbuf.Pixbuf.new_from_file(base_dir + "/images/panel.png")
    texture_panel = Gdk.Texture.new_for_pixbuf(pb_panel)
    panel = Gtk.Picture.new_for_paintable(texture_panel)
    panel.set_content_fit(Gtk.ContentFit.CONTAIN)

    overlayframe = Gtk.Overlay()
    overlayframe.set_child(panel)
    overlayframe.add_overlay(self.notification_label)

    self.notification_revealer.set_child(overlayframe)

    self.notification_revealer.set_hexpand(True)
    hbox0.append(self.notification_revealer)

    # ==========================================================
    #                       CONTAINER
    # ==========================================================

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

    hbox.set_hexpand(True)
    hbox.set_vexpand(True)
    vbox.append(hbox)
    self.set_child(vbox)

    # ==========================================================
    #                    INITIALIZE STACK
    # ==========================================================
    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
    stack.set_transition_duration(350)

    vboxstack1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # vboxstack2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # vboxstack5 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # vboxstack6 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack7 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack8 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # vboxstack9 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack10 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # vboxstack11 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack12 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack13 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack14 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # vboxstack15 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack16 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # vboxstack17 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack18 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack19 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack20 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    # vboxstack21 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack22 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack23 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack24 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack25 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack26 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    # ==========================================================
    #                 ARCOLINUX MIRRORLIST
    # ==========================================================

#     if fn.file_check("/etc/pacman.d/arcolinux-mirrorlist"):
#         arcolinuxmirrors_gui.gui(self, Gtk, vboxstack16)
#     else:
#         hbox31 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
#         lbl1 = Gtk.Label(xalign=0)
#         lbl1.set_text("ArcoLinux Mirrorlist")
#         lbl1.set_name("title")
#         hbox31.append(lbl1)
#
#         hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
#         hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
#         hseparator.set_hexpand(True)
#         hseparator.set_vexpand(True)
#         hbox41.append(hseparator)
#
#         lbl2 = Gtk.Label()
#         lbl2.set_markup(
#             "First install the ArcoLinux Mirrors and ArcoLinux keys\n\
# Then you will be able to set the mirrors of ArcoLinux"
#         )
#
#         vboxstack16.append(hbox31)
#         vboxstack16.append(hbox41)
#         lbl2.set_hexpand(True)
#         vboxstack16.append(lbl2)

    # ==========================================================
    #                 ATT
    # ==========================================================

    att_gui.gui(self, Gtk, vboxstack25, att, fn)

    # ==========================================================
    #                AUTOSTART
    # ==========================================================

    autostart_gui.gui(self, Gtk, vboxstack13, fn)

    # ==========================================================
    #                DESKTOP
    # ==========================================================

    desktopr_gui.gui(self, Gtk, GdkPixbuf, vboxstack12, desktopr, fn, base_dir, Pango)

    # ==========================================================
    #                 DESIGN
    # ==========================================================

    #design_gui.gui(self, Gtk, vboxstack24, design, fn)

    # # ==========================================================
    # #               FASTFETCH
    # # ==========================================================

    if fn.file_check(fn.fastfetch_config):
        fastfetch_gui.gui(self, Gtk, vboxstack8, fastfetch, fn)
    else:
        hbox31 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox41 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl1 = Gtk.Label(xalign=0)
        lbl1.set_text("fastfetch Editor")
        lbl1.set_name("title")
        hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator.set_hexpand(True)
        hseparator.set_vexpand(True)
        hbox41.append(hseparator)
        hbox31.append(lbl1)
        vboxstack8.append(hbox31)
        vboxstack8.append(hbox41)
        fastfetch_message = Gtk.Label()
        fastfetch_message.set_markup(
            "If you install <b>fastfetch</b> and the <i>ArcoLinux \
themes</i> you can customize <b>fastfetch</b>"
        )
        fastfetch_message.set_hexpand(True)
        vboxstack8.append(fastfetch_message)

    # # ==========================================================
    # #               FIXES
    # # ==========================================================

    fixes_gui.gui(self, Gtk, vboxstack19, fn, fixes)

    # ==========================================================
    #                 GRUB
    # ==========================================================

    #grub_gui.gui(self, Gtk, vboxstack4, fn)

    # ==========================================================
    #                         LOGIN
    # ==========================================================

    #login_gui.gui(self, Gtk, vboxstack22, sddm, lightdm, lxdm, fn, login)

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
    #                        TEMPLATE
    # ==========================================================

    # Template_GUI.gui(self, Gtk, vboxstack21, fn)

    # # ==========================================================
    # #                 TERMINALS
    # # ==========================================================

    #terminals_gui.gui(self, Gtk, vboxstack7, terminals)

    # # ==========================================================
    # #               TERMINAL FUN
    # # ==========================================================

    #utilities_gui.gui(self, Gtk, vboxstack20, fn)

    # ==========================================================
    #                 THEMES
    # ==========================================================

    themer_gui.gui(self, Gtk, GdkPixbuf, vboxstack10, themer, fn, base_dir)

    # # ==========================================================
    # #                USER
    # # ==========================================================

    user_gui.gui(self, Gtk, vboxstack18, user, fn)

    # =====================================================
    #                       PACKAGES - EXPORT/INSTALL
    # =====================================================

    packages_gui.gui(self, Gtk, vboxstack26, fn)
    # ==========================================================
    #                   ADD TO WINDOW
    # ==========================================================
    stack.add_titled(vboxstack25, "stack25", "Att")  # Design

    stack.add_titled(vboxstack13, "stack13", "Autostart")  # Autostart

    #stack.add_titled(vboxstack24, "stack24", "Design")  # Design

    stack.add_titled(vboxstack12, "stack12", "Desktop")  # Desktop installer

    stack.add_titled(vboxstack8, "stack4", "Fastfetch")  # fastfetch config

    stack.add_titled(vboxstack19, "stack19", "Fixes")  # Fixes

    #stack.add_titled(vboxstack4, "stack1", "Grub")  # Grub config

    #if fn.distr != "artix":
    #    stack.add_titled(vboxstack22, "stack22", "Login")  # Sddm/Lightdm/Lxdm

    #stack.add_titled(vboxstack16, "stack16", "Mirrors")  # mirrors

    stack.add_titled(vboxstack26, "packages", "Packages")  # Packages

    stack.add_titled(vboxstack1, "stack6", "Pacman")  # Pacman config

    stack.add_titled(vboxstack3, "stack2", "Privacy")  # Privacy

    if fn.distr != "artix":
        stack.add_titled(vboxstack14, "stack14", "Services")  # services

    stack.add_titled(vboxstack23, "stack23", "Shells")  # shell

    # stack.add_titled(vboxstack21, "stack21", "Template")  # template

    #stack.add_titled(vboxstack7, "stack8", "Terminals")  # Terminals

    #stack.add_titled(vboxstack20, "stack20", "Terminal Fun")  # lolcat and others

    stack.add_titled(vboxstack10, "stack11", "Themer")  # Themer

    stack.add_titled(vboxstack18, "stack18", "User")  # user

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
        print("Thanks for using ArchLinux Tweak Tool")
        print("Report issues to make it even better")
        print(
            "---------------------------------------------------------------------------"
        )

    lbl_distro = Gtk.Label(xalign=0)
    lbl_distro.set_markup("Working on\n" + fn.change_distro_label(fn.distr))
    btn_reload_att = Gtk.Button(label="Reload ATT")
    btn_reload_att.set_size_request(100, 30)
    btn_reload_att.connect("clicked", self.on_reload_att_clicked)
    btn_restart_att = Gtk.Button(label="Restart ATT")
    btn_restart_att.set_size_request(100, 30)
    btn_restart_att.connect("clicked", self.on_refresh_att_clicked)
    btn_quit_att = Gtk.Button(label="Quit ATT")
    btn_quit_att.set_size_request(100, 30)
    btn_quit_att.connect("clicked", on_quit)

    # =====================================================
    #               SUPPORT LINK
    # =====================================================

    pbp = GdkPixbuf.Pixbuf.new_from_file_at_size(
        fn.path.join(base_dir, "images/support.png"), 58, 58
    )
    texture_support = Gdk.Texture.new_for_pixbuf(pbp)
    pimage = Gtk.Picture.new_for_paintable(texture_support)
    pimage.set_content_fit(Gtk.ContentFit.CONTAIN)
    pimage.set_cursor(Gdk.Cursor.new_from_name("pointer"))
    pimage.set_tooltip_text("Support or get support")

    support_gesture = Gtk.GestureClick.new()
    support_gesture.connect("pressed", lambda g, n, x, y: self.on_social_clicked(g, None))
    pimage.add_controller(support_gesture)

    # =====================================================
    #                      PACKS
    # =====================================================

    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

    hbox1.append(pimage)
    hbox2.append(lbl_distro)
    hbox5.append(btn_reload_att)
    hbox3.append(btn_restart_att)
    hbox4.append(btn_quit_att)

    stack_switcher.set_size_request(120, -1)
    stack_switcher.set_hexpand(False)
    stack_switcher.set_vexpand(True)
    ivbox.append(stack_switcher)

    ivbox.append(hbox1)
    ivbox.append(hbox2)
    ivbox.append(hbox5)
    ivbox.append(hbox3)
    ivbox.append(hbox4)

    vbox1.append(hbox0)
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
