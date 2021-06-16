#!/bin/bash

cd /tmp/

sudo apt install gcc make build-essential git linux-headers-$(uname -r) -y

git clone https://github.com/slimbook/keyboard.git

cd keyboard/backlight/essential/rgb-module/module/

make && sudo make install

sudo insmod clevo-xsm-wmi.ko

sudo install -m644 clevo-xsm-wmi.ko /lib/modules/$(uname -r)/extra

sudo depmod

sudo tee /etc/modules-load.d/clevo-xsm-wmi.conf <<< clevo-xsm-wmi

tee /etc/modprobe.d/clevo-xsm-wmi.conf <<< 'options clevo-xsm-wmi kb_color=white,white,white, kb_brightness=10'

tee -a /etc/modprobe.d/clevo-xsm-wmi.conf <<< '#last_color=white'


sudo update-initramfs -uk all
