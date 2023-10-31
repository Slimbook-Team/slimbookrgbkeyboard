from gi.repository import Gdk, Gtk, GdkPixbuf
from os.path import expanduser
import gi
import utils
import os
import subprocess
import re

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

HERO_MAX_BACKLIGHT = 0xc8
USER_NAME = utils.get_user()
HOMEDIR = expanduser("~".format(USER_NAME))
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(
    HOMEDIR, '/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf')

_ = utils.load_translation('slimbookrgb')

MODULEDIR = "/sys/devices/platform/qc71_laptop/"

class Grid(Gtk.Grid):

    def __init__(self, *args, **kwargs):
        super(Grid, self).__init__(*args, **kwargs)
        
        self.backlight_red = 0
        self.backlight_green = 0
        self.backlight_blue = 0
        
        self.read_backlight()
        
        print(self.backlight_red)
        print(self.backlight_green)
        print(self.backlight_blue)
        print(self.get_average_rgb())
        
        self.switch1 = Gtk.Switch()
        self.switch1.set_halign(Gtk.Align.END)
        self.switch1.set_active(self.get_average_rgb() > 0)

        self.scale = Gtk.Scale.new_with_range(
            orientation=Gtk.Orientation.HORIZONTAL,
            min=0,
            max=HERO_MAX_BACKLIGHT,
            step=1
        )
        self.scale.connect("button-release-event", self.on_brightness_change)
        self.scale.set_sensitive(
            False) if not self.switch1.get_active() else print("Scale active")

        self.scale.set_value(self.get_average_rgb())
        self.switch1.connect("state-set", self.on_switch_change)
        
        label1 = Gtk.Label(label=_("Light switch"))
        label1.set_halign(Gtk.Align.START)
        label1.set_name('labelw')

        label2 = Gtk.Label(label=_("Brightness"))
        label2.set_halign(Gtk.Align.START)
        label2.set_name('labelw')

        btn_box = Gtk.HBox(spacing=30)

        red_btn = Gtk.Button()
        red_btn.set_name('red')
        red_btn.connect('clicked', self.on_color_change, (1,0,0))
        btn_box.pack_start(red_btn, True, True, 0)

        green_btn = Gtk.Button()
        green_btn.set_name('green')
        green_btn.connect('clicked', self.on_color_change, (0,1,0))
        btn_box.pack_start(green_btn, True, True, 0)

        blue_btn = Gtk.Button()
        blue_btn.set_name('blue')
        blue_btn.connect('clicked', self.on_color_change, (0,0,1))
        btn_box.pack_start(blue_btn, True, True, 0)

        white_btn = Gtk.Button()
        white_btn.set_name('white')
        white_btn.connect('clicked', self.on_color_change, (1,1,1))
        btn_box.pack_start(white_btn, True, True, 0)

        yellow_btn = Gtk.Button()
        yellow_btn.set_name('yellow')
        yellow_btn.connect('clicked', self.on_color_change, (1,1,0))
        btn_box.pack_start(yellow_btn, True, True, 0)

        magenta_btn = Gtk.Button()
        magenta_btn.set_name('magenta')
        magenta_btn.connect('clicked', self.on_color_change, (1,0,1))
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

    def on_switch_change(self, widget, state):
        print("state:",state)
        self.scale.set_sensitive(state)
        
    
    def on_brightness_change(self, widget, value):
        print("brightness:",widget.get_value())
    
    def on_color_change(self,widget, value):
        print("color:",value)
        r,g,b=value
        
        self.backlight_red = HERO_MAX_BACKLIGHT * r
        self.backlight_green = HERO_MAX_BACKLIGHT * g
        self.backlight_blue = HERO_MAX_BACKLIGHT * b
    
        print(self.get_reference_brightness())
        self.scale.set_value(self.get_reference_brightness())
    
    def read_backlight(self):
        output = subprocess.getoutput('heroctl get-kbd-backlight')
        print(output)
        value = int(output,16)
        
        self.backlight_red = (value & 0xff0000) >> 16
        self.backlight_green = (value & 0x00ff00) >> 8
        self.backlight_blue = value & 0x0000ff
    
    def write_backlight(self,value):
        subprocess.getoutput('heroctl set-kbd-backlight {0:06x}'.format(value))
    
    def get_attribute(self,name):
        f = open(MODULEDIR + name,"r")
        data = f.readlines()
        f.close()
        
        return data[0].strip()
        
    def get_backlight_max(self):
        raw = self.get_attribute("kbd_backlight_rgb_max")
        return int(raw,16)
    
    def get_backlight_red(self):
        raw = self.get_attribute("kbd_backlight_rgb_red")
        return int(raw,16)

    def get_backlight_green(self):
        raw = self.get_attribute("kbd_backlight_rgb_green")
        return int(raw,16)

    def get_backlight_blue(self):
        raw = self.get_attribute("kbd_backlight_rgb_blue")
        return int(raw,16)
        
    def get_average_rgb(self):
        return (self.backlight_red + self.backlight_green + self.backlight_blue) / 3.0

    def get_reference_brightness(self):
        top = max(self.backlight_red,self.backlight_green)
        top = max(top,self.backlight_blue)
        
        if top==0.0:
            return 0.0
            
        return top

