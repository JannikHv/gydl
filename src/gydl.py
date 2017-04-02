#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from subprocess import call as subcall

class ErrorGui(Gtk.Window):

    def getInterface(self):
        btn  = Gtk.Button(label="Continue")
        text = Gtk.Label ("")
        fix  = Gtk.Fixed ()

        btn .set_size_request(350, 50)
        text.set_size_request(350, 50)

        btn.connect("clicked", Gtk.main_quit, None)
        text.set_markup("<b>Internet Connection Error</b>")
        fix.put(btn,  0, 50)
        fix.put(text, 0, 0)

        return fix

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(350, 100)
        self.set_resizable   (False)
        self.set_title("Gydl - Connection Error")
        self.set_icon_name("Youtube-youtube.com")
        self.add(self.getInterface())

class DlTrueGui(Gtk.Window):

    def getInterface(self):
        btn  = Gtk.Button(label="Continue")
        text = Gtk.Label ("")
        fix  = Gtk.Fixed()

        btn .set_size_request(350, 50)
        text.set_size_request(350, 50)

        btn.connect("clicked", Gtk.main_quit)
        text.set_markup("<b>Download finished successfully</b>")
        fix.put(btn,  0, 50)
        fix.put(text, 0, 0)

        return fix

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(350, 100)
        self.set_resizable   (False)
        self.set_title("Gydl - Download Successful")
        self.set_icon_name("Youtube-youtube.com")
        self.add(self.getInterface())

class DlFalseGui(Gtk.Window):

    def getInterface(self):
        btn  = Gtk.Button(label="Continue")
        text = Gtk.Label ("")
        fix  = Gtk.Fixed()

        btn .set_size_request(350, 50)
        text.set_size_request(350, 50)

        btn.connect("clicked", Gtk.main_quit)
        text.set_markup("<b>Download finished unsuccessfully</b>")
        fix.put(btn,  0, 50)
        fix.put(text, 0, 0)

        return fix

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(350, 100)
        self.set_resizable   (False)
        self.set_title("Gydl - Download Unsuccessful")
        self.set_icon_name("Youtube-youtube.com")
        self.add(self.getInterface())

class GydlGui(Gtk.Window):

    def downloadMain(self, cmd):
        print(cmd)
        status = subcall(cmd, shell=True)

        if status == 0:
            Exec = DlTrueGui()
            Exec.connect("delete-event", Gtk.main_quit)
            Exec.show_all()
        else:
            Exec = DlFalseGui()
            Exec.connect("delete-event", Gtk.main_quit)
            Exec.show_all()

    def prepareVideo(self):
        cmd = "youtube-dl -f FFF -f bestvideo[height=QQQ] \"UUU\" -o \"~/%(title)s.%(ext)s\""

        cmd = cmd.replace("FFF", self.vFormat.get_active_text())
        cmd = cmd.replace("QQQ", self.vQuality.get_active_text().replace("p", ""))
        cmd = cmd.replace("UUU", self.vEntry.get_text())

        self.downloadMain(cmd)

    def prepareAudio(self):

        cmd = "youtube-dl -x --audio-format FFF --audio-quality QQQ \"UUU\" -o \"~/%(title)s.%(ext)s\""

        cmd = cmd.replace("FFF", self.aFormat.get_active_text())
        cmd = cmd.replace("QQQ", self.aQuality.get_active_text()[0])
        cmd = cmd.replace("UUU", self.aEntry.get_text())

        self.downloadMain(cmd)

    def prepareDownload(self, widget):

        self.hide()
        Gdk.flush()

        status = subcall("ping -c 1 google.com", shell=True)

        if status != 0:
            self.destroy()
            Exec = ErrorGui()
            Exec.connect("delete-event", Gtk.main_quit)
            Exec.show_all()

        if self.stack.get_visible_child_name() == 'A':
            self.prepareAudio()
        else:
            self.prepareVideo()

    def buildVideoStack(self):
        self.vEntry   = Gtk.Entry()
        self.vQuality = Gtk.ComboBoxText()
        self.vFormat  = Gtk.ComboBoxText()
        eLabel        = Gtk.Label("")
        fLabel        = Gtk.Label("")
        qLabel        = Gtk.Label("")
        fix           = Gtk.Fixed()

        self.vEntry.set_placeholder_text("https://youtube.com/watch...")

        eLabel.set_markup("<b>Enter the URL</b>")
        fLabel.set_markup("<b>Format </b>"      )
        qLabel.set_markup("<b>Quality</b>"      )

        # Build the format combobox
        for i in ["3gp", "flv", "mp4", "webm"]:
            self.vFormat.append_text(i)

        # Build the quality combobox
        for i in ["2160p", "1440p", "1080p", "720p",
                  "480p",  "360p",  "240p",  "144p"]:
            self.vQuality.append_text(i)

        # Size the widgets
        self.vEntry  .set_size_request(500, 30)
        self.vQuality.set_size_request(250, 30)
        self.vFormat .set_size_request(250, 30)
        eLabel       .set_size_request(500, 30)
        fLabel       .set_size_request(250, 30)
        qLabel       .set_size_request(250, 30)

        # Add the widgets to the environment
        fix.put(self.vEntry,   0,   35 )
        fix.put(self.vFormat,  0,   125)
        fix.put(self.vQuality, 250, 125)
        fix.put(eLabel,        0,   0  )
        fix.put(fLabel,        0,   90 )
        fix.put(qLabel,        250, 90 )

        self.vFormat .set_active(2)
        self.vQuality.set_active(3)

        self.stack.add_titled(fix, "V", "Video")

    def buildAudioStack(self):
        self.aEntry   = Gtk.Entry()
        self.aQuality = Gtk.ComboBoxText()
        self.aFormat  = Gtk.ComboBoxText()
        eLabel        = Gtk.Label("")
        fLabel        = Gtk.Label("")
        qLabel        = Gtk.Label("")
        fix           = Gtk.Fixed()

        self.aEntry.set_placeholder_text("https://youtube.com/watch...")

        eLabel.set_markup("<b>Enter the URL</b>")
        fLabel.set_markup("<b>Format </b>"      )
        qLabel.set_markup("<b>Quality</b>"      )

        # Build the format combobox
        for i in ["aac", "m4a", "mp3", "ogg", "wav"]:
            self.aFormat.append_text(i)

        # Build the quality combobox
        self.aQuality.append_text("0 (Best)")
        for i in range(1,9):
            self.aQuality.append_text(str(i))

        self.aQuality.append_text("9 (Worst)")

        # Size the widgets
        self.aEntry  .set_size_request(500, 30)
        self.aQuality.set_size_request(250, 30)
        self.aFormat .set_size_request(250, 30)
        eLabel       .set_size_request(500, 30)
        fLabel       .set_size_request(250, 30)
        qLabel       .set_size_request(250, 30)

        # Add the widgets to the environment
        fix.put(self.aEntry,   0,   35 )
        fix.put(self.aFormat,  0,   125)
        fix.put(self.aQuality, 250, 125)
        fix.put(eLabel,        0,   0  )
        fix.put(fLabel,        0,   90 )
        fix.put(qLabel,        250, 90 )

        self.aFormat .set_active(2)
        self.aQuality.set_active(5)

        self.stack.add_titled(fix, "A", "Audio")

    def getHeaderBar(self):
        self.switcher = Gtk.StackSwitcher()
        hbar          = Gtk.HeaderBar()
        btn_dl        = Gtk.Button(label="Download ")

        btn_dl.connect("clicked", self.prepareDownload)
        btn_dl.set_always_show_image(True)
        btn_dl.set_image_position(Gtk.PositionType.RIGHT)
        btn_dl.set_image(Gtk.Image.new_from_icon_name(
                         "folder-download-symbolic",
                         Gtk.IconSize.BUTTON))

        hbar.pack_end        (btn_dl)
        hbar.set_custom_title(self.switcher)
        hbar.set_show_close_button(True)

        return hbar

    def __init__(self):

        # Configuring the window
        Gtk.Window.__init__(self)
        self.connect         ("delete-event", Gtk.main_quit)
        self.set_default_size(500, 250)
        self.set_resizable   (False)
        self.set_border_width(10)
        self.set_title       ("Graphical Youtube-dl")
        self.set_titlebar    (self.getHeaderBar())
        self.set_icon_name("Youtube-youtube.com")

        self.stack = Gtk.Stack()
        self.buildAudioStack()
        self.buildVideoStack()
        self.switcher.set_stack(self.stack)
        self.add(self.stack)

Win = GydlGui()
Win.show_all()
Gtk.main()
