from datetime import datetime


def main(bot, *args):
    """
    date
    Current datetime

    date <username>
    Date someone
    """

    if args:
        return 'обдумав свои чувства, пригласил на свидание {}'.format(' '.join(args))
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
