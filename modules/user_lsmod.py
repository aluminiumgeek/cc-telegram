
def main(bot, *args):
    """
    lsmod
    Show loaded modules.
    See also: load, modprobe, rmmod
    """

    return 'Available commands\nuser: ' + ' '.join(bot.userCommands) + '\nowner: ' + ' '.join(bot.ownerCommands)
