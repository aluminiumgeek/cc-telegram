import random
import sys

from lxml import html
from modules.utils import http


async def main(bot, *args, **kwargs):
    """
    bash
    Random quote from http://bash.im/
    """
    try:
        response_body = await http.perform_request("http://bash.im/random", 'GET')
    except:
        print("Unexpected error:", sys.exc_info()[0])



    tree = html.fromstring(response_body)
    quotes = tree.xpath('//div[@class = "quote"]/div[@class = "text"]/..')
    quote = random.choice(quotes)
    text = quote.xpath('.//div[@class = "text"]')[0]
    for br in text.xpath('.//br'):
        br.tail = '\n' + br.tail if br.tail else '\n'
    text = text.text_content()


    await http.send(bot, chat_id=kwargs.get('chat_id'), text=text, data={'disable_web_page_preview': True})
