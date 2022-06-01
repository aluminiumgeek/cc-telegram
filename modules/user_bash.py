import random
import re
import sys

from lxml import html
from modules.utils import http


async def main(bot, *args, **kwargs):
    """
    bash [query]
    Search for quote on http://bashorg.org/
    If no query specified, return random quote.
    """
    text = await bash_search(*args) if args else await bash_random()

    await http.send(bot, chat_id=kwargs.get('chat_id'), text=text, data={'disable_web_page_preview': True})

async def bash_random():
    url = 'http://bashorg.org/casual'

    try:
        response_body = await http.perform_request(url, 'GET')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return "Can't get data"

    tree = html.fromstring(response_body)
    quote = tree.xpath('//div[@class = "q"]/div[2]')[0]
    for br in quote.xpath('.//br'):
        br.tail = '\n' + br.tail if br.tail else '\n'
    quote_text = quote.text_content()
    quote_title = quote.xpath('..//div[@class = "vote"]/a[4]')[0]
    quote_title_text = re.search('(\d+)$', quote_title.text_content()).group(1)

    text = '#{}\n{}'.format(quote_title_text, quote_text)

    return text

async def bash_search(*args):
    url = 'http://bashorg.org/index.php?do=search'

    params = {
        'do': 'search',
        'subaction': 'search',
        'search_start': 0,
        'full_search': 0,
        'result_from': 1,
        'result_num': 100,
        'story': ' '.join(args).encode('windows-1251')
    }

    try:
        response_body = await http.perform_request(url, 'POST', params=params)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return "Can't get data"

    tree = html.fromstring(response_body)
    quotes = tree.xpath('//div[@id = "quotes"]/table')
    if not quotes:
      return 'No such items'

    quote = random.choice(quotes)
    quote_text = quote.xpath('.//div')[0]
    for br in quote_text.xpath('.//br'):
        br.tail = '\n' + br.tail if br.tail else '\n'
    quote_title = quote.xpath('.//span[@class = "ntitle"]/..')[0]
    quote_title_text = re.search('(\d+)$', quote_title.text_content()).group(1)

    text = '#{}\n{}'.format(quote_title_text, quote_text.text_content())

    return text
