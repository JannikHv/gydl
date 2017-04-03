#!/usr/bin/env python3

__author__     = "Jannik Hauptvogel"
__credits__    = "rg3"
__license__    = "MIT"
__maintainer__ = "Jannik Hauptvogel"

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from subprocess    import call as subcall
from os            import getenv

class GydlMessageGui(Gtk.Window):

    def getLayout(self, errMessage):
        label = Gtk.Label(errMessage)
        return label

    def getHeaderBar(self, errTitle):

        # Configuration of the headerbar
        hbar  = Gtk.HeaderBar()
        label = Gtk.Label(errTitle)
        btn   = Gtk.Button(label="Continue")
        btn.connect("clicked", Gtk.main_quit)

        hbar.set_custom_title(label)
        hbar.pack_end(btn)
        hbar.set_show_close_button(False)

        return hbar

    def __init__(self, errTitle, errMessage):

        # Configure the window
        Gtk.Window.__init__  (self)
        self.set_default_size(375, 100)
        self.set_resizable   (False)
        self.set_border_width(10)
        self.set_icon_name   ("Youtube-youtube.com")
        self.set_titlebar    (self.getHeaderBar(errTitle))
        self.set_position    (Gtk.WindowPosition.CENTER)

        self.add(self.getLayout(errMessage))
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

class GydlMainGui(Gtk.Window):

    def setDownloadMain(self, Cmd, Type):
        status = subcall(Cmd, shell=True)

        if status == 0:
            title   = ("Your download was successful")
            message = ("Your " + Type + " has been downloaded successfully.\n" +
                     "The file has been stored in " + getenv("HOME") + "/ .\n" +
                     "Please press on continue to exit this program.")

            GydlMessageGui(title, message)

        else:
            title   = ("Your download was unsuccessful")
            message = ("Your " + Type + " has not been downloaded.\n" + 
                       "Please press on continue to exit this program.")

            GydlMessageGui(title, message)

    def setDownloadVideo(self):

        # Prepare the command
        cmd = ("youtube-dl --no-playlist -f FFF -f bestvideo[height=QQQ] " +
               "-o \"~/%(title)s.%(ext)s\" \"UUU\"")

        cmd = cmd.replace("FFF", self.vFormat.get_active_text())
        cmd = cmd.replace("QQQ", self.vQuality.get_active_text().replace("p", ""))
        cmd = cmd.replace("UUU", self.vEntry.get_text())

        self.setDownloadMain(cmd, "video")

    def setDownloadAudio(self):

        # Prepare the command
        cmd = ("youtube-dl --no-playlist -x --audio-format FFF " +
               "--audio-quality QQQ -o \"~/%(title)s.%(ext)s\" \"UUU\"")

        if self.aFormat.get_active_text() == "ogg":
            cmd = cmd.replace("FFF", "vorbis")
        else:
            cmd = cmd.replace("FFF", self.aFormat.get_active_text())

        cmd = cmd.replace("QQQ", self.aQuality.get_active_text()[0])
        cmd = cmd.replace("UUU", self.aEntry.get_text())

        self.setDownloadMain(cmd, "audio")

    def setDownloadPrepare(self, widget):

        # Hide the main window
        self.hide()
        Gdk.flush()

        # Check if internet connection is present
        status = subcall("ping -c 1 google.com", shell=True)
        if status != 0:
            GydlMessageGui("Connection Error", "No internet connection has been established.\n" +
                                               "Please press on continue to exit this program.")
        else:
            # Find out if Video or Audio is selected
            if self.stack.get_visible_child_name() == "A":
                self.setDownloadAudio()
            else:
                self.setDownloadVideo()

    def getVideoArea(self):

        # Create basic widgets
        self.vEntry    = Gtk.Entry()
        self.vFormat   = Gtk.ComboBoxText()
        self.vQuality  = Gtk.ComboBoxText()
        eLabel         = Gtk.Label()
        fLabel         = Gtk.Label()
        qLabel         = Gtk.Label()
        fix            = Gtk.Fixed()

        # Add entries to comboboxes
        for i in ["3gp", "flv", "mp4", "webm"]:
            self.vFormat.append_text(i)

        for i in ["2160p", "1440p", "1080p", "720p",
                  "480p",  "360p",  "240p",  "144p"]:
            self.vQuality.append_text(i)

        self.vFormat .set_active(2)
        self.vQuality.set_active(3)

        # Add text to widgets
        eLabel.set_markup("<big>Enter the URL</big>" )
        fLabel.set_markup("<big><u>Format</u></big>" )
        qLabel.set_markup("<big><u>Quality</u></big>")

        # Sizing the widgets
        self.vEntry   .set_size_request(500, 30)
        self.vFormat  .set_size_request(250, 30)
        self.vQuality .set_size_request(250, 30)
        eLabel        .set_size_request(500, 30)
        fLabel        .set_size_request(250, 30)
        qLabel        .set_size_request(250, 30)

        # Add the widgets to the interface
        fix.put(self.vEntry,    0,   50 )
        fix.put(self.vFormat,   0,   140)
        fix.put(self.vQuality,  250, 140)
        fix.put(eLabel,         0,   10 )
        fix.put(fLabel,         0,   105)
        fix.put(qLabel,         250, 105)

        return fix

    def getAudioArea(self):

        # Create basic widgets
        self.aEntry    = Gtk.Entry()
        self.aFormat   = Gtk.ComboBoxText()
        self.aQuality  = Gtk.ComboBoxText()
        eLabel         = Gtk.Label()
        fLabel         = Gtk.Label()
        qLabel         = Gtk.Label()
        fix            = Gtk.Fixed()

        # Add entries to comboboxes
        for i in ["aac", "m4a", "mp3", "ogg", "wav"]:
            self.aFormat.append_text(i)

        self.aQuality.append_text("0 (Best)")

        for i in range(1,9):
            self.aQuality.append_text(str(i))

        self.aQuality.append_text("9 (Worst)")

        self.aFormat .set_active(2)
        self.aQuality.set_active(5)

        # Add text to widgets
        eLabel.set_markup("<big>Enter the URL</big>" )
        fLabel.set_markup("<big><u>Format</u></big>" )
        qLabel.set_markup("<big><u>Quality</u></big>")

        # Size the widgets
        self.aEntry  .set_size_request(500, 30)
        self.aFormat .set_size_request(250, 30)
        self.aQuality.set_size_request(250, 30)
        eLabel       .set_size_request(500, 30)
        fLabel       .set_size_request(250, 30)
        qLabel       .set_size_request(250, 30)

        # Add the widgets to the interface
        fix.put(self.aEntry,    0,   50 )
        fix.put(self.aFormat,   0,   140)
        fix.put(self.aQuality,  250, 140)
        fix.put(eLabel,         0,   10 )
        fix.put(fLabel,         0,   105)
        fix.put(qLabel,         250, 105)

        return fix

    def getHeaderBar(self, switch):

        # Create download button
        bDownload = Gtk.Button(label=" Download")
        bDownload.connect("clicked", self.setDownloadPrepare)
        bDownload.set_always_show_image(True)
        bDownload.set_image_position(Gtk.PositionType.RIGHT)
        bDownload.set_image(Gtk.Image.new_from_icon_name(
                            "folder-download-symbolic",
                            Gtk.IconSize.BUTTON))

        # Configuration of the headerbar
        hbar = Gtk.HeaderBar()
        hbar.set_show_close_button(True)
        hbar.set_custom_title(switch)
        hbar.pack_end(bDownload)

        return hbar

    def __init__(self):

        # Declare main variables
        switch = Gtk.StackSwitcher()
        self.stack  = Gtk.Stack()

        # Configuring the window
        Gtk.Window.__init__  (self)
        self.set_default_size(500, 250)
        self.set_resizable   (False)
        self.set_border_width(10)
        self.set_icon_name   ("Youtube-youtube.com")
        self.set_titlebar    (self.getHeaderBar(switch))
        self.set_position    (Gtk.WindowPosition.CENTER)

        self.stack.add_titled(self.getAudioArea() , "A", "Audio" )
        self.stack.add_titled(self.getVideoArea() , "V", "Video" )
        switch.set_stack(self.stack)
        self.add(self.stack)



if __name__ == "__main__":
    Win = GydlMainGui()
    Win.connect("delete-event", Gtk.main_quit)
    Win.show_all()
    Gtk.main()
