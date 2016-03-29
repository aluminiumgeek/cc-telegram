RU_BR = {
    u'⠁': u'А',
    u'⠃': u'Б',
    u'⠺': u'В',
    u'⠛': u'Г',
    u'⠙': u'Д',
    u'⠑': u'Е',
    u'⠡': u'Ё',
    u'⠚': u'Ж',
    u'⠵': u'З',
    u'⠊': u'И',
    u'⠯': u'Й',
    u'⠅': u'К',
    u'⠇': u'Л',
    u'⠍': u'М',
    u'⠝': u'Н',
    u'⠕': u'О',
    u'⠏': u'П',
    u'⠗': u'Р',
    u'⠎': u'С',
    u'⠞': u'Т',
    u'⠥': u'У',
    u'⠋': u'Ф',
    u'⠓': u'Х',
    u'⠉': u'Ц',
    u'⠟': u'Ч',
    u'⠱': u'Ш',
    u'⠭': u'Щ',
    u'⠷': u'Ъ',
    u'⠮': u'Ы',
    u'⠾': u'Ь',
    u'⠪': u'Э',
    u'⠳': u'Ю',
    u'⠫': u'Я'
}

EN_BR = {
    u'⠁': u'A',
    u'⠃': u'B',
    u'⠉': u'C',
    u'⠙': u'D',
    u'⠑': u'E',
    u'⠋': u'F',
    u'⠛': u'G',
    u'⠓': u'H',
    u'⠊': u'I',
    u'⠚': u'J',
    u'⠅': u'K',
    u'⠇': u'L',
    u'⠍': u'M',
    u'⠝': u'N',
    u'⠕': u'O',
    u'⠏': u'P',
    u'⠟': u'Q',
    u'⠗': u'R',
    u'⠎': u'S',
    u'⠞': u'T',
    u'⠥': u'U',
    u'⠧': u'V',
    u'⠺': u'W',
    u'⠭': u'X',
    u'⠽': u'Y',
    u'⠵': u'Z'
}

SIGNS_BR = {
    u'⠼': u'#',
    u'⠲': u'.',
    u'⠂': u',',
    u'⠢': u'?',
    u'⠆': u';',
    u'⠤': u'-',
    u'⠤': u'—',
    u'⠤': u'−',
    ' ': ' '
}


async def main(bot, *args, **kwargs):
    """
    br [lang] <text>
    Braille to text converter
    Available languages: ru en
    Default language: ru
    See also: rb
    """
    if not args:
        return
    else:
        braille_table = RU_BR
        args = list(args)
        if args[0] == 'en': 
            braille_table = EN_BR
            del args[0]
        elif args[0] == 'ru':
            del args[0]
        
        text = ' '.join(args)
        
        result = ''
        for braille in text:
            if braille in braille_table:
                result += braille_table[braille].lower()
            elif braille in SIGNS_BR:
                result += SIGNS_BR[braille]
            else:
                result += braille
            
        return result
