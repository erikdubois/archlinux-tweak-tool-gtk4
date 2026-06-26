#
# 40-aliases.fish — Kiro's alias library, grouped by purpose.
# Each alias has a short note so you know what it is for.
# Personal / dev-box aliases are kept commented at the very bottom.
#

# ── Navigation & typo guards ──────────────────────────────────────────────────
alias ..='cd ..'                  # go up one directory
alias ...='cd ../..'              # go up two directories
alias ....='cd ../../..'          # go up three directories
alias cd..='cd ..'                # typo guard for "cd.."
alias pdw='pwd'                   # typo guard for "pwd"
alias udpate='sudo pacman -Syyu'  # typo guard: misspelled "update"
alias upate='sudo pacman -Syyu'   # typo guard: misspelled "update"
alias updte='sudo pacman -Syyu'   # typo guard: misspelled "update"
alias updqte='sudo pacman -Syyu'  # typo guard: misspelled "update"

# ── Listing ───────────────────────────────────────────────────────────────────
alias la='ls -a'                       # list including hidden files
alias ll='ls -alFh'                    # long list, human sizes, all files
alias l='ls'                           # short alias for ls
alias l.="ls -A | grep -E '^\\.'"      # list only the hidden dotfiles
alias listdir='ls -d */ > list'        # write the folder names to a file named "list"
if type -q eza                         # prefer eza (modern ls) when installed
    alias ls='eza'                                                                      # plain listing via eza
    alias xls='eza -a --icons --color=always --group-directories-first'                 # all files, icons, dirs first
    alias xll='eza -lag --icons --color=always --group-directories-first --octal-permissions'  # long listing with octal perms
else if type -q exa                    # fall back to exa (older eza)
    alias ls='exa'                                                                      # plain listing via exa
    alias xls='exa -a --icons --color=always --group-directories-first'                 # all files, icons, dirs first
    alias xll='exa -lag --icons --color=always --group-directories-first --octal-permissions'  # long listing with octal perms
else
    alias ls='ls --color=auto'         # plain coloured ls when neither is installed
end

# ── grep / colour ─────────────────────────────────────────────────────────────
alias grep='grep --color=auto'    # highlight grep matches
alias egrep='egrep --color=auto'  # highlight extended-grep matches
alias fgrep='fgrep --color=auto'  # highlight fixed-string grep matches
alias ip='ip -color'              # colourised ip output

# ── Readable output ───────────────────────────────────────────────────────────
alias df='df -h'      # disk free space in human-readable sizes
alias free='free -mt' # memory usage in MB, with totals row

# ── Pacman / AUR ──────────────────────────────────────────────────────────────
alias sps='sudo pacman -S'                  # install a package
alias spr='sudo pacman -R'                  # remove a package
alias sprs='sudo pacman -Rs'                # remove a package and its unused deps
alias sprdd='sudo pacman -Rdd'              # force-remove, ignoring dependencies
alias spqo='sudo pacman -Qo'                # which package owns a file
alias spsii='sudo pacman -Sii'              # detailed info about a package
alias depends='function_depends'            # show what depends on a package
alias u='sudo pacman -Syyu'                 # full system update (force refresh)
alias update='sudo pacman -Syyu'            # full system update (force refresh)
alias upd='sudo pacman -Syu'                # system update (normal refresh)
alias upall='paru -Syu --noconfirm'         # update everything incl. AUR, no prompts
alias upa='paru -Syu --noconfirm'           # update everything incl. AUR, no prompts
alias upqll='paru -Syu --noconfirm'         # update everything incl. AUR, no prompts
alias upal='paru -Syu --noconfirm'          # update everything incl. AUR, no prompts
alias ua='paru -Syu --noconfirm'            # update everything incl. AUR, no prompts
alias paruskip='paru -S --mflags --skipinteg' # build AUR pkg, skip integrity checks
alias yayskip='yay -S --mflags --skipinteg'   # build AUR pkg via yay, skip integrity checks

# ── Package queries & maintenance ─────────────────────────────────────────────
alias unlock='sudo rm -f /var/lib/pacman/db.lck'            # clear a stuck pacman lock
alias pamac-unlock='sudo rm /var/tmp/pamac/dbs/db.lock'  # clear a stuck pamac lock
alias big='expac -H M "%m\t%n" | sort -h | nl'           # installed packages sorted by size
alias rip="expac --timefmt='%Y-%m-%d %T' '%l\t%n %v' | sort | tail -200 | nl"   # last 200 packages installed
alias riplong="expac --timefmt='%Y-%m-%d %T' '%l\t%n %v' | sort | tail -3000 | nl" # last 3000 packages installed
alias list='sudo pacman -Qqe'         # list explicitly installed packages
alias listt='sudo pacman -Qqet'       # list explicitly installed, no dependencies
alias listaur='sudo pacman -Qqem'     # list installed AUR/foreign packages
alias gitpkg='pacman -Q | grep -i "\-git"' # list installed -git (AUR) packages

# ── System info ───────────────────────────────────────────────────────────────
alias hw='hwinfo --short'                       # short hardware summary
alias cpu='cpuid -i | grep uarch | head -n 1'   # CPU microarchitecture
alias microcode='grep . /sys/devices/system/cpu/vulnerabilities/*' # CPU vulnerability status
alias howold='sudo lshw | grep -B 3 -A 8 BIOS'  # rough hardware age from the BIOS info
alias audio="pactl info | grep 'Server Name'"   # which audio server is running (pulse/pipewire)
alias probe='sudo kiro-probe'                   # Kiro system probe/report
alias sysfailed='systemctl list-units --failed' # show failed systemd units
alias whichvga='/usr/local/bin/kiro-which-vga'  # which graphics card is in use
alias kernel='ls /usr/lib/modules'              # installed kernels
alias kernels='ls /usr/lib/modules'             # installed kernels
alias xd='ls /usr/share/xsessions'              # available X11 desktop sessions
alias xdw='ls /usr/share/wayland-sessions'      # available Wayland desktop sessions
alias userlist='cut -d: -f1 /etc/passwd | sort' # list user accounts on the system
alias ff='fastfetch'                            # system info screen (fastfetch)
alias neo='neofetch'                            # system info screen (neofetch)

# ── Logs ──────────────────────────────────────────────────────────────────────
alias jctl='journalctl -p 3 -xb'    # show errors from the current boot
alias jclean='sudo journalctl --rotate && sudo journalctl --vacuum-time=1s' # wipe old journal logs
alias lcalamares='bat /var/log/Calamares.log'  # read the installer log
alias lpacman='bat /var/log/pacman.log'        # read the pacman log
alias lxorg='bat /var/log/Xorg.0.log'          # read the Xorg log
alias lxorgo='bat /var/log/Xorg.0.log.old'     # read the previous Xorg log

# ── Mirrors ───────────────────────────────────────────────────────────────────
alias mirror='sudo reflector -f 30 -l 30 --number 10 --verbose --save /etc/pacman.d/mirrorlist'                                    # rank 10 fastest mirrors
alias mirrord='sudo reflector --latest 30 --number 10 --sort delay --save /etc/pacman.d/mirrorlist'                                # 10 mirrors sorted by delay
alias mirrors='sudo reflector --latest 30 --number 10 --sort score --save /etc/pacman.d/mirrorlist'                               # 10 mirrors sorted by score
alias mirrora='sudo reflector --latest 30 --number 10 --sort age --save /etc/pacman.d/mirrorlist'                                  # 10 mirrors sorted by age
alias mirrorx='sudo reflector --age 6 --latest 20 --fastest 20 --threads 5 --sort rate --protocol https --save /etc/pacman.d/mirrorlist'   # https mirrors by rate (Kiro default)
alias mirrorxx='sudo reflector --age 6 --latest 20 --fastest 20 --threads 20 --sort rate --protocol https --save /etc/pacman.d/mirrorlist' # same, more threads
alias ram='rate-mirrors --allow-root --disable-comments arch | sudo tee /etc/pacman.d/mirrorlist'                                 # rank mirrors with rate-mirrors
alias rams='rate-mirrors --allow-root --disable-comments --protocol https arch | sudo tee /etc/pacman.d/mirrorlist'               # rank https mirrors with rate-mirrors

# ── Config edit (open a config in your editor) ────────────────────────────────
alias nlightdm="sudo $EDITOR /etc/lightdm/lightdm.conf"          # edit LightDM config
alias npacman="sudo $EDITOR /etc/pacman.conf"                    # edit pacman config
alias ncalamareslog="sudo $EDITOR /var/log/Calamares.log"        # open the installer log
alias nmakepkg="sudo $EDITOR /etc/makepkg.conf"                  # edit makepkg config
alias nmkinitcpio="sudo $EDITOR /etc/mkinitcpio.conf"            # edit initramfs config
alias nmirrorlist="sudo $EDITOR /etc/pacman.d/mirrorlist"        # edit the mirror list
alias nchaoticmirrorlist="sudo $EDITOR /etc/pacman.d/chaotic-mirrorlist" # edit the Chaotic-AUR mirror list
alias nsddm="sudo $EDITOR /etc/sddm.conf"                        # edit SDDM config
alias nsddmk="sudo $EDITOR /etc/sddm.conf.d/kde_settings.conf"   # edit SDDM KDE settings
alias nsddmd="sudo $EDITOR /usr/lib/sddm/sddm.conf.d/default.conf" # edit SDDM default config
alias nfstab="sudo $EDITOR /etc/fstab"                           # edit mount table (fstab)
alias nnsswitch="sudo $EDITOR /etc/nsswitch.conf"               # edit name-service switch config
alias nsamba="sudo $EDITOR /etc/samba/smb.conf"                 # edit Samba config
alias ngnupgconf="sudo $EDITOR /etc/pacman.d/gnupg/gpg.conf"     # edit pacman's gpg config
alias nhosts="sudo $EDITOR /etc/hosts"                          # edit the hosts file
alias nhostname="sudo $EDITOR /etc/hostname"                    # edit the hostname
alias nresolv="sudo $EDITOR /etc/resolv.conf"                   # edit DNS resolver config
alias nb="$EDITOR ~/.bashrc"                                    # edit your bash config
alias nz="$EDITOR ~/.zshrc"                                     # edit your zsh config
alias nf="$EDITOR ~/.config/fish/config.fish"                  # edit your fish config
alias nfastfetch="$EDITOR ~/.config/fastfetch/config.jsonc"    # edit your fastfetch config
alias nplymouth="sudo $EDITOR /etc/plymouth/plymouthd.conf"     # edit the boot splash config
alias nvconsole="sudo $EDITOR /etc/vconsole.conf"              # edit the TTY console config
alias nenvironment="sudo $EDITOR /etc/environment"             # edit system-wide environment vars
alias nloader="sudo $EDITOR /boot/efi/loader/loader.conf"      # edit systemd-boot loader config
alias nalacritty="$EDITOR ~/.config/alacritty/alacritty.toml"  # edit your Alacritty config
alias nkitty="$EDITOR ~/.config/kitty/kitty.conf"             # edit your Kitty config

# ── Networking / download ─────────────────────────────────────────────────────
alias wget='wget -c'                                          # download, resuming if interrupted
alias yta-aac='yt-dlp --extract-audio --audio-format aac'    # download audio as AAC
alias yta-best='yt-dlp --extract-audio --audio-format best'  # download audio, best format
alias yta-flac='yt-dlp --extract-audio --audio-format flac'  # download audio as FLAC
alias yta-mp3='yt-dlp --extract-audio --audio-format mp3'    # download audio as MP3
alias ytv-best="yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio' --merge-output-format mp4" # download best-quality video as MP4

# ── Keyboard / locale ─────────────────────────────────────────────────────────
alias give-me-azerty-be='sudo localectl set-x11-keymap be'   # switch keyboard to Belgian AZERTY
alias give-me-qwerty-us='sudo localectl set-x11-keymap us'   # switch keyboard to US QWERTY
alias setlocale='sudo localectl set-locale LANG=en_US.UTF-8' # set system language to US English
alias setlocales='sudo localectl set-x11-keymap be && sudo localectl set-locale LANG=en_US.UTF-8' # set BE keymap + US English locale

# ── Shells & display managers ─────────────────────────────────────────────────
alias tobash="sudo chsh $USER -s /bin/bash && echo 'Done. Now log out.'" # make bash your login shell
alias tozsh="sudo chsh $USER -s /bin/zsh && echo 'Done. Now log out.'"   # make zsh your login shell
alias tofish="sudo chsh $USER -s /bin/fish && echo 'Done. Now log out.'" # make fish your login shell
alias tolightdm="sudo pacman -S lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings --noconfirm --needed ; sudo systemctl enable lightdm.service -f ; echo 'Lightdm is active - reboot now'" # install & enable LightDM
alias tosddm="sudo pacman -S sddm --noconfirm --needed ; sudo systemctl enable sddm.service -f ; echo 'Sddm is active - reboot now'"          # install & enable SDDM
alias toly="sudo pacman -S ly --noconfirm --needed ; sudo systemctl enable ly.service -f ; echo 'Ly is active - reboot now'"                  # install & enable Ly
alias togdm="sudo pacman -S gdm --noconfirm --needed ; sudo systemctl enable gdm.service -f ; echo 'Gdm is active - reboot now'"              # install & enable GDM
alias tolxdm="sudo pacman -S lxdm --noconfirm --needed ; sudo systemctl enable lxdm.service -f ; echo 'Lxdm is active - reboot now'"          # install & enable LXDM
alias toemptty="sudo pacman -S emptty --noconfirm --needed ; sudo systemctl enable emptty.service -f ; echo 'Emptty is active - reboot now'"  # install & enable emptty

# ── Skel / config copy ────────────────────────────────────────────────────────
alias bupskel='cp -Rf /etc/skel ~/.skel-backup-(date +%Y.%m.%d-%H.%M.%S)'                  # back up /etc/skel into your home
alias cb='cp /etc/skel/.bashrc ~/.bashrc && echo "Copied."'                                # reset your bash config from skel
alias cz='cp /etc/skel/.zshrc ~/.zshrc && echo "Copied."'                                  # reset your zsh config from skel
alias cf='cp /etc/skel/.config/fish/config.fish ~/.config/fish/config.fish && exec fish'   # reset your fish config from skel

# ── Process / kill ────────────────────────────────────────────────────────────
alias psa='ps auxf'                                          # process tree, all users
alias psgrep='ps aux | grep -v grep | grep -i -e VSZ -e'    # search running processes
alias kc='killall conky'    # kill all conky instances
alias kp='killall polybar'  # kill all polybar instances
alias kpi='killall picom'   # kill all picom instances

# ── Fixes ─────────────────────────────────────────────────────────────────────
alias fix-permissions="sudo chown -R $USER:$USER ~/.config ~/.local" # fix ownership of your config dirs
alias keyfix='/usr/local/bin/kiro-fix-pacman-keys'        # repair pacman keyring
alias key-fix='/usr/local/bin/kiro-fix-pacman-keys'       # repair pacman keyring
alias keys-fix='/usr/local/bin/kiro-fix-pacman-keys'      # repair pacman keyring
alias fixkey='/usr/local/bin/kiro-fix-pacman-keys'        # repair pacman keyring
alias fixkeys='/usr/local/bin/kiro-fix-pacman-keys'       # repair pacman keyring
alias fix-key='/usr/local/bin/kiro-fix-pacman-keys'       # repair pacman keyring
alias fix-keys='/usr/local/bin/kiro-fix-pacman-keys'      # repair pacman keyring
alias fix-pacman-conf='/usr/local/bin/kiro-fix-pacman-conf'  # reset pacman.conf to Kiro default
alias fix-pacman-keyserver='/usr/local/bin/kiro-fix-gpg-conf' # fix the gpg keyserver config
alias fix-archlinux-mirrors='/usr/local/bin/kiro-fix-mirrors' # reset the Arch mirror list

# ── GPG ───────────────────────────────────────────────────────────────────────
alias gpg-check='gpg2 --keyserver-options auto-key-retrieve --verify'        # verify a signature, fetching the key
alias fix-gpg-check='gpg2 --keyserver-options auto-key-retrieve --verify'    # verify a signature, fetching the key
alias gpg-retrieve='gpg2 --keyserver-options auto-key-retrieve --receive-keys' # fetch a developer's gpg key
alias fix-gpg-retrieve='gpg2 --keyserver-options auto-key-retrieve --receive-keys' # fetch a developer's gpg key
alias fix-keyserver="[ -d ~/.gnupg ] || mkdir ~/.gnupg ; cp /etc/pacman.d/gnupg/gpg.conf ~/.gnupg/ ; echo 'done'" # copy pacman's gpg config to your home

# ── hblock (ad/tracker blocking) ──────────────────────────────────────────────
alias unhblock='hblock -S none -D none' # turn hblock blocking back off

# ── Misc ──────────────────────────────────────────────────────────────────────
alias merge='xrdb -merge ~/.Xresources'   # reload X resources
alias update-fc='sudo fc-cache -fv'       # rebuild the font cache
alias clean='clear; seq 1 (tput cols) | sort -R | sparklines | lolcat'  # clear screen with a colourful flourish
alias cls='clear; seq 1 (tput cols) | sort -R | sparklines | lolcat'    # clear screen with a colourful flourish
alias rg='rg --sort path'                 # ripgrep, results sorted by path
alias grh='git reset --hard'              # discard all local git changes
alias rmgitcache='rm -r ~/.cache/git'     # clear the git credential/cache dir
alias ssn='sudo shutdown now'             # shut down immediately
alias sr='reboot'                         # reboot
alias start-vmware='sudo systemctl enable --now vmtoolsd.service' # start VMware guest tools
alias vmware-start='sudo systemctl enable --now vmtoolsd.service' # start VMware guest tools
alias sv='sudo systemctl enable --now vmtoolsd.service'          # start VMware guest tools

# ── Personal / dev-box (disabled by default — uncomment what you want) ─────────
# alias up='./up.sh'                                 # run the repo's up.sh
# alias build='./build.sh'                           # run the repo's build.sh
# alias setup='./setup.sh'                           # run the repo's setup.sh
# alias c='claude'                                   # launch Claude Code
# alias scal='subl /var/log/Calamares.log'           # open installer log in Sublime
# alias spac='subl /etc/pacman.conf'                 # open pacman.conf in Sublime
# alias undopush='git push -f origin HEAD^:master'   # undo last push (force-push, use with caution)
