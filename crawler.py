import tweepy, sys, os
import pandas as pd
from datetime import datetime
from API import API

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
    data.to_csv(f'output/Crawl Twitter Jakarta {datetime.today().strftime("%Y-%m-%d")}.csv', index=False)

if __name__ == '__main__':
    try:
        n = int(sys.argv[1])
    except:
        raise KeyError('Harus menspesifikasikan "N" (Banyaknya data yang akan dicrawl)')

    # Key
    api = API('API.json').data
    consumer_key = api['consumer_key']
    consumer_secret = api['consumer_secret']
    access_token = api['access_token']
    access_token_secret = api['access_token_secret']

    # Auth & API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Query
    query = '#corona OR covid OR Covid19 OR #DiRumahAja OR #quarantine OR Corona OR DiRumahAja OR wabah OR pandemi OR quarantine'

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
    for tweet in tweepy.Cursor(api.search, q=query, tweet_mode='extended', count = 200, geocode ='-6.213621,106.832673,20km',
                                lang = "id").items(n):
        # Logging
        print(tweet.created_at, tweet.full_text)

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
        
        # Count Logging
        print(f'Tweet count : {len(Id)}')

    # Check if output directory is available
    if not os.path.isdir('output'):
        os.mkdir('output')

    # Export to json
    data_json = pd.DataFrame(tweetan)
    data_json.to_json(f'output/Crawl Twitter Jakarta {datetime.today().strftime("%Y-%m-%d")}.json')

    # Export to csv
    to_csv(tweetan, tanggal, teks, Id, sn, source, rtc, rts, hashtag)