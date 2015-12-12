#!/usr/bin/env python3
# C.C. - telegram bot

import importlib
import sys
import os
from optparse import OptionParser
os.chdir(sys.path[0])

from telegram import Bot


def main(settings_module):
    settings = importlib.import_module(settings_module)
    bot = Bot(settings)
    bot.start()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-d', '--daemon', action='store_true', dest='daemon', default=False, help='Run in background')
    parser.add_option('-s', '--settings', dest='settings', default='settings', help='Settings module')
    options, _ = parser.parse_args()

    if options.daemon:
        pid = os.fork()
        if pid == 0:
            os.setsid()
            pid = os.fork()
            if pid == 0:
                main(options.settings)
    else:
        main(options.settings)
