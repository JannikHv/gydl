# Gydl
Gydl (Graphical Youtube-dl) is a GUI wrapper around the already existing youtube-dl program.

It's developed to be a dialog'ish GUI for quick video or audio downloads without disturbances.

Big thank you to the developer(s) of youtube-dl, you can check out their project over here:

https://github.com/rg3/youtube-dl

# Installation and dependencies
Gydl currently only exists as one single script written in Python 3.

To run it, you need to have the following dependencies installed:
* gtk+3
* python3
* pygobject

# Future
I will keep developing gydl in Python 3 until it's stable. Perhaps, in the future, I will rewrite it in a more suitable language.

Currently gydl just works, if there are flaws, please submit an issue.

The code is written to be readable and easy to develope onto.

# Usage
The GUI will show an entry to put the URL in and two boxes which will let you choose the quality and format of the video/audio. As of now, gydl will download everything in your home folder. That will be changed later though.

There are three different scenarios after **download** has been clicked.

* Internet Connection Error
* Download Unsuccessful
* Download Successful

These messages will appear as a window.

![alt tag](http://i.imgur.com/8QeD4Ri.png)


Thanks for any involvement in this project.

Kind regards, Jannik Hauptvogel.
