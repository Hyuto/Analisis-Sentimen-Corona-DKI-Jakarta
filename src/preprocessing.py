"""Preprocessing modul yang berfungsi untuk menampung semua proses preprocessing data teks"""

import re
import string
import unicodedata

from indoNLP.preprocessing import (
    emoji_to_words,
    remove_html,
    remove_url,
    replace_slang,
    replace_word_elongation,
)
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

STEMMER = StemmerFactory().create_stemmer()


def preprocessing(text: str) -> str:
    """Preprocessing raw text

    Args:
        text (str): Raw text.

    Returns:
        str: Cleaned text.
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text, flags=re.UNICODE)  # remove whitespace
    text = emoji_to_words(text)  # remove emoji
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = remove_html(text)  # remove html tags
    text = remove_url(text)  # remove url
    text = replace_word_elongation(text)  # replace WE
    text = replace_slang(text)  # replace slang words
    # text = remove_stopwords(text)
    text = text.translate(str.maketrans("", "", string.digits))  # remove numbers
    text = text.translate(
        str.maketrans(string.punctuation, " " * len(string.punctuation))
    )  # remove punctuation
    text = " ".join(text.split())
    text = STEMMER.stem(text)
    return " ".join(text.split())
