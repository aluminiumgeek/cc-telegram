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
    Post messages to some channel
    """
    channel_id = getattr(bot.settings, 'channel_id', None)
    if not channel_id:
        return 'Module is not configured. You must set `channel_id` in settings'

    message = kwargs['update']['message']

    reply = message.get('reply_to_message', None)
   
    if reply is None:
        name = message_author(message)
        text = "{}: {}".format(name, ' '.join(args))
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
            'from_chat_id': reply.get('chat').get('id'),
            'chat_id': channel_id,
            'message_id': reply.get('message_id')
        }
        channel_message = bot.call('forwardMessage', 'POST', data=data)

    try:
        result = "https://t.me/c/{}/{}".format(channel_id[4:], channel_message.get('message_id'))
    except Exception as e:
        result = "Polomkah: {}".format(e) 

    return result
