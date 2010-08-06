#!/usr/bin/env python
"""This program is found at
http://pygstdocs.berlios.de/pygst-tutorial/playbin.html
it will be used as a possible base for a pomodoro implementation"""

import sys, os, time, thread
import glib, gobject
import pygst
pygst.require("0.10")
import gst

class CLI_Main:
    def __init__(self):
        self.player = gst.element_factory_make("playbin2", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.playmode = False
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.playmode = False

    def start(self):
        for filepath in sys.argv[1:]:
            if os.path.isfile(filepath):
                self.playmode = True
                self.player.set_property("uri", "file://" + filepath)
                self.player.set_state(gst.STATE_PLAYING)
                while self.playmode:
                    time.sleep(1)
        time.sleep(1)
        loop.quit()

mainclass = CLI_Main()
thread.start_new_thread(mainclass.start, ())
gobject.threads_init()
loop = glib.MainLoop()
loop.run()
