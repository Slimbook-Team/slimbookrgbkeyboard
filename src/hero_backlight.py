from gi.repository import Gdk, Gtk, GdkPixbuf
from os.path import expanduser
import gi
import utils
import os
import subprocess
import re

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

USER_NAME = utils.get_user()
HOMEDIR = expanduser("~".format(USER_NAME))
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(
    HOMEDIR, '/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf')

_ = utils.load_translation('slimbookrgb')

MODULEDIR = "/sys/devices/platform/qc71_laptop/"

class Grid(Gtk.Grid):

    def __init__(self, *args, **kwargs):

        self.switch1 = Gtk.Switch()
        self.switch1.set_halign(Gtk.Align.END)
        self.switch1.connect("state-set", self.switch_light)

        self.scale = Gtk.Scale.new_with_range(
            orientation=Gtk.Orientation.HORIZONTAL,
            min=0,
            max=100,
            step=1
        )
        self.scale.connect("button-release-event", self.set_brightness)
        self.scale.set_sensitive(
            False) if not self.switch1.get_active() else print("Scale active")

        label1 = Gtk.Label(label=_("Light switch"))
        label1.set_halign(Gtk.Align.START)
        label1.set_name('labelw')

        label2 = Gtk.Label(label=_("Brightness"))
        label2.set_halign(Gtk.Align.START)
        label2.set_name('labelw')

        btn_box = Gtk.HBox(spacing=30)

        red_btn = Gtk.Button()
        red_btn.set_name('red')
        red_btn.connect('clicked', self.color_change, '0xff0000')
        btn_box.pack_start(red_btn, True, True, 0)

        green_btn = Gtk.Button()
        green_btn.set_name('green')
        green_btn.connect('clicked', self.color_change, '0x00ff00')
        btn_box.pack_start(green_btn, True, True, 0)

        blue_btn = Gtk.Button()
        blue_btn.set_name('blue')
        blue_btn.connect('clicked', self.color_change, '0x0000ff')
        btn_box.pack_start(blue_btn, True, True, 0)

        white_btn = Gtk.Button()
        white_btn.set_name('white')
        white_btn.connect('clicked', self.color_change, '0xffffff')
        btn_box.pack_start(white_btn, True, True, 0)

        yellow_btn = Gtk.Button()
        yellow_btn.set_name('yellow')
        yellow_btn.connect('clicked', self.color_change, '0xffff00')
        btn_box.pack_start(yellow_btn, True, True, 0)

        magenta_btn = Gtk.Button()
        magenta_btn.set_name('magenta')
        magenta_btn.connect('clicked', self.color_change, '0xff00ff')
        btn_box.pack_start(magenta_btn, True, True, 0)

        colors_lbl = Gtk.Label(label='Colors')
        colors_lbl.set_name('labelw')
        colors_lbl.set_halign(Gtk.Align.START)

        self.set_halign(Gtk.Align.CENTER)
        self.attach(label1, 0, 0, 1, 1)
        self.attach(self.switch1, 3, 0, 1, 1)
        self.attach(label2, 0, 1, 1, 1)
        self.attach(self.scale, 2, 1, 2, 1)
        self.attach(colors_lbl, 0, 4, 4, 1)
        self.attach(btn_box, 0, 6, 4, 1)

        self.show_all()

    def get_attribute(self,name):
        f = open(MODULEDIR + name,"r")
        data = f.readlines()
        f.close()
        
        return data[0].strip()
        
    def get_backlight_max(self):
        raw = self.get_attribute("kbd_backlight_max")
        return int(raw)
