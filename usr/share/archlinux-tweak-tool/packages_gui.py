# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================

import functions as fn
from packages import Packages


def gui(self, Gtk, vbox_stack, fn):
    """create a gui"""
    try:
        packages_obj = Packages()

        hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl_packages_title = Gtk.Label(xalign=0)
        lbl_packages_title.set_name("title")
        lbl_packages_title.set_text("Packages")

        frame_export = Gtk.Frame(label="")
        frame_export_label = frame_export.get_label_widget()
        frame_export_label.set_markup("<b>Export Packages</b>")

        label_export_desc = Gtk.Label(xalign=0)
        label_export_desc.set_markup(
            f""
            f" <b>No AUR packages are exported</b>\n"
            f" - Option: <b>Explicitly Installed Packages</b> (recommended) will export installed packages only found in sync db (less packages)\n"
            f" - Option: <b>All Installed Packages</b> will export all packages currently installed on your system (lots of packages)\n"
            f" - Tip: To see packages installed from AUR in the terminal type: pacman -Qqem\n\n"
            f""
            f" A list of installed packages will be exported to <b>{packages_obj.default_export_path}</b>"
        )

        label_export_desc.set_selectable(True)

        hbox_export = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        hbox_title.append(lbl_packages_title)

        hbox_title_install = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label_install_title = Gtk.Label(xalign=0)
        label_install_title.set_markup("<b> Install Packages</b>")

        hbox_title_install.append(label_install_title)

        hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hsep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hsep.set_hexpand(True)
        hsep.set_vexpand(False)
        hbox_sep.append(hsep)

        button_export_packages = Gtk.Button(label="Export Packages")

        rb_export_all = Gtk.CheckButton(label="All Installed Packages")
        rb_export_all.set_name("rb_packages_export_all")

        rb_export_explicit = Gtk.CheckButton(label="Explicitly Installed Packages")
        rb_export_explicit.set_group(rb_export_all)
        rb_export_explicit.set_name("rb_packages_export_explicit")
        rb_export_explicit.set_active(True)

        # button_export_packages.set_size_request(100, 30)

        lbl_export_padding1 = Gtk.Label(xalign=0, yalign=0)
        lbl_export_padding1.set_text(" ")
        grid_export = Gtk.Grid()

        grid_export.attach(rb_export_explicit, 0, 2, 1, 1)
        grid_export.attach_next_to(
            lbl_export_padding1, rb_export_explicit, Gtk.PositionType.RIGHT, 1, 1
        )

        grid_export.attach_next_to(
            rb_export_all, lbl_export_padding1, Gtk.PositionType.RIGHT, 1, 1
        )

        vbox_export_button = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        vbox_export_button.append(button_export_packages)

        vbox_export = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        label_export_desc.set_margin_start(10)
        label_export_desc.set_margin_end(10)
        vbox_export.append(label_export_desc)
        grid_export.set_margin_start(10)
        grid_export.set_margin_end(10)
        vbox_export.append(grid_export)
        vbox_export_button.set_margin_start(10)
        vbox_export_button.set_margin_end(10)
        vbox_export.append(vbox_export_button)

        vbox_export.set_margin_start(10)
        vbox_export.set_margin_end(10)
        hbox_export.append(vbox_export)

        frame_export.set_child(hbox_export)

        frame_install = Gtk.Frame(label="")
        frame_install_label = frame_install.get_label_widget()
        frame_install_label.set_markup("<b>Install Packages</b>")

        hbox_install = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label_install_desc = Gtk.Label(xalign=0, yalign=0)
        label_install_desc.set_markup(
            f""
            f" <b>WARNING: Proceed with caution this will install packages onto your system!</b>\n"
            f" <b>Packages from the AUR are not supported </b>\n"
            f" <b>This also performs a full system upgrade</b>\n\n"
            f" - A list of packages are sourced from <b>{packages_obj.default_export_path}</b>\n"
            f" - To ignore a package, add a # in front of the package name\n"
            f" - Log file: {packages_obj.logfile}\n"
            f" - <b>A reboot is recommended when core Linux packages are installed</b>"
        )

        label_install_desc.set_selectable(True)

        grid_package_status = Gtk.Grid()
        grid_package_count = Gtk.Grid()

        label_package_status = Gtk.Label(xalign=0, yalign=0)
        label_package_status.set_name("label_package_status")
        label_package_status.set_markup("Status: ")

        grid_package_status.attach(label_package_status, 0, 1, 1, 1)
        grid_package_status.set_halign(Gtk.Align.START)

        label_package_count = Gtk.Label(xalign=0, yalign=0)
        label_package_count.set_name("label_package_status")
        label_package_count.set_markup("Progress: ")
        grid_package_count.attach(label_package_count, 0, 1, 1, 1)
        grid_package_count.set_halign(Gtk.Align.START)

        vbox_install = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        label_install_desc.set_margin_start(10)
        label_install_desc.set_margin_end(10)
        vbox_install.append(label_install_desc)

        hbox_install = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox_install.set_margin_start(10)
        vbox_install.set_margin_end(10)
        hbox_install.append(vbox_install)

        frame_install.set_child(hbox_install)

        vbox_pacmanlog = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        grid_pacmanlog = Gtk.Grid()

        textbuffer_pacmanlog = Gtk.TextBuffer()

        textview_pacmanlog = Gtk.TextView()
        textview_pacmanlog.set_property("editable", False)
        textview_pacmanlog.set_property("monospace", True)
        textview_pacmanlog.set_margin_start(5)
        textview_pacmanlog.set_margin_end(5)
        textview_pacmanlog.set_margin_top(5)
        textview_pacmanlog.set_margin_bottom(5)
        textview_pacmanlog.set_name("textview_log")

        textview_pacmanlog.set_vexpand(True)
        textview_pacmanlog.set_hexpand(True)
        textview_pacmanlog.set_size_request(0, 500)
        # set the height using size request on the textview
        # otherwise you get extra padding inside the scrolledwindow

        textview_pacmanlog.set_buffer(textbuffer_pacmanlog)

        pacmanlog_scrolledwindow = Gtk.ScrolledWindow()

        pacmanlog_scrolledwindow.set_propagate_natural_height(True)
        pacmanlog_scrolledwindow.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC
        )

        pacmanlog_scrolledwindow.set_size_request(100, 400)

        pacmanlog_scrolledwindow.set_child(textview_pacmanlog)

        label_grid_padding_right = Gtk.Label(xalign=0)
        label_grid_padding_right.set_text("     ")

        grid_pacmanlog.attach(pacmanlog_scrolledwindow, 0, 1, 1, 1)
        grid_pacmanlog.attach_next_to(
            label_grid_padding_right,
            pacmanlog_scrolledwindow,
            Gtk.PositionType.RIGHT,
            1,
            1,
        )

        vbox_pacmanlog.append(grid_pacmanlog)

        button_install_packages = Gtk.Button(label="Install Packages")

        gui_parts = (
            vbox_stack,
            grid_package_status,
            grid_package_count,
            vbox_pacmanlog,
            textbuffer_pacmanlog,
            textview_pacmanlog,
            label_package_status,
            label_package_count,
        )

        button_export_packages.connect(
            "clicked",
            self.on_click_export_packages,
            packages_obj,
            rb_export_all,
            rb_export_explicit,
            gui_parts,
        )

        button_install_packages.connect(
            "clicked",
            self.on_click_install_packages,
            packages_obj,
            gui_parts,
        )

        vbox_install_button = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        vbox_install_button.append(button_install_packages)

        vbox_install_button.set_margin_start(10)
        vbox_install_button.set_margin_end(10)
        vbox_install.append(vbox_install_button)

        vbox_stack.append(hbox_title)
        vbox_stack.append(hbox_sep)

        vbox_stack.append(frame_export)
        vbox_stack.append(frame_install)

    except Exception as e:
        fn.logger.error("Exception in packages_gui.gui(): %s" % e)
