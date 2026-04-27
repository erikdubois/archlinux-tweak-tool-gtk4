# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================


def gui(self, Gtk, vboxstack3, fn):
    """create a gui"""
    # Title
    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_title = Gtk.Label(xalign=0)
    lbl_title.set_text("Privacy/Security")
    lbl_title.set_name("title")
    hbox_title.append(lbl_title)

    # Separator
    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox_sep.append(hseparator)

    # ========== SECTION 1: CONTENT BLOCKING ==========

    hbox_section1_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_section1_title = Gtk.Label(xalign=0)
    label_section1_title.set_markup("<b>Content Blocking</b>")
    label_section1_title.set_margin_start(10)
    label_section1_title.set_margin_end(10)
    hbox_section1_title.append(label_section1_title)

    hbox_ublock = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_ublock = Gtk.Label(xalign=0)
    label_ublock.set_markup("Install/remove uBlock Origin")
    label_ublock.set_margin_start(30)
    label_ublock.set_margin_end(10)
    label_ublock.set_halign(Gtk.Align.START)
    label_ublock.set_hexpand(True)

    state = fn.ublock_get_state(self)

    self.firefox_ublock_switch = Gtk.Switch()
    self.firefox_ublock_switch.connect("notify::active", self.set_ublock_firefox)
    self.firefox_ublock_switch.set_active(state)
    self.firefox_ublock_switch.set_margin_start(10)
    self.firefox_ublock_switch.set_margin_end(10)
    self.firefox_ublock_switch.set_halign(Gtk.Align.END)

    hbox_ublock.append(label_ublock)
    hbox_ublock.append(self.firefox_ublock_switch)

    # ========== SECTION 2: NETWORK & TRACKING PROTECTION ==========

    hbox_section2_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    label_section2_title = Gtk.Label(xalign=0)
    label_section2_title.set_markup("<b>Network & Tracking Protection</b>")
    label_section2_title.set_margin_start(10)
    label_section2_title.set_margin_end(10)
    hbox_section2_title.append(label_section2_title)

    hbox_hblock = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    label_hblock = Gtk.Label(xalign=0)
    label_hblock.set_text(
        "Enable/install hblock - Your orignal /etc/hosts file can be found in /etc/hosts.bak"
    )

    self.label7 = Gtk.Label(xalign=0)
    self.label7.set_visible(False)
    self.progress = Gtk.ProgressBar()
    self.progress.set_pulse_step(0.2)
    self.progress.set_visible(False)

    state = fn.hblock_get_state(self)

    self.hbswich = Gtk.Switch()
    self.hbswich.connect("notify::active", self.set_hblock)
    self.hbswich.set_active(state)

    label_hblock.set_margin_start(30)
    label_hblock.set_margin_end(10)
    label_hblock.set_hexpand(True)
    label_hblock.set_halign(Gtk.Align.START)
    hbox_hblock.append(label_hblock)
    self.hbswich.set_margin_start(10)
    self.hbswich.set_margin_end(10)
    self.hbswich.set_halign(Gtk.Align.END)
    hbox_hblock.append(self.hbswich)

    # ========== APPEND TO VBOX ==========

    vboxstack3.append(hbox_title)
    vboxstack3.append(hbox_sep)

    vboxstack3.append(hbox_section1_title)
    vboxstack3.append(hbox_ublock)

    vboxstack3.append(hbox_section2_title)
    vboxstack3.append(hbox_hblock)

    vboxstack3.append(self.label7)
    vboxstack3.append(self.progress)
