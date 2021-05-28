import sys, os
import tweepy
import analizer as ana
from pandas import DataFrame
from API import API
from datetime import datetime

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
        s = ana.analyst(tweet.full_text)
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