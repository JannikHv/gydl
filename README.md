# About
Gydl (Graphical Youtube-dl) is a GUI wrapper around the already existing youtube-dl program.

It's developed to be a dialog'ish GUI for quick and easy video or audio downloads without disturbances.

Big **thank you** to the developer(s) of youtube-dl! Check out their project:

https://github.com/rg3/youtube-dl

# Installation and dependencies

Gydl is written in Python3 and uses the Gtk+3 toolkit.

To run it you need to have installed:

* Gtk+3
* Python3
* PyGobject

**ArchLinux:**

[AffeAli](https://github.com/AffeAli) has created an [AUR Package](https://aur.archlinux.org/packages/gydl-git/) for Gydl, so you can install it by:

*$ yaourt -S gydl-git*

Big thanks to him.

# Usage

When using Gydl, you have the option to download your Youtube Video as a **Video** or **Audio**.

Each of these options have a Text Entry, a Quality Combobox and a Format Combobox.

![alt tag](http://i.imgur.com/rRPfQAQ.png)

When clicking on **Download** there are 3 scenarious you can face:

* Download Successful      - When your download was finished successfully.

![alt tag](http://imgur.com/pQLJLVP)

* Download Unsuccessful    - When a bad URL was entered or similar errors occured.

![alt tag](http://i.imgur.com/yRdpYUU.png)

* Internet Conection Error - When no internet connection could be established.

![alt tag](http://i.imgur.com/zcJedAp.png)

These dialogs will be presented to you as a little dialog'ish windows.

Thanks for any involvement in this project, I hope you like it.

Kind regards, Jannik Hauptvogel.
