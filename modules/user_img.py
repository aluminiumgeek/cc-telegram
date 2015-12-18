import json
import base64
import requests

from modules.utils.data import prepare_binary_from_url

def check_store(bot, url):
    if bot.store:
        return bot.store.get(url)


def main(bot, *args):
    """
    img [query]
    Search for images around the internet.
    If no query specified, return next image from previous query.
    See also: g
    """

    query = ' '.join(args)
    last_query = getattr(bot, 'img_last_query', None)
    i = 0

    if last_query == query or (not args and last_query):
        if not args:
            query = last_query
        i = bot.img_last_num + 1
    elif not args:
        return 'Invalid syntax, read `/man img`'

    bot.img_last_query = query

    key = getattr(bot.settings, 'azure_bing_api_key', None)
    if not key:
        return 'Azure Bing API Key is not specified in settings'
    auth = base64.b64encode(bytes('{0}:{0}'.format(key), 'utf-8'))
    headers = {'Authorization': 'Basic {}'.format(auth.decode('utf-8'))}

    # Send custom chat action
    bot.pre_send(action='upload_photo')

    # Cache response to decrease number of requests to the bing api
    if last_query != query:
        # TODO: use `params` here, investigate 'Query is not of type String' error from azure
        response = requests.get('https://api.datamarket.azure.com/Bing/Search/v1/Image?Market=%27ru-RU%27&Adult=%27Moderate%27&Query=%27{}%27&$format=json&$top=20'.format(query), headers=headers).content
        bot.img_last_response = response
    else:
        response = bot.img_last_response

    try:
        search_data = json.loads(response.decode('utf-8'))
    except ValueError:
        return 'Can not get results'

    results = search_data.get('d', {}).get('results', [])
    if len(results) >= i + 1:
        while results[i - 1 if i > 1 else i:]:
            bot.img_last_num = i
            url = results[i]['MediaUrl']
            ext = url.rsplit('.', 1)[1]
            if ext.lower() in ('jpg', 'jpeg', 'gif', 'png'):
                file_id = check_store(bot, url)
                photo = file_id if file_id else prepare_binary_from_url(url)
                if photo:
                    break
            i += 1
        else:
            return 'No such images'

        data = {'chat_id': bot.chat_id}
        if file_id:
            data.update(photo=file_id)
            files = None
        else:
            files = {'photo': ('file.{}'.format(ext), photo, results[i]['ContentType'])}

        response = bot.call(
            'sendPhoto',
            'POST',
            data=data,
            files=files
        )
        if response and response.get('photo') and not file_id and bot.store:
            bot.store.set(url, response['photo'][-1]['file_id'])
    else:
        return 'No such images'

main.prevent_pre_send = True
