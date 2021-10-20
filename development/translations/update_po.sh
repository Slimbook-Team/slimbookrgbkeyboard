#!/bin/bash
# This file must be executed inside src
# set -x

cd ./../../src
# 1. Generating .pot / .po

for programa in *.py
do
    
    eval cat $programa | grep '_ = '
    if [ $? -eq 0 ]; then
        echo $programa
        programa=$(echo $programa | cut -d'.' -f1)
        echo $programa
        pygettext3 -d $programa $programa.py
        if [ $? -eq 0 ]; then
            eval "mv $programa.pot ./translations/$programa.template.po"
            echo Done
        else
            echo 'Not done'
        fi
        echo
    fi
done