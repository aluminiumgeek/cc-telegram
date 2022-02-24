from modules.utils import http
from lxml import html

async def main(bot, *args, **kwargs):
    """
    usd
    Get latest USD/RUB quote
    """
    try:
        url = 'https://ru.investing.com/currencies/usd-rub'
        response_body = await http.perform_request(url, 'GET')
        tree = html.fromstring(response_body)
        quote = tree.xpath('//span[@class="text-2xl"]/text()')[0]
        result = "{} ₽".format(quote)
    except Exception as e:
        result = "Polomkah: {}".format(e)

    return result
