#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Pango, GObject
from gi.repository import GLib

import os
from subprocess import Popen, PIPE
import fcntl


# Main Window -----------------------------------------------------------------------
currpath = os.path.dirname(os.path.realpath(__file__))

wnd = Gtk.Window()
wnd.set_default_size(400, 400)
wnd.set_position(Gtk.WindowPosition.CENTER)
wnd.connect("destroy", Gtk.main_quit)
textview = Gtk.TextView(margin=10)
scroll = Gtk.ScrolledWindow()
scroll.add(textview)

# box = Gtk.Box(spacing=50)
# box.set_hexpand(True)
# box.add(scroll)
# wnd.add(box)

wnd.add(scroll)

file=os.path.join(currpath, "install_rgb.sh")

wnd.show_all()
sub_proc = Popen("bash "+file, stdout=PIPE, shell=True)
sub_outp = ""


def non_block_read(output):
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read().decode("utf-8")
    except:
        return ''


def update_terminal():
    textview.get_buffer().insert_at_cursor(non_block_read(sub_proc.stdout))
    return sub_proc.poll() is None

GLib.timeout_add(100, update_terminal)
Gtk.main()
