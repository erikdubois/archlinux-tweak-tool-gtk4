# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0103,
import functools
import fastfetch
import utilities
import functions_startup

import desktopr_gui


def init_fastfetch_lazy_load(self, fn):
    """Lazy load fastfetch switch states when page is visible"""
    try:
        import time
        start = time.time()
        fastfetch_enabled = fastfetch.get_term_rc() and fn.path.exists("/usr/bin/fastfetch")
        lolcat_enabled = False
        if fastfetch_enabled:
            config = utilities.get_config_file()
            if config:
                with open(config, "r", encoding="utf-8") as f:
                    content = f.read()
                lolcat_enabled = "fastfetch | lolcat" in content
        self.ff_initializing = True
        if hasattr(self, 'fast_util'):
            self.fast_util.set_active(fastfetch_enabled)
        if hasattr(self, 'fast_lolcat'):
            self.fast_lolcat.set_active(lolcat_enabled)
            self.fast_lolcat.set_sensitive(fastfetch_enabled)
        self.ff_initializing = False
        elapsed = time.time() - start
        fn.debug_print(f"[LAZY] Fastfetch page switches loaded in {elapsed:.3f}s")
    except Exception as e:
        fn.debug_print(f"[LAZY] Fastfetch lazy load failed: {e}")


def gui(self, Gtk, GdkPixbuf, vboxstack8, fastfetch, fn, base_dir):
    """create a gui"""
    from gi.repository import Gdk

    # Setup fastfetch config on-demand
    functions_startup.setup_fastfetch_config()

    img_load = desktopr_gui.IMAGE_PREVIEW_LOAD
    img_min = desktopr_gui.IMAGE_PREVIEW_MIN
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl1 = Gtk.Label(xalign=0)
    lbl1.set_text("Fastfetch Editor")
    lbl1.set_name("title")
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox4.append(hseparator)
    hbox3.append(lbl1)

    # ==========================================================
    #                     fastfetch
    # ==========================================================

    hbox23 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    warning_label = Gtk.Label(xalign=0)
    warning_label.set_markup(
        "<b>Some distros have their own configuration and/or application, investigate</b>"
    )
    warning_label.set_margin_start(10)
    warning_label.set_margin_end(10)
    hbox23.append(warning_label)

    self.fast_util = Gtk.Switch()
    fast_util_label = Gtk.Label(xalign=0)
    fast_util_label.set_markup("Fastfetch install/enable")

    self.fast_lolcat = Gtk.Switch()
    fast_lolcat_label = Gtk.Label(xalign=0)
    fast_lolcat_label.set_markup("Lolcat install/enable")

    self.fast_util.connect("notify::active", functools.partial(fastfetch.on_fast_util_toggled, self))
    self.fast_lolcat.connect("notify::active", functools.partial(fastfetch.on_fast_lolcat_toggled, self))

    applyfastfetch = Gtk.Button(label="Apply Fastfetch configuration")
    resetnormalfastfetch = Gtk.Button(label="Reset your Fastfetch backup")
    resetattfastfetch = Gtk.Button(label="Reset Fastfetch (ATT defaults)")

    applyfastfetch.connect("clicked", functools.partial(fastfetch.on_apply_fast, self))
    resetnormalfastfetch.connect("clicked", functools.partial(fastfetch.on_reset_fast, self))
    resetattfastfetch.connect("clicked", functools.partial(fastfetch.on_reset_fast_att, self))

    hbox22 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    hbox22.set_margin_top(10)
    hbox24 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox25 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    hbox25.set_margin_top(10)
    self.hbox26 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    hbox27 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

    self.os = Gtk.CheckButton(label="Show os")
    self.host = Gtk.CheckButton(label="Show hostname")
    self.kernel = Gtk.CheckButton(label="Show kernel")
    self.uptime = Gtk.CheckButton(label="Show uptime")
    self.packages = Gtk.CheckButton(label="Show packages")
    self.shell = Gtk.CheckButton(label="Show shell")
    self.display = Gtk.CheckButton(label="Show display")
    self.de = Gtk.CheckButton(label="Show de")
    self.wm = Gtk.CheckButton(label="Show wm")
    self.wmtheme = Gtk.CheckButton(label="Show wm theme")
    self.themes = Gtk.CheckButton(label="Show theme")
    self.icons = Gtk.CheckButton(label="Show icons")
    self.term = Gtk.CheckButton(label="Show terminal")
    self.termfont = Gtk.CheckButton(label="Show terminal font")
    self.cpu = Gtk.CheckButton(label="Show cpu")
    self.gpu = Gtk.CheckButton(label="Show gpu")
    self.mem = Gtk.CheckButton(label="Show memory")
    self.swap = Gtk.CheckButton(label="Show swap")
    self.cursor = Gtk.CheckButton(label="Show cursor")
    self.font = Gtk.CheckButton(label="Show font")
    self.disks = Gtk.CheckButton(label="Show disks")
    self.lIP = Gtk.CheckButton(label="Show local ip")
    self.PIP = Gtk.CheckButton(label="Show public ip")
    self.local = Gtk.CheckButton(label="Show locale")
    self.batt = Gtk.CheckButton(label="Show battery")
    self.pwr = Gtk.CheckButton(label="Show power adapter")
    self.title = Gtk.CheckButton(label="Show title")
    self.cblocks = Gtk.CheckButton(label="Show color blocks")

    fastfetch.get_checkboxes(self)

    hbox21 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label21 = Gtk.Label()
    label21.set_text("Or choose what to select with a button")
    btn_all_selection = Gtk.Button(label="All")
    btn_all_selection.connect("clicked", functools.partial(fastfetch.on_click_fastfetch_all_selection, self))
    btn_normal_selection = Gtk.Button(label="Normal")
    btn_normal_selection.connect("clicked", functools.partial(fastfetch.on_click_fastfetch_normal_selection, self))
    btn_small_selection = Gtk.Button(label="Small")
    btn_small_selection.connect("clicked", functools.partial(fastfetch.on_click_fastfetch_small_selection, self))
    btn_none_selection = Gtk.Button(label="None")
    btn_none_selection.connect("clicked", functools.partial(fastfetch.on_click_fastfetch_none_selection, self))
    label21.set_margin_start(10)
    label21.set_margin_end(10)
    hbox21.append(label21)
    btn_all_selection.set_margin_start(10)
    btn_all_selection.set_margin_end(10)
    hbox21.append(btn_all_selection)  # pack_end
    btn_normal_selection.set_margin_start(10)
    btn_normal_selection.set_margin_end(10)
    hbox21.append(btn_normal_selection)  # pack_end
    btn_small_selection.set_margin_start(10)
    btn_small_selection.set_margin_end(10)
    hbox21.append(btn_small_selection)  # pack_end
    btn_none_selection.set_margin_start(10)
    btn_none_selection.set_margin_end(10)
    hbox21.append(btn_none_selection)  # pack_end

    hbox9 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox9_label = Gtk.Label(xalign=0)
    hbox9_label.set_markup(
        "<b>Distro specific:  </b>" + fn.change_distro_label(fn.distr)
    )
    hbox9_label.set_margin_start(10)
    hbox9_label.set_margin_end(10)
    hbox9.append(hbox9_label)

    hbox28 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label28 = Gtk.Label()
    label28.set_text(
        "AmOS is using a personalized fastfetch application\n\
Switch to the default fastfetch to use this tab"
    )
    label28.set_margin_start(10)
    label28.set_margin_end(10)
    hbox28.append(label28)

    hbox29 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    label29 = Gtk.Label()
    label29.set_text(
        "Archcraft is using a personalized fastfetch configuration\n\
Switch to the default fastfetch to use this tab - delete the ~/.config/fastfetch/config.conf"
    )
    label29.set_margin_start(10)
    label29.set_margin_end(10)
    hbox29.append(label29)

    flowbox = Gtk.FlowBox()
    flowbox.set_valign(Gtk.Align.START)
    flowbox.set_max_children_per_line(10)
    flowbox.set_selection_mode(Gtk.SelectionMode.NONE)

    flowbox.append(self.title)
    flowbox.append(self.os)
    flowbox.append(self.host)
    flowbox.append(self.kernel)
    flowbox.append(self.uptime)
    flowbox.append(self.packages)
    flowbox.append(self.shell)
    flowbox.append(self.display)
    flowbox.append(self.de)
    flowbox.append(self.wm)
    flowbox.append(self.wmtheme)
    flowbox.append(self.themes)
    flowbox.append(self.icons)
    flowbox.append(self.font)
    flowbox.append(self.cursor)
    flowbox.append(self.term)
    flowbox.append(self.termfont)
    flowbox.append(self.cpu)
    flowbox.append(self.gpu)
    flowbox.append(self.mem)
    flowbox.append(self.swap)
    flowbox.append(self.disks)
    flowbox.append(self.lIP)
    flowbox.append(self.PIP)
    flowbox.append(self.batt)
    flowbox.append(self.pwr)
    flowbox.append(self.local)
    flowbox.append(self.cblocks)

    flowbox.set_hexpand(True)
    flowbox.set_vexpand(True)
    flowbox.set_margin_start(10)
    flowbox.set_margin_end(10)
    hbox25.append(flowbox)

    fastfetch_image = Gtk.Picture()
    try:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            base_dir + "/images/fastfetch.jpg",
            img_load,
            img_load,
        )
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        fastfetch_image.set_paintable(texture)
    except Exception as e:
        fn.debug_print(f"Failed to load fastfetch image: {e}")
    fastfetch_image.set_content_fit(Gtk.ContentFit.SCALE_DOWN)
    fastfetch_image.set_size_request(img_min, img_min)
    fastfetch_image.set_hexpand(True)
    fastfetch_image.set_vexpand(False)
    fastfetch_image.set_halign(Gtk.Align.CENTER)
    fastfetch_image.set_valign(Gtk.Align.CENTER)
    fastfetch_image.set_margin_start(10)
    fastfetch_image.set_margin_end(10)
    fastfetch_image.set_margin_top(10)
    fastfetch_image.set_margin_bottom(10)

    fast_util_label.set_margin_start(10)
    fast_util_label.set_margin_end(10)
    hbox27.append(fast_util_label)
    self.fast_util.set_margin_start(30)
    self.fast_util.set_margin_end(30)
    hbox27.append(self.fast_util)
    hbox27.append(fast_lolcat_label)
    self.fast_lolcat.set_margin_start(30)
    self.fast_lolcat.set_margin_end(30)
    hbox27.append(self.fast_lolcat)

    hbox24.append(resetnormalfastfetch)
    spacer1 = Gtk.Box()
    spacer1.set_hexpand(True)
    hbox24.append(spacer1)
    hbox24.append(resetattfastfetch)
    spacer2 = Gtk.Box()
    spacer2.set_hexpand(True)
    hbox24.append(spacer2)
    hbox24.append(applyfastfetch)

    vboxstack8.append(hbox3)
    vboxstack8.append(hbox4)
    vboxstack8.append(hbox23)
    vboxstack8.append(hbox27)
    vboxstack8.append(hbox22)
    vboxstack8.append(hbox25)
    vboxstack8.append(fastfetch_image)
    vboxstack8.append(hbox21)

    if fn.distr == "amos":
        vboxstack8.append(hbox9)
        vboxstack8.append(hbox28)

    if fn.distr == "archcraft":
        vboxstack8.append(hbox9)
        vboxstack8.append(hbox29)

    vboxstack8.append(hbox24)  # pack_end

    fn.GLib.idle_add(init_fastfetch_lazy_load, self, fn, priority=fn.GLib.PRIORITY_LOW)
