
def main(bot, *args):
    """
    echo [text]
    Echoes input text
    """

    bot.send(text=' '.join(args))
