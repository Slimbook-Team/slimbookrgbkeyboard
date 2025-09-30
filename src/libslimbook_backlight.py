import slimbook.kbd

from gi.repository import Gdk, Gtk, GdkPixbuf
from os.path import expanduser

import gi
import utils
import os
import subprocess

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

_ = utils.load_translation('slimbookrgb')

class Grid(Gtk.Grid):

    def __init__(self, *args, **kwargs):
        super(Grid, self).__init__(*args, **kwargs)
        
        self.backlight_red = 0
        self.backlight_green = 0
        self.backlight_blue = 0
        self.brightness = 0
        
        self.read_backlight()
        
        self.switch1 = Gtk.Switch()
        self.switch1.set_halign(Gtk.Align.END)
        self.switch1.set_active(self.get_average_rgb() > 0)

        self.max_brightness = slimbook.kbd.brightness_max(0)
        
        self.scale = Gtk.Scale.new_with_range(
            orientation = Gtk.Orientation.HORIZONTAL,
            min = 0,
            max = self.max_brightness,
            step = 1
        )
        self.scale.connect("button-release-event", self.on_brightness_change)
        self.scale.set_sensitive(self.switch1.get_active())

        self.scale.set_value(self.brightness)
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
        
        
        self.sample = Gtk.DrawingArea()
        self.sample.connect('draw', self.on_draw)
        self.sample.set_size_request(-1,32)
        
        self.set_halign(Gtk.Align.CENTER)
        self.attach(label1, 0, 0, 1, 1)
        self.attach(self.switch1, 3, 0, 1, 1)
        self.attach(label2, 0, 1, 1, 1)
        self.attach(self.scale, 2, 1, 2, 1)
        self.attach(colors_lbl, 0, 4, 4, 1)
        self.attach(btn_box, 0, 6, 4, 1)

        self.set_row_spacing(4)
        self.attach(self.sample, 0, 7, 4, 2)

        self.show_all()

    def on_draw(self, widget, ctx):

        br = self.brightness
        r = (self.backlight_red * br) / 0xff
        g = (self.backlight_green * br) / 0xff
        b = (self.backlight_blue * br) / 0xff
        
        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        
        ctx.set_source_rgba (r,g,b,1)
        ctx.rectangle(0,0,w,h)
        ctx.fill()

    def on_switch_change(self, widget, state):
        self.scale.set_sensitive(state)
        
        if (not state):
            self.backlight_red = 0
            self.backlight_green = 0
            self.backlight_blue = 0
            
            self.write_backlight()
        else:
            self.backlight_red = 0xff
            self.backlight_green = 0xff
            self.backlight_blue = 0xff
            
            self.write_backlight()
        
        self.sample.queue_draw()
    
    def on_brightness_change(self, widget, value):
        self.brightness = self.scale.get_value()
        self.sample.queue_draw()
        self.write_backlight()
    
    def on_color_change(self,widget, value):
        r,g,b=value
        
        self.backlight_red = 0xff * r
        self.backlight_green = 0xff * g
        self.backlight_blue = 0xff * b
        
        self.sample.queue_draw()
        self.write_backlight()
    
    def read_backlight(self):
    
        output = subprocess.getoutput('slimbookctl get-kbd-backlight')
        color = int(output,16)
        
        self.backlight_red = (color & 0xff0000) >> 16
        self.backlight_green = (color & 0x00ff00) >> 8
        self.backlight_blue = color & 0x0000ff
        
        output = subprocess.getoutput('slimbookctl get-kbd-brightness')
        self.brightness = int(color,16)
        
    def write_backlight(self):
        br = self.brightness
        r = int(self.backlight_red * br)
        g = int(self.backlight_green * br)
        b = int(self.backlight_blue * br)
        
        value = (r<<16) | (g<<8) | b
        
        subprocess.getoutput('slimbookctl set-kbd-backlight {0:06x}'.format(value))
        subprocess.getoutput('slimbookctl set-kbd-brightness {0:06x}'.format(br))
    
    def get_average_rgb(self):
        return (self.backlight_red + self.backlight_green + self.backlight_blue) / 3.0

