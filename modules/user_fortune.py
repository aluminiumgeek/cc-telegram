import os
import random


def main(bot, *args, **kwargs):
    """
    fortune
    Print a random, hopefully interesting, adage
    """

    fortunes_path = '/usr/share/games/fortunes/'

    try:
        types = filter(lambda x: not x.endswith('.dat'), os.listdir(fortunes_path))
    except OSError:
        return 'Package `fortunes` is not installed in your system. Run `aptitude install fortunes`'

    fortune_file = random.choice(list(types))
    with open(os.path.join(fortunes_path, fortune_file)) as fortune_file:
        data = fortune_file.read()
        quotes = data.split('%\n')
        return random.choice(quotes)
