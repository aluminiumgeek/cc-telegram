 
import unittest

from modules.utils import text


class UtilsTestCase(unittest.TestCase):

    def test_clean_text_should_remove_inappropriate_chars(self):
        line = 'This :;requirement? # !is @only = $necessary %when ^you &place *your (1st ;order |with us, Mr -.'
        expected = 'This requirement  is only  necessary when you place your 1st order with us, Mr -.'
        self.assertEqual(text.clean_text(line), expected)
