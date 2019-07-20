import tweepy
from pathlib import Path
import pandas as pd
import os

consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_TOKEN')
access_token_secret = os.environ.get('TWITTER_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline(count=200, tweet_mode="extended")

df = pd.DataFrame.from_records([tweet._json for tweet in public_tweets])
df.created_at = pd.to_datetime(df.created_at)
df["date"] = df.created_at.apply(lambda x: x.date())
dates = df.date.unique()

for i in dates:
    my_file = Path("data/" + "tweets_" + str(i) + ".pickle")
    if my_file.is_file():
        temp_read = pd.read_pickle(my_file)
        new_dump = pd.merge(temp_read, df[df.date == i], on="id")
        new_dump.to_pickle(my_file)
    else:
        df[df.date == i].to_pickle(my_file)