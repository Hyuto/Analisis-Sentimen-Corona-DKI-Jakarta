import tweepy
import pandas as pd

#Key
consumer_key = '##################################'
consumer_secret = '################################################'
access_token = '###################################################'
access_token_secret = '#############################################'

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
data_json.to_json('Dataset/Crawling Twitter 4.json')

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
data.to_csv('Dataset/Crawling Twitter Jakarta Baru 27.csv',index=False)
