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
MODULEDIR = "/sys/devices/platform/clevo_platform/"


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

        # -- SWITCH --
        self.switch1 = Gtk.Switch()
        if not self.get_value('state')[1] == '0':
            self.switch1.set_active(True)
        print('Switch  loaded: '+str(self.switch1.get_state()))

        self.switch1.set_halign(Gtk.Align.END)
        self.switch1.connect("state-set", self.switch_light)

        # -- SCALE --
        self.scale = Gtk.Scale.new_with_range(
            orientation=Gtk.Orientation.HORIZONTAL,
            min=0,
            max=100,
            step=1
        )
        try:
            value = float(self.get_brightness())/255 * 100
        except:
            value = float(self.get_value("brightness")[1])/255 * 100
        self.scale.set_value(value)
        self.scale.connect("button-release-event", self.set_brightness)
        self.scale.set_sensitive(
            False) if not self.switch1.get_active() else print("Scale active")

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

    # Grid attach --------------------------------------------------

        self.set_halign(Gtk.Align.CENTER)
        self.attach(label1, 0, 0, 1, 1)
        self.attach(self.switch1, 3, 0, 1, 1)
        self.attach(label2, 0, 1, 1, 1)
        self.attach(self.scale, 2, 1, 2, 1)
        self.attach(colors_lbl, 0, 4, 4, 1)
        self.attach(btn_box, 0, 6, 4, 1)

        self.show_all()

    # Returns a str with param actual_value in .conf
    def get_value(self, parameter):
        exit_code, res = subprocess.getstatusoutput(
            'cat /etc/modprobe.d/clevo_platform.conf')
        if exit_code == 0:
            res = str(res)
            patron = re.compile("{}\=(\w+)".format(parameter)).search(res)
            return patron
        else:
            try:
                file = os.path.join(
                    CURRENT_PATH, "configuration", "clevo_platform.conf")
                exit_code, res = subprocess.getstatusoutput("cat "+file)
                patron = re.compile("{}\=(\w+)".format(parameter)).search(res)
                return patron
            except:
                print("Failed to get clevo_platform.conf")

    def switch_light(self, switch, state):
        if switch.get_active():
            state = 1
            self.scale.set_sensitive(True)
        else:
            state = 0
            self.scale.set_sensitive(False)

        self.apply_and_save(state, "state")

    def color_change(self, widget, color):

        COLORS = {
            "color_left",
            "color_right",
            "color_center"
        }

        for color_zone in COLORS:

            self.apply_and_save(color, color_zone)

    def get_brightness(self):
        exit_code, result = subprocess.getstatusoutput(
            "cat {}{}".format(MODULEDIR, "brightness"))
        return result

    def set_brightness(self, scale, X):

        value = str(scale.get_value())[:-2]

        result = int(255 * int(value) / 100)

        self.apply_and_save(result, "brightness")

    def apply_and_save(self, value, var):
        print("Apply: "+str(value)+" "+str(var))
        group = self.get_value(var).group()
        sudo("echo {} | tee {}{}".format(value, MODULEDIR, var))
        sudo("sed -i 's/{}/{}={}/g' /etc/modprobe.d/clevo_platform.conf".format(group, var, value))

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
            print('Module is not installed')


def sudo(cmd):
    # print('pkexec slimbookrgbkeyboard-applyconfig-pkexec cmd "{}"'.format(cmd))
    os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec cmd "{}"'.format(cmd))
