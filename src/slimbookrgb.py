#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import gi
import subprocess
import gettext, locale
import re

from slimbookrgbkeyboardinfo import CURRENT_PATH #Busca patrones expresiones regulares

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gdk, Gtk, GdkPixbuf

currpath = os.path.dirname(os.path.realpath(__file__))
USER = subprocess.getoutput("logname")
#IDIOMAS ----------------------------------------------------------------

# CMD(Genera .pot):  pygettext -d slimbookamdcontrollercopy slimbookamdcontrollercopy.py
# CMD(Genera .mo a partir de .po):  msgfmt -o slimbookamdcontrollercopy.po slimbookamdcontrollercopy.mo

entorno_usu = locale.getlocale()[0]
if entorno_usu.find("en") >= 0 or entorno_usu.find("es") >= 0 or entorno_usu.find("fr") >= 0:
	idiomas = [entorno_usu]
else: 
    idiomas = ['en_EN'] 

""" entorno_usu="fr_FR"
idiomas = ['fr_FR']  """

print('Language: ', entorno_usu)
t = gettext.translation('slimbookamdcontroller',
						currpath+'/locale',
						languages=idiomas,
						fallback=True,) 
_ = t.gettext


MODULEDIR = "/sys/devices/platform/clevo_platform/"

class SlimbookRGB(Gtk.Window):

    switch1 = Gtk.Switch()
    

#sudo tee /etc/modprobe.d/clevo_platform.conf <<< options 'kb_color=red,red,red kb_brightness=10'
#sudo modprobe -r clevo_xsm_wmi && sudo modprobe clevo_platform

    def __init__(self):
  
        #COMPROBATION

        call = subprocess.getstatusoutput('modinfo clevo_platform')   
        
        if call[0] == 0:
            print('Module detected!')
            with open('/etc/modprobe.d/clevo_platform.conf', 'w') as file:
                file.write('options clevo_platform brightness=255 state=1 color_left=0x0000ff color_center=0x0000ff color_right=0x0000ff')

        else:      
            #Preguntar antes de instalar
            print('Module is not installed')
            os.system("python3 "+currpath+"/install_window.py")


    # WINDOW       

        Gtk.Window.__init__(self, title ="Slimbook RGB Keyboard")    
        self.set_icon_from_file(currpath+"/images/icono.png") 
        self.set_size_request(500,300) #anchoxalto
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.get_style_context().add_class("bg-image")  
        #self.set_decorated(False)

        win_box= Gtk.VBox()
        self.add(win_box) 

        # -- SWITCH --
        if not self.get_value('state')[1]=='0':
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
            value=float(self.get_brightness())/255 * 100
        except:
            value=float(self.get_value("brightness")[1])/255 * 100
        self.scale.set_value(value)
        self.scale.connect("button-release-event", self.set_brightness)
        self.scale.set_sensitive(False) if not self.switch1.get_active() else print("Scale active")
        # print('Scale loaded: '+value)

    # CONTENT -------------------------------------

        pixbuf1 = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = currpath+'/images/logo.png',
			width = 300,
			height = 100,
			preserve_aspect_ratio=True)
        
        logo = Gtk.Image.new_from_pixbuf(pixbuf1)
        logo.get_style_context().add_class("logo")
        logo.set_halign(Gtk.Align.START)
        logo_box =Gtk.Box()
        logo_box.pack_start(logo, True, True, 0)

        win_box.pack_start(logo_box, True, True, 0)

        label1 = Gtk.Label(label=_("Light switch"))
        label1.set_halign(Gtk.Align.START)
        label1.set_name('labelw')

        label2 = Gtk.Label(label=_("Brightness"))
        label2.set_halign(Gtk.Align.START)
        label2.set_name('labelw')

        btn_box= Gtk.HBox(spacing=30)
        
        red_btn= Gtk.Button()
        red_btn.set_name('red')
        red_btn.connect('clicked', self.color_change,'0xff0000')
        btn_box.pack_start(red_btn, True, True, 0)

        green_btn= Gtk.Button()
        green_btn.set_name('green')
        green_btn.connect('clicked', self.color_change, '0x00ff00')
        btn_box.pack_start(green_btn, True, True, 0)

        blue_btn= Gtk.Button()
        blue_btn.set_name('blue')
        blue_btn.connect('clicked', self.color_change, '0x0000ff')
        btn_box.pack_start(blue_btn, True, True, 0)

        white_btn= Gtk.Button()
        white_btn.set_name('white')
        white_btn.connect('clicked', self.color_change, '0xffffff')
        btn_box.pack_start(white_btn, True, True, 0)

        yellow_btn= Gtk.Button()
        yellow_btn.set_name('yellow')
        yellow_btn.connect('clicked', self.color_change, '0xffff00')
        btn_box.pack_start(yellow_btn, True, True, 0)

        magenta_btn= Gtk.Button()
        magenta_btn.set_name('magenta')
        magenta_btn.connect('clicked', self.color_change, '0xff00ff')
        btn_box.pack_start(magenta_btn, True, True, 0)

        colors_lbl = Gtk.Label(label='Colors')
        colors_lbl.set_name('labelw')
        colors_lbl.set_halign(Gtk.Align.START)

        pixbuf1 = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = currpath+'/images/icono.png',
			width = 150,
			height = 150,
			preserve_aspect_ratio=True)

        
        icon = Gtk.Image.new_from_pixbuf(pixbuf1)
        icon.get_style_context().add_class("logo")
        icon.set_halign(Gtk.Align.CENTER)


    # Info
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = currpath+'/images/question.png',
			width = 30,
			height = 30,
			preserve_aspect_ratio=True)

        iconApp = Gtk.Image.new_from_pixbuf(pixbuf)
        iconApp.get_style_context().add_class("help")
        iconApp.set_halign(Gtk.Align.END)

        lbl_info = Gtk.Label(label="Info  ")


        info_box = Gtk.Box()
        info_box.pack_start(lbl_info, True, True, 0)
        info_box.pack_start(iconApp, True, True, 0)

        evnt_box = Gtk.EventBox()
        evnt_box.add(info_box)
        evnt_box.set_halign(Gtk.Align.END)

        evnt_box.connect("button_press_event", self.about_us)

    # Grid attach --------------------------------------------------

        grid = Gtk.Grid(column_homogeneous=True,
                         row_homogeneous=False,
                         column_spacing=10,
                         row_spacing=10)

        grid.set_halign(Gtk.Align.CENTER)

        grid.attach(label1, 0, 0, 1, 1)
        grid.attach(self.switch1, 3, 0, 1, 1)
        grid.attach(label2, 0, 1, 1, 1)
        grid.attach(self.scale, 2, 1, 2, 1)

        grid.attach(colors_lbl, 0, 4, 4, 1)

        grid.attach(btn_box, 0, 6, 4, 1)
        
        grid.attach(icon, 4, 0, 2, 7)
        grid.attach(evnt_box, 4, 10, 2, 1)

        win_box.pack_start(grid, False, False, 0)
        

    def about_us(self, widget, x):
        import slimbookrgbkeyboardinfo

    #Returns a str with param actual_value in .conf
    def get_value(self, parameter):
        exit_code, res = subprocess.getstatusoutput('cat /etc/modprobe.d/clevo_platform.conf' )
        if exit_code == 0:
            res = str(res)
            patron = re.compile("{}\=(\w+)".format(parameter)).search(res)
            return patron
        else:
            try:
                file = os.path.join(CURRENT_PATH, "configuration", "clevo_platform.conf")
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
        exit_code, result = subprocess.getstatusoutput("cat {}{}".format(MODULEDIR, "brightness"))
        return result
        # result = int(255 * int(value) / 100)

    def set_brightness(self, scale, X):

        value = str(scale.get_value())[:-2]

        result = int(255 * int(value) / 100)

        self.apply_and_save(result, "brightness")

    def apply_and_save(self, value, var):
        print("Apply: "+str(value)+" "+str(var))
        group = self.get_value(var).group()
        os.system("echo {} | tee {}{}".format(value, MODULEDIR, var))
        os.system("sudo sed -i 's/{}/{}={}/g' /etc/modprobe.d/clevo_platform.conf".format(group, var, value))


#CSS
style_provider = Gtk.CssProvider()
style_provider.load_from_path(currpath+'/style.css')

Gtk.StyleContext.add_provider_for_screen (
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
win = SlimbookRGB()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()