# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================


def gui(self, Gtk, vboxstack_network, fn):
    """create a gui"""
    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_title_label = Gtk.Label(xalign=0)
    hbox_title_label.set_text("Network")
    hbox_title_label.set_name("title")
    hbox_title_label.set_margin_start(10)
    hbox_title_label.set_margin_end(10)
    hbox_title.append(hbox_title_label)

    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox_sep.append(hseparator)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

    vboxstack1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
    stack.set_transition_duration(350)
    stack.set_hhomogeneous(False)
    stack.set_vhomogeneous(False)

    stack_switcher = Gtk.StackSwitcher()
    stack_switcher.set_orientation(Gtk.Orientation.HORIZONTAL)
    stack_switcher.set_stack(stack)

    # ==================================================================
    #                       NETWORK TAB
    # ==================================================================

    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox2_label = Gtk.Label(xalign=0)
    hbox2_label.set_text(
        "Discover other computers in your network (to access other computers)"
    )
    button_install_discovery = Gtk.Button(label="Install network discovery")
    button_install_discovery.connect("clicked", self.on_install_discovery_clicked)
    button_remove_discovery = Gtk.Button(label="Uninstall network discovery")
    button_remove_discovery.connect("clicked", self.on_remove_discovery_clicked)
    hbox2_label.set_margin_start(10)
    hbox2_label.set_margin_end(10)
    hbox2_label.set_hexpand(True)
    hbox2.append(hbox2_label)
    button_install_discovery.set_margin_start(10)
    button_install_discovery.set_margin_end(10)
    hbox2.append(button_install_discovery)
    button_remove_discovery.set_margin_start(10)
    button_remove_discovery.set_margin_end(10)
    hbox2.append(button_remove_discovery)

    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox3_label = Gtk.Label(xalign=0)
    hbox3_label.set_text("Change the /etc/nsswitch.conf to connect to computers/NAS")
    hbox3_label.set_margin_start(10)
    hbox3_label.set_margin_end(10)
    hbox3.append(hbox3_label)

    hbox30 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.nsswitch_choices = Gtk.DropDown.new_from_strings([
        "ArcoLinux",
        "ArchLinux",
        "BigLinux",
        "EndeavourOS",
        "Garuda",
        "Manjaro",
    ])
    self.nsswitch_choices.set_selected(0)
    button_apply_nsswitch = Gtk.Button(label="Apply selected nsswitch.conf")
    button_apply_nsswitch.connect("clicked", self.on_click_apply_nsswitch)
    button_reset_nsswitch = Gtk.Button(label="Reset to default nsswitch")
    button_reset_nsswitch.connect("clicked", self.on_click_reset_nsswitch)
    self.nsswitch_choices.set_margin_start(10)
    self.nsswitch_choices.set_margin_end(10)
    hbox30.append(self.nsswitch_choices)
    button_apply_nsswitch.set_margin_start(10)
    button_apply_nsswitch.set_margin_end(10)
    hbox30.append(button_apply_nsswitch)
    button_reset_nsswitch.set_margin_start(10)
    button_reset_nsswitch.set_margin_end(10)
    hbox30.append(button_reset_nsswitch)

    hbox92 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox92_label = Gtk.Label(xalign=0)
    hbox92_label.set_markup(
        '<span foreground="red" size="large">We found a firewall on your system</span>'
    )
    hbox92_label.set_margin_start(10)
    hbox92_label.set_margin_end(10)
    hbox92.append(hbox92_label)

    hbox91 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox91_label = Gtk.Label(xalign=0)
    hbox91_label.set_text(
        "With the Avahi daemon (network discovery) running on both the server \
and client,\nthe file manager on the client should automatically find the server - \
Beware of firewalls"
    )
    restart_smb = Gtk.Button(label="Restart Smb")
    restart_smb.connect("clicked", self.on_click_restart_smb)
    hbox91_label.set_margin_start(10)
    hbox91_label.set_margin_end(10)
    hbox91_label.set_hexpand(True)
    hbox91.append(hbox91_label)
    restart_smb.set_margin_start(10)
    restart_smb.set_margin_end(10)
    hbox91.append(restart_smb)

    hbox93 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox93_label = Gtk.Label(xalign=0)

    status1 = fn.check_service("smb")
    if status1 is True:
        status1 = "<b>active</b>"
    else:
        status1 = "inactive"

    status2 = fn.check_service("nmb")
    if status2 is True:
        status2 = "<b>active</b>"
    else:
        status2 = "inactive"

    status3 = fn.check_service("avahi-daemon")
    if status3 is True:
        status3 = "<b>active</b>"
    else:
        status3 = "inactive"

    hbox93_label.set_markup(
        "Samba : " + status1 + "   Nmb : " + status2 + "   Avahi : " + status3
    )
    hbox93_label.set_margin_start(10)
    hbox93_label.set_margin_end(10)
    hbox93.append(hbox93_label)

    # ==================================================================
    #                       SAMBA TAB
    # ==================================================================

    hbox_header_samba = Gtk.Label(xalign=0)
    hbox_header_samba.set_markup(
        "You install a samba server if you need to \
share a folder and its contents in your home network\n\
The purpose is to create <b>one</b> shared folder - the current user can later \
access this folder from other computers\n\
The easy configuration will create the folder 'Shared' in your home directory \
if it is not already there\n\
The usershares configuration will not create a 'Shared' folder - you share any folder you like\n\
Follow the instruction numbers below - <b>we recommend the easy configuration</b>"
    )

    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("samba"):
        hbox4_label.set_markup("1. Install the samba server - <b>installed</b>")
    else:
        hbox4_label.set_text("1. Install the samba server")
    button_uninstall_samba = Gtk.Button(label="Uninstall Samba")
    button_uninstall_samba.connect("clicked", self.on_click_uninstall_samba)
    button_install_samba = Gtk.Button(label="Install Samba")
    button_install_samba.connect("clicked", self.on_click_install_samba)
    hbox4_label.set_margin_start(10)
    hbox4_label.set_margin_end(10)
    hbox4_label.set_hexpand(True)
    hbox4.append(hbox4_label)
    button_uninstall_samba.set_margin_start(10)
    button_uninstall_samba.set_margin_end(10)
    hbox4.append(button_uninstall_samba)
    button_install_samba.set_margin_start(10)
    button_install_samba.set_margin_end(10)
    hbox4.append(button_install_samba)

    hbox4bis = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4bis_label = Gtk.Label(xalign=0)
    hbox4bis_label.set_text("2. Apply the /etc/samba/smb.conf of your choice")
    self.samba_choices = Gtk.DropDown.new_from_strings([
        "Easy",
        "Usershares",
        "Windows",
        "ArcoLinux",
        "Original",
        "BigLinux",
    ])
    self.samba_choices.set_selected(0)
    button_apply_samba = Gtk.Button(label="Apply selected samba.conf")
    button_apply_samba.connect("clicked", self.on_click_apply_samba)
    button_reset_samba = Gtk.Button(label="Reset to default samba.conf")
    button_reset_samba.connect("clicked", self.on_click_reset_samba)
    hbox4bis_label.set_margin_start(10)
    hbox4bis_label.set_margin_end(10)
    hbox4bis_label.set_hexpand(True)
    hbox4bis.append(hbox4bis_label)
    self.samba_choices.set_hexpand(True)
    self.samba_choices.set_vexpand(False)
    self.samba_choices.set_margin_start(10)
    self.samba_choices.set_margin_end(10)
    hbox4bis.append(self.samba_choices)
    button_apply_samba.set_hexpand(True)
    button_apply_samba.set_vexpand(False)
    button_apply_samba.set_margin_start(10)
    button_apply_samba.set_margin_end(10)
    hbox4bis.append(button_apply_samba)
    button_reset_samba.set_margin_start(10)
    button_reset_samba.set_margin_end(10)
    hbox4bis.append(button_reset_samba)

    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox5_label = Gtk.Label(xalign=0)
    hbox5_label.set_text(
        "3. Create a password for the current user to be able to access the Samba server"
    )
    button_create_samba_user = Gtk.Button(
        label="Create a password for the current user (pop-up)"
    )
    button_create_samba_user.connect("clicked", self.on_click_create_samba_user)
    hbox5_label.set_margin_start(10)
    hbox5_label.set_margin_end(10)
    hbox5.append(hbox5_label)
    button_create_samba_user.set_margin_start(10)
    button_create_samba_user.set_margin_end(10)
    hbox5.append(button_create_samba_user)

    hbox16 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox16_label = Gtk.Label(xalign=0)
    hbox16_label.set_markup(
        "You can now reboot and enjoy the <b>'Shared'</b> folder if you choose '<b>easy</b>' "
    )
    hbox16_label.set_margin_start(10)
    hbox16_label.set_margin_end(10)
    hbox16.append(hbox16_label)

    hbox18 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox18_label = Gtk.Label(xalign=0)
    hbox18_label.set_markup(
        "If you choose '<b>usershares</b>' then we recommend you install \
also thunar and its plugin and \
right-click to share any folder in your home directory\nThere are other filemanagers with \
their plugins at the bottom"
    )
    hbox18_label.set_margin_start(10)
    hbox18_label.set_margin_end(10)
    hbox18.append(hbox18_label)

    hbox94 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox94_label = Gtk.Label(xalign=0)
    hbox94_label.set_markup(
        "Samba : " + status1 + "   Nmb : " + status2 + "   Avahi : " + status3
    )
    hbox94_label.set_margin_start(10)
    hbox94_label.set_margin_end(10)
    hbox94.append(hbox94_label)

    hbox95 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox95_label = Gtk.Label(xalign=0)
    hbox95_label.set_text(
        "With the Avahi daemon (network discovery) running on both \
the server and client,\n\
the file manager on the client should automatically find the server- Beware of firewalls\n\
All computers in your network must have a unique name /etc/hostname"
    )
    restart_smb2 = Gtk.Button(label="Restart Smb")
    restart_smb2.connect("clicked", self.on_click_restart_smb)
    hbox95_label.set_margin_start(10)
    hbox95_label.set_margin_end(10)
    hbox95_label.set_hexpand(True)
    hbox95.append(hbox95_label)
    restart_smb2.set_margin_start(10)
    restart_smb2.set_margin_end(10)
    hbox95.append(restart_smb2)

    hbox19 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    install_arco_thunar_plugin = Gtk.Button(label="Install Thunar share plugin")
    install_arco_thunar_plugin.connect(
        "clicked", self.on_click_install_arco_thunar_plugin
    )
    install_arco_nemo_plugin = Gtk.Button(label="Install Nemo share plugin")
    install_arco_nemo_plugin.connect("clicked", self.on_click_install_arco_nemo_plugin)
    install_arco_caja_plugin = Gtk.Button(label="Install Caja share plugin")
    install_arco_caja_plugin.connect("clicked", self.on_click_install_arco_caja_plugin)
    install_arco_thunar_plugin.set_margin_start(10)
    install_arco_thunar_plugin.set_margin_end(10)
    hbox19.append(install_arco_thunar_plugin)
    install_arco_nemo_plugin.set_margin_start(10)
    install_arco_nemo_plugin.set_margin_end(10)
    hbox19.append(install_arco_nemo_plugin)
    install_arco_caja_plugin.set_margin_start(10)
    install_arco_caja_plugin.set_margin_end(10)
    hbox19.append(install_arco_caja_plugin)

    # ======================================================================
    #                       PACK TO VBOXSTACKS
    # ======================================================================

    # network tab
    vboxstack1.append(hbox2)
    vboxstack1.append(hbox3)
    vboxstack1.append(hbox30)
    if fn.check_service("firewalld"):
        hbox92.set_margin_start(10)
        hbox92.set_margin_end(10)
        vboxstack1.append(hbox92)
    hbox91.set_margin_start(10)
    hbox91.set_margin_end(10)
    vboxstack1.append(hbox91)
    hbox93.set_margin_start(10)
    hbox93.set_margin_end(10)
    vboxstack1.append(hbox93)

    # samba tab
    hbox_header_samba.set_margin_start(10)
    hbox_header_samba.set_margin_end(10)
    vboxstack2.append(hbox_header_samba)
    vboxstack2.append(hbox4)
    vboxstack2.append(hbox4bis)
    vboxstack2.append(hbox5)
    hbox16.set_margin_start(10)
    hbox16.set_margin_end(10)
    vboxstack2.append(hbox16)
    hbox18.set_margin_start(10)
    hbox18.set_margin_end(10)
    vboxstack2.append(hbox18)
    hbox94.set_margin_start(10)
    hbox94.set_margin_end(10)
    vboxstack2.append(hbox94)
    hbox95.set_margin_start(10)
    hbox95.set_margin_end(10)
    vboxstack2.append(hbox95)
    hbox19.set_margin_start(10)
    hbox19.set_margin_end(10)
    vboxstack2.append(hbox19)

    stack.add_titled(vboxstack1, "stack_net1", "Network")
    stack.add_titled(vboxstack2, "stack_net2", "Samba")

    vbox.append(stack_switcher)
    stack.set_hexpand(True)
    stack.set_vexpand(True)
    vbox.append(stack)

    vboxstack_network.append(hbox_title)
    vboxstack_network.append(hbox_sep)
    vbox.set_hexpand(True)
    vbox.set_vexpand(True)
    vboxstack_network.append(vbox)
