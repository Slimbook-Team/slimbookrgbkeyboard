#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import gi
import subprocess
import gettext, locale
import re #Busca patrones expresiones regulares

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


class SlimbookRGB(Gtk.Window):

    switch1 = Gtk.Switch()
    

#sudo tee /etc/modprobe.d/clevo-xsm-wmi.conf <<< options 'kb_color=red,red,red kb_brightness=10'
#sudo modprobe -r clevo_xsm_wmi && sudo modprobe clevo-xsm-wmi

    def __init__(self):
  
        #COMPROBATION

        

        call = subprocess.getstatusoutput('ls /lib/modules/$(uname -r)/extra/clevo-xsm-wmi.ko')   
                   
        """ if os.system("python3 "+currpath+"/custom_conf.sh") == 0:
            print ("ok") """

        
        if call[0] == 0:
            print('Module detected!')
            try:
                self.get_value("last_color")

            except:
                print("Rewriting .conf (adding last_color)")
                #REQUIRES SUDO
                """ with open('/etc/modprobe.d/clevo-xsm-wmi.conf', 'w') as file:
                    file.write('options clevo-xsm-wmi kb_color=white,white,white, kb_brightness=10')
                """
                with open('/etc/modprobe.d/clevo-xsm-wmi.conf', 'a') as file:
                    file.write('\n#last_color=white\n')


        else:      

            #Instalar directamente --> os.system("python3 "+currpath+"/install_window.py")

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
        red_btn.connect('clicked', self.color_change,'red')
        btn_box.pack_start(red_btn, True, True, 0)

        green_btn= Gtk.Button()
        green_btn.set_name('green')
        green_btn.connect('clicked', self.color_change, 'green')
        btn_box.pack_start(green_btn, True, True, 0)

        blue_btn= Gtk.Button()
        blue_btn.set_name('blue')
        blue_btn.connect('clicked', self.color_change, 'blue')
        btn_box.pack_start(blue_btn, True, True, 0)

        white_btn= Gtk.Button()
        white_btn.set_name('white')
        white_btn.connect('clicked', self.color_change, 'white')
        btn_box.pack_start(white_btn, True, True, 0)

        yellow_btn= Gtk.Button()
        yellow_btn.set_name('yellow')
        yellow_btn.connect('clicked', self.color_change, 'yellow')
        btn_box.pack_start(yellow_btn, True, True, 0)

        magenta_btn= Gtk.Button()
        magenta_btn.set_name('magenta')
        magenta_btn.connect('clicked', self.color_change, 'magenta')
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
        grid.attach(scale, 2, 1, 2, 1)

        grid.attach(colors_lbl, 0, 4, 4, 1)

        grid.attach(btn_box, 0, 6, 4, 1)
        
        grid.attach(icon, 4, 0, 2, 7)
        grid.attach(evnt_box, 4, 10, 2, 1)

        win_box.pack_start(grid, False, False, 0)
        

    def about_us(self, widget, x):
        print('\nINFO:')
        print('\n')
        #Abre la ventana de info
        print('sudo -u '+USER+' python3 '+currpath+'/slimbookrgbkeyboardinfo.py')
        os.system('sudo -u '+USER+' python3 '+currpath+'/slimbookrgbkeyboardinfo.py')

    #Returns a str with param actual_value in .conf
    def get_value(self, parameter):
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
            #If switch is on; we also apply changes
            if self.switch1.get_active() == True:
                os.system("sudo sed -i 's/"+param+"/"+new_value+"/g' /etc/modprobe.d/clevo-xsm-wmi.conf") 
                os.system('sudo modprobe -r clevo_xsm_wmi && sudo modprobe clevo-xsm-wmi')  
    
    def light_change(self, scale, X):

        #Existent value
        old_value = self.get_value('kb_brightness')
        param = 'kb_brightness='+old_value

        new_value = 'kb_brightness='+str(scale.get_value())[:-2]

        print (param+' will be replaced by '+new_value)

        os.system("sudo sed -i 's/"+param+"/"+new_value+"/g' /etc/modprobe.d/clevo-xsm-wmi.conf")
        os.system('sudo modprobe -r clevo_xsm_wmi && sudo modprobe clevo-xsm-wmi')

  

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