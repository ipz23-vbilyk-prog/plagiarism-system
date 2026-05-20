import re


def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zа-я0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_shingles(text: str, n: int = 3):
    words = text.split()
    return [" ".join(words[i:i+n]) for i in range(len(words) - n + 1)]