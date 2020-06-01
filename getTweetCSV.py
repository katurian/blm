from setup import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def getCityGeocode(city, radius_km):
    geolocator = Nominatim(user_agent="BLM")
    location = geolocator.geocode(city)
    geocode = f'{location.latitude},{location.longitude},{radius_km}km'
    return geocode

def getTweetsInHashtag(query, count, geocode):
    tweets = tweepy.Cursor(api.search, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, q=query, geocode=geocode, tweet_mode='extended', rpp=100).items(count)
    data = [[tweet.author.screen_name, tweet.created_at, tweet.author.location, tweet.retweet_count, tweet.full_text.encode('utf-8')] for tweet in tweets if 'RT' not in tweet.full_text]
    return data

tweetsDF = pd.DataFrame(data=getTweetsInHashtag('#ChicagoRiots', 5000, getCityGeocode('Chicago, IL', 100)), columns = ['Handle', 'Date_Created', 'Bio_Loc', 'Retweet_Count', 'Text'])

tweetsDF.to_csv('blm_chicago_2020.csv', index=False)
