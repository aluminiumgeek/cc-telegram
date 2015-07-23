import os
import sys
import time
import imp
import logging
import json

import requests

import settings

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Bot:

    def __init__(self, token):
        self.token = token
        self.update_id = 0

        self.load()

    def load(self):
        """
        load
        Load all modules.
        See also: modprobe, rmmod, lsmod
        """

        self.userCommands = {}
        self.ownerCommands = {
            'load': self.load,
            'modprobe': self.modprobe,
            'rmmod': self.rmmod
        }

        for file in os.listdir('modules'):
            if file.endswith('.py') and (file.startswith('user_') or file.startswith('owner_')):
                pos = file.index('_') + 1
                self.modprobe(self, file[pos:-3])

    def modprobe(self, bot, *args):
        """
        modprobe <module>
        Load module.
        See also: load, rmmod, lsmod
        """

        if len(args) != 1:
            return

        name1 = 'modules/user_%s' % args[0]
        name2 = 'modules/owner_%s' % args[0]

        user = None
        try:
            file, pathname, description = imp.find_module(name1)
            user = True
            name = name1
        except:
            try:
                file, pathname, description = imp.find_module(name2)
                name = name2
            except:
                error = 'MODULE: %s not found' % args[0]
                logging.error(error)
                return error

        try:
            method = imp.load_module(name, file, pathname, description).main
        except Exception as e:
            error = 'MODULE: can\'t load %s' % args[0]
            logging.error(e)
            return error
        else:
            if user:
                self.userCommands[args[0]] = method
            else:
                self.ownerCommands[args[0]] = method

        info = 'MODULE: %s loaded' % args[0]
        logging.info(info)
        return info

    def rmmod(self, bot, *args):
        """
        rmmod <module>
        Remove module.
        See also: load, modprobe, lsmod
        """

        if len(args) != 1:
            return

        if args[0] == 'load' or args[0] == 'modprobe' or args[0] == 'rmmod':
            return 'MODULE: can\'t remove %s' % args[0]

        if args[0] in self.userCommands:
            del self.userCommands[args[0]]
        elif args[0] in self.ownerCommands:
            del self.ownerCommands[args[0]]
        else:
            return 'MODULE: %s not loaded' % args[0]

        info = 'MODULE: %s removed' % args[0]
        logging.info(info)
        return info

    def start(self):
        while True:
            updates = self.get_updates()
            logging.debug(updates)
            for update in updates:
                self.process(update)

            #time.sleep(getattr(settings, 'UPDATE_INTERVAL', 1))

    def process(self, update):
        """
        Process an update
        """

        if 'message' in update and 'text' in update['message'] and update['message']['text'].startswith('/'):
            text = update['message']['text'].lstrip('/')
            prefix = None
            error = False

            # Some user have been highlighted
            if ' > ' in text:
                text, prefix = text.split(' > ', 1)
                if not prefix.startswith('@') and prefix:
                    prefix = '@' + prefix

            cmd, *args = text.split()
            self.chat_id = self._get_chat_id(update)
            result = None

            self.pre_send()

            if cmd in self.userCommands:
                try:
                    result = self.userCommands[cmd](self, *args)
                except TypeError as e:
                    if 'positional argument' in str(e):
                        result = 'wrong parameters'
                        error = True
                    else:
                        raise
            elif cmd in self.ownerCommands:
                if self._is_owner(update):
                    try:
                        result = self.ownerCommands[cmd](self, *args)
                    except TypeError as e:
                        if 'positional argument' in str(e):
                            result = 'wrong parameters'
                            error = True
                        else:
                            raise
                else:
                    result = '{}: access denied'.format(cmd)
                    error = True
            else:
                result = 'Command not found: {}'.format(cmd)
                error = True

            if result is not None:
                if prefix and not error:
                    result = '{}, {}'.format(prefix, result)
                self.send(self.chat_id, text=result)

    def pre_send(self, chat_id=None, action='typing'):
        """
        Pre send hook. Send 'typing...' or another chat action 
        """

        data = {
            'chat_id': chat_id if chat_id is not None else self.chat_id,
            'action': action
        }
        self.call('sendChatAction', 'POST', data=data)

    def send(self, chat_id=None, text=None, data={}):
        """
        Send message to a chat
        """

        if text is not None:
            data = {
                'chat_id': chat_id if chat_id is not None else self.chat_id,
                'text': text
            }
            logging.debug('Sending: {}'.format(data))
            self.call('sendMessage', 'POST', data=data)

    def get_updates(self):
        """
        Get updates from telegram
        """

        updates = self.call('getUpdates', 'GET', params={
                            'timeout': getattr(settings, 'updates_timeout', 60), 'offset': self.update_id})
        if updates:
            self.update_id = updates[-1]['update_id'] + 1
        return updates

    def call(self, method_name, http_method, **kwargs):
        """
        Call a Telegram API method
        """

        uri = 'https://api.telegram.org/bot{}/{}'.format(
            self.token, method_name)
        resp = requests.request(http_method, uri, **kwargs)
        content = json.loads(resp.content.decode('utf-8'))

        if content['ok']:
            return content['result']
        else:
            logging.error(resp.content)

    def _is_owner(self, update):
        return update.get('message', {}).get('from', {}).get('username', '') == settings.owner

    def _get_chat_id(self, update):
        return update.get('message', {}).get('chat', {}).get('id', None)
