RB = {
    u'А': u'⠁',
    u'Б': u'⠃',
    u'В': u'⠺',
    u'Г': u'⠛',
    u'Д': u'⠙',
    u'Е': u'⠑',
    u'Ё': u'⠡',
    u'Ж': u'⠚',
    u'З': u'⠵',
    u'И': u'⠊',
    u'Й': u'⠯',
    u'К': u'⠅',
    u'Л': u'⠇',
    u'М': u'⠍',
    u'Н': u'⠝',
    u'О': u'⠕',
    u'П': u'⠏',
    u'Р': u'⠗',
    u'С': u'⠎',
    u'Т': u'⠞',
    u'У': u'⠥',
    u'Ф': u'⠋',
    u'Х': u'⠓',
    u'Ц': u'⠉',
    u'Ч': u'⠟',
    u'Ш': u'⠱',
    u'Щ': u'⠭',
    u'Ъ': u'⠷',
    u'Ы': u'⠮',
    u'Ь': u'⠾',
    u'Э': u'⠪',
    u'Ю': u'⠳',
    u'Я': u'⠫',
    u'A': u'⠁',
    u'B': u'⠃',
    u'C': u'⠉',
    u'D': u'⠙',
    u'E': u'⠑',
    u'F': u'⠋',
    u'G': u'⠛',
    u'H': u'⠓',
    u'I': u'⠊',
    u'J': u'⠚',
    u'K': u'⠅',
    u'L': u'⠇',
    u'M': u'⠍',
    u'N': u'⠝',
    u'O': u'⠕',
    u'P': u'⠏',
    u'Q': u'⠟',
    u'R': u'⠗',
    u'S': u'⠎',
    u'T': u'⠞',
    u'U': u'⠥',
    u'V': u'⠧',
    u'W': u'⠺',
    u'X': u'⠭',
    u'Y': u'⠽',
    u'Z': u'⠵',
    u'#': u'⠼',
    u'.': u'⠲',
    u',': u'⠂',
    u'?': u'⠢',
    u';': u'⠆',
    u'-': u'⠤',
    u'—': u'⠤',
    u'−': u'⠤',
    ' ': ' '
}


async def main(bot, *args, **kwargs):
    """
    rb <text>
    Text to Braille converter
    See also: br
    """
    if not args:
        return
    else:
        text = ' '.join(args)

        result = ''
        for letter in text:
            if letter.upper() in RB:
                result += RB[letter.upper()]
            else:
                result += letter

        return result
