
def main(bot, module=None, **kwargs):
    """
    man <module>
    Show manual page for a module
    """

    if module in bot.commands['user']:
        result = bot.commands['user'][module].__doc__
    elif module in bot.commands['owner']:
        result = bot.commands['owner'][module].__doc__
    elif module is None:
        return 'What manual page do you want?'
    else:
        return 'No such command'

    result = result or 'No manual entry for `{}`'.format(module)
    bot.send(chat_id=kwargs.get('chat_id'), text=result, data={'disable_web_page_preview': True})
