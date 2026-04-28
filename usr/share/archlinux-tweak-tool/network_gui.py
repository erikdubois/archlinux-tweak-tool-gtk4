# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools
import services


def gui(self, Gtk, vboxstack_network, fn):
    """create a gui"""
    def format_status(service_name):
        """Format service status for display"""
        return "<b>active</b>" if fn.check_service(service_name) else "inactive"

    status_smb = format_status("smb")
    status_nmb = format_status("nmb")
    status_avahi = format_status("avahi-daemon")
    status_text = f"Samba: {status_smb}   Nmb: {status_nmb}   Avahi: {status_avahi}"

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
    button_install_discovery.connect("clicked", functools.partial(services.on_install_discovery_clicked, self))
    button_remove_discovery = Gtk.Button(label="Uninstall network discovery")
    button_remove_discovery.connect("clicked", functools.partial(services.on_remove_discovery_clicked, self))
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
    button_apply_nsswitch.connect("clicked", functools.partial(services.on_click_apply_nsswitch, self))
    button_reset_nsswitch = Gtk.Button(label="Reset to your default nsswitch.conf")
    button_reset_nsswitch.connect("clicked", functools.partial(services.on_click_reset_nsswitch, self))
    button_apply_nsswitch.set_margin_start(10)
    button_apply_nsswitch.set_margin_end(10)
    hbox_nsswitch_buttons.append(button_apply_nsswitch)
    button_reset_nsswitch.set_margin_start(10)
    button_reset_nsswitch.set_margin_end(10)
    hbox_nsswitch_buttons.append(button_reset_nsswitch)

    hbox_edit_nsswitch = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_edit_nsswitch = Gtk.Button(label="Edit the /etc/nsswitch.conf in terminal")
    button_edit_nsswitch.connect("clicked", functools.partial(services.on_click_edit_nsswitch, self))
    button_edit_nsswitch.set_margin_start(10)
    button_edit_nsswitch.set_margin_end(10)
    hbox_edit_nsswitch.append(button_edit_nsswitch)

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
    hbox91_label.set_margin_start(10)
    hbox91_label.set_margin_end(10)
    hbox91_label.set_hexpand(True)
    hbox91.append(hbox91_label)

    hbox93 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox93_label = Gtk.Label(xalign=0)
    hbox93_label.set_markup(status_text)
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
We will create the folder 'Shared' in your home directory \
if it is not already there\n ")

    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4_label = Gtk.Label(xalign=0)
    if fn.check_package_installed("samba"):
        hbox4_label.set_markup("1. Install the samba server - <b>installed</b>")
    else:
        hbox4_label.set_text("1. Install the samba server")
    button_install_samba = Gtk.Button(label="Install Samba")
    button_install_samba.connect("clicked", functools.partial(services.on_click_install_samba, self))
    button_uninstall_samba = Gtk.Button(label="Uninstall Samba")
    button_uninstall_samba.connect("clicked", functools.partial(services.on_click_uninstall_samba, self))
    hbox4_label.set_margin_start(10)
    hbox4_label.set_margin_end(10)
    hbox4_label.set_hexpand(True)
    hbox4.append(hbox4_label)
    button_install_samba.set_margin_start(10)
    button_install_samba.set_margin_end(10)
    hbox4.append(button_install_samba)
    button_uninstall_samba.set_margin_start(10)
    button_uninstall_samba.set_margin_end(10)
    hbox4.append(button_uninstall_samba)

    hbox4bis = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4bis_label = Gtk.Label(xalign=0)
    hbox4bis_label.set_text("2. Apply the /etc/samba/smb.conf of your choice")
    hbox4bis_label.set_margin_start(10)
    hbox4bis_label.set_margin_end(10)
    hbox4bis.append(hbox4bis_label)

    hbox4bis_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_apply_samba = Gtk.Button(label="Apply selected samba.conf")
    button_apply_samba.connect("clicked", functools.partial(services.on_click_apply_samba, self))
    button_reset_samba = Gtk.Button(label="Reset to default samba.conf")
    button_reset_samba.connect("clicked", functools.partial(services.on_click_reset_samba, self))
    button_apply_samba.set_margin_start(10)
    button_apply_samba.set_margin_end(10)
    hbox4bis_buttons.append(button_apply_samba)
    button_reset_samba.set_margin_start(10)
    button_reset_samba.set_margin_end(10)
    hbox4bis_buttons.append(button_reset_samba)

    hbox_edit_samba = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_edit_samba = Gtk.Button(label="Edit samba.conf in terminal")
    button_edit_samba.connect("clicked", functools.partial(services.on_click_edit_samba_nano, self))
    button_edit_samba.set_margin_start(10)
    button_edit_samba.set_margin_end(10)
    hbox_edit_samba.append(button_edit_samba)

    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox5_label = Gtk.Label(xalign=0)
    hbox5_label.set_text(
        "3. Create a password for the current user to be able to access the Samba server"
    )
    hbox5_label.set_margin_start(10)
    hbox5_label.set_margin_end(10)
    hbox5.append(hbox5_label)

    hbox5_button = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_create_samba_user = Gtk.Button(
        label="Create a password for the current user (pop-up)"
    )
    button_create_samba_user.connect("clicked", functools.partial(services.on_click_create_samba_user, self))
    button_create_samba_user.set_margin_start(10)
    button_create_samba_user.set_margin_end(10)
    hbox5_button.append(button_create_samba_user)

    hbox16 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox16_label = Gtk.Label(xalign=0)
    hbox16_label.set_markup(
        "You can now reboot and enjoy the <b>'Shared'</b> folder if you choose '<b>easy</b>' "
    )
    hbox16_label.set_margin_start(10)
    hbox16_label.set_margin_end(10)
    hbox16.append(hbox16_label)

    hbox94 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox94_label = Gtk.Label(xalign=0)
    hbox94_label.set_markup(status_text)
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
    hbox95_label.set_margin_start(10)
    hbox95_label.set_margin_end(10)
    hbox95_label.set_hexpand(True)
    hbox95.append(hbox95_label)

    hbox19 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    install_arco_thunar_plugin = Gtk.Button(label="Install Thunar share plugin")
    install_arco_thunar_plugin.connect(
        "clicked", functools.partial(services.on_click_install_arco_thunar_plugin, self)
    )
    install_arco_thunar_plugin.set_margin_start(10)
    install_arco_thunar_plugin.set_margin_end(10)
    hbox19.append(install_arco_thunar_plugin)

    # ======================================================================
    #                       SHARED STATUS BAR
    # ======================================================================

    hbox_status = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.network_status_label = Gtk.Label(xalign=0)
    self.network_status_label.set_markup(status_text)
    self.network_status_label.set_hexpand(True)
    self.network_status_label.set_margin_start(10)
    self.network_status_label.set_margin_end(10)
    hbox_status.append(self.network_status_label)

    restart_smb_button3 = Gtk.Button(label="Restart Smb")
    restart_smb_button3.connect("clicked", functools.partial(services.on_click_restart_smb, self))
    restart_smb_button3.set_margin_start(10)
    restart_smb_button3.set_margin_end(10)
    hbox_status.append(restart_smb_button3)

    hbox_discovery_status = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    discovery_status_label = Gtk.Label(xalign=0)
    if status_avahi.startswith("<b>"):
        discovery_status_label.set_markup("<b>✓ Network discovery installed</b>")
    else:
        discovery_status_label.set_markup("✗ Network discovery not installed")
    discovery_status_label.set_margin_start(10)
    discovery_status_label.set_margin_end(10)
    hbox_discovery_status.append(discovery_status_label)

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
    hbox_discovery_status.set_margin_start(10)
    hbox_discovery_status.set_margin_end(10)
    vbox.append(hbox_discovery_status)
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
    hbox_edit_nsswitch.set_margin_start(20)
    hbox_edit_nsswitch.set_margin_end(10)
    vbox.append(hbox_edit_nsswitch)
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
    hbox4bis_buttons.set_margin_start(20)
    hbox4bis_buttons.set_margin_end(10)
    vbox.append(hbox4bis_buttons)
    hbox_edit_samba.set_margin_start(20)
    hbox_edit_samba.set_margin_end(10)
    vbox.append(hbox_edit_samba)
    hbox5.set_margin_start(20)
    hbox5.set_margin_end(10)
    vbox.append(hbox5)
    hbox5_button.set_margin_start(20)
    hbox5_button.set_margin_end(10)
    vbox.append(hbox5_button)
    hbox16.set_margin_start(20)
    hbox16.set_margin_end(10)
    vbox.append(hbox16)

    vboxstack_network.append(hbox_title)
    vboxstack_network.append(hbox_sep)
    vbox.set_hexpand(True)
    vbox.set_vexpand(True)
    vboxstack_network.append(vbox)
