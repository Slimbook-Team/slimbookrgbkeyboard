#!/bin/bash

sudo apt install gcc make build-essential git linux-headers-$(uname -r) -y

cd /usr/share/slimbookrgbkeyboard

sudo apt install ./clevo-platform-dkms_0.0_amd64.deb

# sudo tee /etc/modules-load.d/clevo_platform.conf <<< clevo_platform

tee /etc/modprobe.d/clevo_platform.conf <<< 'options clevo_platform color_left=0xFFFFFF color_center=0xFFFFFF color_right=0xFFFFFF kb_brightness=200'

tee -a /etc/modprobe.d/clevo_platform.conf <<< '#last_color=0xFFFFFF'


sudo update-initramfs -uk all
