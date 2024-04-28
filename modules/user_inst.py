import os
import re
import time

from modules.utils import http
from instascrape import Reel


async def main(bot, *args, **kwargs):
    """
    inst <Reel URL>
    Get reels media by link
    """
    file_path = None
    try:
        inst_options = getattr(bot.settings, 'inst_keys', None)
        if not inst_options:
            return 'Module is not configured. You must set `inst_keys` in settings'
        # session id
        SESSIONID = inst_options['sessionid']
        
        # Header with session id
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 \
            Safari/537.36 Edg/79.0.309.43",
            "cookie": f'sessionid={SESSIONID};'
        }

        url = args[0] if args else None
        if not url or not re.match(r'^https://(www\.)?instagram.com/', url):
            return 'Nothing to download'

        # Passing Instagram reel link as argument in Reel Module
        insta_reel = Reel(url)

        chat_id = kwargs.get('chat_id')
        bot.pre_send(chat_id=chat_id, action='upload_video')

        # Using  scrape function and passing the headers
        insta_reel.scrape(headers=headers)
        
        file_path = f"./tmp/reel{int(time.time())}.mp4"
        # Giving path where we want to download reel to the 
        # download function
        insta_reel.download(fp=file_path)
        
        files = {'video': (file_path, open(file_path, 'rb'), 'video/mp4')}
        data = {'chat_id': chat_id, 'disable_notification': True}
        telegram_response = bot.call('sendVideo', 'POST', data=data, files=files)
    except Exception as e:
        return f"Polomkah: {e}"
    finally:
        file_path and os.path.exists(file_path) os.remove(file_path)
