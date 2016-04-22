import os
from calibre.customize.conversion import OutputFormatPlugin

from calibre.constants import get_version
from calibre.customize.conversion import OutputFormatPlugin
from calibre.ebooks.conversion import ConversionUserFeedBack
from calibre.ebooks.conversion.plugins.epub_output import EPUBOutput
from calibre.ebooks.oeb.base import OPF
from calibre.utils.logging import Log


class HelloWorldOutput(OutputFormatPlugin):

    name                = 'Hello World Output Plugin' # Name of the plugin
    description         = 'blah '
    supported_platforms = ['linux'] # Platforms this plugin will run on
    author              = 'BBP' # The author of this plugin
    version             = (1, 0, 0)   # The version number of this plugin
    file_type           = 'bbp'
#    file_types          = set(['epub', 'mobi']) # The file types that this plugin will be applied to
#    on_postprocess      = True # Run this plugin after conversion is complete
    minimum_calibre_version = (0, 7, 53)

    def __init__(self, *args, **kwargs):
        self.epub_output_plugin = EPUBOutput(*args, **kwargs)
        OutputFormatPlugin.__init__(self, *args, **kwargs)
    
    def convert(self, oeb_book, output, input_plugin, opts, log):
        self.report_version(log)

        from calibre.rpdb import set_trace
        set_trace()

        from calibre.ebooks.txt.txtml import TXTMLizer
        from calibre.utils.cleantext import clean_ascii_chars
        from calibre.ebooks.txt.newlines import specified_newlines, TxtNewlines

        self.writer = TXTMLizer(log)

        txt = self.writer.extract_content(oeb_book, opts)
        txt = clean_ascii_chars(txt)
        from calibre import ipython
        ipython(locals())
        """ 
        asin = None
        for ident in oeb_book.metadata["identifier"]:
            scheme = ident.get(OPF("scheme"), None).lower()
            if (scheme.startswith("amazon") or scheme == "asin") and ident.value.startswith("B"):
                asin = ident.value
                break
        
        epub_filename = self.temporary_file(".epub").name
        self.epub_output_plugin.convert(oeb_book, epub_filename, input_plugin, opts, log)  # convert input format to EPUB
        log.info("Successfully converted input format to EPUB")
        
        self.convert_from_epub(JobLog(log), epub_filename, asin, output)
        """ 
    def report_version(self, log):
        log.info("bbp output")
        

