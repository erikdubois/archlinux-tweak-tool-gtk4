# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functools
import services


def gui(self, Gtk, vboxstack_network, fn):
    def format_status(service_name):
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

    hbox_discovery = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_discovery = Gtk.Label(xalign=0)
    label_discovery.set_text("Discover other computers in your network")
    button_install_discovery = Gtk.Button(label="Install network discovery")
    button_install_discovery.connect("clicked", functools.partial(services.on_install_discovery_clicked, self))
    button_remove_discovery = Gtk.Button(label="Uninstall network discovery")
    button_remove_discovery.connect("clicked", functools.partial(services.on_remove_discovery_clicked, self))
    label_discovery.set_margin_start(10)
    label_discovery.set_margin_end(10)
    label_discovery.set_hexpand(True)
    hbox_discovery.append(label_discovery)
    button_install_discovery.set_margin_start(10)
    button_install_discovery.set_margin_end(10)
    hbox_discovery.append(button_install_discovery)
    button_remove_discovery.set_margin_start(10)
    button_remove_discovery.set_margin_end(10)
    hbox_discovery.append(button_remove_discovery)

    hbox_nsswitch_desc = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_nsswitch_desc = Gtk.Label(xalign=0)
    label_nsswitch_desc.set_text("Select hosts: line for name resolution (connect to computers/NAS)")
    label_nsswitch_desc.set_margin_start(10)
    label_nsswitch_desc.set_margin_end(10)
    hbox_nsswitch_desc.append(label_nsswitch_desc)

    hbox_nsswitch_dropdown = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.nsswitch_choices = Gtk.DropDown.new_from_strings([
        "Standard (no mdns)",
        "With mdns + wins",
        "With mdns_minimal",
        "With mdns4_minimal",
        "Custom order (no systemd)",
    ])
    self.nsswitch_choices.set_selected(0)
    self.nsswitch_choices.set_margin_start(10)
    self.nsswitch_choices.set_margin_end(10)
    hbox_nsswitch_dropdown.append(self.nsswitch_choices)

    hbox_nsswitch_preview = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_nsswitch_preview = Gtk.Label(xalign=0)
    label_nsswitch_preview.set_margin_start(10)
    label_nsswitch_preview.set_margin_end(10)

    def _update_nsswitch_preview(*args):
        key = fn.get_combo_text(self.nsswitch_choices)
        hosts_line = services.NSSWITCH_OPTIONS.get(key, "")
        label_nsswitch_preview.set_markup(f"<tt>hosts: {hosts_line}</tt>")
        if args:
            fn.log_info(f"  Selected : {key}")
            fn.log_info(f"  hosts:   : {hosts_line}")

    _update_nsswitch_preview()
    self.nsswitch_choices.connect("notify::selected", _update_nsswitch_preview)
    hbox_nsswitch_preview.append(label_nsswitch_preview)

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

    hbox_firewall_warning = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_firewall_warning = Gtk.Label(xalign=0)
    label_firewall_warning.set_markup(
        '<span foreground="red" size="large">We found a firewall on your system</span>'
    )
    label_firewall_warning.set_margin_start(10)
    label_firewall_warning.set_margin_end(10)
    hbox_firewall_warning.append(label_firewall_warning)

    hbox_discovery_info = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_discovery_info = Gtk.Label(xalign=0)
    label_discovery_info.set_text(
        "With the Avahi daemon (network discovery) running on both the server \
and client,\nthe file manager on the client should automatically find the server - \
Beware of firewalls"
    )
    label_discovery_info.set_margin_start(10)
    label_discovery_info.set_margin_end(10)
    label_discovery_info.set_hexpand(True)
    hbox_discovery_info.append(label_discovery_info)

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

    hbox_samba_install = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_samba_install = Gtk.Label(xalign=0)
    if fn.check_package_installed("samba"):
        label_samba_install.set_markup("1. Install the samba server - <b>installed</b>")
    else:
        label_samba_install.set_text("1. Install the samba server")
    button_install_samba = Gtk.Button(label="Install Samba")
    button_install_samba.connect("clicked", functools.partial(services.on_click_install_samba, self))
    button_uninstall_samba = Gtk.Button(label="Uninstall Samba")
    button_uninstall_samba.connect("clicked", functools.partial(services.on_click_uninstall_samba, self))
    label_samba_install.set_margin_start(10)
    label_samba_install.set_margin_end(10)
    label_samba_install.set_hexpand(True)
    hbox_samba_install.append(label_samba_install)
    button_install_samba.set_margin_start(10)
    button_install_samba.set_margin_end(10)
    hbox_samba_install.append(button_install_samba)
    button_uninstall_samba.set_margin_start(10)
    button_uninstall_samba.set_margin_end(10)
    hbox_samba_install.append(button_uninstall_samba)

    hbox_samba_conf_desc = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_samba_conf_desc = Gtk.Label(xalign=0)
    label_samba_conf_desc.set_text("2. Apply the configuration")
    label_samba_conf_desc.set_margin_start(10)
    label_samba_conf_desc.set_margin_end(10)
    hbox_samba_conf_desc.append(label_samba_conf_desc)

    hbox_samba_conf_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_apply_samba = Gtk.Button(label="Apply default samba.conf")
    button_apply_samba.connect("clicked", functools.partial(services.on_click_apply_samba, self))
    button_reset_samba = Gtk.Button(label="Reset to your default samba.conf")
    button_reset_samba.connect("clicked", functools.partial(services.on_click_reset_samba, self))
    button_apply_samba.set_margin_start(10)
    button_apply_samba.set_margin_end(10)
    hbox_samba_conf_buttons.append(button_apply_samba)
    button_reset_samba.set_margin_start(10)
    button_reset_samba.set_margin_end(10)
    hbox_samba_conf_buttons.append(button_reset_samba)

    hbox_edit_samba = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_edit_samba = Gtk.Button(label="Edit samba.conf in terminal")
    button_edit_samba.connect("clicked", functools.partial(services.on_click_edit_samba_nano, self))
    button_edit_samba.set_margin_start(10)
    button_edit_samba.set_margin_end(10)
    hbox_edit_samba.append(button_edit_samba)

    hbox_samba_password_desc = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_samba_password_desc = Gtk.Label(xalign=0)
    label_samba_password_desc.set_text(
        "3. Create a password for the current user to be able to access the Samba server"
    )
    label_samba_password_desc.set_margin_start(10)
    label_samba_password_desc.set_margin_end(10)
    hbox_samba_password_desc.append(label_samba_password_desc)

    hbox_samba_password_button = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    button_create_samba_user = Gtk.Button(
        label="Create a password for the current user (pop-up)"
    )
    button_create_samba_user.connect("clicked", functools.partial(services.on_click_create_samba_user, self))
    button_create_samba_user.set_margin_start(10)
    button_create_samba_user.set_margin_end(10)
    hbox_samba_password_button.append(button_create_samba_user)

    hbox_samba_reboot_note = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_samba_reboot_note = Gtk.Label(xalign=0)
    label_samba_reboot_note.set_markup(
        "You can now reboot and enjoy the <b>'Shared'</b> folder"
    )
    label_samba_reboot_note.set_margin_start(10)
    label_samba_reboot_note.set_margin_end(10)
    hbox_samba_reboot_note.append(label_samba_reboot_note)

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

    button_restart_smb = Gtk.Button(label="Restart Smb")
    button_restart_smb.connect("clicked", functools.partial(services.on_click_restart_smb, self))
    button_restart_smb.set_margin_start(10)
    button_restart_smb.set_margin_end(10)
    hbox_status.append(button_restart_smb)

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

    hbox_section_discovery = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_section_discovery = Gtk.Label(xalign=0)
    label_section_discovery.set_markup("<b>Network Discovery</b>")
    label_section_discovery.set_margin_start(10)
    label_section_discovery.set_margin_end(10)
    hbox_section_discovery.append(label_section_discovery)

    # ======================================================================
    #                   SECTION 2: SAMBA FILE SHARING
    # ======================================================================

    hbox_section_samba = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_section_samba = Gtk.Label(xalign=0)
    label_section_samba.set_markup("<b>Samba File Sharing</b>")
    label_section_samba.set_margin_start(10)
    label_section_samba.set_margin_end(10)
    hbox_section_samba.append(label_section_samba)

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
    vbox.append(hbox_section_discovery)
    hbox_discovery.set_margin_start(20)
    hbox_discovery.set_margin_end(10)
    vbox.append(hbox_discovery)
    if fn.check_service("firewalld"):
        hbox_firewall_warning.set_margin_start(20)
        hbox_firewall_warning.set_margin_end(10)
        vbox.append(hbox_firewall_warning)
    hbox_nsswitch_desc.set_margin_start(20)
    hbox_nsswitch_desc.set_margin_end(10)
    vbox.append(hbox_nsswitch_desc)
    hbox_nsswitch_dropdown.set_margin_start(20)
    hbox_nsswitch_dropdown.set_margin_end(10)
    vbox.append(hbox_nsswitch_dropdown)
    hbox_nsswitch_preview.set_margin_start(20)
    hbox_nsswitch_preview.set_margin_end(10)
    vbox.append(hbox_nsswitch_preview)
    hbox_nsswitch_buttons.set_margin_start(20)
    hbox_nsswitch_buttons.set_margin_end(10)
    vbox.append(hbox_nsswitch_buttons)
    hbox_edit_nsswitch.set_margin_start(20)
    hbox_edit_nsswitch.set_margin_end(10)
    vbox.append(hbox_edit_nsswitch)
    hbox_discovery_info.set_margin_start(20)
    hbox_discovery_info.set_margin_end(10)
    vbox.append(hbox_discovery_info)

    vbox.append(sep2)

    # Section 2: Samba File Sharing
    vbox.append(hbox_section_samba)
    hbox_header_samba.set_margin_start(20)
    hbox_header_samba.set_margin_end(10)
    vbox.append(hbox_header_samba)
    hbox_samba_install.set_margin_start(20)
    hbox_samba_install.set_margin_end(10)
    vbox.append(hbox_samba_install)
    hbox_samba_conf_desc.set_margin_start(20)
    hbox_samba_conf_desc.set_margin_end(10)
    vbox.append(hbox_samba_conf_desc)
    hbox_samba_conf_buttons.set_margin_start(20)
    hbox_samba_conf_buttons.set_margin_end(10)
    vbox.append(hbox_samba_conf_buttons)
    hbox_edit_samba.set_margin_start(20)
    hbox_edit_samba.set_margin_end(10)
    vbox.append(hbox_edit_samba)
    hbox_samba_password_desc.set_margin_start(20)
    hbox_samba_password_desc.set_margin_end(10)
    vbox.append(hbox_samba_password_desc)
    hbox_samba_password_button.set_margin_start(20)
    hbox_samba_password_button.set_margin_end(10)
    vbox.append(hbox_samba_password_button)
    hbox_samba_reboot_note.set_margin_start(20)
    hbox_samba_reboot_note.set_margin_end(10)
    vbox.append(hbox_samba_reboot_note)

    vboxstack_network.append(hbox_title)
    vboxstack_network.append(hbox_sep)
    vbox.set_hexpand(True)
    vbox.set_vexpand(True)
    vboxstack_network.append(vbox)
