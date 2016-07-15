import json
import base64
import requests
from datetime import datetime, timedelta
from requests.exceptions import RequestException

from modules.utils.data import prepare_binary_from_url


def check_store(bot, url):
    if bot.store:
        return bot.store.get(url)


def response(bot, message, chat_id):
    setattr(bot, 'img_last_time_{}'.format(chat_id), datetime.now())
    return message


def main(bot, *args, **kwargs):
    """
    img [query]
    Search for images around the internet.
    If no query specified, return next image from previous query.
    See also: g
    """

    global response

    chat_id = kwargs.pop('chat_id')
    query = ' '.join(args)
    last_query = getattr(bot, 'img_last_query_{}'.format(chat_id), None)
    i = 0

    last_time = getattr(bot, 'img_last_time_{}'.format(chat_id), None)
    if last_time and last_time > datetime.now() - timedelta(seconds=1):
        return 'Not so fast'

    if last_query == query or (not args and last_query):
        if not args:
            query = last_query
        i = getattr(bot, 'img_last_num_{}'.format(chat_id)) + 1
    elif not args:
        return response(bot, 'Invalid syntax, read `/man img`', chat_id)

    setattr(bot, 'img_last_query_{}'.format(chat_id), query)

    key = getattr(bot.settings, 'azure_bing_api_key', None)
    if not key:
        return response(bot, 'Azure Bing API Key is not specified in settings', chat_id)
    auth = base64.b64encode(bytes('{0}:{0}'.format(key), 'utf-8'))
    headers = {'Authorization': 'Basic {}'.format(auth.decode('utf-8'))}

    # Cache return response to decrease number of requests to the bing api
    if last_query != query:
        # TODO: use `params` here, investigate 'Query is not of type String' error from azure
        try:
            azure_response = requests.get('https://api.datamarket.azure.com/Bing/Search/v1/Image?Market=%27ru-RU%27&Adult=%27Moderate%27&Query=%27{}%27&$format=json&$top=20'.format(query), headers=headers, timeout=(1, 2)).content
        except requests.exceptions.Timeout:
            return response(bot, 'Can not get results', chat_id)
        except RequestException:
            return response(bot, 'Can not get results')
        setattr(bot, 'img_last_response_{}'.format(chat_id), azure_response)
    else:
        azure_response = getattr(bot, 'img_last_response_{}'.format(chat_id))

    try:
        search_data = json.loads(azure_response.decode('utf-8'))
    except ValueError:
        return response(bot, 'Can not get results', chat_id)

    results = search_data.get('d', {}).get('results', [])
    if len(results) >= i + 1:
        while results[i - 1 if i > 1 else i:]:
            setattr(bot, 'img_last_num_{}'.format(chat_id), i)
            if len(results) <= i:
                return response(bot, 'No such images', chat_id)
            url = results[i]['MediaUrl']
            ext = url.rsplit('.', 1)[1]
            if ext.lower() in ('jpg', 'jpeg', 'gif', 'png'):
                file_id = check_store(bot, url)
                photo = file_id if file_id else prepare_binary_from_url(url)
                if photo:
                    break
            i += 1
        else:
            return response(bot, 'No such images', chat_id)

        data = {'chat_id': chat_id}
        if file_id:
            data.update(photo=file_id)
            files = None
        else:
            files = {'photo': ('file.{}'.format(ext), photo, results[i]['ContentType'])}

        # Send custom chat action
        bot.pre_send(chat_id=chat_id, action='upload_photo')

        telegram_response = bot.call(
            'sendPhoto',
            'POST',
            data=data,
            files=files
        )
        setattr(bot, 'img_last_time_{}'.format(chat_id), datetime.now())
        if telegram_response and telegram_response.get('photo') and not file_id and bot.store:
            bot.store.set(url, telegram_response['photo'][-1]['file_id'])
        elif not telegram_response or telegram_response.get('status_code') == 400:
            return "Telegram can't process the image"
    else:
        return response(bot, 'No such images', chat_id)

main.prevent_pre_send = True
