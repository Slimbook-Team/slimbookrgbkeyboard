#!/usr/bin/python3
# -*- coding: utf-8 -*-

# triggered by .autostrart
import os
import sys
import subprocess
import utils
from configparser import ConfigParser

USER_NAME = utils.get_user()
HOMEDIR = os.path.expanduser("~{}".format(USER_NAME))
CONFIG_FILE = os.path.join(
    HOMEDIR, ".config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf")
print("Configuration file: {}\n".format(CONFIG_FILE))

AUTOSTART_FILE = os.path.join(
    HOMEDIR, ".config/autostart/slimbookrgbkeyboard-autostart.desktop")

config = ConfigParser()
config.read(CONFIG_FILE)




def main(args):
    check_config()
    # Argument 0 is the current route
    if len(args) > 1:
        print("Setting "+args[1]+" ...")

        if args[1] == "cmd":
            cmd = ' '.join(args[2:])
            subprocess.Popen(cmd, shell=True)

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
            call = subprocess.getstatusoutput(
                "sudo su -c 'echo "+lb_state+" > /sys/class/leds/qc71_laptop\:\:lightbar/brightness'")
            print("Exit: "+str(call[0]))  # Apply state

        elif args[1] == "lb_rainbow":
            lb_rainbow = config.get('CONFIGURATION', 'lb_rainbow')
            print("Aplicando rainbow "+lb_rainbow)
            call = subprocess.getstatusoutput(
                "sudo su -c 'echo "+lb_rainbow+" > /sys/class/leds/qc71_laptop\:\:lightbar/rainbow_mode'")
            print("Exit: "+str(call[0]))  # Apply rainbow

        elif args[1] == "lb_color":
            lb_color = config.get('CONFIGURATION', 'lb_color')
            print("Aplicando color "+lb_color)
            call = subprocess.getstatusoutput(
                "sudo su -c 'echo "+lb_color+" > /sys/class/leds/qc71_laptop\:\:lightbar/color'")
            print("Exit: "+str(call[0]))  # Apply color

        elif args[1] == "pre":
            print('Suspending ...')
            os.system("sudo ite8291r3-ctl off")  # Turn off keyboard
            call = subprocess.getstatusoutput(
                "sudo su -c 'echo 0 > /sys/class/leds/qc71_laptop\:\:lightbar/brightness'")
            print(str(call))  # Apply

            # We change our variable: config.set(section, variable, value)
            config.set('CONFIGURATION', "suspension", "")

            # Writing our configuration file
            with open(CONFIG_FILE, 'w') as configfile:
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
                if state == "on":
                    print(state)
                    os.system(effect)
                    call = subprocess.getstatusoutput(effect)
                    print("Exit: "+str(call))  # Apply state

                    call = subprocess.getstatusoutput(
                        "sudo ite8291r3-ctl brightness "+brightness)
                    print("Exit: "+str(call))  # Apply state

                else:
                    os.system("sudo ite8291r3-ctl off")

                # We apply the lightbar config
                if lb_state == "1":
                    print("Aplicando cambios lightbar")

                    print("Aplicando color "+lb_state)
                    call = subprocess.getstatusoutput(
                        "sudo su -c 'echo "+lb_state+" > /sys/class/leds/qc71_laptop\:\:lightbar/brightness'")

                    print("Exit: "+str(call))  # Apply state

                    print("Aplicando rainbow "+lb_rainbow)
                    call = subprocess.getstatusoutput(
                        "sudo su -c 'echo "+lb_rainbow+" > /sys/class/leds/qc71_laptop\:\:lightbar/rainbow_mode'")

                    print("Exit: "+str(call))  # Apply state

                    print("Aplicando color "+lb_color)
                    call = subprocess.getstatusoutput(
                        "sudo su -c 'echo "+lb_color+" > /sys/class/leds/qc71_laptop\:\:lightbar/color'")

                    print("Exit: "+str(call))  # Apply state

                else:
                    # Turn off light bar
                    os.system(
                        "echo 0 > /sys/class/leds/qc71_laptop\:\:lightbar/brightness")

    elif config.get('CONFIGURATION', 'state'):

        state = config.get('CONFIGURATION', 'state')
        effect = config.get('CONFIGURATION', 'effect')
        brightness = config.get('CONFIGURATION', 'brightness')
        suspension = config.get('CONFIGURATION', 'suspension')

        lb_state = config.get('CONFIGURATION', 'lb_state')
        lb_rainbow = config.get('CONFIGURATION', 'lb_rainbow')
        lb_color = config.get('CONFIGURATION', 'lb_color')

        # We apply the keyboard config
        if state == "on":
            print(state)
            os.system(effect)
            call = subprocess.getstatusoutput(effect)
            print("Exit: "+str(call))  # Apply state

            call = subprocess.getstatusoutput(
                "sudo ite8291r3-ctl brightness "+brightness)
            print("Exit: "+str(call))  # Apply state

        else:
            os.system("sudo ite8291r3-ctl off")

        # We apply the lightbar config
        if lb_state == "1":
            print("Aplicando cambios lightbar")

            print("Aplicando color "+lb_state)
            call = subprocess.getstatusoutput(
                "sudo su -c 'echo "+lb_state+" > /sys/class/leds/qc71_laptop\:\:lightbar/brightness'")

            print("Exit: "+str(call))  # Apply state

            print("Aplicando rainbow "+lb_rainbow)
            call = subprocess.getstatusoutput(
                "sudo su -c 'echo "+lb_rainbow+" > /sys/class/leds/qc71_laptop\:\:lightbar/rainbow_mode'")

            print("Exit: "+str(call))  # Apply state

            print("Aplicando color "+lb_color)
            call = subprocess.getstatusoutput(
                "sudo su -c 'echo "+lb_color+" > /sys/class/leds/qc71_laptop\:\:lightbar/color'")

            print("Exit: "+str(call))  # Apply state

        else:
            # Turn off light bar
            os.system(
                "echo 0 > /sys/class/leds/qc71_laptop\:\:lightbar/brightness")


def check_config():

    if not os.path.isfile(CONFIG_FILE):
        print("File doesn't exist")
        if os.path.exists(HOMEDIR+'/.config/slimbookrgbkeyboard'):
            print('Directory already exists')
            os.system('sudo -u '+USER_NAME+' touch '+CONFIG_FILE)
            print('Creating file')

            with open(HOMEDIR + '/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf', 'w') as conf:
                fichero_conf().write(conf)

            print('File created succesfully!\n')

            print(os.system("cat " + HOMEDIR +
                  "/.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf"))
        else:
            print("Directory doesen't exist")
            os.system('mkdir '+HOMEDIR+'/.config/slimbookrgbkeyboard')
            os.system('touch '+CONFIG_FILE)
            print('Creating file')

            with open(CONFIG_FILE, 'w') as conf:
                fichero_conf().write(conf)

            print('File created succesfully!\n')

            print(os.system("cat " + CONFIG_FILE))
    
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
    # Se obtiene las variables que se le pasa desde el archivo /usr/share/slimbookface/slimbookface
    main(sys.argv)
