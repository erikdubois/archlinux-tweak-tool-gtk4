# ============================================================
# Authors: Erik Dubois
# ============================================================

import streamline
from gi.repository import GLib


def gui(self, Gtk, vbox_stack, fn):
    """Create the Streamline page — remove optional apps by category, save/import profiles."""
    categories = fn.load_streamline_categories()

    # ── Title ──────────────────────────────────────────────
    hbox_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    lbl_title = Gtk.Label(xalign=0)
    lbl_title.set_name("title")
    lbl_title.set_text("Streamline")
    lbl_title.set_margin_start(10)
    lbl_title.set_margin_end(10)
    hbox_title.append(lbl_title)

    hbox_sep = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hseparator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    hseparator.set_hexpand(True)
    hbox_sep.append(hseparator)

    lbl_desc = Gtk.Label(xalign=0)
    lbl_desc.set_markup(
        " Remove optional apps that shipped on this system, grouped by category.\n"
        " Tick a <b>category</b> to select all its apps, then untick the ones you want to keep.\n"
        " <b>Save profile</b> stores your selection so you can re-apply it after a future reinstall."
    )
    lbl_desc.set_margin_start(10)
    lbl_desc.set_margin_top(5)
    lbl_desc.set_margin_bottom(10)

    self.streamline_recursive = Gtk.CheckButton(label="Also remove unused dependencies (-Rns)")
    self.streamline_recursive.set_active(True)
    self.streamline_recursive.set_margin_start(10)

    # ── Category list (scrollable) ─────────────────────────
    scrolled = Gtk.ScrolledWindow()
    scrolled.set_vexpand(True)
    scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    container.set_margin_start(10)
    container.set_margin_end(10)
    scrolled.set_child(container)

    def on_category_toggled(category_check, child_checks):
        active = category_check.get_active()
        for child_check in child_checks:
            child_check.set_active(active)

    def populate():
        child = container.get_first_child()
        while child is not None:
            nxt = child.get_next_sibling()
            container.remove(child)
            child = nxt

        self.streamline_checks = []
        all_pkgs = [pkg for pkgs in categories.values() for pkg in pkgs]
        installed = fn.check_packages_installed(all_pkgs)

        shown = False
        for category, pkgs in categories.items():
            present = [pkg for pkg in pkgs if installed.get(pkg)]
            if not present:
                continue
            shown = True

            category_check = Gtk.CheckButton()
            category_label = Gtk.Label(xalign=0)
            category_label.set_markup(f"<b>{GLib.markup_escape_text(category)}</b>")
            category_check.set_child(category_label)
            category_check.set_margin_top(8)
            container.append(category_check)

            child_checks = []
            for pkg in present:
                row_check = Gtk.CheckButton(label=pkg)
                row_check.set_margin_start(25)
                container.append(row_check)
                self.streamline_checks.append((pkg, row_check))
                child_checks.append(row_check)

            category_check.connect("toggled", on_category_toggled, child_checks)

        if not shown:
            lbl_empty = Gtk.Label(xalign=0)
            lbl_empty.set_text("No optional apps from the Kiro package list are installed on this system.")
            lbl_empty.set_margin_top(10)
            container.append(lbl_empty)

    def on_remove(_widget):
        packages = streamline.selected_packages(self)
        if not packages:
            fn.log_warn("Streamline: remove clicked with no packages selected")
            fn.show_in_app_notification(self, "No packages selected")
            return
        recursive = self.streamline_recursive.get_active()
        returncode, preview = streamline.removal_preview(packages, recursive)

        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"Remove {len(packages)} selected package(s)?",
        )
        if returncode == 0:
            dialog.format_secondary_text("This will remove:\n\n" + preview)
        else:
            dialog.format_secondary_text("pacman reported a problem with this selection:\n\n" + preview)
            # Removal would fail (e.g. a dependency is required elsewhere) — block confirming it.
            dialog.set_response_sensitive(Gtk.ResponseType.YES, False)
        dialog.set_default_response(Gtk.ResponseType.NO)

        def on_response(_dialog, response):
            _dialog.destroy()
            if response == Gtk.ResponseType.YES:
                streamline.do_remove(self, packages, recursive, populate)

        dialog.connect("response", on_response)
        dialog.present()

    def on_save(_widget):
        packages = streamline.selected_packages(self)
        if not packages:
            fn.log_warn("Streamline: save clicked with no packages selected")
            fn.show_in_app_notification(self, "No packages selected")
            return
        streamline.save_profile(self, packages)

    def apply_imported(packages):
        wanted = set(packages)
        matched = 0
        for pkg, check in self.streamline_checks:
            in_profile = pkg in wanted
            check.set_active(in_profile)
            if in_profile:
                matched += 1
        fn.log_info(f"Streamline: imported profile selected {matched} installed package(s)")
        fn.show_in_app_notification(self, f"Profile imported — {matched} installed app(s) selected")

    def on_import(_widget):
        import gi

        gi.require_version("Gio", "2.0")
        from gi.repository import Gio

        fn.log_subsection("Streamline — import profile")
        file_chooser = Gtk.FileChooserDialog(
            title="Select a Streamline profile to import",
            transient_for=self,
            action=Gtk.FileChooserAction.OPEN,
        )
        file_chooser.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        file_chooser.add_button("_Open", Gtk.ResponseType.OK)
        if fn.path.isdir(fn.att_streamline_dir):
            file_chooser.set_current_folder(Gio.File.new_for_path(fn.att_streamline_dir))
        file_filter = Gtk.FileFilter()
        file_filter.set_name("Profile files (*.txt)")
        file_filter.add_pattern("*.txt")
        file_chooser.add_filter(file_filter)

        handled = [False]

        def on_response(dialog, response_id, _user_data=None):
            if handled[0]:
                return
            handled[0] = True
            if response_id == Gtk.ResponseType.OK:
                selected_file = dialog.get_file()
                if selected_file:
                    apply_imported(streamline.read_profile_file(selected_file.get_path()))
            else:
                fn.show_in_app_notification(self, "Import cancelled")
            dialog.close()

        file_chooser.connect("response", on_response)
        file_chooser.present()

    populate()

    # ── Action bar ─────────────────────────────────────────
    hbox_actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_actions.set_margin_start(10)
    hbox_actions.set_margin_top(10)
    hbox_actions.set_margin_bottom(10)
    btn_remove = Gtk.Button(label="Remove selected")
    btn_remove.connect("clicked", on_remove)
    btn_save = Gtk.Button(label="Save profile")
    btn_save.connect("clicked", on_save)
    btn_import = Gtk.Button(label="Import profile")
    btn_import.connect("clicked", on_import)
    hbox_actions.append(btn_remove)
    hbox_actions.append(btn_save)
    hbox_actions.append(btn_import)

    vbox_stack.append(hbox_title)
    vbox_stack.append(hbox_sep)
    vbox_stack.append(lbl_desc)
    vbox_stack.append(self.streamline_recursive)
    vbox_stack.append(scrolled)
    vbox_stack.append(hbox_actions)
