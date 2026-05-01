# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn

# ====================================================================
# PRIVACY CALLBACKS
# ====================================================================


def set_hblock(self, widget, param_spec=None):
    if getattr(self, 'initializing', False):
        return
    active = widget.get_active()
    fn.log_subsection("Configure Hblock")
    fn.threading.Thread(target=fn.set_hblock, args=(self, widget, active), daemon=True).start()


def set_ublock_firefox(self, widget, param_spec=None):
    if getattr(self, 'initializing', False):
        return
    active = widget.get_active()
    fn.log_subsection("Configure uBlock Origin in Firefox")
    fn.threading.Thread(target=fn.set_firefox_ublock, args=(self, widget, active), daemon=True).start()
