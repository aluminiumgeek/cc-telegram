import requests
import shutil
import uuid
from io import BytesIO

from requests.exceptions import RequestException


def prepare_binary_from_url(url, verify=True):
    try:
        content = requests.get(url, timeout=(1, 3), verify=verify).content
    except RequestException:
        pass
    else:
        return BytesIO(content)


def download_file(url, max_length=20 * 1024 * 1024, headers={}):
    try:
        length = requests.head(url).headers.get('content-length', 0)
        if int(length) > max_length:
            return
        r = requests.get(url, timeout=(1, 3), stream=True, headers=headers)
        ext = url.rsplit('.', 1)[1]
        file_name = '{}.{}'.format(uuid.uuid4(), ext)
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return file_name
    except RequestException:
        return
