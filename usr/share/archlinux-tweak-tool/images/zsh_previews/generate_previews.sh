#!/usr/bin/env bash
# =============================================================
# ATT Zsh Theme Preview Generator
# Captures a screenshot of each oh-my-zsh theme with the
# Arch Linux logo via fastfetch, saved as <theme>.jpg
#
# Requirements: alacritty, fastfetch, scrot, zsh, oh-my-zsh
# Run from an X11 session (uses scrot for screenshots)
# =============================================================

set -euo pipefail

PREVIEW_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OMZ_THEMES_DIR="/usr/share/oh-my-zsh/themes"
OMZ_HOME="/usr/share/oh-my-zsh"
ZSH_BIN="/usr/bin/zsh"
DELAY=3        # seconds to wait for alacritty to render before screenshot
COLS=110
ROWS=36

# --- Dependency checks ---
echo "Checking dependencies..."
for cmd in alacritty fastfetch scrot zsh; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "ERROR: '$cmd' is required but not installed"
        exit 1
    fi
done

if [ ! -d "$OMZ_THEMES_DIR" ]; then
    echo "ERROR: oh-my-zsh themes not found at $OMZ_THEMES_DIR"
    exit 1
fi

# --- Theme list ---
mapfile -t themes < <(
    ls "$OMZ_THEMES_DIR"/*.zsh-theme \
    | xargs -I{} basename {} .zsh-theme \
    | sort
)

total=${#themes[@]}
echo "Found $total themes in $OMZ_THEMES_DIR"
echo "Output directory: $PREVIEW_DIR"
echo ""
echo "Each theme will open an alacritty window. Keep it focused."
echo "Press Enter to start..."
read -r

count=0
for theme in "${themes[@]}"; do
    out="$PREVIEW_DIR/${theme}.jpg"
    count=$((count + 1))
    echo "[$count/$total] $theme → $out"

    # Write a temporary zsh startup script for this theme.
    # Source oh-my-zsh directly so ~/.zshrc doesn't interfere.
    tmp=$(mktemp /tmp/att_preview_XXXXXX.zsh)
    cat > "$tmp" << ZSHEOF
export ZSH="$OMZ_HOME"
export ZSH_THEME="$theme"
export SHELL="$ZSH_BIN"
export DISABLE_UPDATE_PROMPT=true
source "\$ZSH/oh-my-zsh.sh" 2>/dev/null || true
clear
fastfetch --logo arch
echo ""
ls --color=always "\$HOME"
echo ""
print -P "%B%F{cyan}Theme: $theme%f%b"
print -P "\$PROMPT"
print -P "\$PROMPT"
print -P "\$PROMPT"
sleep 60
ZSHEOF
    chmod +x "$tmp"

    alacritty \
        --option "window.dimensions.columns=$COLS" \
        --option "window.dimensions.lines=$ROWS" \
        --option "window.startup_mode=Windowed" \
        --title "ATT-Preview-$theme" \
        -e "$ZSH_BIN" "$tmp" &
    PID=$!

    # Wait for the terminal to render, then capture the focused window
    sleep "$DELAY"
    scrot -u "$out"

    kill "$PID" 2>/dev/null || true
    wait "$PID" 2>/dev/null || true
    rm -f "$tmp"

    echo "  saved"
done

echo ""
echo "✓ Done — $count previews generated in $PREVIEW_DIR"
