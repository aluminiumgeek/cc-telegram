import wolframalpha

def main(bot, *args, **kwargs):
    """
    wa <query>
    Send query to Wolfram|Alpha.
    See also: g, w, img
    """

    chat_id = kwargs.get('chat_id')
    app_id = getattr(bot.settings, 'wa_app_id', None)
    if not app_id:
        return 'Module is not configured. You must set `wa_app_id` in settings'
    client = wolframalpha.Client(app_id)

    query = ' '.join(args)
    if not query:
        return 'Invalid syntax'
    res = client.query(query)
    result = []
    pods = getattr(res, 'pods', None)
    if not pods:
        return 'No results'
    for pod in res.pods:
        title = getattr(pod, 'title', None)
        if not title:
            continue
        result.append('<b>{}</b>'.format(title))
        for sub in pod.subpods:
            text = sub.get('plaintext')
            if not text:
                continue
            result.append('    {}'.format(text.replace('\n', '\n    ')))

    bot.send(chat_id=kwargs.get('chat_id'), text='\n'.join(result), data={'disable_web_page_preview': True, 'parse_mode': 'HTML'})
