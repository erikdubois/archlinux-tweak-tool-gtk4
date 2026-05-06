# ATT - Ideas for future features

## Performance tab additions

- **preload** (`preload`) — adaptive readahead daemon that prefetches frequently used binaries into memory; same install/enable/disable pattern
- **IO scheduler** — dropdown to set the I/O scheduler (bfq, mq-deadline, kyber, none) per block device; useful for HDD vs NVMe

## New tabs worth adding

- **Gaming Stack** — Steam, Lutris, MangoHud, vkbasalt, vm.max_map_count tweak; could live in a dedicated Gaming tab

## Already implemented this session

- Ananicy CPP + cachyos-ananicy-rules-git (Performance)
- GameMode (Performance)
- Tuned + tuned-ppd combined enable/disable (Performance)
- Swapfile size display + btrfs detection (Performance)
- AUR Helper — yay-git / paru-git with chaotic-aur detection (Pacman)

---

## Claude's Ideashop

### Wallpaper Slideshow Mode — variety-lite built into ATT

Add a **Slideshow** toggle to the wallpaper page that rotates through the selected folder on a user-defined interval (5 min, 15 min, 1 h) using a `GLib.timeout_add_seconds` loop calling `on_random_wallpaper`. No variety required, no extra package — ATT already has all the pieces. A single `GLib` timer, a stop button, and an interval dropdown is the entire implementation. Pairs naturally with the existing folder browser and thumbnail grid.

**Why this is worth building:** Users who don't want the full variety daemon just want their wallpaper to rotate. This delivers that in ~30 lines reusing code ATT already has.

---

### System Health Score — a living pulse for your Arch install

Add a persistent **Health Score** widget to the ATT sidebar (or as a dedicated tab) that computes a single 0–100 score in real time from factors ATT already knows how to read:

| Factor | Weight | Source |
| --- | --- | --- |
| Failed systemd units | 25 | `systemctl list-units --failed` |
| Orphaned packages | 20 | `pacman -Qdtq` |
| Journal critical errors (last 24h) | 20 | `journalctl -p crit --since "24h ago"` |
| Disk usage on `/` and `/home` | 20 | `shutil.disk_usage()` |
| Broken/unreachable mirrors | 15 | test first mirror in `/etc/pacman.d/mirrorlist` |

The score updates every time the user opens ATT (lazy, low-cost) and recomputes live when the Maintenance tab runs a cleanup. Each factor shows its contribution inline so the user knows exactly what is dragging the score down. Tapping a factor jumps to the relevant ATT tab — failed services → Services tab, orphans → Maintenance tab.

**Why this is worth building:** Most users never notice their system degrading because every problem lives in a separate tab. A single number gives an immediate "is my system happy?" answer and turns ATT from a collection of manual tools into something that proactively surfaces problems — without adding any new system knowledge to the codebase.
