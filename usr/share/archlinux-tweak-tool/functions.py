# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0103,C0116,C0411,C0413,I1101,R1705,W0621,W0611,W0622
import gi

gi.require_version("Gtk", "4.0")

from os import rmdir, unlink, walk, execl, getpid, system, stat, readlink
from os import path, getlogin, mkdir, makedirs, listdir
from distro import id
import os
from gi.repository import GLib, Gtk
import sys
import threading
import shutil
import psutil
import datetime
import subprocess
import logging
import time
from queue import Queue
import pwd

# =====================================================
#              BEGIN DECLARATION OF VARIABLES
# =====================================================

distr = id()

sudo_username = getlogin()
home = "/home/" + str(sudo_username)

gpg_conf = "/etc/pacman.d/gnupg/gpg.conf"
gpg_conf_local = home + "/.gnupg/gpg.conf"

gpg_conf_original = "/usr/share/archlinux-tweak-tool/data/any/gpg.conf"
gpg_conf_local_original = "/usr/share/archlinux-tweak-tool/data/any/gpg.conf"

# login managers

# sddm
sddm_default_d1 = "/etc/sddm.conf"
sddm_default_d1_bak = "/etc/bak.sddm.conf"
sddm_default_d2 = "/etc/sddm.conf.d/kde_settings.conf"
sddm_default_d2_bak = "/etc/bak.kde_settings.conf"
sddm_default_d2_dir = "/etc/sddm.conf.d/"
sddm_default_d1_kiro = "/usr/share/archlinux-tweak-tool/data/kiro/sddm/sddm.conf"
sddm_default_d2_kiro = (
    "/usr/share/archlinux-tweak-tool/data/kiro/sddm.conf.d/kde_settings.conf"
)
icons_default = "/usr/share/icons/default/index.theme"

samba_config = "/etc/samba/smb.conf"

mirrorlist = "/etc/pacman.d/mirrorlist"
pacman = "/etc/pacman.conf"
pacman_arch = "/usr/share/archlinux-tweak-tool/data/arch/pacman/pacman.conf"
pacman_arco = "/usr/share/archlinux-tweak-tool/data/arco/pacman/pacman.conf"
pacman_eos = "/usr/share/archlinux-tweak-tool/data/eos/pacman/pacman.conf"
pacman_garuda = "/usr/share/archlinux-tweak-tool/data/garuda/pacman/pacman.conf"
blank_pacman_arch = "/usr/share/archlinux-tweak-tool/data/arch/pacman/blank/pacman.conf"
blank_pacman_arco = "/usr/share/archlinux-tweak-tool/data/arco/pacman/blank/pacman.conf"
blank_pacman_eos = "/usr/share/archlinux-tweak-tool/data/eos/pacman/blank/pacman.conf"
blank_pacman_garuda = (
    "/usr/share/archlinux-tweak-tool/data/garuda/pacman/blank/pacman.conf"
)
neofetch_arco = "/usr/share/archlinux-tweak-tool/data/arco/neofetch/config.conf"
fastfetch_arco = "/usr/share/archlinux-tweak-tool/data/arco/fastfetch/config.jsonc"
alacritty_arco = "/usr/share/archlinux-tweak-tool/data/arco/alacritty/alacritty.toml"

oblogout_conf = "/etc/oblogout.conf"
gtk3_settings = home + "/.config/gtk-3.0/settings.ini"
gtk2_settings = home + "/.gtkrc-2.0"
xfce_config = home + "/.config/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml"
xfce4_terminal_config = home + "/.config/xfce4/terminal/terminalrc"
alacritty_config = home + "/.config/alacritty/alacritty.toml"
alacritty_config_dir = home + "/.config/alacritty"
slimlock_conf = "/etc/slim.conf"
termite_config = home + "/.config/termite/config"
neofetch_config = home + "/.config/neofetch/config.conf"
fastfetch_config = home + "/.config/fastfetch/config.jsonc"
nsswitch_config = "/etc/nsswitch.conf"
bd = ".att_backups"
config = home + "/.config/archlinux-tweak-tool/settings.ini"
config_dir = home + "/.config/archlinux-tweak-tool/"
polybar = home + "/.config/polybar/"
desktop = ""
autostart = home + "/.config/autostart/"
pulse_default = "/etc/pulse/default.pa"
bash_config = ""
zsh_config = ""
fish_config = ""

if path.isfile(home + "/.config/fish/config.fish"):
    fish_config = home + "/.config/fish/config.fish"
if path.isfile(home + "/.zshrc"):
    zsh_config = home + "/.zshrc"
if path.isfile(home + "/.bashrc"):
    bash_config = home + "/.bashrc"

bashrc_arco = "/usr/share/archlinux-tweak-tool/data/arco/.bashrc"
zshrc_arco = "/usr/share/archlinux-tweak-tool/data/arco/.zshrc"
fish_arco = "/usr/share/archlinux-tweak-tool/data/arco/config.fish"
account_list = ["Standard", "Administrator"]
i3wm_config = home + "/.config/i3/config"
awesome_config = home + "/.config/awesome/rc.lua"
qtile_config = home + "/.config/qtile/config.py"
qtile_config_theme = home + "/.config/qtile/themes/arcolinux-default.theme"
leftwm_config = home + "/.config/leftwm/config.ron"
leftwm_config_theme = home + "/.config/leftwm/themes/"
leftwm_config_theme_current = home + "/.config/leftwm/themes/current"

seedhostmirror = "Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"
aarnetmirror = "Server = https://mirror.aarnet.edu.au/pub/arcolinux/$repo/$arch"

atestrepo = "#[arcolinux_repo_testing]\n\
#SigLevel = Never\n\
#Server = https://arcolinux.github.io/$repo/$arch"

arepo = "[arcolinux_repo]\n\
SigLevel = Never\n\
Server = https://arcolinux.github.io/$repo/$arch"

a3drepo = "[arcolinux_repo_3party]\n\
SigLevel = Never\n\
Server = https://arcolinux.github.io/$repo/$arch"

axlrepo = "#[arcolinux_repo_xlarge]\n\
#SigLevel = Never\n\
#Server = https://arcolinux.github.io/$repo/$arch"

garuda_repo = "[garuda]\n\
SigLevel = Required DatabaseOptional\n\
Include = /etc/pacman.d/chaotic-mirrorlist"

chaotics_repo = "[chaotic-aur]\n\
SigLevel = Required DatabaseOptional\n\
Include = /etc/pacman.d/chaotic-mirrorlist"

endeavouros_repo = "[endeavouros]\n\
SigLevel = PackageRequired\n\
Include = /etc/pacman.d/endeavouros-mirrorlist"

nemesis_repo = "[nemesis_repo]\n\
SigLevel = Never\n\
Server = https://erikdubois.github.io/$repo/$arch"

# xero_repo = "[xerolinux_repo]\n\
# SigLevel = Optional TrustAll\n\
# Include = /etc/pacman.d/xero-mirrorlist"

# xero_xl_repo = "[xerolinux_repo_xl]\n\
# SigLevel = Optional TrustAll\n\
# Include = /etc/pacman.d/xero-mirrorlist"

# xero_nv_repo = "[xerolinux_nvidia_repo]\n\
# SigLevel = Optional TrustAll\n\
# Include = /etc/pacman.d/xero-mirrorlist"

arch_testing_repo = "[core-testing]\n\
Include = /etc/pacman.d/mirrorlist"

arch_core_repo = "[core]\n\
Include = /etc/pacman.d/mirrorlist"

arch_extra_repo = "[extra]\n\
Include = /etc/pacman.d/mirrorlist"

arch_extra_testing_repo = "[extra-testing]\n\
Include = /etc/pacman.d/mirrorlist"

arch_multilib_testing_repo = "[multilib-testing]\n\
Include = /etc/pacman.d/mirrorlist"

arch_multilib_repo = "[multilib]\n\
Include = /etc/pacman.d/mirrorlist"

reborn_repo = "[Reborn-OS]\n\
SigLevel = PackageRequired DatabaseNever\n\
Include = /etc/pacman.d/reborn-mirrorlist"

leftwm_themes_list = [
    "arise",
    "candy",
    "db",
    "db-color-dev",
    "db-comic",
    "db-labels",
    "db-nemesis",
    "db-scifi",
    "docky",
    "doublebar",
    "eden",
    "forest",
    "grayblocks",
    "greyblocks",
    "halo",
    "kittycafe-dm",
    "kittycafe-sm",
    "material",
    "matrix",
    "mesh",
    "parker",
    "pi",
    "sb-horror",
    "shades",
    "smooth",
    "space",
    "starwars",
]

# pacman log file
pacman_logfile = "/var/log/pacman.log"

# pacman cache directory
pacman_cache_dir = "/var/cache/pacman/pkg/"

# pacman lock file
pacman_lockfile = "/var/lib/pacman/db.lck"

# logging setup
logger = logging.getLogger("logger")
# create console handler and set level to debug
ch = logging.StreamHandler()

logger.setLevel(logging.INFO)
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter(
    "%(asctime)s:%(levelname)s > %(message)s", "%Y-%m-%d %H:%M:%S"
)
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


# =====================================================
#              END DECLARATION OF VARIABLES
# =====================================================
# =====================================================
# =====================================================
# =====================================================
# =====================================================
#               BEGIN GLOBAL FUNCTIONS
# =====================================================


def get_combo_text(combo):
    """Get selected text from a Gtk.DropDown with Gtk.StringList model."""
    item = combo.get_selected_item()
    return item.get_string() if item is not None else None


def get_lines(files):
    try:
        if path.isfile(files):
            with open(files, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            return lines
    except Exception as error:
        print(error)
    # get position in list


def get_position(lists, value):
    data = [string for string in lists if value in string]
    if len(data) != 0:
        position = lists.index(data[0])
        return position
    return 0


# get positions in list


def get_positions(lists, value):
    data = [string for string in lists if value in string]
    position = []
    for d in data:
        position.append(lists.index(d))
    return position


# get variable from list


def _get_variable(lists, value):
    data = [string for string in lists if value in string]

    if len(data) >= 1:
        data1 = [string for string in data if "#" in string]

        for i in data1:
            if i[:4].find("#") != -1:
                data.remove(i)
    if data:
        data_clean = [data[0].strip("\n").replace(" ", "")][0].split("=")
    return data_clean


# Check  value exists remove data


def check_value(list, value):
    data = [string for string in list if value in string]
    if len(data) >= 1:
        data1 = [string for string in data if "#" in string]
        for i in data1:
            if i[:4].find("#") != -1:
                data.remove(i)
    return data


# check backups


def check_backups(now):
    if not path.exists(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H")):
        makedirs(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H"), 0o777)
        permissions(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H"))


# check process is running


def check_if_process_is_running(processName):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            if processName == pinfo["name"]:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


# copytree


def copytree(self, src, dst, symlinks=False, ignore=None):  # noqa
    if not path.exists(dst):
        makedirs(dst)
    for item in listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.exists(d):
            try:
                shutil.rmtree(d)
            except Exception as error:
                print(error)
                unlink(d)
        if path.isdir(s):
            try:
                shutil.copytree(s, d, symlinks, ignore)
            except Exception as error:
                print(error)
                print("ERROR2")
                self.ecode = 1
        else:
            try:
                shutil.copy2(s, d)
            except:  # noqa
                print("ERROR3")
                self.ecode = 1


# check sddm value


def check_sddm_value(list, value):
    data = [string for string in list if value in string]
    return data


# check if file exists


def file_check(file):
    if path.isfile(file):
        return True

    return False


# check if path exists


def path_check(path):
    if os.path.isdir(path):
        return True

    return False


# check if directory is empty


def is_empty_directory(path):
    if os.path.exists(path) and not os.path.isfile(path):
        if not os.listdir(path):
            return True
        else:
            return False


# check if value is true or false in file


def check_content(value, file):
    try:
        with open(file, "r", encoding="utf-8") as myfile:
            lines = myfile.readlines()
            myfile.close()

        for line in lines:
            if value in line:
                if value in line:
                    return True
                else:
                    return False
        return False
    except:
        return False


# check if package is installed or not
def check_package_installed(package):  # noqa
    try:
        subprocess.check_output(
            "pacman -Qi " + package, shell=True, stderr=subprocess.PIPE
        )
        # package is installed
        return True
    except subprocess.CalledProcessError:
        # package is not installed
        return False


# check if service is active


def check_service(service):  # noqa
    try:
        command = "systemctl is-active " + service + ".service"
        output = subprocess.run(
            command.split(" "),
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        status = output.stdout.decode().strip()
        if status == "active":
            return True
        else:
            return False
    except Exception:
        return False


def check_socket(socket):  # noqa
    try:
        command = "systemctl is-active " + socket + ".socket"
        output = subprocess.run(
            command.split(" "),
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        status = output.stdout.decode().strip()
        if status == "active":
            return True
        else:
            return False
    except Exception:
        return False


# list normal users


def list_users(filename):  # noqa
    try:
        data = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if "1001" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1002" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1003" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1004" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1005" in line.split(":")[2]:
                    data.append(line.split(":")[0])
            data.sort()
            return data
    except Exception as error:
        print(error)


# check if user is part of the group


def check_group(group):
    try:
        groups = subprocess.run(
            ["sh", "-c", "id " + sudo_username],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        for x in groups.stdout.decode().split(" "):
            if group in x:
                return True
            else:
                return False
    except Exception as error:
        print(error)


def check_systemd_boot():
    if (
        path_check("/boot/loader") is True
        and file_check("/boot/loader/loader.conf") is True
    ):
        return True
    else:
        return False


# =====================================================
#               END GLOBAL FUNCTIONS
# =====================================================
# =====================================================
# =====================================================
# =====================================================


def check_arco_repos_active():
    with open(pacman, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()

        arco_base = "[arcolinux_repo]"
        arco_3p = "[arcolinux_repo_3party]"
        # arco_xl = "[arcolinux_repo_xlarge]"

    for line in lines:
        if arco_base in line:
            if "#" + arco_base in line:
                return False
            else:
                return True

    for line in lines:
        if arco_3p in line:
            if "#" + arco_3p in line:
                return False
            else:
                return True


def check_edu_repos_active():
    with open(pacman, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()

        nemesis = "[nemesis_repo]"

    for line in lines:
        if nemesis in line:
            if "#" + nemesis in line:
                return False
            else:
                return True


_nemesis_packages_cache = None

def load_nemesis_packages():
    """Load the list of nemesis_repo packages from file"""
    global _nemesis_packages_cache
    if _nemesis_packages_cache is not None:
        return _nemesis_packages_cache

    nemesis_file = "/usr/share/archlinux-tweak-tool/data/nemesis_packages.txt"
    _nemesis_packages_cache = set()

    try:
        if path.exists(nemesis_file):
            with open(nemesis_file, 'r') as f:
                _nemesis_packages_cache = set(line.strip() for line in f if line.strip())
            print(f"[INFO] Loaded {len(_nemesis_packages_cache)} nemesis packages from {nemesis_file}")
        else:
            print(f"[INFO] nemesis_packages.txt not found at {nemesis_file}")
    except Exception as e:
        print(f"[ERROR] Failed to load nemesis packages: {e}")

    return _nemesis_packages_cache


def find_package_repo(package_name):
    """Determine which repo a package belongs to (nemesis_repo or chaotic-aur)"""
    print(f"[INFO] find_package_repo() called for: {package_name}")

    nemesis_packages = load_nemesis_packages()
    if package_name in nemesis_packages:
        print(f"[INFO] Found {package_name} in nemesis_repo")
        return "nemesis_repo"

    print(f"[INFO] Package {package_name} not in nemesis_repo, assuming chaotic-aur")
    return "chaotic-aur"


def check_missing_repo_error(self, error_msg, package):
    """Check if installation error is due to missing repo and show appropriate error"""
    print(f"\n[INFO] check_missing_repo_error() called")
    print(f"[INFO] Package: {package}")
    print(f"[INFO] Error message length: {len(error_msg)}")
    print(f"[INFO] Error message (first 200 chars): {error_msg[:200]}")

    if "target not found" not in error_msg.lower():
        print(f"[INFO] 'target not found' not in error message, returning False")
        return False

    print(f"[INFO] 'target not found' detected, querying repo for {package}")
    repo = find_package_repo(package)

    if repo:
        notification = f"Package not found. Please enable {repo} in pacman.conf"
    else:
        notification = "Package not found. Please enable nemesis_repo or chaotic-aur in pacman.conf"

    print(f"[INFO] Showing notification: {notification}")
    GLib.idle_add(show_in_app_notification, self, notification)
    return True


def install_package(self, package):
    try:
        # Map package names to their binary names (some packages have different binary names)
        binary_map = {
            "fastfetch-git": "fastfetch",
            "yay-git": "yay",
            "paru-git": "paru",
        }
        binary_name = binary_map.get(package, package)
        binary_path = f"/usr/bin/{binary_name}"

        if path.exists(binary_path):
            print(f"\n[INFO] {package} already installed")
            GLib.idle_add(show_in_app_notification, self, f"{package} already installed")
            return

        print(f"\n[INFO] {package} not installed, starting installation")
        process = launch_pacman_install_in_terminal(package)
        GLib.idle_add(show_in_app_notification, self, f"{package} installation started")
        wait_install_and_update(process, binary_path, None, None, self, f"{package} installed", package)
    except Exception as error:
        print(error)
        GLib.idle_add(show_in_app_notification, self, f"Error installing {package}: {error}")


def install_local_package(self, package):
    command = "pacman -U " + package + " --noconfirm"
    # if more than one package - checf fails and will install
    try:
        print(f"[INFO] Executing: {command}")
        print(f"[INFO] Installing package: {package}")
        print(f"[INFO] Verifying package file exists: {package}")
        if not os.path.exists(package):
            raise Exception(f"Package file not found: {package}")
        print(f"[INFO] Package file verified")
        result = subprocess.run(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            print(f"[INFO] {package} is now installed")
            GLib.idle_add(show_in_app_notification, self, package + " is now installed")
        else:
            error_output = result.stderr if result.stderr else result.stdout
            print(f"[ERROR] Installation failed with exit code: {result.returncode}")
            print(f"[ERROR] Pacman output: {error_output}")
            GLib.idle_add(show_in_app_notification, self, f"Installation failed: {error_output[:100]}")
    except Exception as error:
        print(f"[ERROR] Installation error: {error}")
        GLib.idle_add(show_in_app_notification, self, f"Installation error: {error}")


def install_arco_package(self, package):
    if check_edu_repos_active():
        command = "pacman -S " + package + " --noconfirm --needed"
        if check_package_installed(package):
            print(package + " is already installed - nothing to do")
            GLib.idle_add(
                show_in_app_notification,
                self,
                package + " is already installed - nothing to do",
            )
        else:
            try:
                print(command)
                subprocess.call(
                    command.split(" "),
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                print(package + " is now installed")
                GLib.idle_add(
                    show_in_app_notification, self, package + " is now installed"
                )
            except Exception as error:
                print(error)
    else:
        print("You need to activate the Nemesis repo")
        print("Check the pacman tab of the ArchLinux Tweak Tool")
        print("and/or the content of /etc/pacman.conf")
        GLib.idle_add(
            show_in_app_notification, self, "You need to activate the Nemesis repo"
        )


def install_edu_package(self, package):
    if check_edu_repos_active():
        command = "pacman -S " + package + " --noconfirm --needed"
        if check_package_installed(package):
            print(package + " is already installed - nothing to do")
            GLib.idle_add(
                show_in_app_notification,
                self,
                package + " is already installed - nothing to do",
            )
        else:
            try:
                print(command)
                subprocess.call(
                    command.split(" "),
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                print(package + " is now installed")
                GLib.idle_add(
                    show_in_app_notification, self, package + " is now installed"
                )
            except Exception as error:
                print(error)
    else:
        print("You need to activate the Nemesis repo")
        print("Check the pacman tab of the ArchLinux Tweak Tool")
        print("and/or the content of /etc/pacman.conf")
        GLib.idle_add(
            show_in_app_notification, self, "You need to activate the Nemesis repo"
        )


def clear_skel_directory(path="/etc/skel"):
    # Ensure the provided path is indeed /etc/skel or a user-defined path
    if not os.path.exists(path):
        print(f"The directory {path} does not exist.")
        return

    # Iterate over all the items in the directory
    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        # Check if the item is a file or a directory and remove it
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove the file or symlink
                print(f"Removed file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove the directory and its content
                print(f"Removed directory: {item_path}")
        except Exception as e:
            print(f"Failed to remove {item_path}. Reason: {e}")


def remove_file(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return f"File '{file_path}' has been removed successfully."
        except OSError as e:
            return f"Error: {e.strerror}"
    else:
        return f"File '{file_path}' does not exist."


def remove_package(self, package):
    command = "pacman -R " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(package + " is now removed")
            GLib.idle_add(show_in_app_notification, self, package + " is now removed")
        except Exception as error:
            print(error)
    else:
        print(package + " is already removed")
        GLib.idle_add(show_in_app_notification, self, package + " is already removed")


def remove_package_s(self, package):
    command = "pacman -Rs " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(package + " is now removed")
            GLib.idle_add(show_in_app_notification, self, package + " is now removed")
        except Exception as error:
            print(error)
    else:
        print(package + " is already removed")
        GLib.idle_add(show_in_app_notification, self, package + " is already removed")


def remove_package_rns(self, package):
    command = "pacman -Rns " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(package + " is now removed")
            GLib.idle_add(show_in_app_notification, self, package + " is now removed")
        except Exception as error:
            print(error)
    else:
        print(package + " is already removed")
        GLib.idle_add(show_in_app_notification, self, package + " is already removed")


def remove_package_ss(self, package):
    command = "pacman -Rss " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(package + " is now removed")
            GLib.idle_add(show_in_app_notification, self, package + " is now removed")
        except Exception as error:
            print(error)
    else:
        print(package + " is already removed")
        GLib.idle_add(show_in_app_notification, self, package + " is already removed")


def remove_package_dd(self, package):
    command = "pacman -Rdd " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(package + " is now removed")
            GLib.idle_add(show_in_app_notification, self, package + " is now removed")
        except Exception as error:
            print(error)
    else:
        print(package + " is already removed")
        GLib.idle_add(show_in_app_notification, self, package + " is already removed")


def enable_login_manager(self, loginmanager):
    if check_package_installed(loginmanager):
        try:
            command = "systemctl enable " + loginmanager + ".service -f"
            print(command)
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(loginmanager + " has been enabled - reboot")
            GLib.idle_add(
                show_in_app_notification,
                self,
                loginmanager + " has been enabled - reboot",
            )
        except Exception as error:
            print(error)
    else:
        print(loginmanager + " is not installed")
        GLib.idle_add(
            show_in_app_notification, self, loginmanager + " is not installed"
        )


def add_autologin_group(self):
    com = subprocess.run(
        ["sh", "-c", "su - " + sudo_username + " -c groups"],
        check=True,
        shell=False,
        stdout=subprocess.PIPE,
    )
    groups = com.stdout.decode().strip().split(" ")
    if "autologin" not in groups:
        command = "groupadd autologin"
        try:
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as error:
            print(error)
        try:
            subprocess.run(
                ["gpasswd", "-a", sudo_username, "autologin"], check=True, shell=False
            )
        except Exception as error:
            print(error)


# =====================================================
#              CAJA SHARE PLUGIN
# =====================================================


def install_arco_caja_plugin(self, widget):
    # install = "pacman -S caja arcolinux-caja-share --noconfirm"
    install = "pacman -S caja caja-share --noconfirm"

    if check_package_installed("caja-share"):
        print("caja-share is already installed")
    else:
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("Caja-share is now installed - reboot")
        GLib.idle_add(self.label7.set_text, "Caja-share is now installed - reboot")
    print("Other apps that might be interesting for sharing are :")
    print(" - thunar-share-plugin (thunar)")
    print(" - nemo-share (cinnamon)")
    print(" - nautilus-share (gnome - budgie)")
    print(" - kdenetwork-filesharing (plasma)")


# =====================================================
#              CHANGE SHELL
# =====================================================


def change_shell(self, shell):
    command = "sudo chsh " + sudo_username + " -s /bin/" + shell
    subprocess.call(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    print("Shell changed to " + shell + " for the user - logout")
    GLib.idle_add(
        show_in_app_notification,
        self,
        "Shell changed to " + shell + " for user - logout",
    )


# =====================================================
#               CONVERT COLOR
# =====================================================


def rgb_to_hex(rgb):
    if "rgb" in rgb:
        rgb = rgb.replace("rgb(", "").replace(")", "")
        vals = rgb.split(",")
        return "#{0:02x}{1:02x}{2:02x}".format(
            clamp(int(vals[0])), clamp(int(vals[1])), clamp(int(vals[2]))
        )
    return rgb


def clamp(x):
    return max(0, min(x, 255))


# =====================================================
#               COPY FUNCTION
# =====================================================


def copy_func(src, dst, isdir=False):
    if isdir:
        subprocess.run(["cp", "-Rp", src, dst], check=True, shell=False)
    else:
        subprocess.run(["cp", "-p", src, dst], check=True, shell=False)


# =====================================================
#               DISTRO LABEL
# =====================================================

# exceptions
if distr == "manjaro" and check_content("biglinux", "/etc/os-release"):
    distr = "biglinux"


def change_distro_label(name):  # noqa
    if name == "arcolinux":
        name = "ArcoLinux"
    if name == "biglinux":
        name = "BigLinux"
    if name == "garuda":
        name = "Garuda"
    if name == "endeavouros":
        name = "EndeavourOS"
    if name == "arch":
        name = "Arch Linux"
    if name == "manjaro":
        name = "Manjaro"
    if name == "xerolinux":
        name = "Xerolinux"
    if name == "axyl":
        name = "Axyl"
    if name == "rebornos":
        name = "RebornOS"
    if name == "amos":
        name = "AmOs"
    if name == "archcraft":
        name = "Archcraft"
    if name == "artix":
        name = "Artix"
    if name == "Archman":
        name = "ArchMan"
    if name == "cachyos":
        name = "CachyOS"
    return name


def reset_login_wallpaper(self, image):
    if path.isfile(sddm_default_d2):
        try:
            with open(sddm_default_d2, "r", encoding="utf-8") as f:
                lists = f.readlines()
                f.close()
            val = get_position(lists, "Current=")
            theme = lists[val].strip("\n").split("=")[1]
        except:
            pass

    if path.isfile("/usr/share/sddm/themes/" + theme + "/theme.conf.user"):
        try:
            unlink("/usr/share/sddm/themes/" + theme + "/theme.conf.user")
            print("Standard background has been reset")
            show_in_app_notification(self, "Background reset successfully")
        except:
            pass


# =====================================================
#               HBLOCK CONF
# =====================================================


def hblock_get_state(self):
    lines = int(
        subprocess.check_output("wc -l /etc/hosts", shell=True).strip().split()[0]
    )
    if path.exists("/usr/bin/hblock") and lines > 100:
        return True

    self.firstrun = False
    return False


def do_pulse(data, prog):
    prog.pulse()
    return True


def set_hblock(self, toggle, state):
    GLib.idle_add(toggle.set_sensitive, False)
    GLib.idle_add(self.label7.set_visible, True)
    GLib.idle_add(self.progress.set_visible, True)
    GLib.idle_add(self.label7.set_text, "Run..")
    GLib.idle_add(self.progress.set_fraction, 0.2)

    timeout_id = None
    timeout_id = GLib.timeout_add(100, do_pulse, None, self.progress)

    if not path.isfile("/etc/hosts.bak"):
        shutil.copy("/etc/hosts", "/etc/hosts.bak")

    try:
        install = "pacman -S edu-hblock-git --needed --noconfirm"
        enable = "/usr/bin/hblock"

        if state:
            if path.exists("/usr/bin/hblock"):
                GLib.idle_add(self.label7.set_text, "Database update...")
                subprocess.call(
                    [enable],
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            else:
                GLib.idle_add(self.label7.set_text, "Install Hblock......")
                subprocess.call(
                    install.split(" "),
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                GLib.idle_add(self.label7.set_text, "Database update...")
                subprocess.call(
                    [enable],
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

        else:
            GLib.idle_add(self.label7.set_text, "Remove update...")
            subprocess.run(
                ["sh", "-c", "HBLOCK_SOURCES='' /usr/bin/hblock"],
                check=True,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        GLib.idle_add(self.label7.set_text, "Complete")
        GLib.source_remove(timeout_id)
        timeout_id = None
        GLib.idle_add(self.progress.set_fraction, 0)

        GLib.idle_add(toggle.set_sensitive, True)
        if state:
            GLib.idle_add(self.label7.set_text, "HBlock Active")
        else:
            GLib.idle_add(self.label7.set_text, "HBlock Inactive")
        GLib.idle_add(self.label7.set_visible, False)
        GLib.idle_add(self.progress.set_visible, False)

    except Exception as error:
        messagebox(self, "ERROR!!", str(error))
        print(error)


# =====================================================
#               LOG FILE CREATION
# =====================================================


log_dir = "/var/log/archlinux/"
att_log_dir = "/var/log/archlinux/att/"


def create_log(self):
    print("Making log in /var/log/archlinux")
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d-%H-%M-%S")
    destination = att_log_dir + "att-log-" + time
    command = "sudo pacman -Q > " + destination
    subprocess.call(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    # GLib.idle_add(show_in_app_notification, self, "Log file created")

# =====================================================
#               MESSAGEBOX
# =====================================================


def messagebox(self, title, message):
    md2 = Gtk.MessageDialog(
        transient_for=self,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=title,
    )
    md2.props.secondary_text = message
    md2.props.secondary_use_markup = True
    loop = GLib.MainLoop()

    def on_response(d, response_id):
        loop.quit()
        d.destroy()

    md2.connect("response", on_response)
    md2.show()
    loop.run()


# =====================================================
#              NEMO SHARE PLUGIN
# =====================================================


def install_arco_nemo_plugin(self, widget):
    # install = "pacman -S nemo arcolinux-nemo-share --noconfirm"
    install = "pacman -S nemo nemo-share --noconfirm"

    if check_package_installed("nemo-share"):
        print("Nemo-share is already installed")
    else:
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("Nemo-share is now installed - reboot")
        GLib.idle_add(self.label7.set_text, "Nemo-share is now installed - reboot")
    print("Other apps that might be interesting for sharing are :")
    print(" - thunar-share-plugin (thunar)")
    print(" - caja-share (mate)")
    print(" - kdenetwork-filesharing (plasma)")
    print(" - nautilus-share (gnome - budgie)")


# =====================================================
#               NEOFETCH CONF
# =====================================================


def neofetch_set_value(lists, pos, text, state):
    if state:
        if text in lists[pos]:
            if "#" in lists[pos]:
                lists[pos] = lists[pos].replace("#", "")
    else:
        if text in lists[pos]:
            if "#" not in lists[pos]:
                lists[pos] = "#" + lists[pos]

    return lists


def neofetch_set_backend_value(lists, pos, text, value):
    if text in lists[pos] and "#" not in lists[pos]:
        lists[pos] = text + value + '"\n'


# =====================================================
#               FASTFETCH CONF
# =====================================================


def fastfetch_set_value(lists, pos, text, state):
    if state:
        if text in lists[pos]:
            if "#" in lists[pos]:
                lists[pos] = lists[pos].replace("#", "")
    else:
        if text in lists[pos]:
            if "#" not in lists[pos]:
                lists[pos] = "#" + lists[pos]

    return lists


def fastfetch_set_backend_value(lists, pos, text, value):
    if text in lists[pos] and "#" not in lists[pos]:
        lists[pos] = text + value + '"\n'

def get_shell_config():
    # Get the actual user's home directory
    user_name = os.getlogin()
    user_home = pwd.getpwnam(user_name).pw_dir

    possible_configs = [
        os.path.join(user_home, '.bashrc'),
        os.path.join(user_home, '.zshrc'),
        os.path.join(user_home, '.config', 'fish', 'config.fish')
    ]

    for config in possible_configs:
        if os.path.isfile(config):
            return config

    return None

# =====================================================
#               NOTIFICATIONS
# =====================================================


def show_in_app_notification(self, message):
    if self.timeout_id is not None:
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None

    self.notification_label.set_markup(
        '<span foreground="white">' + message + "</span>"
    )
    self.notification_revealer.set_reveal_child(True)
    self.timeout_id = GLib.timeout_add(3000, timeOut, self)


def timeOut(self):
    close_in_app_notification(self)


def close_in_app_notification(self):
    self.notification_revealer.set_reveal_child(False)
    GLib.source_remove(self.timeout_id)
    self.timeout_id = None


# =====================================================
#               NSSWITCH CONF COPY
# =====================================================


def copy_nsswitch(new_hosts_line):
    dest_file = "/etc/nsswitch.conf"

    try:
        # Read the current nsswitch.conf
        with open(dest_file, 'r') as f:
            dest_lines = f.readlines()

        # Find and replace only the hosts: line
        old_hosts_line = None
        updated_lines = []
        for line in dest_lines:
            if line.startswith('hosts:'):
                old_hosts_line = line.rstrip('\n')
                updated_lines.append(new_hosts_line + '\n')
            else:
                updated_lines.append(line)

        # Write back to nsswitch.conf
        with open(dest_file, 'w') as f:
            f.writelines(updated_lines)

        # Show what changed
        if old_hosts_line:
            print(f"[INFO] Previous code: {old_hosts_line}")
            print(f"[INFO] New code:      {new_hosts_line}")
    except Exception as e:
        print(f"[INFO] Error updating nsswitch.conf: {e}")


# =====================================================
#               OBLOGOUT CONF
# =====================================================
# Get shortcuts index


def get_shortcuts(conflist):
    sortcuts = _get_variable(conflist, "shortcuts")
    shortcuts_index = get_position(conflist, sortcuts[0])
    return int(shortcuts_index)


# Get commands index


def get_commands(conflist):
    commands = _get_variable(conflist, "commands")
    commands_index = get_position(conflist, commands[0])
    return int(commands_index)

# =====================================================
#               PACMAN EXTRA KEYS AND MIRRORS
# =====================================================


def install_reborn(self):
    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/reborn/packages/keyring/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("RebornOS keyring is now installed")
    except Exception as error:
        print(error)

    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/reborn/packages/mirrorlist/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("RebornOS mirrorlist is now installed")
    except Exception as error:
        print(error)


def install_chaotics(self):
    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/garuda/packages/keyring/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("Chaotics keyring is now installed")
    except Exception as error:
        print(error)

    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/garuda/packages/mirrorlist/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("Chaotics mirrorlist is now installed")
    except Exception as error:
        print(error)


def install_endeavouros(self):
    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/eos/packages/keyring/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("EndeavourOS keyring is now installed")
    except Exception as error:
        print(error)

    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/eos/packages/mirrorlist/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("EndeavourOS mirrorlist is now installed")
    except Exception as error:
        print(error)


def install_arcolinux(self):
    """Add the ArcoLinux repos to /etc/pacman.conf if none are present."""
    if not check_content("arcolinux", pacman):

        print("[INFO] : Adding ArcoLinux repos")
        try:
            with open(pacman, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as error:
            print(error)
            return  # Exit early if read fails

        # Repos to be added at the end
        text = (
            "\n\n"
            + arepo
            + "\n\n"
            + a3drepo
            + "\n"
        )

        lines.append(text)

        try:
            with open(pacman, "w", encoding="utf-8") as f:
                f.writelines(lines)
        except Exception as error:
            print(error)


def test(dst):
    for root, dirs, filesr in walk(dst):
        for folder in dirs:
            pass
            for file in filesr:
                pass
        for file in filesr:
            pass


def permissions(dst):
    try:
        groups = subprocess.run(
            ["sh", "-c", "id " + sudo_username],
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        group = None
        for x in groups.stdout.decode().split(" "):
            if "gid" in x.lower():  # match gid and GID
                try:
                    g = x.split("(")[1]
                    group = g.replace(")", "").strip()
                    break
                except IndexError:
                    raise ValueError("Unexpected format in 'id' command output.")

        # Ensure the group is retrieved
        if not group:
            raise ValueError(f"Could not determine group for user {sudo_username}.")

        subprocess.call(["chown", "-R", sudo_username + ":" + group, dst], shell=False)
    except Exception as error:
        print(error)

def findgroup():
    try:
        groups = subprocess.run(
            ["sh", "-c", "id " + sudo_username],
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        group = None
        for x in groups.stdout.decode().split(" "):
            if "gid" in x.lower():  # match gid and GID
                try:
                    g = x.split("(")[1]
                    group = g.replace(")", "").strip()
                    break
                except IndexError:
                    raise ValueError("Unexpected format in 'id' command output.")

        # Ensure the group is retrieved
        if not group:
            raise ValueError(f"Could not determine group for user {sudo_username}.")
        print("[INFO] : Group = " + group)

    except Exception as error:
        print(error)


# =====================================================
#               RESTART PROGRAM
# =====================================================


def restart_program():
    if path.exists("/tmp/att.lock"):
        unlink("/tmp/att.lock")
        python = sys.executable
        execl(python, python, *sys.argv)


# =====================================================
#               SERVICES - GENERAL FUNCTIONS CUPS
# =====================================================


def enable_service(service):
    try:
        command = "systemctl enable " + service + ".service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("We enabled the following service : " + service)
    except Exception as error:
        print(error)


def restart_service(service):
    try:
        command = "systemctl reload-or-restart " + service + ".service"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("We restarted the following service (if avalable) : " + service)
    except Exception as error:
        print(error)


def disable_service(service):
    try:
        command = "systemctl stop " + service
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        command = "systemctl disable " + service
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("We stopped and disabled the following service " + service)
    except Exception as error:
        print(error)


def find_active_audio():
    output = subprocess.run(["pactl", "info"], check=True, stdout=subprocess.PIPE)

    pipewire_active = check_value(output, "pipewire")

    if pipewire_active == True:
        return pipewire_active
    else:
        return pipewire_active


# =====================================================
#               SERVICES - AVAHI
# =====================================================


def install_discovery(self):
    try:
        packages = "avahi nss-mdns gvfs-smb"
        print(f"[INFO] Opening terminal to install: {packages}")
        launch_pacman_install_in_terminal(packages)

        command = "systemctl enable avahi-daemon.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("[INFO] Avahi daemon enabled")
    except Exception as error:
        print(f"[INFO] Error installing discovery: {error}")


def remove_discovery(self):
    try:
        command = "systemctl stop avahi-daemon.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        command = "systemctl disable avahi-daemon.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("[INFO] Avahi daemon disabled")

        command = "systemctl stop avahi-daemon.socket -f"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        command = "systemctl disable avahi-daemon.socket -f"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("[INFO] Avahi socket disabled")

        packages = "avahi nss-mdns gvfs-smb"
        print(f"[INFO] Opening terminal to remove: {packages}")
        launch_pacman_remove_in_terminal(packages)
    except Exception as error:
        print(f"[INFO] Error removing discovery: {error}")


# =====================================================
#               SERVICES - SAMBA
# =====================================================


def install_samba(self):
    try:
        install = "pacman -S samba gvfs-smb --needed --noconfirm"

        if not path.isdir("/var/cache/samba"):
            makedirs("/var/cache/samba", 0o755)

        if check_package_installed("samba") and check_package_installed("gvfs-smb"):
            pass
        else:
            subprocess.call(
                install.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print("Samba and gvfs-smb are now installed")

        command = "systemctl enable smb.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("We enabled smb.service")

        command = "systemctl enable nmb.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("We enabled nmb.service")
    except Exception as error:
        print(error)


def uninstall_samba(self):
    try:
        command = "systemctl disable smb.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("We disabled smb.service")

        command = "systemctl disable nmb.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("We disabled nmb.service")

        command = "pacman -Rs samba --noconfirm"
        if check_package_installed("samba"):
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print("Samba was removed if there were no dependencies")

        command = "pacman -Rs gvfs-smb --noconfirm"
        if check_package_installed("nss-mdns"):
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print("gvfs-smb was removed")
    except Exception as error:
        print(error)


# =====================================================
#               SAMBA CONF COPY
# =====================================================


def copy_samba(choice):
    command = (
        "cp /usr/share/archlinux-tweak-tool/data/any/samba/"
        + choice
        + "/smb.conf /etc/samba/smb.conf"
    )
    subprocess.call(
        command.split(" "),
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if choice == "example":
        if not path.isdir("/home/" + sudo_username + "/Shared"):
            makedirs("/home/" + sudo_username + "/Shared", 0o755)
        permissions("/home/" + sudo_username + "/Shared")
        try:
            with open(samba_config, "r", encoding="utf-8") as f:
                lists = f.readlines()
                f.close()

            val = get_position(lists, "[SAMBASHARE]")
            lists[val + 1] = "path = " + "/home/" + sudo_username + "/Shared\n"

            print("You have choosen to install Samba with an example share")
            print("We have added a folder called 'Shared' to your home directory")
            print("You can access this folder from any computer in your network")
            print("You can write and remove items from the shared folder")
            print("Reboot or restart smb first")
            print(lists[val + 1])

            with open(samba_config, "w", encoding="utf-8") as f:
                f.writelines(lists)
                f.close()
        except Exception as error:
            print(error)

    if choice == "usershares":
        # make folder
        if not path.isdir("/var/lib/samba/usershares"):
            makedirs("/var/lib/samba/usershares", 0o770)

        # create system sambashare group
        try:
            if check_group("sambashare"):
                pass
            else:
                try:
                    command = "groupadd -r sambashare"
                    subprocess.call(
                        command.split(" "),
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                except Exception as error:
                    print(error)

        except Exception as error:
            print(error)

        # add user to group
        try:
            command = "gpasswd -a " + sudo_username + " sambashare"
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as error:
            print(error)

        try:
            command = "chown root:sambashare /var/lib/samba/usershares"
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as error:
            print(error)

        try:
            command = "chmod 1770 /var/lib/samba/usershares"
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as error:
            print(error)


# =====================================================
#               SAMBA EDIT
# =====================================================


# samba advanced - TODO
def save_samba_config(self):
    # create smb.conf if there is none?
    if path.isfile(samba_config):
        if not path.isfile(samba_config + ".bak"):
            shutil.copy(samba_config, samba_config + ".bak")
        try:
            with open(samba_config, "r", encoding="utf-8") as f:
                lists = f.readlines()
                f.close()

            path = self.entry_path.get_text()
            browseable = self.samba_share_browseable.get_active()
            if browseable:
                browseable = "yes"
            else:
                browseable = "no"
            guest = self.samba_share_guest.get_active()
            if guest:
                guest = "yes"
            else:
                guest = "no"
            public = self.samba_share_public.get_active()
            if public:
                public = "yes"
            else:
                public = "no"
            writable = self.samba_share_writable.get_active()
            if writable:
                writable = "yes"
            else:
                writable = "no"

            val = get_position(lists, "[SAMBASHARE]")
            if lists[val] == ";[SAMBASHARE]\n":
                lists[val] = "[SAMBASHARE]" + "\n"
            lists[val + 1] = "path = " + path + "\n"
            lists[val + 2] = "browseable  = " + browseable + "\n"
            lists[val + 3] = "guest ok = " + guest + "\n"
            lists[val + 4] = "public = " + public + "\n"
            lists[val + 5] = "writable = " + writable + "\n"

            print("These lines have been saved at the end of /etc/samba/smb.conf")
            print("Edit this file to add more shares")
            print(lists[val])
            print(lists[val + 1])
            print(lists[val + 2])
            print(lists[val + 3])
            print(lists[val + 4])
            print(lists[val + 5])

            with open(samba_config, "w", encoding="utf-8") as f:
                f.writelines(lists)
                f.close()

            print("Smb.conf has been saved")
            show_in_app_notification(self, "Smb.conf has been saved")
        except:
            pass
    else:
        print(
            "Choose or create your own smb.conf in /etc/samba/smb.conf then change settings"
        )
        show_in_app_notification(self, "Choose or create your own smb.conf")


# =====================================================
#                       SDDM
# =====================================================


def create_sddm_k_dir():
    if not path.isdir(sddm_default_d2_dir):
        try:
            mkdir(sddm_default_d2_dir)
        except Exception as error:
            print(error)


# =====================================================
#                       SHELL
# =====================================================


def source_shell(self):
    process = subprocess.run(
        ["sh", "-c", 'echo "$SHELL"'], check=True, stdout=subprocess.PIPE
    )

    output = process.stdout.decode().strip()
    if output == "/bin/bash":
        subprocess.run(
            [
                "bash",
                "-c",
                "su - " + sudo_username + ' -c "source ' + home + '/.bashrc"',
            ],
            check=True,
            stdout=subprocess.PIPE,
        )
    elif output == "/bin/zsh":
        subprocess.run(
            ["zsh", "-c", "su - " + sudo_username + ' -c "source ' + home + '/.zshrc"'],
            check=True,
            stdout=subprocess.PIPE,
        )
    elif output == "/usr/bin/fish":
        subprocess.run(
            [
                "fish",
                "-c",
                "su - "
                + sudo_username
                + ' -c "source '
                + home
                + '/.config/fish/config.fish"',
            ],
            check=True,
            stdout=subprocess.PIPE,
        )


def get_shell():
    try:
        process = subprocess.run(
            ["su", "-", sudo_username, "-c", 'echo "$SHELL"'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output = process.stdout.decode().strip().strip("\n")
        if output in ("/bin/bash", "/usr/bin/bash"):
            return "bash"
        elif output in ("/bin/zsh", "/usr/bin/zsh"):
            return "zsh"
        elif output in ("/bin/fish", "/usr/bin/fish"):
            return "fish"
    except Exception as error:
        print(error)


def run_as_user(script):
    subprocess.call(["su - " + sudo_username + " -c " + script], shell=False)

# =====================================================
#               THUNAR SHARE PLUGIN
# =====================================================


def install_arco_thunar_plugin(self, widget):
    # install = "pacman -S thunar arcolinux-thunar-shares-plugin --noconfirm"
    install = "pacman -S thunar thunar-shares-plugin --noconfirm"

    if check_package_installed("thunar-shares-plugin"):
        print("Thunar-shares-plugin is already installed")
    else:
        try:
            subprocess.call(
                install.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print("Thunar-shares-plugin is now installed - reboot")
            GLib.idle_add(
                self.label7.set_text,
                "Thunar-shares-plugin is now installed - reboot",
            )
            print("Other apps that might be interesting for sharing are :")
            print(" - nemo-share (cinnamon)")
            print(" - caja-share (mate)")
            print(" - nautilus-share (gnome - budgie)")
            print(" - kdenetwork-filesharing (plasma)")

        except Exception as error:
            print(error)


# =====================================================
#               UBLOCK ORIGIN
# =====================================================


def ublock_get_state(self):
    if path.exists("/usr/lib/firefox/browser/extensions/uBlock0@raymondhill.net.xpi"):
        return True
    return False


def set_firefox_ublock(self, toggle, state):
    GLib.idle_add(toggle.set_sensitive, False)
    GLib.idle_add(self.label7.set_visible, True)
    GLib.idle_add(self.progress.set_visible, True)
    GLib.idle_add(self.label7.set_text, "Run..")
    GLib.idle_add(self.progress.set_fraction, 0.2)

    timeout_id = None
    timeout_id = GLib.timeout_add(100, do_pulse, None, self.progress)

    try:
        install_ublock = "pacman -S firefox-ublock-origin --needed --noconfirm"
        uninstall_ublock = "pacman -Rs firefox-ublock-origin --noconfirm"

        if state:
            GLib.idle_add(self.label7.set_text, "Installing ublock Origin...")
            subprocess.call(
                install_ublock.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        else:
            GLib.idle_add(self.label7.set_text, "Removing ublock Origin...")
            subprocess.call(
                uninstall_ublock.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        GLib.idle_add(self.label7.set_text, "Complete")
        GLib.source_remove(timeout_id)
        timeout_id = None
        GLib.idle_add(self.progress.set_fraction, 0)

        GLib.idle_add(toggle.set_sensitive, True)
        if state:
            GLib.idle_add(self.label7.set_text, "uBlock Origin installed")
        else:
            GLib.idle_add(self.label7.set_text, "uBlock Origin removed")
        GLib.idle_add(self.label7.set_visible, False)
        GLib.idle_add(self.progress.set_visible, False)

    except Exception as error:
        messagebox(self, "ERROR!!", str(error))
        print(error)


# ====================================================================
#                      UPDATE REPOS
# ====================================================================


def update_repos(self):
    try:
        command = "pacman -Sy"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception as error:
        print(error)

# =====================================================
#               THREADING
# =====================================================

# check if the named thread is running
def is_thread_alive(thread_name):
    for thread in threading.enumerate():
        if thread.name == thread_name and thread.is_alive():
            return True

    return False


# =====================================================
#               MONITOR PACMAN LOG FILE
# =====================================================

# write lines from the pacman log onto a queue, this is called from a non-blocking thread
def _add_pacmanlog_queue(self):
    try:
        lines = []
        with open(pacman_logfile, "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                if line:
                    # encode in utf-8
                    # this fixes Gtk-CRITICAL **: gtk_text_buffer_emit_insert:
                    # assertion 'g_utf8_validate (text, len, NULL)' failed
                    lines.append(line.encode("utf-8"))
                    self.pacmanlog_queue.put(lines)
                else:
                    time.sleep(0.5)

    except Exception as e:
        logger.error("Exception in add_pacmanlog_queue() : %s" % e)
    finally:
        logger.debug("No new lines found inside the pacman log file")


# un-used code


# start log timer to update the textview called from a non-blocking thread
def _start_log_timer(self, textbuffer_pacmanlog, textview_pacmanlog):
    while True:
        # once the pacman process has completed, do not keep updating the textview, so break out the loop
        if self.start_logtimer is False:
            break

        GLib.idle_add(
            _update_textview_pacmanlog,
            self,
            textbuffer_pacmanlog,
            textview_pacmanlog,
            priority=GLib.PRIORITY_DEFAULT,
        )
        time.sleep(2)


# un-used code

# update the textview component with new lines from the pacman log file
# To fix: Gtk-CRITICAL **: gtk_text_buffer_emit_insert: assertion 'g_utf8_validate (text, len, NULL)' failed
# Make sure the line read from the pacman log file is encoded in utf-8
# Then decode the line when inserting inside the buffer


def _update_textview_pacmanlog(self, textbuffer_pacmanlog, textview_pacmanlog):
    lines = self.pacmanlog_queue.get()

    try:
        if len(lines) > 0:
            end_iter = textbuffer_pacmanlog.get_end_iter()
            for line in lines:
                if len(line) > 0:
                    textbuffer_pacmanlog.insert(
                        end_iter,
                        line.decode("utf-8"),
                        len(line),
                    )

    except Exception as e:
        logger.error("Exception in update_textview_pacmanlog() : %s" % e)
    finally:
        self.pacmanlog_queue.task_done()

        if len(lines) > 0:
            text_mark_end = textbuffer_pacmanlog.create_mark(
                "END", textbuffer_pacmanlog.get_end_iter(), False
            )
            # auto-scroll the textview to the bottom as new content is added

            textview_pacmanlog.scroll_mark_onscreen(text_mark_end)

        lines.clear()


# update textview with pacman progress
def update_progress_textview(self, line):
    try:
        if len(line) > 0:
            self.textbuffer.insert(
                self.textbuffer.get_end_iter(),
                " %s" % line,
                len(" %s" % line),
            )

    except Exception as e:
        logger.error("Exception in update_progress_textview(): %s" % e)
    finally:
        self.messages_queue.task_done()
        text_mark_end = self.textbuffer.create_mark(
            "end", self.textbuffer.get_end_iter(), False
        )
        # scroll to the end of the textview
        self.textview.scroll_mark_onscreen(text_mark_end)


# update the package install status label called from outside the main thread
def update_package_status_label(label, text):
    label.set_markup(text)


# check if the pacman lock file exists on the system
def check_pacman_lockfile():
    return os.path.exists(pacman_lockfile)


# keep track of messages added to the queue, and updates the textview in almost realtime
def monitor_messages_queue(self):
    try:
        while True:
            message = self.messages_queue.get()
            GLib.idle_add(
                update_progress_textview,
                self,
                message,
                priority=GLib.PRIORITY_DEFAULT,
            )
    except Exception as e:
        logger.error("Exception in monitor_messages_queue(): %s" % e)


# =====================================================
#        AUR HELPER & TERMINAL LAUNCH UTILITIES
# =====================================================

def wait_install_and_update(process, binary_path, label_widget, installed_markup, self_ref, notification, package_name=None):
    def _wait():
        try:
            print(f"\n[INFO] wait_install_and_update() started for package: {package_name}")
            print(f"[INFO] Binary path: {binary_path}")
            print(f"[INFO] Waiting for process to complete...")
            process.communicate()
            time.sleep(1)

            error_output = ""
            if hasattr(process, 'temp_file') and process.temp_file:
                try:
                    print(f"[INFO] Reading temp file: {process.temp_file}")
                    with open(process.temp_file, 'r') as f:
                        error_output = f.read()
                    print(f"[INFO] Temp file contents: {len(error_output)} bytes")
                    import os as os_module
                    os_module.unlink(process.temp_file)
                except Exception as e:
                    print(f"[INFO] Error reading temp file: {e}")

            if path.exists(binary_path):
                print(f"[INFO] Binary exists at {binary_path}, installation successful")
                if label_widget:
                    GLib.idle_add(label_widget.set_markup, installed_markup)
                GLib.idle_add(show_in_app_notification, self_ref, notification)
            else:
                print(f"[INFO] Binary NOT found at {binary_path}, checking for errors...")
                print(f"[INFO] Total error output length: {len(error_output)} bytes")
                if package_name:
                    print(f"[INFO] Calling check_missing_repo_error with package: {package_name}")
                    check_missing_repo_error(self_ref, error_output, package_name)
                else:
                    print(f"[INFO] No package_name provided, skipping error check")
        except Exception as e:
            print(f"[ERROR] Exception in wait_install_and_update: {e}")
            import traceback
            traceback.print_exc()
    threading.Thread(target=_wait, daemon=True).start()


def wait_remove_and_update(process, binary_path, label_widget, plain_markup, self_ref, notification):
    def _wait():
        try:
            print(f"\n[INFO] wait_remove_and_update() started")
            print(f"[INFO] Binary path to check: {binary_path}")
            print(f"[INFO] Waiting for removal process to complete...")
            stdout_data, stderr_data = process.communicate()
            print(f"[INFO] Process completed")
            print(f"[INFO] Captured output: stdout={len(stdout_data) if stdout_data else 0} bytes, stderr={len(stderr_data) if stderr_data else 0} bytes")
            time.sleep(1)

            error_output = ""
            if hasattr(process, 'temp_file') and process.temp_file:
                try:
                    print(f"[INFO] Reading output from temp file: {process.temp_file}")
                    with open(process.temp_file, 'r') as f:
                        error_output = f.read()
                    print(f"[INFO] Temp file size: {len(error_output)} bytes")
                    print(f"[INFO] Parsing output for errors...")
                    import os as os_module
                    os_module.unlink(process.temp_file)
                    print(f"[INFO] Cleaned up temp file")
                except Exception as e:
                    print(f"[INFO] Could not read temp file: {e}")

            print(f"[INFO] Checking if binary still exists at: {binary_path}")
            if not path.exists(binary_path):
                print(f"[INFO] ✓ Binary successfully removed from {binary_path}")
                print(f"[INFO] Updating UI and showing notification")
                GLib.idle_add(label_widget.set_markup, plain_markup)
                GLib.idle_add(show_in_app_notification, self_ref, notification)
                print(f"[INFO] {notification}")
            else:
                print(f"[INFO] ✗ Binary still exists at {binary_path}")
                print(f"[INFO] Removal may have failed or encountered issues")
        except Exception as e:
            print(f"[ERROR] Exception in wait_remove_and_update: {e}")
            import traceback
            traceback.print_exc()
    threading.Thread(target=_wait, daemon=True).start()


def wait_and_notify(process, self_ref, notification):
    def _wait():
        try:
            process.communicate()
            import os as os_module
            if hasattr(process, 'temp_file') and process.temp_file:
                try:
                    os_module.unlink(process.temp_file)
                except Exception:
                    pass
            print(f"[INFO] {notification}")
            GLib.idle_add(show_in_app_notification, self_ref, notification)
        except Exception as e:
            print(f"[ERROR] Exception in wait_and_notify: {e}")
    threading.Thread(target=_wait, daemon=True).start()


def get_aur_helper():
    for helper in ["yay", "paru", "trizen", "pikaur"]:
        if path.exists("/usr/bin/" + helper):
            return helper
    return None


def ensure_firefox_installed():
    import shutil
    if not shutil.which("firefox"):
        print("[INFO] Firefox not found, installing...")
        install_proc = subprocess.run(["pacman", "-S", "--noconfirm", "--needed", "firefox"],
                                     capture_output=True, text=True)
        if install_proc.returncode != 0:
            print(f"[ERROR] Failed to install Firefox: {install_proc.stderr}")
            return False
    return True


def ensure_nodejs_installed():
    import time

    npm_paths = ["/usr/bin/npm", "/usr/local/bin/npm"]
    for npm_path in npm_paths:
        if path.exists(npm_path):
            return True

    print("[INFO] Node.js not found, installing...")
    install_proc = subprocess.run(["pacman", "-S", "--noconfirm", "--needed", "nodejs", "npm"],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print(f"[DEBUG] pacman stdout: {install_proc.stdout}")
    print(f"[DEBUG] pacman stderr: {install_proc.stderr}")
    print(f"[DEBUG] pacman returncode: {install_proc.returncode}")

    time.sleep(2)

    for npm_path in npm_paths:
        if path.exists(npm_path):
            print("[INFO] Node.js installed successfully")
            return True

    print("[ERROR] Node.js/npm installation failed - npm not found in common paths")
    return False


def ensure_git_installed():
    import shutil
    import time

    if shutil.which("git"):
        return True

    print("[INFO] Git not found, installing...")
    install_proc = subprocess.run(["pacman", "-S", "--noconfirm", "--needed", "git"],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if install_proc.returncode != 0:
        print(f"[ERROR] Failed to install Git: {install_proc.stderr}")
        return False

    time.sleep(1)

    if shutil.which("git"):
        print("[INFO] Git installed successfully")
        return True
    else:
        print("[ERROR] Git installed but not found in PATH")
        return False


def launch_pacman_install_in_terminal(packages):
    import tempfile
    import shutil

    if not shutil.which("alacritty"):
        print("[INFO] alacritty not found, installing...")
        install_proc = subprocess.run(["pacman", "-S", "--noconfirm", "--needed", "alacritty"],
                                     capture_output=True, text=True)
        if install_proc.returncode != 0:
            print(f"[ERROR] Failed to install alacritty: {install_proc.stderr}")
            return None

    temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.log')
    temp_path = temp_file.name
    temp_file.close()

    script = f"""
set -o pipefail
pacman -S --noconfirm --needed {packages} 2>&1 | tee {temp_path}
RESULT=$?

echo ''
if [ $RESULT -eq 0 ]; then
    echo '✓ Installation successful'
else
    echo '✗ Installation failed'
    if grep -q 'target not found' {temp_path}; then
        REPO="chaotic-aur"
        NEMESIS_FILE="/usr/share/archlinux-tweak-tool/data/nemesis_packages.txt"

        # Check if package is in nemesis_repo
        if [ -f "$NEMESIS_FILE" ]; then
            if grep -q "^{packages}$" "$NEMESIS_FILE"; then
                REPO="nemesis_repo"
            fi
        fi

        echo ''
        echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        echo 'REASON: Missing repository'
        echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        echo 'SOLUTION:'
        echo ". Enable $REPO in /etc/pacman.conf"
        echo ". Try again in the ATT"
        echo ". Or run: pacman -Sy {packages}"
        echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
    fi
fi

echo ''
echo '=== Operation Finished ==='
echo 'You can close this window'
read -p 'Press Enter to close...'
"""
    print(f"[INFO] Launching pacman install with output to: {temp_path}")
    process = subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.temp_file = temp_path
    return process


def launch_pacman_remove_in_terminal(packages):
    import tempfile
    import shutil

    if not shutil.which("alacritty"):
        print("[INFO] alacritty not found, installing...")
        install_proc = subprocess.run(["pacman", "-S", "--noconfirm", "--needed", "alacritty"],
                                     capture_output=True, text=True)
        if install_proc.returncode != 0:
            print(f"[ERROR] Failed to install alacritty: {install_proc.stderr}")
            return None

    temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.log')
    temp_path = temp_file.name
    temp_file.close()

    script = f"""
set -o pipefail
pacman -Rs --noconfirm {packages} 2>&1 | tee {temp_path}
RESULT=$?

echo ''
if [ $RESULT -eq 0 ]; then
    echo '✓ Removal successful'
else
    echo '✗ Removal failed'
    if grep -q 'target not found' {temp_path}; then
        echo ''
        echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        echo 'REASON: Package might be removed already'
        echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        echo 'SOLUTION:'
        echo '. Check if package is installed: pacman -Q {packages}'
        echo '. Try manual removal: pacman -R {packages}'
        echo '. For dependencies: pacman -Rdd {packages}'
        echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
    elif grep -qE 'error:|failed' {temp_path}; then
        echo ''
        echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        echo 'REASON: Package might be removed already'
        echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        echo 'SOLUTION:'
        echo '. Check if package is installed: pacman -Q {packages}'
        echo '. Try manual removal: pacman -R {packages}'
        echo '. For dependencies: pacman -Rdd {packages}'
        echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
    fi
fi

echo ''
echo '=== Operation Finished ==='
echo 'You can close this window'
read -p 'Press Enter to close...'
"""
    print(f"[INFO] Launching pacman remove with output to: {temp_path}")
    process = subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.temp_file = temp_path
    return process


def launch_aur_install_in_terminal(aur_helper, package, username=None):
    import shutil
    if not shutil.which("alacritty"):
        print("[INFO] alacritty not found, installing...")
        install_proc = subprocess.run(["pacman", "-S", "--noconfirm", "--needed", "alacritty"],
                                     capture_output=True, text=True)
        if install_proc.returncode != 0:
            print(f"[ERROR] Failed to install alacritty: {install_proc.stderr}")
            return None
    if username is None:
        username = sudo_username
    script = f"sudo -u {username} {aur_helper} -S --noconfirm {package}; echo ''; echo '=== Installation complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
    return subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def launch_aur_remove_in_terminal(aur_helper, package, username=None):
    import shutil
    if not shutil.which("alacritty"):
        print("[INFO] alacritty not found, installing...")
        install_proc = subprocess.run(["pacman", "-S", "--noconfirm", "--needed", "alacritty"],
                                     capture_output=True, text=True)
        if install_proc.returncode != 0:
            print(f"[ERROR] Failed to install alacritty: {install_proc.stderr}")
            return None
    if username is None:
        username = sudo_username
    script = f"sudo -u {username} {aur_helper} -Rs --noconfirm {package}; echo ''; echo '=== Removal complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
    return subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def launch_npm_install_in_terminal(npm_package):
    import shutil
    if not shutil.which("alacritty"):
        print("[INFO] alacritty not found, installing...")
        install_proc = subprocess.run(["pacman", "-S", "--noconfirm", "--needed", "alacritty"],
                                     capture_output=True, text=True)
        if install_proc.returncode != 0:
            print(f"[ERROR] Failed to install alacritty: {install_proc.stderr}")
            return None
    if not ensure_nodejs_installed():
        print("[ERROR] Node.js installation failed")
        return None
    script = f"/usr/bin/npm install -g {npm_package}; echo ''; echo '=== Installation complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
    return subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def launch_npm_remove_in_terminal(npm_package):
    import shutil
    if not shutil.which("alacritty"):
        print("[INFO] alacritty not found, installing...")
        install_proc = subprocess.run(["pacman", "-S", "--noconfirm", "--needed", "alacritty"],
                                     capture_output=True, text=True)
        if install_proc.returncode != 0:
            print(f"[ERROR] Failed to install alacritty: {install_proc.stderr}")
            return None
    if not ensure_nodejs_installed():
        print("[ERROR] Node.js installation failed")
        return None
    script = f"/usr/bin/npm uninstall -g {npm_package}; echo ''; echo '=== Removal complete ===' && echo 'You can close this window' && read -p 'Press Enter to close...'"
    return subprocess.Popen(["alacritty", "-e", "bash", "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
