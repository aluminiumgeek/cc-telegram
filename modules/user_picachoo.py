import re
import requests
import json

from modules.utils.data import prepare_binary_from_url


def main(bot, *args, **kwargs):
    """
    picachoo
    Return picture from picachoo.ru
    Usage: /picachoo [pic number] [page number]
    """
    user_page = None
    user_index = None

    try:
        user_page = int(args[1])
        user_index = int(args[0])
    except:
        pass

    matricies = json.loads(bot.store.get('picachoo_matricies') or '[]')
    curr_index = int(bot.store.get('picachoo_index') or 0)
    curr_page = int(bot.store.get('picachoo_page') or 0)

    if not user_page is None:
        curr_page = user_page

    if curr_index >= len(matricies) or not user_page is None:
        response = requests.get(
            'https://www.picachoo.ru/more/{}'.format(curr_page + 1), verify=False)
        matricies = list(
            set(re.findall("/files/thumb/.*?.jpg", response.content.decode('utf-8'))))
        matricies = list(
            map(lambda x: 'https://picachoo.ru{}'.format(x.replace('/thumb', '')), matricies))
        bot.store.set('picachoo_matricies', json.dumps(matricies))
        curr_page += 1
        curr_index = 0

    if not user_page is None and not user_index is None:
        curr_index = user_index % len(matricies)

    try:
        matrix = matricies[curr_index]
    except IndexError:
        return 'Page not found'

    ext = matrix.split('.')[2]
    chat_id = kwargs.pop('chat_id')

    bot.pre_send(chat_id=chat_id, action='upload_photo')

    if user_page is None and user_index is None:
        bot.store.set('picachoo_index', curr_index + 1)
        bot.store.set('picachoo_page', curr_page)

    bot.call(
        'sendPhoto',
        'POST',
        data={'chat_id': chat_id},
        files={'photo': (
            'file.{}'.format(ext),
            prepare_binary_from_url(matrix, verify=False),
            'image/' + ext
        )}
    )


main.prevent_pre_send = True
