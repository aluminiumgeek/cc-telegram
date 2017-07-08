import re
import requests

def main(bot, *args, **kwargs):
    """
    kot
    Stupid cat memes from http://kotomatrix.ru
    """

    matricies = bot.store.get('kot_matricies', default = [])
    curr_index = bot.store.get('kot_index', default = 0)

    if curr_index >= len(matricies) :
        response = requests.get('http://kotomatrix.ru/rand/')
        matricies = list(set(re.findall(
            "http://kotomatrix.ru/images/.*.jpg",
            response.content.decode('utf-8')
        )))
        bot.store.set('kot_matricies', matricies)
        curr_index = 0

    bot.store.set('kot_index', curr_index + 1)

    return matricies[curr_index]
