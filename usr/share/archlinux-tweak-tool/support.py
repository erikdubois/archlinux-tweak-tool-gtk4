# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0115,C0116,I1101

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GdkPixbuf, Gdk
import functions as fn


base_dir = fn.path.dirname(fn.path.realpath(__file__))


def _make_clickable_image(pixbuf, url, tooltip_text, click_callback):
    """Create an image with a click gesture and tooltip (replaces EventBox pattern)."""
    texture = Gdk.Texture.new_for_pixbuf(pixbuf)
    image = Gtk.Image.new_from_paintable(texture)
    image.set_cursor(Gdk.Cursor.new_from_name("pointer"))
    image.set_tooltip_text(tooltip_text)
    gesture = Gtk.GestureClick.new()
    gesture.connect("pressed", lambda g, n, x, y, u=url: click_callback(u))
    image.add_controller(gesture)
    return image


class Support(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Credits - Support Development", transient_for=parent)

        self.set_size_request(550, 100)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        box = self.get_content_area()
        box.append(vbox)

        label = Gtk.Label()
        label.set_wrap(True)
        label.set_justify(Gtk.Justification.CENTER)
        label.set_markup(
            "Big thanks to <b>Brad Heffernan</b> who was the driving force behind the ArchLinux Tweak Tool.\n\
After his departure <b>Cameron Percival</b> and <b>Erik Dubois</b> kept developing \
this easy and efficient tool.\n\n\
You can support the project with providing code, fixes, ideas, ... via github.\n\
You can give support via donations.\n\
Nowadays the goal of the app is to bridge all Arch Linux based systems.\n\n\
IT is all Arch Linux\n\
the right setting - the right config - the right application - at the right place"
        )

        label2 = Gtk.Label()
        label2.set_justify(Gtk.Justification.CENTER)
        label2.set_markup("Support this app")

        logo = GdkPixbuf.Pixbuf.new_from_file_at_size(
            fn.path.join(base_dir, "images/archlinux-tweak-tool.png"), 100, 100
        )
        logo_texture = Gdk.Texture.new_for_pixbuf(logo)
        logo_image = Gtk.Image.new_from_paintable(logo_texture)

        pbdisc = GdkPixbuf.Pixbuf.new_from_file_at_size(
            fn.path.join(base_dir, "images/donate.png"), 54, 54
        )
        donate_image = _make_clickable_image(
            pbdisc,
            "https://www.arcolinux.info/donation/",
            "Different ways to support",
            self._open_link,
        )

        pbp = GdkPixbuf.Pixbuf.new_from_file_at_size(
            fn.path.join(base_dir, "images/patreon.png"), 48, 48
        )
        patreon_image = _make_clickable_image(
            pbp,
            "https://www.patreon.com/arcolinux",
            "Support ArcoLinux on Patreon",
            self._open_link,
        )

        pbpp = GdkPixbuf.Pixbuf.new_from_file_at_size(
            fn.path.join(base_dir, "images/paypal.png"), 54, 54
        )
        paypal_image = _make_clickable_image(
            pbpp,
            "https://www.paypal.com/paypalme/erikdubois",
            "Donate to this project via paypal",
            self._open_link,
        )

        pbdisc2 = GdkPixbuf.Pixbuf.new_from_file_at_size(
            fn.path.join(base_dir, "images/discord.png"), 54, 54
        )
        discord_image = _make_clickable_image(
            pbdisc2,
            "https://discord.gg/R2amEEz",
            "Get ATT support on Discord",
            self._open_link,
        )

        pbghub = GdkPixbuf.Pixbuf.new_from_file_at_size(
            fn.path.join(base_dir, "images/github.png"), 54, 54
        )
        github_image = _make_clickable_image(
            pbghub,
            "https://github.com/erikdubois/archlinux-tweak-tool-gtk4",
            "Donate time and code to this project",
            self._open_link,
        )

        label.set_margin_start(10)
        label.set_margin_end(10)
        hbox.append(label)

        donate_image.set_margin_start(10)
        #hbox2.append(donate_image)
        github_image.set_margin_start(10)
        hbox2.append(github_image)
        #hbox2.append(patreon_image)
        paypal_image.set_margin_start(10)
        hbox2.append(paypal_image)
        discord_image.set_margin_start(10)
        #hbox2.append(discord_image)
        hbox3.append(hbox2)

        logo_image.set_margin_top(10)
        vbox.append(logo_image)
        hbox.set_margin_top(10)
        vbox.append(hbox)

        label2.set_margin_bottom(10)
        vbox.append(label2)
        vbox.append(hbox1)
        hbox3.set_margin_bottom(10)
        vbox.append(hbox3)

        self.present()

    def _open_link(self, link):
        thread = fn.threading.Thread(target=self.weblink, args=(link,))
        thread.daemon = True
        thread.start()

    def weblink(self, link):
        if fn.check_package_installed("firefox"):
            fn.subprocess.call(
                [
                    "sudo",
                    "-H",
                    "-u",
                    fn.sudo_username,
                    "bash",
                    "-c",
                    "firefox --new-tab " + link,
                ],
                shell=False,
            )
        else:
            if fn.check_package_installed("chromium"):
                fn.subprocess.call(
                    [
                        "sudo",
                        "-H",
                        "-u",
                        fn.sudo_username,
                        "bash",
                        "-c",
                        "chromium " + link,
                    ],
                    shell=False,
                )
            else:
                fn.subprocess.call(
                    [
                        "sudo",
                        "-H",
                        "-u",
                        fn.sudo_username,
                        "bash",
                        "-c",
                        "exo-open --launch webbrowser " + link,
                    ],
                    shell=False,
                )
