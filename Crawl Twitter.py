import tweepy
import pandas as pd

#Bu Selly
consumer_key = 'wU2srXqhIlZEHPUNRn71Ligs9'
consumer_secret = 'BAdzrCvTmunLHENsjWX91DK6G31Hsx622hL3LDWmbZnFIK9gtM'
access_token = '110120311-sD6JPWSdPv45TlIHvD0zQIgRMYMcCZSX8vXCnwno'
access_token_secret = '9YTWxh5rS9PqX0eh3BbyAOolFVRTEBMOBB22OgGIWFjrO'

#Rizky
consumer_key = '2xPzS0XSEIdpyiI65o9uABjro'
consumer_secret = 'ChMPw04zMTX12sv1amYcced8sF6rmlAFqzM5nMkGOWlXbcMG3z'
access_token = '51395041-xBkiyOCZrY2xHXnR08EszW4aVUM4SU85KqrB6beEC'
access_token_secret = 'DxzSengsN9V8j8bLuUHsP73Z8bj39aEL9MqSP3FD39KJS'

#Wahyu
consumer_key = '2NBRV4vmmVeimyznPpFPMNVTc'
consumer_secret = 'jVe6ujjn7yqc6mZmHqHxOqSUz4S7o4rEuVHl6p3yqdK2PJcpvE'
access_token = '1240469132551708672-9d23s1S9oQpJWOpeV9aMJ9VT2Gdpf8'
access_token_secret = 'uuZQhai6FuCLBsRAFnOOlMMvLCbsz04BFHPBZeJhdtxdS'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
query = '#corona OR covid OR Covid19 OR #DiRumahAja OR #quarantine OR Corona OR DiRumahAja OR wabah OR pandemi OR quarantine'
#'Corona' or 'DiRumahAja' or 'wabah' or 'pandemi' or 'quarantine'

#List
tweetan=[]
tanggal=[]
teks=[]
Id=[]
sn=[]
source=[]
rtc=[]
rts=[]
hashtag =[]

for tweet in tweepy.Cursor(api.search, q=query, tweet_mode='extended', count = 200, geocode ='-6.213621,106.832673,20km',
                            lang = "id",until = '2020-04-28',since = '2020-04-27').items():
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


#To Json
data_json = pd.DataFrame(tweetan)
data_json.to_json('Crawling Twitter 4.json')

#To_CSV
data = pd.DataFrame()
data['Tanggal']=tanggal
data['Tweets']=teks
data['ID']=Id
data['Screen Name']=sn
data['Banyak Retweet']=rtc
data['Source']=source
data['Retweet Status']=rts
data['Hashtags'] = hashtag
data.to_csv('Crawling Twitter Jakarta Baru 27.csv',index=False)