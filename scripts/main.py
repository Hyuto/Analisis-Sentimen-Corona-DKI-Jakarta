import argparse
import os
import pickle
import re
import string
from datetime import datetime

import tweepy
from pandas import DataFrame
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from utils import CONFIG


STEMMER = StemmerFactory().create_stemmer()
with open("kamus/Stopword.txt", "r") as f:
    STOPWORDS = f.readline().split()

# Preprocessor
def preprocessing(text):
    # Convert to lower case
    text = text.lower()
    text = " ".join(text.split())
    # Convert www.* or https?://* to URL
    text = re.sub("((www\.[^\s]+)|(https?://[^\s]+))", "", text)
    # Convert @username to AT_USER
    text = re.sub("@[^\s]+", "", text)
    # Remove additional white spaces
    text = re.sub("[\s]+", " ", text)
    # Replace #word with word
    text = re.sub(r"#([^\s]+)", r"\1", text)
    # Menghapus angka dari teks
    text = re.sub(r"\d+", "", text)
    # Menganti tanda baca dengan spasi
    text = text.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    return text


# Tokenizer
def tokenizer(text):
    words = word_tokenize(text)
    tokens = [STEMMER.stem(w.lower()) for w in words if len(w) > 3 and w not in stopwords]
    return " ".join(tokens)


# Load saved vectorizer
vectorizer_tfidf = pickle.load(open(config["VECTORIZER"]["path"], "rb"))

# Load Model
model = pickle.load(open(config["MODEL"]["path"], "rb"))

# Label dictionary
label = {0: "Negatif", 1: "Netral", 2: "Positif"}


def analyst(string):
    """Analyst"""
    string = [tokenizer(preprocessor(cleaning(string)))]
    string = vectorizer_tfidf.transform(string)

    return label[model.predict(string)[0]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="main script untuk sentiment analisis \
                                                  tweet terbaru mengenai corona"
    )
    parser.add_argument(
        "-n", "--number", help="Banyak tweet yang akan di crawl.", type=int, required=True
    )
    parser.add_argument("-e", "--export", help="Notasi export", action="store_true")
    args = parser.parse_args()

    
        s = analyst(tweet.full_text)
        tweetan.append(tweet.full_text)
        sentimen.append(s)

        # Logging
        text = tweet.full_text
        if len(text) > 65:
            text = text[:65] + "..."
        print(f"{len(sentimen)} : {repr(text)} : {s}")

    # Export
    if args.export:
        if not os.path.isdir("output"):
            os.mkdir("output")

        data = DataFrame({"Tweet": tweetan, "Dugaan Sentimen": sentimen})

        file_name, i = (
            f'output/{datetime.today().strftime("%Y-%m-%d")} - Jakarta Covid Tweet Sentiment Analysis',
            1,
        )
        while os.path.isfile(file_name + ".csv"):
            file_name = f'output/{datetime.today().strftime("%Y-%m-%d")} - Jakarta Covid Tweet Sentiment Analysis ({i})'
            i += 1

        data.to_csv(file_name + ".csv", index=False)
        print('\n[INFO] : Exported to "output" folder')
