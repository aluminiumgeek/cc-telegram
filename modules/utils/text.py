import re


def clean_text(text):
    return re.sub('[^\w\d_,\. -]', '', text, flags=re.UNICODE)
