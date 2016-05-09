import re
import json
import requests
from urllib.parse import unquote


def main(bot, *args, **kwargs):
    """
    g [y|w|m] <search query>
    Search on google
    `y` option enables site:youtube.com
    `w` option enables site:en.wikipedia.org
    `m` option enables site:myanimelist.net
    See also: img
    """

    if not args:
        return 'Invalid syntax, read `/man g`'

    args = list(args)

    options = {
        'y': 'site:youtube.com',
        'w': 'site:en.wikipedia.org',
        'm': 'site:myanimelist.net'
    }

    appendix = ''
    if args[0] in options and len(args) > 1:
        appendix = options[args.pop(0)]
    query = '{} {}'.format(' '.join(args), appendix)

    key = getattr(bot.settings, 'google_api_key', None)
    if not key:
        return 'Google API Key is not specified in settings'
    cx = getattr(bot.settings, 'google_cse_cx', None)
    if not cx:
        return 'Google Custom Search Engine CX is not specified in settings'
    params = {
        'cx': cx,
        'q': query,
        'key': key
    }
    response = requests.get('https://www.googleapis.com/customsearch/v1?parameters', params=params)

    try:
        response = json.loads(response.content.decode('utf-8'))
    except ValueError:
        return 'Can not get results'

    items = response.get('items', [])
    if len(items) > 0:
        item = items[0]
        return '{}\n{}\n{}'.format(item['title'], re.sub(r'<.*?>', '', item['snippet']), unquote(item['link']))

    return 'No such items'
