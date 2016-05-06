# Install the plugin

    calibre-customize -b path_to_plugin_dir

# Converting a book

    ebook-convert something.epub something.pef
    ebook-convert something.txt something.pef 

# Options

Look for the section on output options:

    ebook-convert -h

In particular:

* --num-rows defaults to 4 and is number of rows per page
* --max-line-length defaults to 40 and is the maximum number of cells per row

# TODO

* pef header
