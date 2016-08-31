import hashlib
from modules.utils import http


async def main(bot, *args, **kwargs):
    update = kwargs.get('update', {})
    message_id = update.get('message', {}).get('message_id')
    # message_id is always even for one-to-one chats and odd for group chats, so let's calculate hash instead of returning raw value
    roll_id = int(hashlib.sha1(str(message_id).encode('utf-8')).hexdigest(), 16) % (10 ** 8)
    await http.send(bot, chat_id=kwargs.get('chat_id'), text=str(roll_id), data={'reply_to_message_id': message_id})
