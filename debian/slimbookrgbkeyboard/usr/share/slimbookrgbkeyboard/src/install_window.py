#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk
from gi.repository import GLib

import os
from subprocess import Popen, PIPE
import fcntl


# Main Window -----------------------------------------------------------------------
currpath = os.path.dirname(os.path.realpath(__file__))

win = Gtk.Window()
win.set_default_size(1000, 400)
win.connect("destroy", Gtk.main_quit)
win.set_position(Gtk.WindowPosition.CENTER)
win.set_decorated(False)

label = Gtk.Label()
label.set_name("cmd_text")
label.set_name('labelw')

lbl_info = Gtk.Label(label="Estamos instalando un módulo necesario para SlimbookRGB.\n\nTen en cuenta que este proceso puede tardar un tiempo...")
lbl_info.set_line_wrap(True)
lbl_info.set_valign(Gtk.Align.START)
lbl_info.set_name('labelw')

lbl_info2 = Gtk.Label(label="Esta ventana se cerrará automáticamente. Gracias por esperar.")
lbl_info2.set_halign(Gtk.Align.END)
lbl_info2.set_name('labelw')

labl_terminal = Gtk.Label(label="Terminal")
labl_terminal.set_halign(Gtk.Align.CENTER)
labl_terminal.set_name('labelw')

scrolled_window = Gtk.ScrolledWindow()
scrolled_window.set_vexpand(True)
scrolled_window.add(label)
scrolled_window.set_name('terminal')

grid = Gtk.Grid(column_homogeneous=True,
                         row_homogeneous=False,
                         column_spacing=20,
                         row_spacing=10)

#grid.set_halign(Gtk.Align.CENTER)

grid.attach(lbl_info, 0, 1, 1, 3)
grid.attach(scrolled_window, 1, 1, 2, 1)
grid.attach(labl_terminal, 1, 0, 2, 1)
grid.attach(lbl_info2, 1, 3, 2, 1)

win.add(grid)
win.show_all()

sub_proc =  Popen("sudo bash "+currpath+"/install_rgb.sh", shell=True, stdin=None, stdout=PIPE, stderr=None)
sub_outp = ""



def non_block_read(output):
    ''' even in a thread, a normal read with block until the buffer is full '''
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    op = output.read()
    if op == None:
        return ''
    update_scroll()
    
    return op.decode('utf-8')

def update_terminal():
    label.set_text(label.get_text() + non_block_read(sub_proc.stdout))
    if not sub_proc.poll() is None:
        Gtk.main_quit()        
    return sub_proc.poll() is None

def update_scroll():
    adjustment = scrolled_window.get_vadjustment()
    adjustment.set_value( adjustment.get_upper() - adjustment.get_page_size() )
    


#CSS
style_provider = Gtk.CssProvider()
style_provider.load_from_path(currpath+'/style.css')

Gtk.StyleContext.add_provider_for_screen (
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
GLib.timeout_add(50, update_terminal)

Gtk.main()