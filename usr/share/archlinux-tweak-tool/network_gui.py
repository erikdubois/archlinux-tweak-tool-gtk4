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

    # ==================================================================
    #                       NETWORK TAB
    # ==================================================================

    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox2_label = Gtk.Label(xalign=0)
    hbox2_label.set_text(
        "Discover other computers in your network"
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
    hbox3_label.set_text("Select hosts: line for name resolution (connect to computers/NAS)")
    hbox3_label.set_margin_start(10)
    hbox3_label.set_margin_end(10)
    hbox3.append(hbox3_label)

    hbox30 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.nsswitch_choices = Gtk.DropDown.new_from_strings([
        "mymachines resolve [!UNAVAIL=return] files myhostname dns",
        "mymachines resolve [!UNAVAIL=return] files dns mdns wins myhostname",
        "mymachines mdns_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] files myhostname dns",
        "mymachines mdns4_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] files myhostname dns",
        "files mymachines myhostname mdns_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] dns wins",
    ])
    self.nsswitch_choices.set_selected(0)
    self.nsswitch_choices.set_margin_start(10)
    self.nsswitch_choices.set_margin_end(10)
    hbox30.append(self.nsswitch_choices)

    hbox_nsswitch_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_apply_nsswitch = Gtk.Button(label="Apply selected nsswitch.conf")
    button_apply_nsswitch.connect("clicked", self.on_click_apply_nsswitch)
    button_reset_nsswitch = Gtk.Button(label="Reset to your default nsswitch.conf")
    button_reset_nsswitch.connect("clicked", self.on_click_reset_nsswitch)
    button_edit_nsswitch = Gtk.Button(label="Edit the /etc/nsswitch.conf manually")
    button_edit_nsswitch.connect("clicked", self.on_click_edit_nsswitch)
    button_apply_nsswitch.set_margin_start(10)
    button_apply_nsswitch.set_margin_end(10)
    hbox_nsswitch_buttons.append(button_apply_nsswitch)
    button_reset_nsswitch.set_margin_start(10)
    button_reset_nsswitch.set_margin_end(10)
    hbox_nsswitch_buttons.append(button_reset_nsswitch)
    button_edit_nsswitch.set_margin_start(10)
    button_edit_nsswitch.set_margin_end(10)
    hbox_nsswitch_buttons.append(button_edit_nsswitch)

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
    #                       SHARED STATUS BAR
    # ======================================================================

    hbox_status = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.network_status_label = Gtk.Label(xalign=0)

    status1 = fn.check_service("smb")
    status1_text = "<b>active</b>" if status1 else "inactive"
    status2 = fn.check_service("nmb")
    status2_text = "<b>active</b>" if status2 else "inactive"
    status3 = fn.check_service("avahi-daemon")
    status3_text = "<b>active</b>" if status3 else "inactive"

    self.network_status_label.set_markup(
        "Samba: " + status1_text + "   Nmb: " + status2_text + "   Avahi: " + status3_text
    )
    self.network_status_label.set_hexpand(True)
    self.network_status_label.set_margin_start(10)
    self.network_status_label.set_margin_end(10)
    hbox_status.append(self.network_status_label)

    restart_smb_main = Gtk.Button(label="Restart Smb")
    restart_smb_main.connect("clicked", self.on_click_restart_smb)
    restart_smb_main.set_margin_start(10)
    restart_smb_main.set_margin_end(10)
    hbox_status.append(restart_smb_main)

    # ======================================================================
    #                   SECTION 1: NETWORK DISCOVERY
    # ======================================================================

    hbox_section1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    section1_label = Gtk.Label(xalign=0)
    section1_label.set_markup("<b>Network Discovery</b>")
    section1_label.set_margin_start(10)
    section1_label.set_margin_end(10)
    hbox_section1.append(section1_label)

    # ======================================================================
    #                   SECTION 2: SAMBA FILE SHARING
    # ======================================================================

    hbox_section2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    section2_label = Gtk.Label(xalign=0)
    section2_label.set_markup("<b>Samba File Sharing</b>")
    section2_label.set_margin_start(10)
    section2_label.set_margin_end(10)
    hbox_section2.append(section2_label)

    sep1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    sep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

    hbox_section_status = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    section_status_label = Gtk.Label(xalign=0)
    section_status_label.set_markup("<b>Status</b>")
    section_status_label.set_margin_start(10)
    section_status_label.set_margin_end(10)
    hbox_section_status.append(section_status_label)

    # ======================================================================
    #                       PACK ALL TO VBOX
    # ======================================================================

    # Status section
    vbox.append(hbox_section_status)
    hbox_status.set_margin_start(10)
    hbox_status.set_margin_end(10)
    vbox.append(hbox_status)
    vbox.append(sep1)

    # Section 1: Network Discovery
    vbox.append(hbox_section1)
    hbox2.set_margin_start(20)
    hbox2.set_margin_end(10)
    vbox.append(hbox2)
    if fn.check_service("firewalld"):
        hbox92.set_margin_start(20)
        hbox92.set_margin_end(10)
        vbox.append(hbox92)
    hbox3.set_margin_start(20)
    hbox3.set_margin_end(10)
    vbox.append(hbox3)
    hbox30.set_margin_start(20)
    hbox30.set_margin_end(10)
    vbox.append(hbox30)
    hbox_nsswitch_buttons.set_margin_start(20)
    hbox_nsswitch_buttons.set_margin_end(10)
    vbox.append(hbox_nsswitch_buttons)
    hbox91.set_margin_start(20)
    hbox91.set_margin_end(10)
    vbox.append(hbox91)

    vbox.append(sep2)

    # Section 2: Samba File Sharing
    vbox.append(hbox_section2)
    hbox_header_samba.set_margin_start(20)
    hbox_header_samba.set_margin_end(10)
    vbox.append(hbox_header_samba)
    hbox4.set_margin_start(20)
    hbox4.set_margin_end(10)
    vbox.append(hbox4)
    hbox4bis.set_margin_start(20)
    hbox4bis.set_margin_end(10)
    vbox.append(hbox4bis)
    hbox5.set_margin_start(20)
    hbox5.set_margin_end(10)
    vbox.append(hbox5)
    hbox16.set_margin_start(20)
    hbox16.set_margin_end(10)
    vbox.append(hbox16)
    hbox18.set_margin_start(20)
    hbox18.set_margin_end(10)
    vbox.append(hbox18)

    vboxstack_network.append(hbox_title)
    vboxstack_network.append(hbox_sep)
    vbox.set_hexpand(True)
    vbox.set_vexpand(True)
    vboxstack_network.append(vbox)
