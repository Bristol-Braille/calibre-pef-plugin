# getting started

I wanted a new version of calibre to make use of the remote debugging.
It was too hard to install from source (dependencies) so I downloaded the binary package.

# install the plugin

calibre-customize -b path_to_plugin_dir

This sometimes needs to be run multiple times to correctly install the plugin.

# converting a book

ebook-convert something.epub something.pef

# todo

* pef header

# useful links

* https://manual.calibre-ebook.com/creating_plugins.html
* based on the TXTOutput plugin for Calibre by John Schember <john@nachtimwald.com

# debugging

https://manual.calibre-ebook.com/develop.html#using-the-python-debugger-as-a-remote-debugger

unfortunately as it is now, it doesn't show any program file context (list doesn't work)
