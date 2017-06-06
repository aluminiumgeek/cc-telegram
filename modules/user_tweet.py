import twitter
import pprint

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
    	api = bot.twitter_api = twitter.Api(consumer_key=twitter_options['consumer_key'],
      		  				                consumer_secret=twitter_options['consumer_secret'],
      		  				                access_token_key=twitter_options['access_token_key'],
  			  				                access_token_secret=twitter_options['access_token_secret'])

    message = kwargs['update']['message']

    reply = message.get('reply_to_message', None)

    if reply is None:
    	tweet = api.PostUpdate(' '.join(args))
    else:
    	message_from = reply['from']
    	first_name = message_from.get('first_name','')
    	last_name = message_from.get('last_name','')
    	text = first_name 
    	if last_name:
    		text += ' '+last_name
    	text += ': ' + reply['text']

    	tweet = api.PostUpdate(text)

    result  = 'https://twitter.com/JabrachOfficial/status/'+tweet.id_str

    bot.send(chat_id=kwargs.get('chat_id'), text=result, data={})