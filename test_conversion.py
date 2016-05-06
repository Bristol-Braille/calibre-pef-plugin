import unittest
import os
import lxml.etree as etree

ebook_convert = "../calibre/ebook-convert"
calibre_customize = "../calibre/calibre-customize"
test_text_file = "text.txt"
test_epub_file = "text.epub"
pef_file = "text.pef"
rows_per_page = 4


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

    def create_text_file(self):
        # create a simple text file
        with open(test_text_file, 'w') as fh:
            for i in range(100):
                fh.write("test line number %d\n" % i)

    def test_text_conversion(self):
        self.create_text_file()
        os.system(ebook_convert + " " + test_text_file + " " + pef_file)
        self.assertTrue(os.path.exists(pef_file))
        tree = etree.parse(pef_file)
        root = tree.getroot()
        pages = list(root.iter('page'))
        rows = list(root.iter('row'))
        self.assertEqual(len(rows), len(pages) * rows_per_page)

    def test_epub_conversion(self):
        self.create_text_file()
        # first convert to epub
        os.system(ebook_convert + " " + test_text_file + " " + test_epub_file)
        # then to pef
        os.system(ebook_convert + " " + test_epub_file + " " + pef_file)
        self.assertTrue(os.path.exists(pef_file))
        tree = etree.parse(pef_file)
        root = tree.getroot()
        pages = list(root.iter('page'))
        rows = list(root.iter('row'))
        self.assertEqual(len(rows), len(pages) * rows_per_page)

if __name__ == '__main__':
    unittest.main()
