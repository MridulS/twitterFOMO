## twitterFOMO

Don't want to spend hours scrolling away on Twitter but also feel that your feed
is important to keep up with updates (fear of missing out).

Setup a cron job to send you daily updates of your Twitter feed in your inbox.

No more scrolling away!!

Currently it sends you tweets in the format
```
tweet text - user_name - link_to_tweet

tweet text - user_name - link_to_tweet

tweet text - user_name - link_to_tweet

```

#### Quick Setup

The scripts works with Python 3, and assumes you have a server/computer which takes care of running the python script.

You would need API keys from Twitter(to get tweets) and Sendgrid(to send the email) for authentication.

Create a twitter dev account: https://developer.twitter.com/en/application/use-case

Sendgrid: https://sendgrid.com/docs/for-developers/sending-email/api-getting-started/

Clone the repo on your server/computer, create a directory to hold the data and install requirements.

```
$ git clone https://github.com/MridulS/twitterFOMO/
$ cd twitterFOMO
$ mkdir data
$ pip install -r requirements.txt
```

Edit the config file `config.env` to store your API keys and email address.

```
export SENDGRID_API_KEY='YOUR_API_KEY'
export TWITTER_CONSUMER_KEY='TWITTER_CONSUMER_KEY_FROM_YOUR_TWITTER_APP'
export TWITTER_CONSUMER_SECRET='TWITTER_CONSUMER_SECRET_FROM_YOUR_TWITTER_APP'
export TWITTER_TOKEN='TWITTER_TOKEN_FROM_YOUR_TWITTER_APP'
export TWITTER_TOKEN_SECRET='TWITTER_TOKEN_SECRET_FROM_YOUR_TWITTER_APP'
export FROM_EMAIL="YOUR_EMAIL"
export TO_EMAIL="TO_EMAIL"
export FETCH=6
```
Run the config file to load in your API keys.
```
source ./config.env
```

[Email at 01:00 server time, and fetch twitter updates every 6 hours. Change it to hourly (`FETCH=1`) if you follow a LOT of people, as the API restricts to last 200 tweets on your homepage]





