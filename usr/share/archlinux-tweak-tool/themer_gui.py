# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0103,W0612

import functools
import desktopr_gui
import themer


def init_themer_lazy_load(self, fn):
    """Lazy load themer switch states when page is visible"""
    try:
        import time
        start = time.time()
        if hasattr(self, 'poly'):
            if fn.os.path.isfile(fn.i3wm_config) and fn.check_package_installed(
                "edu-i3-git"
            ):
                if themer.check_polybar(themer.get_list(fn.i3wm_config)):
                    self.poly.set_active(True)
        elapsed = time.time() - start
        fn.debug_print(f"[LAZY] Themer page switches loaded in {elapsed:.3f}s")
    except Exception:
        pass


def refresh_themer_dropdowns(self, fn, themer):
    fn.log_info("Refreshing themer dropdowns after desktop change...")

    i3_ok = fn.os.path.isfile(fn.i3wm_config) and fn.check_package_installed("edu-i3-git")
    if i3_ok:
        i3_list = themer.get_list(fn.i3wm_config)
        themer.get_i3_themes(self.i3_combo, i3_list)
    self.i3_combo.set_sensitive(i3_ok)
    self.applyi3.set_sensitive(i3_ok)
    self.reseti3.set_sensitive(i3_ok)
    self.poly.set_sensitive(i3_ok)

    aw_ok = fn.os.path.isfile(fn.awesome_config) and fn.check_package_installed("edu-awesome-git")
    if aw_ok:
        try:
            awesome_list = themer.get_list(fn.awesome_config)
            awesome_lines = themer.get_awesome_themes(awesome_list)
            self.store.clear()
            for x, theme in enumerate(awesome_lines):
                self.store.append([x, theme])
        except Exception:
            pass
    self.awesome_combo.set_sensitive(aw_ok)
    self.applyawesome.set_sensitive(aw_ok)
    self.resetawesome.set_sensitive(aw_ok)

    qt_ok = fn.path_check(fn.qtile_config_theme) and fn.check_package_installed("edu-qtile-git")
    if qt_ok:
        qtile_list = themer.get_list(fn.qtile_config)
        themer.get_qtile_themes(self.qtile_combo, qtile_list)
    self.qtile_combo.set_sensitive(qt_ok)
    self.applyqtile.set_sensitive(qt_ok)
    self.resetqtile.set_sensitive(qt_ok)

    lft_ok = fn.os.path.isfile(fn.leftwm_config) and fn.check_package_installed("edu-leftwm-git")
    self.leftwm_combo.set_sensitive(lft_ok)
    self.applyleftwm.set_sensitive(lft_ok)
    self.resetleftwm.set_sensitive(lft_ok)
    self.removeleftwm.set_sensitive(lft_ok)

    fn.log_success("Themer dropdowns refreshed")


def gui(self, Gtk, GdkPixbuf, vboxstack10, themer, fn, base_dir):
    """create a gui"""
    from gi.repository import Gdk

    # Match desktop installer preview: decode resolution vs minimum Gtk.Picture size.
    img_load = desktopr_gui.IMAGE_PREVIEW_LOAD
    img_min = desktopr_gui.IMAGE_PREVIEW_MIN
    hbox6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox7 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl1 = Gtk.Label(xalign=0)
    lbl1.set_text("Theme Switcher")
    lbl1.set_name("title")
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hseparator.set_vexpand(False)
    hbox7.append(hseparator)
    hbox6.append(lbl1)

    if fn.os.path.isfile(fn.i3wm_config) and fn.check_package_installed(
        "edu-i3-git"
    ):
        i3_list = themer.get_list(fn.i3wm_config)
    if fn.os.path.isfile(fn.awesome_config) and fn.check_package_installed(
        "edu-awesome-git"
    ):
        awesome_list = themer.get_list(fn.awesome_config)
    if fn.path_check(fn.qtile_config_theme) and fn.check_package_installed(
        "edu-qtile-git"
    ):
        qtile_list = themer.get_list(fn.qtile_config)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

    vboxstack1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack1.set_hexpand(True)
    vboxstack1.set_vexpand(True)
    vboxstack2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack2.set_hexpand(True)
    vboxstack2.set_vexpand(True)
    vboxstack3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack3.set_hexpand(True)
    vboxstack3.set_vexpand(True)
    vboxstack4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vboxstack4.set_hexpand(True)
    vboxstack4.set_vexpand(True)

    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
    stack.set_transition_duration(350)
    stack.set_hhomogeneous(False)
    stack.set_vhomogeneous(False)

    stack_switcher = Gtk.StackSwitcher()
    stack_switcher.set_orientation(Gtk.Orientation.HORIZONTAL)
    stack_switcher.set_stack(stack)

    # ==================================================================
    #                       I3WM TAB
    # ==================================================================

    label3 = Gtk.Label()
    label3.set_markup(
        "Reload your window manager with <b>Super + Shift + R</b>\
 after you make your changes..\nInstall the desktop with ATT to theme it."
    )

    label = Gtk.Label(label="Select theme")
    i3_model = Gtk.StringList()
    self.i3_combo = Gtk.DropDown(model=i3_model)
    self.i3_combo.set_size_request(280, 0)
    if fn.os.path.isfile(fn.i3wm_config) and fn.check_package_installed(
        "edu-i3-git"
    ):
        themer.get_i3_themes(self.i3_combo, i3_list)

    vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    vbox2.append(self.i3_combo)

    self.applyi3 = Gtk.Button(label="Apply theme")
    self.applyi3.connect("clicked", functools.partial(themer.i3wm_apply_clicked, self))
    self.reseti3 = Gtk.Button(label="Reset")
    self.reseti3.connect("clicked", functools.partial(themer.i3wm_reset_clicked, self))

    lbls = Gtk.Label(label="Toggle polybar")
    self.poly = Gtk.Switch()
    self.poly.connect("notify::active", functools.partial(themer.on_polybar_toggle, self))

    if not fn.os.path.isfile(fn.i3wm_config) or not fn.check_package_installed(
        "edu-i3-git"
    ):
        self.applyi3.set_sensitive(False)
        self.reseti3.set_sensitive(False)
        self.poly.set_sensitive(False)

    label.set_margin_start(10)
    label.set_margin_end(10)
    label.set_hexpand(True)
    hbox1.append(label)
    vbox2.set_margin_start(10)
    vbox2.set_margin_end(10)
    hbox1.append(vbox2)  # pack_end

    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
        base_dir + "/images/i3-sample.jpg", img_load, img_load
    )
    if self.i3_combo.get_selected_item() is None:
        pass
    elif fn.os.path.isfile(
        base_dir + "/themer_data/i3" + fn.get_combo_text(self.i3_combo) + ".jpg"
    ):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            base_dir + "/themer_data/i3/" + fn.get_combo_text(self.i3_combo) + ".jpg",
            img_load,
            img_load,
        )
    texture = Gdk.Texture.new_for_pixbuf(pixbuf)
    i3_image = Gtk.Picture.new_for_paintable(texture)
    i3_image.set_content_fit(Gtk.ContentFit.SCALE_DOWN)
    i3_image.set_size_request(img_min, img_min)
    i3_image.set_halign(Gtk.Align.CENTER)
    i3_image.set_valign(Gtk.Align.CENTER)
    i3_image.set_hexpand(True)
    i3_image.set_vexpand(False)

    self.i3_combo.connect(
        "notify::selected",
        lambda w, _p, img, tt, ab, iw, ih: fn.update_image(self, w, img, tt, ab, iw, ih),
        i3_image,
        "i3",
        base_dir,
        img_load,
        img_load,
    )

    hbox2.append(self.reseti3)  # pack_end
    hbox2.append(self.applyi3)  # pack_end

    hbox3.append(lbls)  # pack_end
    hbox3.append(self.poly)  # pack_end

    hbox1.set_margin_start(10)
    hbox1.set_margin_end(10)
    vboxstack1.append(hbox1)
    vboxstack1.append(hbox3)
    vboxstack1.append(i3_image)
    label3.set_hexpand(True)
    label3.set_vexpand(True)
    vboxstack1.append(label3)
    vboxstack1.append(hbox2)  # pack_end

    # ==================================================================
    #                       AWESOMEWM TAB
    # ==================================================================

    label4 = Gtk.Label()
    label4.set_markup(
        "Reload your window manager with <b>Super + Shift + R</b>\
 after you make your changes..\nInstall the desktop with ATT to theme it."
    )

    label2 = Gtk.Label(label="Select theme")
    self.store = Gtk.ListStore(int, str)
    if fn.os.path.isfile(fn.awesome_config) and fn.check_package_installed(
        "edu-awesome-git"
    ):
        try:
            awesome_lines = themer.get_awesome_themes(awesome_list)
            for x, theme in enumerate(awesome_lines):
                self.store.append([x, theme])
        except Exception:
            pass

    self.awesome_combo = Gtk.ComboBox.new_with_model(self.store)
    self.awesome_combo.set_size_request(180, 0)
    renderer_text = Gtk.CellRendererText()

    if fn.os.path.isfile(fn.awesome_config) and fn.check_package_installed(
        "edu-awesome-git"
    ):
        try:
            val = int(
                themer.get_value(awesome_list, "local chosen_theme =")
                .replace("themes[", "")
                .replace("]", "")
            )
            self.awesome_combo.set_active(val - 1)
        except Exception:
            pass

    self.awesome_combo.pack_start(renderer_text, False)
    self.awesome_combo.add_attribute(renderer_text, "text", 1)
    # self.awesome_combo.connect("changed", self.on_awesome_change)
    self.awesome_combo.set_entry_text_column(1)

    vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    vbox4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox5.set_hexpand(True)
    hbox5.set_vexpand(True)

    vbox3.append(self.awesome_combo)
    label2.set_margin_start(10)
    label2.set_margin_end(10)
    label2.set_hexpand(True)
    hbox2.append(label2)
    vbox3.set_margin_start(10)
    vbox3.set_margin_end(10)
    hbox2.append(vbox3)  # pack_end

    frame = Gtk.Frame(label="")
    frmlbl = frame.get_label_widget()
    frmlbl.set_markup("<b>Preview</b>")

    tree_iter = self.awesome_combo.get_active_iter()
    if tree_iter is not None:
        model = self.awesome_combo.get_model()
        # row_id is used for image
        row_id, name = model[tree_iter][:2]

    if fn.os.path.isfile(fn.awesome_config) and fn.check_package_installed(
        "edu-awesome-git"
    ):
        try:
            if tree_iter is not None:
                pimage = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    base_dir + "/themer_data/awesomewm/" + name + ".jpg",
                    img_load,
                    img_load,
                )
            else:
                pimage = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    base_dir + "/themer_data/awesomewm/multicolor.jpg",
                    img_load,
                    img_load,
                )
        except Exception:
            pimage = GdkPixbuf.Pixbuf.new_from_file_at_size(
                base_dir + "/themer_data/awesomewm/multicolor.jpg",
                img_load,
                img_load,
            )
    else:
        pimage = GdkPixbuf.Pixbuf.new_from_file_at_size(
            base_dir + "/themer_data/awesomewm/multicolor.jpg",
            img_load,
            img_load,
        )

    texture = Gdk.Texture.new_for_pixbuf(pimage)
    self.image = Gtk.Picture.new_for_paintable(texture)
    self.image.set_content_fit(Gtk.ContentFit.SCALE_DOWN)
    self.image.set_size_request(img_min, img_min)
    self.image.set_halign(Gtk.Align.CENTER)
    self.image.set_valign(Gtk.Align.CENTER)
    self.image.set_hexpand(True)
    self.image.set_vexpand(False)

    self.awesome_combo.connect(
        "changed",
        functools.partial(fn.update_image, self),
        self.image,
        "awesome",
        base_dir,
        img_load,
        img_load,
    )

    frame.set_name("awesome")
    frame.set_child(self.image)

    frame.set_hexpand(True)
    frame.set_vexpand(True)
    frame.set_margin_start(10)
    frame.set_margin_end(10)
    hbox5.append(frame)

    self.applyawesome = Gtk.Button(label="Apply theme")
    self.applyawesome.connect("clicked", functools.partial(themer.awesome_apply_clicked, self))
    self.resetawesome = Gtk.Button(label="Reset")
    self.resetawesome.connect("clicked", functools.partial(themer.awesome_reset_clicked, self))

    if not fn.os.path.isfile(fn.awesome_config) or not fn.check_package_installed(
        "edu-awesome-git"
    ):
        self.applyawesome.set_sensitive(False)
        self.resetawesome.set_sensitive(False)

    hbox4.append(self.resetawesome)  # pack_end
    hbox4.append(self.applyawesome)  # pack_end

    hbox2.set_margin_start(10)
    hbox2.set_margin_end(10)
    vboxstack2.append(hbox2)
    hbox5.set_margin_start(10)
    hbox5.set_margin_end(10)
    vboxstack2.append(hbox5)
    label4.set_hexpand(True)
    label4.set_vexpand(True)
    label4.set_margin_start(10)
    label4.set_margin_end(10)
    vboxstack2.append(label4)
    vboxstack2.append(hbox4)  # pack_end

    # ==================================================================
    #                       Qtile TAB
    # ==================================================================

    label5 = Gtk.Label()
    label5.set_markup(
        "Reload your window manager with <b>Super + Shift\
 + R</b> after you make your changes.\nInstall the desktop with ATT to theme it."
    )

    labelqt = Gtk.Label(label="Select theme")
    qtile_model = Gtk.StringList()
    self.qtile_combo = Gtk.DropDown(model=qtile_model)
    self.qtile_combo.set_size_request(280, 0)
    if fn.path_check(fn.qtile_config_theme) and fn.check_package_installed(
        "edu-qtile-git"
    ):
        themer.get_qtile_themes(self.qtile_combo, qtile_list)

    vbox4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    hbox8 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox9 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox10 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    vbox4.append(self.qtile_combo)

    self.applyqtile = Gtk.Button(label="Apply theme")
    self.applyqtile.connect("clicked", functools.partial(themer.qtile_apply_clicked, self))
    self.resetqtile = Gtk.Button(label="Reset")
    self.resetqtile.connect("clicked", functools.partial(themer.qtile_reset_clicked, self))

    if not fn.path_check(fn.qtile_config_theme) or not fn.check_package_installed(
        "edu-qtile-git"
    ):
        self.applyqtile.set_sensitive(False)
        self.resetqtile.set_sensitive(False)

    labelqt.set_margin_start(10)
    labelqt.set_margin_end(10)
    labelqt.set_hexpand(True)
    hbox8.append(labelqt)
    vbox4.set_margin_start(10)
    vbox4.set_margin_end(10)
    hbox8.append(vbox4)  # pack_end

    qtile_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
        base_dir + "/images/qtile-sample.jpg", img_load, img_load
    )
    if self.qtile_combo.get_selected_item() is None:
        pass
    elif fn.os.path.isfile(
        base_dir + "/themer_data/qtile/" + fn.get_combo_text(self.qtile_combo) + ".jpg"
    ):
        qtile_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            base_dir
            + "/themer_data/qtile/"
            + fn.get_combo_text(self.qtile_combo)
            + ".jpg",
            img_load,
            img_load,
        )
    texture = Gdk.Texture.new_for_pixbuf(qtile_pixbuf)
    qtile_image = Gtk.Picture.new_for_paintable(texture)
    qtile_image.set_content_fit(Gtk.ContentFit.SCALE_DOWN)
    qtile_image.set_size_request(img_min, img_min)
    qtile_image.set_halign(Gtk.Align.CENTER)
    qtile_image.set_valign(Gtk.Align.CENTER)
    qtile_image.set_hexpand(True)
    qtile_image.set_vexpand(False)

    self.qtile_combo.connect(
        "notify::selected",
        lambda w, _p, img, tt, ab, iw, ih: fn.update_image(self, w, img, tt, ab, iw, ih),
        qtile_image,
        "qtile",
        base_dir,
        img_load,
        img_load,
    )

    hbox9.append(self.resetqtile)  # pack_end
    hbox9.append(self.applyqtile)  # pack_end

    vboxstack3.append(hbox8)
    vboxstack3.append(hbox10)
    vboxstack3.append(qtile_image)
    label5.set_hexpand(True)
    label5.set_vexpand(True)
    vboxstack3.append(label5)
    vboxstack3.append(hbox9)  # pack_end

    # ==================================================================
    #                       LEFTWM TAB
    # ==================================================================

    self.status_leftwm = Gtk.Label()
    # self.status_leftwm.set_markup("<b>Theme is installed and applied</b>")

    label6 = Gtk.Label()
    label6.set_markup(
        "Reload your window manager with <b>Super + Shift + R</b>\
 after you make your changes.\n\
Sometimes you even need to logout to let the theme apply fully\n\
Be patient if it is the first time you install the theme or use the scripts to \
install them in one go"
    )

    labellft = Gtk.Label(label="Select theme - candy is the default theme")
    self.leftwm_combo = Gtk.DropDown.new_from_strings(list(fn.leftwm_themes_list))
    self.leftwm_combo.set_size_request(280, 0)
    self.leftwm_combo.connect("notify::selected", functools.partial(themer.on_leftwm_combo_changed, self))
    if fn.path_check(fn.leftwm_config_theme_current):
        link_theme = fn.os.path.basename(fn.os.readlink(fn.leftwm_config_theme_current))
        for i, theme in enumerate(fn.leftwm_themes_list):
            if link_theme == theme:
                self.leftwm_combo.set_selected(i)
    else:
        self.leftwm_combo.set_sensitive(False)

    vbox5 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    hbox12 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox13 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    vbox5.append(self.leftwm_combo)

    self.applyleftwm = Gtk.Button(label="Install and apply selected theme")
    self.applyleftwm.connect("clicked", functools.partial(themer.leftwm_apply_clicked, self))
    self.removeleftwm = Gtk.Button(label="Remove selected theme and apply Candy")
    self.removeleftwm.connect("clicked", functools.partial(themer.leftwm_remove_clicked, self))
    self.resetleftwm = Gtk.Button(label="Reset selected theme")
    self.resetleftwm.connect("clicked", functools.partial(themer.leftwm_reset_clicked, self))

    if not fn.os.path.isfile(fn.leftwm_config) or not fn.check_package_installed(
        "edu-leftwm-git"
    ):
        self.applyleftwm.set_sensitive(False)
        self.resetleftwm.set_sensitive(False)
        self.removeleftwm.set_sensitive(False)

    hbox11 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    labellft.set_margin_start(10)
    labellft.set_margin_end(10)
    labellft.set_hexpand(True)
    hbox11.append(labellft)
    vbox5.set_margin_start(10)
    vbox5.set_margin_end(10)
    hbox11.append(vbox5)  # pack_end

    leftwm_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
        base_dir + "/images/leftwm-sample.jpg", img_load, img_load
    )
    if self.leftwm_combo.get_selected_item() is None:
        pass
    elif fn.os.path.isfile(
        base_dir + "/themer_data/leftwm/" + fn.get_combo_text(self.leftwm_combo) + ".jpg"
    ):
        leftwm_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            base_dir
            + "/themer_data/leftwm/"
            + fn.get_combo_text(self.leftwm_combo)
            + ".jpg",
            img_load,
            img_load,
        )
    texture = Gdk.Texture.new_for_pixbuf(leftwm_pixbuf)
    leftwm_image = Gtk.Picture.new_for_paintable(texture)
    leftwm_image.set_content_fit(Gtk.ContentFit.SCALE_DOWN)
    leftwm_image.set_size_request(img_min, img_min)
    leftwm_image.set_halign(Gtk.Align.CENTER)
    leftwm_image.set_valign(Gtk.Align.CENTER)
    leftwm_image.set_hexpand(True)
    leftwm_image.set_vexpand(False)

    self.leftwm_combo.connect(
        "notify::selected",
        lambda w, _p, img, tt, ab, iw, ih: fn.update_image(self, w, img, tt, ab, iw, ih),
        leftwm_image,
        "leftwm",
        base_dir,
        img_load,
        img_load,
    )

    hbox12.append(self.removeleftwm)  # pack_end
    hbox12.append(self.resetleftwm)  # pack_end
    hbox12.append(self.applyleftwm)  # pack_end

    vboxstack4.append(hbox11)
    vboxstack4.append(hbox13)
    vboxstack4.append(leftwm_image)
    self.status_leftwm.set_hexpand(True)
    self.status_leftwm.set_vexpand(True)
    vboxstack4.append(self.status_leftwm)
    label6.set_hexpand(True)
    label6.set_vexpand(True)
    vboxstack4.append(label6)
    vboxstack4.append(hbox12)  # pack_end

    # ==================================================================
    #                       PACK TO STACK
    # ==================================================================

    stack.add_titled(vboxstack2, "stack2", "Awesome")
    stack.add_titled(vboxstack1, "stack1", "I3")
    stack.add_titled(vboxstack4, "stack4", "Leftwm")
    stack.add_titled(vboxstack3, "stack3", "Qtile")

    vbox.append(stack_switcher)
    stack.set_hexpand(True)
    stack.set_vexpand(True)
    vbox.append(stack)

    vboxstack10.append(hbox6)
    vboxstack10.append(hbox7)
    vbox.set_hexpand(True)
    vbox.set_vexpand(True)
    vboxstack10.append(vbox)

    fn.GLib.idle_add(init_themer_lazy_load, self, fn, priority=fn.GLib.PRIORITY_LOW)
