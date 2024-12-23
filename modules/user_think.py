import json

from modules.utils import http


async def main(bot, *args, **kwargs):
    """
    think
    Use AI to think about it
    """
    try:
        url = 'https://api.openai.com/v1/chat/completions'
        system_prompt = "Think about it"
        message = kwargs['update']['message']
        reply = message.get('reply_to_message', None)
        if reply is None:
            return 'Nothing to think about'
        prompt = reply.get('text', '')
        openai_api_key = getattr(bot.settings, 'open_ai_api_key', None)
        headers = {
            'Authorization': f'Bearer {openai_api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'gpt-4o-mini',
            'messages': [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': prompt}],
            'temperature': 0.6,
            'presence_penalty': 0.5,
            'frequency_penalty': 0.5,
            'max_tokens': 400
        }
        response_body = await http.perform_request(url, 'POST', headers=headers, data=json.dumps(data))
        response_json = json.loads(response_body)
        result = response_json['choices'][0]['message']['content']
    except Exception as e:
        result = "Polomkah: {}".format(e)

    return result


