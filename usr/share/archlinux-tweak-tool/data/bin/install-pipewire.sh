#!/bin/bash

##################################################################################################################################
# Author    : Erik Dubois
# Website   : https://www.erikdubois.be
# Youtube   : https://youtube.com/erikdubois
##################################################################################################################################
#
#   DO NOT JUST RUN THIS. EXAMINE AND JUDGE. RUN AT YOUR OWN RISK.
#
##################################################################################################################################
# Purpose
# - Install PipeWire audio stack (modern Arch default)
# - Remove PulseAudio audio packages
# - Enable PipeWire's PulseAudio emulation for backward compatibility (pavucontrol, etc.)
# - Keep Bluetooth audio support enabled
##################################################################################################################################

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

pkg_installed()    { pacman -Q "$1" &>/dev/null; }
install_packages() { sudo pacman -S --needed --noconfirm "$@"; }

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

header "Installing PipeWire audio stack"

# Force remove PulseAudio and any packages that depend on it
if pkg_installed pulseaudio; then
    info "Removing packages that depend on PulseAudio..."
    dependents=$(pacman -Qi pulseaudio 2>/dev/null | awk '/^Required By/ {$1=$2=""; print $0}' | tr ' ' '\n' | grep -v '^$' | grep -v '^None$')
    for dep in $dependents; do
        if pkg_installed "$dep"; then
            info "Removing dependent: $dep"
            sudo pacman -Rdd --noconfirm "$dep" 2>/dev/null || true
        fi
    done
    info "Removing PulseAudio..."
    sudo pacman -Rdd --noconfirm pulseaudio 2>/dev/null || true
fi

# Clean up stale PipeWire ALSA config
if [[ -f /etc/alsa/conf.d/99-pipewire-default.conf ]]; then
    sudo rm /etc/alsa/conf.d/99-pipewire-default.conf
    info "Removed stale PipeWire ALSA config"
fi

# Install PipeWire stack
header "Installing PipeWire"
install_packages \
    pipewire \
    pipewire-alsa \
    pipewire-audio \
    pipewire-session-manager \
    wireplumber \
    volctl

# Install PulseAudio emulation
header "Enabling PulseAudio emulation"
install_packages pipewire-pulse

systemctl --user enable pipewire-pulse.service 2>/dev/null || true
systemctl --user start pipewire-pulse.service 2>/dev/null || true
info "PulseAudio emulation enabled (pavucontrol and PulseAudio apps will work)"

# Enable Bluetooth service
sudo systemctl enable --now bluetooth.service

success "PipeWire installation completed"
warn "Reboot recommended"
