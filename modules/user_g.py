import re
import json
import requests


def main(bot, *args):
    """
    g [y|w] [search query]
    Search on Google.
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

    response = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q={}'.format(query))
    try:
        response = json.loads(response.content.decode('utf-8'))
    except ValueError:
        return 'Can not get results'

    items = response.get('responseData', {}).get('results', [])
    if len(items) > 0:
        item = items[1]
        return '{}\n{}\n{}'.format(item['titleNoFormatting'], re.sub(r'<.*?>', '', item['content']), item['url'])

    return 'No such items'
