import Analizer as ana
import tweepy

consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
# query = '#corona OR covid OR Covid19 OR #DiRumahAja OR #quarantine OR Corona OR DiRumahAja OR wabah OR pandemi OR quarantine'

# Geocode Jakarta
for tweet in tweepy.Cursor(api.search, q="*", tweet_mode='extended', count = 200, geocode ='-6.213621,106.832673,20km',
                            lang = "id").items(10):
                            print(tweet.full_text, ana.analis(tweet.full_text))
