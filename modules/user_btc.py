import json

from modules.utils import http


async def main(bot, *args, **kwargs):
    """
    btc
    Get latest bitcoin price
    """
    tickers = [
        {'name': 'CEX.IO', 'url': 'https://cex.io/api/ticker/BTC/USD', 'field': 'last', 'sign': '$'},
        {'name': 'Bitstamp', 'url': 'https://www.bitstamp.net/api/v2/ticker/btcusd/', 'field': 'last', 'sign': '$'},
        {'name': 'BTC-E', 'url': 'https://btc-e.com/api/3/ticker/btc_usd', 'field': 'btc_usd.last', 'sign': '$'},
        {'name': 'BTC-E', 'url': 'https://btc-e.com/api/3/ticker/btc_rur', 'field': 'btc_rur.last', 'sign': '₽'}
    ]
    for ticker in tickers:
        try:
            response_body = await http.perform_request(ticker['url'], 'GET')
            response_json = json.loads(response_body)
        except:
            continue

        value = response_json
        for key in ticker['field'].split('.'):
            value = value.get(key, {})
        ticker['value'] = float(value) if value else None

    text = '\n'.join(['{}: {:.2f}{}'.format(t['name'], t['value'], t['sign']) for t in filter(lambda x: x.get('value'), tickers)])
    await http.send(bot, chat_id=kwargs.get('chat_id'), text=text, data={'disable_web_page_preview': True})
