import unittest
import os
import lxml.etree as etree
import louis

ebook_convert = "../calibre/ebook-convert"
calibre_customize = "../calibre/calibre-customize"
# use markdown so ebook-converter doesn't turn every new line into a paragraph
test_text_file = "text.md"  
test_book_lines = 100

test_epub_file = "text.epub"
pef_file = "text.pef"
rows_per_page = 4
chars_per_row = 40

# namespaces
PEFNS = "http://www.daisy.org/ns/2008/pef" 
DCNS = "http://purl.org/dc/elements/1.1/"


class TestConversion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # ensure plugin is up to date
        os.system(calibre_customize + " -b . ")

    @classmethod
    def setUp(cls):
        for test_file in [test_text_file, test_epub_file, pef_file]:
            try:
                os.remove(test_file)
            except OSError:
                pass

    @staticmethod
    def unicode_to_alpha(unicode):
        mapping = " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="
        return mapping[ord(unicode) - 10240]

    def create_text_file(self):
        # create a simple text file that will fits in the chars_per_row width
        # and not short enough to get joined into multiple lines (harder to test)
        content = []
        with open(test_text_file, 'w') as fh:
            for i in range(test_book_lines):
                line = "The quickbrownfoxjumpedoverlazydog.%03d\n" % i
                fh.write(line)
                content.append(line)
                self.assertLess(len(line), chars_per_row)
                self.assertGreater(len(line), chars_per_row - 5)
        return content

    def create_text_file_for_grade2(self):
        content = []
        with open(test_text_file, 'w') as fh:
            for i in range(test_book_lines):
                line = "the in and of how bigger what when why\n"
                fh.write(line)
                content.append(line)
                self.assertLess(len(line), chars_per_row)
        return content

    def test_text_conversion(self):
        test_content = self.create_text_file()
        os.system(ebook_convert + " " + test_text_file + " " + pef_file)
        self.assertTrue(os.path.exists(pef_file))
        self.pef_test(pef_file, test_content)

    def test_grade2_text_conversion(self):
        #test_content = self.create_text_file()
        test_content = self.create_text_file_for_grade2()
        grade2 = []
        for line in test_content:
            grade2.append(louis.translateString(['en-GB-g2.ctb'], line))
        os.system(ebook_convert + " " + test_text_file + " " + pef_file + " --ueb2")
        self.assertTrue(os.path.exists(pef_file))
        self.pef_test_grade2(pef_file, grade2)

    def test_epub_conversion(self):
        test_content = self.create_text_file()
        # first convert to epub
        os.system(ebook_convert + " " + test_text_file + " " + test_epub_file)
        # then to pef
        os.system(ebook_convert + " " + test_epub_file + " " + pef_file)
        self.assertTrue(os.path.exists(pef_file))
        self.pef_test(pef_file, test_content)

    def pef_test(self, pef_file, test_content):
        tree = etree.parse(pef_file)
        root = tree.getroot()
        pages = list(root.iter('{%s}page' % PEFNS))
        rows = list(root.iter('{%s}row' % PEFNS))

        # basic checks
        self.assertEqual(len(rows), len(test_content))
        self.assertEqual(len(pages), test_book_lines / rows_per_page)

        # check the encoding worked
        for pef, text in zip(rows, test_content):
            for i in range(len(pef.text)):
                self.assertEqual(TestConversion.unicode_to_alpha(pef.text[i]), text[i].upper())
                
    def pef_test_grade2(self, pef_file, test_content):
        tree = etree.parse(pef_file)
        root = tree.getroot()
        pages = list(root.iter('{%s}page' % PEFNS))
        rows = list(root.iter('{%s}row' % PEFNS))

        # basic checks
        self.assertEqual(len(rows), len(test_content))
        self.assertEqual(len(pages), test_book_lines / rows_per_page)

        # check the encoding worked
        for pef, text in zip(rows, test_content):
            for i in range(len(pef.text)):
                self.assertEqual(TestConversion.unicode_to_alpha(pef.text[i]), text[i].upper())

if __name__ == '__main__':
    unittest.main()
