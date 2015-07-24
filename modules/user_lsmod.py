
def main(bot, *args):
    """
    lsmod
    Show loaded modules.
    See also: load, modprobe, rmmod
    """

    return 'Available\nuser: {}\nowner: {}'.format(' '.join(bot.commands['user']), ' '.join(bot.commands['owner']))
