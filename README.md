# Analisis Sentimen Twitter Corona DKI Jakarta

UTS Big Data : Analisis Sentimen Twitter untuk mengetahui Dampak dari Pandemi COVID-19 terhadap masyarakat Jakarta menggunakan TF-IDF Vectorizer &amp; Random Forest Classifier

Json data : [Here](https://drive.google.com/drive/folders/1Ye6a_u68oq8Hw6NZuZuQ4sQLKogfrXnP?usp=sharing")

<img src="Wordcloud.png"
     alt="Markdown Monster icon"
     style="display:block;float:none;margin-left:auto;margin-right:auto;width:80%" />


## Usage

<hr />

### 1. Install Requirements

Cd ke direktori & run pada cmd anda.

```
pip install --user -r requirements.txt
```

### 2. Twitter API

Masukkan API yang sudah di dapat dari pihak twitter ke API.txt. Jika belum memiliki API anda bisa mengunjungi <a href ="https://developer.twitter.com/en/apps">Twitter Dev App</a> untuk pengajuan API-nya.
<br>
Contoh :<br>
<strong>API.txt</strong>
```
consumer_key = "2NBRV4vm#################"
consumer_secret = "jVe6ujjn7yqc6mZmHqHxOqS###################"
access_token = "as254as1das2######################"
access_token_secret = "asd214wq4g4r4y2t6####################"
```
<p style="font-size : 10pt">Note : Isi ruang diantara dua kutip(").</p>

### 3. Run ~ run ~
### <strong>Crawl Twitter</strong><br>
Arg : Banyak Tweet target. `python Crawl_Twitter.py N`<br>
<strong>Contoh</strong>
```
python Crawl_Twitter.py 100000
```
<p style="font-size : 10pt">Note : Jika N tidak dispesifikasikan maka program akan memasuki endless loop.</p>

### <strong>Main</strong><br>
Run dengan default option.
* N (Banyak Tweet) = `True` ~ Endless loop
* Export = False
```
python Main.py
```
Set banyak tweet dan Export. `python Main.py N EXPORT`<br>
<strong>Contoh</strong>
```
python Main.py 1000 True
```