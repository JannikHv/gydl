#!/usr/bin/env python3

__author__     = "Jannik Hauptvogel"
__maintainer__ = "Jannik Hauptvogel"
__email__      = "JannikHv@gmail.com"
__twitter__    = "https://twitter.com/JannikHv"
__git__        = "https://github.com/JannikHv/gydl"
__aur__        = "https://aur.archlinux.org/packages/gydl-git/"
__credits__    = "rg3"
__license__    = "GPLv2"

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import (Gtk, Gdk, GLib, Gio)
from os import system
from subprocess import Popen, PIPE

class Gydl:
    class DialogType:
        NET_ERROR = 0
        DL_ERROR  = 1
        DL_FINISH = 2



    class ViewType:
        AUDIO = 0
        VIDEO = 1



    class Downloader:
        def get_can_reach(self, URL):
            try:
                Gio.NetworkMonitor.can_reach(Gio.NetworkMonitor.get_default(),
                                             Gio.NetworkAddress.new(URL, 0),
                                             Gio.Cancellable.new())
                return True
            except:
                pass

            return False

        def get_audio(self, URL, FORMAT, QUALITY):
            cmd = ("youtube-dl --no-playlist -x "
                 + "--audio-format FFF "
                 + "--audio-quality QQQ "
                 + "-o \""
                 + GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOWNLOAD)
                 + "/%(title)s.%(ext)s\" \"UUU\"")

            cmd = cmd.replace("FFF", FORMAT)
            cmd = cmd.replace("QQQ", QUALITY)
            cmd = cmd.replace("UUU", URL)
            if system(cmd) is 0:
                return True
            else:
                return False

        def get_video(self, URL, FORMAT, QUALITY):
            pre = ("youtube-dl --no-playlist -F \"" + URL + "\"| grep " + FORMAT + " | grep " + QUALITY + " | cut -f 1 -d ' ' | tail -n 1")
            settings = Popen(pre, shell = True,stdout=PIPE).communicate()[0]
            settings="".join(map(chr, settings)).rstrip("\n")
            if settings=="":
                 settings = "best"
            cmd = ("youtube-dl --no-playlist "
                 + "-f " 
                 + settings
                 + " -o \""
                 + GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOWNLOAD)
                 + "/%(title)s.%(ext)s\" \"UUU\"")

            cmd = cmd.replace("UUU", URL)
            if system(cmd) is 0:
                return True
            else:
                return False



    class Dialog(Gtk.Window):
        def __continue_button_clicked(self, widget, data):
            self.disconnect_by_func(Gtk.main_quit)
            self.close()

        def __get_title_from_type(self, dialog_type):
            if dialog_type is Gydl.DialogType.NET_ERROR:
                return "Connection Error"
            elif dialog_type is Gydl.DialogType.DL_ERROR:
                return "Download Failed"
            elif dialog_type is Gydl.DialogType.DL_FINISH:
                return "Download Successful"
            else:
                return None

        def __get_text_from_type(self, dialog_type):
            if dialog_type is Gydl.DialogType.NET_ERROR:
                return ("An internet connection error has occured.\n"
                      + "Make sure you're connected to the internet.")
            elif dialog_type is Gydl.DialogType.DL_ERROR:
                return ("The download has been unsuccessful.\n"
                      + "Make sure the URL you've entered is valid."
            elif dialog_type is Gydl.DialogType.DL_FINISH:
                return ("The download has been successful.\n"
                      + "The file has been saved in your download folder.")
            else:
                return None

        def __init__(self, dialog_type):
            Gtk.Window.__init__(self, Gtk.WindowType.TOPLEVEL)

            self.hbar = Gtk.HeaderBar()
            self.grid = Gtk.Grid()

            self.label        = Gtk.Label()
            self.btn_leave    = Gtk.Button.new_with_mnemonic("_Leave")
            self.btn_continue = Gtk.Button.new_with_mnemonic("_Continue")

            # Window
            self.set_default_size(400, 200)
            self.set_titlebar(self.hbar)
            self.set_position(Gtk.WindowPosition.CENTER)
            self.set_icon_name("gydl")
            self.add(self.grid)
            self.connect("destroy", Gtk.main_quit, None)

            # Header bar
            self.hbar.set_title(self.__get_title_from_type(dialog_type))

            # Grid
            self.grid.set_column_homogeneous(True)
            self.grid.set_row_homogeneous(True)

            # Label
            self.label.set_text(self.__get_text_from_type(dialog_type))

            # Buttons
            self.btn_leave.connect("clicked", Gtk.main_quit, None)
            self.btn_continue.connect("clicked", self.__continue_button_clicked, None)
            self.btn_continue.get_style_context().add_class("suggested-action")

            # Attach widgets to grid
            self.grid.attach(self.label,        0, 0, 2, 3)
            self.grid.attach(self.btn_leave,    0, 3, 1, 1)
            self.grid.attach(self.btn_continue, 1, 3, 1, 1)



    class View(Gtk.Grid):
        def __build_audio(self):
            for entry in ["aac", "m4a", "mp3", "vorbis", "wav"]:
                self.format.append_text(entry)

            for entry in ["0 (Best)", "1", "2", "3", "4", "5 (Average)", "6", "7", "8", "9 (Worst)"]:
                self.quality.append_text(entry)

            self.format.set_active(2)
            self.quality.set_active(0)

        def __build_video(self):
            for entry in ["3gp", "flv", "mp4", "webm"]:
                self.format.append_text(entry)

            for entry in ["2160p", "1440p", "1080p", "720p",
                          "480p", "360p", "240p", "144p"]:
                self.quality.append_text(entry)

            self.format.set_active(2)
            self.quality.set_active(3)

        def get_url(self):
            return self.entry.get_text()

        def get_format(self):
            return self.format.get_active_text()

        def get_aquality(self):
            return self.quality.get_active_text()[0]

        def get_vquality(self):
            return self.quality.get_active_text()

        def __init__(self, view_type):
            Gtk.Grid.__init__(self)

            self.l_entry   = Gtk.Label()
            self.l_format  = Gtk.Label()
            self.l_quality = Gtk.Label()

            self.entry   = Gtk.Entry()
            self.format  = Gtk.ComboBoxText()
            self.quality = Gtk.ComboBoxText()

            # Grid
            self.set_column_homogeneous(True)
            self.set_border_width(10)

            # Labels
            self.l_entry.set_markup("<span size='15000'><u>\nEnter the URL\n</u></span>")
            self.l_format.set_markup("<span size='15000'><u>\nFormat\n</u></span>")
            self.l_quality.set_markup("<span size='15000'><u>\nQuality\n</u></span>")

            # Entry
            self.entry.set_placeholder_text("https://youtube.com/watch...")

            # Combo boxes
            self.format.set_border_width(5)
            self.quality.set_border_width(5)

            # Attach widgets to grid
            self.attach(self.l_entry,   0, 0, 4, 1)
            self.attach(self.entry,     0, 1, 4, 1)
            self.attach(self.l_format,  0, 2, 2, 1)
            self.attach(self.l_quality, 2, 2, 2, 1)
            self.attach(self.format,    0, 3, 2, 1)
            self.attach(self.quality,   2, 3, 2, 1)

            # Check view type
            if view_type is Gydl.ViewType.AUDIO:
                self.__build_audio()
            elif view_type is Gydl.ViewType.VIDEO:
                self.__build_video()
            else:
                pass



    class Window(Gtk.Window):
        def __hide_all(self):
            self.hide()
            Gdk.flush()

        def __show_all(self):
            self.show_all()
            Gdk.flush()

        def __dialog_closed(self, widget, data, null):
            self.__show_all()

        def __download_button_clicked(self, widget, data):
            self.__hide_all()

            # Check internet connection
            if not self.downloader.get_can_reach("youtube.com"):
                dialog = Gydl.Dialog(Gydl.DialogType.NET_ERROR)
                dialog.show_all()
                dialog.connect("delete-event", self.__dialog_closed, None)
                return

            # Collect data
            if self.stack.get_visible_child_name() == "Audio":
                dl_exit = self.downloader.get_audio(self.view_audio.get_url(),
                                                    self.view_audio.get_format(),
                                                    self.view_audio.get_aquality())
            elif self.stack.get_visible_child_name() == "Video":
                dl_exit = self.downloader.get_video(self.view_video.get_url(),
                                                    self.view_video.get_format(),
                                                    self.view_video.get_vquality())
            else:
                dl_exit = False

            if dl_exit:
                dialog = Gydl.Dialog(Gydl.DialogType.DL_FINISH)
            else:
                dialog = Gydl.Dialog(Gydl.DialogType.DL_ERROR)

            dialog.connect("delete-event", self.__dialog_closed, None)
            dialog.show_all()

        def __init__(self):
            Gtk.Window.__init__(self, Gtk.WindowType.TOPLEVEL)

            self.downloader = Gydl.Downloader()

            self.hbar       = Gtk.HeaderBar()
            self.stack      = Gtk.Stack()
            self.view_audio = Gydl.View(Gydl.ViewType.AUDIO)
            self.view_video = Gydl.View(Gydl.ViewType.VIDEO)

            self.switcher = Gtk.StackSwitcher()
            self.btn_lv   = Gtk.Button.new_with_mnemonic("_Leave")
            self.btn_dl   = Gtk.Button.new_with_mnemonic("_Download")

            # Window
            self.set_default_size(525, 275)
            self.set_titlebar(self.hbar)
            self.set_position(Gtk.WindowPosition.CENTER)
            self.set_icon_name("gydl")
            self.add(self.stack)

            # Header bar
            self.hbar.pack_start(self.btn_lv)
            self.hbar.pack_end(self.btn_dl)
            self.hbar.set_custom_title(self.switcher)

            # Stack
            self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
            self.stack.add_titled(self.view_audio, "Audio", "Audio")
            self.stack.add_titled(self.view_video, "Video", "Video")

            # Stack switcher
            self.switcher.set_stack(self.stack)

            # Header bar buttons
            self.btn_lv.connect("clicked", Gtk.main_quit, None)
            self.btn_dl.connect("clicked", self.__download_button_clicked, None)
            self.btn_dl.get_style_context().add_class("suggested-action")



if __name__ == "__main__":
    Window = Gydl.Window()
    Window.connect("delete-event", Gtk.main_quit, None)
    Window.show_all()
    Gtk.main()
