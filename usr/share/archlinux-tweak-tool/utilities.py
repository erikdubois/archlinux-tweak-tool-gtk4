# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=R0911,R1705,

import functions as fn

# This function has one job, and one job only; ensure that check
# boxes match what is passed to it, based on the logic from the calling function


def set_util_state(self, util, util_state, lolcat_state):
    """set utility state for fastfetch"""
    import fastfetch

    if util == "fastfetch":
        self.fast_util.set_state(util_state)
        self.fast_lolcat.set_state(lolcat_state)
        fastfetch.write_configs(util_state, lolcat_state)


def get_util_state(self, util):
    """get utility state"""
    if util == "neofetch":
        return self.neofetch_util.get_active()
    elif util == "fastfetch":
        return self.fastfetch_util.get_active()
    elif util == "screenfetch":
        return self.screenfetch_util.get_active()
    elif util == "ufetch":
        return self.ufetch_util.get_active()
    elif util == "ufetch-arco":
        return self.ufetch_arco_util.get_active()
    elif util == "pfetch":
        return self.pfetch_util.get_active()
    elif util == "paleofetch":
        return self.paleofetch_util.get_active()
    elif util == "alsi":
        return self.alsi_util.get_active()
    elif util == "hfetch":
        return self.hfetch_util.get_active()
    elif util == "fetch":
        return self.fetch_util.get_active()
    elif util == "sfetch":
        return self.sfetch_util.get_active()
    elif util == "sysinfo":
        return self.sysinfo_util.get_active()
    elif util == "sysinfo-retro":
        return self.sysinfo_retro_util.get_active()
    elif util == "cpufetch":
        return self.cpufetch_util.get_active()
    elif util == "hyfetch":
        return self.hyfetch_util.get_active()
    elif util == "colorscript random":
        return self.colorscripts.get_active()
    else:
        return False


def get_lolcat_state(self, util):
    """get lolcat state"""
    if util == "neofetch":
        return self.neofetch_lolcat.get_active()
    elif util == "fastfetch":
        return self.fastfetch_lolcat.get_active()
    elif util == "screenfetch":
        return self.screenfetch_lolcat.get_active()
    elif util == "ufetch":
        return self.ufetch_lolcat.get_active()
    elif util == "ufetch-arco":
        return self.ufetch_arco_lolcat.get_active()
    elif util == "pfetch":
        return self.pfetch_lolcat.get_active()
    elif util == "paleofetch":
        return self.paleofetch_lolcat.get_active()
    elif util == "alsi":
        return self.alsi_lolcat.get_active()
    elif util == "hfetch":
        return self.hfetch_lolcat.get_active()
    elif util == "fetch":
        return self.fetch_lolcat.get_active()
    elif util == "sfetch":
        return self.sfetch_lolcat.get_active()
    elif util == "sysinfo":
        return self.sysinfo_lolcat.get_active()
    elif util == "sysinfo-retro":
        return self.sysinfo_retro_lolcat.get_active()
    elif util == "cpufetch":
        return self.cpufetch_lolcat.get_active()
    elif util == "hyfetch":
        return self.hyfetch_lolcat.get_active()
    elif util == "colorscript random":  # no lolcat for colorscripts
        return False
    else:
        return False


def install_util(self, util):
    """install utility"""
    if util == "fastfetch":
        fn.install_package(self, "fastfetch-git")
    elif util == "lolcat":
        fn.install_package(self, "lolcat")
        
        
def get_config_file():
    """get config file"""
    if fn.get_shell() == "bash":
        return fn.bash_config
    elif fn.get_shell() == "zsh":
        return fn.zsh_config
    else:
        return fn.fish_config
