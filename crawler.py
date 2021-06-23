import argparse, os, tweepy
import pandas as pd
from datetime import datetime
from config import CONFIG

def to_csv(tweetan, tanggal, teks, Id, sn, source, rtc, rts, hashtag):
    """Mengeksport data menjadi file csv

    Args:
        tweetan (list): List yang berisi tweet -  tweet yang telah di crawl
        tanggal (list): List tanggal saat tweet / retweet di buat
        teks (list): List yang berisi text / context dari tweet
        Id (list): List yang berisi ID pengguna
        sn (list): List yang berisi Screen name pengguna
        source (list): List yang berisi source / device yang digunakan oleh pengguna
        rtc (list): List yang berisi banyak retweet
        rts (list): List yang menunjukkan apakah post retweet atau bukan
        hashtag (bool): List yang berisi list dari hashtag yang digunakan di dalam sebuah tweet
    """
    data = pd.DataFrame({
        'Tanggal': tanggal,
        'Tweets': teks,
        'ID': Id,
        'Screen Name': sn,
        'Banyak Retweet': rtc,
        'Source': source,
        'Retweet Status': rts,
        'Hashtags': hashtag
    })

    file_name, i = f'output/Crawl Twitter Jakarta {datetime.today().strftime("%Y-%m-%d")}', 1
    while os.path.isfile(file_name + '.csv'):
        file_name = f'output/Crawl Twitter Jakarta {datetime.today().strftime("%Y-%m-%d")} ({i})'
        i += 1
    data.to_csv(file_name + '.csv', index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script untuk melakukan crawling \
                                                  tweet terbaru mengenai corona")
    parser.add_argument("-n",
                        "--number",
                        help="Banyak tweet yang akan di crawl.",
                        type=int, 
                        required = True)
    args = parser.parse_args()

    # Key
    config = CONFIG('CONFIG.json').data
    consumer_key = config['TWEETER-API']['consumer_key']
    consumer_secret = config['TWEETER-API']['consumer_secret']
    access_token = config['TWEETER-API']['access_token']
    access_token_secret = config['TWEETER-API']['access_token_secret']

    # Auth & API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Lists
    tweetan=[]
    tanggal=[]
    teks=[]
    Id=[]
    sn=[]
    source=[]
    rtc=[]
    rts=[]
    hashtag =[]

    # Crawl using tweepy
    for tweet in tweepy.Cursor(api.search, q=config['SEARCH-PLAN']['query'], tweet_mode='extended', 
                                count = 200, geocode=config['SEARCH-PLAN']['geocode'],
                                lang = "id").items(args.number):
        # Appends 
        tweetan.append(tweet)
        tanggal.append(tweet.created_at) 
        teks.append(tweet.full_text.encode("utf-8"))
        Id.append(tweet.id)
        sn.append(tweet.user.screen_name)
        source.append(tweet.source)
        rtc.append(tweet.retweet_count)
        hashtag.append([x['text'] for x in tweet.entities['hashtags']])
        if 'RT' in tweet.full_text :
            rts.append(1)
        else :
            rts.append(0)
        
        # Logging
        text = tweet.full_text
        if len(text) > 65:
            text = text[:65] + '...'
        print(f'{len(Id)} : {tweet.created_at} : {repr(text)}')

    # Check if output directory is available
    if not os.path.isdir('output'):
        os.mkdir('output')

    # Export
    to_csv(tweetan, tanggal, teks, Id, sn, source, rtc, rts, hashtag)