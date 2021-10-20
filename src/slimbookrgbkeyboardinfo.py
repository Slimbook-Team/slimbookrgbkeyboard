#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import gi
import utils

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, GdkPixbuf     
from os.path import expanduser   

# AÑADIR CLASE --> .get_style_context().add_class("button-none")

#IDIOMAS ----------------------------------------------------------------

# pygettext -d slimbookamdcontrollercopy slimbookamdcontrollercopy.py
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

_ = utils.load_translation('slimbookrgbkeyboardinfo')


user = expanduser("~")
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

style_provider = Gtk.CssProvider()
style_provider.load_from_path(CURRENT_PATH+'/style.css')

Gtk.StyleContext.add_provider_for_screen (
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

class PreferencesDialog(Gtk.Dialog):
	
    def __init__(self):
		
        Gtk.Dialog.__init__(self,
			title='',
            parent=None,
            flags=0)

        self.set_icon_from_file("{}/images/icono.png".format(CURRENT_PATH))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)     
        self.get_style_context().add_class("bg-color")
        self.set_default_size(900, 600)     
        self.set_decorated(False)

        vbox = Gtk.VBox(spacing=5)
        vbox.set_border_width(40)

        self.get_content_area().add(vbox)

        # Icono APP
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename= CURRENT_PATH+'/images/logo-sb.png',
			width=200,
			height=100,
			preserve_aspect_ratio=True)
        iconApp = Gtk.Image.new_from_pixbuf(pixbuf)
        iconApp.set_name('top')


        info = Gtk.Label()
        info.set_markup("<span>{}</span>".format(
            _('The Slimbook RGB Keyboard app enables full customization of your built-in keyboard backlight color, brightness and visual effects.\n\nThanks to pobrn.')
        ))
        info.set_name('info')
        info.set_line_wrap(True)
        
         # Hya que meter el link de patreon.com/slimbook

        info2 = Gtk.Label()
        info2.set_markup("<span>{}</span>".format(
            _("If you want to support the Slimbook team with the development of this app and several more to come, you can do so by joining our <b><a href='https://patreon.com/slimbook'>patreon</a></b> or buying a brand new Slimbook.")
        ))
        info2.set_name('info')
        info2.set_line_wrap(True)

        enlaces_box = Gtk.Box(spacing=5)
        enlaces_box.set_name('center')
        enlaces_box.set_halign(Gtk.Align.CENTER)

        info3 = Gtk.Label(label=_('This software is provided * as is * without warranty of any kind..'))

        license1 = Gtk.Label()
        license1.set_markup("<span><b>"+_("You are free from:")+"</b></span>")


        license2 = Gtk.Label()
        license2.set_markup("<span><b><small>"+_("Share: ")+"</small></b><small>"+_("copy and redistribute the material in any medium or format\nSlimbook Copyright - License Creative Commons BY-NC-ND")+"</small></span>")


        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=CURRENT_PATH+'/images/cc.png',
			width=100,
			height=50,
			preserve_aspect_ratio=True)

        licencia = Gtk.Image.new_from_pixbuf(pixbuf)

       

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=CURRENT_PATH+'/images/cross.png',
			width=20,
			height=20,
			preserve_aspect_ratio=True)

        close = Gtk.Image.new_from_pixbuf(pixbuf)
        close.set_halign(Gtk.Align.END)

        evnt_close = Gtk.EventBox()
        evnt_close.add(close)
        evnt_close.connect("button_press_event", self.on_button_close)

    # REDES SOCIALES --------------------------------------------------------------
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=CURRENT_PATH+'/images/twitter.png',
			width=25,
			height=25,
			preserve_aspect_ratio=True)

        itwitter = Gtk.Image.new_from_pixbuf(pixbuf)
        enlaces_box.pack_start(itwitter, False, False, 0)

        twitter = Gtk.Label()
        twitter.set_markup("<span><b><a href='https://twitter.com/SlimbookEs'>@SlimbookEs</a></b>    </span>")
        twitter.set_justify(Gtk.Justification.CENTER)
        
        enlaces_box.pack_start(twitter, False, False, 0)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=CURRENT_PATH+'/images/facebook.png',
			width=25,
			height=25,
			preserve_aspect_ratio=True)

        ifacebook = Gtk.Image.new_from_pixbuf(pixbuf)
        enlaces_box.pack_start(ifacebook, False, False, 0)

        facebook = Gtk.Label()
        facebook.set_markup("<span><b><a href='https://www.facebook.com/slimbook.es'>Slimbook</a></b>    </span>")
        facebook.set_justify(Gtk.Justification.CENTER)
        enlaces_box.pack_start(facebook, False, False, 0)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=CURRENT_PATH+'/images/insta.png',
			width=25,
			height=25,
			preserve_aspect_ratio=True)

        iinstagram = Gtk.Image.new_from_pixbuf(pixbuf)
        enlaces_box.pack_start(iinstagram, False, False, 0)

        instagram = Gtk.Label()
        instagram.set_markup("<span><b><a href='https://www.instagram.com/slimbookes'>@Slimbook</a></b></span>")
        instagram.set_justify(Gtk.Justification.CENTER)
        enlaces_box.pack_start(instagram, False, False, 0)

    # Enlaces --------------------------------------------------------------------------
        web_link=''
        idiomas = utils.get_languages()[0]
        if idiomas.find('es') >= 0:
            web_link = 'https://slimbook.es/es/'
        else:
            web_link = 'https://slimbook.es/en/'

        box = Gtk.HBox()
        box.set_halign(Gtk.Align.CENTER)
        web = Gtk.Label()
        web.set_markup("<span><b><a href='"+web_link+"'>"+_("@Visit Slimbook web")+"</a></b>    </span>")
        web.set_justify(Gtk.Justification.CENTER)
        box.add(web)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=os.path.join(CURRENT_PATH+ '/images/GitHub_Logo_White.png'),
            width=150,
            height=30,
            preserve_aspect_ratio=True)

        icon = Gtk.Image()
        icon.set_from_pixbuf(pixbuf)
        github = Gtk.LinkButton(uri="https://github.com/slimbook/slimbookrgbkeyboard")
        github.set_name('link')
        github.set_halign(Gtk.Align.CENTER)
        github.set_image(icon)
        box.add(github)

        link = Gtk.LinkButton(uri="https://github.com/slimbook/slimbookrgbkeyboard/tree/main/src/translations",
                              label=(_('Help us with translations!')))
        link.set_name('link')
        link.set_halign(Gtk.Align.CENTER)
        box.add(link)

        #TUTORIAL
        email = Gtk.Label()
        email.set_markup("<span><b>"+_("Send an e-mail a: ")+"dev@slimbook.es</b></span>")
        email.set_justify(Gtk.Justification.CENTER)
        email.set_name('label')

    
    # PACKKING ----------------------------------------------------------------------

        vbox.pack_start(evnt_close,True, True, 0)
        vbox.pack_start(iconApp,True, True,20)

        vbox.pack_start(info,True, True,10)
        vbox.pack_start(info2,True, True,10)
        
        vbox.pack_start(enlaces_box, True, True, 5)
        vbox.pack_start(box, True, True, 10)
        vbox.pack_start(email, True, True, 10)
        vbox.pack_start(info3, True, True, 10)

        vbox.pack_start(license1, True, True, 0)
        vbox.pack_start(license2, True, True, 0)
        vbox.pack_start(licencia, True, True, 10)
        
        #SHOW
        self.show_all()
    
    def on_buttonCopyEmail_clicked(self, buttonCopyEmail):
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.clipboard.set_text('dev@slimbook.es', -1)
        os.system("notify-send 'Slimbook AMD Controller' "+_("'The email has been copied to the clipboard'") + " -i '" + CURRENT_PATH + "/images/icono.png'")

    def on_button_close(self, button, state):
        self.close()
        self.hide()
        self.destroy()




