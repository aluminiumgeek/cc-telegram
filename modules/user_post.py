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
    /post
    Post replayed message to channel
    """
    channel_id = getattr(bot.settings, 'channel_id', None)
    if not channel_id:
        return 'Module is not configured. You must set `channel_id` in settings'

    message = kwargs['update']['message']

    reply = message.get('reply_to_message', None)

    chat_id = message.get('peer_id')
    
    if reply is None:
        name = message_author(message)
        text = "{}: {}".format(name, args)
        data = {
            'chat_id': channel_id,
            'text': text
        }
        channel_message = bot.call('sendMessage', 'POST', data=data)
    else:
        name = message_author(reply)
        from_chat_id = reply.get('peer_id')
        reply_id = reply.get('id')
        data = {
            'from_chat_id': from_chat_id,
            'chat_id': channel_id,
            'message_id': reply_id
        }
        channel_message = bot.call('forwardMessage', 'POST', data=data)
    try:
        result = "https://t.me/c/{}/{}".format(channel_id, channel_message.get('id'))
    except Exception as e:
        result = "Polomkah: {}".format(e) 

    return result