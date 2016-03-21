
def main(bot, *args, **kwargs):
    """
    echo <text>
    Echoes input text
    """
    bot.send(chat_id=kwargs.get('chat_id'), text=' '.join(args))
