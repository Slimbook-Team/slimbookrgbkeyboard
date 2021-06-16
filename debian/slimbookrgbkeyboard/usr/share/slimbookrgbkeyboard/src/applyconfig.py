#!/usr/bin/python3
# -*- coding: utf-8 -*-

#unused yet but it will go on .autostrart
import os
import sys
import subprocess
from configparser import ConfigParser

USER_NAME = subprocess.getoutput("logname")
print("Username: "+USER_NAME)

HOMEDIR = subprocess.getoutput("echo ~"+USER_NAME)
print("Homedir: "+HOMEDIR+"\n")

config_file = HOMEDIR+'/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf'

config = ConfigParser()
config.read(config_file)

os.system("cat "+config_file)

def main(args):

    #print("Total Args --> "+ str(len(args)) +" --> arg[0] = "+args[0])

    # Argument 0 is the current route
    if len(args) > 1:
        print("Setting "+args[1]+" ...")


        if args[1] == "state":
            state = config.get('CONFIGURATION', 'state')
            if state == "on":
                effect = config.get('CONFIGURATION', 'effect')
                os.system(effect)
            else:   
                os.system("sudo ite8291r3-ctl off") 
            
        elif args[1] == "effect":
            effect = config.get('CONFIGURATION', 'effect')
            os.system(effect)

        elif args[1] == "brightness":
            brightness = config.get('CONFIGURATION', 'brightness')
            os.system("sudo ite8291r3-ctl brightness "+brightness)  

        elif args[1] == "lb_state":
            lb_state = config.get('CONFIGURATION', 'lb_state')
            print("Aplicando color "+lb_state)            	
            call = subprocess.getstatusoutput("sudo su -c 'echo "+lb_state+" > /sys/class/leds/qc71_laptop\:\:lightbar/brightness'")
            print("Exit: "+str(call[0]))#Apply state        	

        elif args[1] == "lb_rainbow":
            lb_rainbow = config.get('CONFIGURATION', 'lb_rainbow')
            print("Aplicando rainbow "+lb_rainbow)
            call = subprocess.getstatusoutput("sudo su -c 'echo "+lb_rainbow+" > /sys/class/leds/qc71_laptop\:\:lightbar/rainbow_mode'")
            print("Exit: "+str(call[0]))#Apply rainbow
        
        elif args[1] == "lb_color":
            lb_color = config.get('CONFIGURATION', 'lb_color')
            print("Aplicando color "+lb_color)            	
            call = subprocess.getstatusoutput("sudo su -c 'echo "+lb_color+" > /sys/class/leds/qc71_laptop\:\:lightbar/color'")
            print("Exit: "+str(call[0]))#Apply color

    else:
        
        if config.get('CONFIGURATION', 'state'):
            state = config.get('CONFIGURATION', 'state')
            effect = config.get('CONFIGURATION', 'effect')
            brightness = config.get('CONFIGURATION', 'brightness')
            suspension = config.get('CONFIGURATION', 'suspension')

            lb_state = config.get('CONFIGURATION', 'lb_state')
            lb_rainbow = config.get('CONFIGURATION', 'lb_rainbow')
            lb_color = config.get('CONFIGURATION', 'lb_color')
        

        if suspension=="pre":
            os.system("sudo ite8291r3-ctl off")  #Turn off keyboard
            call = subprocess.getstatusoutput("sudo su -c 'echo 0 > /sys/class/leds/qc71_laptop\:\:lightbar/brightness'")
            print(str(call))#Apply 

            # We change our variable: config.set(section, variable, value)
            config.set('CONFIGURATION', "suspension", "")

            # Writing our configuration file 
            with open(config_file, 'w') as configfile:
                config.write(configfile)

        else:
            if suspension=="post" or suspension=="":
                # We apply the config
                if state=="on":
                    os.system(effect)
                    os.system("sudo ite8291r3-ctl brightness "+brightness)   
                    
                else:
                    os.system("sudo ite8291r3-ctl off")  

                # We apply the config
                if lb_state == "1":
                    print("Aplicando cambios lightbar")    

                    print("Aplicando color "+lb_state)            	
                    call = subprocess.getstatusoutput("sudo su -c 'echo "+lb_state+" > /sys/class/leds/qc71_laptop\:\:lightbar/brightness'")
                    print("Exit: "+str(call[0]))#Apply state        	
                    
                    print("Aplicando rainbow "+lb_rainbow)
                    call = subprocess.getstatusoutput("sudo su -c 'echo "+lb_rainbow+" > /sys/class/leds/qc71_laptop\:\:lightbar/rainbow_mode'")
                    print("Exit: "+str(call[0]))#Apply rainbow
                    
                    print("Aplicando color "+lb_color)            	
                    call = subprocess.getstatusoutput("sudo su -c 'echo "+lb_color+" > /sys/class/leds/qc71_laptop\:\:lightbar/color'")
                    print("Exit: "+str(call[0]))#Apply color
                    
                else:
                    os.system("echo 0 > /sys/class/leds/qc71_laptop\:\:lightbar/brightness")  #Turn off light bar 
            
        
os.system("cat "+config_file)

if __name__ == "__main__":
    #Se obtiene las variables que se le pasa desde el archivo /usr/share/slimbookface/slimbookface
    main(sys.argv)