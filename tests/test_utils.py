# -*- coding: utf-8 -*-
import unittest

from modules.utils import text


class UtilsTestCase(unittest.TestCase):

    def test_clean_text_should_remove_inappropriate_chars(self):
        line = u'This :;requirement? # !is @only = $necessary %when ^you &place *your (1st ;order |with us, Mr -. а также кириллица 何か'
        expected = u'This requirement  is only  necessary when you place your 1st order with us, Mr -. а также кириллица 何か'
        self.assertEqual(text.clean_text(line), expected)
