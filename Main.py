import sys, os, re, string, pickle
import tweepy
from pandas import DataFrame
from API import API
from datetime import datetime
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Create Sastrawi stemmer
STEMMER = StemmerFactory().create_stemmer()

# Create Stopword
with open("kamus/Stopword.txt", "r") as f:
    STOPWORDS = f.readline().split()

# Cleanner 
def cleaning(text):
    text= text[2:]
    text = text.replace('\\n',' ')
    return text

# Preprocessor
def preprocessor(text):
    # Convert to lower case
    text = text.lower()
    # Remove additional code
    text = text.replace('\\xe2\\x80\\xa6', '')
    # Convert www.* or https?://* to URL
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',text)
    # Convert @username to AT_USER
    text = re.sub('@[^\s]+','',text)
    # Remove additional white spaces
    text = re.sub('[\s]+', ' ', text)
    # Replace #word with word
    text = re.sub(r'#([^\s]+)', r'\1',text)
    # Menghapus angka dari teks
    text = re.sub(r"\d+", "", text)
    # Menganti tanda baca dengan spasi
    text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    return text

# Tokenizer
def tokenizer(text):
    words = word_tokenize(text)
    tokens=[]
    for w in words:
        # add tokens
        if len(w) > 3:
            w = STEMMER.stem(w)
            tokens.append(w.lower())
    return tokens

# Load saved vectorizer
vectorizer_tfidf = pickle.load(open('model/vectorizer/vectorizer_tfidf.pickle', 'rb'))

# Load Model
model = pickle.load(open('model/[TRAINED] Random Forest Classifier.pickle', 'rb'))

def analyst(string) :
    """ Analyst """
    string = cleaning(string)
    string = preprocessor(string)
    string = tokenizer(string)
    
    string = vectorizer_tfidf.transform(string)

    print(model.predict(string))

def args_prep(args):
    """ Preprocess args """
    # Set n to true : Infinite Loop
    # and export to false
    export, n = False, None

    # Jika ada argumen lakukan preprocess
    # n arg ada di posisi pertama
    # export arg adalah '-e'
    if args:
        if args[0].isdigit():
            n = int(args[0])
        else:
            raise KeyError('Invalid argumen N')

        args = list(map(lambda x : x.lower(), args))

        if '-e' in args:
            export = True
    else:
        raise KeyError('Harus memasukkan N (banyak data yang akan di crawl) \
                        \nContoh : python main.py 1000 -e')
    
    return n, export

if __name__ == '__main__':
    # Arguments
    args = sys.argv[1:]
    n, export = args_prep(args)

    print(f'[INFO] Running on N : {n} & Export : {export}')

    # Tweeter API
    api = API('API.json').data
    consumer_key = api['consumer_key']
    consumer_secret = api['consumer_secret']
    access_token = api['access_token']
    access_token_secret = api['access_token_secret']

    # Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Data : tweet & sentiment
    tweetan, sentimen = [], []

    # Search / crawl. Plan :
    # - query : Hal yang berhubungan dengan covid
    # - geocode : Jakarta; pusat : (-6.213621, 106.832673) , jari - jari : 20 km
    query = '#corona OR covid OR Covid19 OR #DiRumahAja OR #quarantine OR Corona \
             OR DiRumahAja OR wabah OR pandemi OR quarantine'
    for tweet in tweepy.Cursor(api.search, q=query, tweet_mode='extended', 
                                count = 200, geocode ='-6.213621,106.832673,20km',
                                lang = "id").items(n):
        s = analyst(tweet.full_text)
        tweetan.append(tweet.full_text)
        sentimen.append(s)
        
        # Logging
        text = tweet.full_text
        if len(text) > 77:
            text = text[:77] + '...'
        print(f'{repr(text)} : {s}')

    # Export
    if export:
        if not os.path.isdir('output'):
            os.mkdir('output')

        data = DataFrame({'Tweet' : tweetan, 'Dugaan Sentimen' : sentimen})
        data.to_csv(f'output/{datetime.today().strftime("%Y-%m-%d")} - Jakarta' + 
                     ' Covid Tweet Sentiment Analysis.csv', index=False)
        print('[INFO] : Exported to "output" folder')