# ============================================================
# Authors: Erik Dubois
# ============================================================

"""Funding channels for the Kiro project and the action to open them."""

import functions as fn

# Canonical funding channels — mirror of kiro-website/.github/FUNDING.yml.
# These URLs are stable; if a channel ever changes, edit it here.
SOURCES = [
    ("GitHub Sponsors", "https://github.com/sponsors/erikdubois", "Low fees — most reaches the project"),
    ("Patreon", "https://www.patreon.com/c/kiroproject", "Recurring membership tiers"),
    ("YouTube Membership", "https://www.youtube.com/@ErikDubois/join", "Early access and member-only perks"),
    ("Ko-fi", "https://ko-fi.com/erikdubois", "One-off donation, low fees"),
    ("PayPal", "https://www.paypal.me/erikdubois", "One-off donation"),
]


def on_click_open(self, url, _widget):
    """Open a funding URL in the real user's default browser (drop root via sudo -u)."""
    fn.open_url_as_user(url)
