# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0115,I1101

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk
import functions as fn


base_dir = fn.path.dirname(fn.path.realpath(__file__))


class SplashScreen(Gtk.Window):
    def __init__(self, transient_for=None):
        super().__init__()
        self.set_decorated(False)
        self.maximize()

        # GTK4 window placement is compositor-controlled. Making the splash transient
        # and modal gives the compositor a strong hint to center it.
        if transient_for is not None:
            try:
                self.set_transient_for(transient_for)
                self.set_modal(True)
            except Exception:
                pass

        texture = Gdk.Texture.new_from_filename(base_dir + "/images/splash.jpg")
        picture = Gtk.Picture.new_for_paintable(texture)
        picture.set_can_shrink(True)
        picture.set_content_fit(Gtk.ContentFit.COVER)
        picture.set_hexpand(True)
        picture.set_vexpand(True)
        self.set_child(picture)

        self.present()
