# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
from functions import GLib


def choose_nsswitch(self):
    """choose a nsswitch based on hosts: line"""
    choice = fn.get_combo_text(self.nsswitch_choices)

    # Map hosts: lines to config directories
    hosts_to_config = {
        "mymachines resolve [!UNAVAIL=return] files myhostname dns": ("arch", "Standard (no mdns)"),
        "mymachines resolve [!UNAVAIL=return] files dns mdns wins myhostname": ("arco", "With mdns + wins"),
        "mymachines mdns_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] files myhostname dns": ("biglinux", "With mdns_minimal"),
        "mymachines mdns4_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] files myhostname dns": ("manjaro", "With mdns4_minimal"),
        "files mymachines myhostname mdns_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] dns wins": ("garuda", "Custom order (no systemd)"),
    }

    if choice in hosts_to_config:
        label = hosts_to_config[choice][1]
        fn.copy_nsswitch(choice)
        GLib.idle_add(fn.show_in_app_notification, self, f"Nsswitch: {label}")


def choose_smb_conf(self):
    """Apply the Easy samba configuration"""
    fn.copy_samba("example")
    GLib.idle_add(
        fn.show_in_app_notification, self, "Smb.conf easy configuration applied"
    )


def create_samba_user(self):
    """create a new user for samba"""

    username = fn.sudo_username
    # password = self.entry_password.get_text()

    if username:
        fn.install_package(self, "alacritty")
        print("Type in your password for the Sambashare")
        print(
            "Although the user name is shared with Linux system, Samba uses a password"
        )
        print("separate from that of the Linux user accounts.")
        try:
            fn.subprocess.call(
                "alacritty -e /usr/bin/smbpasswd -a " + username,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            print("Created a password for the current user")
            print("Alacritty should pop open and you can type your Samba password")
            print("If you can not type your password - type the command in a terminal")
            print("sudo smbpasswd -a 'your_username'")
            fn.show_in_app_notification(self, "Created a password for the current user")
        except Exception as error:
            print(error)


def add_autoconnect_pulseaudio(self):
    if fn.file_check(fn.pulse_default):
        if fn.check_content("load-module module-switch-on-connect\n", fn.pulse_default):
            print("We have already enabled your headset to autoconnect")
        else:
            try:
                with open(fn.pulse_default, "r", encoding="utf-8") as f:
                    lists = f.readlines()
                    f.close()

                lists.append("\nload-module module-switch-on-connect\n")

                with open(fn.pulse_default, "w", encoding="utf-8") as f:
                    f.writelines(lists)
                    f.close()
                print("We have added this line to /etc/pulse/default.pa")
                print("load-module module-switch-on-connect")
                fn.show_in_app_notification(
                    self, "Pulseaudio bluetooth autoconnection enabled"
                )
            except Exception as error:
                print(error)


def restart_smb(self):
    """restart samba with detailed status checklist"""
    print("\n" + "=" * 70)
    print("SAMBA SERVICE RESTART - STATUS CHECKLIST")
    print("=" * 70)
    print(f"Configuration: {fn.samba_config}")
    print("=" * 70)

    smb_active = fn.check_service("smb")
    nmb_active = fn.check_service("nmb")
    avahi_active = fn.check_service("avahi-daemon")

    print(f"✓ Samba (smb):           {'✓ ACTIVE' if smb_active else '✗ INACTIVE'}")
    print(f"✓ NetBIOS (nmb):         {'✓ ACTIVE' if nmb_active else '✗ INACTIVE'}")
    print(f"✓ Avahi (discovery):     {'✓ ACTIVE' if avahi_active else '✗ INACTIVE'}")
    print("=" * 70)

    if smb_active:
        print("\nRestarting samba services...")
        fn.system("systemctl restart smb")
        if nmb_active:
            fn.system("systemctl restart nmb")
        print("✓ Samba services restarted successfully")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "✓ Samba restarted. Check other services in the status bar.",
        )
    else:
        print("\n✗ Samba is not installed or running")
        print("\nREQUIRED SETUP:")
        print("1. Install samba package: pacman -S samba")
        print("2. Enable services:")
        print("   - systemctl enable smb")
        if not nmb_active:
            print("   - systemctl enable nmb")
        if not avahi_active:
            print("   - systemctl enable avahi-daemon")
        print("3. Start services: systemctl start smb (and nmb/avahi if needed)")
        print("\nFor help, run: sudo systemctl status smb")
        print("=" * 70 + "\n")
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "✗ Samba not running. Check terminal output for setup instructions.",
        )
