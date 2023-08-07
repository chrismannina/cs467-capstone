import re


def remove_non_ascii(text):
    return re.sub(r"[^\x00-\x7F]+", " ", text)
