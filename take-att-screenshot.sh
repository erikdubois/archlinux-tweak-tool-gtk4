#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMAGES_DIR="$SCRIPT_DIR/images"

TABS=(
    "AI Tools"
    "Autostart"
    "Desktop"
    "Fastfetch"
    "Icons"
    "Kernels"
    "Locale"
    "Logging"
    "Maintenance"
    "Network"
    "Packages"
    "Pacman"
    "Plymouth"
    "Privacy"
    "Performance"
    "Sddm"
    "Services"
    "Shells"
    "Software"
    "System"
    "Themer"
    "Arc themes"
    "User"
    "Wallpaper"
)

TOTAL=${#TABS[@]}

if [[ "${1:-}" =~ ^[0-9]+$ ]]; then
    NUM=$1
else
    NUM=1
    while [[ -f "$IMAGES_DIR/att${NUM}.png" ]]; do
        ((NUM++))
    done
fi

if [[ $NUM -gt $TOTAL ]]; then
    echo "All $TOTAL tabs already captured."
    exit 0
fi

TAB_NAME="${TABS[$((NUM - 1))]}"
OUTFILE="$IMAGES_DIR/att${NUM}.png"

echo ""
echo "  Tab $NUM / $TOTAL : $TAB_NAME"
echo "  Navigate to the '$TAB_NAME' tab in ATT, then press Enter..."
read -r

WIN_ID=$(xdotool search --name "Arch Linux Tweak Tool" 2>/dev/null | head -1 || true)
if [[ -z "$WIN_ID" ]]; then
    echo "ERROR: ATT window not found. Make sure it is running."
    exit 1
fi

sleep 0.2
maim --window "$WIN_ID" "$OUTFILE"
echo "  Saved: $OUTFILE"

NEXT=$((NUM + 1))
if [[ $NEXT -le $TOTAL ]]; then
    echo "  Next tab: '${TABS[$((NEXT - 1))]}' — run: $0 $NEXT"
    echo "  Or just run: $0   (auto-detects next slot)"
fi
echo ""
