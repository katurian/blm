from setup import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()

def getCityGeocode(city, radius_km):
    geolocator = Nominatim(user_agent="BLM", timeout=10)
    location = geolocator.geocode(city)
    geocode = f'{location.latitude},{location.longitude},{radius_km}km'
    return geocode

def getTweetsInHashtag(query, count, geocode, since, until, filter_retweets):
    if (since == False) and (until == False):
        timeframe = ''
    else:
        timeframe = f'since:{since} until:{until}'
    if filter_retweets == False:
        retweets = ''
    else:
        retweets = 'filter:retweets'
    tweets = tweepy.Cursor(api.search, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, q=f'{query} {retweets} {timeframe}', geocode=geocode, tweet_mode='extended', rpp=100).items(count)
    data = [{'tweet_id':tweet.id_str, 'handle':tweet.author.screen_name, 'created_at':tweet.created_at, 'author_loc':tweet.author.location, 'retweet_count':tweet.retweet_count,
             'text':tweet.full_text,} for tweet in tweets]
    data = json.dumps(data, default=default)
    return data

def getHandles(query, count, geocode, since, until, filter_retweets):
    if (since == False) and (until == False):
        timeframe = ''
    else:
        timeframe = f'since:{since} until:{until}'
    if filter_retweets == False:
        retweets = ''
    else:
        retweets = 'filter:retweets'
    tweets = tweepy.Cursor(api.search, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, q=f'{query} {retweets} {timeframe}', geocode=geocode, tweet_mode='extended', rpp=100).items(count)
    data = [tweet.author.screen_name for tweet in tweets]
    data = list(set(data)) 
    return data

def findVisitors(all_handles, local_handles): 
    temp = set(local_handles) 
    visitors = [handle for handle in all_handles if handle not in local_handles] 
    return visitors

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

