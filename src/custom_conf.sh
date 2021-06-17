#!/bin/bash

tee /etc/modprobe.d/clevo-xsm-wmi.conf <<< 'options clevo-xsm-wmi kb_color=white,white,white, kb_brightness=10'

tee -a /etc/modprobe.d/clevo-xsm-wmi.conf <<< '#last_color=white'
