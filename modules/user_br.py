RU_BR = {
    '⠁': 'А',
    '⠃': 'Б',
    '⠺': 'В',
    '⠛': 'Г',
    '⠙': 'Д',
    '⠑': 'Е',
    '⠡': 'Ё',
    '⠚': 'Ж',
    '⠵': 'З',
    '⠊': 'И',
    '⠯': 'Й',
    '⠅': 'К',
    '⠇': 'Л',
    '⠍': 'М',
    '⠝': 'Н',
    '⠕': 'О',
    '⠏': 'П',
    '⠗': 'Р',
    '⠎': 'С',
    '⠞': 'Т',
    '⠥': 'У',
    '⠋': 'Ф',
    '⠓': 'Х',
    '⠉': 'Ц',
    '⠟': 'Ч',
    '⠱': 'Ш',
    '⠭': 'Щ',
    '⠷': 'Ъ',
    '⠮': 'Ы',
    '⠾': 'Ь',
    '⠪': 'Э',
    '⠳': 'Ю',
    '⠫': 'Я'
}

EN_BR = {
    '⠁': 'A',
    '⠃': 'B',
    '⠉': 'C',
    '⠙': 'D',
    '⠑': 'E',
    '⠋': 'F',
    '⠛': 'G',
    '⠓': 'H',
    '⠊': 'I',
    '⠚': 'J',
    '⠅': 'K',
    '⠇': 'L',
    '⠍': 'M',
    '⠝': 'N',
    '⠕': 'O',
    '⠏': 'P',
    '⠟': 'Q',
    '⠗': 'R',
    '⠎': 'S',
    '⠞': 'T',
    '⠥': 'U',
    '⠧': 'V',
    '⠺': 'W',
    '⠭': 'X',
    '⠽': 'Y',
    '⠵': 'Z'
}

SIGNS_BR = {
    '⠼': '#',
    '⠲': '.',
    '⠂': ',',
    '⠢': '?',
    '⠆': ';',
    '⠤': '-',
    '⠤': '—',
    '⠤': '−',
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
