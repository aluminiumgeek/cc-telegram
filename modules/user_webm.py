import os
import re
import time

from moviepy.editor import *
import requests

from modules.utils.data import download_file


def main(bot, *args, **kwargs):
    """
    webm
    Return random webm from csgoanime.
    See also: img
    """
    last_dt = bot.store.get('webm_dt')
    if last_dt is not None and float(last_dt.decode()) > time.time() - 60:
        return 'Let me get some rest.'
    bot.store.set('webm_dt', time.time())

    chat_id = kwargs.get('chat_id')
    resp = requests.get('http://csgoani.me')
    if resp.status_code != 200:
        return 'Error getting data'

    urls = re.findall(r'http.*\.webm', resp.content.decode())
    print(urls)
    if not urls:
        return 'Error getting data'
    url = urls[0]
    file_id = bot.store.get(url)
    data = {'chat_id': chat_id, 'disable_notification': True}
    if file_id:
        data.update(video=file_id)
        files = None
    else:
        file_name = download_file(url, headers={'Referer': resp.url})
        if not file_name:
            return 'Error processing data'

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
