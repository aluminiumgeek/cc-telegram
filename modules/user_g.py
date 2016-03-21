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
    params = {
        'v': '1.0',
        'q': query,
        'key': key
    }
    response = requests.get('http://ajax.googleapis.com/ajax/services/search/web', params=params)
    try:
        response = json.loads(response.content.decode('utf-8'))
    except ValueError:
        return 'Can not get results'

    items = response.get('responseData', {}).get('results', [])
    if len(items) > 0:
        item = items[0]
        return '{}\n{}\n{}'.format(item['titleNoFormatting'], re.sub(r'<.*?>', '', item['content']), unquote(item['url']))

    return 'No such items'
