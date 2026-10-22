import slimbook
import slimbook.info
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

        self.lb_color = 0
        self.lb_brightness = 0
        self.lb_rainbow = 0

        self.read_lightbar()
        
        self.switch1 = Gtk.Switch()
        self.switch1.set_halign(Gtk.Align.END)
        self.switch1.set_active(self.get_average_rgb() > 0)

        self.max_brightness = slimbook.kbd.brightness_max(0)
        
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(500)

        stack_switcher = Gtk.StackSwitcher(valign=Gtk.Align.START)
        stack_switcher.set_stack(stack)

        kb_grid = Gtk.Grid(column_homogeneous = True,
                            row_homogeneous = False,
                            column_spacing = 10,
                            row_spacing = 20)

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

        custom_lbl = Gtk.Label(label=_("Custom"))
        custom_lbl.set_halign(Gtk.Align.START)
        custom_lbl.set_name('labelw')
        custom_btn = Gtk.ColorButton()
        custom_btn.set_name('custom')
        custom_btn.connect('color-set', self.on_color_set)

        colors_lbl = Gtk.Label(label='Colors')
        colors_lbl.set_name('labelw')
        colors_lbl.set_halign(Gtk.Align.START)
        
        self.sample = Gtk.DrawingArea()
        self.sample.connect('draw', self.on_draw)
        self.sample.set_size_request(-1,32)
        
        kb_grid.set_halign(Gtk.Align.CENTER)
        kb_grid.attach(label1, 0, 0, 1, 1)
        kb_grid.attach(self.switch1, 3, 0, 1, 1)
        kb_grid.attach(label2, 0, 1, 1, 1)
        kb_grid.attach(self.scale, 2, 1, 2, 1)
        kb_grid.attach(custom_lbl, 0, 3, 1, 1)
        kb_grid.attach(custom_btn, 1, 3, 1, 1)
        kb_grid.attach(colors_lbl, 0, 5, 4, 1)
        kb_grid.attach(btn_box, 0, 6, 5, 1)

        kb_grid.set_row_spacing(4)
        kb_grid.attach(self.sample, 0, 7, 4, 2)

        stack.add_titled(self.load_kb(), "grid", _("Keyboard"))

        self.model = slimbook.info.get_model()

        # Only Titans have the lightbar
        if self.model & slimbook.info.SLB_MODEL_TITAN) > 0:
            pass


        self.attach(stack_switcher, 0,0,5,1)
        self.attach(stack,0,2,5,4)

        self.show_all()

    def on_draw(self, widget, ctx):

        
        r = (self.backlight_red) / 0xff
        g = (self.backlight_green) / 0xff
        b = (self.backlight_blue) / 0xff
        
        w = widget.get_allocated_width()
        h = widget.get_allocated_height()
        
        ctx.set_source_rgba (r,g,b,1)
        ctx.rectangle(0,0,w,h)
        ctx.fill()

    def on_color_set(self, colorbutton):
        color = colorbutton.get_rgba()

        self.backlight_red = int(0xff * color.red)
        self.backlight_green = int(0xff * color.green)
        self.backlight_blue = int(0xff * color.blue)

        self.sample.queue_draw()
        self.write_backlight()

    def on_switch_change(self, widget, state):
        self.scale.set_sensitive(state)
        
        if (not state):
            self.brightness = 0
            
            self.write_backlight()
        else:
            self.brightness = self.max_brightness
            
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
        self.brightness = int(output,16)
        
    def write_backlight(self):
        br = int(self.brightness)
        r = int(self.backlight_red)
        g = int(self.backlight_green)
        b = int(self.backlight_blue)
        
        value = (r<<16) | (g<<8) | b
        
        subprocess.getoutput('slimbookctl set-kbd-backlight {0:06x}'.format(value))
        subprocess.getoutput('slimbookctl set-kbd-brightness {0:06x}'.format(br))
    
    def get_average_rgb(self):
        return (self.backlight_red + self.backlight_green + self.backlight_blue) / 3.0


    def read_lightbar(self):
        output = subprocess.getoutput('slimbookctl get-lightbar-color')
        self.lb_color = int(output,10)

        output = subprocess.getoutput('slimbookctl get-lightbar-brightness')
        self.lb_brightness = int(output,10)

        output = subprocess.getoutput('slimbookctl get-lightbar-rainbow')
        self.lb_rainbow = int(output,10)



