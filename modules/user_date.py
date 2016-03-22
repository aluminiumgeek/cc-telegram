from datetime import datetime


async def main(bot, *args, **kwargs):
    """
    date
    Current datetime

    date <username>
    Date someone
    """

    if args:
        return 'обдумав свои чувства, пригласил на свидание {}'.format(' '.join(args))
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
