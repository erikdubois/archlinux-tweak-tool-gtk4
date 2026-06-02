# ATT Dev Page — Guide

> Plain-language guide to every row on ATT's Dev page: what it means, and what to do if it's red.
>
> **Green = fine, nothing to do.** Red / empty = maybe act (see the table). Orange ⚠ = a warning or a guard firing right now.
>
> Spot a row that isn't here? Please open an issue.

---

## Sections

1. [Session diagnostics](#1-session-diagnostics)
2. [Per-tab status](#2-per-tab-status)
3. [Cross-cutting safeguards](#3-cross-cutting-safeguards)
4. [System integrity (kiro-audit mirror)](#4-system-integrity-kiro-audit-mirror)
5. [Userspace tuning](#5-userspace-tuning)

---

## 1. Session diagnostics

*Info only — confirms ATT read your system correctly. Nothing to fix. If a value looks wrong, open an issue with the output of `cat /etc/os-release`.*

| Check                | What it means                                                        |
|----------------------|---------------------------------------------------------------------|
| `fn.distr`           | Internal distro ID (arch, cachyos, artix…). Decides which tabs show. |
| `get_distro_label()` | Friendly name (Kiro, Arch…). On Kiro: `arch` + label `Kiro` is correct. |
| `XDG_CURRENT_DESKTOP`| Your desktop environment.                                           |
| `fn.sudo_username`   | The real (non-root) user that launched ATT.                         |
| `fn.home`            | That user's home — where ATT writes your configs.                   |
| `XDG_SESSION_TYPE`   | x11 or wayland (shows `(inferred)` if the system didn't set it).    |
| `active shell`       | Your login shell (bash / zsh / fish).                               |
| `bootloader`         | systemd-boot / grub / limine / refind.                              |
| `running kernel`     | Output of `uname -r`.                                               |
| `init system`        | systemd or OpenRC.                                                  |
| `initramfs`          | mkinitcpio or dracut.                                               |
| `systemd PID 1`      | Confirms systemd is really running (not inside a chroot/container). |

---

## 2. Per-tab status

*Shows whether each tab's packages/services are installed. Red usually just means "not installed" — install it from that tab if you want it. Nothing here is a failure on its own.*

### "Is it installed?" tabs

| Tab                  | What it checks                                  | If it's red                          |
|----------------------|-------------------------------------------------|--------------------------------------|
| AI Tools             | ollama / open-webui / aider / claude on PATH    | install from the AI Tools tab        |
| Desktop              | 15 desktops/WMs by their session binary         | install from the Desktop page        |
| Shells               | bash/zsh/fish + completions, alacritty          | install from the Shells page         |
| Software             | 12 app stores / package managers by binary      | install from the Software page       |
| Icons / Themes / Themer | counts of `edu-*` / sardi / surfn packs      | install from that page               |
| Packages             | AUR helpers (yay / paru / trizen / pikaur)      | install one (paru) from Packages     |
| Wallpaper            | variety installed + running                     | install from the Wallpaper page      |
| Fastfetch            | fastfetch / lolcat + your config                | apply a preset from the Fastfetch page |
| Autostart            | count of `~/.config/autostart/*.desktop`        | info only — 0 when you expected more = something cleared it |
| Locale               | LANG / keymap / timezone                        | info only                            |
| `ollama.service active` | ollama daemon running                        | `sudo systemctl start ollama`        |

### Kernels

| Check               | What it means                              | If it's red                              |
|---------------------|--------------------------------------------|------------------------------------------|
| `{kernel}`          | A bootable image in `/boot` (running = green) | —                                      |
| `{kernel}-headers`  | Headers for that kernel — DKMS needs them  | `sudo pacman -S {kernel}-headers`        |
| `(none found)`      | NO kernels in `/boot`                      | **Broken boot — investigate immediately** |

### Network

| Check                       | What it means                          | If it's red                              |
|-----------------------------|----------------------------------------|------------------------------------------|
| avahi / `avahi-daemon`      | mDNS for `.local` hostnames            | `sudo systemctl enable --now avahi-daemon` |
| samba / `smb`               | SMB file sharing                       | enable from Network if you host shares   |
| firewalld (Kiro default ON) | the firewall                           | `sudo systemctl enable --now firewalld`  |
| firewalld allows mdns/samba | those services allowed through         | open them on the Network page            |

### Pacman / repos

| Check                | What it means                                      | If it's red                          |
|----------------------|----------------------------------------------------|--------------------------------------|
| chaotic-AUR active   | extra repo (Kiro default)                          | enable on the Pacman page            |
| nemesis_repo active  | Erik's repo — needed for `edu-*` / `kiro-*` packages | enable on the Pacman page          |
| `[multilib]`         | 32-bit repo — **OFF on Kiro by design**            | enable on Pacman only if you need 32-bit |
| `[testing]`          | Arch testing repo — OFF by default                 | leave off unless you accept breakage |

### Plymouth

*Kiro ships without Plymouth, so red here is normal.*

| Check                    | What it means                       | If it's red                          |
|--------------------------|-------------------------------------|--------------------------------------|
| plymouth installed       | boot-splash package                 | optional — install from Plymouth page |
| active theme             | current theme (if installed)        | apply one on the Plymouth page       |
| HOOKS / att-plymouth.conf| initramfs hook that wires it in     | one-click fix on the Plymouth page   |
| cmdline `splash`         | `quiet splash` on the kernel line   | the Plymouth page adds it            |

### Performance

| Check                     | What it means                                  | If it's red                              |
|---------------------------|------------------------------------------------|------------------------------------------|
| tuned + profile           | tuning daemon (Kiro ships it ON)               | enable from the Performance page         |
| tuned-ppd                 | power-profile front-end (Kiro ON)              | enable from the Performance page         |
| PPD profile ⚠ mismatch    | desktop widget changed profile, tuned lagging  | restart tuned-ppd if it sticks           |
| irqbalance                | spreads IRQs across cores                       | optional                                 |
| ananicy-cpp               | auto-nice daemon (Kiro ON)                      | enable from the Performance page         |
| preload                   | old file preloader                              | optional, rarely useful on SSDs          |
| gamemode / cpupower       | optional perf tools                             | install if you want them                 |
| fstrim.timer (should be ON)| weekly SSD TRIM                               | `sudo systemctl enable fstrim.timer`     |

### SDDM

| Check                    | What it means                          | If it's red                          |
|--------------------------|----------------------------------------|--------------------------------------|
| active display manager   | which DM is enabled (or none)          | —                                    |
| sddm installed / enabled | SDDM package + service state           | enable from the SDDM page            |
| plasma-login ⚠           | CachyOS login shim (not used by Kiro)  | info only                            |

### Services

| Check                    | What it means                                   | If it's red                  |
|--------------------------|-------------------------------------------------|------------------------------|
| cups / `cups.service`    | printing (socket-activated — inactive is fine)  | —                            |
| bluez / bluetooth        | Bluetooth stack                                 | enable from the Services tab |
| bluetooth-autoconnect    | auto-reconnect to last device                   | toggle on the Services tab   |

### User

| Check                    | What it means                          | If it's red                          |
|--------------------------|----------------------------------------|--------------------------------------|
| `{user}` in wheel        | sudo works for you                     | **add your user to `wheel`** (red = sudo broken) |
| `/etc/sudoers.d/` entries| count of drop-in files (normal)        | info only                            |

### Privacy

| Check                    | What it means                          | If it's red                          |
|--------------------------|----------------------------------------|--------------------------------------|
| hblock on PATH           | ad/tracker hosts blocker               | optional                             |
| hosts has hblock marker  | hblock has run                         | run hblock from the Privacy page     |
| firefox-ublock-origin    | adblock extension                      | install from the Privacy page        |

### Maintenance

| Check                    | What it means                          | If it's red / low                    |
|--------------------------|----------------------------------------|--------------------------------------|
| reflector / rate-mirrors | mirror-ranking tools                   | page falls back to manual picker     |
| pacman ParallelDownloads | parallel-download count                | raise it on the Pacman page          |

---

## 3. Cross-cutting safeguards

*Each row is a guard that hides or shows UI so ATT never offers broken actions. Orange = firing right now. Nothing to fix — except the kernel hook.*

| Guard                              | When it fires                  | Effect / action                                            |
|------------------------------------|--------------------------------|------------------------------------------------------------|
| Plymouth page hidden               | on Artix (OpenRC)              | page hidden — Plymouth helpers assume systemd              |
| SDDM page hidden                   | on PrismLinux                 | page hidden — Prism ships its own SDDM config              |
| SDDM page hidden                   | CachyOS plasma-login active   | page hidden — CachyOS replaces SDDM                        |
| pacman-hook-kernel-install         | Arch + systemd-boot           | **if MISSING: `sudo pacman -S pacman-hook-kernel-install`** (critical for boot) |
| visudo section shown               | on Arch                       | User page shows the visudo helper                          |
| Plymouth omarchy marker            | on Omarchy                    | writes a marker when you apply a theme                     |

---

## 4. System integrity (kiro-audit mirror)

*A subset of `kiro-audit`'s checks, shown in the GUI so you don't need a terminal.*

### Microcode

| Check                   | What it means                          | If it's red                              |
|-------------------------|----------------------------------------|------------------------------------------|
| intel-ucode / amd-ucode | microcode image present in `/boot`     | `sudo pacman -S intel-ucode` (or amd-ucode) |
| `(none installed)` ⚠    | no microcode at all                    | install the one for your CPU             |

### Audio (PipeWire)

| Check                                      | What it means              | If it's red                              |
|--------------------------------------------|----------------------------|------------------------------------------|
| pipewire / pipewire-pulse / wireplumber    | audio stack is complete    | `sudo pacman -S pipewire pipewire-pulse wireplumber` |
| pulseaudio not installed                   | old daemon is gone (good)  | `sudo pacman -R pulseaudio`              |

### ZRAM

| Check                | What it means                          | If it's red / off                        |
|----------------------|----------------------------------------|------------------------------------------|
| zram-generator       | compressed-RAM swap package            | `sudo pacman -S zram-generator`          |
| `/dev/zram0` present | the swap device was created            | check `zram-generator.conf`, reboot      |
| active as swap       | it's in use as swap                    | `journalctl -u systemd-zram-setup@zram0` |
| compression          | algorithm (zstd is best)               | other than zstd = works but suboptimal; edit conf |

### Logs

| Check              | What it means                          | If it's red                          |
|--------------------|----------------------------------------|--------------------------------------|
| logrotate.timer    | file logs rotate automatically         | `sudo systemctl enable logrotate.timer` |

### Calamares cleanup

| Check                | What it means                                  | If it's red                              |
|----------------------|------------------------------------------------|------------------------------------------|
| installer pkgs removed | calamares / mkinitcpio-archiso / kiro-calamares-config-next gone | `sudo pacman -R {pkg}` — stop if it cascades |
| installer leftovers  | live-only files were wiped                     | delete the listed paths; `kiro-audit --fix` may help |

### Package integrity

| Check              | What it means                          | If it's red                          |
|--------------------|----------------------------------------|--------------------------------------|
| missing files      | `pacman -Qk` found gaps                 | `sudo pacman -S {pkg}` to restore files |

### Failed units

| Check              | What it means                          | If it's red                              |
|--------------------|----------------------------------------|------------------------------------------|
| failed units       | `systemctl --failed` count             | `systemctl status {unit}` + `journalctl -u {unit} -b` |

---

## 5. Userspace tuning

*Small tweaks shipped by `kiro-system-files`. For any missing file, the fix is the same: `sudo pacman -S kiro-system-files`.*

### systemd-oomd (kills a runaway app before the desktop freezes)

| Check    | What it means                          | If it's red                          |
|----------|----------------------------------------|--------------------------------------|
| enabled  | starts at every boot                   | `sudo systemctl enable systemd-oomd` |
| active   | running and watching memory now        | `sudo systemctl start systemd-oomd`  |

### Intel ME blacklist (closes the mei driver attack surface; harmless on AMD)

| Check                    | What it means                          | If it's red / ⚠                          |
|--------------------------|----------------------------------------|------------------------------------------|
| blacklist-intel-me.conf  | the blacklist file is in place         | reinstall `kiro-system-files`         |
| mei/mei_me not loaded    | drivers actually unloaded              | rebuild initramfs (`sudo mkinitcpio -P`) + reboot |

### Bluetooth USB reset (fixes "BT dead after suspend")

| Check                | What it means                          | If it's red                          |
|----------------------|----------------------------------------|--------------------------------------|
| bluetooth-usb.conf   | sets `btusb reset=1`                   | reinstall `kiro-system-files`     |

### Kernel zswap (off, so pages aren't compressed twice)

| Check                | What it means                          | If it's red / Y                          |
|----------------------|----------------------------------------|------------------------------------------|
| disable-zswap.conf   | the tmpfile that turns zswap off       | reinstall `kiro-system-files`         |
| runtime state N/0    | zswap is off right now                 | `sudo systemd-tmpfiles --create /etc/tmpfiles.d/disable-zswap.conf` |

### NetworkManager loopback (silences a benign boot warning)

| Check                | What it means                          | If it's red                          |
|----------------------|----------------------------------------|--------------------------------------|
| unmanaged-lo.conf    | stops NM managing `lo`                 | reinstall `kiro-system-files`     |

---

## Maintenance (for contributors)

The Dev rows live in `usr/share/archlinux-tweak-tool/dev_gui.py`. **Add a `_row(...)` there → add a line here in the same change**, or the row shows up with no meaning.

This file installs to `/usr/share/doc/archlinux-tweak-tool/DEV_PAGE_GLOSSARY.md`; the Dev page's "What do these rows mean?" link opens this local copy in a GUI editor (no browser, no internet). Spot an undocumented row? Open an issue.
