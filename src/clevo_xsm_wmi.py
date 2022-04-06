import gi
import utils
import os, subprocess
import configparser

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from os.path import expanduser
from gi.repository import Gdk, Gtk, GdkPixbuf

USER_NAME = utils.get_user()

HOMEDIR = expanduser("~".format(USER_NAME))

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

CONFIG_FILE = os.path.join(
    HOMEDIR, '/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf')

_ = utils.load_translation('slimbookrgb')

class Grid(Gtk.Grid):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('column_homogeneous', True)
        kwargs.setdefault('column_spacing', 0)
        kwargs.setdefault('row_spacing', 20)
        # kwargs.setdefault('halign', Gtk.Align.CENTER)
        # kwargs.setdefault('valign', Gtk.Align.CENTER)
        super(Grid, self).__init__(*args, **kwargs)

        self.setup()

    def setup(self):
    
        self.switch1 = Gtk.Switch()
        if not self.get_value('kb_color')=='black':
            self.switch1.set_active(True)
        print('Switch  loaded: '+str(self.switch1.get_state()))

        self.switch1.set_halign(Gtk.Align.END)
        self.switch1.connect("state-set", self.switch_light)

        # -- SCALE --
        scale = Gtk.Scale.new_with_range(
            orientation=Gtk.Orientation.HORIZONTAL,
            min=0,
            max=10,
            step=1
        )
        print('Scale loaded: '+self.get_value('kb_brightness'))
        scale.set_value(value=float(self.get_value('kb_brightness')))
        scale.connect("button-release-event", self.light_change)

    # CONTENT -------------------------------------

        label1 = Gtk.Label(label=_("Light switch"))
        label1.set_halign(Gtk.Align.START)
        label1.set_name('labelw')

        label2 = Gtk.Label(label=_("Brightness"))
        label2.set_halign(Gtk.Align.START)
        label2.set_name('labelw')

        btn_box = Gtk.HBox(spacing=30)

        red_btn = Gtk.Button()
        red_btn.set_name('red')
        red_btn.connect('clicked', self.color_change,'red')
        btn_box.pack_start(red_btn, True, True, 0)

        green_btn = Gtk.Button()
        green_btn.set_name('green')
        green_btn.connect('clicked', self.color_change, 'green')
        btn_box.pack_start(green_btn, True, True, 0)

        blue_btn = Gtk.Button()
        blue_btn.set_name('blue')
        blue_btn.connect('clicked', self.color_change, 'blue')
        btn_box.pack_start(blue_btn, True, True, 0)

        white_btn = Gtk.Button()
        white_btn.set_name('white')
        white_btn.connect('clicked', self.color_change, 'white')
        btn_box.pack_start(white_btn, True, True, 0)

        yellow_btn = Gtk.Button()
        yellow_btn.set_name('yellow')
        yellow_btn.connect('clicked', self.color_change, 'yellow')
        btn_box.pack_start(yellow_btn, True, True, 0)

        magenta_btn = Gtk.Button()
        magenta_btn.set_name('magenta')
        magenta_btn.connect('clicked', self.color_change, 'magenta')
        btn_box.pack_start(magenta_btn, True, True, 0)

        colors_lbl = Gtk.Label(label='Colors')
        colors_lbl.set_name('labelw')
        colors_lbl.set_halign(Gtk.Align.START)

    # Grid attach --------------------------------------------------
   
        self.attach(label1, 0, 0, 1, 1)
        self.attach(self.switch1, 2, 0, 1, 1)
        self.attach(label2, 0, 1, 1, 1)
        self.attach(scale, 1, 1, 2, 1)
        self.attach(colors_lbl, 0, 4, 3, 1)
        self.attach(btn_box, 0, 6, 3, 1)

        self.show_all()

    #Returns a str with param actual_value in .conf
    def get_value(self, parameter):
        import re
        call = subprocess.getoutput('cat /etc/modprobe.d/clevo-xsm-wmi.conf' )
        salida = str(call)

        if parameter == 'kb_brightness':
            patron = re.compile("kb_brightness\=([0-9]{1,2})").search(call)[1]
        else:
            if parameter == 'kb_color':
                patron = re.compile("kb_color\=(\w{1,})\,\w{1,}\,\w{1,}").search(call)[1]
            else:
                if parameter == 'last_color':
                    patron = re.compile("last_color\=(\w{1,})").search(call)[1]
                else:
                    print('Non accepted parameter.')
        value = patron

        return value

    def switch_light(self, switch, state):      
        if switch.get_active() == True:
            print(switch.get_active())
            self.color_change(self, self.get_value('last_color'))
        else:    
            print(switch.get_active())    
            self.color_change(self, 'black')
            
    def color_change(self, widget, color):

        #Getting last color
        last_color = 'last_color='+self.get_value('last_color')

        #Getting color value
        old_value = self.get_value('kb_color')

        #The param we're gonna change
        param = 'kb_color='+old_value+','+old_value+','+old_value

        new_value = 'kb_color='+color+','+color+','+color

        print (param+' will be replaced by '+new_value)

        #If it's black, we apply changes
        if color == 'black':
            os.system("sudo sed -i 's/"+param+"/"+new_value+"/g' /etc/modprobe.d/clevo-xsm-wmi.conf") 
            os.system('sudo modprobe -r clevo_xsm_wmi && sudo modprobe clevo-xsm-wmi')  
        else:
            # If new_color is not black, we save it as a backup for switch on
            os.system("sudo sed -i 's/"+last_color+"/last_color="+color+"/g' /etc/modprobe.d/clevo-xsm-wmi.conf")
            
            # If switch is on; we also apply changes
            if self.switch1.get_active() == True:
                os.system("sudo sed -i 's/"+param+"/"+new_value+"/g' /etc/modprobe.d/clevo-xsm-wmi.conf") 
                os.system('sudo modprobe -r clevo_xsm_wmi && sudo modprobe clevo-xsm-wmi')  
    
    def light_change(self, scale, X):

        #Existent value
        old_value = self.get_value('kb_brightness')
        param = 'kb_brightness={}'.format(old_value)

        new_value = 'kb_brightness={}'.format(str(scale.get_value())[:-2])

        print ('{} will be replaced by {}'.format(param, new_value))

        os.system("sudo sed -i 's/{}/{}/g' /etc/modprobe.d/clevo-xsm-wmi.conf".format(param,new_value))
        os.system('sudo modprobe -r clevo_xsm_wmi && sudo modprobe clevo-xsm-wmi')

  