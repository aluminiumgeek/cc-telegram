import re
import requests
import json

from modules.utils.data import prepare_binary_from_url

def main(bot, *args, **kwargs):
    """
    kot
    Stupid cat memes from http://kotomatrix.ru
    """

    matricies = json.loads(bot.store.get('kot_matricies').decode() or '[]')
    curr_index = int(bot.store.get('kot_index') or 0)

    if curr_index >= len(matricies):
        response = requests.get('http://kotomatrix.ru/rand/')
        matricies = list(set(re.findall(
            "http://kotomatrix.ru/images/.*.jpg",
            response.content.decode('utf-8')
        )))
        bot.store.set('kot_matricies', json.dumps(matricies))
        curr_index = 0

    matrix = matricies[curr_index]
    ext = matrix.split('.')[2]
    chat_id = kwargs.pop('chat_id')

    bot.pre_send(chat_id=chat_id, action='upload_photo')

    bot.call(
        'sendPhoto',
        'POST',
        data = {'chat_id': chat_id},
        files = {'photo': (
            'file.{}'.format(ext),
            prepare_binary_from_url(matrix),
            'image/' + ext
        )}
    )

    bot.store.set('kot_index', curr_index + 1)

main.prevent_pre_send = True
