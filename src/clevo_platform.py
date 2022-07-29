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


class Grid(Gtk.Grid):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('column_homogeneous', True)
        kwargs.setdefault('column_spacing', 0)
        kwargs.setdefault('row_spacing', 20)
        # kwargs.setdefault('halign', Gtk.Align.CENTER)
        # kwargs.setdefault('valign', Gtk.Align.CENTER)
        super(Grid, self).__init__(*args, **kwargs)
        self.check_installation()
        self.setup()

    def setup(self):

        self.switch1 = Gtk.Switch()
        if not self.get_value('kb_color') == 'black':
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
        red_btn.connect('clicked', self.color_change, '0xFFOOOO')
        btn_box.pack_start(red_btn, True, True, 0)

        green_btn = Gtk.Button()
        green_btn.set_name('green')
        green_btn.connect('clicked', self.color_change, '0x7FFF00')
        btn_box.pack_start(green_btn, True, True, 0)

        blue_btn = Gtk.Button()
        blue_btn.set_name('blue')
        blue_btn.connect('clicked', self.color_change, '0x0000FF')
        btn_box.pack_start(blue_btn, True, True, 0)

        white_btn = Gtk.Button()
        white_btn.set_name('white')
        white_btn.connect('clicked', self.color_change, '0xFFFFFF')
        btn_box.pack_start(white_btn, True, True, 0)

        yellow_btn = Gtk.Button()
        yellow_btn.set_name('yellow')
        yellow_btn.connect('clicked', self.color_change, '0xFFFF00')
        btn_box.pack_start(yellow_btn, True, True, 0)

        magenta_btn = Gtk.Button()
        magenta_btn.set_name('magenta')
        magenta_btn.connect('clicked', self.color_change, '0xFF00FF')
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

    # Returns a str with param actual_value in .conf
    def get_value(self, parameter):
        import re
        call = subprocess.getoutput('cat /etc/modprobe.d/clevo_platform.conf')
        salida = str(call)

        if parameter == 'kb_brightness':
            patron = re.compile("kb_brightness\=([0-9]{1,2})").search(call)[1]
        else:
            if parameter == 'color_left':
                patron = re.compile("color_left\=(\w{1,})").search(call)[1]
            else:
                if parameter == 'color_center':
                    patron = re.compile(
                        "color_center\=(\w{1,})").search(call)[1]

                else:
                    if parameter == 'color_right':
                        patron = re.compile(
                            "color_right\=(\w{1,})").search(call)[1]
                    else:
                        if parameter == 'last_color':
                            patron = re.compile(
                                "last_color\=(\w{1,})").search(call)[1]
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
            self.color_change(self, '0x000000')

    def color_change(self, widget, color):

        # Getting last color
        last_color = 'last_color='+self.get_value('last_color')

        # Getting color value
        old_value = self.get_value('kb_color')
        colors = {
            'param1': 'color_left='+old_value,
            'param2': 'color_center='+old_value,
            'param3': 'color_right='+old_value,
        }

        new_values = {
            'new_value1' : 'color_left='+color,
            'new_value2' : 'color_center='+color,
            'new_value3' : 'color_right='+color,
        }

        for param in enumerate(colors):
            print(colors[param]+' will be replaced by '+new_values[param])

        # If it's black, we apply changes
        if color == 'black':
            os.system("sudo sed -i 's/"+param+"/"+new_value +
                      "/g' /etc/modprobe.d/clevo_platform.conf")
            os.system(
                'sudo modprobe -r clevo_platform && sudo modprobe clevo_platform')
        else:
            # If new_color is not black, we save it as a backup for switch on
            os.system("sudo sed -i 's/"+last_color+"/last_color=" +
                      color+"/g' /etc/modprobe.d/clevo_platform.conf")

            # If switch is on; we also apply changes
            if self.switch1.get_active() == True:
                os.system("sudo sed -i 's/"+param+"/"+new_value +
                          "/g' /etc/modprobe.d/clevo_platform.conf")
                os.system(
                    'sudo modprobe -r clevo_platform && sudo modprobe clevo_platform')

    def light_change(self, scale, X):

        # Existent value
        old_value = self.get_value('kb_brightness')
        param = 'kb_brightness={}'.format(old_value)

        new_value = 'kb_brightness={}'.format(str(scale.get_value())[:-2])

        print('{} will be replaced by {}'.format(param, new_value))

        os.system(
            "sudo sed -i 's/{}/{}/g' /etc/modprobe.d/clevo_platform.conf".format(param, new_value))
        os.system('sudo modprobe -r clevo_platform && sudo modprobe clevo_platform')

    def check_installation(self):
        # COMPROBATION
        call = subprocess.getstatusoutput(
            'ls /lib/modules/$(uname -r)/build/clevo_platform.ko')

        if call[0] == 0:
            print('Module detected!')
            try:
                self.get_value("last_color")

            except:
                print("Rewriting .conf (adding last_color)")
                # REQUIRES SUDO
                with open('/etc/modprobe.d/clevo_platform.conf', 'a') as file:
                    file.write('\n#last_color=white\n')

        else:
            # Instalar directamente --> os.system("python3 "+currpath+"/install_window.py")
            # Preguntar antes de instalar
            print('Module is not installed')

            os.system("python3 "+CURRENT_PATH+"/install_window.py")
