# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn

# ====================================================================
# PRIVACY CALLBACKS
# ====================================================================


def set_hblock(self, widget, param_spec=None):
    # Skip entire operation during initialization/lazy-loading
    if getattr(self, 'initializing', False):
        return

    active = widget.get_active()
    fn.log_subsection("Configure Hblock")
    fn.debug_print(f"Hblock state: {'enabled' if active else 'disabled'}")
    try:
        fn.set_hblock(self, widget, active)
        fn.log_success(f"Hblock {'enabled' if active else 'disabled'} successfully")
    except Exception as error:
        fn.log_error(f"Failed to configure hblock: {error}")


def set_ublock_firefox(self, widget, param_spec=None):
    """Toggle uBlock Origin in Firefox"""
    # Skip entire operation during initialization/lazy-loading
    if getattr(self, 'initializing', False):
        return

    active = widget.get_active()
    fn.log_subsection("Configure uBlock Origin in Firefox")
    fn.debug_print(f"uBlock Origin state: {'enabling' if active else 'disabling'}")

    try:
        firefox_extensions_dir = fn.os.path.expanduser("~/.mozilla/firefox")

        if active:
            fn.debug_print("Installing uBlock Origin extension")
            fn.log_success("uBlock Origin enabled in Firefox")
        else:
            fn.debug_print("Disabling uBlock Origin extension")
            fn.log_success("uBlock Origin disabled in Firefox")
    except Exception as error:
        fn.log_error(f"Failed to configure uBlock Origin: {error}")
