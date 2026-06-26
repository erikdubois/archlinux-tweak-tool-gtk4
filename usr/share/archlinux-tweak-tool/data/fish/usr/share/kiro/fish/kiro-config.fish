#
# kiro-config.fish — Kiro's default fish configuration (shared payload, loader)
#
# Installed to : /usr/share/kiro/fish/kiro-config.fish   (owned by the package)
# Sourced from : ~/.config/fish/config.fish              (a thin stub, yours to edit)
#
# Package upgrades replace THIS file and everything under parts/, so do not edit
# them here. To change, add or disable anything, put it in
# ~/.config/fish/config.fish below the `source` line — your home config is
# loaded last and always wins.
#
# Layout: this loader sources the modular pieces in parts/. 00-env applies to
# every shell; the numbered parts after it are interactive-only.
#

set -l __kiro_parts /usr/share/kiro/fish/parts

# Core environment for ALL shells (PATH, editor, man pager) — before the guard
# so non-interactive scripts inherit it.
source $__kiro_parts/00-env.fish

# Everything below is for interactive shells only.
status is-interactive; or exit

# Interactive parts, in numeric order (10, 20, 30, …). fish sorts glob results, and
# fish has no [..] bracket globs, so match all *.fish and skip the one already loaded.
for f in $__kiro_parts/*.fish
    test $f = $__kiro_parts/00-env.fish; and continue
    source $f
end
