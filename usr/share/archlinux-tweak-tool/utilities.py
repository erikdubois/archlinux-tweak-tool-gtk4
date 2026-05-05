# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=R0911,R1705,

import functions as fn

# This function has one job, and one job only; ensure that check
# boxes match what is passed to it, based on the logic from the calling function


def set_util_state(self, util, util_state, lolcat_state):
    fn.log_subsection(f"Set utility state: {util}")
    fn.debug_print(f"set_util_state: util={util} state={util_state} lolcat={lolcat_state}")
    import fastfetch

    if util == "fastfetch":
        self.fast_util.set_state(util_state)
        self.fast_lolcat.set_state(lolcat_state)
        fastfetch.write_configs(util_state, lolcat_state)


def get_util_state(self, util):
    """get utility state"""
    if util == "fastfetch":
        return self.fastfetch_util.get_active()
    return False


def get_lolcat_state(self, util):
    """get lolcat state"""
    if util == "fastfetch":
        return self.fastfetch_lolcat.get_active()
    return False


def install_util(self, util):
    """install utility"""
    if util == "fastfetch":
        fn.install_package(self, "fastfetch-git")
    elif util == "lolcat":
        fn.install_package(self, "lolcat")


def get_config_file():
    """get config file"""
    shell = fn.get_shell()
    if shell == "bash":
        return fn.bash_config
    elif shell == "zsh":
        return fn.zsh_config
    else:
        return fn.fish_config
