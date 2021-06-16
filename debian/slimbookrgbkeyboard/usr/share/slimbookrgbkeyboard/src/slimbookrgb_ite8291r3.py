#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import gi
import subprocess
import configparser
import gettext, locale
import re #Busca patrones expresiones regulares

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from configparser import ConfigParser
from gi.repository import Gdk, Gtk, GdkPixbuf
from os.path import expanduser

USER_NAME= subprocess.getoutput("logname")
HOMEDIR = subprocess.getoutput("echo ~"+USER_NAME)

#user = expanduser("~")

currpath = os.path.dirname(os.path.realpath(__file__))
config_object = ConfigParser()
config_file = HOMEDIR+'/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf'

print("Username: "+USER_NAME)
print("Homedir: "+HOMEDIR)
print("Configfiledir: "+config_file)
print()


#IDIOMAS ----------------------------------------------------------------

# CMD(Genera .pot):  pygettext -d slimbookamdcontrollercopy slimbookamdcontrollercopy.py
# CMD(Genera .mo a partir de .po):  msgfmt -o slimbookamdcontrollercopy.po slimbookamdcontrollercopy.mo

entorno_usu = locale.getlocale()[0]
if entorno_usu.find("es")>= 0:
	idiomas = [entorno_usu]
else: 
    idiomas = ['en_EN'] 

print('Language: ', entorno_usu)
t = gettext.translation('slimbookamdcontroller',
						currpath+'/locale',
						languages=idiomas,
						fallback=True,) 
_ = t.gettext

config = configparser.ConfigParser()
config.read(config_file)

class SlimbookRGB1(Gtk.Window):

    def __init__(self):
        self.check_config()

        config = configparser.ConfigParser()
        config.read(config_file)

        #Comprobación de autostart
        if os.path.exists(HOMEDIR+"/.config/autostart/slimbookrgbkeyboard-autostart.desktop"):
            print("Path exists")
        else:
            os.system("cp "+currpath+"/slimbookrgbkeyboard-autostart.desktop "+HOMEDIR+"/.config/autostart/slimbookrgbkeyboard-autostart.desktop")

    # WINDOW       
        
        Gtk.Window.__init__(self, title ="Slimbook RGB Keyboard")    
        self.set_icon_from_file(currpath+"/images/icono.png") 
        self.set_size_request(900,400) #anchoxalto
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.get_style_context().add_class("bg-image")  
        #self.set_decorated(False)

        win_box= Gtk.VBox()
        self.add(win_box)  

        # -- SWITCH --
        self.switch = Gtk.Switch()
        if not config.get('CONFIGURATION', 'state')=='off':
            self.switch.set_active(True)
        else:
            self.switch.set_active(False)
            
        print('Switch  loaded: '+str(self.switch.get_state()))

        self.switch.set_halign(Gtk.Align.END)
        self.switch.connect("state-set", self.kb_switch_light)
        
        # -- SCALE --
        self.scale = Gtk.Scale.new_with_range(
            orientation=Gtk.Orientation.HORIZONTAL,
            min=0,
            max=50,
            step=1
        )
        value_s = float(config.get('CONFIGURATION', 'brightness'))
        print("Scale loaded: "+str(value_s))
        self.scale.set_value(value=value_s)
        
        self.scale.connect("button-release-event", self.kb_light_change)

        # -- LIGHTBAR SWITCH --
        self.lb_switch = Gtk.Switch()
        if not config.get('CONFIGURATION', 'lb_state')=='0':
            self.lb_switch.set_active(True)
        else:
            self.lb_switch.set_active(False)
            
        print('Switch  loaded: '+str(self.lb_switch.get_state()))

        self.lb_switch.set_halign(Gtk.Align.END)
        self.lb_switch.connect("state-set", self.lb_switch_light)

        # -- LIGHTBAR SWITCH --
        self.lb_rainbow_switch = Gtk.Switch()
        if not config.get('CONFIGURATION', 'lb_rainbow')=='0':
            self.lb_rainbow_switch.set_active(True)
        else:
            self.lb_rainbow_switch.set_active(False)
            
        print('Switch  loaded: '+str(self.lb_rainbow_switch.get_state()))

        self.lb_rainbow_switch.set_halign(Gtk.Align.END)
        self.lb_rainbow_switch.connect("state-set", self._lb_rainbow_switch)

    # CONTENT -------------------------------------

        logo_box= Gtk.HBox()
        logo_box.set_hexpand(True)
        logo_box.set_vexpand(True)
        pixbuf1 = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = currpath+'/images/logo.png',
			width = 400,
			height = 100,
			preserve_aspect_ratio=True)

        
        logo = Gtk.Image.new_from_pixbuf(pixbuf1)
        logo.get_style_context().add_class("logo")
        logo.set_halign(Gtk.Align.START)

        logo_box.pack_start(logo, True, True, 0)

        win_box.pack_start(logo_box, True, True, 0)

        kb_switch = Gtk.Label(label=_("Light switch"))
        kb_switch.set_halign(Gtk.Align.START)
        kb_switch.set_name('labelw')

        label2 = Gtk.Label(label=_("Brightness"))
        label2.set_halign(Gtk.Align.START)
        label2.set_name('labelw')

    # KB BOTONES

        btn_box= Gtk.HBox(spacing=30)
        
        #{black,white,red,green,blue,yellow,aqua,purple,silver,gray,maroon,teal,orange}
           
        white_btn= Gtk.Button()
        white_btn.set_name('white')
        white_btn.connect('clicked', self.kb_color_change, 'white')
        btn_box.pack_start(white_btn, True, True, 0)

        aqua_btn= Gtk.Button()
        aqua_btn.set_name('aqua')
        aqua_btn.connect('clicked', self.kb_color_change, 'aqua')
        btn_box.pack_start(aqua_btn, True, True, 0)

        teal_btn= Gtk.Button()
        teal_btn.set_name('teal')
        teal_btn.connect('clicked', self.kb_color_change, 'teal')
        btn_box.pack_start(teal_btn, True, True, 0)

        blue_btn= Gtk.Button()
        blue_btn.set_name('blue')
        blue_btn.connect('clicked', self.kb_color_change, 'blue')
        btn_box.pack_start(blue_btn, True, True, 0)

        purple_btn= Gtk.Button()
        purple_btn.set_name('purple')
        purple_btn.connect('clicked', self.kb_color_change, 'purple')
        btn_box.pack_start(purple_btn, True, True, 0)

        red_btn= Gtk.Button()
        red_btn.set_name('red')
        red_btn.connect('clicked', self.kb_color_change,'red')
        btn_box.pack_start(red_btn, True, True, 0)

        orange_btn= Gtk.Button()
        orange_btn.set_name('orange')
        orange_btn.connect('clicked', self.kb_color_change, 'orange')
        btn_box.pack_start(orange_btn, True, True, 0)

        yellow_btn= Gtk.Button()
        yellow_btn.set_name('yellow')
        yellow_btn.connect('clicked', self.kb_color_change, 'yellow')
        btn_box.pack_start(yellow_btn, True, True, 0)

        green_btn= Gtk.Button()
        green_btn.set_name('green')
        green_btn.connect('clicked', self.kb_color_change, 'green')
        btn_box.pack_start(green_btn, True, True, 0)

    

        colors_lbl = Gtk.Label(label='Colors')
        colors_lbl.set_name('labelw')
        colors_lbl.set_halign(Gtk.Align.START)

    # LB BOTONES

        lb_btn_box= Gtk.HBox(spacing=30)
        
        #{black,white,red,green,blue,yellow,aqua,purple,silver,gray,maroon,teal,orange}
           
        white_btn= Gtk.Button()
        white_btn.set_name('white')
        white_btn.connect('clicked', self.lb_color_change, '999')
        lb_btn_box.pack_start(white_btn, True, True, 0)

        aqua_btn= Gtk.Button()
        aqua_btn.set_name('aqua')
        aqua_btn.connect('clicked', self.lb_color_change, '799')
        lb_btn_box.pack_start(aqua_btn, True, True, 0)

        teal_btn= Gtk.Button()
        teal_btn.set_name('teal')
        teal_btn.connect('clicked', self.lb_color_change, '688')
        lb_btn_box.pack_start(teal_btn, True, True, 0)

        blue_btn= Gtk.Button()
        blue_btn.set_name('blue')
        blue_btn.connect('clicked', self.lb_color_change, '009')
        lb_btn_box.pack_start(blue_btn, True, True, 0)

        purple_btn= Gtk.Button()
        purple_btn.set_name('purple')
        purple_btn.connect('clicked', self.lb_color_change, '909')
        lb_btn_box.pack_start(purple_btn, True, True, 0)

        red_btn= Gtk.Button()
        red_btn.set_name('red')
        red_btn.connect('clicked', self.lb_color_change,'900')
        lb_btn_box.pack_start(red_btn, True, True, 0)

        orange_btn= Gtk.Button()
        orange_btn.set_name('orange')
        orange_btn.connect('clicked', self.lb_color_change, '940')
        lb_btn_box.pack_start(orange_btn, True, True, 0)

        yellow_btn= Gtk.Button()
        yellow_btn.set_name('yellow')
        yellow_btn.connect('clicked', self.lb_color_change, '990')
        lb_btn_box.pack_start(yellow_btn, True, True, 0)

        green_btn= Gtk.Button()
        green_btn.set_name('green')
        green_btn.connect('clicked', self.lb_color_change, '090')
        lb_btn_box.pack_start(green_btn, True, True, 0)

        lb_colors_lbl = Gtk.Label(label='Ligtbar Colors')
        lb_colors_lbl.set_name('labelw')
        lb_colors_lbl.set_halign(Gtk.Align.START)

    # LABELS
        lb_switch = Gtk.Label(label="Light switch")
        lb_switch.set_name('labelw')
        lb_switch.set_halign(Gtk.Align.START)

        label_rainbow = Gtk.Label(label="Rainbow mode")
        label_rainbow.set_name('labelw')
        label_rainbow.set_halign(Gtk.Align.START)

        label_effects = Gtk.Label(label="Effects")
        label_effects.set_name('labelw')
        label_effects.set_halign(Gtk.Align.START)

        effect_store = Gtk.ListStore(str)
        effects = [
            "breathing",
            "wave",
            "random",
            "rainbow",
            "ripple",
            "marquee",
            "raindrop",
            "aurora",
            "fireworks"
        ]
        for effect in effects:
            effect_store.append([effect])

        animations = subprocess.getoutput("ls "+currpath+"/animations").split("\n")
        print("animations ="+str(animations))

        for animation in animations:
            effect_store.append([animation])


        self.effects_combo = Gtk.ComboBox.new_with_model(effect_store)
        renderer_text = Gtk.CellRendererText()
        self.effects_combo.pack_start(renderer_text, True)
        self.effects_combo.add_attribute(renderer_text, "text", 0)

    # Try to load config last effect on combobox
        try:
            #The last value of 'command' is the effect
            config_effect = config.get('CONFIGURATION', 'effect').split(" ")[-1]

            #If last value contains 'animations/' --> It's a route to an anim file so we get just te anim
            if not config_effect.find("animations/")== -1:
                print("Found '/' in config effect, maybe anim")
                config_effect = config.get('CONFIGURATION', 'effect').split("/")[-1] #Just Anim name

            
            print("Config_effect: "+config_effect)
            config_effect_index = ""

            for i in range(len(effect_store)):
                model = self.effects_combo.get_model()
                if model[i][0] == config_effect:
                    config_effect_index = i
                    combo_effect = model[i][0]
                    print("Combo_effect: "+str(combo_effect))

            print("Index: "+str(config_effect_index))

         
            self.effects_combo.set_active(config_effect_index)
        except:
            print("Last selection was not an effect")

        self.effects_combo.connect("changed", self.kb_effect_changed)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = currpath+'/images/icono.png',
			width = 200,
			height = 200,
			preserve_aspect_ratio=True)

        
        icon = Gtk.Image.new_from_pixbuf(pixbuf)
        icon.get_style_context().add_class("logo")
        icon.set_halign(Gtk.Align.CENTER)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = currpath+'/images/icono.png',
			width = 200,
			height = 200,
			preserve_aspect_ratio=True)

        icon2 = Gtk.Image.new_from_pixbuf(pixbuf)
        icon2.set_halign(Gtk.Align.CENTER)

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
        info_box.set_name("info")


        evnt_box = Gtk.EventBox()
        evnt_box.add(info_box)
        evnt_box.set_halign(Gtk.Align.END)
        

        evnt_box.connect("button_press_event", self.about_us)
    
  
        # Creating stack, transition type and transition duration.
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(500)
  

    # Grid attach KB --------------------------------------------------

        grid = Gtk.Grid(column_homogeneous=True,
                        row_homogeneous=False,
                        column_spacing=10,
                        row_spacing=20)

    
        grid.attach(kb_switch, 0, 0, 1, 1)
        grid.attach(self.switch, 3, 0, 1, 1)
        grid.attach(label2, 0, 1, 1, 1)
        grid.attach(self.scale, 2, 1, 2, 1)

        grid.attach(Gtk.Separator(), 0, 2, 5, 1)

        grid.attach(colors_lbl, 0, 3, 5, 1)
        grid.attach(btn_box, 0, 4, 5, 1)

        grid.attach(Gtk.Separator(), 0, 5, 5, 1)
        grid.attach(label_effects, 0, 6, 5, 1)
        grid.attach(self.effects_combo, 0, 7, 5, 1)

        grid.attach(icon, 5, 0, 3, 7)
        
        stack.add_titled(grid, "grid", "Keyboard")



        grid2 = Gtk.Grid(column_homogeneous=True,
                        row_homogeneous=False,
                        column_spacing=10,
                        row_spacing=20)

        grid2.attach(lb_switch, 0, 0, 1, 1)
        grid2.attach(self.lb_switch, 3, 0, 1, 1)
        grid2.attach(label_rainbow, 0, 2, 1, 1)
        grid2.attach(self.lb_rainbow_switch, 3, 2, 1, 1)
        grid2.attach(Gtk.Separator(), 0, 4, 5, 1)
        grid2.attach(lb_colors_lbl, 0, 5, 5, 1)
        grid2.attach(lb_btn_box, 0, 6, 5, 1)

        grid2.attach(icon2, 5, 0, 3, 10)
        

        stack.add_titled(grid2, "grid2", "Ligth bar")

        # Implementation of stack switcher.
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        

        win_box.pack_start(stack_switcher, True, True, 0)
        win_box.pack_start(stack, True, True, 0)


        win_box.pack_start(evnt_box, True, True, 0)

    def about_us(self, widget, x):
        print('\nINFO:')
        print('\n')
        #Abre la ventana de info
        os.system('python3 '+currpath+'/slimbookrgbkeyboardinfo.py')

    def kb_effect_changed(self, combo):

        config = configparser.ConfigParser()
        config.read(config_file)
        tree_iter = combo.get_active_iter()

        if tree_iter is not None:
            model = combo.get_model()
            effect = model[tree_iter][0].lower()
            print("\nSelected: effect = %s" % effect)


            call = subprocess.getstatusoutput("ls "+currpath+"/animations/ | grep "+effect)
            #print(str(call))

            if not (call[0]==0): #If not in animations --> effect

            #Chek if it's an effect or an animation
                command = "sudo ite8291r3-ctl effect "+effect
                self.update_config_field("effect",command)
                call = subprocess.getstatusoutput('pkexec slimbookrgbkeyboard-applyconfig-pkexec effect')

                if not call[0]==0: #This means there's no error message
                    raise ValueError("Can't execute as effect." )
                print("\nEffect applied") 

            else:
                print("\nI's not an effect going to apply as anim")
                command = "sudo ite8291r3-ctl anim --file "+currpath+"/animations/"+effect
                self.update_config_field("effect",command)
                os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec effect')
                print("\nAnim applied")
            
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec brightness')
                   
    def kb_switch_light(self, switch, state):     
        config = configparser.ConfigParser()
        config.read(config_file)
        

        if switch.get_active() == True:
            #Switch on load effect
            effect = config.get('CONFIGURATION', 'effect')
            self.update_config_field("state","on")
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec state')
        else:      
            self.update_config_field("state","off")    
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec state')       

    def lb_switch_light(self, switch, state):     
        config = configparser.ConfigParser()
        config.read(config_file)
        
        if switch.get_active() == True:
            #Switch on load effect
            self.update_config_field("lb_state","1")
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec lb_state')
        else:      
            self.update_config_field("lb_state","0")    
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec lb_state')

    def _lb_rainbow_switch(self, switch, state):     
        config = configparser.ConfigParser()
        config.read(config_file)
        
        if switch.get_active() == True:
            #Switch on load effect
            self.update_config_field("lb_rainbow","1")
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec lb_rainbow')
        else:      
            self.update_config_field("lb_rainbow","0")    
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec lb_rainbow')
    # TEST
    def kb_color_change(self, widget, color):

        if color[0:2].isnumeric():
            
            command = "sudo ite8291r3-ctl monocolor --rgb "+color
            self.update_config_field("effect",command) 
            self.effects_combo.set_active_iter(None)
            if self.switch.get_state():
                os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec effect') 
            else:
                self.switch.set_active(True)
            
        else:
            # If new_color is not black, we save it as a backup for switch on
            
            command = "sudo ite8291r3-ctl monocolor --name "+color
            self.update_config_field("effect",command)  
            self.effects_combo.set_active_iter(None)
            if self.switch.get_state():
                os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec effect') 
            else:
                self.switch.set_active(True)
            
    def lb_color_change(self, widget, color):

        self.lb_switch.set_active(True)
        self.update_config_field("lb_color", color)
        os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec lb_color')    

    def kb_light_change(self, scale, value):

        #Existent value

        new_value = str(scale.get_value())[:-2]
        self.update_config_field("brightness", new_value)
        os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec brightness')

    def check_config(self):
        if os.path.isfile(HOMEDIR+'/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf'):
            print('File .conf already exists\n')           
        else:
            print ("File doesn't exist")

            if os.path.exists (HOMEDIR+'/.config/slimbookrgbkeyboard'):
                print('Directory already exists')
                os.system('sudo -u '+USER_NAME+' touch '+HOMEDIR+'/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf')
                print('Creating file')

                with open( HOMEDIR + '/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf', 'w') as conf:
                    self.fichero_conf().write(conf)
                
                print('File created succesfully!\n')
                
                print(os.system("cat "+ HOMEDIR + "/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf"))

            else:
                print("Directory doesen't exist")
                os.system('mkdir '+HOMEDIR+'/.config/slimbookrgbkeyboard')
                os.system('touch '+HOMEDIR+'/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf')
                print('Creating file')

                with open( HOMEDIR + '/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf', 'w') as conf:
                    self.fichero_conf().write(conf)
                
                print('File created succesfully!\n')

                print(os.system("cat "+ HOMEDIR + "/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf"))

    #Genera config_object para el .conf
    def fichero_conf(self):
        
        config_object["CONFIGURATION"] = {
        "state": "on",                
        "effect": "effect here",
        "brightness": "50",   
        "suspension": "",
        "lb_state": "0",
        "lb_rainbow": "0",
        "lb_color": "999"

        }
        return config_object
  
    def update_config_field(self, variable, value):

        fichero = HOMEDIR + '/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf'
        config = configparser.ConfigParser()
        config.read(fichero)
        
        # We change our variable: config.set(section, variable, value)
        config.set('CONFIGURATION', str(variable), str(value))

        # Writing our configuration file 
        with open(fichero, 'w') as configfile:
            config.write(configfile)

        print("\n- Variable |"+variable+"| updated in .conf, actual value: "+value)


#CSS
style_provider = Gtk.CssProvider()
style_provider.load_from_path(currpath+'/style.css')

Gtk.StyleContext.add_provider_for_screen (Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
win = SlimbookRGB1()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
