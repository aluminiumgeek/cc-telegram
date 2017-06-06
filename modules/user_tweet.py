import twitter


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

    if reply is None:
    	text = ' '.join(args)
    elif reply.get('text'):
    	message_from = reply['from']
    	first_name = message_from.get('first_name', '')
    	last_name = message_from.get('last_name', '')
    	name = '{} {}'.format(first_name, last_name).strip()
    	if not name:
		    name = message_from.get('username', message_from.get('id'))
    	text = "{}: {}".format(name, reply['text'])
    else:
    	return
    tweet = api.PostUpdate(text)
    screen_name = tweet.user.screen_name
    result  = "https://twitter.com/{}/status/{}".format(screen_name,tweet.id_str)

    return result