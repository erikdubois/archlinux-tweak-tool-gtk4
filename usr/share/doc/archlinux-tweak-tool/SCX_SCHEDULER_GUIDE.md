# CPU Scheduler (scx) — Plain-English Guide

The **CPU scheduler** is the part of Linux that decides which program gets the
CPU next. You can swap in a different one to make the system feel snappier for a
certain task — **games, audio work, battery life** — and swap back, all
**without rebooting**. On Kiro you do this with **scx-manager**, CachyOS's small
GUI for sched-ext schedulers.

> **Short version:** if you're not sure, do nothing. Your kernel's default
> (EEVDF / BORE on Kiro) is already very good. This is for experimenting.

---

## Start from what you want

Don't think about schedulers — think about what you want your computer to feel
like, then pick the matching row in scx-manager.

- **If you want a snappy gaming computer** → scheduler **scx_lavd**, profile
  **Gaming**.
- **If you want glitch-free audio or music production** → **scx_flash**,
  **LowLatency**.
- **If you want the fastest possible compile / ISO build** → **scx_rusty**,
  **Server**.
- **If you want to build *and* keep using the PC at the same time** →
  **scx_lavd**, **LowLatency**.
- **If you want a laptop that lasts longer on battery** → any scheduler,
  **PowerSave**.
- **If you want lots of apps open without stutter** → **scx_bpfland**, **Auto**.
- **If you want a rock-solid, no-surprises computer** → do nothing; the kernel
  default is already excellent.
- **If you want to undo it all** → click **Disable**.

*Not sure what you want? Do nothing — the default is already good.*

*Building but want a usable desktop?* Also keep cores free for the build itself:
the **Performance → Build** tab has a "Keep 2 cores free" button (or run
`makepkg -j$(($(nproc)-2))`). A throughput scheduler finishes a touch sooner;
a LowLatency one keeps the mouse smooth while you work.

---

## Is it safe?

Yes.

- **Nothing changes until you click Apply** in scx-manager.
- **No reboot** — changes are live, and reversible the same second.
- **Disable** instantly returns you to the normal kernel scheduler.
- Worst case if a scheduler misbehaves: click Disable (or reboot — nothing
  persists unless you applied a choice you want to keep).

---

## Opening scx-manager

On Kiro it's **already installed** — just launch **scx-manager** from your
application menu (or run `scx-manager`). On other Arch-based systems, install it
first with `sudo pacman -S scx-manager`.

It drives the `scx_loader` service under the hood — the same mechanism CachyOS's
own tools use — so your choice is remembered across reboots until you Disable it.

---

## Using scx-manager

The dialog has a few fields:

- **Select sched-ext scheduler** — *which* scheduler runs. Each is tuned for a
  job (see the cheat-sheet at the end).
- **Select scheduler profile** — *how* that scheduler leans. **Auto** is the
  safe middle; **Gaming** favours responsiveness, **PowerSave** favours battery,
  **Server** favours throughput, **LowLatency** keeps things smooth under load.
- **Extra scheduler flags** — leave blank unless you know you need one. This is
  for advanced tuning and most people never touch it.

Pick a scheduler and a profile, then click **Apply**. To go back to the stock
kernel scheduler, click **Disable**.

---

## How do I know it worked?

scx-manager shows a **Running sched-ext scheduler** line — that's the real
status. Before you Apply anything it reflects the kernel default; after Apply it
names the scheduler you chose. After Disable it goes back to the default.

---

## Does my choice survive a reboot?

Yes — once you Apply, `scx_loader` remembers it and brings it back at the next
boot. **Disable** removes that, so you're back to the stock scheduler on every
boot.

---

## "It won't switch, or nothing happens"

Both of Kiro's kernels — **linux-cachyos** (default) and **linux-zen** — support
sched-ext out of the box, so scx-manager works on either. If its controls do
nothing, check that you're booted into one of them — the Kernels page shows your
running kernel at the top.

---

## Scheduler cheat-sheet

For when you want the detail behind the picks above:

| Scheduler     | Best for                          |
|---------------|-----------------------------------|
| scx_lavd      | Gaming and a responsive desktop   |
| scx_bpfland   | General interactive desktop use   |
| scx_rusty     | Heavy workloads / throughput      |
| scx_flash     | Audio and multimedia (low jitter) |
| scx_p2dq      | General, scales to many cores     |
| scx_tickless  | Servers and power saving          |
