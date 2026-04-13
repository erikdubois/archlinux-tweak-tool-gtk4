# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================


def gui(self, Gtk, vboxstack13, fn):
    """create a gui"""

    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    lbl1 = Gtk.Label(xalign=0)
    lbl1.set_text("Autostart")
    lbl1.set_name("title")
    hbox3.append(lbl1)

    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox4.append(hseparator)

    toplabelbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    labelbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    labelbox.set_vexpand(True)
    lbls = Gtk.Label(xalign=0)
    lbls.set_text("Current content of ~/.config/autostart/")
    toplabelbox.append(lbls)

    files = [x.replace(".desktop", "") for x in fn.listdir(fn.autostart)]
    mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

    self.vvbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    self.vvbox.set_name("vbox")

    scrolled_window.set_child(self.vvbox)
    scrolled_window.set_hexpand(True)
    scrolled_window.set_vexpand(True)
    mainbox.append(scrolled_window)

    self.load_autostart(files)

    # ==========================================
    #              Button
    # ==========================================
    lbl1 = Gtk.Label(label="Name")
    lbl2 = Gtk.Label(label="Command")
    lbl3 = Gtk.Label(label="Comment")

    self.txtbox1 = Gtk.Entry()  # Name
    self.txtbox2 = Gtk.Entry()  # EXEC
    self.txtbox3 = Gtk.Entry()  # Comment
    self.txtbox1.set_size_request(180, 0)
    self.txtbox2.set_size_request(180, 0)
    self.txtbox3.set_size_request(180, 0)
    self.txtbox1.connect("changed", self.on_comment_changed)
    self.txtbox2.connect("changed", self.on_comment_changed)

    bbutton = Gtk.Button(label="...")
    self.abutton = Gtk.Button(label="Add")
    self.abutton.set_size_request(140, 0)
    self.abutton.set_sensitive(False)

    bbutton.connect("clicked", self.on_exec_browse)

    self.abutton.connect("clicked", self.on_add_autostart)

    vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
    vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
    vbox4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
    vbox5 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
    vbox6 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)

    vbox2.append(lbl1)
    vbox2.append(self.txtbox1)

    vbox3.append(lbl2)
    vbox3.append(self.txtbox2)

    vbox4.append(lbl3)
    vbox4.append(self.txtbox3)

    vbox5.append(Gtk.Label(label=""))
    vbox5.append(bbutton)  # pack_end
    vbox6.append(Gtk.Label(label=""))
    vbox6.append(self.abutton)  # pack_end

    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    vbox2.set_margin_start(5)
    vbox2.set_margin_end(5)
    hbox2.append(vbox2)
    hbox2.append(vbox3)
    hbox2.append(vbox5)
    vbox4.set_margin_start(5)
    vbox4.set_margin_end(5)
    hbox2.append(vbox4)
    vbox6.set_margin_start(5)
    vbox6.set_margin_end(5)
    hbox2.append(vbox6)

    vboxstack13.append(hbox3)
    vboxstack13.append(hbox4)
    vboxstack13.append(toplabelbox)
    mainbox.set_hexpand(True)
    vboxstack13.append(mainbox)
    vboxstack13.append(labelbox)
    vboxstack13.append(hbox2)
