import random
import requests
import sys

from lxml import html


async def main(bot, *args, **kwargs):
    """
    bash [query]
    Search for quote on https://bash.im
    If no query specified, return random quote.
    """

    if args:
        path = 'search'
        params = {
            'text': ' '.join(args).encode('utf-8')
        }
    else:
        path = 'random'
        params = {}

    url = 'https://bash.im/{}'.format(path)
    try:
        response = requests.get(url, params=params, verify=False)
        response_body = response.content.decode('utf-8')
        response_html = html.fromstring(response_body)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return "Can't get data"

    quotes = response_html.xpath('//article[@class = "quote"]')
    if not quotes:
        return 'No such items'

    quote = random.choice(quotes)
    [quote_body] = quote.find_class('quote__body')

    for br in quote_body.findall('br'):
        br.tail = '\n{}'.format(br.tail or '')

    quote_id = quote.get('data-quote')
    quote_text = quote_body.text_content().strip()

    result_text = '#{0}\n{1}'.format(quote_id, quote_text)

    bot.call(
        'sendMessage',
        'POST',
        data={
            'chat_id': kwargs.get('chat_id'),
            'disable_web_page_preview': True,
            'parse_mode': None,
            'text': result_text
        }
    )
