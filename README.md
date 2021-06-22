# Analisis Sentimen Twitter Corona DKI Jakarta

UTS Big Data : Analisis Sentimen Twitter untuk mengetahui Dampak dari Pandemi COVID-19 terhadap masyarakat Jakarta menggunakan TF-IDF Vectorizer &amp; SVM

<img src="assets/Wordcloud.png"
     alt="wordcloud"
     style="display:block;float:none;margin-left:auto;margin-right:auto;width:70%" />

## Run on Local

<hr />

### 1. Clone repository ini

Clone / download repo ini. Anda dapat menggunakan `git` untuk melakukan hal ini. Buka terminal dan run code berikut

```
git clone https://github.com/Hyuto/Analisis-Sentimen-Corona-DKI-Jakarta.git
```

Anda juga dapat mendownload repo ini dengan klik tombol code (pojok kanan atas) dan pilih `Download ZIP` untuk mendowload repo ini sebagai ZIP file lalu extract file tersebut.

Selanjutnya anda bisa langsung `cd` ke-main directory.

```
cd Analisis-Sentimen-Corona-DKI-Jakarta
```

### 2. Install Requirements

Tahap selanjutnya adalah install library yang dibutuhkan.

| OS | Command |
| -- | ------- |
| Linux | `pip install -r requirements.txt` |
| windows | `py -m pip install --user -r requirements.txt` |

### 2. Twitter API

Edit `API.json` menggunakan kode yang didapat dari pihak twitter. Jika belum memiliki API anda bisa mengunjungi [Twitter Dev App](https://developer.twitter.com/en/apps) untuk mengajukan application.

Contoh :

`API.json`

```json
{
     consumer_key: "2NBRV4vm#################",
     consumer_secret: "jVe6ujjn7yqc6mZmHqHxOqS###################",
     access_token: "as254as1das2######################",
     access_token_secret: "asd214wq4g4r4y2t6####################"
}
```

### 3. Running scripts

1. Crawl Twitter menggunakan `tweepy`<br>
   Melakukan crawling tentang `covid` pada user tweeter yang berada diwilayah DKI Jakarta. Anda dapat melakukan running pada `crawler.py` dengan menambahkan argumen `N` atau banyaknya data yang akan di ambil. Contoh :

   | OS | Command |
   | -- | ------- |
   | Linux | `python crawler.py 1000` |
   | windows | `py crawler.py 1000` |

2. Sentiment Analisis<br>
   Melakukan sentimen analisis menggunakan model yang sudah di train sebelumnya. Anda dapat melakukan running pada `main.py` dengan menambahkan beberapa argumen seperti:

   * `N` : Banyaknya data yang akan dicrawl
   * `-e` : Export data menjadi file `csv` [OPTIONAL]
   
   Contoh :

   | OS | Command |
   | -- | ------- |
   | Linux | `python main.py 1000` atau `python main.py 1000 -e` |
   | windows | `py main.py 1000` atau `py main.py 1000 -e` |

## Note

Jika terdapat error pada pengimportan library `nltk` run script `nltk-handler.py`

| OS | Command |
| -- | ------- |
| Linux | `python nltk-handler.py` |
| windows | `py nltk-handler.py` |