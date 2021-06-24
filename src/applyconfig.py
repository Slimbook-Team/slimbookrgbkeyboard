#!/usr/bin/python3
# -*- coding: utf-8 -*-

#triggered by .autostrart
import os
import sys
import subprocess
import configparser

from configparser import ConfigParser

USER_NAME = subprocess.getoutput('last -wn1 | head -n 1 | cut -f 1 -d " "')
print("Username: "+USER_NAME)

HOMEDIR = subprocess.getoutput("echo ~"+USER_NAME)
print("Homedir: "+HOMEDIR+"\n")


config_file = HOMEDIR+'/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf'
print("---- "+config_file+"\n")

config = ConfigParser()
config.read(config_file)

os.system("cat "+config_file)

def main(args):
    check_config()
    #print("Total Args --> "+ str(len(args)) +" --> arg[0] = "+args[0])
    print(str(args))
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

        
        elif args[1]  == "pre":
            print('Suspending ...')
            os.system("sudo ite8291r3-ctl off")  #Turn off keyboard
            call = subprocess.getstatusoutput("sudo su -c 'echo 0 > /sys/class/leds/qc71_laptop\:\:lightbar/brightness'")
            print(str(call))#Apply 

            # We change our variable: config.set(section, variable, value)
            config.set('CONFIGURATION', "suspension", "")

            # Writing our configuration file 
            with open(config_file, 'w') as configfile:
                config.write(configfile)

        elif args[1] == "post":


            if config.get('CONFIGURATION', 'state'):

                state = config.get('CONFIGURATION', 'state')
                effect = config.get('CONFIGURATION', 'effect')
                brightness = config.get('CONFIGURATION', 'brightness')
                suspension = config.get('CONFIGURATION', 'suspension')

                lb_state = config.get('CONFIGURATION', 'lb_state')
                lb_rainbow = config.get('CONFIGURATION', 'lb_rainbow')
                lb_color = config.get('CONFIGURATION', 'lb_color')

                # We apply the keyboard config
                if state=="on":
                    print(state)
                    os.system(effect)
                    call = subprocess.getstatusoutput(effect)   
                    print("Exit: "+str(call))#Apply state

                    call = subprocess.getstatusoutput("sudo ite8291r3-ctl brightness "+brightness)   
                    print("Exit: "+str(call))#Apply state

                else:
                    os.system("sudo ite8291r3-ctl off")  

                # We apply the lightbar config
                if lb_state == "1":
                    print("Aplicando cambios lightbar")    

                    print("Aplicando color "+lb_state)            	
                    call = subprocess.getstatusoutput("sudo su -c 'echo "+lb_state+" > /sys/class/leds/qc71_laptop\:\:lightbar/brightness'")
                    #print("Exit: "+str(call[0]))#Apply state   
                    print("Exit: "+str(call))#Apply state       	
                    
                    print("Aplicando rainbow "+lb_rainbow)
                    call = subprocess.getstatusoutput("sudo su -c 'echo "+lb_rainbow+" > /sys/class/leds/qc71_laptop\:\:lightbar/rainbow_mode'")
                    #print("Exit: "+str(call[0]))#Apply rainbow
                    print("Exit: "+str(call))#Apply state      
                    
                    print("Aplicando color "+lb_color)            	
                    call = subprocess.getstatusoutput("sudo su -c 'echo "+lb_color+" > /sys/class/leds/qc71_laptop\:\:lightbar/color'")
                    #print("Exit: "+str(call[0]))#Apply color
                    print("Exit: "+str(call))#Apply state      
                    
                else:
                    os.system("echo 0 > /sys/class/leds/qc71_laptop\:\:lightbar/brightness")  #Turn off light bar 
    
def check_config():
    
    if os.path.isfile(HOMEDIR+'/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf'):
        print('File .conf already exists\n')           
    else:
        print ("File doesn't exist")

        if os.path.exists (HOMEDIR+'/.config/slimbookrgbkeyboard'):
            print('Directory already exists')
            os.system('sudo -u '+USER_NAME+' touch '+HOMEDIR+'/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf')
            print('Creating file')

            with open( HOMEDIR + '/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf', 'w') as conf:
                fichero_conf().write(conf)
            
            print('File created succesfully!\n')
            
            print(os.system("cat "+ HOMEDIR + "/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf"))

        else:
            print("Directory doesen't exist")
            os.system('mkdir '+HOMEDIR+'/.config/slimbookrgbkeyboard')
            os.system('touch '+HOMEDIR+'/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf')
            print('Creating file')

            with open( HOMEDIR + '/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf', 'w') as conf:
                fichero_conf().write(conf)
            
            print('File created succesfully!\n')

            print(os.system("cat "+ HOMEDIR + "/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf"))

#Genera config_object para el .conf
def fichero_conf():
    config_object = ConfigParser()

    config_object["CONFIGURATION"] = {
    "state": "on",                
    "effect": "sudo ite8291r3-ctl effect rainbow",
    "brightness": "50",   
    "suspension": "",
    "lb_state": "0",
    "lb_rainbow": "0",
    "lb_color": "777"

    }
    return config_object            
    

if __name__ == "__main__":
    #Se obtiene las variables que se le pasa desde el archivo /usr/share/slimbookface/slimbookface
    main(sys.argv)