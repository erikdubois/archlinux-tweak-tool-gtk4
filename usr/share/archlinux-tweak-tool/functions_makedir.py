# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn


def ensure_root_config_dirs():
    fn.log_subsection("Ensuring /root/.config directories")
    fn.debug_print("ensure_root_config_dirs() START")
    fn.debug_print("=" * 75)

    if not fn.path.isdir("/root/.config/"):
        try:
            fn.debug_print("Creating /root/.config directory")
            fn.makedirs("/root/.config", 0o766)
            fn.debug_print("✓ /root/.config created")
        except Exception as error:
            fn.debug_print(f"Error creating /root/.config: {error}")
            fn.log_error(str(error))
    else:
        fn.debug_print("/root/.config already exists")

    if not fn.path.isdir("/root/.config/gtk-3.0"):
        try:
            fn.debug_print("Creating /root/.config/gtk-3.0 directory")
            fn.makedirs("/root/.config/gtk-3.0", 0o766)
            fn.debug_print("✓ /root/.config/gtk-3.0 created")
        except Exception as error:
            fn.debug_print(f"Error creating /root/.config/gtk-3.0: {error}")
            fn.log_error(str(error))
    else:
        fn.debug_print("/root/.config/gtk-3.0 already exists")

    if not fn.path.isdir("/root/.config/gtk-4.0"):
        try:
            fn.debug_print("Creating /root/.config/gtk-4.0 directory")
            fn.makedirs("/root/.config/gtk-4.0", 0o766)
            fn.debug_print("✓ /root/.config/gtk-4.0 created")
        except Exception as error:
            fn.debug_print(f"Error creating /root/.config/gtk-4.0: {error}")
            fn.log_error(str(error))
    else:
        fn.debug_print("/root/.config/gtk-4.0 already exists")

    if not fn.path.isdir("/root/.config/xsettingsd"):
        try:
            fn.debug_print("Creating /root/.config/xsettingsd directory")
            fn.makedirs("/root/.config/xsettingsd", 0o766)
            fn.debug_print("✓ /root/.config/xsettingsd created")
        except Exception as error:
            fn.debug_print(f"Error creating /root/.config/xsettingsd: {error}")
            fn.log_error(str(error))
    else:
        fn.debug_print("/root/.config/xsettingsd already exists")

    fn.debug_print("=" * 75)
    fn.debug_print("ensure_root_config_dirs() END")
    fn.debug_print("=" * 75)


def ensure_app_dirs():
    fn.log_subsection("Ensuring application directories")
    fn.debug_print("ensure_app_dirs() START")
    fn.debug_print("=" * 75)

    if not fn.path.isdir(fn.log_dir):
        try:
            fn.debug_print(f"Creating log directory: {fn.log_dir}")
            fn.mkdir(fn.log_dir)
            fn.debug_print(f"✓ {fn.log_dir} created")
        except Exception as error:
            fn.debug_print(f"Error creating log directory: {error}")
            fn.log_error(str(error))
    else:
        fn.debug_print(f"{fn.log_dir} already exists")

    if not fn.path.isdir(fn.att_log_dir):
        try:
            fn.debug_print(f"Creating ATT log directory: {fn.att_log_dir}")
            fn.mkdir(fn.att_log_dir)
            fn.debug_print(f"✓ {fn.att_log_dir} created")
        except Exception as error:
            fn.debug_print(f"Error creating ATT log directory: {error}")
            fn.log_error(str(error))
    else:
        fn.debug_print(f"{fn.att_log_dir} already exists")

    fastfetch_dir = fn.home + "/.config/fastfetch"
    if not fn.path.exists(fastfetch_dir):
        try:
            fn.debug_print(f"Creating fastfetch directory: {fastfetch_dir}")
            fn.makedirs(fastfetch_dir, 0o766)
            fn.permissions(fastfetch_dir)
            fn.debug_print(f"✓ {fastfetch_dir} created")
        except Exception as error:
            fn.debug_print(f"Error creating fastfetch directory: {error}")
            fn.log_error(str(error))
    else:
        fn.debug_print(f"{fastfetch_dir} already exists")

    autostart_dir = fn.home + "/.config/autostart"
    if not fn.path.exists(autostart_dir):
        try:
            fn.debug_print(f"Creating autostart directory: {autostart_dir}")
            fn.makedirs(autostart_dir, 0o766)
            fn.permissions(autostart_dir)
            fn.debug_print(f"✓ {autostart_dir} created")
        except Exception as error:
            fn.debug_print(f"Error creating autostart directory: {error}")
            fn.log_error(str(error))
    else:
        fn.debug_print(f"{autostart_dir} already exists")

    att_config_dir = fn.home + "/.config/archlinux-tweak-tool"
    if not fn.path.isdir(att_config_dir):
        try:
            fn.debug_print(f"Creating ATT config directory: {att_config_dir}")
            fn.makedirs(att_config_dir, 0o766)
            fn.permissions(att_config_dir)
            fn.debug_print(f"✓ {att_config_dir} created")
        except Exception as error:
            fn.debug_print(f"Error creating ATT config directory: {error}")
            fn.log_error(str(error))
    else:
        fn.debug_print(f"{att_config_dir} already exists")

    fn.debug_print("=" * 75)
    fn.debug_print("ensure_app_dirs() END")
    fn.debug_print("=" * 75)
