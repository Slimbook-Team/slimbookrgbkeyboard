#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import gi
import gettext, locale

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, GdkPixbuf     
from os.path import expanduser   


# AÑADIR CLASE --> .get_style_context().add_class("button-none")

#IDIOMAS ----------------------------------------------------------------

# pygettext -d slimbookamdcontrollercopy slimbookamdcontrollercopy.py
currpath = os.path.dirname(os.path.realpath(__file__))
entorno_usu = locale.getlocale()[0]
if entorno_usu.find("en") >= 0 or entorno_usu.find("es") >= 0:
	idiomas = [entorno_usu]
else: 
    idiomas = ['en_EN'] 

#entorno_usu="fr_FR"
#idiomas = ['fr_FR'] 

print('Language: ', entorno_usu)
t = gettext.translation('slimbookamdcontrollerinfo',
						currpath+'/locale',
						languages=idiomas,
						fallback=True,) 
_ = t.gettext


user = expanduser("~")
currpath = os.path.dirname(os.path.realpath(__file__))

style_provider = Gtk.CssProvider()
style_provider.load_from_path(currpath+'/style.css')

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

        #Botones de aceptar y cerrar
        #self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT)
        #self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)

        self.set_icon_from_file(currpath+"/images/icono.png")
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)     
        self.get_style_context().add_class("bg-color")
        self.set_default_size(900, 600)     
        self.set_decorated(False)

        vbox = Gtk.VBox(spacing=5)
        vbox.set_border_width(40)

        self.get_content_area().add(vbox)

        # Icono APP
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename= currpath+'/images/logo-sb.png',
			width=200,
			height=100,
			preserve_aspect_ratio=True)
        iconApp = Gtk.Image.new_from_pixbuf(pixbuf)
        iconApp.set_name('top')


        info = Gtk.Label()
        info.set_markup("<span>The Slimbook RGB Keyboard app enables full customization of your built-in keyboard backlight color, brightness and visual effects.\n\nThanks to pobrn.</span>")
        info.set_name('info')
        info.set_line_wrap(True)
        
         # Hya que meter el link de patreon.com/slimbook

        info2 = Gtk.Label()
        info2.set_markup("<span>If you want to support the Slimbook team with the development of this app and several more to come, you can do so by joining our <b><a href='https://patreon.com/slimbook'>patreon</a></b> or buying a brand new Slimbook.</span>")
        info2.set_name('info')
        info2.set_line_wrap(True)

        enlaces_box = Gtk.Box(spacing=5)
        enlaces_box.set_name('center')
        enlaces_box.set_halign(Gtk.Align.CENTER)

        salvavidas = Gtk.Label(label=_('This software is provided * as is * without warranty of any kind.'))

        license1 = Gtk.Label()
        license1.set_markup("<span><b>"+_("You are free from:")+"</b></span>")


        license2 = Gtk.Label()
        license2.set_markup("<span><b><small>"+_("Share: ")+"</small></b><small>"+_("copy and redistribute the material in any medium or format\nSlimbook Copyright - License Creative Commons BY-NC-ND")+"</small></span>")


        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=currpath+'/images/cc.png',
			width=100,
			height=50,
			preserve_aspect_ratio=True)

        licencia = Gtk.Image.new_from_pixbuf(pixbuf)

       

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=currpath+'/images/cross.png',
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
			filename=currpath+'/images/twitter.png',
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
			filename=currpath+'/images/facebook.png',
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
			filename=currpath+'/images/insta.png',
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
        #separador = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)

        #WEB
        web_link=''
        if entorno_usu.find('es') >= 0:
            web_link = 'https://slimbook.es/es/'
        else:
            web_link = 'https://slimbook.es/en/'

        web = Gtk.Label()
        web.set_markup("<span><b><a href='"+web_link+"'>"+_("@Visit Slimbook web")+"</a></b>    </span>")
        web.set_justify(Gtk.Justification.CENTER)

        #TUTORIAL
        email = Gtk.Label()
        email.set_markup("<span><b>"+_("Send an e-mail to: ")+"dev@slimbook.es</b></span>")
        email.set_justify(Gtk.Justification.CENTER)
        email.set_name('label')

    
    # PACKKING ----------------------------------------------------------------------

        vbox.pack_start(evnt_close,True, True, 0)
        vbox.pack_start(iconApp,True, True,20)
        #vbox.pack_start(separador, True, True, 5)

        vbox.pack_start(info,True, True,10)
        vbox.pack_start(info2,True, True,10)
        
        vbox.pack_start(enlaces_box, True, True, 5)
        vbox.pack_start(web, True, True, 10)
        vbox.pack_start(email, True, True, 10)
        vbox.pack_start(salvavidas, True, True, 10)

        vbox.pack_start(license1, True, True, 0)
        vbox.pack_start(license2, True, True, 0)
        vbox.pack_start(licencia, True, True, 10)
        
        #SHOW
        self.show_all()
    
    def on_buttonCopyEmail_clicked(self, buttonCopyEmail):
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.clipboard.set_text('dev@slimbook.es', -1)
        os.system("notify-send 'Slimbook AMD Controller' "+_("'The email has been copied to the clipboard'") + " -i '" + currpath + "/images/icono.png'")

    def on_button_close(self, button, state):
        self.close()
        self.hide()
        self.destroy()

dialog = PreferencesDialog()
dialog.connect("destroy", Gtk.main_quit)
dialog.show_all()
Gtk.main()



