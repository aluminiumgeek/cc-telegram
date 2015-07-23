# C.C. - telegram bot

import sys
import os
os.chdir(sys.path[0])

import settings
from telegram import Bot


def main():
    bot = Bot(settings.token)
    bot.start()


def help():
    help = ('Usage: %s [-d|-h|--help]' % sys.argv[0]) +\
        '\n\n' +\
        '-d         daemon\n' +\
        '-h, --help help'
    print(help)
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            help()

        elif sys.argv[1] == '-d':
            logfile = 'bot.log'

            pid = os.fork()
            if pid == 0:
                os.setsid()
                pid = os.fork()
                if pid == 0:
                    main()
        else:
            help()
    else:
        main()
