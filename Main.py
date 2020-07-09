import sys
import tweepy
import Analizer as ana
from pandas import DataFrame
from get_API import *

# ARG
arg = sys.argv
n, export = True, False
if len(arg) > 1:
    n = int(arg[1])
    if len(arg) > 2:
        export = True if arg[2].lower() == 'true' else False

print(f'[INFO] Running on N : {n} & Export : {export}')

# Key
consumer_key, consumer_secret, access_token, access_token_secret = API().get()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
query = '#corona OR covid OR Covid19 OR #DiRumahAja OR #quarantine OR Corona OR DiRumahAja OR wabah OR pandemi OR quarantine'

# List
tweetan, sentimen = [], []

# Geocode Jakarta
for tweet in tweepy.Cursor(api.search, q=query, tweet_mode='extended', count = 200, geocode ='-6.213621,106.832673,20km',
                            lang = "id").items(n):
                            print(tweet.full_text, ana.analis(tweet.full_text))
                            tweetan.append(tweet.full_text)
                            sentimen.append(ana.analis(tweet.full_text))

# Export
if export:
    data = DataFrame({'Tweet' : tweetan, 'Dugaan Sentimen' : sentimen})
    data.to_csv('Output/Output.csv', index=False)
    print('[INFO] : Export to Output\Output.csv')