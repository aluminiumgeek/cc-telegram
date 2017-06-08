import os
import re

from moviepy.editor import *

from modules.utils.data import download_file


def main(bot, message, update, *args, **kwargs):
    chat_id = kwargs.get('chat_id')
    message = message.strip()
    message_id = update.get('message', {}).get('message_id')
    for url in re.findall(r'http.*\.webm', message):
        file_id = bot.store.get(url)

        data = {
            'chat_id': chat_id,
            'reply_to_message_id': message_id,
            'disable_notification': True
        }

        if file_id:
            data.update(video=file_id)
            files = None
        else:
            file_name = download_file(url)
            if not file_name:
                return
            clip = VideoFileClip(file_name)
            clip_filename = '{}.mp4'.format(file_name)

            bot.pre_send(chat_id=chat_id, action='upload_video')

            clip.write_videofile(clip_filename, threads=4, preset='superfast', audio_codec='aac')

            data.update(width=clip.w, height=clip.h, duration=clip.duration)
            files = {'video': (clip_filename, open(clip_filename, 'rb'), 'video/mp4')}

        telegram_response = bot.call('sendVideo', 'POST', data=data, files=files)

        if telegram_response and telegram_response.get('video') and not file_id and bot.store:
            bot.store.set(url, telegram_response['video']['file_id'])

        if not file_id:
            os.remove(file_name)
            os.remove(clip_filename)

main.prevent_pre_send = True
