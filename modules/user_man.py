
def main(bot, module):
    """
    man <module>
    Show manual page for a module
    """

    if module in bot.commands['user']:
        result = bot.commands['user'][module].__doc__
    elif module in bot.commands['owner']:
        result = bot.commands['owner'][module].__doc__
    else:
        result = 'No such command'

    return result or 'No manual entry for `{}`'.format(module)
