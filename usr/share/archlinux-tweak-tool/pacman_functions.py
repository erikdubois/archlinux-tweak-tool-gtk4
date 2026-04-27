# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn


def append_repo(self, text):
    """Append a new repo"""
    with open(fn.pacman, "a", encoding="utf-8") as myfile:
        myfile.write("\n\n")
        myfile.write(text)

    fn.show_in_app_notification(self, "Settings Saved Successfully")


def append_mirror(self, text):
    """Append a new mirror"""
    with open(fn.arcolinux_mirrorlist, "a", encoding="utf-8") as myfile:
        myfile.write("\n\n")
        myfile.write(text)

    fn.show_in_app_notification(self, "Settings Saved Successfully")


def insert_repo(self, text):
    """insert a repo"""
    with open(fn.pacman, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()
    pos = fn.get_position(lines, "[custom]")
    num = pos + 3

    lines.insert(num, "\n" + text + "\n")

    with open(fn.pacman, "w", encoding="utf-8") as f:
        f.writelines(lines)
        f.close()


def check_repo(value):
    """check if repo is there and active"""
    with open(fn.pacman, "r", encoding="utf-8") as myfile:
        lines = myfile.readlines()
        myfile.close()

    for line in lines:
        if value in line:
            if "#" + value in line:
                return False
            else:
                return True
    return False


def check_mirror(value):
    """check if mirror is there and active"""
    with open(fn.arcolinux_mirrorlist, "r", encoding="utf-8") as myfile:
        lines = myfile.readlines()
        myfile.close()

    for line in lines:
        if value in line:
            if "#" + value in line:
                return False
            else:
                return True
    return False


def repo_exist(value):
    """check repo_exists"""
    with open(fn.pacman, "r", encoding="utf-8") as myfile:
        lines = myfile.readlines()
        myfile.close()

    for line in lines:
        if value in line:
            return True
    return False


def mirror_exist(value):
    """check mirror exists"""
    with open(fn.arcolinux_mirrorlist, "r", encoding="utf-8") as myfile:
        lines = myfile.readlines()
        myfile.close()

    for line in lines:
        if value in line:
            return True
    return False


def pacman_on(repo, lines, i, line):
    """set pacman on a given repo"""
    if repo in line:
        lines[i] = line.replace("#", "")
        if (i + 1) < len(lines):
            lines[i + 1] = lines[i + 1].replace("#", "")
        if (i + 2) < len(lines) and "Server" in lines[i + 2]:
            lines[i + 2] = lines[i + 2].replace("#", "")


def mirror_on(mirror, lines, i, line):
    """set mirror on"""
    if mirror in line:
        lines[i] = line.replace("#", "")
        if (i + 1) < len(lines):
            lines[i + 1] = lines[i + 1].replace("#", "")
        if (i + 2) < len(lines) and "Server" in lines[i + 2]:
            lines[i + 2] = lines[i + 2].replace("#", "")


def pacman_off(repo, lines, i, line):
    """set pacman off"""
    if repo in line:
        if "#" not in lines[i]:
            lines[i] = line.replace(lines[i], "#" + lines[i])
        if (i + 1) < len(lines):
            if "#" not in lines[i + 1]:
                lines[i + 1] = lines[i + 1].replace(lines[i + 1], "#" + lines[i + 1])
        if (i + 2) < len(lines) and "Server" in lines[i + 2]:
            if "#" not in lines[i + 2]:
                lines[i + 2] = lines[i + 2].replace(lines[i + 2], "#" + lines[i + 2])


def mirror_off(mirror, lines, i, line):
    """set mirror off"""
    if mirror in line:
        if "#" not in lines[i]:
            lines[i] = line.replace(lines[i], "#" + lines[i])


def spin_on(repo, lines, i, line):
    """set spin on repo"""
    if repo in line:
        lines[i] = line.replace("#", "")
        if (i + 1) < len(lines):
            lines[i + 1] = lines[i + 1].replace("#", "")
        if (i + 2) < len(lines):
            lines[i + 2] = lines[i + 2].replace("#", "")


def spin_off(repo, lines, i, line):
    """set spin off"""
    if repo in line:
        if "#" not in lines[i]:
            lines[i] = line.replace(lines[i], "#" + lines[i])
        if (i + 1) < len(lines):
            if "#" not in lines[i + 1]:
                lines[i + 1] = lines[i + 1].replace(lines[i + 1], "#" + lines[i + 1])
        if (i + 2) < len(lines):
            if "#" not in lines[i + 2]:
                lines[i + 2] = lines[i + 2].replace(lines[i + 2], "#" + lines[i + 2])


def toggle_test_repos(self, state, widget):
    """toggle test repo"""
    if not fn.os.path.isfile(fn.pacman + ".bak"):
        fn.shutil.copy(fn.pacman, fn.pacman + ".bak")
    lines = ""
    if state is True:
        with open(fn.pacman, "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
        try:
            # TODO enumerate
            for i in range(0, len(lines)):
                line = lines[i]
                if widget == "chaotics":
                    spin_on("[chaotic-aur]", lines, i, line)
                if widget == "nemesis":
                    spin_on("[nemesis_repo]", lines, i, line)
                if widget == "testing":
                    pacman_on("[core-testing]", lines, i, line)
                if widget == "core":
                    pacman_on("[core]", lines, i, line)
                if widget == "extra":
                    pacman_on("[extra]", lines, i, line)
                if widget == "community-testing":
                    pacman_on("[extra-testing]", lines, i, line)
                if widget == "community":
                    pacman_on("[extra-testing]", lines, i, line)
                if widget == "multilib-testing":
                    pacman_on("[multilib-testing]", lines, i, line)
                if widget == "multilib":
                    pacman_on("[multilib]", lines, i, line)

            with open(fn.pacman, "w", encoding="utf-8") as f:
                # lines = f.readlines()
                f.writelines(lines)
                f.close()
        except Exception as error:
            print(error)
            fn.messagebox(
                self,
                "ERROR!!",
                "An error has occurred setting this setting 'toggle_test_repos On'",
            )
    else:
        with open(fn.pacman, "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
        try:
            # TODO enumerate
            for i in range(0, len(lines)):
                line = lines[i]
                if widget == "chaotics":
                    spin_off("[chaotic-aur]", lines, i, line)
                if widget == "nemesis":
                    spin_off("[nemesis_repo]", lines, i, line)
                if widget == "testing":
                    pacman_off("[core-testing]", lines, i, line)
                if widget == "core":
                    pacman_off("[core]", lines, i, line)
                if widget == "extra":
                    pacman_off("[extra]", lines, i, line)
                if widget == "community-testing":
                    pacman_off("[extra-testing]", lines, i, line)
                if widget == "community":
                    pacman_off("[extra-testing]", lines, i, line)
                if widget == "multilib-testing":
                    pacman_off("[multilib-testing]", lines, i, line)
                if widget == "multilib":
                    pacman_off("[multilib]", lines, i, line)

            with open(fn.pacman, "w", encoding="utf-8") as f:
                f.writelines(lines)
                f.close()
        except:
            fn.messagebox(
                self,
                "ERROR!!",
                "An error has occurred setting this setting 'toggle_test_repos Off'",
            )

# ============================================================
# AUR Helper Management
# ============================================================


def check_aur_helper():
    """Check which AUR helper is installed (yay or paru)."""
    if fn.path.exists("/usr/bin/yay"):
        return "yay"
    elif fn.path.exists("/usr/bin/paru"):
        return "paru"
    return None


def is_chaotic_aur_enabled():
    """Check if chaotic-aur repository is enabled in pacman.conf."""
    return check_repo("[chaotic-aur]")


def install_yay_pacman(self):
    """Install yay-git from chaotic-aur repository."""
    print("\n[INFO] Installing yay-git from chaotic-aur")
    fn.show_in_app_notification(self, "Opening terminal to install yay-git")
    fn.subprocess.Popen(
        ["alacritty", "-e", "bash", "-c", "sudo pacman -S yay-git; read -p 'Press Enter to exit...'"],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )


def install_yay_git(self):
    """Install yay-git from source in a terminal window. Returns the Popen process."""
    print("\n[INFO] Installing yay-git from source (git)")
    fn.install_package(self, "alacritty base-devel git")
    build_script = "/usr/share/archlinux-tweak-tool/data/any/build-yay-git"
    return fn.subprocess.Popen(
        ["alacritty", "--hold", "-e", build_script, fn.sudo_username],
        shell=False,
    )


def install_paru_pacman(self):
    """Install paru-git from chaotic-aur repository."""
    print("\n[INFO] Installing paru-git from chaotic-aur")
    fn.show_in_app_notification(self, "Opening terminal to install paru-git")
    fn.subprocess.Popen(
        ["alacritty", "-e", "bash", "-c", "sudo pacman -S paru-git; read -p 'Press Enter to exit...'"],
        stdout=fn.subprocess.PIPE,
        stderr=fn.subprocess.PIPE,
    )


def install_paru_git(self):
    """Install paru-git from source in a terminal window. Returns the Popen process."""
    print("\n[INFO] Installing paru-git from source (git)")
    fn.install_package(self, "alacritty base-devel git")
    build_script = "/usr/share/archlinux-tweak-tool/data/any/build-paru-git"
    return fn.subprocess.Popen(
        ["alacritty", "--hold", "-e", build_script, fn.sudo_username],
        shell=False,
    )


def remove_aur_helper(self, binary):
    """Remove yay or paru by detecting the package that owns the binary."""
    try:
        print(f"\n[INFO] Removing {binary}")
        result = fn.subprocess.check_output(
            ["pacman", "-Qo", f"/usr/bin/{binary}"],
            stderr=fn.subprocess.STDOUT,
        ).decode().strip()
        # output: "/usr/bin/yay is owned by yay-git 12.1.0-1"
        pkg = result.split(" is owned by ")[1].split(" ")[0]
        print(f"[INFO] Found package: {pkg}")
        fn.show_in_app_notification(self, f"Opening terminal to remove {pkg}")
        fn.subprocess.Popen(
            ["alacritty", "-e", "bash", "-c", f"sudo pacman -R {pkg}; read -p 'Press Enter to exit...'"],
            stdout=fn.subprocess.PIPE,
            stderr=fn.subprocess.PIPE,
        )
    except Exception as e:
        print(f"[INFO] Could not find package owning {binary}: {e}")
        fn.show_in_app_notification(self, f"Could not find package owning {binary}")
