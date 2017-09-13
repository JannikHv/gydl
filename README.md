# About

Gydl (Graphical Youtube-dl) is a GUI wrapper around the already existing
youtube-dl program.

It's developed with a dialog driven experience in mind. This provides a quick
and easy video or audio downloads without disturbances.

Big **thank you** to the developer(s) of youtube-dl! Check out their project:

https://github.com/rg3/youtube-dl

# News!

Gydl is receiving a rewrite to C. When it's stable, the work on a new design is starting.

Thanks for your patience.

# Installation

## GNU/Linux Packages

* [Arch Linux](https://aur.archlinux.org/packages/gydl-git/)
  (Credit: [AffeAli](https://github.com/AffeAli))

## Source

Gydl is written in Python3 and uses the GTK+3 toolkit.

### Dependencies

To run it you need to have installed:

* gtk+3
* python3
* pygobject
* youtube-dl

### Build & Install

Meson installs to `/usr/local` as the default prefix.

```
meson build
cd build
ninja install
```

### Build Options

Use `meson --help` to get all build options. You may specify any option when
you initially run meson.

```
# Example
meson build --prefix=/app
```

If you already have a build directory, you must use instead use
`meson configure`, from within the build directory.

```
# Example
cd build
meson configure -Dprefix=/app
```

Meson also supports the **DESTDIR** environment variable, which is useful for
building a package.

[See Meson documentation for more](http://mesonbuild.com)


# Translation

Gydl itself is currently not translatable, but the appdata and
the desktop entry is.

Use the build system to generate a POT template file from the latest commit.

```
meson build
ninja -C build Gydl-pot
rm -rf build
```

Copy the POT file into a PO file matching your language code and translate
all strings. Alternatively follow the above steps and use a tool like Poedit.

# Usage

When using Gydl, you have the option to download your Youtube Video as a
**Video** or **Audio**.

Each of these options have a text entry, as well as 2 combo-boxes managing
quality and the format.


![alt tag](http://i.imgur.com/o4pYQrX.png)

When clicking on **Download** there are 3 scenarios you can face:

* Download Finished - When your download has finished successfully.

![alt tag](http://i.imgur.com/yVrmyPH.png)

* Download Unsuccessful - When a bad URL was entered or similar errors occured.

![alt tag](http://i.imgur.com/P7ZIWaX.png)

* Connection Error - When no internet connection could be established.

![alt tag](http://i.imgur.com/Vrys4YO.png)

These dialogues will be presented to you as a little windows.

Notice that not every combination of settings will work.

Thanks for any involvement in this project, I hope you like it.

Kind regards, Jannik Hauptvogel.
