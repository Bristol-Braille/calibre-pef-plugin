# -*- coding: utf-8 -*-

"""
based on the TXTOutput plugin for Calibre by John Schember <john@nachtimwald.com
"""

import os
import shutil
import lxml.etree as etree
import lxml.builder    
import re

# namespaces
PEFNS = "http://www.daisy.org/ns/2008/pef" 
DCNS = "http://purl.org/dc/elements/1.1/"

from calibre.ebooks.metadata.meta import get_metadata, set_metadata
from calibre.rpdb import set_trace
from calibre.ebooks.txt.newlines import specified_newlines, TxtNewlines
from calibre.customize.conversion import OutputFormatPlugin, \
    OptionRecommendation
from calibre.ptempfile import TemporaryDirectory, TemporaryFile

NEWLINE_TYPES = ['system', 'unix', 'old_mac', 'windows']

class PEFOutput(OutputFormatPlugin):

    name = 'PEF Output'
    author = 'Matt Venn'
    file_type = 'pef'

    options = set([
        OptionRecommendation(name='newline', recommended_value='system',
            level=OptionRecommendation.LOW,
            short_switch='n', choices=NEWLINE_TYPES,
            help=_('Type of newline to use. Options are %s. Default is \'system\'. '
                'Use \'old_mac\' for compatibility with Mac OS 9 and earlier. '
                'For Mac OS X use \'unix\'. \'system\' will default to the newline '
                'type used by this OS.') % sorted(NEWLINE_TYPES)),
        OptionRecommendation(name='txt_output_encoding', recommended_value='utf-8',
            level=OptionRecommendation.LOW,
            help=_('Specify the character encoding of the output document. ' \
            'The default is utf-8.')),
        OptionRecommendation(name='ueb2',
            recommended_value=False, level=OptionRecommendation.LOW,
            help=_('Convert to Unified English Braille Grade 2')),
        OptionRecommendation(name='inline_toc',
            recommended_value=False, level=OptionRecommendation.LOW,
            help=_('Add Table of Contents to beginning of the book.')),
        OptionRecommendation(name='num_rows',
            recommended_value=4, level=OptionRecommendation.LOW,
            help=_('The maximum number of rows per page, defaults to 4.')),
        OptionRecommendation(name='max_line_length',
            recommended_value=40, level=OptionRecommendation.LOW,
            help=_('The maximum number of characters per line. This splits on '
            'the first space before the specified value. If no space is found '
            'the line will be broken at the space after and will exceed the '
            'specified value. Also, there is a minimum of 25 characters. '
            'Use 0 to disable line splitting. Default is 40.')),
        OptionRecommendation(name='force_max_line_length',
            recommended_value=True, level=OptionRecommendation.LOW,
            help=_('Force splitting on the max-line-length value when no space '
            'is present. Also allows max-line-length to be below the minimum. '
            'Default true.')),
        OptionRecommendation(name='txt_output_formatting',
             recommended_value='plain',
             choices=['plain', 'markdown', 'textile'],
             help=_('Formatting used within the document.\n'
                    '* plain: Produce plain text.\n'
                    '* markdown: Produce Markdown formatted text.\n'
                    '* textile: Produce Textile formatted text.')),
        OptionRecommendation(name='keep_links',
            recommended_value=False, level=OptionRecommendation.LOW,
            help=_('Do not remove links within the document. This is only ' \
            'useful when paired with a txt-output-formatting option that '
            'is not none because links are always removed with plain text output.')),
        OptionRecommendation(name='keep_image_references',
            recommended_value=False, level=OptionRecommendation.LOW,
            help=_('Do not remove image references within the document. This is only ' \
            'useful when paired with a txt-output-formatting option that '
            'is not none because links are always removed with plain text output.')),
        OptionRecommendation(name='keep_color',
            recommended_value=False, level=OptionRecommendation.LOW,
            help=_('Do not remove font color from output. This is only useful when ' \
                   'txt-output-formatting is set to textile. Textile is the only ' \
                   'formatting that supports setting font color. If this option is ' \
                   'not specified font color will not be set and default to the ' \
                   'color displayed by the reader (generally this is black).')),
     ])

    def convert(self, oeb_book, output_path, input_plugin, opts, log):
        from calibre.ebooks.txt.txtml import TXTMLizer
        from calibre.utils.cleantext import clean_ascii_chars
        
        self.log = log

        if opts.txt_output_formatting.lower() == 'markdown':
            from calibre.ebooks.txt.markdownml import MarkdownMLizer
            self.writer = MarkdownMLizer(log)
        elif opts.txt_output_formatting.lower() == 'textile':
            from calibre.ebooks.txt.textileml import TextileMLizer
            self.writer = TextileMLizer(log)
        else:
            self.writer = TXTMLizer(log)

        txt = self.writer.extract_content(oeb_book, opts)

        txt = clean_ascii_chars(txt)

        log.debug('\tReplacing newlines with selected type...')
        txt = specified_newlines(TxtNewlines(opts.newline).newline, txt)
        txt = txt.encode(opts.txt_output_encoding, 'replace')

        if opts.ueb2:
            import louis
            newline_char = TxtNewlines(opts.newline).newline
            grade2 = ""
            for line in txt.split(newline_char):
                grade2 += louis.translateString(['en-GB-g2.ctb'], line)
                grade2 += "\n"
            log.debug(grade2)
            txt = grade2

        log.debug('\tStripping final newline characters')
        txt = re.sub(TxtNewlines(opts.newline).newline + '*$', '', txt)
        
        log.debug('\tGenerating PEF...')
        metadata = oeb_book.metadata
        pef = self.create_pef(txt, opts, metadata)

        if not os.path.exists(os.path.dirname(output_path)) and os.path.dirname(output_path) != '':
            os.makedirs(os.path.dirname(output_path))

        import codecs
        fh = codecs.open(output_path, "w", "utf-8")
        fh.write(pef)

    def create_pef(self, txt, opts, metadata):
        newline_char = TxtNewlines(opts.newline).newline
        
        # setup PEF doc
        # http://files.pef-format.org/specifications/pef-2008-1/pef-specification.html
        pef = etree.Element('pef', nsmap = {None: PEFNS })
        tree = etree.ElementTree(pef)

        pef.set("version", "2008-1")

        head = etree.SubElement(pef, 'head')
        meta = etree.SubElement(head, 'meta', nsmap = {"dc" : DCNS})

        dc_format = etree.SubElement(meta, '{%s}format' % DCNS)
        dc_format.text = "application/x-pef+xml"

        dc_ident = etree.SubElement(meta, "{%s}identifier" % DCNS)
        dc_ident.text = "org.pef-format.00002"

        if len(metadata.title):
            title = metadata.title[0].value
            dc_title = etree.SubElement(meta, '{%s}title' % DCNS)
            dc_title.text = title

        if len(metadata.author):
            author = metadata.author[0].value
            dc_creator = etree.SubElement(meta, '{%s}creator' % DCNS)
            dc_creator.text = author

        body = etree.SubElement(pef, 'body')

        volume = etree.SubElement(body, 'volume')
        volume.set("cols", str(opts.max_line_length))
        volume.set("rows", str(opts.num_rows))

        section = etree.SubElement(volume, 'section')
       
        page_open = False
        rows = 0
        self.bad_chars = {}
        for line in txt.split(newline_char):
            self.log.debug('got new line [%s]' % line)
            if rows % opts.num_rows == 0:
                page = etree.SubElement(section, 'page')
            try:
                row = etree.SubElement(page, 'row')
                stripped = line.strip()
                pef = self.convert_to_pef(stripped)
                row.text = ''.join(pef)
                rows += 1
            except ValueError as e:
                print e
                print text

        return lxml.etree.tostring(tree, xml_declaration=True, encoding='UTF-8',pretty_print=True)

    # convert a single alpha, digit or some punctuation to 6 pin braille
    # http://en.wikipedia.org/wiki/Braille_ASCII#Braille_ASCII_values
    def alpha_to_pef(self, alpha):
        mapping = " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="
        alpha = alpha.upper()
        try:
            pin_num = mapping.index(alpha)
            return unichr(pin_num+10240)
        except ValueError as e:
            if not self.bad_chars.has_key(alpha):
                self.log.info("can't convert [%s] to braille" % alpha)
                self.bad_chars[alpha] = True
            return unichr(10240)

    # convert a list of alphas to pef unicode
    def convert_to_pef(self, alphas):
        return map(self.alpha_to_pef, alphas)

