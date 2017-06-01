import json
import random
import sys
import re

from modules.utils import http


async def main(bot, *args, **kwargs):
    """
    btc
    Get latest bitcoin price
    """
    news_id = random.randint(3,9524)
    try:
        response_body = await http.perform_request("http://breakingmad.me/ru/%(news_id)s.json"%locals(), 'GET')
        response_json = json.loads(response_body)
    except:
        print("Unexpected error:", sys.exc_info()[0])



    value = response_json[0]
    title = value['title']
    text = re.sub(r'(\[url="(.+)"\])(.+)(\[\/url\])',r'\3',value['text'])
    print('text')


    text = "*%(title)s* \n\n %(text)s"%locals()
    await http.send(bot, chat_id=kwargs.get('chat_id'), text=text, data={'disable_web_page_preview': True, 'parse_mode': 'Markdown'})
