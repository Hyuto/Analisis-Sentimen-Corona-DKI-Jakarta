import tweepy, sys, os
import pandas as pd
from datetime import datetime
from API import API

def to_csv(tweetan, tanggal, teks, Id, sn, source, rtc, rts, hashtag):
    # To CSV
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
    n = int(sys.argv[1])

    # Key
    api = API().data
    consumer_key = api['consumer_key']
    consumer_secret = api['consumer_secret']
    access_token = api['access_token']
    access_token_secret = api['access_token_secret']

    # Auth & API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    # Query
    query = '#corona OR covid OR Covid19 OR #DiRumahAja OR #quarantine OR Corona OR DiRumahAja OR wabah OR pandemi OR quarantine'

    # List
    tweetan=[]
    tanggal=[]
    teks=[]
    Id=[]
    sn=[]
    source=[]
    rtc=[]
    rts=[]
    hashtag =[]

    # Crawl ~ Crawl
    for tweet in tweepy.Cursor(api.search, q=query, tweet_mode='extended', count = 200, geocode ='-6.213621,106.832673,20km',
                                lang = "id").items(n):
        print(tweet.created_at, tweet.full_text)
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
        print(len(Id))

    if not os.path.isdir('output'):
        os.mkdir('output')

    # Export to json
    data_json = pd.DataFrame(tweetan)
    data_json.to_json(f'output/Crawl Twitter Jakarta {datetime.today().strftime("%Y-%m-%d")}.json')

    # Export to csv
    to_csv(tweetan, tanggal, teks, Id, sn, source, rtc, rts, hashtag)