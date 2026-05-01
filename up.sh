#!/bin/bash
#set -e
##################################################################################################################
# Author    : Erik Dubois
# Website   : https://www.erikdubois.be
##################################################################################################################
#
#   DO NOT JUST RUN THIS. EXAMINE AND JUDGE. RUN AT YOUR OWN RISK.
#
##################################################################################################################
#tput setaf 0 = black
#tput setaf 1 = red
#tput setaf 2 = green
#tput setaf 3 = yellow
#tput setaf 4 = dark blue
#tput setaf 5 = purple
#tput setaf 6 = cyan
#tput setaf 7 = gray
#tput setaf 8 = light blue
##################################################################################################################

workdir=$(pwd)

./chaotic

# reset - commit your changes or stash them before you merge
# git reset --hard - personal alias - grh

# Generate nemesis_packages.txt from nemesis_repo
echo "Generating nemesis_packages.txt from nemesis_repo..."
python3 << 'PYEOF' > $workdir/usr/share/archlinux-tweak-tool/data/nemesis_packages.txt
import re
import os

repo_dir = "/home/erik/EDU/nemesis_repo/x86_64/"
packages = set()

for filename in os.listdir(repo_dir):
    if filename.endswith('.pkg.tar.zst'):
        match = re.match(r'^(.+?)-([^-]+-[^-]+)-(x86_64|any)\.pkg\.tar\.zst$', filename)
        if match:
            pkg_name = match.group(1)
            packages.add(pkg_name)

for pkg in sorted(packages):
    print(pkg)
PYEOF
echo "nemesis_packages.txt generated successfully"

if [[ -f "./repo.sh" ]]; then
    echo "Found repo.sh, running it..."
    bash ./repo.sh
fi

# ── Kernel availability check ────────────────────────────────
echo "Checking kernel availability in repos..."
python3 << 'PYEOF'
import sys, subprocess
sys.path.insert(0, "usr/share/archlinux-tweak-tool")
from kernel import KERNELS

missing = []
for k in KERNELS:
    pkg = k["pkg"]
    r = subprocess.run(["pacman", "-Si", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if r.returncode != 0:
        missing.append((pkg, k.get("requires_chaotic", False)))

if missing:
    print("\033[1;33mMissing kernels — update kernel.py:\033[0m")
    for pkg, chaotic in missing:
        src = "chaotic-aur" if chaotic else "Arch repos"
        print(f"  \033[1;31m✗  {pkg}  ({src})\033[0m")
else:
    print("\033[1;32m✓  All kernels present in repos\033[0m")
PYEOF

echo "getting latest .bashrc"
wget https://raw.githubusercontent.com/erikdubois/edu-shells/refs/heads/main/etc/skel/.bashrc-latest -O $workdir/usr/share/archlinux-tweak-tool/data/.bashrc

echo "getting latest .zshrc"
wget https://raw.githubusercontent.com/erikdubois/edu-shells/refs/heads/main/etc/skel/.zshrc -O $workdir/usr/share/archlinux-tweak-tool/data/.zshrc

echo "getting latest config.fish"
wget https://raw.githubusercontent.com/erikdubois/edu-shells/refs/heads/main/etc/skel/.config/fish/config.fish -O $workdir/usr/share/archlinux-tweak-tool/data/config.fish

########### Arch Linux
echo "getting archlinux keyring"
rm $workdir/usr/share/archlinux-tweak-tool/data/kiro/packages/keyring/*
#get latest archlinux-keyring
wget https://archlinux.org/packages/core/any/archlinux-keyring/download --content-disposition -P $workdir/usr/share/archlinux-tweak-tool/data/packages/keyring/

# Below command will backup everything inside the project folder
git add --all .

git commit -m "update"

# Push the local files to github

if grep -q main .git/config; then
	echo "Using main"
		git push -u origin main
fi

if grep -q master .git/config; then
	echo "Using master"
		git push -u origin master
fi

echo "################################################################"
echo "###################    Git Push Done      ######################"
echo "################################################################"
