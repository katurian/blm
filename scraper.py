
from setup import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()

def getCityGeocode(city, radius_km):
    geolocator = Nominatim(user_agent="BLM")
    location = geolocator.geocode(city)
    geocode = f'{location.latitude},{location.longitude},{radius_km}km'
    return geocode

def getTweetsInHashtag(query, count, geocode):
    tweets = tweepy.Cursor(api.search, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, q=f'{query} -filter:retweets', geocode=geocode, tweet_mode='extended', rpp=100).items(count)
    data = [{'tweet_id':tweet.id_str, 'handle':tweet.author.screen_name, 'created_at':tweet.created_at, 'author_loc':tweet.author.location, 'retweet_count':tweet.retweet_count,
             'text':tweet.full_text,} for tweet in tweets if 'RT' not in tweet.full_text]
    data = json.dumps(data, default=default)
    return data
 
def getAccountTweets(handle):
    tweets = []  
    new_tweets = api.user_timeline(screen_name = handle, tweet_mode='extended', wait_on_rate_limit=True, wait_on_rate_limit_notify=True, count=200)
    tweets.extend(new_tweets)
    oldest = tweets[-1].id - 1
    
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name = handle, tweet_mode='extended', wait_on_rate_limit=True, wait_on_rate_limit_notify=True, count=200, max_id=oldest)
        tweets.extend(new_tweets)
        oldest = tweets[-1].id - 1

    data = [{'tweet_id':tweet.id_str, 'handle':tweet.author.screen_name, 'created_at':tweet.created_at, 'author_loc':tweet.author.location, 'retweet_count':tweet.retweet_count,
             'text':tweet.full_text,} for tweet in tweets]

    data = json.dumps(data, default=default)
    return data

data = getTweetsInHashtag('#ChicagoRiots', 50, getCityGeocode('Chicago, IL', 100))

with open('blm_chicagoriots_2020.json', 'w') as file:
    file.write(data)

data = getAccountTweets('realdonaldtrump')
with open('account_example.json', 'w') as file:
    file.write(data)
