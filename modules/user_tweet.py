import twitter

from modules.utils.data import prepare_binary_from_url


def message_author(reply):
    message_from = reply['from']
    first_name = message_from.get('first_name', '')
    last_name = message_from.get('last_name', '')
    name = '{} {}'.format(first_name, last_name).strip()
    if not name:
        name = message_from.get('username', message_from.get('id'))	
    return name


def main(bot, *args, **kwargs):
    """
    /tweet
    Post replayed message to twitter
    """
    twitter_options = getattr(bot.settings, 'twitter_keys', None)
    if not twitter_options:
        return 'Module is not configured. You must set `twitter_keys` in settings'
    api = getattr(bot, 'twitter_api', None)
    if api is None:
        api = bot.twitter_api = twitter.Api(
            consumer_key=twitter_options['consumer_key'],
            consumer_secret=twitter_options['consumer_secret'],
            access_token_key=twitter_options['access_token_key'],
            access_token_secret=twitter_options['access_token_secret']
        )

    message = kwargs['update']['message']

    reply = message.get('reply_to_message', None)

    media = None
    
    if reply is None:
        text = ' '.join(args)
    elif reply.get('photo'):
        file = reply.get('photo')[-1]
        file_id = file['file_id']
        data = {'file_id': file_id}
        file_info = bot.call(
            'getFile', 
            'GET', 
            data=data
        )
        file_path = file_info.get('file_path')
        file_url = "https://api.telegram.org/file/bot{}/{}".format(bot.settings.token, file_path)
        media = prepare_binary_from_url(file_url)
        # Hacking for compatibility
        setattr(media, 'mode', 'rb')
        setattr(media, 'name', 'tmp_file.jpg')
        text = message_author(reply)
        if reply.get('text'):
            text = '{}: {}'.format(text, reply['text'])
    elif reply.get('text'):
        name = message_author(reply)
        text = "{}: {}".format(name, reply['text'])
    else:
        return
    try:
        tweet = api.PostUpdate(text, media)
        screen_name = tweet.user.screen_name
        result = "https://twitter.com/{}/status/{}".format(screen_name, tweet.id_str)
    except twitter.error.TwitterError as e:
        result = "Some problem with your tweet: {}".format(e.message)
    except Exception as e:
        result = "Polomkah: {}".format(e) 

    return result