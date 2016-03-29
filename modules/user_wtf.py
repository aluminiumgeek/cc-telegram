import json
import requests


def main(bot, *args, **kwargs):
    """
    wtf [text]
    Detect language of a text or show avialable languages if no text given.
    See also: tr
    """

    mashape_key = getattr(bot.settings, 'mashape_key', None)
    if not mashape_key:
        return 'Mashape key is not provided'
    return detect_lang(' '.join(args), mashape_key)


def detect_lang(text, mashape_key):
    google_langs =\
        { 'af':'Afrikaans','sq':'Albanian','am':'Amharic','ar':'Arabic','hy':'Armenian','az':'Azerbaijani','eu':'Basque'
        , 'be':'Belarusian','bn':'Bengali','bh':'Bihari','bg':'Bulgarian','my':'Burmese','ca':'Catalan','chr':'Cherokee'
        , 'zh':'Chinese','zh-CN':'Chinese_simplified','zh-TW':'Chinese_traditional','hr':'Croatian','cs':'Czech','da':'Danish'
        , 'dv':'Dhivehi','nl':'Dutch','en':'English','eo':'Esperanto','et':'Estonian','tl':'Filipino','fi':'Finnish'
        , 'fr':'French','gl':'Galician','ka':'Georgian','de':'German','el':'Greek','gn':'Guarani','gu':'Gujarati','iw':'Hebrew'
        , 'hi':'Hindi','hu':'Hungarian','is':'Icelandic','id':'Indonesian','iu':'Inuktitut','it':'Italian','ja':'Japanese'
        , 'kn':'Kannada','kk':'Kazakh','km':'Khmer','ko':'Korean','ku':'Kurdish','ky':'Kyrgyz','lo':'Laothian','lv':'Latvian'
        , 'lt':'Lithuanian','mk':'Macedonian','ms':'Malay','ml':'Malayalam','mt':'Maltese','mr':'Marathi','mn':'Mongolian'
        , 'ne':'Nepali','no':'Norwegian','or':'Oriya','ps':'Pashto','fa':'Persian','pl':'Polish','pt-PT':'Portuguese'
        , 'pa':'Punjabi','ro':'Romanian','ru':'Russian','sa':'Sanskrit','sr':'Serbian','sd':'Sindhi','si':'Sinhalese'
        , 'sk':'Slovak','sl':'Slovenian','es':'Spanish','sw':'Swahili','sv':'Swedish','tg':'Tajik','ta':'Tamil','tl':'Tagalog'
        , 'te':'Telugu','th':'Thai','bo':'Tibetan','tr':'Turkish','uk':'Ukrainian','ur':'Urdu','uz':'Uzbek','ug':'Uighur','vi':'Vietnamese'
        }

    if not text:
        return ", ".join(["%s (%s)" %(v, k) for k, v in google_langs.items()])

    headers = {'X-Mashape-Key': mashape_key}
    data = requests.get('https://langdetect.p.mashape.com/language?mode=json&text=%s' % (text), headers=headers).content.decode('utf-8')
    if not data:
        return "Can't get data"
    try:
        data = json.loads(data)
        probes = filter(lambda x: x['code'] != '?', data['probs'])
        probes = map(lambda x: '%s (%.4f)' % (x['code'], x['score']), probes)
        return 'Lang: {}\nProbabilities: {}'.format(data['lang'], ', '.join(probes))
    except:
        return "Can't detect this shit!"
