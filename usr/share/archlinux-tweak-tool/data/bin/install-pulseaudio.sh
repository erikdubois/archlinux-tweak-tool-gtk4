#!/usr/bin/env bash

##################################################################################################################################
# Author    : Erik Dubois
# Website   : https://www.erikdubois.be
# Youtube   : https://youtube.com/erikdubois
##################################################################################################################################
#
#   DO NOT JUST RUN THIS. EXAMINE AND JUDGE. RUN AT YOUR OWN RISK.
#
##################################################################################################################################

set -euo pipefail

##################################################################################################################################
# Purpose
# - Switch from PipeWire to PulseAudio audio stack
# - Remove all PipeWire packages and services
# - Install PulseAudio audio stack
# - Keep Bluetooth audio support enabled
##################################################################################################################################

log_section()  { echo ""; echo "==== $* ===="; echo ""; }
log_info()     { echo "  [INFO] $*"; }
log_success()  { echo "  [SUCCESS] $*"; }
log_warn()     { echo "  [WARN] $*"; }

pkg_installed() { pacman -Q "$1" &>/dev/null; }

remove_if_installed() {
    local pkg="$1"
    if pkg_installed "$pkg"; then
        log_info "Removing $pkg..."
        sudo pacman -Rdd --noconfirm "$pkg" 2>/dev/null || true
    fi
}

install_packages() { sudo pacman -S --needed --noconfirm "$@"; }

audio_summary() {
    log_section "Current audio state"

    local server
    server=$(pactl info 2>/dev/null | awk '/Server Name/ {print $NF}') || server="unknown (pactl failed)"
    log_info "Active server : $server"

    for pkg in pulseaudio pipewire pipewire-pulse wireplumber; do
        local ver
        ver=$(pacman -Q "$pkg" 2>/dev/null | awk '{print $2}') || ver="not installed"
        log_info "  $pkg : $ver"
    done
}

main() {

    audio_summary

    log_section "Switching to PulseAudio audio stack"

    ############################################################################################################
    # Stop and disable PipeWire services
    ############################################################################################################

    systemctl --user disable pipewire-pulse.service 2>/dev/null || true
    systemctl --user stop pipewire-pulse.service 2>/dev/null || true
    systemctl --user disable pipewire.service 2>/dev/null || true
    systemctl --user stop pipewire.service 2>/dev/null || true

    log_info "Stopped PipeWire services"

    ############################################################################################################
    # Clean up stale PipeWire ALSA config
    ############################################################################################################

    if [[ -f /etc/alsa/conf.d/99-pipewire-default.conf ]]; then
        sudo rm /etc/alsa/conf.d/99-pipewire-default.conf
        log_info "Removed stale PipeWire ALSA config"
    fi

    ############################################################################################################
    # Remove conflicting audio packages
    ############################################################################################################

    for pkg in pipewire-media-session pipewire lib32-pipewire libpipewire pipewire-alsa \
               pipewire-audio pipewire-jack lib32-pipewire-jack pipewire-session-manager \
               pipewire-zeroconf pipewire-pulse wireplumber; do
        remove_if_installed "$pkg"
    done

    ############################################################################################################
    # Install PulseAudio stack
    ############################################################################################################

    install_packages \
        pulseaudio \
        pulseaudio-alsa \
        pulseaudio-bluetooth \
        jack2 \
        volctl

    ############################################################################################################
    # Enable Bluetooth service
    ############################################################################################################

    sudo systemctl enable --now bluetooth.service

    log_success "PulseAudio installation completed"
    log_warn "Reboot recommended"
}

main "$@"
