from modules.utils import http
import json

async def main(bot, *args, **kwargs):
    """
    think
    Use AI to think about it
    """
    try:
        url = 'https://api.openai.com/v1/chat/completions'
        system_prompt = "Think about it"
        prompt = kwargs['update']['message']
        openai_api_key = getattr(bot.settings, 'open_ai_api_key', None)
        headers = {
            'Authorization': f'Bearer {openai_api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'gpt-4o',
            'messages': [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': prompt}],
            'temperature': 0.6,
            'presence_penalty': 0.5,
            'frequency_penalty': 0.5,
            'max_tokens': 1500
        }
        response_body = http.perform_request(url, 'POST', headers=headers, data=json.dumps(data))
        response_json = json.loads(response_body)
        result = response_json['choices'][0]['message']['content']
    except Exception as e:
        result = "Polomkah: {}".format(e)

    return result


