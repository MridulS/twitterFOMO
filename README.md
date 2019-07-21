### twitterFOMO

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

The scripts works with Python 3, and assumes you have a server/computer which takes care of running the cron jobs.

You would need API keys from Twitter(to get tweets) and Sendgrid(to send the email) for authentication.

Create a twitter dev account -> https://developer.twitter.com/en/application/use-case

Sendgrid setup -> https://sendgrid.com/docs/for-developers/sending-email/api-getting-started/

Clone the repo on your server/computer, create a directory to hold the data and install requirements.

```
$ git clone https://github.com/MridulS/twitterFOMO/
$ cd twitterFOMO
$ mkdir data
$ pip install -r requirements.txt
```

Also add API keys to your bash profile, use `export` or hardcode your API keys in the scripts.

```
$ export SENDGRID_API_KEY='YOUR_API_KEY'
$ export TWITTER_CONSUMER_KEY='TWITTER_CONSUMER_KEY_FROM_YOUR_TWITTER_APP'
$ export TWITTER_CONSUMER_SECRET='TWITTER_CONSUMER_SECRET_FROM_YOUR_TWITTER_APP'
$ export TWITTER_TOKEN='TWITTER_TOKEN_FROM_YOUR_TWITTER_APP'
$ export TWITTER_TOKEN_SECRET ='TWITTER_TOKEN_SECRET_FROM_YOUR_TWITTER_APP'
```

Change the `from_email` and `to_emails` in `send_email.py` to your email.

Setup cron jobs using `crontab -e` and add the following to the file
```
1 0 * * * Path_to/python3 Path_to/twitterFOMO/send_email.py >> Path_to/cron.log 2>&1
0 1,7,13,19 * * * Path_to/python3 Path_to/twitterFOMO/get_twitter_timeline.py >> Path_to/cron.log 2>&1
```

Note: if using virtual environments you need to take care of `Path_to/python3` in the cron jobs.

[Email at 00:01 server time, and fetch twitter updates at 01:00, 07:00, 13:00, 19:00. Make it hourly if you follow a LOT of people, as the API restricts to last 200 tweets on your homepage]

##### Troubleshoot

Quick Hack: To make sure the cron jobs are working change the time to current time + 5 mins for the `get_twitter_timeline.py` file and current time + 10 mins for `send_email.py` in `crontab` . If you don't get an email, first check spam folder and then check the `cron.log` file to see what went wrong.



