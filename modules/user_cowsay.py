import os

from modules.utils.text import clean_text


def main(bot, *args):
    """
    cowsay [text]
    Speaking cow
    """

    text = clean_text(' '.join(args))
    process = os.popen(u'cowsay {}'.format(text))
    bot.send(text='```{}```'.format(process.read()), data={'parse_mode': 'Markdown'})
    process.close()
