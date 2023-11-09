#!/usr/bin/python3
# -*- coding: utf-8 -*-

import slimbook
import slimbook.info

import gi
import utils
import os, subprocess
import shutil


gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from os.path import expanduser
from gi.repository import Gdk, Gtk, GdkPixbuf

USER_NAME = utils.get_user()

HOMEDIR = expanduser("~{}".format(USER_NAME))

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

CONFIG_FILE = os.path.join(
    HOMEDIR, '.config/slimbookrgbkeyboard/slimbookrgbkeyboard.conf')

AUTOSTART_FILE = os.path.join(
    HOMEDIR, ".config/autostart/slimbookrgbkeyboard-autostart.desktop")


_ = utils.load_translation('slimbookrgb')

# CSS
style_provider = Gtk.CssProvider()
style_provider.load_from_path(CURRENT_PATH+'/style.css')

Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(
), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class SlimbookRGBKeyboard(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Slimbook RGB Keyboard")

        self.set_icon_from_file(os.path.join(
            CURRENT_PATH, "images/icono.png"))

        self.set_size_request(900, 400)

        self.set_resizable(False)

        self.set_position(Gtk.WindowPosition.CENTER)

        self.get_style_context().add_class("bg-image")

        win_grid = Gtk.Grid(column_homogeneous=True,
                            row_homogeneous=True,
                            column_spacing=20,
                            row_spacing=0) 

        self.add(win_grid)

        self.load_main_grid(win_grid)

    def load_main_grid(self, win_grid):

        logo_box = Gtk.HBox()
        logo_box.set_hexpand(True)
        logo_box.set_vexpand(True)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=CURRENT_PATH+'/images/logo.png',
            width=400,
            height=100,
            preserve_aspect_ratio=True)

        logo = Gtk.Image.new_from_pixbuf(pixbuf)
        logo.get_style_context().add_class("logo")
        logo.set_halign(Gtk.Align.START)
        logo_box.pack_start(logo, True, True, 0)

        win_grid.attach(logo_box, 0, 0, 7, 1)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=CURRENT_PATH+'/images/icono.png',
            width=200,
            height=200,
            preserve_aspect_ratio=True)

        icon = Gtk.Image.new_from_pixbuf(pixbuf)

        icon.set_halign(Gtk.Align.CENTER)

        win_grid.attach(icon, 5, 1, 2, 5)
        
        self.model = slimbook.info.get_model()
        
        if (self.model & slimbook.info.SLB_MODEL_TITAN) > 0:
            print("Slimbook TITAN detected")
            import ite8291r3_ctl
            win_grid.attach(ite8291r3_ctl.Grid(), 0, 1, 5, 5)
            self.check_autostart()
        
        if (self.model == slimbook.info.SLB_MODEL_HERO_RPL_RTX):
            print("Slimbook HERO detected")
            import hero_backlight
            win_grid.attach(hero_backlight.Grid(), 0, 1, 5, 5)
        
        if (self.model & slimbook.info.SLB_MODEL_ESSENTIAL) > 0 or self.model == slimbook.info.SLB_MODEL_HERO_S_TGL_RTX or self.model == slimbook.info.SLB_MODEL_ELEMENTAL_15_I12:
            print("Slimbook Essential/Elemental/Hero-S detected")
            import clevo_platform
            win_grid.attach(clevo_platform.Grid(), 0, 1, 5, 5)
        
        if (self.model & slimbook.info.SLB_MODEL_PROX) > 0:
            print("Slimbook ProX detected")
            print("No backlight support")

    # Info
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=CURRENT_PATH+'/images/question.png',
            width=30,
            height=30,
            preserve_aspect_ratio=True)

        iconApp = Gtk.Image.new_from_pixbuf(pixbuf)
        iconApp.get_style_context().add_class("help")
        iconApp.set_halign(Gtk.Align.END)

        lbl_info = Gtk.Label(label="Info  ")

        info_box = Gtk.Box()
        info_box.pack_start(lbl_info, True, True, 0)
        info_box.pack_start(iconApp, True, True, 0)
        info_box.set_name("info")

        evnt_box = Gtk.EventBox(valign=Gtk.Align.END, halign=Gtk.Align.END)
        evnt_box.add(info_box)
        evnt_box.connect("button_press_event", self.about_us)

        win_grid.attach(evnt_box, 6, 5, 1, 1)

    def check_autostart(self):
        if not os.path.isfile(AUTOSTART_FILE):
            autostart_dir = os.path.join(HOMEDIR,'.config/autostart')
            if not os.path.exists(autostart_dir):
                print("Directory doesen't exist")
                os.mkdir(autostart_dir)
            autostart_file = os.path.join(
                CURRENT_PATH, 'slimbookrgbkeyboard-autostart.desktop')
            shutil.copy(autostart_file, AUTOSTART_FILE)

    def about_us(self, widget, x):
        
        if os.getlogin() == 'root':
            os.system('sudo -u {} {}'.format(USER_NAME, os.path.join(CURRENT_PATH, 'slimbookrgbkeyboardinfo.py')))
        else:
            import slimbookrgbkeyboardinfo
            dialog = slimbookrgbkeyboardinfo.PreferencesDialog(self)
            dialog.show_all()


def main():
    win = SlimbookRGBKeyboard()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
    
