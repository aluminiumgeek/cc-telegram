from modules.utils import http
import json

async def main(bot, *args, **kwargs):
    """
    usd
    Get latest USD/RUB quote
    """
    try:
        url = 'https://api.tinkoff.ru/v1/currency_rates?from=USD&to=RUB'
        response_body = await http.perform_request(url, 'GET')
        response_json = json.loads(response_body)
        quote = response_json['payload']['rates'][0]['sell']
        result = "{} ₽".format(quote)
    except Exception as e:
        result = "Polomkah: {}".format(e)

    return result
