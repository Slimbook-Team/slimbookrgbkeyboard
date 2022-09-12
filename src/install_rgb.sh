#!/bin/bash

sudo apt-add-repository ppa:slimbook/slimbook

sudo apt install slimbook-keyboard-dkms

# sudo tee /etc/modules-load.d/clevo_platform.conf <<< clevo_platform

tee /etc/modprobe.d/clevo_platform.conf <<< 'options clevo_platform color_left=0xFFFFFF color_center=0xFFFFFF color_right=0xFFFFFF brightness=200 state=on'
