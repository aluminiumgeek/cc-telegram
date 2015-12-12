from io import BytesIO
import requests


def prepare_binary_from_url(url):
    content = requests.get(url).content
    return BytesIO(content)
