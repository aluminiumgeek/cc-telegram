import json
import logging
from typing import Optional

import aiohttp


async def pre_send(bot, chat_id: Optional[str]=None, action: str='typing') -> None:
    """
    Same as Bot.pre_send() but asynchronous
    """
    data = {
        'chat_id': chat_id if chat_id is not None else self.chat_id,
        'action': action
    }
    await call(bot, 'sendChatAction', 'POST', data=data)


async def send(bot, chat_id: Optional[str]=None, text: Optional[str]=None, data: dict={}) -> None:
    """
    Same as Bot.send() but asynchronous
    """
    if not text:
        return
    data.update(chat_id=chat_id if chat_id is not None else bot.chat_id, text=text)
    logging.debug('modules.utils.http.send :: Sending: {}'.format(data))
    await call(bot, 'sendMessage', 'POST', data=data)


async def call(bot, method_name: str, http_method: str, **kwargs):
    """
    Same as Bot.call() but asynchronous
    """

    timeout = getattr(bot.settings, 'updates_timeout', 60)

    uri = 'https://api.telegram.org/bot{}/{}'.format(
        bot.token, method_name)
    session = aiohttp.ClientSession()
    try:
        with aiohttp.ClientSession() as session:
            async with session.request(method=http_method, url=uri, **kwargs) as response:
                logging.debug('modules.utils.http.call :: url: {}, status: {}'.format(uri, response.status))
                response_text = await response.text()
    except Exception as e:
        logging.debug('modules.utils.http.call :: got exception: {}'.format(e))
        return

    logging.debug('modules.utils.http.call :: response: {}'.format(response_text))
    return json.loads(response_text)


async def perform_request(url, method, params={}):
    try:
        with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=url, params=params) as response:
                logging.debug('modules.utils.http.make_request :: url: {}, status: {}'.format(url, response.status))
                response_text = await response.text()
    except Exception as e:
        logging.debug('modules.utils.http.make_request :: got exception: {}'.format(e))
        return
    return response_text

