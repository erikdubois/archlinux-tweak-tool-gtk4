# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0301,I1101,W0104

import functions as fn

from functions import GLib


def create_user(self):
    """Create a new user"""
    fn.log_subsection("Create New User Account")
    # if not empty fields
    username = self.hbox_username.get_text()
    name = self.hbox_name.get_text()
    atype = fn.get_combo_text(self.combo_account_type)
    password = self.hbox_password.get_text()
    confirm_password = self.hbox_confirm_password.get_text()
    if (
        len(username) > 0
        and len(name) > 0
        and len(password) > 0
        and len(confirm_password) > 0
    ):
        # if passwords check out
        if password == confirm_password:
            fn.debug_print(f"Creating user account: {username} ({name})")
            user_password = "echo " + username + ":" + password
            try:
                fn.debug_print("Ensuring sambashare group exists")
                command = "groupadd -r sambashare"
                fn.subprocess.call(
                    command.split(" "),
                    shell=False,
                    stdout=fn.subprocess.PIPE,
                    stderr=fn.subprocess.STDOUT,
                )
            except Exception as error:
                fn.log_warn(f"Sambashare group error: {error}")

            if password == confirm_password:
                try:
                    if atype == "Administrator":
                        fn.debug_print(f"Adding {username} to administrative groups")
                        useradd = (
                            'useradd -m -G audio,video,network,storage,rfkill,wheel,sambashare -c "'
                            + name
                            + '" -s /bin/bash '
                            + username
                        )
                        fn.system(useradd)
                        fn.system(user_password + " | " + "chpasswd -c SHA512")
                    else:
                        fn.debug_print(f"Creating standard user {username}")
                        useradd = (
                            'useradd -m -G audio,video,network,storage,rfkill,sambashare -c "'
                            + name
                            + '" -s /bin/bash '
                            + username
                        )
                        fn.system(useradd)
                        fn.system(user_password + " | " + "chpasswd -c SHA512")
                    fn.log_success(f"User account {username} created successfully")
                    GLib.idle_add(
                        fn.show_in_app_notification, self, "User has been created"
                    )
                except Exception as error:
                    fn.log_error(f"Failed to create user account: {error}")
                    fn.messagebox(self, "Error", f"Failed to create user: {error}")
        else:
            fn.log_warn("Password mismatch")
            fn.show_in_app_notification(self, "Passwords are not the same")
            fn.messagebox(self, "Message", "Passwords are not the same")
    else:
        fn.log_warn("Missing required fields")
        fn.show_in_app_notification(self, "First fill in all the fields")
        fn.messagebox(self, "Message", "First fill in all the fields")


def on_click_delete_user(self, _widget=None):
    """delete user"""
    fn.log_subsection("Delete User Account")
    username = fn.get_combo_text(self.cbt_users)
    if username is not None:
        try:
            fn.debug_print(f"Removing user account: {username}")
            userdel = "userdel " + username
            fn.system(userdel)
            fn.log_success(f"User {username} deleted - home folder retained")
            GLib.idle_add(fn.show_in_app_notification, self, "User has been deleted")
        except Exception as error:
            fn.log_error(f"Failed to delete user: {error}")
            fn.messagebox(self, "Error", f"Failed to delete user: {error}")


def on_click_delete_all_user(self, _widget=None):
    """delete also home dir"""
    fn.log_subsection("Delete User Account and Home Folder")
    username = fn.get_combo_text(self.cbt_users)
    if username is not None:
        try:
            fn.debug_print(f"Removing user account and home folder: {username}")
            userdel = "userdel -r -f " + username
            fn.system(userdel)
            fn.log_success(f"User {username} and home folder deleted")
            GLib.idle_add(
                fn.show_in_app_notification, self, "User and home folder has been deleted"
            )
        except Exception as error:
            fn.log_error(f"Failed to delete user and home folder: {error}")
            fn.messagebox(self, "Error", f"Failed to delete user: {error}")


def pop_cbt_users(self, combo):
    """populate with users - 1000 is default user - not included"""
    _m = combo.get_model(); _m.splice(0, _m.get_n_items(), [])
    users = fn.list_users("/etc/passwd")
    for user in users:
        self.cbt_users.get_model().append(user)
        self.cbt_users.set_selected(0)

# ====================================================================
# USER CALLBACKS
# ====================================================================


def on_click_user_apply(self, widget):
    create_user(self)
    pop_cbt_users(self, self.cbt_users)


def on_click_delete_user(self, widget):
    on_click_delete_user(self)
    pop_cbt_users(self, self.cbt_users)


def on_click_delete_all_user(self, widget):
    on_click_delete_all_user(self)
    pop_cbt_users(self, self.cbt_users)
