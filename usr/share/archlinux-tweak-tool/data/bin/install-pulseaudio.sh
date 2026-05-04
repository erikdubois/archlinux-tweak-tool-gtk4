#!/bin/bash
set -euo pipefail
##################################################################################################################
# Author    : Erik Dubois
# Website   : https://www.erikdubois.be
# Youtube   : https://youtube.com/erikdubois
##################################################################################################################

RESET=$(tput sgr0)
CYAN=$(tput setaf 6)
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
YELLOW=$(tput setaf 3)

separator() { echo "${CYAN}===============================================================================${RESET}"; }
header()    { echo ""; separator; echo "${CYAN}  $1${RESET}"; separator; }
success()   { echo "${GREEN}  ✓ $1${RESET}"; }
info()      { echo "    $1"; }
warn()      { echo "${YELLOW}  ⚠ $1${RESET}"; }
error()     { echo "${RED}  ✗ $1${RESET}"; }

pkg_installed()     { pacman -Q "$1" &>/dev/null; }
install_packages()  { sudo pacman -S --needed --noconfirm "$@"; }

remove_if_installed() {
    local pkg="$1"
    if pkg_installed "$pkg"; then
        info "Removing $pkg..."
        sudo pacman -Rdd --noconfirm "$pkg" 2>/dev/null || true
    fi
}

audio_summary() {
    header "Current audio state"

    local server
    server=$(pactl info 2>/dev/null | awk '/Server Name/ {print $NF}') || server="unknown"
    info "Active server : $server"

    for pkg in pulseaudio pipewire pipewire-pulse wireplumber; do
        local ver
        ver=$(pacman -Q "$pkg" 2>/dev/null | awk '{print $2}') || ver="not installed"
        info "  $pkg : $ver"
    done
}

audio_summary

header "Switching to PulseAudio audio stack"

# Stop and disable PipeWire services
systemctl --user disable pipewire-pulse.service 2>/dev/null || true
systemctl --user stop pipewire-pulse.service 2>/dev/null || true
systemctl --user disable pipewire.service 2>/dev/null || true
systemctl --user stop pipewire.service 2>/dev/null || true
info "Stopped PipeWire services"

# Clean up stale PipeWire ALSA config
if [[ -f /etc/alsa/conf.d/99-pipewire-default.conf ]]; then
    sudo rm /etc/alsa/conf.d/99-pipewire-default.conf
    info "Removed stale PipeWire ALSA config"
fi

# Remove conflicting audio packages
header "Removing PipeWire packages"
for pkg in pipewire-media-session pipewire lib32-pipewire libpipewire pipewire-alsa \
           pipewire-audio pipewire-jack lib32-pipewire-jack pipewire-session-manager \
           pipewire-zeroconf pipewire-pulse wireplumber; do
    remove_if_installed "$pkg"
done

# Install PulseAudio stack
header "Installing PulseAudio"
install_packages \
    pulseaudio \
    pulseaudio-alsa \
    pulseaudio-bluetooth \
    jack2 \
    volctl

# Enable Bluetooth service
sudo systemctl enable --now bluetooth.service

success "PulseAudio installation completed"
warn "Reboot recommended"
