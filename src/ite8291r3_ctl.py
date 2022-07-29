#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi
import utils
import os, subprocess
import configparser

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from os.path import expanduser
from gi.repository import Gdk, Gtk

USER_NAME = utils.get_user()

HOMEDIR = expanduser("~".format(USER_NAME))

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

CONFIG_FILE = os.path.join(
    HOMEDIR, '/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf')

_ = utils.load_translation('slimbookrgb')

# CSS
style_provider = Gtk.CssProvider()
style_provider.load_from_path(CURRENT_PATH+'/style.css')

Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(
), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

class Grid(Gtk.Grid):
    os.system('python3 {}'.format(os.path.join(CURRENT_PATH, 'configuration/check_config.py')))

    config_file = HOMEDIR+'/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf'
    config = configparser.ConfigParser()
    config.read(config_file)

    def __init__(self, *args, **kwargs):

        kwargs.setdefault('column_homogeneous', True)
        kwargs.setdefault('column_spacing', 0)
        kwargs.setdefault('row_spacing', 20)
        super(Grid, self).__init__(*args, **kwargs)

        self.setup()

    def setup(self):
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(500)

        stack.add_titled(self.load_kb(), "grid", _("Keyboard"))
        stack.add_titled(self.load_lb(), "grid2", _("Lightbar"))

        # Lightbar settings check
        exit, text = subprocess.getstatusoutput('modprobe qc71_laptop')
        if exit == 0:
            print(' no lightbar')
            
            self.show_all()

        stack_switcher = Gtk.StackSwitcher(valign=Gtk.Align.START)
        stack_switcher.set_stack(stack)

        self.attach(stack_switcher, 0,0,5,1)
        self.attach(stack,0,2,5,4)

    def load_kb(self):
        
        print('\nLoading Keyboard options ...\n')

        # -- SWITCH --
        self.switch = Gtk.Switch()
        if not self.config.get('CONFIGURATION', 'state')=='off':
            self.switch.set_active(True)
        else:
            self.switch.set_active(False)
            
        print('Switch loaded: '+str(self.switch.get_state()))

        self.switch.set_halign(Gtk.Align.END)
        self.switch.connect("state-set", self.kb_switch_light)
        
        # -- SCALE --
        scale = Gtk.Scale.new_with_range(
            orientation=Gtk.Orientation.HORIZONTAL,
            min=0,
            max=50,
            step=1
        )
        value_s = float(self.config.get('CONFIGURATION', 'brightness'))
        print("Scale loaded: "+str(value_s))
        scale.set_value(value=value_s)
        
        scale.connect("button-release-event", self.kb_light_change)
        label_effects = Gtk.Label(label="Effects")
        label_effects.set_name('labelw')
        label_effects.set_halign(Gtk.Align.START)

        btn_folder = Gtk.ToolButton()
        btn_folder.set_icon_name('folder')
        btn_folder.connect('clicked', self.open_anim)
        btn_folder.set_halign(Gtk.Align.START)

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

        animations = subprocess.getoutput("ls "+CURRENT_PATH+"/animations").split("\n")
        print("animations ="+str(animations))

        for animation in animations:
            effect_store.append([animation])

        effects_combo = Gtk.ComboBox.new_with_model(effect_store)
        renderer_text = Gtk.CellRendererText()
        effects_combo.pack_start(renderer_text, True)
        effects_combo.add_attribute(renderer_text, "text", 0)

        # Try to load config last effect on combobox
        try:
            #The last value of 'command' is the effect
            config_effect = self.config.get('CONFIGURATION', 'effect').split(" ")[-1]

            #If last value contains 'animations/' --> It's a route to an anim file so we get just te anim
            if not config_effect.find("animations/")== -1:
                print("Found '/' in config effect, maybe anim")
                config_effect = self.config.get('CONFIGURATION', 'effect').split("/")[-1] #Just Anim name

            
            print("Config_effect: "+config_effect)
            config_effect_index = ""

            for i in range(len(effect_store)):
                model = effects_combo.get_model()
                if model[i][0] == config_effect:
                    config_effect_index = i
                    combo_effect = model[i][0]
                    print("Combo_effect: "+str(combo_effect))

            print("Index: "+str(config_effect_index))

         
            effects_combo.set_active(config_effect_index)
        except:
            print("Last selection was not an effect")

        effects_combo.connect("changed", self.kb_effect_changed)

        # KB BOTONES

        kb_switch = Gtk.Label(label=_("Light switch"))
        kb_switch.set_halign(Gtk.Align.START)
        kb_switch.set_name('labelw')

        label2 = Gtk.Label(label=_("Brightness"))
        label2.set_halign(Gtk.Align.START)
        label2.set_name('labelw')

        btn_box= Gtk.HBox(spacing=30)
        
        #{black,white,red,green,blue,yellow,aqua,purple,silver,gray,maroon,teal,orange}
           
        white_btn= Gtk.Button()
        white_btn.set_name('white')
        white_btn.connect('clicked', self.kb_color_change, 'white', effects_combo)
        btn_box.pack_start(white_btn, True, True, 0)

        aqua_btn= Gtk.Button()
        aqua_btn.set_name('aqua')
        aqua_btn.connect('clicked', self.kb_color_change, 'aqua', effects_combo)
        btn_box.pack_start(aqua_btn, True, True, 0)

        teal_btn= Gtk.Button()
        teal_btn.set_name('teal')
        teal_btn.connect('clicked', self.kb_color_change, 'teal', effects_combo)
        btn_box.pack_start(teal_btn, True, True, 0)

        blue_btn= Gtk.Button()
        blue_btn.set_name('blue')
        blue_btn.connect('clicked', self.kb_color_change, 'blue', effects_combo)
        btn_box.pack_start(blue_btn, True, True, 0)

        purple_btn= Gtk.Button()
        purple_btn.set_name('purple')
        purple_btn.connect('clicked', self.kb_color_change, 'purple', effects_combo)
        btn_box.pack_start(purple_btn, True, True, 0)

        red_btn= Gtk.Button()
        red_btn.set_name('red')
        red_btn.connect('clicked', self.kb_color_change,'red', effects_combo)
        btn_box.pack_start(red_btn, True, True, 0)

        orange_btn= Gtk.Button()
        orange_btn.set_name('orange')
        orange_btn.connect('clicked', self.kb_color_change, 'orange', effects_combo)
        btn_box.pack_start(orange_btn, True, True, 0)

        yellow_btn= Gtk.Button()
        yellow_btn.set_name('yellow')
        yellow_btn.connect('clicked', self.kb_color_change, 'yellow', effects_combo)
        btn_box.pack_start(yellow_btn, True, True, 0)

        green_btn= Gtk.Button()
        green_btn.set_name('green')
        green_btn.connect('clicked', self.kb_color_change, 'green', effects_combo)
        btn_box.pack_start(green_btn, True, True, 0)

        colors_lbl = Gtk.Label(label='Colors')
        colors_lbl.set_name('labelw')
        colors_lbl.set_halign(Gtk.Align.START)
        
    # Grid attach KB --------------------------------------------------
        kb_grid = Gtk.Grid(column_homogeneous=True,
                            row_homogeneous=False,
                            column_spacing=10,
                            row_spacing=20)

        kb_grid.attach(kb_switch, 0, 0, 2, 1)
        kb_grid.attach(self.switch, 2, 0, 2, 1)
        kb_grid.attach(label2, 0, 1, 2, 1)
        kb_grid.attach(scale, 2, 1, 2, 1)

        kb_grid.attach(colors_lbl, 0, 3, 5, 1)
        kb_grid.attach(btn_box, 0, 4, 6, 1)

        kb_grid.attach(label_effects, 0, 6, 5, 1)
        kb_grid.attach(effects_combo, 0, 7, 5, 1)
        kb_grid.attach(btn_folder, 5, 7, 1, 1)

        return kb_grid

    def load_lb(self):

        print('\nLoading Lightbar options ...\n')


        # -- LIGHTBAR SWITCH --
        self.lb_switch = Gtk.Switch()
        if not self.config.get('CONFIGURATION', 'lb_state')=='0':
            self.lb_switch.set_active(True)
        else:
            self.lb_switch.set_active(False)
            
        print('Switch  loaded: '+str(self.lb_switch.get_state()))

        self.lb_switch.set_halign(Gtk.Align.END)
        self.lb_switch.connect("state-set", self.lb_switch_light)

        # -- LIGHTBAR SWITCH --
        self.lb_rainbow_switch = Gtk.Switch()                 
        if not self.config.get('CONFIGURATION', 'lb_rainbow')=='0':
            self.lb_rainbow_switch.set_active(True)
        else:
            self.lb_rainbow_switch.set_active(False)
            
        print('Switch  loaded: '+str(self.lb_rainbow_switch.get_state()))

        self.lb_rainbow_switch.set_halign(Gtk.Align.END)
        self.lb_rainbow_switch.connect("state-set", self._lb_rainbow_switch)

        # LABELS
        lb_switch = Gtk.Label(label="Light switch")
        lb_switch.set_name('labelw')
        lb_switch.set_halign(Gtk.Align.START)

        label_rainbow = Gtk.Label(label="Rainbow mode")
        label_rainbow.set_name('labelw')
        label_rainbow.set_halign(Gtk.Align.START)

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

    # GRID ATTACH

        lb_grid = Gtk.Grid(column_homogeneous=True,
                    row_homogeneous=False,
                    column_spacing=10,
                    row_spacing=25)

        lb_grid.attach(lb_switch, 0, 0, 1, 1)
        lb_grid.attach(self.lb_switch, 1, 0, 2, 1)
        lb_grid.attach(label_rainbow, 0, 2, 1, 1)
        lb_grid.attach(self.lb_rainbow_switch, 1, 2, 2, 1)
        lb_grid.attach(Gtk.Separator(), 0, 4, 5, 1)
        lb_grid.attach(lb_colors_lbl, 0, 4, 5, 1)
        lb_grid.attach(lb_btn_box, 0, 6, 5, 1)

        return lb_grid


    def kb_effect_changed(self, combo):

        config = configparser.ConfigParser()
        config.read(self.config_file)
        tree_iter = combo.get_active_iter()

        if tree_iter is not None:
            model = combo.get_model()
            effect = model[tree_iter][0].lower()
            print("\nSelected: effect = %s" % effect)


            call = subprocess.getstatusoutput("ls "+CURRENT_PATH+"/animations/ | grep "+effect)
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
                command = "sudo ite8291r3-ctl anim --file "+CURRENT_PATH+"/animations/"+effect
                self.update_config_field("effect",command)
                os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec effect')
                print("\nAnim applied")
            
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec brightness')
                   
    def kb_switch_light(self, switch, state):     
        config = configparser.ConfigParser()
        config.read(self.config_file)
        

        if switch.get_active() == True:
            #Switch on load effect
            effect = config.get('CONFIGURATION', 'effect')
            self.update_config_field("state","on")
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec state')
        else:      
            self.update_config_field("state","off")    
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec state')

    def kb_color_change(self, widget, color, effects_combo):
        print(widget)

        if color[0:2].isnumeric():
            
            command = "sudo ite8291r3-ctl monocolor --rgb "+color
            self.update_config_field("effect",command) 
            effects_combo.set_active_iter(None)
            if self.switch.get_state():
                os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec effect') 
            else:
                self.switch.set_active(True)
            
        else:
            # If new_color is not black, we save it as a backup for switch on
            
            command = "sudo ite8291r3-ctl monocolor --name "+color
            self.update_config_field("effect",command)  
            effects_combo.set_active_iter(None)
            if self.switch.get_state():
                os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec effect') 
            else:
                self.switch.set_active(True)

    def kb_light_change(self, scale, value):

        #Existent value

        new_value = str(scale.get_value())[:-2]
        self.update_config_field("brightness", new_value)
        os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec brightness')


    def lb_switch_light(self, switch, state):     
        config = configparser.ConfigParser()
        config.read(self.config_file)
        
        if switch.get_active() == True:
            #Switch on load effect
            self.update_config_field("lb_state","1")
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec lb_state')
        else:      
            self.update_config_field("lb_state","0")    
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec lb_state')

    def _lb_rainbow_switch(self, switch, state):     
        config = configparser.ConfigParser()
        config.read(self.config_file)
        
        if switch.get_active() == True:
            #Switch on load effect
            self.update_config_field("lb_rainbow","1")
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec lb_rainbow')
        else:      
            self.update_config_field("lb_rainbow","0")    
            os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec lb_rainbow')
            
    def lb_color_change(self, widget, color):

        self.lb_switch.set_active(True)
        if self.lb_rainbow_switch.get_state():
            print('Rainbow deactivation')
            self.lb_rainbow_switch.set_active(False)
        self.update_config_field("lb_color", color)
        os.system('pkexec slimbookrgbkeyboard-applyconfig-pkexec lb_color')    

    
    def open_anim(self, button):
        os.system('xdg-open '+CURRENT_PATH+'/animations')

    def update_config_field(self, variable, value):
        
        fichero = HOMEDIR + '/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf'
        config = configparser.ConfigParser()
        config.read(fichero)
        
        # We change our variable: config.set(section, variable, value)
        config.set('CONFIGURATION', str(variable), str(value))

        # Writing our configuration file 
        with open(fichero, 'w') as configfile:
            config.write(configfile)
