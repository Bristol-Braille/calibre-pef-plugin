# PEF converter plugin for Calibre

A plugin for the open source ebook library and converter [Calibre](https://calibre-ebook.com/)

Converts any book format that Calibre supports to the [PEF format](http://files.pef-format.org/specifications/pef-2008-1/pef-specification.html)

This plugin is based on the [TXTOutput](https://github.com/kovidgoyal/calibre/blob/ac8363713b8d82b33516c3806fc142bc04b5ace6/src/calibre/ebooks/conversion/plugins/txt_output.py) plugin by John Schember.

# Install the plugin

    calibre-customize -b path_to_plugin_dir

# Converting a book

    ebook-convert something.epub something.pef
    ebook-convert something.txt something.pef 

# Options

Look for the section on output options:

    ebook-convert -h

In particular:

* --ueb2 use liblouis to convert to contracted grade 2
* --num-rows defaults to 4 and is number of rows per page
* --max-line-length defaults to 40 and is the maximum number of cells per row

# Dependencies

If you want to use liblouis to contract the braille, you will need to install
the library and the python bindings.

    https://github.com/liblouis/liblouis

# TODO

* more testing
