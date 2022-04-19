# Analisis Sentimen Twitter Corona DKI Jakarta

![](https://img.shields.io/badge/Made%20with-Python-green?style=flat&logo=Python)
[![](https://img.shields.io/badge/Notebook-disini-orange?style=flat&logo=Jupyter)](./notebook)
[![](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://www.linkedin.com/in/wahyu-setianto/)

UTS Big Data : Analisis Sentimen Twitter untuk mengetahui Dampak dari Pandemi COVID-19 terhadap
masyarakat Jakarta menggunakan TF-IDF Vectorizer &amp; SVM

<img src="assets/Wordcloud.png"
     alt="wordcloud"
     style="display:block;float:none;margin-left:auto;margin-right:auto;width:70%" />

## Run on Local

### 1. Clone repository ini

Clone/download repo ini. Anda dapat menggunakan `git` untuk melakukan hal ini.
Buka terminal dan run code berikut

```
git clone https://github.com/Hyuto/Analisis-Sentimen-Corona-DKI-Jakarta.git
```

Anda juga dapat mendownload repo ini dengan klik tombol `code` (pojok kanan atas) dan pilih
`Download ZIP` untuk mendowload repo ini sebagai ZIP file lalu extract file tersebut.

Selanjutnya anda bisa langsung `cd` ke-main directory.

```
cd Analisis-Sentimen-Corona-DKI-Jakarta
```

### 2. Setup virtual environment

Tahap selanjutnya adalah setup `virtualenv`.

| OS      | Command               |
| ------- | --------------------- |
| Linux   | `python3 -m venv env` |
| windows | `py -m venv env`      |

### 3. Install Requirements

Tahap selanjutnya adalah install library yang dibutuhkan.

| OS      | Command                                        |
| ------- | ---------------------------------------------- |
| Linux   | `pip install -r requirements.txt`              |
| windows | `py -m pip install --user -r requirements.txt` |

### 4. Twitter API

Edit `config.json` menggunakan kode yang didapat dari pihak twitter. Jika belum memiliki API anda
bisa mengunjungi [Twitter Dev App](https://developer.twitter.com/en/apps) untuk mengajukan
application.

Contoh :

`config.json`

```json
{
   "TWITTER-API": {
      consumer_key: "2NBRV4vm#################",
      consumer_secret: "jVe6ujjn7yqc6mZmHqHxOqS###################",
      access_token: "as254as1das2######################",
      access_token_secret: "asd214wq4g4r4y2t6####################"
   },

   ...
}
```

### 5. Running scripts

1. Crawl Twitter menggunakan `tweepy`<br>
   Melakukan crawling tentang `covid` pada user tweeter yang berada diwilayah DKI Jakarta.
   Anda dapat melakukan running pada `crawler.py` dengan menambahkan argumen `n` atau banyaknya
   data yang akan di ambil. Contoh :

   | OS      | Command                     |
   | ------- | --------------------------- |
   | Linux   | `python crawler.py -n 1000` |
   | windows | `py crawler.py -n 1000`     |

2. Sentiment Analisis<br>
   Melakukan sentimen analisis menggunakan model yang sudah di train sebelumnya. Anda dapat
   melakukan running pada `main.py` dengan menambahkan beberapa argumen seperti:

   - `n` : Banyaknya data yang akan dicrawl
   - `-e` : Export data menjadi file `csv` [OPTIONAL]

   Contoh :

   | OS      | Command                                                   |
   | ------- | --------------------------------------------------------- |
   | Linux   | `python main.py -n 1000` atau `python main.py -n 1000 -e` |
   | windows | `py main.py -n 1000` atau `py main.py -n 1000 -e`         |

## Magic `config.json`

Kustomisasi dapat dilakukan dengan mengedit `config.json`

1. `"TWITTER-API"` : Bagian wajib yang harus diisi dengan key yang telah anda dapatkan dari pihak
   tweeter.
2. `"VECTORIZER"` : Bagian yang mencangkup `path` atau letak file pickle vectorizer yang telah
   dilakukan _fitting_ untuk diload.
3. `"MODEL"` : Bagian yang mencangkup `path` atau letak file pickle model yang telah dilatih untuk
   diload. **Note** : Terdapat beberapa model yang telah dilatih di dalam folder `model`
4. `"SEARCH-PLAN"` : Bagian yang mengatur pencarian/crawling tweet.
   - `"query"` : Query pencarian tweet. Tweet yang dicari akan mengandung kata - kata yang terdapat
     dalam `query`
   - `"geocode"` : Geocode/letak tweet yang akan dicari dalam format `"longitude,latitude,jari-jari"`

## Convert model to `onnx`

Convert trained model using `skl2onnx` and run model anda dimana saja. Ubah _path_ pada
`"VECTORIZER"` dan `"MODEL"` dalam `config.json` ke custom model yang sudah dilatih.

```json
...
"VECTORIZER": {
   "path": "path/to/custom-tfidf.pickle"
},

"MODEL": {
   "path": "path/to/custom-model.pickle"
},
...
```

Selanjutnya jalankan `onnx-converter.py`.

```bash
python onnx-converter.py
```

Anda dapat menambahkan argumen `--split` untuk memisahkan _tf-idf_ dengan _main-model_ agar masing -
masing menjadi file _onnx_ yang independen.

## Note

Jika terdapat error pada pengimportan library `nltk` run script `nltk-handler.py`

| OS      | Command                  |
| ------- | ------------------------ |
| Linux   | `python nltk-handler.py` |
| windows | `py nltk-handler.py`     |
