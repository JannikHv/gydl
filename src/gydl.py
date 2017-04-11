#!/usr/bin/env python3



__author__     = "Jannik Hauptvogel"
__maintainer__ = "Jannik Hauptvogel"
__email__      = "JannikHv@gmail.com"
__twitter__    = "https://twitter.com/TheJannikHa"
__git__        = "https://github.com/JannikHv/gydl"
__credits__    = "rg3"
__license__    = "GPLv2"



import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from os            import getenv
from subprocess    import call as subcall



class GydlMessageGui(Gtk.Window):

    def closeWindow(self, Widget, Data):
        self.close()

    def getLayout(self, Message):
        Label = Gtk.Label(Message)
        return Label

    def getHeaderBar(self, Title, Image):

        # Configure of the headerbar
        hBar  = Gtk.HeaderBar()
        Label = Gtk.Label(Title)
        Btn   = Gtk.Button(label="Done")
        Btn.get_style_context().add_class("download")

        # If a connection error occurs solely close the dialog
        if Title[0] == "C":
            Btn.connect("clicked", self.closeWindow, None)
        else:
            Btn.connect("clicked", Gtk.main_quit, None)

        # Configure the headerbar
        hBar.set_show_close_button(False)
        hBar.set_custom_title     (Label)
        hBar.pack_start           (Image)
        hBar.pack_end             (Btn)

        return hBar

    def __init__(self, Title, Message, Image):

        # Configure the window
        Gtk.Window.__init__  (self)
        self.set_default_size(375, 100)
        self.set_resizable   (False)
        self.set_border_width(10)
        self.set_icon_name   ("Youtube-youtube.com")
        self.set_titlebar    (self.getHeaderBar(Title, Image))
        self.set_position    (Gtk.WindowPosition.CENTER)

        self.add(self.getLayout(Message))
        self.show_all()



class GydlMainGui(Gtk.Window):

    def downloadMain(self, Cmd, Type):

        # Start the main download calling youtube-dl
        Status = subcall(Cmd, shell=True)

        if Status == 0:
            Title   = ("Download Finished")
            Message = ("Your "
                       + Type
                       + " has been downloaded successfully.\n"
                       + "The file has been stored in "
                       + getenv("HOME")
                       + "/ .\n"
                       + "Please press on \"Done\" to exit this program.")

            GydlMessageGui(Title, Message, Gtk.Image.new_from_icon_name(
                                           "object-select-symbolic",
                                           Gtk.IconSize.BUTTON))

        else:
            Title   = ("Download Unsuccessful")
            Message = ("Your "
                       + Type
                       + " has not been downloaded.\n"
                       + "Please press on \"Done\" to exit this program.")

            GydlMessageGui(Title, Message, Gtk.Image.new_from_icon_name(
                                           "action-unavailable-symbolic",
                                           Gtk.IconSize.BUTTON))

    def downloadVideo(self):

        # Prepare the command
        Cmd = ("youtube-dl --no-playlist -f FFF -f [height=QQQ] "
               + "-o \"~/%(title)s.%(ext)s\" \"UUU\"")

        Cmd = Cmd.replace("FFF", self.vFormat.get_active_text())
        Cmd = Cmd.replace("QQQ", self.vQuality.get_active_text().replace("p", ""))
        Cmd = Cmd.replace("UUU", self.vEntry.get_text())

        self.downloadMain(Cmd, "video")

    def downloadAudio(self):

        # Prepare the command
        Cmd = ("youtube-dl --no-playlist -x --audio-format FFF "
               + "--audio-quality QQQ -o \"~/%(title)s.%(ext)s\" \"UUU\"")

        if self.aFormat.get_active_text() == "ogg":
            Cmd = Cmd.replace("FFF", "vorbis")
        else:
            Cmd = Cmd.replace("FFF", self.aFormat.get_active_text())

        Cmd = Cmd.replace("QQQ", self.aQuality.get_active_text()[0])
        Cmd = Cmd.replace("UUU", self.aEntry.get_text())

        self.downloadMain(Cmd, "audio")

    def prepareDownload(self, widget, Stack):

        # Check internet connection
        try:
            Gio.NetworkMonitor.can_reach(Gio.NetworkMonitor.get_default(),
                                         Gio.NetworkAddress.new("google.com", 0),
                                         Gio.Cancellable.new())

            # Hide the main window
            self.hide()
            Gdk.flush()

            # Procceed to either Video or Audio download
            if Stack.get_visible_child_name() == "A":
                self.downloadAudio()
            else:
                self.downloadVideo()

        except Exception:

            # Show Connection error dialog
            Title   = ("Connection Error")
            Message = ("No internet connection has been established.\n"
                       + "Please press on \"Done\" to exit this program.")

            GydlMessageGui(Title, Message, 
                           Gtk.Image.new_from_icon_name(
                           "network-error-symbolic",
                           Gtk.IconSize.BUTTON))

    def getVideoArea(self):

        # Create basic widgets
        self.vEntry   = Gtk.Entry()
        self.vFormat  = Gtk.ComboBoxText()
        self.vQuality = Gtk.ComboBoxText()
        eLabel        = Gtk.Label("")
        fLabel        = Gtk.Label("")
        qLabel        = Gtk.Label("")
        Grid          = Gtk.Grid()

        # Add entries to comboboxes
        for i in ["3gp", "flv", "mp4", "webm"]:
            self.vFormat.append_text(i)

        for i in ["2160p", "1440p", "1080p", "720p",
                  "480p",  "360p",  "240p",  "144p"]:
            self.vQuality.append_text(i)

        self.vFormat .set_active(2)
        self.vQuality.set_active(3)

        # Add text to widgets
        eLabel.set_markup("<big>Enter the URL</big>"       )
        fLabel.set_markup("<big><u>Video-Format</u></big>" )
        qLabel.set_markup("<big><u>Video-Quality</u></big>")

        self.vEntry.set_placeholder_text("https://youtube.com/watch...")

        # Tweak the grid
        Grid.set_row_spacing(20)
        Grid.set_column_homogeneous(True)

        # Add the widgets to the grid
        Grid.attach(eLabel,       0, 0, 2, 1)
        Grid.attach(self.vEntry,  0, 1, 2, 1)
        Grid.attach(fLabel,       0, 2, 1, 1)
        Grid.attach_next_to(qLabel,
                            fLabel,
                            Gtk.PositionType.RIGHT, 1, 1)

        Grid.attach(self.vFormat, 0, 3, 1, 1)
        Grid.attach_next_to(self.vQuality,
                            self.vFormat,
                            Gtk.PositionType.RIGHT, 1, 1)

        return Grid

    def getAudioArea(self):

        # Create basic widgets
        self.aEntry   = Gtk.Entry()
        self.aFormat  = Gtk.ComboBoxText()
        self.aQuality = Gtk.ComboBoxText()
        eLabel        = Gtk.Label("")
        fLabel        = Gtk.Label("This Format")
        qLabel        = Gtk.Label("This Quality")
        Grid          = Gtk.Grid()

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
        eLabel.set_markup("<big>Enter the URL</big>"       )
        fLabel.set_markup("<big><u>Audio-Format</u></big>" )
        qLabel.set_markup("<big><u>Audio-Quality</u></big>")

        self.aEntry.set_placeholder_text("https://youtube.com/watch...")

        # Tweak the grid
        Grid.set_row_spacing(20)
        Grid.set_column_homogeneous(True)

        # Add the widgets to the grid
        Grid.attach(eLabel,       0, 0, 2, 1)
        Grid.attach(self.aEntry,  0, 1, 2, 1)
        Grid.attach(fLabel,       0, 2, 1, 1)
        Grid.attach_next_to(qLabel,
                            fLabel,
                            Gtk.PositionType.RIGHT, 1, 1)

        Grid.attach(self.aFormat, 0, 3, 1, 1)
        Grid.attach_next_to(self.aQuality,
                            self.aFormat,
                            Gtk.PositionType.RIGHT, 1, 1)

        return Grid

    def getHeaderBar(self, Switch, Stack):

        # Create download button
        bDownload = Gtk.Button(label="Download ")
        bDownload.connect("clicked", self.prepareDownload, Stack)
        bDownload.set_always_show_image(True)
        bDownload.get_style_context().add_class("download")
        bDownload.set_image_position(Gtk.PositionType.RIGHT)
        bDownload.set_image(Gtk.Image.new_from_icon_name(
                            "folder-download-symbolic",
                            Gtk.IconSize.BUTTON))

        # Create leave button
        bLeave = Gtk.Button(label=" Leave")
        bLeave.connect("clicked", Gtk.main_quit, None)
        bLeave.set_always_show_image(True)
        bLeave.set_image_position(Gtk.PositionType.LEFT)
        bLeave.set_image(Gtk.Image.new_from_icon_name(
                         "go-home-symbolic",
                         Gtk.IconSize.BUTTON))

        # Configure the headerbar
        hBar = Gtk.HeaderBar()
        hBar.set_show_close_button(False)
        hBar.set_custom_title(Switch)
        hBar.pack_start(bLeave)
        hBar.pack_end(bDownload)

        return hBar

    def setStyle(self):

        # Prepare the Css data
        GydlStyle = """
        button.download {
            background: #5baad2;
            color:      #ffffff;
        }

        button.download:hover {
            background: #7ebedd;
            color:      #ffffff;
        }
        """

        # Setup the CssProvider
        cssProv = Gtk.CssProvider()
        cssProv.load_from_data(bytes(GydlStyle.encode()))
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
                                                 cssProv,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def __init__(self):

        # Declare essential variables
        Switch = Gtk.StackSwitcher()
        Stack  = Gtk.Stack()

        # Configure the window
        Gtk.Window.__init__  (self)
        self.set_default_size(525, 230)
        self.set_resizable   (True)
        self.set_border_width(15)
        self.set_icon_name   ("Youtube-youtube.com")
        self.set_titlebar    (self.getHeaderBar(Switch, Stack))
        self.set_position    (Gtk.WindowPosition.CENTER)

        Stack.add_titled(self.getAudioArea(), "A", "Audio")
        Stack.add_titled(self.getVideoArea(), "V", "Video")
        Switch.set_stack(Stack)
        self.setStyle()
        self.add(Stack)



if __name__ == "__main__":
    Win = GydlMainGui()
    Win.connect("delete-event", Gtk.main_quit)
    Win.show_all()
    Gtk.main()
