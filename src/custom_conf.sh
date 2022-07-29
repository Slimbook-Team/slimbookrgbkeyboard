#!/bin/bash

tee /etc/modprobe.d/clevo_platform.conf <<< 'options clevo_platform color_left=0xFFFFFF color_left=0xFFFFFF color_left=0xFFFFFF kb_brightness=200'

tee -a /etc/modprobe.d/clevo_platform.conf <<< '#last_color=0xFFFFFF'
