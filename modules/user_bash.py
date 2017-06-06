import random
import sys

from lxml import html
from modules.utils import http


async def main(bot, *args, **kwargs):
    """
    bash [query]
    Search for quote on http://bash.im/
    If no query specified, return random quote.
    """

    path = 'index' if args else 'random'
    params = {'text': ' '.join(args).encode('windows-1251')} if args else {}
    url = 'http://bash.im/{}'.format(path)

    try:
        response_body = await http.perform_request(url, 'GET', params=params)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return "Can't get data"

    tree = html.fromstring(response_body)
    quotes = tree.xpath('//div[@class = "quote"]/div[@class = "text"]/..')
    if not quotes:
      return 'No such items'

    quote = random.choice(quotes)
    quote_id = quote.xpath('.//div[@class = "actions"]/a[@class = "id"]')[0]
    quote_text = quote.xpath('.//div[@class = "text"]')[0]
    for br in quote_text.xpath('.//br'):
        br.tail = '\n' + br.tail if br.tail else '\n'

    text = '{}\n{}'.format(quote_id.text_content(), quote_text.text_content())
    await http.send(bot, chat_id=kwargs.get('chat_id'), text=text, data={'disable_web_page_preview': True})
