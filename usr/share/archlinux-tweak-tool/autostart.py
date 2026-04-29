# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

from ast import literal_eval
import functools
import functions as fn
from gi.repository import Gtk, Gio, GdkPixbuf, Gdk


def get_startups(name):
    """find out if there are .desktop files - hidden = true / false"""
    try:
        with open(fn.autostart + name + ".desktop", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
        state = True
    except:
        return True

    if fn.check_content("Hidden=", fn.autostart + name + ".desktop"):
        try:
            pos = fn.get_position(lines, "Hidden=")
            state = lines[pos].split("=")[1].strip()

            state = state.capitalize()
            state = not literal_eval(state)
            return state
        except Exception as error:
            fn.log_error(str(error))
            return True
    else:
        return state


def add_autostart(self, name, com, comnt):
    """Add a new autostart"""
    # lists = [x for x in fn.os.listdir(fn.home + "/.config/autostart/")]
    lists = list(fn.listdir(fn.home + "/.config/autostart"))
    if not name + ".desktop" in lists:
        content = (
            "[Desktop Entry]\n\
Encoding=UTF-8\n\
Version=1.0\n\
Type=Application\n\
Name="
            + name
            + "\n\
Comment="
            + comnt
            + "\n\
Exec="
            + com
            + "\n\
TryExec="
            + com
            + "\n\
StartupNotify=false\n\
X-GNOME-Autostart-enabled=true\n\
Terminal=false\n\
Hidden=false\n"
        )

        with open(
            fn.home + "/.config/autostart/" + name + ".desktop", "w", encoding="utf-8"
        ) as f:
            f.write(content)
            f.close()
        self.add_row(name)
        # self.startups.append([True, name, comnt])


# ====================================================================
# AUTOSTART CALLBACKS
# ====================================================================

def on_comment_changed(self, widget):
    if len(self.txtbox1.get_text()) >= 3 and len(self.txtbox2.get_text()) >= 3:
        self.abutton.set_sensitive(True)


def on_auto_toggle(self, widget, data, lbl):
    failed = False
    try:
        with open(fn.autostart + lbl + ".desktop", "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
        try:
            pos = fn.get_position(lines, "Hidden=")
        except:
            failed = True
            with open(fn.autostart + lbl + ".desktop", "a", encoding="utf-8") as f:
                f.write("Hidden=" + str(not widget.get_active()).lower())
                f.close()
    except:
        pass
    if not failed:
        try:
            val = lines[pos].split("=")[1].strip()
            lines[pos] = lines[pos].replace(
                val, str(not widget.get_active()).lower()
            )
            with open(fn.autostart + lbl + ".desktop", "w", encoding="utf-8") as f:
                f.writelines(lines)
                f.close()
        except:
            pass


def on_auto_remove_clicked(self, gesture_or_widget, listbox, lbl):
    try:
        fn.unlink(fn.autostart + lbl + ".desktop")
        fn.debug_print("Removed item from ~/.config/autostart/")
        self.vvbox.remove(listbox)
    except Exception as error:
        fn.log_error(str(error))
        fn.debug_print("We were unable to remove it")
        fn.debug_print("Evaluate if it can/should be removed")
        fn.debug_print("Then remove it manually")
        fn.debug_print("We only remove .desktop files")


def clear_autostart(self):
    child = self.vvbox.get_first_child()
    while child is not None:
        next_child = child.get_next_sibling()
        self.vvbox.remove(child)
        child = next_child


def load_autostart(self, files, base_dir=None):
    clear_autostart(self)

    for x in files:
        add_row(self, x, base_dir)


def add_row(self, x, base_dir=None):
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

    lbl = Gtk.Label(xalign=0)
    lbl.set_text(x)

    swtch = Gtk.Switch()
    swtch.connect("notify::active", functools.partial(on_auto_toggle, self, lbl=x))
    swtch.set_active(get_startups(x))

    listbox = Gtk.ListBox()

    image_path = fn.path.join(base_dir, "images/remove.png") if base_dir else fn.path.join(fn.path.dirname(__file__), "images/remove.png")
    pbfb = GdkPixbuf.Pixbuf.new_from_file_at_size(
        image_path, 28, 28
    )
    texture = Gdk.Texture.new_for_pixbuf(pbfb)
    fbimage = Gtk.Image.new_from_paintable(texture)
    fbimage.set_cursor(Gdk.Cursor.new_from_name("pointer"))
    fbimage.set_tooltip_text("Remove")

    _listbox = listbox
    _text = lbl.get_text()
    fb_gesture = Gtk.GestureClick.new()
    fb_gesture.connect(
        "pressed",
        lambda g, n, x, y, lb=_listbox, t=_text: on_auto_remove_clicked(self, g, lb, t),
    )
    fbimage.add_controller(fb_gesture)

    lbl.set_hexpand(True)
    hbox.append(lbl)
    swtch.set_margin_top(10)
    swtch.set_margin_bottom(10)
    vbox2.append(swtch)
    hbox.append(vbox2)
    hbox.append(fbimage)

    vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    hbox.set_margin_top(5)
    hbox.set_margin_bottom(5)
    vbox1.append(hbox)

    listbox.set_selection_mode(Gtk.SelectionMode.NONE)
    listboxrow = Gtk.ListBoxRow()
    listboxrow.set_child(vbox1)
    listbox.append(listboxrow)

    self.vvbox.append(listbox)


def on_remove_auto(self, widget):
    selection = self.treeView4.get_selection()
    model, paths = selection.get_selected_rows()

    for path in paths:
        iter = model.get_iter(path)
        value = model.get_value(iter, 1)
        model.remove(iter)
        fn.unlink(fn.home + "/.config/autostart/" + value + ".desktop")
        fn.debug_print("Item has been removed from autostart")
        fn.show_in_app_notification(self, "Item has been removed from autostart")


def on_add_autostart(self, widget):
    if len(self.txtbox1.get_text()) > 1 and len(self.txtbox2.get_text()) > 1:
        add_autostart(
            self,
            self.txtbox1.get_text(),
            self.txtbox2.get_text(),
            self.txtbox3.get_text(),
        )
    fn.debug_print("Item has been added to autostart")
    fn.show_in_app_notification(self, "Item has been added to autostart")


def on_exec_browse(self, widget):
    dialog = Gtk.FileChooserDialog(
        title="Please choose a file",
        transient_for=self,
        action=Gtk.FileChooserAction.OPEN,
    )

    dialog.set_select_multiple(False)
    dialog.set_current_folder(Gio.File.new_for_path(fn.home))
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Open", Gtk.ResponseType.OK)
    dialog.connect("response", open_response_auto)

    dialog.present()


def open_response_auto(dialog, response):
    if response == Gtk.ResponseType.OK:
        files = dialog.get_files()
        if files:
            foldername = files[0].get_path()
            fn.debug_print(foldername)
            dialog.destroy()
    elif response == Gtk.ResponseType.CANCEL:
        dialog.destroy()


def create_autostart_columns(self, treeView):
    rendererText = Gtk.CellRendererText()
    renderer_checkbox = Gtk.CellRendererToggle()
    column_checkbox = Gtk.TreeViewColumn("", renderer_checkbox, active=0)
    renderer_checkbox.connect("toggled", renderer_checkbox_callback, self.startups)
    renderer_checkbox.set_activatable(True)
    column_checkbox.set_sort_column_id(0)

    column = Gtk.TreeViewColumn("Name", rendererText, text=1)
    column.set_sort_column_id(1)

    column2 = Gtk.TreeViewColumn("Comment", rendererText, text=2)
    column2.set_sort_column_id(2)

    treeView.append_column(column_checkbox)
    treeView.append_column(column)
    treeView.append_column(column2)


def create_columns(self, treeView):
    rendererText = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn("Name", rendererText, text=0)
    column.set_sort_column_id(0)
    treeView.append_column(column)


def renderer_checkbox_callback(renderer, path, model):
    if path is not None:
        it = model.get_iter(path)
        model[it][0] = not model[it][0]


def on_activated(self, treeview, path, column):
    failed = False
    treestore, selected_treepaths = treeview.get_selection().get_selected_rows()
    selected_treepath = selected_treepaths[0]
    selected_row = treestore[selected_treepath]
    bool = selected_row[0]
    text = selected_row[1]

    if bool:
        bools = False
    else:
        bools = True

    with open(
        fn.home + "/.config/autostart/" + text + ".desktop", "r", encoding="utf-8"
    ) as f:
        lines = f.readlines()
        f.close()
    try:
        pos = fn.get_position(lines, "Hidden=")
    except:
        failed = True
        with open(
            fn.home + "/.config/autostart/" + text + ".desktop",
            "a",
            encoding="utf-8",
        ) as f:
            f.write("Hidden=" + str(bools))
            f.close()
    if not failed:
        val = lines[pos].split("=")[1].strip()
        lines[pos] = lines[pos].replace(val, str(bools).lower())
        with open(
            fn.home + "/.config/autostart/" + text + ".desktop",
            "w",
            encoding="utf-8",
        ) as f:
            f.writelines(lines)
            f.close()


# ====================================================================
# AUTOSTART GUI
# ====================================================================

def gui(self, Gtk, vboxstack13, fn_module):
    """create a gui"""

    base_dir = fn_module.path.dirname(fn_module.path.realpath(__file__))

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
    lbls.set_text("This is the current content of ~/.config/autostart/")
    toplabelbox.append(lbls)

    files = [x.replace(".desktop", "") for x in fn_module.listdir(fn_module.autostart)]
    mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

    self.vvbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    self.vvbox.set_name("vbox")

    scrolled_window.set_child(self.vvbox)
    scrolled_window.set_hexpand(True)
    scrolled_window.set_vexpand(True)
    mainbox.append(scrolled_window)

    load_autostart(self, files, base_dir)

    hbox_add_label = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    lbl_add_manual = Gtk.Label(xalign=0)
    lbl_add_manual.set_markup("<b>Add a manual autostart file</b>")
    lbl_add_manual.set_margin_start(5)
    lbl_add_manual.set_margin_top(10)
    lbl_add_manual.set_margin_bottom(5)
    hbox_add_label.append(lbl_add_manual)

    lbl1 = Gtk.Label(label="Name")
    lbl2 = Gtk.Label(label="Command")
    lbl3 = Gtk.Label(label="Comment")

    self.txtbox1 = Gtk.Entry()
    self.txtbox2 = Gtk.Entry()
    self.txtbox3 = Gtk.Entry()
    self.txtbox1.set_size_request(180, 0)
    self.txtbox2.set_size_request(180, 0)
    self.txtbox3.set_size_request(180, 0)
    self.txtbox1.connect("changed", functools.partial(on_comment_changed, self))
    self.txtbox2.connect("changed", functools.partial(on_comment_changed, self))

    bbutton = Gtk.Button(label="...")
    self.abutton = Gtk.Button(label="Add")
    self.abutton.set_size_request(140, 0)
    self.abutton.set_sensitive(False)

    bbutton.connect("clicked", functools.partial(on_exec_browse, self))

    self.abutton.connect("clicked", functools.partial(on_add_autostart, self))

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
    vbox5.append(bbutton)
    vbox6.append(Gtk.Label(label=""))
    vbox6.append(self.abutton)

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
    vboxstack13.append(hbox_add_label)
    vboxstack13.append(hbox2)
