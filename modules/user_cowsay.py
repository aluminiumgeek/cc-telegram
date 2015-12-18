import subprocess

from modules.utils.text import clean_text


def main(bot, *args):
    """
    cowsay <text>
    Speaking cow
    """

    text = clean_text(' '.join(args))
    if not text.strip() or not list(filter(lambda x: not x.startswith('-'), text.split())):
        return

    process = subprocess.Popen(
        u'cowsay {}'.format(text),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    output, error = process.communicate()
    if output or error:
        bot.send(text='```{}```'.format(output if output else error), data={'parse_mode': 'Markdown'})
