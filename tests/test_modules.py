# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch, MagicMock
from freezegun import freeze_time

from modules.utils import text
from modules import user_cowsay, user_date, user_g


class BaseModuleTestCase(unittest.TestCase):

    def setUp(self):
        self.bot = MagicMock()


class UserCowsayTestCase(BaseModuleTestCase):

    @patch('os.popen')
    def test_run_module_with_args_should_call_bot_send(self, popen):
        user_cowsay.main(self.bot, 'test', 'message')
        self.assertEqual(self.bot.send.call_count, 1)

    def test_run_module_without_args_should_return_none(self):
        user_cowsay.main(self.bot)
        self.assertEqual(self.bot.send.call_count, 0)


class UserDateTestCase(BaseModuleTestCase):

    @freeze_time('2015-12-14 12:13:14')
    def test_run_module_without_args_should_return_current_datetime(self):
        self.assertEqual(user_date.main(self.bot), '2015-12-14 12:13:14')

    def test_run_module_with_args_should_return_dating_text(self):
        self.assertEqual(user_date.main(self.bot, 'username'), 'обдумав свои чувства, пригласил на свидание username')


class UserGoogleTestCase(BaseModuleTestCase):

    def setUp(self):
        super(UserGoogleTestCase, self).setUp()
        self.bot.settings.google_api_key = 'api-key'

    @patch('modules.user_g.requests.get', lambda *args, **kwargs: MagicMock(content=b'{"responseData": {"results": [{"titleNoFormatting": "hello", "content": "content <b>of the</b> result", "url": "http://example.com"}]}}'))
    def test_run_module_with_args_should_return_search_result(self):
        self.assertEqual(user_g.main(self.bot, 'green', 'apples'), 'hello\ncontent of the result\nhttp://example.com')

    @patch('modules.user_g.requests.get', return_value=MagicMock(content=b''))
    def test_run_module_with_option_and_args_should_enable_query_option(self, get):
        user_g.main(self.bot, 'y', 'rare', 'jazz')
        params = {
            'v': '1.0',
            'q': 'rare jazz site:youtube.com',
            'key': 'api-key'
        }
        get.assert_called_once_with('http://ajax.googleapis.com/ajax/services/search/web', params=params)

    def test_run_module_without_args_should_return_error_message(self):
        self.assertEqual(user_g.main(self.bot), 'Invalid syntax, read `/man g`')

    @patch('modules.user_g.requests.get', lambda *args, **kwargs: MagicMock(content=b'{"responseData": {"results": []}}'))
    def test_module_should_return_error_message_when_no_results(self):
        self.assertEqual(user_g.main(self.bot, 'dank', 'memes'), 'No such items')
