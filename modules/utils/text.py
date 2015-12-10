import re


def clean_text(text):
    return re.sub('[^a-zA-Z0-9-_,\. ]', '', text)
