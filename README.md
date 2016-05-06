# getting started

I wanted a new version of calibre to make use of the remote debugging.
It was too hard to install from source (dependencies) so I downloaded the binary package.

# install the plugin

calibre-customize -b path_to_plugin_dir

This sometimes needs to be run multiple times to correctly install the plugin.

# converting a book

ebook-convert something.epub something.pef

# useful links

* https://manual.calibre-ebook.com/creating_plugins.html
* based off the KFX output plugin http://www.mobileread.com/forums/showthread.php?t=272407 by J Howell

# debugging

https://manual.calibre-ebook.com/develop.html#using-the-python-debugger-as-a-remote-debugger
